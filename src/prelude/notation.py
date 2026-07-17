"""Human notation for the semantic foundation language."""

from skfd.authoring.language import LanguageRequirement
from skfd.authoring.notation import (
    InfixForm,
    NotationDecl,
    NotationId,
    NotationSpec,
    PrefixForm,
    resolve_notation,
)

from .language import IMP, LANGUAGE, NOT

PRELUDE_UNICODE_NOTATION_ID = NotationId("metamath-prelude#notation:unicode")

PRELUDE_UNICODE_NOTATION_SPEC = NotationSpec(
    id=PRELUDE_UNICODE_NOTATION_ID,
    language=LanguageRequirement(
        id=LANGUAGE.id,
        semantic_digest=LANGUAGE.semantic_digest,
    ),
    declarations=(
        NotationDecl(
            constructor=NOT,
            form=PrefixForm(token="¬", precedence=30),
            aliases=("-.", "~"),
        ),
        NotationDecl(
            constructor=IMP,
            form=InfixForm(token="→", precedence=20, associativity="right"),
            aliases=("->", "⇒"),
        ),
    ),
)

PRELUDE_UNICODE_NOTATION = resolve_notation(
    PRELUDE_UNICODE_NOTATION_SPEC,
    LANGUAGE,
    {},
)

__all__ = [
    "PRELUDE_UNICODE_NOTATION",
    "PRELUDE_UNICODE_NOTATION_ID",
    "PRELUDE_UNICODE_NOTATION_SPEC",
]
