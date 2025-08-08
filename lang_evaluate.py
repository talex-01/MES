from langAST import *

from lang_parser import parse_code
from testcases import programa1, programa2, programa3, programa4

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class Environment:
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent

    def get(self, name):
        if name in self.vars:
            return self.vars[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise Exception(f"Variável '{name}' não definida.")

    def set(self, name, value):
        if name in self.vars:
            self.vars[name] = value
        elif self.parent:
            self.parent.set(name, value)
        else:
            raise Exception(f"Variável '{name}' não definida para atribuição.")

    def declare(self, name, value):
        self.vars[name] = value

def eval_expr(expr, env, functions):
    if isinstance(expr, Literal):
        return expr.value
    elif isinstance(expr, Variable):
        return env.get(expr.name)
    elif isinstance(expr, Assignment):
        value = eval_expr(expr.expr, env, functions)
        env.set(expr.var, value)
        return value
    elif isinstance(expr, BinaryOp):
        left = eval_expr(expr.left, env, functions)
        right = eval_expr(expr.right, env, functions)
        op = expr.op
        if op == '+': return left + right
        elif op == '-': return left - right
        elif op == '*': return left * right
        elif op == '/': return left // right if isinstance(left, int) else left / right
        elif op == '%': return left % right
        elif op == '==': return left == right
        elif op == '!=': return left != right
        elif op == '<': return left < right
        elif op == '>': return left > right
        elif op == '<=': return left <= right
        elif op == '>=': return left >= right
        elif op == '&&': return bool(left) and bool(right)
        elif op == '||': return bool(left) or bool(right)
        else:
            raise Exception(f"Operador binário inválido: {op}")
    elif isinstance(expr, UnaryOp):
        value = eval_expr(expr.expr, env, functions)
        if expr.op == '-': return -value
        elif expr.op == '!': return not value
        elif expr.op == '++':
            if isinstance(expr.expr, Variable):
                current = env.get(expr.expr.name)
                updated = current + 1
                env.set(expr.expr.name, updated)
                return updated if expr.prefix else current
            else:
                raise Exception("++ só pode ser aplicado a variáveis.")
        else:
            raise Exception(f"Operador unário inválido: {expr.op}")
    elif isinstance(expr, FunctionCall):
        func = next((f for f in functions if f.name == expr.name), None)
        if not func:
            raise Exception(f"Função '{expr.name}' não definida.")
        if len(func.params) != len(expr.args):
            raise Exception("Número incorreto de argumentos.")
        args = [eval_expr(arg, env, functions) for arg in expr.args]
        new_env = Environment()
        for param, arg_val in zip(func.params, args):
            new_env.declare(param.name, arg_val)
        try:
            exec_block(func.body, new_env, functions)
        except ReturnException as r:
            return r.value
        return 0
    else:
        raise Exception(f"Expressão desconhecida: {expr}")

def exec_stmt(stmt, env, functions):
    if isinstance(stmt, VarDecl):
        value = eval_expr(stmt.init, env, functions) if stmt.init else 0
        env.declare(stmt.name, value)
    elif isinstance(stmt, ExprStmt):
        eval_expr(stmt.expr, env, functions)
    elif isinstance(stmt, Print):
        val = eval_expr(stmt.expr, env, functions)
        print(val)
    elif isinstance(stmt, Return):
        value = eval_expr(stmt.value, env, functions) if stmt.value else 0
        raise ReturnException(value)
    elif isinstance(stmt, Block):
        new_env = Environment(parent=env)
        exec_block(stmt, new_env, functions)
    elif isinstance(stmt, If):
        cond = eval_expr(stmt.condition, env, functions)
        if cond:
            exec_stmt(stmt.then_branch, env, functions)
        elif stmt.else_branch:
            exec_stmt(stmt.else_branch, env, functions)
    elif isinstance(stmt, While):
        while eval_expr(stmt.condition, env, functions):
            try:
                exec_stmt(stmt.body, env, functions)
            except ReturnException as r:
                raise r
    elif isinstance(stmt, For):
        loop_env = Environment(parent=env)
        if isinstance(stmt.init, VarDecl):
            exec_stmt(stmt.init, loop_env, functions)
        elif isinstance(stmt.init, ExprStmt):
            eval_expr(stmt.init.expr, loop_env, functions)
        while eval_expr(stmt.condition, loop_env, functions):
            try:
                exec_stmt(stmt.body, loop_env, functions)
            except ReturnException as r:
                raise r
            if stmt.increment:
                eval_expr(stmt.increment, loop_env, functions)
    else:
        raise Exception(f"Instrução desconhecida: {stmt}")

def exec_block(block: Block, env: Environment, functions):
    for stmt in block.statements:
        exec_stmt(stmt, env, functions)

def evaluate(ast: Program, inputs: list[tuple[str, int]]) -> int:
    global_env = Environment()
    for name, value in inputs:
        global_env.declare(name, value)
    
    main_func = next((f for f in ast.functions if f.name == 'main'), None)
    if not main_func:
        raise Exception("Função main não encontrada.")
    
    try:
        exec_block(main_func.body, global_env, ast.functions)
    except ReturnException as r:
        return r.value # retorna o valor do programa
    return -1



if __name__ == "__main__":
    programas = [
        ("programa1", programa1, [("num", 10)]),
        ("programa2", programa2, [("n", 5)]),
        ("programa3", programa3, [("number", 4)]),
        ("programa4", programa4, [("x", 10), ("y", 5), ("z", 0)]),
    ]

    for nome, codigo, inputs in programas:
        print(f"Executando {nome} com inputs {inputs}...")
        ast = parse_code(codigo)
        resultado = evaluate(ast, inputs)
        print(f"Resultado do {nome}: {resultado}\n")
