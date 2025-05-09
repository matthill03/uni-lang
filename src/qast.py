from enum import Enum
from tokens import TokenKind, OperatorType

class QwrkRuntimeError(RuntimeError):
    def __init__(self, node, message):
        super().__init__(message)
        self.node = node
        self.message = message

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.message

class SymbolTableEntry:
    def __init__(self, type, value, parameters=None):
        self.type = type
        self.value = value
        self.parameters = parameters

class ASTContext:
    def __init__(self, parent=None):
        self.parent = parent
        self.variables = {}

    def get_variable(self, var_name):
        if var_name not in self.variables:
            if self.parent is None:
                raise QwrkRuntimeError(self, f"Undefined variable ({var_name})")

            return self.parent.get_variable(var_name)

        return self.variables[var_name]

    def set_new_function(self, fn_name, return_type, parameters, body):
        if fn_name in self.variables:
            raise QwrkRuntimeError(self, f"Function name already exists ({fn_name})")
        
        for param in parameters:
            body.context.set_new_variable(param[0], param[1], None)
        
        self.variables[fn_name] = SymbolTableEntry(return_type, body, parameters)

    def set_new_variable(self, var_name, type, value):
        if var_name in self.variables:
            if self.parent is None:
                raise QwrkRuntimeError(self, f"Variable name already exists ({var_name})")

            try:
                par_var = self.parent.get_variable(var_name)
            except:
                print("Var does not exist")


        self.variables[var_name] = SymbolTableEntry(type, value)

    def set_existing_variable(self, var_name, value):
        if var_name not in self.variables:
            if self.parent is None:
                raise QwrkRuntimeError(self, f"Undefined variable ({var_name})")

            self.parent.set_existing_variable(var_name, value)

        var = self.get_variable(var_name)
        var.value = value

class LiteralType(Enum):
    type_i32 = 0,
    type_f32 = 1,
    type_string = 2,
    type_bool = 3,

TOKEN_TO_LITERAL_TYPE = {
    TokenKind.tok_key_i32: LiteralType.type_i32,
    TokenKind.tok_key_f32: LiteralType.type_f32,
    TokenKind.tok_key_string: LiteralType.type_string,
    TokenKind.tok_key_bool: LiteralType.type_bool,
}

def token_to_literal_type(tok_type):
    if tok_type in TOKEN_TO_LITERAL_TYPE:
        return TOKEN_TO_LITERAL_TYPE[tok_type]
    
    return None

class ASTNodeKind(Enum):
    # Root
    ast_root = 7,
    ast_fn_body = 15,

    # Literals
    ast_num = 0,
    ast_bool = 1,
    ast_str = 2,
    ast_op = 3,
    ast_id = 8,

    # Expressions/Statements
    ast_var_decl = 4,
    ast_var_assign = 9,
    ast_if_stmt = 10,
    ast_while_stmt = 11,
    ast_return_stmt = 14,
    ast_unr_expr = 5,
    ast_bin_expr = 6,
    ast_fn_decl = 12,
    ast_fn_call = 13,
    ast_echo_builtin = 16,

class ASTRoot():
    def __init__(self, parent_context=None):
        self.kind = ASTNodeKind.ast_root
        self.context = ASTContext(parent_context)
        self.children = []

    def evaluate(self):
        for child in self.children:
            child.evaluate(self.context)

    def append_child(self, child):
        self.children.append(child)

class Number(ASTRoot):
    def __init__(self, value, type):
        self.kind = ASTNodeKind.ast_num
        self.type = type

        if type == LiteralType.type_f32:
            self.value = float(value)
        elif type == LiteralType.type_i32:
            self.value = int(value)
        else:
            raise QwrkRuntimeError(self, f"Invalid number literal type ({type})")

    def __str__(self):
        return f"(value: {self.value}, type: {self.type})"

    def evaluate(self, context):
        return (self.value, self.type)

