from Utils import *
from executor import executeInNewThread

def runPy(pyPath, inputFilePath):
    command = f'python3 {pyPath} <{inputFilePath} > {tempDir}{pyPath.split("/")[-1]}.output'
    executeInNewThread(command)


def CompareOutput():
    for base in getBases():
        base_output = ""
        try:
            with open(tempDir + base + ".output") as f:
                base_output = f.read()
        except FileNotFoundError:
            colorPrint(f"Base file {base} not found!", "red")
            continue

        colorPrint(f"Comparing semantics with {base}", "yellow")
        for comparer in getComparersFor(base):
            comparer_output = ""
            isSame = None
            with open(tempDir + comparer + ".output") as f:
                comparer_output = f.read()
            if base_output==comparer_output:
                print("\t"+comparer+": ",end="")
                colorPrint("SAME","green")
                isSame = True
            else:
                print("\t"+comparer+": ",end="")
                colorPrint("DIFFERENT","red")
                isSame = False
            CompareResult.logSemantic(base,comparer,isSame)


def executeAll():
    for baseFileName in getBases():
        baseFilePath = basesPath+baseFileName
        
        comparersFiles = getComparersFor(baseFileName)
        #print(f"readed comparers for {baseFileName}: {str(comparersFiles)}\n")

        colorPrint(f"Executing {baseFileName}", "green")
        runPy(baseFilePath, testcaseInputPath)

        for comparer in comparersFiles:
            compareFilePath = comparersPath+comparer
            colorPrint(f"Executing {comparer}", "yellow")
            runPy(compareFilePath, testcaseInputPath)