import re
from parsec import generate, string, regex, many, optional, Parser, ParseError, sepBy, try_choice, eof
from langAST import *

whitespace = regex(r'\s*', re.MULTILINE)
lexeme = lambda p: p << whitespace

# Tokens básicos
lparen = lexeme(string('('))
rparen = lexeme(string(')'))
lbrace = lexeme(string('{'))
rbrace = lexeme(string('}'))
semi = lexeme(string(';'))
comma = lexeme(string(','))
eq = lexeme(string('='))
ident = lexeme(regex(r'[a-zA-Z_][a-zA-Z0-9_]*'))
type_parser = lexeme(regex(r'\b(?:int|float|char|bool|void)\b'))

def attempt(p):
    @Parser
    def attempt_parser(text, index):
        try:
            return p(text, index)
        except ParseError:
            return ParseError(text, index, ["attempt"])
    return attempt_parser

class Forward(Parser):
    def __init__(self):
        self.parser = None
    
    def define(self, parser):
        self.parser = parser
        return self
    
    def __call__(self, text, index):
        if self.parser is None:
            raise ValueError("Forward parser não definido")
        return self.parser(text, index)

def choice_parser(*parsers):
    if not parsers:
        raise ValueError("Pelo menos um parser deve ser fornecido")
    
    result = parsers[0]
    for p in parsers[1:]:
        result = try_choice(result, p)
    
    return result

# ------ PARSERS BÁSICOS ------

def parse_int():
    return lexeme(regex(r'-?[0-9]+')).parsecmap(lambda s: Literal(int(s)))

def parse_float():
    return lexeme(regex(r'-?[0-9]+\.[0-9]+')).parsecmap(lambda s: Literal(float(s)))

def parse_string():
    quoted = lexeme(regex(r'"[^"]*"'))
    return quoted.parsecmap(lambda s: Literal(s[1:-1]))

def parse_bool():
    true = lexeme(string('true')).result(Literal(True))
    false = lexeme(string('false')).result(Literal(False))
    return true | false

@generate
def parse_variable():
    name = yield ident
    return Variable(name)

# ------ EXPRESSÕES  ------
parse_expr = Forward()

@generate
def parse_paren_expr():
    yield lparen
    expr = yield parse_expr  
    yield rparen
    return expr

@generate
def parse_function_call():
    name = yield ident
    yield lparen
    args = yield sepBy(parse_expr, comma)
    yield rparen
    return FunctionCall(name, args)

@generate
def parse_primary():
    """Parse primary expressions: literals, variables, parenthesized expressions, function calls"""
    expr = yield choice_parser(
        attempt(parse_function_call),
        attempt(parse_int()),
        attempt(parse_float()),
        attempt(parse_string()),
        attempt(parse_bool()),
        attempt(parse_paren_expr),
        parse_variable
    )
    return expr

# Expressões unárias
@generate
def parse_unary():
    op = yield optional(lexeme(string('++')) | lexeme(string('--')) | lexeme(string('!')))
    expr = yield parse_primary
    post_op = yield optional(lexeme(string('++')) | lexeme(string('--')))

    if op and post_op:
        raise Exception("Não é possível ter operador pré e pós ao mesmo tempo")

    if op:
        return UnaryOp(op, expr, prefix=True)
    elif post_op:
        return UnaryOp(post_op, expr, prefix=False)
    else:
        return expr

@generate
def parse_factor():
    left = yield parse_unary
    rest = yield many(
        ((lexeme(string('*')) | lexeme(string('/')) | lexeme(string('%'))) + parse_unary)
    )
    
    result = left
    for op, right in rest:
        result = BinaryOp(result, op, right)
    
    return result

@generate
def parse_term():
    left = yield parse_factor
    rest = yield many(
        ((lexeme(string('+')) | lexeme(string('-'))) + parse_factor)
    )
    
    result = left
    for op, right in rest:
        result = BinaryOp(result, op, right)
    
    return result

