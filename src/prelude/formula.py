# prelude/formula.py
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import (
    Any,
)

from skfd.authoring.formula import TokenSeq, Wff
from skfd.core.peg import Rule, TokenStream
from skfd.core.symbols import SymbolId, SymbolInterner

# -----------------------------------------------------------------------------
# Reserved / builtin tokens (by name)
# -----------------------------------------------------------------------------

# Canonical foundation symbol namespace. Downstream logic packages may call
# Builtins.ensure(...) to recover the same builtin Const ids, but proof labels
# still have to come through package exports and linker access checks.
GLOBAL_PRELUDE_MODULE_ID: str = "__prelude__"


@dataclass(frozen=True)
class Builtins:
    """Builtin constant tokens used by foundation/propositional authoring.

    These are Const symbols in the interner, not magic.
    """

    lp: SymbolId  # "("
    rp: SymbolId  # ")"
    imp: SymbolId  # "->"
    neg: SymbolId  # "-."
    and_: SymbolId  # "/\\"
    iff: SymbolId  # "<->"
    or_: SymbolId  # "\/"
    tru: SymbolId  # "T." (verum / top)
    fal: SymbolId  # "F." (falsum / bottom)

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
            origin_module_id=origin_module_id, local_name="(", kind="Const", origin_ref=origin_ref
        )
        rp = interner.intern(
            origin_module_id=origin_module_id, local_name=")", kind="Const", origin_ref=origin_ref
        )
        imp = interner.intern(
            origin_module_id=origin_module_id, local_name="->", kind="Const", origin_ref=origin_ref
        )
        neg = interner.intern(
            origin_module_id=origin_module_id, local_name="-.", kind="Const", origin_ref=origin_ref
        )
        and_ = interner.intern(
            origin_module_id=origin_module_id, local_name="/\\", kind="Const", origin_ref=origin_ref
        )
        iff = interner.intern(
            origin_module_id=origin_module_id, local_name="<->", kind="Const", origin_ref=origin_ref
        )
        or_ = interner.intern(
            origin_module_id=origin_module_id, local_name="\\/", kind="Const", origin_ref=origin_ref
        )
        tru = interner.intern(
            origin_module_id=origin_module_id, local_name="T.", kind="Const", origin_ref=origin_ref
        )
        fal = interner.intern(
            origin_module_id=origin_module_id, local_name="F.", kind="Const", origin_ref=origin_ref
        )
        return Builtins(
            lp=lp,
            rp=rp,
            imp=imp,
            neg=neg,
            and_=and_,
            iff=iff,
            or_=or_,
            tru=tru,
            fal=fal,
        )


# -----------------------------------------------------------------------------
# Constructors
# -----------------------------------------------------------------------------


def wff_atom(sym: SymbolId) -> Wff:
    """Construct an atomic wff from a single symbol token (usually a Var/Const)."""
    return Wff("wff", (sym,))


def imp(b: Builtins, phi: Wff, psi: Wff) -> Wff:
    """Construct ( phi -> psi ) at token level."""
    return Wff("wff", (b.lp, *phi.tokens, b.imp, *psi.tokens, b.rp))


def wn(b: Builtins, phi: Wff) -> Wff:
    """Construct ~phi."""
    return Wff("wff", (b.neg, *phi.tokens))


def wa(b: Builtins, phi: Wff, psi: Wff) -> Wff:
    r"""Construct ( phi /\ psi )."""
    return Wff("wff", (b.lp, *phi.tokens, b.and_, *psi.tokens, b.rp))


def wo(b: Builtins, phi: Wff, psi: Wff) -> Wff:
    r"""Construct ( phi \/ psi )."""
    return Wff("wff", (b.lp, *phi.tokens, b.or_, *psi.tokens, b.rp))


def wb(b: Builtins, phi: Wff, psi: Wff) -> Wff:
    """Construct ( phi <-> psi )."""
    return Wff("wff", (b.lp, *phi.tokens, b.iff, *psi.tokens, b.rp))


def wtru(b: Builtins) -> Wff:
    """Construct T. (verum / top)."""
    return Wff("wff", (b.tru,))


def wfal(b: Builtins) -> Wff:
    """Construct F. (falsum / bottom)."""
    return Wff("wff", (b.fal,))


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


def _peg_tokenize(b: Builtins, tokens: Sequence[SymbolId]) -> list[_Tok]:
    out: list[_Tok] = []
    for i, t in enumerate(tokens):
        if t == b.lp:
            out.append(_Tok("LPAREN", t, i))
        elif t == b.rp:
            out.append(_Tok("RPAREN", t, i))
        else:
            out.append(_Tok("SYM", t, i))
    out.append(_Tok("EOF", -1, len(tokens)))
    return out


def _peg_bal(
    b: Builtins,
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
        return (b.lp, *inner, b.rp), j + 1

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
    b: Builtins, tokens: Sequence[SymbolId], *, op: SymbolId
) -> tuple[TokenSeq, TokenSeq] | None:
    ts: TokenStream[TokenSeq] = TokenStream(text="", tokens=_peg_tokenize(b, tokens))
    bal, group = _peg_bal(b)

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
    parts = _peg_try_parse_split_binary(b, tokens, op=b.imp)
    if parts is None:
        return None
    left, right = parts
    return ImpShape(phi=left, psi=right)


@dataclass(frozen=True)
class NegShape:
    body: TokenSeq


def try_parse_wn(b: Builtins, tokens: Sequence[SymbolId]) -> NegShape | None:
    toks = tuple(tokens)
    if len(toks) < 2 or toks[0] != b.neg:
        return None
    ts: TokenStream[TokenSeq] = TokenStream(text="", tokens=_peg_tokenize(b, toks[1:]))
    bal, _ = _peg_bal(b)
    out = bal(ts, 0)
    if out is None:
        return None
    body, j = out
    if not body or ts.peek(j).type != "EOF":
        return None
    return NegShape(body=body)


@dataclass(frozen=True)
class AndShape:
    left: TokenSeq
    right: TokenSeq


def try_parse_wa(b: Builtins, tokens: Sequence[SymbolId]) -> AndShape | None:
    parts = _peg_try_parse_split_binary(b, tokens, op=b.and_)
    if parts is None:
        return None
    left, right = parts
    return AndShape(left=left, right=right)


__all__ = [
    "GLOBAL_PRELUDE_MODULE_ID",
    "Builtins",
    "wff_atom",
    "imp",
    "wn",
    "wa",
    "wo",
    "wb",
    "wtru",
    "wfal",
]
