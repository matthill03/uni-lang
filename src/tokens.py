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
    tok_open_brace = 36,
    tok_close_brace = 37,
    tok_semi = 4,
    tok_colon = 31,

    # Keywords
    # Reserved Words
    tok_true = 5,
    tok_false = 6,
    tok_if = 34,
    tok_else = 38,
    tok_while = 35,

    # Builtin
    tok_echo = 27,

    # Types
    tok_key_i32 = 28,
    tok_key_f32 = 33,
    tok_key_bool = 29,
    tok_key_string = 30,

    # Operators
    # Maths
    tok_plus = 7,
    tok_dash = 8,
    tok_star = 9,
    tok_fslash = 10,
    tok_percent = 11,

    # String Manipulation
    tok_concat = 32,

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

# -------------- TYPE SETS -------------- 
BINARY_0PERATORS = [TokenKind.tok_plus, TokenKind.tok_dash, TokenKind.tok_fslash, TokenKind.tok_percent, TokenKind.tok_star]
COMP_0PERATORS = [TokenKind.tok_gt, TokenKind.tok_lt, TokenKind.tok_equal, TokenKind.tok_not_equal, TokenKind.tok_gt_equal, TokenKind.tok_lt_equal]
LOGIGAL_OPERATORS = [TokenKind.tok_and_op, TokenKind.tok_or_op, TokenKind.tok_not_op]
STRING_OPERATORS = [TokenKind.tok_concat]

OPERATORS = [TokenKind.tok_plus, TokenKind.tok_dash, TokenKind.tok_fslash, TokenKind.tok_percent, TokenKind.tok_star, TokenKind.tok_and_op, TokenKind.tok_or_op, TokenKind.tok_not_op, TokenKind.tok_gt, TokenKind.tok_lt, TokenKind.tok_equal, TokenKind.tok_not_equal, TokenKind.tok_gt_equal, TokenKind.tok_lt_equal, TokenKind.tok_concat]

DIGITS = [TokenKind.tok_int, TokenKind.tok_float]

class OperatorType(Enum):
    type_logical = 0,
    type_maths = 1,
    type_string = 2,
    type_comp = 3,

class Token:
    def __init__(self, kind, value, line, column):
        self.kind = kind
        self.value = value
        self.line = line
        self.column = column

    def __str__(self):
        return f"Kind: {self.kind}, Value: {self.value}, Line: {self.line}, Column: {self.column}"

    # -------------- HELPERS -------------- 
    def is_operator(self):
        if self.kind in OPERATORS:
            return True

        return False

    def op_type(self):
        if self.kind in LOGIGAL_OPERATORS:
            return OperatorType.type_logical
        elif self.kind in BINARY_0PERATORS:
            return OperatorType.type_maths
        elif self.kind in STRING_OPERATORS:
            return OperatorType.type_string
        elif self.kind in COMP_0PERATORS:
            return OperatorType.type_comp

    def is_binary_op(self):
        if self.kind in BINARY_0PERATORS:
            return True

        return False

    def is_comparison_op(self):
        if self.kind in COMP_0PERATORS:
            return True

        return False

    def is_logical_op(self):
        if self.kind in LOGIGAL_OPERATORS:
            return True

        return False

    def is_digit(self):
        if self.kind in DIGITS:
            return True

        return False


