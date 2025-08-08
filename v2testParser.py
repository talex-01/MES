from lang_parser import *
def test_individual_parsers():
    """Testa cada parser individualmente para identificar problemas"""
    
    print("=== TESTE DE PARSERS INDIVIDUAIS ===")
    
    # Testar parse_int
    try:
        result = parse_int().parse("42")
        print("✓ parse_int funciona: ", result)
    except Exception as e:
        print("✗ Erro em parse_int:", e)
    
    # Testar parse_variable
    try:
        result = parse_variable.parse("variavel")
        print("✓ parse_variable funciona: ", result)
    except Exception as e:
        print("✗ Erro em parse_variable:", e)
    
    # Testar parse_primary
    try:
        result = parse_primary.parse("42")
        print("✓ parse_primary funciona com int: ", result)
        result2 = parse_primary.parse("True")
        print("✓ parse_primary funciona com bool: ", result2)
        result3 = parse_primary.parse("9.22")
        print("✓ parse_primary funciona com float: ", result3.value)
        result4 = parse_primary.parse("OLA")
        print("✓ parse_primary funciona com String: ", result4)
        
    except Exception as e:
        print("✗ Erro em parse_primary:", e)
    
    # Testar parse_unary
    try:
        result = parse_unary.parse("++i")
        print("✓ parse_unary funciona com incremento: ", result)
        result = parse_unary.parse("!c")
        print("✓ parse_unary funciona com diferente: ", result)
        result = parse_unary.parse("--v")
        print("✓ parse_unary funciona com decremento: ", result)
        result = parse_unary.parse("a--")
        print("✓ parse_unary funciona com decremento: ", result)
    except Exception as e:
        print("✗ Erro em parse_unary:", e)

    # Testar parse_factor
    try:
        result = parse_factor.parse("i / 2")
        print("✓ parse_factor funciona com divisão: ", result)
        
    except Exception as e:
        print("✗ Erro em parse_factor:", e)

    # Testar parse_term
    try:
        result = parse_term.parse("(i / 2) + (8 % 4)")
        print("✓ parse_term funciona : ", result)
        
    except Exception as e:
        print("✗ Erro em parse_term:", e)


    # Testar parse_comparison
    try:
        result = parse_comparison.parse("i * 2 > 8")
        print("✓ parse_comparison funciona : ", result)
        
    except Exception as e:
        print("✗ Erro em parse_comparison:", e)

    
    # Testar parse_expr
    try:
        result = parse_expr.parse("42")
        print("✓ parse_expr funciona com int: ", result)
        
        result = parse_expr.parse("variavel")
        print("✓ parse_expr funciona com variável: ", result)
        
        result = parse_expr.parse("(42)")
        print("✓ parse_expr funciona com parênteses: ", result)
    except Exception as e:
        print("✗ Erro em parse_expr:", e)

    # Teste do parse_var_decl
    print("2. TESTANDO PARSE_VAR_DECL")
    var_decl_code = "int i = 0;"
    var_decl_code2 = "bool a = True;"

    try:
        result = parse_var_decl.parse(var_decl_code)
        print(f"✓ Declaração de variável parseada com sucesso: {type(result).__name__}")
        print(f"  Tipo: {result.type}")
        print(f"  Nome: {result.name}")
        print(f"  Init: {result.init.value if result.init and isinstance(result.init, Literal) else '(expressão)' if result.init else 'Nenhuma'}")
        result2 = parse_var_decl.parse(var_decl_code2)
        print(f"✓ Declaração de variável parseada com sucesso: {type(result).__name__}")
        print(f"  Tipo: {result2.type}")
        print(f"  Nome: {result2.name}")
        print(f"  Init: {result2.init.value if result2.init and isinstance(result2.init, Literal) else '(expressão)' if result2.init else 'Nenhuma'}")
    except Exception as e:
        print(f"✗ Erro ao parsear declaração de variável: {e}")
    print()

    
    # Teste do parse_if
    print("TESTANDO PARSE_IF")
    if_code = "if (x > 0) { return x; } else { return 0; }"
   
    try:
        result = parse_if.parse(if_code)
        print(f"✓ Statement if parseado com sucesso: {type(result).__name__}")
        print(f"  Tem condição: {result.condition}")
        print(f"  Tem ramo then: {result.then_branch}")
        print(f"  Tem ramo else: {result.else_branch}") 
     
    except Exception as e:
        print(f"✗ Erro ao parsear statement if: {e}")
    print()

    #  Teste do parse_while
    print("4. TESTANDO PARSE_WHILE")
    while_code = "while (i < 10) { i = i + 1; }"
    try:
        result = parse_while.parse(while_code)
        print(f"✓ Loop while parseado com sucesso: {type(result).__name__}")
        print(f"  Tem condição: {result.condition}")
        print(f"  Tem corpo: {result.body}")
    except Exception as e:
        print(f"✗ Erro ao parsear loop while: {e}")
    print()

    # Teste do parse_for
    print("TESTANDO PARSE_FOR")
    for_code = "for (i = 0; i < 5; i = i + 1) { ++s; }"
    try:
        result = parse_for.parse(for_code)
        print(f"✓ Loop for parseado com sucesso: {type(result).__name__}")
        print(f"  Tipo da inicialização: {type(result.init).__name__}")
        print(f"  Tem condição: {result.condition}")
        print(f"  Tem incremento: {result.increment}")
        print(f"  Tem corpo: {result.body}")
    except Exception as e:
        print(f"✗ Erro ao parsear loop for: {e}")
    print()

    #Teste do parse_print
    print("TESTANDO PARSE_PRINT")
    print_code = "print(x);"
    try:
        result = parse_print.parse(print_code)
        print(f"✓ Statement print parseado com sucesso: {type(result).__name__}")
        print(f"  Tem expressão: {result.expr}")
    except Exception as e:
        print(f"✗ Erro ao parsear statement print: {e}")
    print()


    # Testar parse_return
    try:
        result = parse_return.parse("return 0;")
        print("✓ parse_return funciona: ", result)
        
        result = parse_return.parse("return;")
        print("✓ parse_return funciona sem valor: ", result)
    except Exception as e:
        print("✗ Erro em parse_return:", e)
    
    # Testar parse_block
    try:
        result = parse_block.parse("{ return 0; return 0; }")
        print("✓ parse_block funciona: ", result)
        
        result = parse_block.parse("{ }")
        print("✓ parse_block funciona vazio: ", result)
    except Exception as e:
        print("✗ Erro em parse_block:", e)
    
    # Testar parse_function
    try:
        result = parse_function.parse('''int main(){
                                             x = i * 2 ;
                                       }''')
        print("✓ parse_function funciona: ", result)
    except Exception as e:
        print("✗ Erro em parse_function:", e)
    
    # Testar parse_program
    try:
        result = parse_program.parse('''
int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

int main() {
    int num = 5;
    int result;
    result = factorial(num);
    print(result);
    return 0;
}
''')
        print("✓ parse_code funciona: ", result)
    except Exception as e:
        print("✗ Erro em parse_code:", e)


