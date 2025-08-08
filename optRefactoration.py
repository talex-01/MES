from langAST import *
from typing import List, Dict, Union
import operator

_ARITH_OPS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '%': operator.mod,
}

_COMP_OPS = {
    '<': operator.lt,
    '>': operator.gt,
    '<=': operator.le,
    '>=': operator.ge,
    '==': operator.eq,
    '!=': operator.ne,
}

#### OPTIMIZATION

def opt(ast: Program) -> Program:
    # globals
    new_globals = []
    for gv in ast.global_vars:
        init = optimize_expr(gv.init) if gv.init is not None else None
        new_globals.append(VarDecl(gv.type, gv.name, init))
    # functions
    new_funcs = []
    for fn in ast.functions:
        body = optimize_block(fn.body)
        new_funcs.append(Function(fn.return_type, fn.name, fn.params, body))
    return Program(functions=new_funcs, global_vars=new_globals)


def optimize_block(block: Block) -> Block:
    new_stmts: List[Stmt] = []
    for stmt in block.statements:
        if isinstance(stmt, VarDecl):
            init = optimize_expr(stmt.init) if stmt.init else None
            new_stmts.append(VarDecl(stmt.type, stmt.name, init))
        elif isinstance(stmt, ExprStmt):
            new_stmts.append(ExprStmt(optimize_expr(stmt.expr)))
        elif isinstance(stmt, Print):
            new_stmts.append(Print(optimize_expr(stmt.expr)))
        elif isinstance(stmt, Return):
            val = optimize_expr(stmt.value) if stmt.value else None
            new_stmts.append(Return(val))
        elif isinstance(stmt, If):
            cond = optimize_expr(stmt.condition)
            then_b = optimize_block(_wrap_block(stmt.then_branch))
            else_b = optimize_block(_wrap_block(stmt.else_branch)) if stmt.else_branch else None
            new_stmts.append(If(cond, then_b, else_b))
        elif isinstance(stmt, While):
            cond = optimize_expr(stmt.condition)
            body = optimize_block(_wrap_block(stmt.body))
            new_stmts.append(While(cond, body))
        elif isinstance(stmt, For):
            init = stmt.init
            if isinstance(init, ExprStmt): 
                init = ExprStmt(optimize_expr(init.expr))
            elif isinstance(init, VarDecl) and init.init is not None:
                init = VarDecl(init.type, init.name, optimize_expr(init.init))
            cond = optimize_expr(stmt.condition)
            inc = optimize_expr(stmt.increment) if stmt.increment else None
            body = optimize_block(_wrap_block(stmt.body))
            new_stmts.append(For(init, cond, inc, body))
        elif isinstance(stmt, Block):
            new_stmts.append(optimize_block(stmt))
        else:
            new_stmts.append(stmt)
    return Block(new_stmts)


def optimize_expr(expr: Expr) -> Expr:
    if expr is None:
        return None
    if isinstance(expr, (Literal, Variable)):
        return expr
    if isinstance(expr, FunctionCall):
        return FunctionCall(expr.name, [optimize_expr(a) for a in expr.args])
    if isinstance(expr, UnaryOp):
        return UnaryOp(expr.op, optimize_expr(expr.expr), expr.prefix)
    if isinstance(expr, Assignment):
        return Assignment(expr.var, optimize_expr(expr.expr))
    if isinstance(expr, BinaryOp):
        left = optimize_expr(expr.left)
        right = optimize_expr(expr.right)
        
        # constant folding for arithmetic
        if isinstance(left, Literal) and isinstance(right, Literal):
            if expr.op in _ARITH_OPS:
                func = _ARITH_OPS[expr.op]
                try: 
                    result = func(left.value, right.value)
                    return Literal(result)
                except: 
                    pass
            # constant folding for comparisons
            if expr.op in _COMP_OPS:
                func = _COMP_OPS[expr.op]
                try:
                    result = func(left.value, right.value)
                    return Literal(result)
                except:
                    pass
        
        # algebraic simplifications
        if expr.op == '+':
            if _is_zero(right): return left
            if _is_zero(left): return right
        if expr.op == '-':
            if _is_zero(right): return left
        if expr.op == '*':
            if _is_one(right): return left
            if _is_one(left): return right
            if _is_zero(right) or _is_zero(left): return Literal(0)
        if expr.op == '/':
            if _is_one(right): return left
        
        # boolean simplifications
        if expr.op in ('&&','||'):
            l, r = _bool_val(left), _bool_val(right)
            if expr.op == '&&':
                if l is True: return right
                if l is False: return Literal(False)
                if r is True: return left
                if r is False: return Literal(False)
            if expr.op == '||':
                if l is False: return right
                if l is True: return Literal(True)
                if r is False: return left
                if r is True: return Literal(True)
        
        return BinaryOp(left, expr.op, right)
    return expr


