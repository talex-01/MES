from lang_parser import *
def test_invalid_programs():
    """Testa programas inválidos que devem ser rejeitados pelo parser"""
    invalid_tests = [
        # Teste 1: Função sem ponto-e-vírgula após return
        {
            "name": "Falta de Ponto-e-Vírgula",
            "code": """
                int main() {
                    return 0
                }
            """,
            "error_desc": "Falta ponto-e-vírgula após o statement return"
        },
        
        # Teste 2: Parêntese não fechado na condição if
        {
            "name": "Parêntese Não Fechado",
            "code": """
                int main() {
                    if (x > 5 {
                        return 1;
                    }
                    return 0;
                }
            """,
            "error_desc": "Parêntese não fechado na condição if"
        },
        
        # Teste 3: Chave não fechada no bloco
        {
            "name": "Chave Não Fechada",
            "code": """
                int main() {
                    {
                        int x = 10;
                    
                    return 0;
                }
            """,
            "error_desc": "Chave de fechamento faltando em um bloco"
        },
        
        # Teste 4: Atribuição com tipos incompatíveis
        {
            "name": "Tipos Incompatíveis",
            "code": """
                int main() {
                    int x = "string";
                    return x;
                }
            """,
            "error_desc": "Atribuição de string a uma variável int"
        },
        
        # Teste 5: Variável não declarada
        {
            "name": "Variável Não Declarada",
            "code": """
                int main() {
                    y = 10;
                    return y;
                }
            """,
            "error_desc": "Uso de variável não declarada"
        },
        
        # Teste 6: Sintaxe incorreta no loop for
        {
            "name": "Erro de Sintaxe no For",
            "code": """
                int main() {
                    for (int i = 0; i < 10) {
                        return i;
                    }
                }
            """,
            "error_desc": "Falta a parte de incremento no loop for"
        },
        
        # Teste 7: Palavra-chave inválida
        {
            "name": "Palavra-chave Inválida",
            "code": """
                int main() {
                    switch (x) {
                        case 1: return 1;
                        default: return 0;
                    }
                }
            """,
            "error_desc": "Uso de palavra-chave 'switch' não suportada pela linguagem"
        },
        
        # Teste 8: Erro de sintaxe em expressão
        {
            "name": "Erro em Expressão",
            "code": """
                int main() {
                    int x = 5 + * 3;
                    return x;
                }
            """,
            "error_desc": "Erro de sintaxe na expressão '5 + * 3'"
        },
        
        # Teste 9: Operador não definido
        {
            "name": "Operador Não Definido",
            "code": """
                int main() {
                    int x = 5 ** 2;  // Operador de potência
                    return x;
                }
            """,
            "error_desc": "Uso de operador '**' não definido na linguagem"
        },
        
        # Teste 10: Função sem tipo de retorno
        {
            "name": "Função Sem Tipo",
            "code": """
                main() {
                    return 0;
                }
            """,
            "error_desc": "Falta o tipo de retorno na definição da função"
        }
    ]
    
    print("=== TESTES DE PROGRAMAS INVÁLIDOS ===")
    
    for i, test in enumerate(invalid_tests, 1):
        print(f"\nTeste {i}: {test['name']}")
        print(f"Erro esperado: {test['error_desc']}")
        print(f"Código:\n{test['code']}")
        
        try:
            result = parse_code(test['code'])
            print(f"✗ Falha no teste: o código inválido foi aceito!")
        except Exception as e:
            print(f"✓ Erro detectado corretamente: {e}")
    
    print("\n=== FIM DOS TESTES INVÁLIDOS ===")