test_individual_parsers()

def test_individual_parsersSta():
    """Testa cada parser de statement individualmente"""
    print("=== TESTES DE PARSERS INDIVIDUAIS ===\n")
    
    # Teste do parse_expr_stmt
    print("1. TESTANDO PARSE_EXPR_STMT")
    expr_code = "x=10 ;"
    try:
        result = parse_expr_stmt.parse(expr_code)
        print(f"✓ Statement de expressão parseado com sucesso: {type(result).__name__}")
        if isinstance(result, ExprStmt) and isinstance(result.expr, Assignment):
            print(f"  Variável: {result.expr.var}")
            print(f"  Valor: {result.expr.expr.value if isinstance(result.expr.expr, Literal) else '(expressão)'}")
    except Exception as e:
        print(f"✗ Erro ao parsear statement de expressão: {e}")
    print()

test_individual_parsersSta()

def test_assignment_parser():
    """Testa o parser de atribuição em vários cenários"""
    print("=== TESTE DO PARSER DE ATRIBUIÇÃO ===\n")
    
    expr_code = "x = 10"
    try:
        result = parse_assignment.parse(expr_code)
        print(f"✓ Statement de assignment parseado com sucesso: {type(result).__name__}")
        if isinstance(result, ExprStmt) and isinstance(result.expr, Assignment):
            print(f"  Variável: {result.expr.var}")
            print(f"  Valor: {result.expr.expr.value if isinstance(result.expr.expr, Literal) else '(expressão)'}")
    except Exception as e:
        print(f"✗ Erro ao parsear statement de expressão: {e}")
    print()
test_assignment_parser()


