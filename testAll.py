from lang_parser import parse_code
from optRefactoration import opt, opt_refact, refactor
from examples import programa1, programa2, programa3, programa4, programa5, programa6, programa7  
from prettyPrinting import PrettyPrinter
from copy import deepcopy


programs = [
    ("Programa 1 - Factorial", programa1, True),
    ("Programa 2 - Fibonacci", programa2, True),
    ("Programa 3 - isPrime", programa3, True),
    ("Programa 4 - Optimization Test", programa4, True),
    ("Programa 5 - Invalid (no var name)", programa5, False),
    ("Programa 6 - Invalid (missing semicolon)", programa6, False),
    ("Programa 7 - Invalid (no return type)", programa7, False)
]

printer = PrettyPrinter(indent_size=2)

for i, (name, src, should_be_valid) in enumerate(programs, start=1):
    print(f"=== {name} ===\n")

    # 1) Parser
    try:
        ast = parse_code(str(src))  
        if should_be_valid:
            print("✓ Parser: OK (programa válido aceito)")
        else:
            print("✗ Parser: ERRO - programa inválido foi aceito!")
    except Exception as e:
        if not should_be_valid:
            print(f"✓ Parser: OK (programa inválido rejeitado: {e})")
            print("\n" + "="*40 + "\n")
            continue
        else:
            print(f"✗ Parser ERROR: {e}")
            print("\n" + "="*40 + "\n")
            continue

   
    if not should_be_valid:
        print("\n" + "="*40 + "\n")
        continue

    # 2) Pretty-print
    try:
        pretty = printer.pprint(ast)
        print("\nPretty-printed:")
        print(pretty)
    except Exception as e:
        print(f"Pretty-print ERROR: {e}")
        print("\n" + "="*40 + "\n")
        continue

    # 3) Round-trip
    try:
        ast2 = parse_code(pretty)
        pretty2 = printer.pprint(ast2)
        roundtrip_ok = pretty == pretty2
        print(f"\nRoundtrip: {'✓ OK' if roundtrip_ok else '✗ FAIL'}")
        if not roundtrip_ok:
            print("Diferenças encontradas!")
            print("\n" + "="*40 + "\n")
            continue
    except Exception as e:
        print(f"Roundtrip ERROR: {e}")
        print("\n" + "="*40 + "\n")
        continue

    # 4) Optimize only
    try:
        original_pretty = pretty
        optimized = opt(deepcopy(ast))
        after_opt = printer.pprint(optimized)
        if after_opt != original_pretty:
            print("\n✓ Optimized (mudanças aplicadas):")
            print(after_opt)
        else:
            print("\n– No optimization changes")
    except Exception as e:
        print(f"Optimize ERROR: {e}")
        after_opt = original_pretty

    # 5) Refactor only
    try:
        refactored = refactor(deepcopy(ast))
        after_ref = printer.pprint(refactored)
        if after_ref != original_pretty:
            print("\n✓ Refactored (mudanças aplicadas):")
            print(after_ref)
        else:
            print("\n– No refactoring changes")
    except Exception as e:
        print(f"Refactor ERROR: {e}")

    # 6) Optimize + Refactor combined
    try:
        combined = opt_refact(deepcopy(ast))
        after_combined = printer.pprint(combined)
        if after_combined != original_pretty and after_combined != after_opt and after_combined != after_ref:
            print("\n✓ Optimized + Refactored (mudanças combinadas):")
            print(after_combined)
        else:
            print("\n– No additional changes from combined optimization + refactoring")
    except Exception as e:
        print(f"Combined Opt+Refactor ERROR: {e}")

    print("\n" + "="*40 + "\n")