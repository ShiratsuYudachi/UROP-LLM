from black import format_str, FileMode
import ast
import astor

from SemanticComparator import *
from Utils import *


class RenameVisitor(ast.NodeVisitor):
    def __init__(self):
        self.var_map = {}
        self.var_count = 1

    def visit_Name(self, node):
        if node.id not in self.var_map:
            self.var_map[node.id] = f'var{self.var_count}'
            self.var_count += 1
        node.id = self.var_map[node.id]
        self.generic_visit(node)


def normalize(program : str):
    # remove redundant spaces
    try:
        program = format_str(program, mode=FileMode())
    except Exception:
        # TODO: handle syntax error properly
        return False
    #print(formatted_code)

    ast1 = ast.parse(program)

    # normalize AST
    renamer = RenameVisitor()
    renamer.visit(ast1)

    program = astor.to_source(ast1)

    return program
    

def CompareSyntax():
    for base in getBases():
        base_program = ""
        try:
            with open(basesPath + base) as f:
                base_program = f.read()
        except FileNotFoundError:
            colorPrint(f"Base file {base} not found!", "red")
            continue
        base_program = normalize(base_program)

        colorPrint(f"Comparing syntax with {base}", "yellow")
        for comparer in getComparersFor(base):
            comparer_program = ""
            with open(comparersPath + comparer) as f:
                comparer_program = f.read()
            comparer_program = normalize(comparer_program)
            
            isSame = None
            if (base_program!=False) and (comparer_program!=False) and base_program==comparer_program:
                print("\t"+comparer+": ",end="")
                colorPrint("SAME","green")
                isSame = True
            elif (base_program==False) and (comparer_program==False):
                colorPrint("BOTH INVALID","yellow")
                isSame = None
            else:
                print("\t"+comparer+": ",end="")
                colorPrint("DIFFERENT","red")
                isSame = False
            
            CompareResult.logSyntax(base,comparer,isSame)


#CompareSyntax()