from langAST import *
from lang_parser import parse_code, parse_program
from examples import programa1, programa2, programa3


class PrettyPrinter:
    def __init__(self, indent_size: int = 2):
        self.indent_level = 0
        self.indent_size = indent_size

    def indent(self):
        self.indent_level += 1

    def dedent(self):
        self.indent_level -= 1
        if self.indent_level < 0:
            raise ValueError("Indentation level cannot be negative")

    def newline(self) -> str:
        return "\n" + " " * (self.indent_level * self.indent_size)

    def join(self, parts: List[str], sep: str) -> str:
        return sep.join(parts)

    def pprint(self, node: Any, parent_prec: int = 0) -> str:
        method = 'pprint_' + node.__class__.__name__
        if hasattr(self, method):
            return getattr(self, method)(node, parent_prec)
        else:
            raise NotImplementedError(f"Pretty printing not implemented for {node.__class__.__name__}")
        
    # Precedência dos operadores (maior número = maior precedência)
    def get_precedence(self, op: str) -> int:
        precedence_map = {
            '||': 1,
            '&&': 2,
            '==': 3, '!=': 3,
            '<': 4, '>': 4, '<=': 4, '>=': 4,
            '+': 5, '-': 5,
            '*': 6, '/': 6, '%': 6,
        }
        return precedence_map.get(op, 0)
    
    # PP for AST elements and strucs
    
    def pprint_Literal(self, node, parent_prec: int = 0):
        if isinstance(node.value, str):
            return f'"{node.value}"'
        if isinstance(node.value, bool):
            return 'true' if node.value else 'false'
        if isinstance(node.value, str):
            s = node.value.replace('\\', '\\\\').replace('"', '\\"')
            return f'"{s}"'
        return str(node.value)

    def pprint_Variable(self, node, parent_prec: int = 0):
        return node.name

    def pprint_BinaryOp(self, node: BinaryOp, parent_prec: int = 0) -> str:
        my_prec = self.get_precedence(node.op)
        left = self.pprint(node.left, my_prec)
        right = self.pprint(node.right, my_prec + 1)  # +1 para associatividade à esquerda
        
        result = f"{left} {node.op} {right}"
        
        # Adicionar parênteses se necessário
        if parent_prec > my_prec:
            result = f"({result})"
        
        return result

    def pprint_UnaryOp(self, node: UnaryOp, parent_prec: int = 0) -> str:
        expr = self.pprint(node.expr)
        return f"{node.op}{expr}" if node.prefix else f"{expr}{node.op}"

    def pprint_Assignment(self, node: Assignment, parent_prec: int = 0) -> str:
        return f"{node.var} = {self.pprint(node.expr)}"

    def pprint_FunctionCall(self, node: FunctionCall, parent_prec: int = 0) -> str:
        args = ", ".join(self.pprint(arg) for arg in node.args)
        return f"{node.name}({args})"

    # Statements
    def pprint_ExprStmt(self, node: ExprStmt, parent_prec: int = 0) -> str:
        return f"{self.pprint(node.expr)};"

    def pprint_VarDecl(self, node: VarDecl, parent_prec: int = 0) -> str:
        init = f" = {self.pprint(node.init)}" if node.init else ""
        return f"{node.type} {node.name}{init};"

    def pprint_Print(self, node: Print, parent_prec: int = 0) -> str:
        return f"print({self.pprint(node.expr)});"

    def pprint_Return(self, node: Return, parent_prec: int = 0) -> str:
        val = f" {self.pprint(node.value)}" if node.value else ""
        return f"return{val};"

    def pprint_If(self, node: If, parent_prec: int = 0) -> str:
        cond = self.pprint(node.condition)
        then_b = self.pprint(node.then_branch)
        code = f"if ({cond}) {then_b}"
        if node.else_branch:
            else_b = self.pprint(node.else_branch)
            code += f" else {else_b}"
        return code

    def pprint_While(self, node: While, parent_prec: int = 0) -> str:
        cond = self.pprint(node.condition)
        body = self.pprint(node.body)
        return f"while ({cond}) {body}"

    def pprint_For(self, node, parent_prec: int = 0):
        # Handle init
        if node.init is None:
            init = ""
        elif isinstance(node.init, VarDecl):
            # Remove o ';' do VarDecl pois vamos adicionar depois
            init = self.pprint(node.init)[:-1]
        elif isinstance(node.init, ExprStmt):
            init = self.pprint(node.init.expr)
        else:
            init = ""

        cond = self.pprint(node.condition) if node.condition else ""
        increment = self.pprint(node.increment) if node.increment else ""
        body = self.pprint(node.body)
        return f"for ({init}; {cond}; {increment}) {body}"

        
    def pprint_Block(self, node, parent_prec: int = 0):
        if not node.statements:
            return "{}"
        
        parts = ["{"]
        self.indent()
        for stmt in node.statements:
            parts.append(self.newline())
            parts.append(self.pprint(stmt))
        self.dedent()
        if node.statements:  # Only add newline if there were statements
            parts.append(self.newline())
        parts.append("}")
        return "".join(parts)

    def pprint_Function(self, node: Function, parent_prec: int = 0) -> str:
        params = ", ".join(f"{p.type} {p.name}" for p in node.params)
        body = self.pprint(node.body)
        return f"{node.return_type} {node.name}({params}) {body}"

    def pprint_Program(self, node: Program, parent_prec: int = 0) -> str:
        parts: List[str] = []
        
        # Global variables first
        for gv in node.global_vars:
            parts.append(self.pprint(gv))
            parts.append(self.newline())
        
        # Functions
        for i, func in enumerate(node.functions):
            if i > 0 or node.global_vars:  # Add newline if not first element
                parts.append(self.newline())
            parts.append(self.pprint(func))
        
        return "".join(parts)


## Test PrettyPrinter

def prop_roundtrip(prog_str: str) -> bool:
    printer = PrettyPrinter(indent_size=2)
    
    # Parse the string
    ast = parse_code(prog_str)
    
    # Pretty print it
    pretty = printer.pprint(ast)
    
    # Parse the pretty printed version
    ast2 = parse_code(pretty)
    
    # Pretty print again
    pretty2 = printer.pprint(ast2)
    
    # Compare the pretty printed versions (not the ASTs)
    return pretty == pretty2

# Test harness for pretty-printing and round-trip

def test_pretty_printer():
    printer = PrettyPrinter(indent_size=2)

    print("\n=== Pretty Printing ===\n")
    for name, prog in (
        ("programa1", programa1),
        ("programa2", programa2),
        ("programa3", programa3)
    ):
        print(f"--- {name} ---")
        ok = prop_roundtrip(prog)
        symbol = '✓' if ok else '✗'
        print(f"\n{symbol} {name}")
        assert ok, f"Round-trip failed for {name}"  

if __name__ == "__main__":
    test_pretty_printer()