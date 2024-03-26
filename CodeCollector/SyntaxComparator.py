from black import format_str, FileMode
import ast
import astor

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
    
