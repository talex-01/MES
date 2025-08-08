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

def expr_to_str(expr):
    if isinstance(expr, Literal):
        return str(expr.value)
    elif isinstance(expr, Variable):
        return expr.name
    elif isinstance(expr, Assignment):
        return f"{expr.var} = {expr_to_str(expr.expr)}"
    elif isinstance(expr, BinaryOp):
        left = expr_to_str(expr.left)
        right = expr_to_str(expr.right)
        return f"({left} {expr.op} {right})"
    elif isinstance(expr, UnaryOp):
        inner = expr_to_str(expr.expr)
        if expr.prefix:
            return f"({expr.op}{inner})"
        else:
            return f"({inner}{expr.op})"
    elif isinstance(expr, FunctionCall):
        args_str = ", ".join(expr_to_str(a) for a in expr.args)
        return f"{expr.name}({args_str})"
    else:
        return f"<expr desconhecido: {expr}>"

def _eval_expr_trace(expr, env, functions, trace_log, current_func_name=None):
    if isinstance(expr, Literal):
        return expr.value
    elif isinstance(expr, Variable):
        return env.get(expr.name)
    elif isinstance(expr, Assignment):
        value = _eval_expr_trace(expr.expr, env, functions, trace_log, current_func_name)
        env.set(expr.var, value)
        return value
    elif isinstance(expr, BinaryOp):
        left = _eval_expr_trace(expr.left, env, functions, trace_log, current_func_name)
        right = _eval_expr_trace(expr.right, env, functions, trace_log, current_func_name)
        if expr.op == '+': return left + right
        elif expr.op == '-': return left - right
        elif expr.op == '*': return left * right
        elif expr.op == '/': return left // right
        elif expr.op == '%': return left % right
        elif expr.op == '==': return left == right
        elif expr.op == '!=': return left != right
        elif expr.op == '<': return left < right
        elif expr.op == '>': return left > right
        elif expr.op == '<=': return left <= right
        elif expr.op == '>=': return left >= right
        elif expr.op == '&&': return bool(left) and bool(right)
        elif expr.op == '||': return bool(left) or bool(right)
        else: raise Exception(f"Operador binário inválido: {expr.op}")
    elif isinstance(expr, UnaryOp):
        value = _eval_expr_trace(expr.expr, env, functions, trace_log, current_func_name)
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
    elif isinstance(expr, FunctionCall):
        func = next((f for f in functions if f.name == expr.name), None)
        if not func:
            raise Exception(f"Função '{expr.name}' não definida.")
        args = [_eval_expr_trace(arg, env, functions, trace_log, current_func_name) for arg in expr.args]
        call_env = Environment()
        for param, val in zip(func.params, args):
            call_env.declare(param.name, val)
        try:
            # Reinicia instr_id para cada chamada de função e usa o nome correto na trace
            _exec_block_trace(func.body, call_env, functions, trace_log, current_func_name=expr.name, start_id=1)
        except ReturnException as r:
            return r.value
        return 0
    else:
        raise Exception(f"Expressão desconhecida: {expr}")

def _exec_stmt_trace(stmt, env, functions, trace_log, current_func_name=None, instr_id=1):
    prefix = f"[{current_func_name}] "

    def log(msg):
        trace_log.append(f"{prefix}Instrução {instr_id}: {msg}")

    if isinstance(stmt, VarDecl):
        value = _eval_expr_trace(stmt.init, env, functions, trace_log, current_func_name) if stmt.init else 0
        env.declare(stmt.name, value)
        log(f"VarDecl {stmt.type} {stmt.name} = {value}")

    elif isinstance(stmt, ExprStmt):
        expr_str = expr_to_str(stmt.expr)
        val = _eval_expr_trace(stmt.expr, env, functions, trace_log, current_func_name)
        log(f"ExprStmt {expr_str} = {val}")

    elif isinstance(stmt, Print):
        val = _eval_expr_trace(stmt.expr, env, functions, trace_log, current_func_name)
        log(f"Print {val}")
        trace_log.append(f"{prefix}{val}")

    elif isinstance(stmt, Return):
        value = _eval_expr_trace(stmt.value, env, functions, trace_log, current_func_name) if stmt.value else 0
        log(f"Return {value}")
        raise ReturnException(value)

    elif isinstance(stmt, Block):
        # Sem logs de entrada/saída de bloco para simplicidade
        next_id = _exec_block_trace(stmt, Environment(env), functions, trace_log, current_func_name, start_id=instr_id + 1)
        return next_id

    elif isinstance(stmt, If):
        cond_val = _eval_expr_trace(stmt.condition, env, functions, trace_log, current_func_name)
        cond_str = expr_to_str(stmt.condition)
        trace_log.append(f"{prefix}If cond: {cond_str} → {cond_val}")
        if cond_val:
            next_id = _exec_stmt_trace(stmt.then_branch, env, functions, trace_log, current_func_name, instr_id + 1)
        elif stmt.else_branch:
            next_id = _exec_stmt_trace(stmt.else_branch, env, functions, trace_log, current_func_name, instr_id + 1)
        else:
            next_id = instr_id + 1
        return next_id

    elif isinstance(stmt, While):
        cond_str = expr_to_str(stmt.condition)
        loop_id = instr_id + 1
        while _eval_expr_trace(stmt.condition, env, functions, trace_log, current_func_name):
            try:
                loop_id = _exec_stmt_trace(stmt.body, env, functions, trace_log, current_func_name, loop_id)
            except ReturnException as r:
                raise r
        return loop_id

    elif isinstance(stmt, For):
        loop_env = Environment(env)
        next_id = instr_id
        if stmt.init:
            next_id = _exec_stmt_trace(stmt.init, loop_env, functions, trace_log, current_func_name, next_id)
        cond_str = expr_to_str(stmt.condition)
        while _eval_expr_trace(stmt.condition, loop_env, functions, trace_log, current_func_name):
            try:
                next_id = _exec_stmt_trace(stmt.body, loop_env, functions, trace_log, current_func_name, next_id)
            except ReturnException as r:
                raise r
            if stmt.increment:
                _eval_expr_trace(stmt.increment, loop_env, functions, trace_log, current_func_name)
        return next_id

    else:
        raise Exception(f"Instrução desconhecida: {stmt}")

    return instr_id + 1

