from tokens import TokenKind
from qast import BinaryExpr, UnaryExpr, Number, Boolean, String, Identifier, ASTRoot, VariableAssignment, VariableDeclaration, IfStmt, WhileStmt, EchoBuiltin, Operator, LiteralType

PRECEDENCE = {
    # Maths
    TokenKind.tok_star: 6,
    TokenKind.tok_fslash: 6,
    TokenKind.tok_percent: 6,
    TokenKind.tok_dash: 5,
    TokenKind.tok_plus: 5,
    TokenKind.tok_concat: 5,

    # Comparison
    TokenKind.tok_lt: 4,
    TokenKind.tok_lt_equal: 4,
    TokenKind.tok_gt: 4,
    TokenKind.tok_gt_equal: 4,
    TokenKind.tok_equal: 3,
    TokenKind.tok_not_equal: 3,

    # Logical
    TokenKind.tok_and_op: 2,
    TokenKind.tok_or_op: 1,
}


class ParseError(RuntimeError):
    def __init__(self, token, message):
        super().__init__(message)
        self.token = token

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.variables = {}

    def peek(self):
        return self.tokens[self.position]

    def peek_offset(self, offset):
        return self.tokens[self.position + offset]

    def advance(self):
        if self.position + 1 >= len(self.tokens):
            return

        self.position += 1

    def advance_with_expected(self, *expected_kinds):
        if self.peek().kind not in expected_kinds:
            raise ParseError(self.peek(), f"Unexpected token ({self.peek().kind}), wanted -> {expected_kinds}")

        self.advance()

    def parse_operator(self):
        if self.peek().is_operator():
            return Operator(self.peek().value, self.peek().op_type())

    def parse_variable_declaration(self):
        # identifier: type = value;
        var_name = self.peek().value # identifier
        self.advance_with_expected(TokenKind.tok_id)
        self.advance_with_expected(TokenKind.tok_colon)

        var_type = self.peek().kind # type
        self.advance_with_expected(TokenKind.tok_key_i32, TokenKind.tok_key_f32, TokenKind.tok_key_bool, TokenKind.tok_key_string)
        self.advance_with_expected(TokenKind.tok_assign)

        var_value = self.parse_bin_expr() # value
        self.advance_with_expected(TokenKind.tok_semi)

        return VariableDeclaration(var_name, var_type, var_value)

    def parse_variable_assignment(self):
        # identifier = value;
        var_name = self.peek().value # identifier
        self.advance_with_expected(TokenKind.tok_id)
        self.advance_with_expected(TokenKind.tok_assign)

        var_value = self.parse_bin_expr() # value
        self.advance_with_expected(TokenKind.tok_semi)

        return VariableAssignment(var_name, var_value)

    def parse_primary(self):
        token = self.peek()

        LITERAL_MAP = {
            TokenKind.tok_int: lambda: Number(token.value, LiteralType.type_i32),
            TokenKind.tok_float: lambda: Number(token.value, LiteralType.type_f32),
            TokenKind.tok_string: lambda: String(token.value),
            TokenKind.tok_true: lambda: Boolean(token.value),
            TokenKind.tok_false: lambda: Boolean(token.value),
            TokenKind.tok_id: lambda: Identifier(token.value),
        }

        if token.kind in LITERAL_MAP:
            self.advance()
            return LITERAL_MAP[token.kind]()

        if token.kind == TokenKind.tok_not_op:
            op = self.parse_operator()
            self.advance() # !
            operand = self.parse_primary()
            return UnaryExpr(op, operand)

        if token.kind == TokenKind.tok_dash:
            op = self.parse_operator()
            self.advance() # -
            operand = self.parse_primary()
            return UnaryExpr(op, operand)

        if token.kind == TokenKind.tok_open_paren:
            self.advance()  # (
            expr = self.parse_bin_expr()
            self.advance_with_expected(TokenKind.tok_close_paren)  # )
            return expr

        if token.kind == TokenKind.tok_echo:
            # echo(expr)
            self.advance() # echo
            self.advance_with_expected(TokenKind.tok_open_paren)  # (
            param = self.parse_bin_expr()

            self.advance_with_expected(TokenKind.tok_close_paren)  # )
            # self.advance_with_expected(TokenKind.tok_semi)

            echo_node = EchoBuiltin(param)
            return echo_node

        if token.kind == TokenKind.tok_if:
            # if (expr) {
            #     body
            # }

            self.advance() # if
            self.advance_with_expected(TokenKind.tok_open_paren)  # (
            condition = self.parse_bin_expr()

            self.advance_with_expected(TokenKind.tok_close_paren)  # )
            self.advance_with_expected(TokenKind.tok_open_brace)  # {

            body_tokens = []
            while self.peek().kind != TokenKind.tok_close_brace:
                body_tokens.append(self.peek())
                self.advance()

            body = parse(body_tokens)
            print(body)

            self.advance_with_expected(TokenKind.tok_close_brace)  # {

            
            if_node = IfStmt(condition, body)
            return if_node
            
        if token.kind == TokenKind.tok_while:
            # while (expr) {
            #     body
            # }

            self.advance() # while
            self.advance_with_expected(TokenKind.tok_open_paren)  # (
            condition = self.parse_bin_expr()

            self.advance_with_expected(TokenKind.tok_close_paren)  # )
            self.advance_with_expected(TokenKind.tok_open_brace)  # {

            body_tokens = []
            while self.peek().kind != TokenKind.tok_close_brace:
                body_tokens.append(self.peek())
                self.advance()

            body = parse(body_tokens)
            print(body)

            self.advance_with_expected(TokenKind.tok_close_brace)  # {

            
            while_node = WhileStmt(condition, body)
            return while_node

        raise ParseError(token, f"Unexpected token ({token.kind})")

    def parse_bin_expr(self, min_precedence=0):
        if self.peek().kind == TokenKind.tok_semi:
            return

        lhs = self.parse_primary()

        while self.peek().kind in PRECEDENCE and PRECEDENCE[self.peek().kind] >= min_precedence:
            if self.peek().kind == TokenKind.tok_semi:
                break

            op = self.parse_operator()
            op_precendence = PRECEDENCE[self.peek().kind]
            self.advance()

            rhs = self.parse_bin_expr(op_precendence + 1)

            lhs = BinaryExpr(lhs, op, rhs)

        return lhs

def parse(token_array):
    parser = Parser(token_array)
    root = ASTRoot()

    while parser.position < len(parser.tokens):
        if parser.peek().kind == TokenKind.tok_id and parser.peek_offset(1).kind == TokenKind.tok_colon:
            var_decl = parser.parse_variable_declaration()
            if var_decl == None:
                break

            # print(var_decl)
            root.append_child(var_decl)
        elif parser.peek().kind == TokenKind.tok_id and parser.peek_offset(1).kind == TokenKind.tok_assign:
            var_assign = parser.parse_variable_assignment()
            if var_assign == None:
                break

            # print(var_assign)
            root.append_child(var_assign)
        else:
            expr = parser.parse_bin_expr()
            print(token_array)
            parser.advance_with_expected(TokenKind.tok_semi)
            if expr == None:
                break

            # print(expr)
            root.append_child(expr)

    return root