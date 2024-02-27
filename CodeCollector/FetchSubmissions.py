from Utils import *

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
from tqdm import tqdm

# Import the Verdict and CFSubmission classes here
# Assume they are defined as provided in the task description

def parse_verdict(text):
    if "Accepted" in text:
        return Verdict(True, Verdict.ErrorType.OTHER)
    elif "Wrong answer" in text:
        return Verdict(False, Verdict.ErrorType.ANSWER, int(text.split(' ')[-1]))
    elif "Compilation error" in text:
        return Verdict(False, Verdict.ErrorType.COMPILATION)
    elif "Runtime error" in text:
        return Verdict(False, Verdict.ErrorType.RUNTIME, int(text.split(' ')[-1]))
    elif "Time limit exceeded" in text:
        return Verdict(False, Verdict.ErrorType.TIME, int(text.split(' ')[-1]))
    else:
        return Verdict(False, Verdict.ErrorType.OTHER)

def parse_submission(tr):
    submission_id = tr['data-submission-id']
    time_str = tr.find('td', class_='status-small').text.strip()
    author = tr.find('td', class_='status-party-cell').a.text.strip()
    problem = tr.find('td', {'data-problemid': True}).a.text.strip()
    lang = tr.find('td', class_=None).text.strip()
    verdict_str = tr.find('td', class_='status-cell').span.text.strip()
    run_time = int(tr.find('td', class_='time-consumed-cell').text.strip().split('\xa0')[0])
    memory = int(tr.find('td', class_='memory-consumed-cell').text.strip().split('\xa0')[0])
    submission_time = datetime.strptime(time_str, '%b/%d/%Y %H:%M').timestamp()

    verdict = parse_verdict(verdict_str)
    return CFSubmission(contestID="1915", problem=problem, submissionID=submission_id, author=author, lang=lang, verdict=verdict, runTime=run_time, memory=memory, submissionTime=submission_time)

def fetch_submissions(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table_rows = soup.find('table', class_='status-frame-datatable').find_all('tr')[1:]  # skip header row
    with open('output.html','w') as f:
        f.write(str(table_rows))

    submissions = []
    for tr in table_rows:
        submission = parse_submission(tr)
        submissions.append(submission)
    return submissions

def save_submissions_to_json(submissions, filename=submissionsPath):
    submissions_dicts = [submission.to_dict() for submission in submissions]
    with open(filename, 'w') as file:
        json.dump(submissions_dicts, file, indent=4)


url_template = "https://codeforces.com/contest/1915/status/page/{page}?order=BY_JUDGED_DESC"
submissions = []
for page in tqdm(range(1, 7050)):  # 从1到7049
    url = url_template.format(page=page)
    page_submissions = fetch_submissions(url)
    submissions.extend(page_submissions)
    save_submissions_to_json(submissions)  # 保存当前的submissions到JSON文件