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
        run_time = int(tr.find('td', class_='time-consumed-cell').text.strip().split('\xa0')[0])
        memory = int(tr.find('td', class_='memory-consumed-cell').text.strip().split('\xa0')[0])
        submission_time = datetime.strptime(time_str, '%b/%d/%Y %H:%M').timestamp()

        verdict = Verdict.parse_dict(verdict_str)
        return CFSubmission(contestID="1915", problem=problem, submissionID=submission_id, author=author, lang=lang, verdict=verdict, runTime=run_time, memory=memory, submissionTime=submission_time)


def fetch_submission_code(contest_id, submission_id):
    # Build the URL from the given contest_id and submission_id
    url = f"https://codeforces.com/contest/{contest_id}/submission/{submission_id}"

    # Make a request to the URL
    response = requests.get(url)
    
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the <pre> tag with the specific id containing the submission code
    code_pre_tag = soup.find('pre', id="program-source-text")
    
    # Extract the text from the <pre> tag, which is the submission code
    code = code_pre_tag.get_text() if code_pre_tag else "Code not found"
    
    return code

# TODO: test below
def fetch_error_test_case():
    url = "https://codeforces.com/data/submitSource"

# Headers as specified in the fetch request
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
        "x-csrf-token": "e72c792cf3bcca95c4647f0736be7c2a",
        "x-requested-with": "XMLHttpRequest"
    }

    # Data to be sent with the request
    data = {
        "submissionId": "248602789",
        "csrf_token": "e72c792cf3bcca95c4647f0736be7c2a"
    }

    # Sending the POST request
    response = requests.post(url, headers=headers, data=data)

    # Assuming the response is in JSON format, convert it to a dictionary
    result_dict = response.json()

    print(result_dict)