from token import TokenKind, Token

def get_file_content(file_path):
    with open(file_path, "r") as file:
        content = file.read()

    return content

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

def lex(file_path):
    lexer = Lexer(file_path)
    tokens = []
    while True:
        token = lexer.next_token()

        tokens.append(token)

        if token.kind == TokenKind.tok_eof:
            break

    return tokens