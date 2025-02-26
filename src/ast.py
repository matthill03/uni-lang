from enum import Enum
from tokens import TokenKind

class SymbolTableEntry:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class ASTContext:
    def __init__(self):
        self.variables = {}
    
    def get_variable(self, var_name):
        if var_name not in self.variables:
            raise ValueError(f"Undefined variable ({var_name})")
        
        return self.variables[var_name]

    def set_new_variable(self, var_name, type, value):
        if var_name in self.variables:
            raise ValueError(f"Variable already exists ({var_name})")
        
        self.variables[var_name] = SymbolTableEntry(type, value)

    def set_existing_variable(self, var_name, value):
        if var_name not in self.variables:
            raise ValueError(f"Undefined variable ({var_name})")

        self.variables[var_name].value = value

class LiteralType(Enum):
    type_i32 = 0,
    type_float = 1,
    type_string = 2,
    type_bool = 3,

class ASTNodeKind(Enum):
    # Root
    ast_root = 7,

    # Literals
    ast_num = 0,
    ast_bool = 1,
    ast_str = 2,
    ast_op = 3,
    ast_id = 7,

    # Expressions/Statements
    ast_var_decl = 4,
    ast_var_assign = 8,
    ast_unr_expr = 5,
    ast_bin_expr = 6,

class ASTRoot():
    def __init__(self):
        self.kind = ASTNodeKind.ast_root
        self.children = []
        self.context = ASTContext()
    
    def __str__(self):
        pass

    def evaluate(self):
        for child in self.children:
            child.evaluate(self.context)

    def append_child(self, child):
        self.children.append(child)

class Number(ASTRoot):
    def __init__(self, value, type):
        self.kind = ASTNodeKind.ast_num
        self.type = type

        if type == LiteralType.type_float:
            self.value = float(value)
        elif type == LiteralType.type_i32:
            self.value = int(value)
        else:
            print(f"Invalid number literal type ({type})")
            exit(1)

    def __str__(self):
        return f"(value: {self.value}, type: {self.type})"

    def evaluate(self, context):
        return (self.value, self.type)
    
class Identifier(ASTRoot):
    def __init__(self, value):
        self.kind = ASTNodeKind.ast_id
        self.value = value
    
    def __str__(self):
        return f"(Value: {self.value})"
    
    def evaluate(self, context):
        var = context.get_variable(self.value)
        return (var.value, var.type)

class Boolean(ASTRoot):
    def __init__(self, value):
        self.kind = ASTNodeKind.ast_bool
        self.type = LiteralType.type_bool

        if value == "true":
            self.value = True
        elif value == "false":
            self.value = False
        else:
            print(f"Invalid bool literal ({value})")
            exit(1)

    def __str__(self):
        return f"{self.value}"

    def evaluate(self, context):
        return (self.value, self.type)

class String(ASTRoot):
    def __init__(self, value):
        self.kind = ASTNodeKind.ast_str
        self.type = LiteralType.type_string
        self.value = str(value)

    def __str__(self):
        return f'"{self.value}"'

    def evaluate(self, context):
        return (self.value, self.type)

class Operator(ASTRoot):
    def __init__(self, op):
        self.kind = ASTNodeKind.ast_op
        self.value = op

    def __str__(self):
        return f"{self.value}"

    def evaluate(self, context):
        return self.value
    
class VariableDeclaration(ASTRoot):
    def __init__(self, name, type, value):
        self.kind = ASTNodeKind.ast_var_decl
        self.name = name
        self.type = type
        self.value = value
    
    def __str__(self):
        return f"(Name: {self.name}, Type: {self.type}, Value: {self.value})"
    
    def evaluate(self, context):
        # TODO: Should check if evaluated value is the correct type
        if self.type == TokenKind.tok_key_i32:
            self.type = LiteralType.type_i32
        if self.type == TokenKind.tok_key_bool:
            self.type = LiteralType.type_bool
        if self.type == TokenKind.tok_key_string:
            self.type = LiteralType.type_string

        var = self.value.evaluate(context)
        context.set_new_variable(self.name, var[1], var[0])

