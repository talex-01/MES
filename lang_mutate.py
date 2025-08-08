import copy
import random
import signal

from lang_parser import parse_code
from lang_test import runTestSuite
from prettyPrinting import PrettyPrinter
from testcases import programa1, programa2, programa3, programa4
from langAST import Literal, BinaryOp, Return, Assignment, If

# --- Timeout para abortar testes demorados ---
class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException()

signal.signal(signal.SIGALRM, timeout_handler)

# --- Coleta nós mutáveis do AST ---
def collect_mutable_nodes(node, collected):
    if node is None:
        return
    for attr in dir(node):
        if attr.startswith('_'):
            continue
        child = getattr(node, attr)
        if isinstance(child, list):
            for c in child:
                collect_mutable_nodes(c, collected)
        elif hasattr(child, '__dict__'):
            collect_mutable_nodes(child, collected)
    if isinstance(node, (Literal, BinaryOp, Return, Assignment, If)):
        collected.append(node)

# --- Aplica mutação válida num nó do AST ---
def mutate_node(node, ast_str_hint=""):
    if isinstance(node, Literal):
        if isinstance(node.value, int):
            if node.value in [0, 1]:
                return False
            delta = random.choice([-2, -1, 1, 2])
            novo_valor = node.value + delta
            if novo_valor <= 0:
                return False
            node.value = novo_valor
            return True

    elif isinstance(node, BinaryOp):
        # Apenas operadores seguros para troca (sem / e %)
        aritmeticos = ['+', '-', '*']
        if node.op in aritmeticos:
            ops = [op for op in aritmeticos if op != node.op]

            if not ops:
                return False

            new_op = random.choice(ops)
            node.op = new_op
            return True

        # Troca sinais em condições if para isPrime (opcional)
        if 'isPrime' in ast_str_hint:
            if node.op == '==':
                node.op = '!='
                return True
            elif node.op == '!=':
                node.op = '=='
                return True
            elif node.op == '%':
                node.op = '*'
                return True
            elif node.op in ['<=', '<', '>=', '>']:
                inversoes = {'<=':'>', '<':'>=', '>=':'<', '>':'<='}
                node.op = inversoes.get(node.op, node.op)
                return True

    elif isinstance(node, If):
        cond = getattr(node, 'cond', None)
        if isinstance(cond, BinaryOp):
            if cond.op in ['<=', '<', '>=', '>']:
                if isinstance(cond.right, Literal):
                    if cond.right.value in [0,1] and ('factorial' in ast_str_hint or 'soma' in ast_str_hint):
                        return False
                    if isinstance(cond.right.value, int):
                        novo_valor = cond.right.value + random.choice([-1, 1])
                        if novo_valor >= 0:
                            cond.right.value = novo_valor
                            return True

    elif isinstance(node, Assignment):
        lit = getattr(node, 'value', None)
        if isinstance(lit, Literal):
            if lit.value in [0, 1]:
                return False
            if isinstance(lit.value, int):
                novo_valor = lit.value + random.choice([-1, 1])
                if novo_valor > 0:
                    lit.value = novo_valor
                    return True
    return False

# --- Aplica múltiplas mutações no AST (pelo menos uma) ---
def mutate_ast_one(ast, min_mutations=1, max_mutations=None):
    ast_str_hint = str(ast)[:200]
    mutable_nodes = []
    collect_mutable_nodes(ast, mutable_nodes)

    if not mutable_nodes:
        return None

    # Define max_mutations baseado no número de nós mutáveis se não passado
    if max_mutations is None:
        max_mutations = random.randint(min_mutations, max(1, len(mutable_nodes)))

    ast_copy = copy.deepcopy(ast)
    nodes_copy = []
    collect_mutable_nodes(ast_copy, nodes_copy)
    random.shuffle(nodes_copy)

    mutacoes_aplicadas = 0
    for node in nodes_copy:
        if mutate_node(node, ast_str_hint):
            mutacoes_aplicadas += 1
        if mutacoes_aplicadas >= max_mutations:
            break

    if mutacoes_aplicadas == 0:
        return None
    return ast_copy

# --- Testa mutações com tentativas para evitar mutantes problemáticos ---
def testar_mutacoes(codigo:str, testCases, max_tentativas=10):
    ast = parse_code(codigo)
    attempts = 0

    while attempts < max_tentativas:
        mutante = mutate_ast_one(ast)
        if not mutante:
            print("Nenhuma mutação aplicada, tentando novamente.")
            attempts += 1
            continue
        
        printer = PrettyPrinter(indent_size=2)
        codigo_mutado = printer.pprint(mutante)

        try:
            signal.alarm(5)  # Timeout 5 segundos

            runTestSuite(codigo_mutado, testCases)

            signal.alarm(0)  # Desliga timeout

            print(f"\n=== Mutante do programa encontrado na tentativa {attempts + 1} ===\n")
            print(codigo_mutado)
            print("\n--- Resultados dos testes ---\n")

            return attempts + 1, codigo_mutado

        except TimeoutException:
            print(f"Tentativa {attempts + 1}: Timeout - mutante possivelmente infinito, tentando outro...")
        except RecursionError:
            print(f"Tentativa {attempts + 1}: Recursão infinita detectada, tentando outro mutante...")
        except Exception as e:
            print(f"Tentativa {attempts + 1}: Erro durante testes: {e}, tentando outro mutante...")

        attempts += 1

    print(f"Não foi possível gerar um mutante válido após {max_tentativas} tentativas.")
    return attempts, None

# --- Testa os programas ---
if __name__ == "__main__":
    programas = [
        ("programa1", programa1, [
            ({"num": 10}, 3628800),
            ({"num": 3}, 6),
            ({"num": 1}, 1),
        ]),
        ("programa2", programa2, [
            ({"n": 5}, 5),
            ({"n": 10}, 55),
            ({"n": 1}, 1),
        ]),
        ("programa3", programa3, [
            ({"number": 2}, 1),
            ({"number": 4}, 0),
            ({"number": 17}, 1),
        ]),
        ("programa4", programa4, [
            ({"x": 10, "y": 5, "z": 0}, 35),
            ({"x": -5, "y": 2, "z": 10}, 17),
            ({"x": 0, "y": 0, "z": 0}, 20),
        ]),
    ]

    for nome, codigo, testCases in programas:
        print(f"\n==== Mutante do programa {nome} ====")
        tentativas, mutante_valido = testar_mutacoes(codigo, testCases)
        print(f"Tentativas feitas: {tentativas}")
        if mutante_valido:
            print("Mutante válido gerado.\n")
        else:
            print("Nenhum mutante válido gerado.\n")
