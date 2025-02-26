import tokens
import ast

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

    def advance_with_expected(self, expected_kinds):
        if self.peek().kind not in expected_kinds:
            print(f"Unexpected token ({self.peek().kind}), wanted -> {expected_kinds}")
            exit(1)

        self.advance()

    def parse_operator(self):
        if self.peek().kind in tokens.OPERATORS:
            return ast.Operator(self.peek().value)
        
    def parse_variable_declaration(self):
        # identifier: type = value;
        var_name = self.peek().value # identifier
        self.advance_with_expected([tokens.TokenKind.tok_id])
        self.advance_with_expected([tokens.TokenKind.tok_colon])

        var_type = self.peek().value # type
        self.advance_with_expected(tokens.TYPES)
        self.advance_with_expected([tokens.TokenKind.tok_assign])

        var_value = self.parse_bin_expr() # value
        self.advance_with_expected([tokens.TokenKind.tok_semi])

        return ast.VariableDeclaration(var_name, var_type, var_value)

    def parse_primary(self):
        if self.peek().kind == tokens.TokenKind.tok_int:
            num = ast.Number(self.peek().value, ast.LiteralType.type_int)
            self.advance()
            return num

        if self.peek().kind == tokens.TokenKind.tok_float:
            num = ast.Number(self.peek().value, ast.LiteralType.type_float)
            self.advance()
            return num

        if self.peek().kind == tokens.TokenKind.tok_string:
            num = ast.String(self.peek().value)
            self.advance()
            return num

        if self.peek().kind == tokens.TokenKind.tok_true:
            bol = ast.Boolean(self.peek().value)
            self.advance()
            return bol

        if self.peek().kind == tokens.TokenKind.tok_false:
            bol = ast.Boolean(self.peek().value)
            self.advance()
            return bol

        if self.peek().kind == tokens.TokenKind.tok_id:
            iden = ast.Identifier(self.peek().value)
            self.advance()
            return iden

        if self.peek().kind == tokens.TokenKind.tok_not_op:
            op = self.parse_operator()
            self.advance() # !
            operand = self.parse_primary()
            return ast.UnaryExpr(op, operand)

        if self.peek().kind == tokens.TokenKind.tok_open_paren:
            self.advance()  # (
            expr = self.parse_bin_expr()
            self.advance_with_expected([tokens.TokenKind.tok_close_paren])  # )
            return expr

        if self.peek().kind == tokens.TokenKind.tok_echo:
            # echo(expr)
            self.advance() # echo
            self.advance_with_expected([tokens.TokenKind.tok_open_paren])  # (
            param = self.parse_bin_expr()

            self.advance_with_expected([tokens.TokenKind.tok_close_paren])  # )
            # self.advance_with_expected([tokens.TokenKind.tok_semi])

            echo_node = ast.EchoBuiltin(param)
            return echo_node

        raise ValueError(f"Unexpected token ({self.peek().kind})")

    def parse_bin_expr(self, min_precedence=0):
        if self.peek().kind == tokens.TokenKind.tok_semi:
            return

        lhs = self.parse_primary()

        while self.peek().kind in ast.PRECEDENCE and ast.PRECEDENCE[self.peek().kind] >= min_precedence:
            if self.peek().kind == tokens.TokenKind.tok_semi:
                break

            op = self.parse_operator()
            op_precendence = ast.PRECEDENCE[self.peek().kind]
            self.advance()

            rhs = self.parse_bin_expr(op_precendence + 1)

            lhs = ast.BinaryExpr(lhs, op, rhs)

        return lhs

def parse(token_array):
    parser = Parser(token_array)
    root = ast.ASTRoot()

    while parser.position < len(parser.tokens):

        if parser.peek().kind == tokens.TokenKind.tok_id and parser.peek_offset(1).kind == tokens.TokenKind.tok_colon:
            var_decl = parser.parse_variable_declaration()
            print(var_decl)
            root.append_child(var_decl)
        else:
            expr = parser.parse_bin_expr()

            if expr == None:
                break

            # parser.advance_with_expected([tokens.TokenKind.tok_semi])

            # print(expr)
            root.append_child(expr)

    root.evaluate()