lt_op = lexeme(string('<'))
gt_op = lexeme(string('>'))
le_op = lexeme(string('<='))
ge_op = lexeme(string('>='))
eq_op = lexeme(string('=='))  
ne_op = lexeme(string('!='))

@generate
def parse_comparison():
    left = yield parse_term
    op = yield optional(choice_parser(le_op, ge_op, eq_op, ne_op, lt_op, gt_op))
    
    if op:
        right = yield parse_term
        return BinaryOp(left, op, right)
    else:
        return left

@generate
def parse_logical_and():
    left = yield parse_comparison
    rest = yield many(lexeme(string('&&')) >> parse_comparison)
    
    result = left
    for right in rest:
        result = BinaryOp(result, '&&', right)
    
    return result

@generate
def parse_logical_or():
    left = yield parse_logical_and
    rest = yield many(lexeme(string('||')) >> parse_logical_and)
    
    result = left
    for right in rest:
        result = BinaryOp(result, '||', right)
    
    return result

@generate
def parse_assignment():
    var = yield ident
    yield eq
    expr = yield parse_expr
    return Assignment(var, expr)

parse_expr.define(choice_parser(
    attempt(parse_assignment),
    parse_logical_or   
))

# ------ STATEMENTS ------

parse_stmt = Forward()

@generate
def parse_expr_stmt():
    """Parse an expression statement: expr;"""
    expr = yield parse_expr
    yield semi
    return ExprStmt(expr)

@generate
def parse_var_decl():
    type_name = yield type_parser
    name = yield ident  
    init = yield optional(eq >> parse_expr)
    yield semi
    return VarDecl(type_name, name, init)

@generate
def parse_if():
    yield lexeme(string('if'))
    yield lparen
    condition = yield parse_expr
    yield rparen
    then_branch = yield parse_stmt
    else_branch = yield optional(lexeme(string('else')) >> parse_stmt)
    return If(condition, then_branch, else_branch)

@generate
def parse_while():
    yield lexeme(string('while'))
    yield lparen
    condition = yield parse_expr
    yield rparen
    body = yield parse_stmt
    return While(condition, body)

@generate
def parse_for():
    yield lexeme(string('for'))
    yield lparen

    init = yield choice_parser(
        parse_var_decl,
        (parse_expr << semi).parsecmap(lambda e: ExprStmt(e))
    )

    condition = yield parse_expr
    yield semi
    increment = yield parse_expr
    yield rparen
    body = yield parse_stmt
    return For(init, condition, increment, body)


@generate
def parse_print():
    yield lexeme(string('print'))
    yield lparen
    expr = yield parse_expr
    yield rparen
    yield semi
    return Print(expr)

@generate
def parse_return():
    yield lexeme(string('return'))
    value = yield optional(parse_expr)  
    yield semi
    return Return(value)

@generate
def parse_block():
    yield lbrace
    yield whitespace
    statements = yield sepBy(parse_stmt, whitespace)
    yield whitespace
    yield rbrace
    return Block(statements)

@generate
def parse_function():
    return_type = yield type_parser
    name = yield ident
    yield lparen
    params = yield optional(sepBy(
        (type_parser + ident).parsecmap(lambda t_n: VarDecl(t_n[0], t_n[1])),
        comma
    ))
    yield rparen
    body = yield parse_block
    yield whitespace
    return Function(return_type, name, params or [], body)


parse_stmt.define(choice_parser(
    attempt(parse_var_decl),
    attempt(parse_block),
    attempt(parse_if),
    attempt(parse_while),
    attempt(parse_for),
    attempt(parse_return),
    attempt(parse_print),
    parse_expr_stmt
))

@generate 
def parse_program():
    yield whitespace
    functions = yield sepBy(parse_function, whitespace)
    yield whitespace
    return Program(functions, [])

def parse_code(code: str) -> Program:
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse_program()