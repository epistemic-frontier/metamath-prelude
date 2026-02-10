from __future__ import annotations

from collections.abc import Sequence

from skfd.authoring.dsl import Var, symbol
from skfd.authoring.formula import Wff
from skfd.authoring.typing import WFF

from .formula import Builtins, imp, wa, wb, wn, wo

phi = Var("φ")
psi = Var("ψ")
chi = Var("χ")
th = Var("θ")
ta = Var("τ")


@symbol("->", 2, (WFF, WFF), WFF, op="rshift", precedence=20, assoc="right", aliases=["→", "⇒"])
def Imp(b: Builtins, args: Sequence[Wff]) -> Wff:
    return imp(b, args[0], args[1])


@symbol("-.", 1, (WFF,), WFF, op="invert", precedence=30, assoc="right", aliases=["¬", "~"])
def Not(b: Builtins, args: Sequence[Wff]) -> Wff:
    return wn(b, args[0])


@symbol("/\\", 2, (WFF, WFF), WFF, op="and", precedence=25, assoc="left", aliases=["∧", "&"])
def And(b: Builtins, args: Sequence[Wff]) -> Wff:
    return wa(b, args[0], args[1])


@symbol("\\/", 2, (WFF, WFF), WFF, op="or", precedence=24, assoc="left", aliases=["∨", "|"])
def Or(b: Builtins, args: Sequence[Wff]) -> Wff:
    return wo(b, args[0], args[1])


@symbol("<->", 2, (WFF, WFF), WFF, precedence=10, assoc="right", aliases=["↔"])
def Iff(b: Builtins, args: Sequence[Wff]) -> Wff:
    return wb(b, args[0], args[1])


__all__ = [
    "phi",
    "psi",
    "chi",
    "th",
    "ta",
    "Imp",
    "Not",
    "And",
    "Or",
    "Iff",
]
