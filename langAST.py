from dataclasses import dataclass
from typing import List, Optional, Union, Any

# Expressões
@dataclass
class Expr:
    pass

@dataclass
class Literal(Expr):
    value: Union[int, float, bool, str]

@dataclass
class Variable(Expr):
    name: str

@dataclass
class BinaryOp(Expr):
    left: Expr
    op: str  # "+", "-", "*", "/", "%", "==", "!=", ">", "<", ">=", "<=", "&&", "||"
    right: Expr

@dataclass
class UnaryOp(Expr):
    op: str  # "-", "!", "++"
    expr: Expr
    prefix: bool = True  # True para prefixo (++x), False para sufixo (x++)

@dataclass
class Assignment(Expr):
    var: str
    expr: Expr

@dataclass
class FunctionCall(Expr):
    name: str
    args: List[Expr]

# Statements
@dataclass
class Stmt:
    pass

@dataclass
class ExprStmt(Stmt):
    expr: Expr

@dataclass
class VarDecl(Stmt):
    type: str
    name: str
    init: Optional[Expr] = None

@dataclass
class Block(Stmt):
    statements: List[Stmt]

@dataclass
class If(Stmt):
    condition: Expr
    then_branch: Stmt
    else_branch: Optional[Stmt] = None

@dataclass
class While(Stmt):
    condition: Expr
    body: Stmt

@dataclass
class For(Stmt):

    init: Optional[Union[Expr, VarDecl]]
    condition: Expr
    increment: Optional[Expr]
    body: Stmt

@dataclass
class Return(Stmt):
    value: Optional[Expr] = None

@dataclass
class Print(Stmt):
    expr: Expr

# Definição de função
@dataclass
class Function:

    return_type: str
    name: str
    params: List[VarDecl]
    body: Block

# Programa completo
@dataclass
class Program:
    functions: List[Function]
    global_vars: List[VarDecl]
    
    def __str__(self) -> str:
        from prettyPrinting import PrettyPrinter
        return PrettyPrinter(indent_size=2).pprint(self)
        