class Identifier(ASTRoot):
    def __init__(self, value):
        self.kind = ASTNodeKind.ast_id
        self.value = value

    def __str__(self):
        return f"(Value: {self.value})"

    def evaluate(self, context):
        var = context.get_variable(self.value)
        return (var.value, var.type)

class Boolean(ASTRoot):
    def __init__(self, value):
        self.kind = ASTNodeKind.ast_bool
        self.type = LiteralType.type_bool

        if value == "true":
            self.value = True
        elif value == "false":
            self.value = False
        else:
            raise QwrkRuntimeError(self, f"Invalid bool literal ({value})")

    def __str__(self):
        return f"{self.value}"

    def evaluate(self, context):
        return (self.value, self.type)

class String(ASTRoot):
    def __init__(self, value):
        self.kind = ASTNodeKind.ast_str
        self.type = LiteralType.type_string
        self.value = str(value)

    def __str__(self):
        return f'"{self.value}"'

    def evaluate(self, context):
        return (self.value, self.type)

class Operator(ASTRoot):
    def __init__(self, op, type):
        self.kind = ASTNodeKind.ast_op
        self.type = type
        self.value = op

    def __str__(self):
        return f"{self.value}"

    def evaluate(self, context):
        return self.value

    def is_mathmatical(self):
        if self.type == OperatorType.type_maths:
            return True

        return False

    def is_logical(self):
        if self.type == OperatorType.type_logical:
            return True

        return False

    def is_comp(self):
        if self.type == OperatorType.type_comp:
            return True

        return False

    def is_string_op(self):
        if self.type == OperatorType.type_string:
            return True

        return False

class FunctionBody(ASTRoot):
    def __init__(self, return_type, parent_context):
        self.kind = ASTNodeKind.ast_fn_body
        self.return_type = token_to_literal_type(return_type)
        self.context = ASTContext(parent_context)
        self.children = []

    def __str__(self):
        return f""
    
    def evaluate(self):
        for child in self.children:
            if child.kind == ASTNodeKind.ast_return_stmt:
                ret_val, ret_type = child.evaluate(self.context)

                if ret_type != self.return_type:
                    raise QwrkRuntimeError(self, f"Invalid return type ({ret_type}), expected ({self.return_type}).")

                return ret_val, ret_type
            
            child.evaluate(self.context)
    
    def append_child(self, child):
        self.children.append(child)

class FunctionDeclaration(ASTRoot):
    def __init__(self, name, parameters, return_type, body):
        self.kind = ASTNodeKind.ast_fn_decl
        self.name = name
        self.parameters = parameters
        self.return_type = return_type
        self.body = body

    def __str__(self):
        return f""
    
    def evaluate(self, context):
        if self.return_type in TOKEN_TO_LITERAL_TYPE:
            self.return_type = TOKEN_TO_LITERAL_TYPE[self.return_type]
        else:
            raise QwrkRuntimeError(self, f"Return Type ({self.return_type}) not a supported type")
        
        new_parameters = []
        for parameter in self.parameters:
            param_val = parameter[0]
            param_type = parameter[1]

            if param_type in TOKEN_TO_LITERAL_TYPE:
                param_type = TOKEN_TO_LITERAL_TYPE[param_type]
            else:
                raise QwrkRuntimeError(self, f"({param_val}) -> Parameter Type ({param_type}) not a supported type")
            
            new_parameters.append((param_val, param_type))
        
        self.parameters = new_parameters
            
        context.set_new_function(self.name, self.return_type, self.parameters, self.body)

class FunctionCall(ASTRoot):
    def __init__(self, name, arguments):
        self.kind = ASTNodeKind.ast_fn_call
        self.name = name
        self.arguments = arguments

    def __str__(self):
        return f""
    
    def evaluate(self, context):
        fn = context.get_variable(self.name)

        if len(fn.parameters) != len(self.arguments):
            raise QwrkRuntimeError(self, f"Invalid argument length: ({len(self.arguments)} )given, but expected ({len(fn.parameters)}).")
        
        for i in range(len(fn.parameters)):
            arg = self.arguments[i]
            param = fn.parameters[i]

            arg_val, arg_type = arg.evaluate(context)
            if arg_type != param[1]:
                raise QwrkRuntimeError(self, f"Invalid argument type: ({arg_type}) given, but expected ({param[1]}).")
            
            fn.value.context.set_existing_variable(param[0], arg_val)
        
        return fn.value.evaluate()

