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

    def handle_word(self, value):
        if value == "true":
            return Token(TokenKind.tok_true, value, self.line, self.column)
        elif value == "false":
            return Token(TokenKind.tok_false, value, self.line, self.column)
        else:
            return Token(TokenKind.tok_id, value, self.line, self.column)

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
        elif value == '>':
            self.advance()
            return Token(TokenKind.tok_gt, self.src[self.position - 1:self.position], self.line, self.column)
        elif value == '<':
            self.advance()
            return Token(TokenKind.tok_lt, self.src[self.position - 1:self.position], self.line, self.column)
        elif value == '!':
            if self.peek_offset(1) == '=':
                self.advance_n(2)
                return Token(TokenKind.tok_not_equal, self.src[self.position - 2:self.position], self.line, self.column)

            self.advance()
            return Token(TokenKind.tok_not_op, self.src[self.position - 1:self.position], self.line, self.column)
        elif value == '=':
            if self.peek_offset(1) == '=':
                self.advance_n(2)
                return Token(TokenKind.tok_equal, self.src[self.position - 2:self.position], self.line, self.column)

            self.advance()
            return Token(TokenKind.tok_assign, self.src[self.position - 1:self.position], self.line, self.column)
        elif value == '&':
            if self.peek_offset(1) == '&':
                self.advance_n(2)
                return Token(TokenKind.tok_and_op, self.src[self.position - 2:self.position], self.line, self.column)

            self.advance()
            return Token(TokenKind.tok_bit_and_op, self.src[self.position - 1:self.position], self.line, self.column)
        elif value == '|':
            if self.peek_offset(1) == '|':
                self.advance_n(2)
                return Token(TokenKind.tok_or_op, self.src[self.position - 2:self.position], self.line, self.column)

            self.advance()
            return Token(TokenKind.tok_bit_or_op, self.src[self.position - 1:self.position], self.line, self.column)

    def next_token(self):
        begin = 0
        end = 0

        while self.peek().isspace():
            try:
                self.advance() 
            except EOFError:
                return Token(TokenKind.tok_eof, "", self.line, self.column)

        if self.peek().isalpha():
            begin = self.position
            while self.peek().isalnum() or self.peek() == '_':
                self.advance() 
            end = self.position
            return self.handle_word(self.src[begin:end])

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
        # print(token)

        tokens.append(token)

        if token.kind == TokenKind.tok_eof:
            break

    return tokens
