from qast import ASTContext

class Interpreter:
    def __init__(self, ast_root):
        self.root = ast_root
        self.glob_vars = ASTContext()

def interpret(ast_root):
    interpreter = Interpreter(ast_root)

    interpreter.root.evaluate(interpreter.glob_vars)