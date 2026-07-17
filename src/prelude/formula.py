# prelude/formula.py
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import (
    Any,
    cast,
)

from skfd.authoring.formula import TokenSeq, Wff
from skfd.authoring.legacy_metamath import (
    build_legacy_formula,
    legacy_binary_formation,
    legacy_prefix_formation,
)
from skfd.authoring.metamath_language import TokenRef
from skfd.core.peg import Rule, TokenStream
from skfd.core.symbols import SymbolId, SymbolInterner

from .language import IMP, NOT, WFF
from .metamath_binding import (
    SETMM_IMP_TOKEN,
    SETMM_LPAREN_TOKEN,
    SETMM_NEG_TOKEN,
    SETMM_PRELUDE_BINDING,
    SETMM_RPAREN_TOKEN,
)

# -----------------------------------------------------------------------------
# Reserved / builtin tokens (by name)
# -----------------------------------------------------------------------------

# Canonical foundation symbol namespace. Downstream packages may call
# Builtins.ensure(...) to recover the same foundation Const ids, but proof
# labels still have to come through package exports and linker access checks.
GLOBAL_PRELUDE_MODULE_ID: str = "__prelude__"


@dataclass(frozen=True)
class Builtins:
    """Builtin constant tokens owned by the foundation prelude.

    These are Const symbols in the interner, not magic.
    """

    lp: SymbolId  # "("
    rp: SymbolId  # ")"
    imp: SymbolId  # "->"
    neg: SymbolId  # "-."

    @staticmethod
    def ensure(
        interner: SymbolInterner,
        *,
        origin_module_id: str = GLOBAL_PRELUDE_MODULE_ID,
        origin_ref: Any = None,
    ) -> Builtins:
        """Intern canonical foundation vocabulary tokens.

        IMPORTANT:
        - The default namespace is the global foundation namespace.
        - This is for vocabulary SymbolId identity only; it is not a dependency
          import mechanism for theorem labels.
        - If you override origin_module_id, you are intentionally creating a
          distinct builtin set.
        """
        lp = interner.intern(
            origin_module_id=origin_module_id,
            local_name=SETMM_LPAREN_TOKEN.local_name,
            kind="Const",
            origin_ref=origin_ref,
        )
        rp = interner.intern(
            origin_module_id=origin_module_id,
            local_name=SETMM_RPAREN_TOKEN.local_name,
            kind="Const",
            origin_ref=origin_ref,
        )
        imp = interner.intern(
            origin_module_id=origin_module_id,
            local_name=SETMM_IMP_TOKEN.local_name,
            kind="Const",
            origin_ref=origin_ref,
        )
        neg = interner.intern(
            origin_module_id=origin_module_id,
            local_name=SETMM_NEG_TOKEN.local_name,
            kind="Const",
            origin_ref=origin_ref,
        )
        return Builtins(
            lp=lp,
            rp=rp,
            imp=imp,
            neg=neg,
        )

    def token_symbols(self) -> dict[TokenRef, SymbolId]:
        """Return the explicit runtime realization of the Prelude token vocabulary."""
        return {
            SETMM_LPAREN_TOKEN: self.lp,
            SETMM_RPAREN_TOKEN: self.rp,
            SETMM_IMP_TOKEN: self.imp,
            SETMM_NEG_TOKEN: self.neg,
        }


# -----------------------------------------------------------------------------
# Constructors
# -----------------------------------------------------------------------------


def wff_atom(sym: SymbolId) -> Wff:
    """Construct an atomic wff from a single symbol token (usually a Var/Const)."""
    return Wff("wff", (sym,))


def imp(b: Builtins, phi: Wff, psi: Wff) -> Wff:
    """Construct ( phi -> psi ) at token level."""
    formula = build_legacy_formula(
        SETMM_PRELUDE_BINDING,
        IMP,
        (phi, psi),
        token_symbols=b.token_symbols(),
        legacy_sorts={WFF: "wff"},
    )
    return cast(Wff, formula)


def wn(b: Builtins, phi: Wff) -> Wff:
    """Construct ~phi."""
    formula = build_legacy_formula(
        SETMM_PRELUDE_BINDING,
        NOT,
        (phi,),
        token_symbols=b.token_symbols(),
        legacy_sorts={WFF: "wff"},
    )
    return cast(Wff, formula)


# -----------------------------------------------------------------------------
# Shape matching for implication
# -----------------------------------------------------------------------------


@dataclass(frozen=True)
class ImpShape:
    phi: TokenSeq
    psi: TokenSeq


@dataclass(frozen=True)
class _Tok:
    type: str
    value: SymbolId
    pos: int


def _peg_tokenize(
    tokens: Sequence[SymbolId],
    *,
    left_delimiter: SymbolId,
    right_delimiter: SymbolId,
) -> list[_Tok]:
    out: list[_Tok] = []
    for i, t in enumerate(tokens):
        if t == left_delimiter:
            out.append(_Tok("LPAREN", t, i))
        elif t == right_delimiter:
            out.append(_Tok("RPAREN", t, i))
        else:
            out.append(_Tok("SYM", t, i))
    out.append(_Tok("EOF", -1, len(tokens)))
    return out