class VariableDeclaration(ASTRoot):
    def __init__(self, name, type, value):
        self.kind = ASTNodeKind.ast_var_decl
        self.name = name
        self.type = type
        self.value = value

    def __str__(self):
        return f"(Name: {self.name}, Type: {self.type}, Value: {self.value})"

    def evaluate(self, context):
        if self.type in TOKEN_TO_LITERAL_TYPE:
            self.type = TOKEN_TO_LITERAL_TYPE[self.type]
        else:
            raise QwrkRuntimeError(self, f"({self.name}) -> Type ({self.type}) not a supported type")

        var, var_type = self.value.evaluate(context)
        if var_type != self.type:
            raise QwrkRuntimeError(self, f"Cannot assign type ({var_type}) to type ({self.type})")

        context.set_new_variable(self.name, var_type, var)

class VariableAssignment(ASTRoot):
    def __init__(self, name, value):
        self.kind = ASTNodeKind.ast_var_assign
        self.name = name
        self.value = value

    def __str__(self):
        return f"(Name: {self.name}, Value: {self.value})"

    def evaluate(self, context):
        var = self.value.evaluate(context)
        var_type = context.get_variable(self.name).type

        if var[1] != var_type:
            raise QwrkRuntimeError(self, f"Cannot assign type ({var[1]}) to type ({var_type})")

        context.set_existing_variable(self.name, var[0])

class IfStmt(ASTRoot):
    def __init__(self, condition, body, else_branch=None):
        self.kind = ASTNodeKind.ast_if_stmt
        self.condition = condition
        self.body = body
        self.else_branch = else_branch

    def __str__(self):
        pass

    def evaluate(self, context):
        if self.condition.evaluate(context)[0] == True:
            self.body.evaluate()
        elif self.else_branch:
            self.else_branch.evaluate(context)

class WhileStmt(ASTRoot):
    def __init__(self, condition, body):
        self.kind = ASTNodeKind.ast_while_stmt
        self.condition = condition
        self.body = body

    def __str__(self):
        pass

    def evaluate(self, context):
        while self.condition.evaluate(context)[0] == True:
            self.body.evaluate()

class UnaryExpr(ASTRoot):
    def __init__(self, op, stmt):
        self.kind = ASTNodeKind.ast_unr_expr
        self.op = op
        self.stmt = stmt

    def __str__(self):
        return f"(op: {self.op}, stmt: {self.stmt})"

    def evaluate(self, context):
        operand, operand_type = self.stmt.evaluate(context)
        op = self.op.evaluate(context)

        if op == '!':
            return (not operand, LiteralType.type_bool)
        if op == '-':
            if operand_type != LiteralType.type_f32 and operand_type != LiteralType.type_i32:
                raise QwrkRuntimeError(self, f"Invalid operand for '-' ({operand} -> {operand_type})") 

            return (-operand, operand_type)
        else:
            raise QwrkRuntimeError(self, f"Unknown unary operator ({op})")

