from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import TypeAlias, cast

from prelude.formula import Builtins, imp, try_parse_imp, wa, wn
from skfd.authoring.formula import Wff
from skfd.authoring.rules import (
    RuleBundle,
    RuleRegistry,
    build_rule_bundle,
    build_rule_catalog,
    rule,
    rules_view,
)
from skfd.authoring.typing import (
    WFF,
    HypWff,
    PreludeShapeError,
    PreludeTypingError,
    RuleSig,
    require_hyp_sort_typed,
)

RuleFn: TypeAlias = Callable[..., Wff]

REGISTRY = RuleRegistry()

@rule(label="wi", kind="axiom", sig=RuleSig(in_sorts=(WFF, WFF), out_sort=WFF), registry=REGISTRY)
@dataclass(frozen=True)
class Wi:
    label: str = "wi"
    sig: RuleSig = RuleSig(in_sorts=(WFF, WFF), out_sort=WFF)
    b: Builtins | None = None

    def __call__(self, hphi: HypWff, hpsi: HypWff) -> Wff:
        if self.b is None:
            raise PreludeTypingError("wi: requires Builtins (Wi(b=...))")
        require_hyp_sort_typed(hphi, "wff", ctx=self.label)
        require_hyp_sort_typed(hpsi, "wff", ctx=self.label)
        return imp(self.b, hphi.body, hpsi.body)


@rule(label="mp", kind="rule", sig=RuleSig(in_sorts=(WFF, WFF), out_sort=WFF), registry=REGISTRY)
@dataclass(frozen=True)
class Mp:
    label: str = "mp"
    sig: RuleSig = RuleSig(in_sorts=(WFF, WFF), out_sort=WFF)
    b: Builtins | None = None

    def __call__(self, hyp_phi: HypWff, hyp_imp: HypWff) -> Wff:
        if self.b is None:
            raise PreludeTypingError("mp: requires Builtins (Mp(b=...))")
        require_hyp_sort_typed(hyp_phi, "wff", ctx=self.label)
        require_hyp_sort_typed(hyp_imp, "wff", ctx=self.label)

        shp = try_parse_imp(self.b, hyp_imp.body.tokens)
        if shp is None:
            raise PreludeShapeError(f"{self.label}: expected token shape '( phi -> psi )'")

        if hyp_phi.body.tokens != shp.phi:
            raise PreludeShapeError(f"{self.label}: antecedent mismatch (token-level)")

        return Wff("wff", shp.psi)


@rule(label="wn", kind="axiom", sig=RuleSig(in_sorts=(WFF,), out_sort=WFF), registry=REGISTRY)
@dataclass(frozen=True)
class Wn:
    label: str = "wn"
    sig: RuleSig = RuleSig(in_sorts=(WFF,), out_sort=WFF)
    b: Builtins | None = None

    def __call__(self, hphi: HypWff) -> Wff:
        if self.b is None:
            raise PreludeTypingError("wn: requires Builtins (Wn(b=...))")
        require_hyp_sort_typed(hphi, "wff", ctx=self.label)
        return wn(self.b, hphi.body)


@rule(label="wa", kind="axiom", sig=RuleSig(in_sorts=(WFF, WFF), out_sort=WFF), registry=REGISTRY)
@dataclass(frozen=True)
class Wa:
    label: str = "wa"
    sig: RuleSig = RuleSig(in_sorts=(WFF, WFF), out_sort=WFF)
    b: Builtins | None = None

    def __call__(self, hphi: HypWff, hpsi: HypWff) -> Wff:
        if self.b is None:
            raise PreludeTypingError("wa: requires Builtins (Wa(b=...))")
        require_hyp_sort_typed(hphi, "wff", ctx=self.label)
        require_hyp_sort_typed(hpsi, "wff", ctx=self.label)
        return wa(self.b, hphi.body, hpsi.body)


def make_rules(b: Builtins) -> RuleBundle:
    def _bind(cls: Callable[..., object]) -> Callable[..., object]:
        return cast(Callable[..., object], cls(b=b))

    return build_rule_bundle(REGISTRY, bind=_bind)


def _bind_debug(cls: Callable[..., object]) -> Callable[..., object]:
    return cast(Callable[..., object], cls())

DEBUG_CATALOG = build_rule_catalog(REGISTRY, bind=_bind_debug)

DEBUG_RULES: Mapping[str, RuleFn] = cast(Mapping[str, RuleFn], rules_view(DEBUG_CATALOG))


__all__ = [
    "Wi",
    "Mp",
    "Wn",
    "Wa",
    "make_rules",
    "DEBUG_CATALOG",
    "DEBUG_RULES",
]
