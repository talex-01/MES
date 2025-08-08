from typing import Tuple, Dict, List

from lang_parser import parse_code
from lang_evaluate import evaluate
from testcases import programa1, programa2, programa3, programa4

# Função para executar um teste unitário:
def runTest(codigo: str, testCase: Tuple[Dict[str, int], int]) -> Tuple[bool, str]:
    inputs, expected = testCase
    ast = parse_code(codigo)
    # Converter dict para lista de tuplas (nome, valor)
    inputs_tuples = list(inputs.items())
    resultado = evaluate(ast, inputs_tuples)
    passou = (resultado == expected)
    msg = f"Test with inputs {inputs}: expected {expected}, got {resultado}. {'PASS' if passou else 'FAIL'}"
    return passou, msg

# Função para executar um conjunto de testes (test suite):
def runTestSuite(codigo: str, testCases: List[Tuple[Dict[str, int], int]]) -> bool:
    todos_passaram = True
    for i, testCase in enumerate(testCases, 1):
        passou, msg = runTest(codigo, testCase)
        print(f"Test {i}: {msg}")
        if not passou:
            todos_passaram = False
    print("\nResultado do Test Suite:", "TODOS PASSARAM" if todos_passaram else "ALGUNS FALHARAM")
    return todos_passaram



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
        ({"x": 10, "y": 5, "z": 0}, 35),   # 42 + 10 + 5 + 0 + 1 + 1
        ({"x": -5, "y": 2, "z": 10}, 17),  # 42 -5 +2 +0 +1 +1
        ({"x": 0, "y": 0, "z": 0}, 20),    # 42 +0 +0 +0 +1 +1
    ]),
]

if __name__ == "__main__":
    for nome, codigo, testCases in programas:
        print(f"\nExecutando test suite: {nome}\n{'='*40}")
        runTestSuite(codigo, testCases)
