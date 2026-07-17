"""set.mm-compatible realization of the semantic foundation language."""

from skfd.authoring.ids import (
    AssertionSemanticId,
    BackendBindingId,
    BackendVocabularyId,
    FoundationId,
)
from skfd.authoring.language import LanguageRequirement
from skfd.authoring.metamath_language import (
    ArgumentPart,
    FormationBinding,
    FoundationRequirement,
    LiteralPart,
    MetamathLanguageBinding,
    SortTypecodeBinding,
    TokenRef,
    resolve_metamath_language,
)

from .language import IMP, LANGUAGE, NOT, WFF

PRELUDE_VOCABULARY = BackendVocabularyId("metamath-prelude#vocabulary:setmm")
SETMM_FOUNDATION = FoundationId("metamath-prelude#foundation:setmm")
SETMM_PRELUDE_BINDING_ID = BackendBindingId("metamath-prelude#binding:setmm")


def _token(local_name: str) -> TokenRef:
    return TokenRef(PRELUDE_VOCABULARY, local_name)


SETMM_LPAREN_TOKEN = _token("(")
SETMM_RPAREN_TOKEN = _token(")")


SETMM_PRELUDE_BINDING_SPEC = MetamathLanguageBinding(
    id=SETMM_PRELUDE_BINDING_ID,
    language=LanguageRequirement(
        id=LANGUAGE.id,
        semantic_digest=LANGUAGE.semantic_digest,
    ),
    foundation=FoundationRequirement(id=SETMM_FOUNDATION),
    sort_typecodes=(SortTypecodeBinding(sort=WFF, typecode=_token("wff")),),
    formations=(
        FormationBinding(
            constructor=NOT,
            syntax_assertion=AssertionSemanticId("metamath-prelude#formation:wn"),
            template=(LiteralPart(_token("-.")), ArgumentPart(0)),
        ),
        FormationBinding(
            constructor=IMP,
            syntax_assertion=AssertionSemanticId("metamath-prelude#formation:wi"),
            template=(
                LiteralPart(SETMM_LPAREN_TOKEN),
                ArgumentPart(0),
                LiteralPart(_token("->")),
                ArgumentPart(1),
                LiteralPart(SETMM_RPAREN_TOKEN),
            ),
        ),
    ),
)

SETMM_PRELUDE_BINDING = resolve_metamath_language(
    SETMM_PRELUDE_BINDING_SPEC,
    LANGUAGE,
    {},
)

__all__ = [
    "PRELUDE_VOCABULARY",
    "SETMM_FOUNDATION",
    "SETMM_LPAREN_TOKEN",
    "SETMM_PRELUDE_BINDING",
    "SETMM_PRELUDE_BINDING_ID",
    "SETMM_PRELUDE_BINDING_SPEC",
    "SETMM_RPAREN_TOKEN",
]