def _is_zero(expr: Expr) -> bool:
    return isinstance(expr, Literal) and expr.value == 0

def _is_one(expr: Expr) -> bool:
    return isinstance(expr, Literal) and expr.value == 1

def _bool_val(expr: Expr):
    return expr.value if isinstance(expr, Literal) and isinstance(expr.value, bool) else None

# Wrap single stmt into block
def _wrap_block(node):
    if node is None:
        return None
    return node if isinstance(node, Block) else Block([node])


# #### Refactoring

def refactor(ast: Program) -> Program:
    new_globals = [_ref_vardecl(v) for v in ast.global_vars]
    new_funcs   = [_ref_function(f) for f in ast.functions]
    return Program(functions=new_funcs, global_vars=new_globals)


def _ref_function(fn: Function) -> Function:
    return Function(fn.return_type, fn.name, fn.params, _ref_block(fn.body))


def _ref_vardecl(v: VarDecl) -> VarDecl:
    init = _ref_expr(v.init) if v.init is not None else None
    return VarDecl(v.type, v.name, init)


def _ref_block(block: Block) -> Block:
    new_stmts = []
    for s in block.statements:
        refactored = _ref_stmt(s)
        # Handle case where if statement is replaced by just its branch
        if isinstance(refactored, Block):
            new_stmts.extend(refactored.statements)
        else:
            new_stmts.append(refactored)
    return Block(new_stmts)


def _ref_stmt(stmt: Stmt) -> Stmt:
    if isinstance(stmt, ExprStmt): 
        return ExprStmt(_ref_expr(stmt.expr))
    if isinstance(stmt, Print):    
        return Print(_ref_expr(stmt.expr))
    if isinstance(stmt, Return):   
        return Return(_ref_expr(stmt.value) if stmt.value else None)
    if isinstance(stmt, If):
        cond = _ref_expr(stmt.condition)
        # if True then X else Y -> X
        if isinstance(cond, Literal) and cond.value is True:  
            return _ref_stmt(stmt.then_branch) if isinstance(stmt.then_branch, (If, While, For)) else _wrap_block(stmt.then_branch)
        # if False then X else Y -> Y
        if isinstance(cond, Literal) and cond.value is False: 
            if stmt.else_branch:
                return _ref_stmt(stmt.else_branch) if isinstance(stmt.else_branch, (If, While, For)) else _wrap_block(stmt.else_branch)
            else:
                return Block([])  # Empty block for no else branch
        
        then_branch = _ref_stmt(stmt.then_branch) if isinstance(stmt.then_branch, (If, While, For)) else _wrap_block(stmt.then_branch)
        else_branch = None
        if stmt.else_branch:
            else_branch = _ref_stmt(stmt.else_branch) if isinstance(stmt.else_branch, (If, While, For)) else _wrap_block(stmt.else_branch)
        
        return If(cond, then_branch, else_branch)
    if isinstance(stmt, While): 
        return While(_ref_expr(stmt.condition), _ref_block(_wrap_block(stmt.body)))
    if isinstance(stmt, For):
        init = _ref_stmt(stmt.init) if stmt.init else None
        cond = _ref_expr(stmt.condition)
        inc  = _ref_expr(stmt.increment) if stmt.increment else None
        body = _ref_block(_wrap_block(stmt.body))
        return For(init, cond, inc, body)
    if isinstance(stmt, VarDecl): 
        return _ref_vardecl(stmt)
    if isinstance(stmt, Block):
        return _ref_block(stmt)
    return stmt


