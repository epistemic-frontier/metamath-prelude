"""Semantic foundation language shared by standard ProofScaffold packages."""

from __future__ import annotations

from skfd.authoring.ids import ConstructorId, LanguageId, SortId, VariableKindId
from skfd.authoring.language import (
    ConstructorDecl,
    LanguageSpec,
    SortDecl,
    VariableKindDecl,
    resolve_language,
)
from skfd.authoring.term import App, Term

PRELUDE_LANGUAGE_ID = LanguageId("metamath-prelude#language:foundation")

WFF = SortId("metamath-prelude#sort:wff")
WFF_VARIABLE = VariableKindId("metamath-prelude#variable-kind:wff")

NOT = ConstructorId("metamath-prelude#constructor:not")
IMP = ConstructorId("metamath-prelude#constructor:imp")

LANGUAGE_SPEC = LanguageSpec(
    id=PRELUDE_LANGUAGE_ID,
    sorts=(SortDecl(id=WFF),),
    variable_kinds=(VariableKindDecl(id=WFF_VARIABLE, sort=WFF),),
    constructors=(
        ConstructorDecl(id=NOT, inputs=(WFF,), output=WFF),
        ConstructorDecl(id=IMP, inputs=(WFF, WFF), output=WFF),
    ),
)

LANGUAGE = resolve_language(LANGUAGE_SPEC, {})


def Not(term: Term) -> App:
    """Construct semantic negation without binding a Metamath runtime."""
    return LANGUAGE.apply(NOT, (term,))


def Imp(left: Term, right: Term) -> App:
    """Construct semantic implication without binding a Metamath runtime."""
    return LANGUAGE.apply(IMP, (left, right))


__all__ = [
    "IMP",
    "LANGUAGE",
    "LANGUAGE_SPEC",
    "NOT",
    "PRELUDE_LANGUAGE_ID",
    "WFF",
    "WFF_VARIABLE",
    "Imp",
    "Not",
]
