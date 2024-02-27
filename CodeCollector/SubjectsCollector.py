import json
from Utils import *
from FetchManager import fetch_submission_code
from tqdm import tqdm

def filter_lang(submissions):
    filtered_submissions = []
    for submission in submissions:
        lang = submission["lang"]
        if lang in acceptedLangs:
            filtered_submissions.append(submission)
    return filtered_submissions
    
def find_pairs(submissions):
    authors_dict = {}
    for submission in filter_lang(submissions):
        author = submission["author"]
        if author not in authors_dict:
            authors_dict[author] = {"accepted": [], "rejected": []}
        
        if submission["verdict"]["isAccepted"]:
            authors_dict[author]["accepted"].append(submission)
        else:
            authors_dict[author]["rejected"].append(submission)

    pairs = []
    for author, submissions in authors_dict.items():
        for accepted in submissions["accepted"]:
            closest_rejected = None
            min_time_diff = float("inf")
            for rejected in submissions["rejected"]:
                if accepted["submissionTime"] > rejected["submissionTime"]:
                    time_diff = accepted["submissionTime"] - rejected["submissionTime"]
                    if time_diff < min_time_diff:
                        min_time_diff = time_diff
                        closest_rejected = rejected
            
            if closest_rejected:
                pairs.append([accepted, closest_rejected])
                break  # Only keep one pair per author

    return pairs

def convert_to_CFSubmission(submissions):
    cf_submissions = []
    for pair in submissions:
        cf_pair = []
        for submission in pair:
            verdict = Verdict(isAccepted=submission["verdict"]["isAccepted"],
                              errorType=submission["verdict"]["errorType"],
                              errorCase=submission["verdict"].get("errorCase"))
            cf_sub = CFSubmission(contestID=submission["contestID"],
                                  problem=submission["problem"],
                                  submissionID=submission["submissionID"],
                                  author=submission["author"],
                                  lang=submission["lang"],
                                  verdict=verdict,
                                  runTime=submission["runTime"],
                                  memory=submission["memory"],
                                  submissionTime=submission["submissionTime"])
            cf_pair.append(cf_sub)
        cf_submissions.append(cf_pair)
    return cf_submissions

def print_pairs(pairs):
    for pair in pairs:
        print(f"Pair for {pair[0].author}:")
        print(f"Accepted: {pair[0].submissionID}, Time: {pair[0].submissionTime}")
        print(f"Rejected: {pair[1].submissionID}, Time: {pair[1].submissionTime}")
        print()

def get_subject_from_pairs(cf_pairs):
    results = []
    for submission_pair in tqdm(cf_pairs):
        accepted_code = fetch_submission_code(submission_pair[0].contestID, submission_pair[0].submissionID)
        rejected_code = fetch_submission_code(submission_pair[1].contestID, submission_pair[1].submissionID)
        subject = CFSubject(acceptedSubmission=submission_pair[0],
                            rejectedSubmission=submission_pair[1],
                            acceptedCode=accepted_code,
                            rejectedCode=rejected_code)
        results.append(subject)
    return results

def getSubjects(contestID):
    submissions = read_submissions(contestID)
    pairs = find_pairs(submissions)
    cf_pairs = convert_to_CFSubmission(pairs)
    print_pairs(cf_pairs)
    return get_subject_from_pairs(cf_pairs)
    