class VariableAssignment(ASTRoot):
    def __init__(self, name, value):
        self.kind = ASTNodeKind.ast_var_assign
        self.name = name
        self.value = value

    def __str__(self):
        return f"(Name: {self.name}, Value: {self.value})"

    def evaluate(self, context):
        var = self.value.evaluate(context)
        context.set_new_variable(self.name, var[1], var[0])

class UnaryExpr(ASTRoot):
    def __init__(self, op, stmt):
        self.kind = ASTNodeKind.ast_unr_expr
        self.op = op
        self.stmt = stmt

    def __str__(self):
        return f"(op: {self.op}, stmt: {self.stmt})"

    def evaluate(self, context):
        operand = self.stmt.evaluate(context)
        op = self.op.evaluate(context)

        if op == '!':
            return not operand
        else:
            print(f"Unknown unary operator ({op})")

class BinaryExpr(ASTRoot):
    def __init__(self, lhs, op, rhs):
        self.kind = ASTNodeKind.ast_bin_expr
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def __str__(self):
        return f"(lhs: {self.lhs}, op: {self.op}, rhs: {self.rhs})"
    
    def evaluate(self, context):
        lhs, lhs_type = self.lhs.evaluate(context)
        rhs, rhs_type = self.rhs.evaluate(context)
        op = self.op.evaluate(context)

        if lhs_type == LiteralType.type_i32 and (rhs_type != LiteralType.type_i32 and rhs_type != LiteralType.type_float):
            raise Exception(f"Incompatible types ({lhs_type} - {rhs_type})")

        if lhs_type == LiteralType.type_float and (rhs_type != LiteralType.type_i32 and rhs_type != LiteralType.type_float):
            raise Exception(f"Incompatible types ({lhs_type} - {rhs_type})")

        if lhs_type == LiteralType.type_string and rhs_type != LiteralType.type_string:
            raise Exception(f"Incompatible types ({lhs_type} - {rhs_type})")

        if lhs_type == LiteralType.type_bool and rhs_type != LiteralType.type_bool:
            raise Exception(f"Incompatible types ({lhs_type} - {rhs_type})")

        if op == '+':
            return lhs + rhs, lhs_type
        elif op == '-':
            return lhs - rhs, lhs_type
        elif op == '*':
            return lhs * rhs, lhs_type
        elif op == '/':
            return lhs / rhs, lhs_type
        elif op == '%':
            return lhs % rhs, lhs_type
        elif op == '==':
            return lhs == rhs, lhs_type
        elif op == '!=':
            return lhs != rhs, lhs_type
        elif op == '<':
            return lhs < rhs, lhs_type
        elif op == '<=':
            return lhs <= rhs, lhs_type
        elif op == '>':
            return lhs > rhs, lhs_type
        elif op == '>=':
            return lhs >= rhs, lhs_type
        elif op == '&&':
            return lhs and rhs, lhs_type
        elif op == '||':
            return lhs or rhs, lhs_type
        else:
            print(f"Unknown Operator ({self.op.value})")

PRECEDENCE = {
    # Maths
    TokenKind.tok_star: 6,
    TokenKind.tok_fslash: 6,
    TokenKind.tok_percent: 6,
    TokenKind.tok_dash: 5,
    TokenKind.tok_plus: 5,

    # Comparison
    TokenKind.tok_lt: 4,
    TokenKind.tok_lt_equal: 4,
    TokenKind.tok_gt: 4,
    TokenKind.tok_gt_equal: 4,
    TokenKind.tok_equal: 3,
    TokenKind.tok_not_equal: 3,

    # Logical
    TokenKind.tok_and_op: 2,
    TokenKind.tok_or_op: 1,
}

class EchoBuiltin(ASTRoot):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"(Value: {self.value})"
    
    def evaluate(self, context):
        print(self.value.evaluate(context)[0])

 # type: ignore