def test_function_parser():

    print("=== TESTE DO PARSER DE FUNÇÕES ===\n")
    
    # Casos de teste válidos e inválidos
    test_cases = [
    
        {
            "input": "int main() { return 0; }",
            "description": "Função básica sem parâmetros",
            "expected_success": True,
            "expected_type": "int",
            "expected_name": "main",
            "expected_params": 0
        },

        {
            "input": "int square(int x) { return 0; }",
            "description": "Função com um único parâmetro",
            "expected_success": True,
            "expected_type": "int",
            "expected_name": "square",
            "expected_params": 1
        },
        {
            "input": "int add(int a, int b) { return 0; }",
            "description": "Função com múltiplos parâmetros",
            "expected_success": True,
            "expected_type": "int",
            "expected_name": "add",
            "expected_params": 2
        },
        {
            "input": "void printMsg() { return; }",
            "description": "Função com tipo void",
            "expected_success": True,
            "expected_type": "void",
            "expected_name": "printMsg",
            "expected_params": 0
        },

        {
            "input": "int calculate(int x, float y, bool flag) { return 0; }",
            "description": "Função com parâmetros de tipos diferentes",
            "expected_success": True,
            "expected_type": "int",
            "expected_name": "calculate",
            "expected_params": 3
        },
    
        {
            "input": "void noop() { }",
            "description": "Função com corpo vazio",
            "expected_success": True,
            "expected_type": "void",
            "expected_name": "noop",
            "expected_params": 0
        },
       
        {
            "input": "int complex(){return 0; return 1;}",
            "description": "Função com múltiplos statements",
            "expected_success": True,
            "expected_type": "int",
            "expected_name": "complex",
            "expected_params": 0
        },
       
        {
            "input": "main() { return 0; }",
            "description": "Sem tipo de retorno",
            "expected_success": False
        },
        {
            "input": "int () { return 0; }",
            "description": "Sem nome de função",
            "expected_success": False
        },
        {
            "input": "int main { return 0; }",
            "description": "Sem parênteses de parâmetros",
            "expected_success": False
        },
        {
            "input": "int main() return 0; }",
            "description": "Sem chave de abertura",
            "expected_success": False
        },
        {
            "input": "int main() { return 0;",
            "description": "Sem chave de fechamento",
            "expected_success": False
        }
    ]
 
    for i, test in enumerate(test_cases, 1):
        print(f"Teste {i}: {test['description']}")
        print(f"Input: '{test['input']}'")
        
        try:
            result = parse_function.parse(test['input'])
            
            if test['expected_success']:
                print(f"✓ Sucesso! Resultado: {type(result).__name__}")
                print(f"  Tipo de retorno: {result.return_type}")
                print(f"  Nome da função: {result.name}")
                print(f"  Número de parâmetros: {len(result.params)}")
                
              
                if result.params:
                    print("  Parâmetros:")
                    for i, param in enumerate(result.params):
                        print(f"    {i+1}. {param.type} {param.name}")
                
                
                print(f"  Corpo: {type(result.body).__name__} com {len(result.body.statements)} statements")
                
                
                if result.return_type != test.get('expected_type'):
                    print(f"!Tipo de retorno ({result.return_type}) diferente do esperado ({test.get('expected_type')})")
                
                if result.name != test.get('expected_name'):
                    print(f"!Nome da função ({result.name}) diferente do esperado ({test.get('expected_name')})")
                
                if len(result.params) != test.get('expected_params'):
                    print(f"!Número de parâmetros ({len(result.params)}) diferente do esperado ({test.get('expected_params')})")
            else:
                print(f"!Teste passou quando deveria falhar")
        except Exception as e:
            if not test['expected_success']:
                print(f"✓ Falhou conforme esperado: {str(e)[:50]}...")
            else:
                print(f"✗ Erro inesperado: {e}")
        
        print()
    
    print("=== FIM DO TESTE DE FUNÇÕES ===")
    

test_function_parser()

def test_block_with_multiple_statements():
   
    block_code = """{
    int x = 10;
    int y = 20;
    
    for (int i = 0; i < 5; i++) {
        x = x + i;
    }
    if( x > 0){
        x = x * 2;
    }
    return x;
}"""
    
    print("=== TESTE DO PARSER DE BLOCO COM MÚLTIPLOS STATEMENTS ===")
    print(f"Código a ser parseado:\n{block_code}\n")
    
    try:
        result = parse_block.parse(block_code)
        print("Bloco parseado com sucesso!")
        print(f"Número de statements: {len(result.statements)}")
        
        statement_types = {}
        for i, stmt in enumerate(result.statements):
            stmt_type = type(stmt).__name__
            statement_types[stmt_type] = statement_types.get(stmt_type, 0) + 1
            print(f"Statement {i+1}: {stmt}")
        
        print("\nResumo de statements:")
        for stmt_type, count in statement_types.items():
            print(f"- {stmt_type}: {count}")
        
        return result
    except Exception as e:
        print(f"Erro: {e}")
        if hasattr(e, 'pos'):
            print(f"Posição do erro: {e.pos}")
        return None


test_block_with_multiple_statements()