def test_specific_features():
    """Testes específicos para características particulares da linguagem"""
    tests = [
        # Teste 1: Expressões aritméticas complexas
        {
            "name": "Expressões Aritméticas Complexas",
            "code": """
                int main() {
                    int a = 5;
                    int b = 3;
                    int c = 2;
                    int result = a * (b + c) / (a - c) % b;
                    return result;
                }
            """,
            "valid": True,
            "description": "Expressões aritméticas com vários operadores e precedência"
        },
        
        # Teste 2: Incremento pós-fixo em várias situações
        {
            "name": "Incremento Pós-fixo",
            "code": """
                int main() {
                    int i = 0;
                    i++;
                    
                    for (int j = 0; j < 5; j++) {
                        i = i + j++;
                    }
                    
                    return i;
                }
            """,
            "valid": True,
            "description": "Uso de incremento pós-fixo em várias situações"
        },
        
        # Teste 3: Expressões booleanas complexas
        {
            "name": "Expressões Booleanas Complexas",
            "code": """
                int main() {
                    int a = 5;
                    int b = 10;
                    int c = 15;
                    
                    if ((a < b && b < c) || !(a == 5) && (b != 10)) {
                        return 1;
                    }
                    
                    return 0;
                }
            """,
            "valid": True,
            "description": "Expressões booleanas complexas com operadores lógicos"
        },
        
        # Teste 4: Blocos aninhados com escopo
        {
            "name": "Blocos Aninhados com Escopo",
            "code": """
                int main() {
                    int x = 10;
                    {
                        int x = 20;  // Variável com mesmo nome em escopo diferente
                        {
                            int x = 30;  // Outro escopo
                            print(x);    // Deve imprimir 30
                        }
                        print(x);        // Deve imprimir 20
                    }
                    print(x);            // Deve imprimir 10
                    return 0;
                }
            """,
            "valid": True,
            "description": "Blocos aninhados com variáveis de mesmo nome em escopos diferentes"
        },
        
        # Teste 5: Comentários
        {
            "name": "Comentários",
            "code": """
                // Este é um comentário de linha
                int main() {
                    int x = 10; // Comentário após statement
                    /* Este é um comentário
                       de múltiplas linhas */
                    return 0;
                }
            """,
            "valid": True,
            "description": "Programa com comentários de linha e bloco"
        },
        
        # Teste 6: Loops aninhados
        {
            "name": "Loops Aninhados",
            "code": """
                int main() {
                    int sum = 0;
                    
                    for (int i = 0; i < 5; i++) {
                        for (int j = 0; j < 3; j++) {
                            sum = sum + (i * j);
                        }
                    }
                    
                    return sum;
                }
            """,
            "valid": True,
            "description": "Loops for aninhados"
        },
        
        # Teste 7: Operador decremento
        {
            "name": "Operador Decremento",
            "code": """
                int main() {
                    int i = 10;
                    i--;
                    
                    while (i > 0) {
                        i--;
                    }
                    
                    return i;
                }
            """,
            "valid": True,
            "description": "Uso do operador de decremento"
        },
        
        # Teste 8: Print com expressões
        {
            "name": "Print com Expressões",
            "code": """
                int main() {
                    int a = 5;
                    int b = 10;
                    
                    print(a + b);
                    print(a * b);
                    print(a == b);
                    
                    return 0;
                }
            """,
            "valid": True,
            "description": "Uso de print com diferentes tipos de expressões"
        }
    ]
    
    print("=== TESTES DE CARACTERÍSTICAS ESPECÍFICAS ===")
    
    for i, test in enumerate(tests, 1):
        print(f"\nTeste {i}: {test['name']}")
        print(f"Descrição: {test['description']}")
        print(f"Código:\n{test['code']}")
        
        try:
            result = parse_code(test['code'])
            if test['valid']:
                print(f"✓ Sucesso! Código aceito conforme esperado.")
            else:
                print(f"✗ Falha! Código inválido foi aceito.")
        except Exception as e:
            if not test['valid']:
                print(f"✓ Erro detectado corretamente: {e}")
            else:
                print(f"✗ Erro inesperado: {e}")
    
    print("\n=== FIM DOS TESTES ESPECÍFICOS ===")


