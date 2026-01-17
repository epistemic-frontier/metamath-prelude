# src/prelude/structures.py
from __future__ import annotations

from skfd.authoring.dsl import Var, symbol
from skfd.authoring.typing import WFF

from .formula import imp as mk_imp
from .formula import wn as mk_wn
from .formula import wa as mk_wa
from .formula import wo as mk_wo
from .formula import wb as mk_wb
from .formula import forall2 as mk_forall2
from .formula import exist as mk_exist
from .formula import eq as mk_eq
from .formula import elem as mk_elem

# Formal variables (generic placeholders)
phi = Var(name="ph")
psi = Var(name="ps")
chi = Var(name="ch")
th = Var(name="th")
ta = Var(name="ta")
et = Var(name="et")
ze = Var(name="ze")
si = Var(name="si")
rh = Var(name="rh")
mu = Var(name="mu")
la = Var(name="la")
ka = Var(name="ka")

x = Var(name="x")
y = Var(name="y")
z = Var(name="z")

# Core constructors (author-visible symbols)
# These match the syntax axioms in set.mm

@symbol("→", 2, (WFF, WFF), WFF, op="rshift", notes="implication", precedence=10, assoc="right", aliases=["->"])
def Imp(b, xs):
    return mk_imp(b, xs[0], xs[1])

@symbol("¬", 1, (WFF,), WFF, op="invert", notes="negation", precedence=40, aliases=["-."])
def Not(b, xs):
    return mk_wn(b, xs[0])

@symbol("∧", 2, (WFF, WFF), WFF, op="and", notes="conjunction", precedence=30, assoc="left", aliases=["/\\"])
def And(b, xs):
    return mk_wa(b, xs[0], xs[1])

@symbol("∨", 2, (WFF, WFF), WFF, op="or", notes="disjunction", precedence=20, assoc="left", aliases=["\\/"])
def Or(b, xs):
    return mk_wo(b, xs[0], xs[1])

@symbol("↔", 2, (WFF, WFF), WFF, notes="biconditional", precedence=10, assoc="none", aliases=["<->"])
def Iff(b, xs):
    return mk_wb(b, xs[0], xs[1])

@symbol("∀", 2, (WFF, WFF), WFF, notes="universal quantification", aliases=["A."])
def Forall(b, xs):
    # Expects (var, body)
    return mk_forall2(b, xs[0], xs[1])

@symbol("∃", 2, (WFF, WFF), WFF, notes="existential quantification", aliases=["E."])
def Exists(b, xs):
    return mk_exist(b, xs[0], xs[1])

@symbol("=", 2, (WFF, WFF), WFF, op="eq", notes="equality", precedence=50)
def Eq(b, xs):
    return mk_eq(b, xs[0], xs[1])

@symbol("∈", 2, (WFF, WFF), WFF, notes="membership", precedence=50, aliases=["e."])
def Elem(b, xs):
    return mk_elem(b, xs[0], xs[1])

__all__ = [
    "phi", "psi", "chi", "th", "ta", "et", "ze", "si", "rh", "mu", "la", "ka",
    "x", "y", "z",
    "Imp", "Not", "And", "Or", "Iff",
    "Forall", "Exists", "Eq", "Elem",
]
