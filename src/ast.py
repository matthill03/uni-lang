from abc import ABC, abstractmethod
from token import TokenKind

class ASTNode(ABC):
    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def evaluate(self):
        pass

class Number(ASTNode):
    def __init__(self, value):
        self.value = int(value)

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
        else:
            print(f"Unknown Operator ({self.op.value})")

PRECEDENCE = {
    TokenKind.tok_dash: 1,
    TokenKind.tok_plus: 1,
    TokenKind.tok_star: 2,
    TokenKind.tok_fslash: 2,
    TokenKind.tok_percent: 2
}