def _peg_bal(
    *,
    left_delimiter: SymbolId,
    right_delimiter: SymbolId,
) -> tuple[Rule[TokenSeq], Rule[TokenSeq]]:
    def sym_fn(s: TokenStream, i: int) -> tuple[TokenSeq, int] | None:
        tok = s.peek(i)
        if tok.type != "SYM":
            return None
        return (tok.value,), i + 1

    sym = Rule("bal.sym", sym_fn)

    def group_fn(s: TokenStream, i: int) -> tuple[TokenSeq, int] | None:
        tok = s.peek(i)
        if tok.type != "LPAREN":
            return None
        inner_out = bal(s, i + 1)
        if inner_out is None:
            return None
        inner, j = inner_out
        close = s.peek(j)
        if close.type != "RPAREN":
            return None
        return (left_delimiter, *inner, right_delimiter), j + 1

    group = Rule("bal.group", group_fn)

    def bal_fn(s: TokenStream, i: int) -> tuple[TokenSeq, int] | None:
        acc: list[SymbolId] = []
        j = i
        while True:
            tok = s.peek(j)
            if tok.type in ("RPAREN", "EOF"):
                break
            part: tuple[TokenSeq, int] | None
            if tok.type == "LPAREN":
                part = group(s, j)
            else:
                part = sym(s, j)
            if part is None:
                return None
            frag, j = part
            acc.extend(frag)
        return tuple(acc), j

    bal = Rule("bal", bal_fn)
    return bal, group


def _peg_try_parse_split_binary(
    tokens: Sequence[SymbolId],
    *,
    left_delimiter: SymbolId,
    op: SymbolId,
    right_delimiter: SymbolId,
) -> tuple[TokenSeq, TokenSeq] | None:
    ts: TokenStream[TokenSeq] = TokenStream(
        text="",
        tokens=_peg_tokenize(
            tokens,
            left_delimiter=left_delimiter,
            right_delimiter=right_delimiter,
        ),
    )
    bal, group = _peg_bal(
        left_delimiter=left_delimiter,
        right_delimiter=right_delimiter,
    )

    def sym_any_fn(s: TokenStream, i: int) -> tuple[TokenSeq, int] | None:
        tok = s.peek(i)
        if tok.type != "SYM":
            return None
        return (tok.value,), i + 1

    sym_any = Rule("bal_no_op.sym", sym_any_fn)

    def bal_no_op_fn(s: TokenStream, i: int) -> tuple[TokenSeq, int] | None:
        acc: list[SymbolId] = []
        j = i
        while True:
            tok = s.peek(j)
            if tok.type in ("RPAREN", "EOF"):
                break
            if tok.type == "SYM" and tok.value == op:
                break
            part: tuple[TokenSeq, int] | None
            if tok.type == "LPAREN":
                part = group(s, j)
            else:
                part = sym_any(s, j)
            if part is None:
                return None
            frag, j = part
            acc.extend(frag)
        return tuple(acc), j

    bal_no_op = Rule("bal_no_op", bal_no_op_fn)

    i = 0
    if ts.peek(i).type != "LPAREN":
        return None
    left_out = bal_no_op(ts, i + 1)
    if left_out is None:
        return None
    left, j = left_out
    if not left:
        return None
    mid = ts.peek(j)
    if mid.type != "SYM" or mid.value != op:
        return None
    right_out = bal(ts, j + 1)
    if right_out is None:
        return None
    right, k = right_out
    if not right:
        return None
    if ts.peek(k).type != "RPAREN":
        return None
    if ts.peek(k + 1).type != "EOF":
        return None
    return left, right


def try_parse_imp(b: Builtins, tokens: Sequence[SymbolId]) -> ImpShape | None:
    formation = legacy_binary_formation(SETMM_PRELUDE_BINDING, IMP)
    symbols = b.token_symbols()
    parts = _peg_try_parse_split_binary(
        tokens,
        left_delimiter=symbols[formation.left_delimiter],
        op=symbols[formation.operator],
        right_delimiter=symbols[formation.right_delimiter],
    )
    if parts is None:
        return None
    left, right = parts
    return ImpShape(phi=left, psi=right)


@dataclass(frozen=True)
class NegShape:
    body: TokenSeq


def try_parse_wn(b: Builtins, tokens: Sequence[SymbolId]) -> NegShape | None:
    negation = legacy_prefix_formation(SETMM_PRELUDE_BINDING, NOT)
    implication = legacy_binary_formation(SETMM_PRELUDE_BINDING, IMP)
    symbols = b.token_symbols()
    prefix = symbols[negation.prefix]
    toks = tuple(tokens)
    if len(toks) < 2 or toks[0] != prefix:
        return None
    left_delimiter = symbols[implication.left_delimiter]
    right_delimiter = symbols[implication.right_delimiter]
    ts: TokenStream[TokenSeq] = TokenStream(
        text="",
        tokens=_peg_tokenize(
            toks[1:],
            left_delimiter=left_delimiter,
            right_delimiter=right_delimiter,
        ),
    )
    bal, _ = _peg_bal(
        left_delimiter=left_delimiter,
        right_delimiter=right_delimiter,
    )
    out = bal(ts, 0)
    if out is None:
        return None
    body, j = out
    if not body or ts.peek(j).type != "EOF":
        return None
    return NegShape(body=body)


__all__ = [
    "GLOBAL_PRELUDE_MODULE_ID",
    "Builtins",
    "ImpShape",
    "NegShape",
    "wff_atom",
    "imp",
    "wn",
    "try_parse_imp",
    "try_parse_wn",
]
