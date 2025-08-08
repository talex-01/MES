from lang_parser import *
def test_parse_code_comprehensive():
    """Teste abrangente para a função parse_code"""
    print("=== TESTE ABRANGENTE DE PARSE_CODE ===\n")
    
    test_cases = [
        {
            "name": "Função Simples",
            "code": """
int main() {
    return 0;
}
""",
            "expected_functions": 1
        },
        {
            "name": "Múltiplas Funções",
            "code": """
int main() {
    num = 5;
    int result = square(num);
    return result;
}
int square(int x) {
    x = x * 2;
    return x;
}

""",
            "expected_functions": 2
        },
        {
            "name": "Função com Chamadas Recursivas",
            "code": """
int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return 0;
}

int main() {
    num = 5;
    int result = factorial(num*2);
    return result;
}
""",
            "expected_functions": 2
        }
    ]
    
    for test in test_cases:
        print(f"Testando: {test['name']}")
        
        try:
            # Chame parse_code como uma função
            result = parse_code(test["code"])
            
            print(f"✓ Parsing bem-sucedido!")
            print(f"  Número de funções: {len(result.functions)}")
            
            if len(result.functions) == test["expected_functions"]:
                print(f"  ✓ Número de funções correto")
            else:
                print(f"  ✗ Número de funções incorreto (esperado {test['expected_functions']}, encontrado {len(result.functions)})")
            
            # Verificar as funções
            for i, func in enumerate(result.functions):
                print(f"  Função {i+1}: {func.name} ({func.return_type})")
                print(f"    Número de parâmetros: {len(func.params)}")
                print(f"    Número de statements no corpo: {func.body.statements}")
        except Exception as e:
            print(f"✗ Erro ao parsear: {e}")
        
        print()
    
    print("=== FIM DO TESTE ===")
test_parse_code_comprehensive()