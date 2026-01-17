# src/prelude/build.py
from typing import Any
from skfd import mm
from skfd.authoring.dsl import compile_wff, CompileEnv, DEFAULT_BUILDERS
from .formula import Builtins
from .structures import (
    Imp, Not, And, Or, Iff, Forall, Exists, Eq, Elem,
    phi, psi, x, y
)

# 1. Constants
# Primitive constants from set.mm Pre-logic section
mm.c("(", ")", "->", "-.", "wff", "|-")

# Logic / Set Theory constants
mm.c("/\\", "\\/", "<->", "A.", "E.", "=", "e.", "setvar", "class")

# 2. Variables
# Standard propositional variables
vars_prop = ["ph", "ps", "ch", "th", "ta", "et", "ze", "si", "rh", "mu", "la", "ka"]
for v in vars_prop:
    mm.v(v)
    
# Standard individual variables
vars_ind = ["x", "y", "z", "w", "v", "u"]
for v in vars_ind:
    mm.v(v)

# 3. Floating Hypotheses (Type Declarations)
for v in vars_prop:
    mm.f(f"w{v}", "wff", v)
    
for v in vars_ind:
    mm.f(f"v{v}", "setvar", v)

# 4. Syntax Axioms (Grammar)
builtins = Builtins.ensure(mm._interner)
env = CompileEnv(
    interner=mm._interner,
    builtins=builtins,
    ctor_builders=DEFAULT_BUILDERS.all(),
    origin_module_id=mm._module_id
)

def gen_axiom(label: str, typecode: str, expr: Any):
    """Generate a syntax axiom from an authoring expression."""
    wff = compile_wff(expr, env=env)
    tokens = []
    symtab = mm._interner.symbol_table()
    for sid in wff.tokens:
        sym = symtab.get(sid)
        if sym is None:
            raise ValueError(f"Unknown symbol ID {sid}")
        tokens.append(sym.local_name)
    mm.a(label, typecode, tokens)

# wn: wff -. ph
gen_axiom("wn", "wff", Not(phi))

# wimp: wff ( ph -> ps )
gen_axiom("wimp", "wff", Imp(phi, psi))

# wa: wff ( ph /\ ps )
gen_axiom("wa", "wff", And(phi, psi))

# wo: wff ( ph \/ ps )
gen_axiom("wo", "wff", Or(phi, psi))

# wb: wff ( ph <-> ps )
gen_axiom("wb", "wff", Iff(phi, psi))

# wal: wff A. x ph
gen_axiom("wal", "wff", Forall(x, phi))

# wex: wff E. x ph
gen_axiom("wex", "wff", Exists(x, phi))

# cv: class x
gen_axiom("cv", "class", x)

# wceq: wff x = y
gen_axiom("wceq", "wff", Eq(x, y))

# wel: wff x e. y
gen_axiom("wel", "wff", Elem(x, y))

# 5. Export
# Explicit export using mm.export()

# Export constants
for c in ["(", ")", "->", "-.", "wff", "|-", "/\\", "\\/", "<->", "A.", "E.", "=", "e.", "setvar", "class"]:
    mm.export(c)
    
# Export variables
for v in vars_prop + vars_ind:
    mm.export(v)
        
# Export labels
labels = [f"w{v}" for v in vars_prop] + [f"v{v}" for v in vars_ind] + \
         ["wn", "wimp", "wa", "wo", "wb", "wal", "wex", "cv", "wceq", "wel"]
         
for l in labels:
    mm.export(l)