def _exec_block_trace(block, env, functions, trace_log, current_func_name=None, start_id=1):
    instr_id = start_id
    for stmt in block.statements:
        instr_id = _exec_stmt_trace(stmt, env, functions, trace_log, current_func_name, instr_id)
    return instr_id

def evaluate_with_trace(ast: Program, inputs: list[tuple[str, int]]) -> tuple[int, list[str]]:
    global_env = Environment()
    for name, val in inputs:
        global_env.declare(name, val)

    main = next((f for f in ast.functions if f.name == 'main'), None)
    if not main:
        raise Exception("Função main não encontrada.")

    trace_log = []
    try:
        _exec_block_trace(main.body, global_env, ast.functions, trace_log, current_func_name='main', start_id=1)
    except ReturnException as r:
        return r.value, trace_log
    return 0, trace_log

def instrumentation(ast: Program) -> Program:
    def instrument_block(block: Block) -> Block:
        new_statements = []
        for stmt in block.statements:
            if isinstance(stmt, Block):
                new_statements.append(instrument_block(stmt))
            else:
                new_statements.append(stmt)
            new_statements.append(Print(Literal(f"Executou: {type(stmt).__name__}")))
        return Block(new_statements)

    new_functions = []
    for func in ast.functions:
        new_body = instrument_block(func.body)
        new_functions.append(Function(func.return_type, func.name, func.params, new_body))

    return Program(new_functions, ast.global_vars)

def instrumentedTestSuite(ast: Program, testCases: list[tuple[dict, int]]) -> bool:
    instrumented_ast = instrumentation(ast)
    all_passed = True

    for i, (inputs_dict, expected) in enumerate(testCases):
        inputs = list(inputs_dict.items())
        result, trace_log = evaluate_with_trace(instrumented_ast, inputs)

        print(f"\nTeste {i+1} com inputs {inputs_dict}: Esperado={expected}, Obtido={result}")
        print("Log da execução:")
        for linha in trace_log:
            print("  " + linha)
        print("-" * 40)

        if result != expected:
            print(f"ERRO: Resultado do teste {i+1} não corresponde ao esperado.")
            all_passed = False

    return all_passed


# Lista dos programas com apenas 3 testes cada
# Lista dos programas com apenas 3 testes cada
programas = [
    ("programa1", programa1, [
        ({"num": 1}, 1),      # base case
        ({"num": 3}, 6),      # 3! = 6
        ({"num": 5}, 120),    # 5! = 120
    ]),
    
    ("programa2", programa2, [
        ({"n": 2}, 1),        # fib(2) = 1
        ({"n": 5}, 3),        # fib seq: 0,1,1,2,3 → fib2 = 3
        ({"n": 7}, 8),        # fib2 = 8 (0,1,1,2,3,5,8)
    ]),

    ("programa3", programa3, [
        ({"number": 2}, 1),   # primo
        ({"number": 15}, 0),   # não primo
        ({"number": 17}, 1),   # primo
    ]),

    ("programa4", programa4, [
        ({"x": 10, "y": 5, "z": 0}, 35),  
        ({"x": -5, "y": 2, "z": 10}, 17),  
        ({"x": 0, "y": 0, "z": 0}, 20),    
    ]),
]


def run_all_tests():
    for name, program_code, test_cases in programas:
        print(f"\nExecutando testes para {name}...")
        ast = parse_code(program_code)
        passed = instrumentedTestSuite(ast, test_cases)
        print(f"Todos testes passaram: {passed}\n{'='*50}")

if __name__ == "__main__":
    run_all_tests()
