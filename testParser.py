from lang_parser import *

with open('./progsParser/prog1.c', 'r') as f:
    prog1_texto = f.read()
    print(prog1_texto)
with open('./progsParser/prog2.c', 'r') as f:
    prog2_texto = f.read()
    print(prog2_texto)
with open('./progsParser/prog3.c', 'r') as f:
    prog3_texto = f.read()
    print(prog3_texto)
# Exemplos inválidos
with open('./progsParser/prog1_inv.c', 'r') as f:
    prog4_texto = f.read()

with open('./progsParser/prog2_inv.c', 'r') as f:
    prog5_texto = f.read()

with open('./progsParser/prog3_inv.c', 'r') as f:
    prog6_texto = f.read()

# Testando o parser com programas válidos
def test_parse_valid():
    print("Testagem de programas válidos:")
    
    try:
        ast1 = parse_code(prog1_texto)
        print("Programa 1 (Fatorial) parseado com sucesso!")
        print(f"Número de funções: {len(ast1.functions)}")
        print(f"Funções: {[f.name for f in ast1.functions]}")
        print()
    except Exception as e:
        print(f"Erro ao parsear programa 1: {e}")
        
    try:
        ast2 = parse_code(prog2_texto)
        print("Programa 2 (Fibonacci) parseado com sucesso!")
        print(f"Número de funções: {len(ast2.functions)}")
        print(f"Funções: {[f.name for f in ast2.functions]}")
        print()
    except Exception as e:
        print(f"Erro ao parsear programa 2: {e}")
        
    try:
        ast3 = parse_code(prog3_texto)
        print("Programa 3 (Verificação de primo) parseado com sucesso!")
        print(f"Número de funções: {len(ast3.functions)}")
        print(f"Funções: {[f.name for f in ast3.functions]}")
        print()
    except Exception as e:
        print(f"Erro ao parsear programa 3: {e}")

# Testando o parser com programas inválidos
def test_parse_invalid():
    print("Testagem de programas inválidos:")
    
    try:
        ast4 = parse_code(prog4_texto)
        print("ERRO: Programa 4 (falta ponto e vírgula) foi parseado sem erros!")
    except Exception as e:
        print("Programa 4 rejeitado corretamente!")
        print(f"Erro: {e}")
        print()
        
    try:
        ast5 = parse_code(prog5_texto)
        print("ERRO: Programa 5 (parênteses desbalanceados) foi parseado sem erros!")
    except Exception as e:
        print("Programa 5 rejeitado corretamente!")
        print(f"Erro: {e}")
        print()
        
    try:
        ast6 = parse_code(prog6_texto)
        print("ERRO: Programa 6 (tipo inválido) foi parseado sem erros!")
    except Exception as e:
        print("Programa 6 rejeitado corretamente!")
        print(f"Erro: {e}")
        print()

# Executar os testes
print("=== TESTE DO PARSER DA LINGUAGEM LANG ===")
test_parse_valid()
print("=======================================")
test_parse_invalid()
print("=======================================")

