import time
import json
from datetime import datetime
import csv

acceptedLangs = ["Python 3", "Python 2", "PyPy 2", "PyPy 3", "PyPy 3-64"]


def wrapDir(dir: str):
    if not dir.endswith("/"):
        dir+="/"
    return dir

submissionsPath = "/Users/tsuyue/Documents/GitHub/UROP-LLM/CodeCollector/submissions/"
subjectPath = "/Users/tsuyue/Documents/GitHub/UROP-LLM/CodeCollector/subjects/"

# CF for Codeforces
class CFSubmission:
    def __init__(self, contestID:str, problem:str, submissionID:str, author:str, lang:str, isAccepted:bool, errorType:str, errorCaseNo:int, runTime:int, memory:int, submissionTime:int) -> None:
        self.contestID = contestID
        self.problem = problem
        self.submissionID = submissionID
        self.author = author
        self.lang = lang
        self.isAccepted = isAccepted
        self.errorType = errorType
        self.errorCaseNo = errorCaseNo
        self.runTime = runTime
        self.memory = memory
        self.submissionTime = submissionTime
    

    @staticmethod
    def save_to_csv(submissions, contestID):
        filename = get_submission_csv_name(contestID)
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            # 写入列标题
            writer.writerow(['contestID', 'problem', 'submissionID', 'author', 'lang', 'isAccepted', 'errorType', 'errorCaseNo', 'runTime', 'memory', 'submissionTime'])
            # 写入每个提交的数据
            for submission in submissions:
                writer.writerow([submission.contestID, submission.problem, submission.submissionID, submission.author, submission.lang, submission.isAccepted, submission.errorType, submission.errorCaseNo, submission.runTime, submission.memory, submission.submissionTime])

    @staticmethod
    def read_from_csv(contestID):
        filename = get_submission_csv_name(contestID)
        submissions = []
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                submission = CFSubmission(row['contestID'], row['problem'], row['submissionID'], row['author'], row['lang'], row['isAccepted'] == 'True', row['errorType'], int(row['errorCaseNo']), int(row['runTime']), int(row['memory']), int(float(row['submissionTime'])))
                submissions.append(submission)
        return submissions
    
    @staticmethod
    def append_to_csv(submissions, contestID):
        filename = get_submission_csv_name(contestID)
        with open(filename, mode='a', newline='') as file:  # 使用追加模式'a'
            writer = csv.writer(file)
            # 直接写入每个提交的数据，不需要再写列标题
            for submission in submissions:
                writer.writerow([submission.contestID, submission.problem, submission.submissionID, submission.author, submission.lang, submission.isAccepted, submission.errorType, submission.errorCaseNo, submission.runTime, submission.memory, submission.submissionTime])
    
    
    def to_dict(self):
        return {
            'contestID': self.contestID,
            'problem': self.problem,
            'submissionID': self.submissionID,
            'author': self.author,
            'lang': self.lang,
            'isAccepted': self.isAccepted,
            'errorType': self.errorType,
            'errorCaseNo': self.errorCaseNo,
            'runTime': self.runTime,
            'memory': self.memory,
            'submissionTime': self.submissionTime
        }
    
    # NOT USABLE
    @staticmethod
    def parse_dict(submissionDict):
        contestID = submissionDict['contestID']
        problem = submissionDict['problem']
        submissionID = submissionDict['submissionID']
        author = submissionDict['author']
        lang = submissionDict['lang']
        isAccepted = submissionDict['isAccepted']
        errorType = submissionDict['errorType']
        errorCaseNo = submissionDict['errorCaseNo']
        runTime = submissionDict['runTime']
        memory = submissionDict['memory']
        submissionTime = submissionDict['submissionTime']

        return CFSubmission(contestID=contestID, problem=problem, submissionID=submissionID, author=author, lang=lang, isAccepted=isAccepted, errorType=errorType, errorCaseNo=errorCaseNo, runTime=runTime, memory=memory, submissionTime=submissionTime)

    # NOT USABLE
    @staticmethod
    def parse_dict_list(ls): # ls: CFSubmission[] type
        return [CFSubmission.parse_dict(x) for x in ls]
    

    
    
class CFSubject:
    def __init__(self, acceptedSubmission:CFSubmission, rejectedSubmission:CFSubmission, acceptedCode:str, rejectedCode:str, failedTestCase={}, errorLine:int=0) -> None:
        self.acceptedSubmission = acceptedSubmission
        self.rejectedSubmission = rejectedSubmission
        self.acceptedCode = acceptedCode
        self.rejectedCode = rejectedCode
        self.failedTestCase = failedTestCase
        self.errorLine = errorLine
        
    def to_dict(self):
        return {
            'acceptedSubmission': self.acceptedSubmission.to_dict(),
            'rejectedSubmission': self.rejectedSubmission.to_dict(),
            'acceptedCode': self.acceptedCode,
            'rejectedCode': self.rejectedCode,
            'failedTestCase': self.failedTestCase,
            'errorLine': self.errorLine
        }
    
    @staticmethod
    def parse_dict(subjectDict):
        acceptedSubmission = CFSubmission.parse_dict(subjectDict['acceptedSubmission'])
        rejectedSubmission = CFSubmission.parse_dict(subjectDict['rejectedSubmission'])
        acceptedCode = subjectDict['acceptedCode']
        rejectedCode = subjectDict['rejectedCode']
        failedTestCase = subjectDict['failedTestCase']
        errorLine = subjectDict.get('errorLine', 0)  # Use .get() to handle missing errorLine with default 0

        return CFSubject(
            acceptedSubmission=acceptedSubmission,
            rejectedSubmission=rejectedSubmission,
            acceptedCode=acceptedCode,
            rejectedCode=rejectedCode,
            failedTestCase=failedTestCase,
            errorLine=errorLine
        )

    

def get_subject_json_name(contestID):
    return subjectPath+str(contestID)+'.json'

def get_submission_csv_name(contestID):
    return submissionsPath+str(contestID)+'.csv'


def colorPrint(info:str , color: str):
    colorCode = 31
    if color=="red":
        colorCode = 31
    elif color=="green":
        colorCode = 32
    elif color=="yellow":
        colorCode = 33
    print(f"\033[0;{colorCode}m%s\033[0m" % info)

def save_subjects(subjects, contestID):
    subject_dicts = [subject.to_dict() for subject in subjects]
    filename = get_subject_json_name(contestID)
    with open(filename, 'w') as file:
        json.dump(subject_dicts, file, indent=4)