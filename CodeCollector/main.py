from Utils import *
from FetchManager import fetch_submissions
from SubjectsCollector import getSubjects
from tqdm import tqdm
import os
import time


if __name__ == "__main__":
    print("""options:
          1: fetch all submissions of given contest
          2: get Subjects from fetched submission, and fetch code for them
          command: get runPy command
          """)
    option = input("option?= ")
    if (option == "1"):
        # fetch all submissions of the below contest
        default_contestID = 1915
        contestID = input("contestID=")
        if contestID=='':
            contestID = default_contestID
        
        url_template = "https://codeforces.com/contest/{contestID}/status/page/{page}?order=BY_ARRIVED_DESC"
        submissions = []
        startPage = 1
        if os.path.exists(get_submission_json_name(contestID)):
            submissionsDict = read_submissions(contestID)
            submissions = CFSubmission.parse_dict_list(submissionsDict)
            dictLen = len(submissionsDict)
            startPage = dictLen//50 + 1
            print(f"imported {dictLen} entries, starting from page {startPage}")
            if (startPage == 7049 and dictLen/50 - dictLen//50 > 0):
                startPage = 7050
                colorPrint("INFO: contest already fully fetched", "yellow")

        for page in tqdm(range(startPage, 7050)):  # TODO: fetch page number
            url = url_template.format(page=page, contestID=contestID)
            page_submissions = fetch_submissions(url)
            if page_submissions != None:
                submissions.extend(page_submissions)
                save_submissions(submissions, contestID)
            else:
                colorPrint('exit with error!', 'red')
                # http error happenned
                break
            time.sleep(2)

    elif (option == "2"):
        # fetch all submissions of the below contest
        default_contestID = 1915
        contestID = input("contestID=")
        if contestID=='':
            contestID = default_contestID
        getSubjects(contestID)
        pass
    else:
        # test branch
        pass