class BinaryExpr(ASTRoot):
    def __init__(self, lhs, op, rhs):
        self.kind = ASTNodeKind.ast_bin_expr
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def __str__(self):
        return f"(lhs: {self.lhs}, op: {self.op}, rhs: {self.rhs})"

    def evaluate_arithmatic(self, op, context):
        lhs, lhs_type = self.lhs.evaluate(context)
        rhs, rhs_type = self.rhs.evaluate(context)

        if lhs_type != LiteralType.type_i32 and lhs_type != LiteralType.type_f32:
            raise QwrkRuntimeError(self, f"Invalid Arethmatic operation type ({lhs_type})")

        if rhs_type != LiteralType.type_i32 and rhs_type != LiteralType.type_f32:
            raise QwrkRuntimeError(self, f"Invalid Arethmatic operation type ({rhs_type})")

        if op == '+':
            return lhs + rhs, lhs_type
        elif op == '-':
            return lhs - rhs, lhs_type
        elif op == '*':
            return lhs * rhs, lhs_type
        elif op == '/':
            return lhs / rhs, lhs_type
        elif op == '%':
            return lhs % rhs, lhs_type

    def evaluate_logical(self, op, context):
        lhs, lhs_type = self.lhs.evaluate(context)
        rhs, rhs_type = self.rhs.evaluate(context)

        if lhs_type == LiteralType.type_bool and rhs_type != LiteralType.type_bool:
            raise QwrkRuntimeError(self, f"Incompatible types ({lhs_type} - {rhs_type})")

        elif op == '&&':
            return lhs and rhs, LiteralType.type_bool
        elif op == '||':
            return lhs or rhs, LiteralType.type_bool

    def evaluate_comp(self, op, context):
        lhs, lhs_type = self.lhs.evaluate(context)
        rhs, rhs_type = self.rhs.evaluate(context)

        if lhs_type == LiteralType.type_i32 and (rhs_type != LiteralType.type_i32 and rhs_type != LiteralType.type_f32):
            raise QwrkRuntimeError(self, f"Incompatible types ({lhs_type} - {rhs_type})")

        if lhs_type == LiteralType.type_f32 and (rhs_type != LiteralType.type_i32 and rhs_type != LiteralType.type_f32):
            raise QwrkRuntimeError(self, f"Incompatible types ({lhs_type} - {rhs_type})")

        if lhs_type == LiteralType.type_bool and rhs_type != LiteralType.type_bool:
            raise QwrkRuntimeError(self, f"Incompatible types ({lhs_type} - {rhs_type})")

        if op == '==':
            return lhs == rhs, LiteralType.type_bool
        elif op == '!=':
            return lhs != rhs, LiteralType.type_bool
        elif op == '<':
            return lhs < rhs, LiteralType.type_bool
        elif op == '<=':
            return lhs <= rhs, LiteralType.type_bool
        elif op == '>':
            return lhs > rhs, LiteralType.type_bool
        elif op == '>=':
            return lhs >= rhs, LiteralType.type_bool

    def evaluate_string(self, op, context):
        lhs, lhs_type = self.lhs.evaluate(context)
        rhs, rhs_type = self.rhs.evaluate(context)

        if lhs_type != LiteralType.type_string:
            raise QwrkRuntimeError(self, f"Invalid String operation type ({lhs_type})")

        if rhs_type != LiteralType.type_string:
            raise QwrkRuntimeError(self, f"Invalid String operation type ({rhs_type})")

        if op == '++':
            return lhs + rhs, LiteralType.type_string

    def evaluate(self, context):
        if self.op.is_mathmatical():
            return self.evaluate_arithmatic(self.op.evaluate(context), context)

        if self.op.is_logical():
            return self.evaluate_logical(self.op.evaluate(context), context)

        if self.op.is_comp():
            return self.evaluate_comp(self.op.evaluate(context), context)

        if self.op.is_string_op():
            return self.evaluate_string(self.op.evaluate(context), context)

        raise QwrkRuntimeError(self, f"Unknown Operator ({self.op.value})")

class EchoBuiltin(ASTRoot):
    def __init__(self, value):
        self.kind = ASTNodeKind.ast_echo_builtin
        self.value = value

    def __str__(self):
        return f"(Value: {self.value})"
    
    def evaluate(self, context):
        print(self.value.evaluate(context)[0])

 # type: ignore

class ReturnExpr(ASTRoot):
    def __init__(self, expr):
        self.kind = ASTNodeKind.ast_return_stmt
        self.expr = expr

    def __str__(self):
        return f""
    
    def evaluate(self, context):
        return self.expr.evaluate(context)