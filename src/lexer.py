from token import TokenKind, Token

class Lexer:
    def __init__(self, src):
        self.src = src
        self.line = 0
        self.column = 1
        self.position = 0

    def peek(self):
        return self.src[self.position]

    def peek_offset(self, offset):
        return self.src[self.position + offset]

    def advance(self):
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
            return Token(TokenKind.tok_fslash, '/', self.line, self.column)
        elif value == '+':
            self.advance()
            return Token(TokenKind.tok_plus, '+', self.line, self.column)
        elif value == '-':
            self.advance()
            return Token(TokenKind.tok_dash, '-', self.line, self.column)
        elif value == '*':
            self.advance()
            return Token(TokenKind.tok_star, '*', self.line, self.column)
        elif value == '%':
            self.advance()
            return Token(TokenKind.tok_percent, '%', self.line, self.column)
        elif value == '(':
            self.advance()
            return Token(TokenKind.tok_open_paren, ')', self.line, self.column)
        elif value == ')':
            self.advance()
            return Token(TokenKind.tok_close_paren, ')', self.line, self.column)
        elif value == ';':
            self.advance()
            return Token(TokenKind.tok_semi, ';', self.line, self.column)
        elif value == '>':
            if self.peek_offset(1) == '=':
                self.advance_n(2)
                return Token(TokenKind.tok_gt_equal, ">=", self.line, self.column)

            self.advance()
            return Token(TokenKind.tok_gt, '>', self.line, self.column)
        elif value == '<':
            if self.peek_offset(1) == '=':
                self.advance_n(2)
                return Token(TokenKind.tok_lt_equal, "<=", self.line, self.column)

            self.advance()
            return Token(TokenKind.tok_lt, '<', self.line, self.column)
        elif value == '!':
            if self.peek_offset(1) == '=':
                self.advance_n(2)
                return Token(TokenKind.tok_not_equal, "!=", self.line, self.column)

            self.advance()
            return Token(TokenKind.tok_not_op, '!', self.line, self.column)
        elif value == '=':
            if self.peek_offset(1) == '=':
                self.advance_n(2)
                return Token(TokenKind.tok_equal, "==", self.line, self.column)

            self.advance()
            return Token(TokenKind.tok_assign, '=', self.line, self.column)
        elif value == '&':
            if self.peek_offset(1) == '&':
                self.advance_n(2)
                return Token(TokenKind.tok_and_op, "&&", self.line, self.column)

            self.advance()
            return Token(TokenKind.tok_bit_and_op, '&', self.line, self.column)
        elif value == '|':
            if self.peek_offset(1) == '|':
                self.advance_n(2)
                return Token(TokenKind.tok_or_op, "||", self.line, self.column)

            self.advance()
            return Token(TokenKind.tok_bit_or_op, '|', self.line, self.column)
        elif value == '"':
            self.advance() # "
            begin = self.position

            while (self.position < len(self.src)) and self.src[self.position] != '"':
                self.advance()

            end = self.position
            self.advance() # "
            return Token(TokenKind.tok_string, self.src[begin:end], self.line, self.column)

    def tokenize(self):
        tokens = []
        while self.position < len(self.src):
            char = self.src[self.position]

            if char.isspace():
                self.advance()
                continue

            if char.isalpha():
                begin = self.position
                while (self.position < len(self.src)) and self.src[self.position].isalnum() or self.src[self.position] == '_':
                    self.advance()

                end = self.position
                tokens.append(self.handle_word(self.src[begin:end]))
                continue

            if char.isdigit():
                begin = self.position
                has_dec_point = False

                while (self.position < len(self.src)) and (self.src[self.position].isdigit() or (self.src[self.position] == '.' and not has_dec_point)):
                    if self.src[self.position] == '.':
                        has_dec_point = True

                    self.advance()
                end = self.position

                value = self.src[begin:end]
                if '.' in value:
                    tokens.append(Token(TokenKind.tok_float, value, self.line, self.column))
                    continue

                tokens.append(Token(TokenKind.tok_int, value, self.line, self.column))
                continue

            tokens.append(self.handle_delimiter(char))

        return tokens

def lex(file_path):
    lexer = Lexer(file_path)
    tokens = lexer.tokenize()
    # for token in tokens:
    #     print(token)

    return tokens
