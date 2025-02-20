from enum import Enum

class TokenKind(Enum):
    # Literals
    tok_int = 0,
    tok_float = 25,
    tok_string = 26,
    tok_id = 1,

    # Delimiters
    tok_open_paren = 2,
    tok_close_paren = 3,
    tok_semi = 4,

    # Keywords
    tok_true = 5,
    tok_false = 6,

    # Operators
    # Maths
    tok_plus = 7,
    tok_dash = 8,
    tok_star = 9,
    tok_fslash = 10,
    tok_percent = 11,

    # Comparison
    tok_and_op = 12,
    tok_bit_and_op = 13,
    tok_or_op = 14,
    tok_bit_or_op = 15,
    tok_not_op = 16,

    # Logical
    tok_gt = 17,
    tok_gt_equal = 18,
    tok_lt = 19,
    tok_lt_equal = 20,
    tok_equal = 21,
    tok_not_equal = 22,

    # Other
    tok_assign = 23,

    # EOF
    tok_eof = 24,

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
COMP_0PERATORS = [TokenKind.tok_gt, TokenKind.tok_lt, TokenKind.tok_equal, TokenKind.tok_not_equal, TokenKind.tok_gt_equal, TokenKind.tok_lt_equal]
LOGIGAL_OPERATORS = [TokenKind.tok_and_op, TokenKind.tok_or_op, TokenKind.tok_not_op]

OPERATORS = [TokenKind.tok_plus, TokenKind.tok_dash, TokenKind.tok_fslash, TokenKind.tok_percent, TokenKind.tok_star, TokenKind.tok_and_op, TokenKind.tok_or_op, TokenKind.tok_not_op, TokenKind.tok_gt, TokenKind.tok_lt, TokenKind.tok_equal, TokenKind.tok_not_equal, TokenKind.tok_gt_equal, TokenKind.tok_lt_equal]

DIGITS = [TokenKind.tok_int, TokenKind.tok_float]

# -------------- HELPERS -------------- 
def is_binary_op(token):

    if token.kind in BINARY_0PERATORS:
        return True

    return False

def is_logical_op(token):
    if token.kind in LOGIGAL_OPERATORS:
        return True

    return False