def _ref_expr(expr: Expr) -> Expr:
    if expr is None:
        return None
    if isinstance(expr, Literal) or isinstance(expr, Variable): 
        return expr
    if isinstance(expr, Assignment): 
        return Assignment(expr.var, _ref_expr(expr.expr))
    if isinstance(expr, FunctionCall): 
        return FunctionCall(expr.name, [_ref_expr(a) for a in expr.args])
    if isinstance(expr, UnaryOp): 
        return UnaryOp(expr.op, _ref_expr(expr.expr), expr.prefix)
    if isinstance(expr, BinaryOp):
        left = _ref_expr(expr.left)
        right= _ref_expr(expr.right)
        # x==True -> x ; x==False -> !x
        if expr.op == '==' and isinstance(right, Literal) and isinstance(right.value, bool):
            return left if right.value else UnaryOp('!', left)
        if expr.op == '==' and isinstance(left, Literal) and isinstance(left.value, bool):
            return right if left.value else UnaryOp('!', right)
        return BinaryOp(left, expr.op, right)
    return expr


## utils

def names(ast: Program) -> List[str]:
    result = set(v.name for v in ast.global_vars)
    for fn in ast.functions:
        result.add(fn.name)
        for p in fn.params: result.add(p.name)
        _collect_names(fn.body, result)
    return sorted(result)


def _collect_names(block: Block, acc: set):
    for s in block.statements:
        if isinstance(s, VarDecl): acc.add(s.name)
        if isinstance(s, If):
            _collect_names(_wrap_block(s.then_branch), acc)
            if s.else_branch: _collect_names(_wrap_block(s.else_branch), acc)
        if isinstance(s, While): _collect_names(_wrap_block(s.body), acc)
        if isinstance(s, For):
            if isinstance(s.init, VarDecl): acc.add(s.init.name)
            _collect_names(_wrap_block(s.body), acc)


def instructions(ast: Program) -> Dict[str,int]:
    counts: Dict[str,int] = {}
    for v in ast.global_vars: counts['VarDecl'] = counts.get('VarDecl',0)+1
    for fn in ast.functions:
        counts['Function']=counts.get('Function',0)+1
        _count_block(fn.body, counts)
    return counts

def _count_block(block: Block, counts: Dict[str,int]):
    for s in block.statements:
        t = s.__class__.__name__
        counts[t] = counts.get(t,0)+1
        if isinstance(s, If):
            _count_block(_wrap_block(s.then_branch), counts)
            if s.else_branch: _count_block(_wrap_block(s.else_branch),counts)
        if isinstance(s, While): _count_block(_wrap_block(s.body), counts)
        if isinstance(s, For): _count_block(_wrap_block(s.body), counts)


def code_smells(ast: Program) -> Dict[str,int]:
    smells: Dict[str,int] = {}
    for fn in ast.functions: _detect_smells(fn.body, smells)
    return smells

def _detect_smells(block: Block, smells: Dict[str,int]):
    for s in block.statements:
        if isinstance(s, If) and isinstance(s.condition, Literal) and isinstance(s.condition.value,bool):
            smells['redundant_if']=smells.get('redundant_if',0)+1
        if isinstance(s, ExprStmt) and isinstance(s.expr, BinaryOp) and s.expr.op=='==' and (
           (isinstance(s.expr.left,Literal) and isinstance(s.expr.left.value,bool)) or
           (isinstance(s.expr.right,Literal) and isinstance(s.expr.right.value,bool))):
            smells['bool_comparison']=smells.get('bool_comparison',0)+1
        if isinstance(s, If):
            _detect_smells(_wrap_block(s.then_branch),smells)
            if s.else_branch: _detect_smells(_wrap_block(s.else_branch),smells)
        if isinstance(s, While): _detect_smells(_wrap_block(s.body), smells)
        if isinstance(s, For):   _detect_smells(_wrap_block(s.body), smells)


# optimize + refactor
def opt_refact(ast: Program) -> Program:
    optimized = opt(ast)
    return refactor(optimized)