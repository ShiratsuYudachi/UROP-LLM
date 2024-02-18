from SemanticComparator import executeAll,CompareOutput,runPy
from SyntaxComparator import CompareSyntax
from Utils import *

if __name__ == "__main__":
    print("""options:
          1: compare semantics and syntax, then output to excel table
          2: do above without executeAll()
          command: get runPy command
          """)
    option = input("option?= ")
    if (option == "1"):
        executeAll()
        CompareOutput()
        CompareSyntax()
        CompareResult.printAll()
        CompareResult.toExcel()
    elif (option == "2"):
        CompareOutput()
        CompareSyntax()
        CompareResult.printAll()
        CompareResult.toExcel()
    else:
        # test branch
        runPy("/Users/tsuyue/Documents/GitHub/UROP-LLM/CodeComparator/src.py",testcaseInputPath)