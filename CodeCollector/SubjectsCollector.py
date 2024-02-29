import json
from Utils import *
from FetchManager import fetch_submission_code_error
from tqdm import tqdm
from Comparator import compare_code_lines

def filter_lang(submissions):
    filtered_submissions = []
    for submission in submissions:
        lang = submission.lang
        if lang in acceptedLangs:
            filtered_submissions.append(submission)
    return filtered_submissions
    
def find_pairs(submissions):
    authors_dict = {}
    for submission in filter_lang(submissions):
        author = submission.author
        if author not in authors_dict:
            authors_dict[author] = {"accepted": [], "rejected": []}
        
        if submission.isAccepted:
            authors_dict[author]["accepted"].append(submission)
        else:
            authors_dict[author]["rejected"].append(submission)

    pairs = []
    for author, submissions in authors_dict.items():
        for accepted in submissions["accepted"]:
            closest_rejected = None
            min_time_diff = float("inf")
            for rejected in submissions["rejected"]:
                if accepted.submissionTime > rejected.submissionTime:
                    time_diff = accepted.submissionTime - rejected.submissionTime
                    if time_diff < min_time_diff:
                        min_time_diff = time_diff
                        closest_rejected = rejected
            
            if closest_rejected:
                pairs.append([accepted, closest_rejected])
                break  # Only keep one pair per author

    return pairs

def print_pairs(pairs):
    for pair in pairs:
        print(f"Pair for {pair[0].author}:")
        print(f"Accepted: {pair[0].submissionID}, Time: {pair[0].submissionTime}")
        print(f"Rejected: {pair[1].submissionID}, Time: {pair[1].submissionTime}")
        print()



    

