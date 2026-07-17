from __future__ import annotations

from skfd.authoring.dsl import BuilderFn, Constructor, Var, symbol
from skfd.authoring.ids import ConstructorId
from skfd.authoring.legacy_metamath import legacy_symbol_spec

from .formula import imp, wn
from .language import IMP, NOT, WFF
from .metamath_binding import SETMM_PRELUDE_BINDING
from .notation import PRELUDE_UNICODE_NOTATION

phi = Var("φ")
psi = Var("ψ")
chi = Var("χ")
th = Var("θ")
ta = Var("τ")


def _legacy_symbol(
    constructor: ConstructorId,
    builder: BuilderFn,
    *,
    op: str,
) -> Constructor:
    spec = legacy_symbol_spec(
        SETMM_PRELUDE_BINDING,
        PRELUDE_UNICODE_NOTATION,
        constructor,
        legacy_sorts={WFF: "wff"},
    )
    return symbol(
        spec.name,
        spec.arity,
        spec.in_sorts,
        spec.out_sort,
        op=op,
        precedence=spec.precedence,
        assoc=spec.associativity,
        aliases=spec.aliases,
    )(builder)


Imp = _legacy_symbol(IMP, lambda b, args: imp(b, args[0], args[1]), op="rshift")
Not = _legacy_symbol(NOT, lambda b, args: wn(b, args[0]), op="invert")


__all__ = [
    "phi",
    "psi",
    "chi",
    "th",
    "ta",
    "Imp",
    "Not",
]
