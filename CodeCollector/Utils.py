import time

submissionsPath = "/Users/tsuyue/Documents/GitHub/UROP-LLM/CodeCollector/submissions.json"

acceptedLangs = ["Python 3", "Python 2", "PyPy 2", "PyPy 3", "PyPy 3-64"]
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
    
class CFSubject:
    def __init__(self, acceptedSubmission:CFSubmission, rejectedSubmission:CFSubmission, acceptedCode:str, rejectedCode) -> None:
        self.acceptedSubmission = acceptedSubmission
        self.acceptedCode = acceptedCode
        self.rejectedSubmission = rejectedSubmission
        self.rejectedCode = rejectedCode