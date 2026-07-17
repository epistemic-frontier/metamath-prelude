from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import TypeAlias, cast

from prelude.formula import Builtins, imp, wn
from skfd.authoring.formula import Wff
from skfd.authoring.ids import ConstructorId
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
    PreludeTypingError,
    RuleSig,
    require_hyp_sort_typed,
)

from .language import IMP, LANGUAGE, NOT, WFF as SEMANTIC_WFF
from .metamath_binding import SETMM_WI_LABEL, SETMM_WN_LABEL

RuleFn: TypeAlias = Callable[..., Wff]

REGISTRY = RuleRegistry()


def _formation_sig(constructor: ConstructorId) -> RuleSig:
    declaration = LANGUAGE.constructors[constructor]
    legacy_sorts = {SEMANTIC_WFF: WFF}
    return RuleSig(
        in_sorts=tuple(legacy_sorts[item] for item in declaration.inputs),
        out_sort=legacy_sorts[declaration.output],
    )


WI_SIG = _formation_sig(IMP)
WN_SIG = _formation_sig(NOT)


@rule(label=SETMM_WI_LABEL, kind="axiom", sig=WI_SIG, registry=REGISTRY)
@dataclass(frozen=True)
class Wi:
    label: str = SETMM_WI_LABEL
    sig: RuleSig = WI_SIG
    b: Builtins | None = None

    def __call__(self, hphi: HypWff, hpsi: HypWff) -> Wff:
        if self.b is None:
            raise PreludeTypingError("wi: requires Builtins (Wi(b=...))")
        require_hyp_sort_typed(hphi, "wff", ctx=self.label)
        require_hyp_sort_typed(hpsi, "wff", ctx=self.label)
        return imp(self.b, hphi.body, hpsi.body)


@rule(label=SETMM_WN_LABEL, kind="axiom", sig=WN_SIG, registry=REGISTRY)
@dataclass(frozen=True)
class Wn:
    label: str = SETMM_WN_LABEL
    sig: RuleSig = WN_SIG
    b: Builtins | None = None

    def __call__(self, hphi: HypWff) -> Wff:
        if self.b is None:
            raise PreludeTypingError("wn: requires Builtins (Wn(b=...))")
        require_hyp_sort_typed(hphi, "wff", ctx=self.label)
        return wn(self.b, hphi.body)


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
    "Wn",
    "make_rules",
    "DEBUG_CATALOG",
    "DEBUG_RULES",
]
