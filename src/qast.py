from enum import Enum
from tokens import TokenKind, OperatorType

class QwrkRuntimeError(RuntimeError):
    def __init__(self, node, message):
        super().__init__(message)
        self.node = node
        self.message = message

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.message

class SymbolTableEntry:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class ASTContext:
    def __init__(self):
        self.variables = {}

    def get_variable(self, var_name):
        if var_name not in self.variables:
            raise QwrkRuntimeError(self, f"Undefined variable ({var_name})")

        return self.variables[var_name]

    def set_new_variable(self, var_name, type, value):
        if var_name in self.variables:
            raise QwrkRuntimeError(self, f"Variable name already exists ({var_name})")

        self.variables[var_name] = SymbolTableEntry(type, value)

    def set_existing_variable(self, var_name, value):
        if var_name not in self.variables:
            raise QwrkRuntimeError(self, f"Undefined variable ({var_name})")

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
            raise QwrkRuntimeError(self, f"Invalid number literal type ({type})")

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
            raise QwrkRuntimeError(self, f"Invalid bool literal ({value})")

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
    def __init__(self, op, type):
        self.kind = ASTNodeKind.ast_op
        self.type = type
        self.value = op

    def __str__(self):
        return f"{self.value}"

    def evaluate(self, context):
        return self.value

    def is_mathmatical(self):
        if self.type == OperatorType.type_maths:
            return True

        return False

    def is_logical(self):
        if self.type == OperatorType.type_logical:
            return True

        return False

    def is_comp(self):
        if self.type == OperatorType.type_comp:
            return True

        return False

    def is_string_op(self):
        if self.type == OperatorType.type_string:
            return True

        return False

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

        var, var_type = self.value.evaluate(context)
        if var_type != self.type:
            raise QwrkRuntimeError(self, f"Cannot assign type ({var_type}) to type ({self.type})")

        context.set_new_variable(self.name, var_type, var)

class VariableAssignment(ASTRoot):
    def __init__(self, name, value):
        self.kind = ASTNodeKind.ast_var_assign
        self.name = name
        self.value = value

    def __str__(self):
        return f"(Name: {self.name}, Value: {self.value})"

    def evaluate(self, context):
        var = self.value.evaluate(context)
        var_type = context.get_variable(self.name).type

        if var[1] != var_type:
            raise QwrkRuntimeError(self, f"Cannot assign type ({var[1]}) to type ({var_type})")

        context.set_existing_variable(self.name, var[0])

class UnaryExpr(ASTRoot):
    def __init__(self, op, stmt):
        self.kind = ASTNodeKind.ast_unr_expr
        self.op = op
        self.stmt = stmt

    def __str__(self):
        return f"(op: {self.op}, stmt: {self.stmt})"

    def evaluate(self, context):
        operand, operand_type = self.stmt.evaluate(context)
        op = self.op.evaluate(context)

        if op == '!':
            return (not operand, LiteralType.type_bool)
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

    def evaluate_arithmatic(self, op, context):
        lhs, lhs_type = self.lhs.evaluate(context)
        rhs, rhs_type = self.rhs.evaluate(context)

        if lhs_type != LiteralType.type_i32 and lhs_type != LiteralType.type_float:
            raise QwrkRuntimeError(self, f"Invalid Arethmatic operation type ({lhs_type})")

        if rhs_type != LiteralType.type_i32 and rhs_type != LiteralType.type_float:
            raise QwrkRuntimeError(self, f"Invalid Arethmatic operation type ({rhs_type})")

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

    def evaluate_logical(self, op, context):
        lhs, lhs_type = self.lhs.evaluate(context)
        rhs, rhs_type = self.rhs.evaluate(context)

        if lhs_type == LiteralType.type_bool and rhs_type != LiteralType.type_bool:
            raise QwrkRuntimeError(self, f"Incompatible types ({lhs_type} - {rhs_type})")

        elif op == '&&':
            return lhs and rhs, LiteralType.type_bool
        elif op == '||':
            return lhs or rhs, LiteralType.type_bool

    def evaluate_comp(self, op, context):
        lhs, lhs_type = self.lhs.evaluate(context)
        rhs, rhs_type = self.rhs.evaluate(context)

        if lhs_type == LiteralType.type_i32 and (rhs_type != LiteralType.type_i32 and rhs_type != LiteralType.type_float):
            raise QwrkRuntimeError(self, f"Incompatible types ({lhs_type} - {rhs_type})")

        if lhs_type == LiteralType.type_float and (rhs_type != LiteralType.type_i32 and rhs_type != LiteralType.type_float):
            raise QwrkRuntimeError(self, f"Incompatible types ({lhs_type} - {rhs_type})")

        if lhs_type == LiteralType.type_bool and rhs_type != LiteralType.type_bool:
            raise QwrkRuntimeError(self, f"Incompatible types ({lhs_type} - {rhs_type})")

        if op == '==':
            return lhs == rhs, LiteralType.type_bool
        elif op == '!=':
            return lhs != rhs, LiteralType.type_bool
        elif op == '<':
            return lhs < rhs, LiteralType.type_bool
        elif op == '<=':
            return lhs <= rhs, LiteralType.type_bool
        elif op == '>':
            return lhs > rhs, LiteralType.type_bool
        elif op == '>=':
            return lhs >= rhs, LiteralType.type_bool

    def evaluate_string(self, op, context):
        lhs, lhs_type = self.lhs.evaluate(context)
        rhs, rhs_type = self.rhs.evaluate(context)

        if lhs_type != LiteralType.type_string:
            raise QwrkRuntimeError(self, f"Invalid String operation type ({lhs_type})")

        if rhs_type != LiteralType.type_string:
            raise QwrkRuntimeError(self, f"Invalid String operation type ({rhs_type})")

        if op == '++':
            return lhs + rhs, lhs_type


    def evaluate(self, context):
        if self.op.is_mathmatical():
            return self.evaluate_arithmatic(self.op.evaluate(context), context)

        if self.op.is_logical():
            return self.evaluate_logical(self.op.evaluate(context), context)

        if self.op.is_comp():
            return self.evaluate_comp(self.op.evaluate(context), context)

        if self.op.is_string_op():
            return self.evaluate_string(self.op.evaluate(context), context)

        raise QwrkRuntimeError(self, f"Unknown Operator ({self.op.value})")

class EchoBuiltin(ASTRoot):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"(Value: {self.value})"
    
    def evaluate(self, context):
        print(self.value.evaluate(context)[0])

 # type: ignore
