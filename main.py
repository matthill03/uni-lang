from enum import Enum



class TokenKind(Enum):
    # Literals
    tok_digit = 0,

    # Delimiters
    tok_open_paren = 1,
    tok_close_paren = 2,
    tok_semi = 3,

    # Operators
    tok_plus = 4,
    tok_dash = 5,
    tok_star = 6,
    tok_fslash = 7,
    tok_percent = 8,

    # EOF
    tok_eof = 9,

BINARY_0PERATORS = [TokenKind.tok_plus, TokenKind.tok_dash, TokenKind.tok_fslash, TokenKind.tok_percent, TokenKind.tok_star]

class Token:
    def __init__(self, kind, value, line, column):
        self.kind = kind
        self.value = value
        self.line = line
        self.column = column

    def __str__(self):
        return f"Kind: {self.kind}, Value: {self.value}, Line: {self.line}, Column: {self.column}"

class Lexer:
    def __init__(self, file_path):
        self.src = get_file_content(file_path)
        self.line = 0
        self.column = 1
        self.position = 0

    def peek(self):
        return self.src[self.position]

    def peek_offset(self, offset):
        return self.src[self.position + offset]

    def advance(self):
        if (self.position + 1) >= len(self.src):
            raise EOFError("End of the file has been found")

        if self.peek() == '\n':
            self.line += 1
            self.column = 0
        else:
            self.column += 1

        self.position += 1

    def advance_n(self, number):
        for _ in range(number):
            self.advance()

    def handle_delimiter(self, value):
        if value == '/':
            self.advance()
            return Token(TokenKind.tok_fslash, self.src[self.position - 1:self.position], self.line, self.column)
        elif value == '+':
            self.advance()
            return Token(TokenKind.tok_plus, self.src[self.position - 1:self.position], self.line, self.column)
        elif value == '-':
            self.advance()
            return Token(TokenKind.tok_dash, self.src[self.position - 1:self.position], self.line, self.column)
        elif value == '*':
            self.advance()
            return Token(TokenKind.tok_star, self.src[self.position - 1:self.position], self.line, self.column)
        elif value == '%':
            self.advance()
            return Token(TokenKind.tok_percent, self.src[self.position - 1:self.position], self.line, self.column)
        elif value == '(':
            self.advance()
            return Token(TokenKind.tok_open_paren, self.src[self.position - 1:self.position], self.line, self.column)
        elif value == ')':
            self.advance()
            return Token(TokenKind.tok_close_paren, self.src[self.position - 1:self.position], self.line, self.column)
        elif value == ';':
            self.advance()
            return Token(TokenKind.tok_semi, self.src[self.position - 1:self.position], self.line, self.column)

    def next_token(self):
        begin = 0
        end = 0

        while self.peek().isspace():
            try:
                self.advance() 
            except EOFError:
                return Token(TokenKind.tok_eof, "", self.line, self.column)


        if self.peek().isdigit():
            begin = self.position
            while self.peek().isdigit() or self.peek() == '.':
                self.advance()
            end = self.position
            return Token(TokenKind.tok_digit, self.src[begin:end], self.line, self.column)

        return self.handle_delimiter(self.peek())


def get_file_content(file_path):
    with open(file_path, "r") as file:
        content = file.read()

    return content

def lex(file_path):
    lexer = Lexer(file_path)
    tokens = []
    while True:
        token = lexer.next_token()

        tokens.append(token)

        if token.kind == TokenKind.tok_eof:
            break

    return tokens;

class ASTNode:
    pass

class Number(ASTNode):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"{self.value}"

class Operator(ASTNode):
    def __init__(self, op):
        self.op = op

    def __str__(self):
        return f"{self.op}"

class BinaryOp(ASTNode):
    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def __str__(self):
        return f"lhs: {self.lhs}, op: {self.op}, rhs: {self.rhs}"

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def peek(self):
        return self.tokens[self.position]

    def peek_offset(self, offset):
        return self.tokens[self.position + offset]

    def advance(self):
        self.position += 1

    def advance_with_expected(self, expected_kinds):
        for kind in expected_kinds:
            if self.peek_offset(1).kind == kind:
                self.advance()
                return

        print("Unexpected token")
        exit(1)

    def get_next(self):
        next_token = self.tokens[self.position]
        self.advance()

        return next_token

    def parse_bin_expr(self):
        lhs = Number(self.peek().value)

        if self.peek_offset(1).kind == TokenKind.tok_semi:
            self.advance_with_expected([TokenKind.tok_semi])
            self.advance_with_expected([TokenKind.tok_digit])
            return Number(lhs.value)

        self.advance_with_expected(BINARY_0PERATORS)

        op = Operator(self.peek().value)
        self.advance_with_expected([TokenKind.tok_digit])

        rhs = self.parse_bin_expr()

        return BinaryOp(lhs, op, rhs)

def is_binary_op(token):

    if token.kind in BINARY_0PERATORS:
        return True

    return False

def parse(tokens):
    parser = Parser(tokens)

    if tokens[-1].kind != TokenKind.tok_eof:
        print("End of file token should be at the end of the list!")
        exit(1)

    while parser.peek().kind != TokenKind.tok_eof:
        # token = parser.get_next()

        if is_binary_op(parser.peek_offset(1)):
            bin_op = parser.parse_bin_expr()
            print(bin_op)


if __name__ == "__main__":
    tokens = lex("examples/maths.qk")
    ast = parse(tokens)
