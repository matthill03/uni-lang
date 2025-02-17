from enum import Enum

class TokenKind(Enum):
    # Literals
    tok_digit = 0,
    tok_id = 1,

    # Delimiters
    tok_open_paren = 2,
    tok_close_paren = 3,
    tok_semi = 4,

    # Keywords
    tok_true = 5,
    tok_false = 6,

    # Operators
    tok_plus = 7,
    tok_dash = 8,
    tok_star = 9,
    tok_fslash = 10,
    tok_percent = 11,
    tok_and_op = 12,
    tok_bit_and_op = 13,
    tok_or_op = 14,
    tok_bit_or_op = 15,
    tok_not_op = 16,
    tok_gt = 17,
    tok_lt = 18,
    tok_equal = 19,
    tok_not_equal = 20,
    tok_assign = 21,

    # EOF
    tok_eof = 22,

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
COMP_0PERATORS = [TokenKind.tok_gt, TokenKind.tok_lt, TokenKind.tok_equal, TokenKind.tok_not_equal]
LOGIGAL_OPERATORS = [TokenKind.tok_and_op, TokenKind.tok_or_op, TokenKind.tok_not_op]

# -------------- HELPERS -------------- 
def is_binary_op(token):

    if token.kind in BINARY_0PERATORS:
        return True

    return False

def is_logical_op(token):
    if token.kind in LOGIGAL_OPERATORS:
        return True

    return False

