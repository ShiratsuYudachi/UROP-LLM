import os


#config
tempDir = "/Users/tsuyue/Programs/UROP/syntax_comparison_test/temp_syntaxCache/"
testcaseInputPath = "/Users/tsuyue/Programs/UROP/subjects/test_inputs/input_916e2.txt"
basesPath = "/Users/tsuyue/Programs/UROP/subjects/output/c1/simply_replace/916e2/gemini/"
comparersPath = "/Users/tsuyue/Programs/UROP/subjects/output/c2/add_specific/916e2/gemini/"

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

def runPy(pyPath, inputFilePath):
    os.system(f'python3 {pyPath} <{inputFilePath} > {tempDir}{pyPath.split("/")[-1]}.output')


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
            with open(tempDir + comparer + ".output") as f:
                comparer_output = f.read()
            if base_output==comparer_output:
                print("\t"+comparer+": ",end="")
                colorPrint("SAME","green")
            else:
                print("\t"+comparer+": ",end="")
                colorPrint("DIFFERENT","red")


def executeAll():
    for baseFileName in getBases():
        baseFilePath = basesPath+baseFileName
        
        comparersFiles = getComparersFor(baseFileName)
        #print(f"readed comparers for {baseFileName}: {str(comparersFiles)}\n")

        for comparer in comparersFiles:
            compareFilePath = comparersPath+comparer
            colorPrint(f"Executing {baseFileName}", "yellow")
            runPy(baseFilePath, testcaseInputPath)
            colorPrint(f"Executing {comparer}", "yellow")
            runPy(compareFilePath, testcaseInputPath)

if __name__ == "__main__":
    # executeAll()
    CompareOutput()