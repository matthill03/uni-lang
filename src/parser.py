import token
import ast

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def peek(self):
        return self.tokens[self.position]

    def peek_offset(self, offset):
        return self.tokens[self.position + offset]

    def advance(self):
        if self.position + 1 >= len(self.tokens):
            return

        self.position += 1

    def advance_with_expected(self, expected_kinds):
        if self.peek().kind not in expected_kinds:
            print(f"Unexpected token ({self.peek().kind}), wanted -> {expected_kinds}")
            exit(1)

        self.advance()

    def parse_operator(self):
        if self.peek().kind in token.OPERATORS:
            return ast.Operator(self.peek().value)

    def parse_primary(self):
        if self.peek().kind == token.TokenKind.tok_int:
            num = ast.Number(self.peek().value, ast.LiteralType.type_int)
            self.advance()
            return num

        if self.peek().kind == token.TokenKind.tok_float:
            num = ast.Number(self.peek().value, ast.LiteralType.type_float)
            self.advance()
            return num

        if self.peek().kind == token.TokenKind.tok_true:
            bol = ast.Boolean(self.peek().value)
            self.advance()
            return bol

        if self.peek().kind == token.TokenKind.tok_false:
            bol = ast.Boolean(self.peek().value)
            self.advance()
            return bol

        if self.peek().kind == token.TokenKind.tok_not_op:
            op = self.parse_operator()
            self.advance() # !
            operand = self.parse_primary()
            return ast.UnaryExpr(op, operand)

        if self.peek().kind == token.TokenKind.tok_open_paren:
            self.advance()  # (
            expr = self.parse_bin_expr()
            self.advance_with_expected([token.TokenKind.tok_close_paren])  # )
            return expr

        raise ValueError(f"Unexpected token ({self.peek().kind})")

    def parse_bin_expr(self, min_precedence=0):
        if self.peek().kind == token.TokenKind.tok_semi:
            return

        lhs = self.parse_primary()

        while self.peek().kind in ast.PRECEDENCE and ast.PRECEDENCE[self.peek().kind] >= min_precedence:
            if self.peek().kind == token.TokenKind.tok_semi:
                break

            op = self.parse_operator()
            op_precendence = ast.PRECEDENCE[self.peek().kind]
            self.advance()

            rhs = self.parse_bin_expr(op_precendence + 1)

            lhs = ast.BinaryExpr(lhs, op, rhs)

        return lhs

def parse(tokens):
    parser = Parser(tokens)
    while parser.position < len(parser.tokens):
        expr = parser.parse_bin_expr()
        # print(expr)

        if expr == None:
            break;

        print(expr.evaluate())

        parser.advance_with_expected([token.TokenKind.tok_semi])
