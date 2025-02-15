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

class Token:
    def __init__(self, kind, value, line, column):
        self.kind = kind
        self.value = value
        self.line = line
        self.column = column

    def __str__(self):
        return f"Kind: {self.kind}, Value: {self.value}, Line: {self.line}, Column: {self.column}"

# -------------- TYPE SETS -------------- 
BINARY_0PERATORS = [TokenKind.tok_plus, TokenKind.tok_dash, TokenKind.tok_fslash, TokenKind.tok_percent, TokenKind.tok_star]

# -------------- HELPERS -------------- 
def is_binary_op(token):

    if token.kind in BINARY_0PERATORS:
        return True

    return False