from Utils import *
from FetchManager import fetch_submissions
from SubjectsCollector import find_pairs, print_pairs, fetch_submission_code_error, randomGetFrom
from Comparator import compare_code_lines, recompareAll
from tqdm import tqdm
import os
import time
import threading
from concurrent.futures import ThreadPoolExecutor



if __name__ == "__main__":
    print("""options:
          1: fetch all submissions of given contest
          2: get Subjects from fetched submission, and fetch code for them (multi-thread)
          3: single thread ver of 2 (Suggested! will sleep & retry in case 403 happen)
          4: compare subject codes & update errorLine and bugType attribute
          5: randomly get subject from stored subjects
          command: get runPy command
          """)
    option = input("option?= ")
    default_contestID = 1915
    if (option == "1"):
        # fetch all submissions of the below contest
        contestID = input("contestID=")
        if contestID=='':
            contestID = default_contestID
        
        url_template = "https://codeforces.com/contest/{contestID}/status/page/{page}?order=BY_ARRIVED_DESC"
        startPage = 1
        
        if os.path.exists(get_submission_csv_name(contestID)):
            submissions = CFSubmission.read_from_csv(contestID)
            len = len(submissions)
            startPage = len//50 + 1
            print(f"imported {len} entries, starting from page {startPage}")
            if (startPage == 7049 and len/50 - len//50 > 0):
                startPage = 7050
                colorPrint("INFO: contest already fully fetched", "yellow")

            
        with ThreadPoolExecutor(max_workers=40) as executor:
            total = 7050-startPage
            pbar = tqdm(total=total)
            lock = threading.Lock()

            def task(url):
                submissions = []
                page_submissions = fetch_submissions(url)
                if page_submissions != None:
                    submissions.extend(page_submissions)
                    with lock:
                        if os.path.exists(get_submission_csv_name(contestID)):
                            CFSubmission.append_to_csv(page_submissions, contestID)
                        else:
                            colorPrint('csv created!', 'green')
                            CFSubmission.save_to_csv(submissions, contestID)
                        pbar.update(1)
                else:
                    colorPrint('exit with error!', 'red')
                    # http error happenned
                    # TODO: auto wait 5min and redo
                    exit()
            for page in range(startPage, 7050):  # TODO: fetch page number
                url = url_template.format(page=page, contestID=contestID)
                executor.submit(task, url)
                time.sleep(0.1)

            

    elif (option == "2"):
        # fetch all submissions of the below contest
        contestID = input("contestID=")
        if contestID=='':
            contestID = default_contestID
        
        submissions = CFSubmission.read_from_csv(contestID)
        pairs = find_pairs(submissions)
        pairs_to_fetch = pairs.copy()
        print_pairs(pairs)
        subjects = []
        startPage = 1
        
        if os.path.exists(get_subject_json_name(contestID)):
            subjects = CFSubject.load_list_from_json(contestID)
            for pair in pairs:
                for subject in subjects:
                    if (pair[0].author == subject.acceptedSubmission.author):
                        pairs_to_fetch.remove(pair)
                    
            print(f"imported {len(pairs) - len(pairs_to_fetch)} subjects")

           
        with ThreadPoolExecutor(max_workers=2) as executor:
            lock = threading.Lock()
            pbar = tqdm(len(pairs_to_fetch))

            def task(submission_pair):
                accepted = fetch_submission_code_error(submission_pair[0].contestID, submission_pair[0].submissionID)
                rejected = fetch_submission_code_error(submission_pair[1].contestID, submission_pair[1].submissionID, submission_pair[1].errorCaseNo)

                if (accepted == None or rejected == None):
                    # TODO: auto wait 5min and redo
                    pass
                
                accepted_code = accepted[0]
                subject = CFSubject(acceptedSubmission=submission_pair[0],
                                    rejectedSubmission=submission_pair[1],
                                    acceptedCode=accepted_code,
                                    rejectedCode=rejected[0],
                                    failedTestCase=rejected[1],
                                    errorLine=compare_code_lines(accepted_code,rejected[0])[1]
                                    )
                with lock:
                    subjects.append(subject)
                    CFSubject.save_list_to_json(subjects, contestID)
                    pbar.update(1)
            
            for submission_pair in pairs_to_fetch:
                executor.submit(task, submission_pair)
                time.sleep(1)
    
        pass

    elif (option == "3"):
        # fetch all submissions of the below contest
        # single thread
        contestID = input("contestID=")
        if contestID=='':
            contestID = default_contestID
        
        submissions = CFSubmission.read_from_csv(contestID)
        pairs = find_pairs(submissions)
        pairs_to_fetch = pairs.copy()
        print_pairs(pairs)
        subjects = []
        startPage = 1
        
        if os.path.exists(get_subject_json_name(contestID)):
            subjects = CFSubject.load_list_from_json(contestID)
            for pair in pairs:
                for subject in subjects:
                    if (pair[0].author == subject.acceptedSubmission.author):
                        pairs_to_fetch.remove(pair)
                    
            print(f"imported {len(pairs) - len(pairs_to_fetch)} subjects")

        
        for submission_pair in tqdm(pairs_to_fetch):
            try:
                accepted = fetch_submission_code_error(submission_pair[0].contestID, submission_pair[0].submissionID)
                time.sleep(1)
                rejected = fetch_submission_code_error(submission_pair[1].contestID, submission_pair[1].submissionID, submission_pair[1].errorCaseNo)
            except Exception as e:
                colorPrint("Exception thrown during fetching, skipping...","yellow")
                continue
            if (accepted == None or rejected == None):
                # TODO: auto wait 5min and redo
                colorPrint("sleeping...","yellow")
                time.sleep(100)
                continue
            
            accepted_code = accepted[0]
            subject = CFSubject(acceptedSubmission=submission_pair[0],
                                rejectedSubmission=submission_pair[1],
                                acceptedCode=accepted_code,
                                rejectedCode=rejected[0],
                                failedTestCase=rejected[1],
                                errorLine=compare_code_lines(accepted_code,rejected[0])[1]
                                )
            subjects.append(subject)
            try:
                CFSubject.save_list_to_json(subjects, contestID)
            except Exception:
                colorPrint("Exception thrown during saving, skipping...","yellow")
                continue
    
        pass
    elif (option == "4"):
        contestID = input("contestID=")
        if contestID=='':
            contestID = default_contestID
        recompareAll(contestID)
        colorPrint("compare completed","yellow")
    elif (option == "5"):
        contestID = input("contestID=")
        if contestID=='':
            contestID = default_contestID
        subjects = CFSubject.load_list_from_json(contestID)
        randomGetFrom(subjects).print()
        
    else:
        fetch_submissions("https://codeforces.com/contest/1915/status?order=BY_ARRIVED_DESC")
        pass
