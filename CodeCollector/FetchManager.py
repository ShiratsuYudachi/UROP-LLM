import requests
from bs4 import BeautifulSoup
from datetime import datetime
from Utils import *

def fetch_submissions(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    if response.status_code == 200:
        table_rows = soup.find('table', class_='status-frame-datatable').find_all('tr')[1:]  # skip header row
        submissions = []
        for tr in table_rows:
            submission = parse_submission_html(tr)
            submissions.append(submission)
        return submissions
    else:
        colorPrint("HTTP Error: "+str(response.status_code), "red")
        return None

def parse_submission_html(tr):
        submission_id = tr['data-submission-id']
        time_str = tr.find('td', class_='status-small').text.strip()
        author = tr.find('td', class_='status-party-cell').a.text.strip()
        problem = tr.find('td', {'data-problemid': True}).a.text.strip()
        lang = tr.find('td', class_=None).text.strip()
        verdict_str = tr.find('td', class_='status-cell').span.text.strip()
        isAccepted = verdict_str=='Accepted'
        errorType = None
        errorCaseNo = 0
        if not isAccepted:
            if 'Compilation' in verdict_str:
                errorType = 'Compilation'
            elif 'Runtime' in verdict_str:
                errorType = 'Runtime'
            elif 'Time' in verdict_str:
                errorType = 'Time'
            elif 'Wrong' in verdict_str:
                errorType = 'Answer'
            else:
                errorType = verdict_str
            if errorType in ('Answer','Runtime','Time'):
                errorCaseNo = verdict_str.split(' ')[-1]
        run_time = int(tr.find('td', class_='time-consumed-cell').text.strip().split('\xa0')[0])
        memory = int(tr.find('td', class_='memory-consumed-cell').text.strip().split('\xa0')[0])
        submission_time = datetime.strptime(time_str, '%b/%d/%Y %H:%M').timestamp()

        return CFSubmission(contestID="1915", problem=problem, submissionID=submission_id, author=author, isAccepted=isAccepted, errorType=errorType, errorCaseNo=errorCaseNo, lang=lang, runTime=run_time, memory=memory, submissionTime=submission_time)

def myparser():
    response = requests.get()
    soup = BeautifulSoup(response.text, 'html.parser')
    if response.status_code == 200:
        submissions = []
        table_items = soup.find('datatable').find('table').find_all('td')
        def mystrip(item):
            return item.strip().replace('\n','').replace('\r','').replace(' ','')
        submission_id = mystrip(table_items[0].text)
        author = mystrip(table_items[1].text)
        problem = mystrip(table_items[2].text)
        lang = table_items[3].text.strip()
        verdict_str = table_items[4].text.strip().replace('\n','').replace('\r','')
        runTime = int(mystrip(table_items[5].text).strip('ms'))
        memory = int(mystrip(table_items[6].text).strip('KB'))
        time_str = table_items[7].text.strip()
        submission_time = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S').timestamp()

        isAccepted = verdict_str=='Accepted'
        errorType = None
        errorCaseNo = 0
        if not isAccepted:
            if 'Compilation' in verdict_str:
                errorType = 'Compilation'
            elif 'Runtime' in verdict_str:
                errorType = 'Runtime'
            elif 'Time' in verdict_str:
                errorType = 'Time'
            elif 'Wrong' in verdict_str:
                errorType = 'Answer'
            else:
                errorType = verdict_str
            if errorType in ('Compilation','Runtime','Time'):
                errorCaseNo = verdict_str.split(' ')[-1]
    
# fetch submission code and failed test case
def fetch_submission_code_error(contest_id, submission_id, errorCaseNo = None):
    # Build the URL from the given contest_id and submission_id
    url = f"https://codeforces.com/contest/{contest_id}/submission/{submission_id}"
    session = requests.Session()
    response = session.get(url)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the <pre> tag with the specific id containing the submission code
    code_pre_tag = soup.find('pre', id="program-source-text")
    
    # Extract the text from the <pre> tag, which is the submission code
    
    code = code_pre_tag.get_text()
    if not code:
        colorPrint("ERROR: Code Not Found in submission page")
        return

    errorCase = None

    # find failed test cases
    if errorCaseNo:
        meta_tag = soup.find('meta', attrs={'name': 'X-Csrf-Token'})
        if not meta_tag:
            colorPrint("ERROR: CSRF token Not Found in submission page")
            return
        csrf_token = meta_tag['content']
        submitSource_url = "https://codeforces.com/data/submitSource"
        headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "sec-ch-ua": "\"Not A(Brand\";v=\"99\", \"Google Chrome\";v=\"121\", \"Chromium\";v=\"121\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-csrf-token": csrf_token,
            "x-requested-with": "XMLHttpRequest",
            'Referer': url
        }
        data = {
            "submissionId": submission_id,
            "csrf_token": csrf_token
        }
        response = session.post(submitSource_url, headers=headers, data=data).json()
        errorCase = {
            'input': response[f'input#{errorCaseNo}'],
            'output': response[f'output#{errorCaseNo}'],
            'expectedOutput': response[f'answer#{errorCaseNo}'],
            'CheckerComment': response[f'checkerStdoutAndStderr#{errorCaseNo}']
        }

    
    return code, errorCase