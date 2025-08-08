"""
Script para testar as correções feitas
"""

from lang_parser import parse_code
from optRefactoration import opt, refactor, opt_refact
from prettyPrinting import PrettyPrinter

def test_specific_issues():
    printer = PrettyPrinter()
    
    print("=== TESTE 1: Otimização de Constantes ===")
    code1 = """
    int main() {
        int a = 2 + 3 * 4 - 1;
        return a;
    }
    """
    print("Original:", code1)
    ast1 = parse_code(code1)
    opt_ast1 = opt(ast1)
    print("Otimizado:", printer.pprint(opt_ast1))
    print()
    
    print("=== TESTE 2: Simplificações Algébricas ===")
    code2 = """
    int main() {
        int b = x + 0;
        int c = 1 * y;
        int d = z * 0;
        return b + c + d;
    }
    """
    print("Original:", code2)
    ast2 = parse_code(code2)
    opt_ast2 = opt(ast2)
    print("Otimizado:", printer.pprint(opt_ast2))
    print()
    
    print("=== TESTE 3: Refactoring de If True ===")
    code3 = """
    int main() {
        if (true) {
            return 42;
        } else {
            return 0;
        }
    }
    """
    print("Original:", code3)
    ast3 = parse_code(code3)
    ref_ast3 = refactor(ast3)
    print("Refatorado:", printer.pprint(ref_ast3))
    print()
    
    print("=== TESTE 4: Refactoring de Comparações Booleanas ===")
    code4 = """
    int main() {
        bool flag = true;
        int e = flag == true;
        int f = flag == false;
        return e + f;
    }
    """
    print("Original:", code4)
    ast4 = parse_code(code4)
    ref_ast4 = refactor(ast4)
    print("Refatorado:", printer.pprint(ref_ast4))
    print()
    
    print("=== TESTE 5: Parser Rejeita Código Inválido ===")
    invalid_codes = [
        ("int = 5;", "Sem nome de variável"),
        ("int main() { int = 5; }", "Sem nome de variável em função"),
        ("main() { return 0; }", "Sem tipo de retorno"),
    ]
    
    for code, desc in invalid_codes:
        print(f"\nTestando '{desc}': {code}")
        try:
            parse_code(code)
            print("✗ ERRO: Código inválido foi aceito!")
        except Exception as e:
            print(f"✓ Rejeitado corretamente: {e}")
    print()
    
    print("=== TESTE 6: Programa 4 Completo ===")
    code6 = """
    int main() {
        bool flag = true;
        bool otherFlag = false;
        int a = 2 + 3 * 4 - 1;
        int b = x + 0;
        int c = 1 * y;
        int d = z * 0;

        if (true) {
            a = 42;
        } else {
            a = 0;
        }

        int e = flag == true;
        int f = otherFlag == false;

        return a + b + c + d + e + f;
    }
    """
    print("Original:")
    print(code6)
    ast6 = parse_code(code6)
    final6 = opt_refact(ast6)
    print("\nOtimizado + Refatorado:")
    print(printer.pprint(final6))


if __name__ == "__main__":
    test_specific_issues()