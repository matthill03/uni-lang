from abc import ABC, abstractmethod
from enum import Enum
from token import TokenKind

class LiteralType(Enum):
    type_int = 0,
    type_float = 1,

class ASTNode(ABC):
    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def evaluate(self):
        pass

class Number(ASTNode):
    def __init__(self, value, type):
        self.type = type

        if type == LiteralType.type_float:
            self.value = float(value)
        elif type == LiteralType.type_int:
            self.value = int(value)
        else:
            print(f"Invalid number literal type ({type})")
            exit(1)

    def __str__(self):
        return f"(value: {self.value}, type: {self.type})"

    def evaluate(self):
        return self.value

class Boolean(ASTNode):
    def __init__(self, value):
        if value == "true":
            self.value = True
        elif value == "false":
            self.value = False
        else:
            print(f"Invalid bool literal ({value})")
            exit(1)

    def __str__(self):
        return f"{self.value}"

    def evaluate(self):
        return self.value

class Operator(ASTNode):
    def __init__(self, op):
        self.value = op

    def __str__(self):
        return f"{self.value}"

    def evaluate(self):
        return self.value

class UnaryExpr(ASTNode):
    def __init__(self, op, stmt):
        self.op = op
        self.stmt = stmt

    def __str__(self):
        return f"(op: {self.op}, stmt: {self.stmt})"

    def evaluate(self):
        operand = self.stmt.evaluate()
        op = self.op.evaluate()

        if op == '!':
            return not operand
        else:
            print(f"Unknown unary operator ({op})")

class BinaryExpr(ASTNode):
    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def __str__(self):
        return f"(lhs: {self.lhs}, op: {self.op}, rhs: {self.rhs})"
    
    def evaluate(self):
        lhs = self.lhs.evaluate()
        rhs = self.rhs.evaluate()
        op = self.op.evaluate()

        if op == '+':
            return lhs + rhs
        elif op == '-':
            return lhs - rhs
        elif op == '*':
            return lhs * rhs
        elif op == '/':
            return lhs / rhs
        elif op == '%':
            return lhs % rhs
        elif op == '==':
            return lhs == rhs
        elif op == '!=':
            return lhs != rhs
        elif op == '<':
            return lhs < rhs
        elif op == '<=':
            return lhs <= rhs
        elif op == '>':
            return lhs > rhs
        elif op == '>=':
            return lhs >= rhs
        elif op == '&&':
            return lhs and rhs
        elif op == '||':
            return lhs or rhs
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
