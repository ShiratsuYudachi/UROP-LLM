import os
import pandas as pd

def wrapDir(dir: str):
    if not dir.endswith("/"):
        dir+="/"
    return dir

# configs
tempDir = wrapDir("/Users/tsuyue/Documents/GitHub/UROP-LLM/CodeComparator/temp_ExecuteResult")
testcaseInputPath = "/Users/tsuyue/Documents/GitHub/UROP-LLM/CodeComparator/test_inputs/input_916e2.txt"
basesPath = wrapDir("/Users/tsuyue/Documents/GitHub/UROP-LLM/subjects/output/c1/simply_replace/916e2/gemini")
comparersPath = wrapDir("/Users/tsuyue/Documents/GitHub/UROP-LLM/subjects/output/c2/add_specific/916e2/gemini")

class CompareResult:
    AllResults = []
    initialized = False
    

    def __init__(self, base, comparer) -> None:
        self.base = base
        self.comparer = comparer
        self.isSyntaxSame = None
        self.isSemanticSame = None
    
    @staticmethod
    def initResultList():
        for base in getBases():
            for comparer in getComparersFor(base):
                CompareResult.AllResults.append(CompareResult(base,comparer))
    
    @staticmethod
    def getCompareResult(base,comparer):
        for result in CompareResult.AllResults:
            if result.base == base and result.comparer == comparer:
                return result
        return None
        
    @staticmethod
    def logSyntax(base, comparer, isSame:bool):
        if not CompareResult.initialized:
            CompareResult.initResultList()
            CompareResult.initialized = True
        CompareResult.getCompareResult(base,comparer).isSyntaxSame = isSame
    
    @staticmethod
    def logSemantic(base, comparer, isSame:bool):
        if not CompareResult.initialized:
            CompareResult.initResultList()
            CompareResult.initialized = True
        CompareResult.getCompareResult(base,comparer).isSemanticSame = isSame
    
    @staticmethod
    def printAll():
        currentbase = None
        for result in CompareResult.AllResults:
            if currentbase==result.base:
                print(f" \t{result.comparer}: isSyntaxSame {result.isSyntaxSame}, isSemanticSame {result.isSemanticSame}")
            else:
                currentbase=result.base
                print(f"{result.base}:")
                print(f" \t{result.comparer}: isSyntaxSame {result.isSyntaxSame}, isSemanticSame {result.isSemanticSame}")

    def toExcel():
        # 创建一个DataFrame
        dataFrame = {
            'c1': [],
            'c2': [],
            'syntax': [],
            'semantic': []
        }
        
        currentbase = None
        for result in CompareResult.AllResults:
            if currentbase==result.base:
                dataFrame['c1'].append('')
                dataFrame['c2'].append(result.comparer)
                dataFrame['syntax'].append('SAME' if result.isSyntaxSame==True else ('DIFFERENT' if result.isSyntaxSame==False else 'BOTH INVALID'))
                dataFrame['semantic'].append('SAME' if result.isSemanticSame else 'DIFFERENT')
            else:
                currentbase=result.base
                dataFrame['c1'].append(result.base)
                dataFrame['c2'].append(result.comparer)
                dataFrame['syntax'].append('SAME' if result.isSyntaxSame==True else ('DIFFERENT' if result.isSyntaxSame==False else 'BOTH INVALID'))
                dataFrame['semantic'].append('SAME' if result.isSemanticSame else 'DIFFERENT')

        # 写入Excel文件
                
        pd.DataFrame(dataFrame).to_excel('output.xlsx', sheet_name='Sheet1', index=False)

        



def colorPrint(info:str , color: str):
    colorCode = 31
    if color=="red":
        colorCode = 31
    elif color=="green":
        colorCode = 32
    elif color=="yellow":
        colorCode = 33
    print(f"\033[0;{colorCode}m%s\033[0m" % info)

def getComparersFor(base : str):
    # get files that needs to compare
    comparersFiles = []
    for x in sorted(os.listdir(comparersPath)):
        i = x.split('_')[-2]
        k = base.split('_')[-1].strip(".txt")
        i2 = x.split('_')[1]
        k2 = base.split('_')[1]

        if  i==k and i2==k2:
            comparersFiles.append(x)
    return comparersFiles

def getBases():
    baseFiles = []
    for filename in sorted(os.listdir(basesPath), key=lambda x: int((os.path.splitext(x)[0]).split('_')[1]*10 + (os.path.splitext(x)[0]).split('_')[-1].strip('.txt'))):
        baseFiles.append(filename)
    return baseFiles