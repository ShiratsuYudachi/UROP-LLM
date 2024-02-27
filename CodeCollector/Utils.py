import time
import json
from datetime import datetime

acceptedLangs = ["Python 3", "Python 2", "PyPy 2", "PyPy 3", "PyPy 3-64"]


def wrapDir(dir: str):
    if not dir.endswith("/"):
        dir+="/"
    return dir

submissionsPath = "/Users/tsuyue/Documents/GitHub/UROP-LLM/CodeCollector/submissions/"
subjectPath = "/Users/tsuyue/Documents/GitHub/UROP-LLM/CodeCollector/subjects/"


class Verdict:
    class ErrorType:
        COMPILATION = 0
        RUNTIME = 1
        TIME = 2
        ANSWER = 3
        OTHER = 4
    
    def __init__(self, isAccepted:bool, errorType:int, errorCase:int=None) -> None:
        self.isAccepted = isAccepted
        self.errorType = errorType
        self.errorCase = errorCase
    
    def to_dict(self):
        return {
            'isAccepted': self.isAccepted,
            'errorType': self.errorType,
            'errorCase': self.errorCase
        }
    
    @staticmethod
    def parse_dict(text):
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


# CF for Codeforces
class CFSubmission:
    def __init__(self, contestID:str, problem:str, submissionID:str, author:str, lang:str, verdict:Verdict, runTime:int, memory:int, submissionTime:int) -> None:
        self.contestID = contestID
        self.problem = problem
        self.submissionID = submissionID
        self.author = author
        self.lang = lang
        self.verdict = verdict
        self.runTime = runTime
        self.memory = memory
        self.submissionTime = submissionTime
        
    def to_dict(self):
        return {
            'contestID': self.contestID,
            'problem': self.problem,
            'submissionID': self.submissionID,
            'author': self.author,
            'lang': self.lang,
            'verdict': self.verdict.to_dict(),
            'runTime': self.runTime,
            'memory': self.memory,
            'submissionTime': self.submissionTime
        }
    
    @staticmethod
    def parse_dict(submissionDict):
        contestID = submissionDict['contestID']
        problem = submissionDict['problem']
        submissionID = submissionDict['submissionID']
        author = submissionDict['author']
        lang = submissionDict['lang']
        verdict = Verdict.parse_dict(submissionDict['verdict'])
        runTime = submissionDict['runTime']
        memory = submissionDict['memory']
        submissionTime = submissionDict['submissionTime']

        return CFSubmission(contestID=contestID, problem=problem, submissionID=submissionID, author=author, lang=lang, verdict=verdict, runTime=runTime, memory=memory, submissionTime=submissionTime)

    @staticmethod
    def parse_dict_list(ls): # ls: CFSubmission[] type
        return [CFSubmission.parse_dict(x) for x in ls]
    
    
class CFSubject:
    def __init__(self, acceptedSubmission:CFSubmission, rejectedSubmission:CFSubmission, acceptedCode:str, rejectedCode:str, errorCase={}, errorLine:int=0) -> None:
        self.acceptedSubmission = acceptedSubmission
        self.rejectedSubmission = rejectedSubmission
        self.acceptedCode = acceptedCode
        self.rejectedCode = rejectedCode
        self.errorCase = errorCase
        self.errorLine = errorLine
        
    def to_dict(self):
        return {
            'acceptedSubmission': self.acceptedSubmission.to_dict(),
            'rejectedSubmission': self.rejectedSubmission.to_dict(),
            'acceptedCode': self.acceptedCode,
            'rejectedCode': self.rejectedCode,
            'errorCase': self.errorCase,
            'errorLine': self.errorLine
        }
    
    @staticmethod
    def parse_dict(subjectDict):
        acceptedSubmission = CFSubmission.parse_dict(subjectDict['acceptedSubmission'])
        rejectedSubmission = CFSubmission.parse_dict(subjectDict['rejectedSubmission'])
        acceptedCode = subjectDict['acceptedCode']
        rejectedCode = subjectDict['rejectedCode']
        errorCase = subjectDict['errorCase']
        errorLine = subjectDict.get('errorLine', 0)  # Use .get() to handle missing errorLine with default 0

        return CFSubject(
            acceptedSubmission=acceptedSubmission,
            rejectedSubmission=rejectedSubmission,
            acceptedCode=acceptedCode,
            rejectedCode=rejectedCode,
            errorCase=errorCase,
            errorLine=errorLine
        )

    
    
    

def get_subject_json_name(contestID):
    return subjectPath+str(contestID)+'.json'

def get_submission_json_name(contestID):
    return submissionsPath+str(contestID)+'.json'

def save_submissions(submissions, contestID):
    submissions_dicts = [submission.to_dict() for submission in submissions]
    filename = get_submission_json_name(contestID)
    with open(filename, 'w') as file:
        json.dump(submissions_dicts, file, indent=4)

def read_submissions(contestID):
    filename = get_submission_json_name(contestID)
    with open(filename, 'r') as file:
        submissions = json.load(file)
    return submissions


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