def test_edge_cases():
    """Testes de casos limítrofes que testam os extremos da linguagem"""
    tests = [
        # Teste 1: Programa vazio (só com a função main)
        {
            "name": "Programa Vazio",
            "code": """
                int main() {
                }
            """,
            "valid": True,
            "description": "Função main sem statements"
        },
        
        # Teste 2: Função sem parâmetros mas com parênteses vazios
        {
            "name": "Função Sem Parâmetros",
            "code": """
                int foo() {
                    return 42;
                }
                
                int main() {
                    return foo();
                }
            """,
            "valid": True,
            "description": "Função sem parâmetros mas com parênteses vazios"
        },
        
        # Teste 3: Função com muitos parâmetros
        {
            "name": "Função com Muitos Parâmetros",
            "code": """
                int sum(int a, int b, int c, int d, int e, int f, int g, int h, int i, int j) {
                    return a + b + c + d + e + f + g + h + i + j;
                }
                
                int main() {
                    return sum(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
                }
            """,
            "valid": True,
            "description": "Função com muitos parâmetros"
        },
        
        # Teste 4: Muitos statements em um bloco
        {
            "name": "Muitos Statements em Bloco",
            "code": """
                int main() {
                    int a = 1;
                    int b = 2;
                    int c = 3;
                    int d = 4;
                    int e = 5;
                    int f = 6;
                    int g = 7;
                    int h = 8;
                    int i = 9;
                    int j = 10;
                    int k = 11;
                    int l = 12;
                    int m = 13;
                    int n = 14;
                    int o = 15;
                    int p = 16;
                    int q = 17;
                    int r = 18;
                    int s = 19;
                    int t = 20;
                    return a + b + c + d + e + f + g + h + i + j + k + l + m + n + o + p + q + r + s + t;
                }
            """,
            "valid": True,
            "description": "Bloco com muitos statements consecutivos"
        },
        
        # Teste 5: Expressão muito complexa
        {
            "name": "Expressão Muito Complexa",
            "code": """
                int main() {
                    int a = 1;
                    int b = 2;
                    int c = 3;
                    int d = 4;
                    int e = 5;
                    
                    int result = ((a + b) * (c - d)) / e + (a * b) - (c / d) + (e % a) * ((b + c) * (d - e));
                    
                    return result;
                }
            """,
            "valid": True,
            "description": "Expressão aritmética muito complexa com muitos operadores e parênteses"
        },
        
        # Teste 6: Muitos níveis de aninhamento
        {
            "name": "Muitos Níveis de Aninhamento",
            "code": """
                int main() {
                    int x = 0;
                    if (x < 10) {
                        if (x < 9) {
                            if (x < 8) {
                                if (x < 7) {
                                    if (x < 6) {
                                        if (x < 5) {
                                            if (x < 4) {
                                                if (x < 3) {
                                                    if (x < 2) {
                                                        if (x < 1) {
                                                            x = 100;
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                    return x;
                }
            """,
            "valid": True,
            "description": "Muitos níveis de aninhamento de if statements"
        },
        
        # Teste 7: Identificadores longos
        {
            "name": "Identificadores Longos",
            "code": """
                int main() {
                    int thisIsAReallyReallyReallyReallyReallyReallyReallyReallyReallyReallyReallyLongVariableName = 42;
                    return thisIsAReallyReallyReallyReallyReallyReallyReallyReallyReallyReallyReallyLongVariableName;
                }
            """,
            "valid": True,
            "description": "Uso de identificadores muito longos"
        },
        
        # Teste 8: Literais numéricos grandes
        {
            "name": "Literais Numéricos Grandes",
            "code": """
                int main() {
                    int bigNumber = 1234567890;
                    return bigNumber;
                }
            """,
            "valid": True,
            "description": "Uso de literais numéricos muito grandes"
        }
    ]
    
    print("=== TESTES DE CASOS LIMÍTROFES ===")
    
    for i, test in enumerate(tests, 1):
        print(f"\nTeste {i}: {test['name']}")
        print(f"Descrição: {test['description']}")
        print(f"Código:\n{test['code']}")
        
        try:
            result = parse_code(test['code'])
            if test['valid']:
                print(f"✓ Sucesso! Código aceito conforme esperado.")
            else:
                print(f"✗ Falha! Código inválido foi aceito.")
        except Exception as e:
            if not test['valid']:
                print(f"✓ Erro detectado corretamente: {e}")
            else:
                print(f"✗ Erro inesperado: {e}")
    
    print("\n=== FIM DOS TESTES DE CASOS LIMÍTROFES ===")


def run_all_tests():

        print("======================================================")
        print("             TESTES DO PARSER LANG")
        print("======================================================")
        
        # Inicializar contadores
        total_tests = 0
        passed_tests = 0
        
        # Testar programas válidos
        print("\n\n=== PROGRAMAS VÁLIDOS ===")
        valid_results = run_valid_tests()
        total_tests += valid_results['total']
        passed_tests += valid_results['passed']
        
        # Testar programas inválidos
        print("\n\n=== PROGRAMAS INVÁLIDOS ===")
        invalid_results = run_invalid_tests()
        total_tests += invalid_results['total']
        passed_tests += invalid_results['passed']
        
        # Testar características específicas
        print("\n\n=== CARACTERÍSTICAS ESPECÍFICAS ===")
        specific_results = run_specific_tests()
        total_tests += specific_results['total']
        passed_tests += specific_results['passed']
        
        # Testar casos limítrofes
        print("\n\n=== CASOS LIMÍTROFES ===")
        edge_results = run_edge_tests()
        total_tests += edge_results['total']
        passed_tests += edge_results['passed']
        
        # Mostrar resultados finais
        print("\n\n======================================================")
        print(f"RESULTADOS FINAIS: {passed_tests}/{total_tests} testes passaram ({passed_tests/total_tests*100:.1f}%)")
        print("======================================================")
        
        # Detalhes por categoria
        print(f"- Programas Válidos: {valid_results['passed']}/{valid_results['total']} ({valid_results['passed']/valid_results['total']*100:.1f}%)")
        print(f"- Programas Inválidos: {invalid_results['passed']}/{invalid_results['total']} ({invalid_results['passed']/invalid_results['total']*100:.1f}%)")
        print(f"- Características Específicas: {specific_results['passed']}/{specific_results['total']} ({specific_results['passed']/specific_results['total']*100:.1f}%)")
        print(f"- Casos Limítrofes: {edge_results['passed']}/{edge_results['total']} ({edge_results['passed']/edge_results['total']*100:.1f}%)")

def run_test(code, expected_valid=True, name=""):
        """Executa um único teste e retorna se passou ou não"""
        try:
            result = parse_code(code)
            print(result)
            if expected_valid and result:
                print(f"✓ Teste '{name}' passou: código válido")
                return True
            else:
                print(f"✗ Teste '{name}' falhou: código inválido")
                return False
        except Exception as e:
            if not expected_valid:
                print(f"✓ Teste '{name}' passou: erro detectado corretamente - {e}")
                return True
            else:
                print(f"✗ Teste '{name}' falhou: código rejeitado - {e}")
                return False

def run_valid_tests():
    
        tests = [
            {"name": "Main Básica", "code": "int main() { return 0; }"},
            {"name": "Variáveis", "code": "int main() { int x = 10; return x; }"},
            {"name": "If-Else", "code": "int main() { if (1 > 0) { return 1; } else { return 0; } }"},
            {"name": "Loop For", "code": "int main() { for (int i = 0; i < 5; i++) { } return 0; }"},
            # Adicione mais testes conforme necessário
        ]
        
        total = len(tests)
        passed = 0
        
        for test in tests:
            if run_test(test["code"], True, test["name"]):
                passed += 1
        
        return {"total": total, "passed": passed}

def run_invalid_tests():
        """Executa todos os testes de programas inválidos"""
    
        tests = [
            {"name": "Sem ponto-e-vírgula", "code": "int main() { return 0 }", "valid": False},
            {"name": "Parêntese não fechado", "code": "int main() { if (1 > 0 { return 1; } }", "valid": False},
            {"name": "Chave não fechada", "code": "int main() { int x = 10;", "valid": False},
           
        ]
        
        total = len(tests)
        passed = 0
        
        for test in tests:
            if run_test(test["code"], test["valid"], test["name"]):
                passed += 1
        
        return {"total": total, "passed": passed}

def run_specific_tests():
        """Executa testes de características específicas"""
       
        tests = [
            {"name": "Incremento Pós-fixo", "code": "int main() { int i = 0; i++; return i; }", "valid": True},
            {"name": "Expressões Complexas", "code": "int main() { int a = 5; int b = (a * 2) + (10 / 2); return b; }", "valid": True},
           
        ]
        
        total = len(tests)
        passed = 0
        
        for test in tests:
            if run_test(test["code"], test["valid"], test["name"]):
                passed += 1
        
        return {"total": total, "passed": passed}

def run_edge_tests():
        """Executa testes de casos limítrofes"""
        
        tests = [
            {"name": "Função Vazia", "code": "int main() { }", "valid": True},
            {"name": "Identificador Longo", "code": "int main() { int abcdefghijklmnopqrstuvwxyz = 42; return abcdefghijklmnopqrstuvwxyz; }", "valid": True},
           
        ]
        
        total = len(tests)
        passed = 0
        
        for test in tests:
            if run_test(test["code"], test["valid"], test["name"]):
                passed += 1
        
        return {"total": total, "passed": passed}


if __name__ == "__main__":
    #run_edge_tests()
   #run_specific_tests()
   #run_invalid_tests()
   #run_valid_tests()
    run_all_tests()
