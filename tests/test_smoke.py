def test_import_prelude() -> None:
    import prelude

    assert "make_hilbert_rules" in prelude.__all__
    assert "LANGUAGE" in prelude.__all__


def test_builtins_are_foundation_only() -> None:
    from prelude.formula import Builtins
    from skfd.core.symbols import SymbolInterner

    interner = SymbolInterner()
    b = Builtins.ensure(interner, origin_ref=0)

    assert not hasattr(b, "and_")
    assert not hasattr(b, "iff")
    assert not hasattr(b, "or_")
    assert not hasattr(b, "tru")
    assert not hasattr(b, "fal")
    assert not hasattr(b, "forall")
    assert not hasattr(b, "exist")
    assert not hasattr(b, "eq")
    assert not hasattr(b, "elem")

    names = {d.local_name for d in interner.symbol_table().values()}
    assert "A." not in names
    assert "E." not in names
    assert "=" not in names
    assert "e." not in names
    assert "/\\" not in names
    assert "<->" not in names
    assert "\\/" not in names
    assert "T." not in names
    assert "F." not in names


def test_hilbert_rules_are_foundation_syntax_only() -> None:
    from prelude.hilbert_rules import DEBUG_RULES

    assert set(DEBUG_RULES) == {"wi", "wn"}


def test_semantic_language_is_separate_from_notation_and_setmm_binding() -> None:
    from skfd.authoring.ids import OwnerId
    from skfd.authoring.formula import Wff
    from skfd.authoring.metamath_language import LiteralAtom, VariableAtom
    from skfd.authoring.term import VariableRef
    from skfd.core.symbols import SymbolInterner

    from prelude.formula import Builtins, imp, wn
    from prelude.language import IMP, LANGUAGE, NOT, WFF_VARIABLE, Imp, Not
    from prelude.metamath_binding import SETMM_PRELUDE_BINDING
    from prelude.notation import PRELUDE_UNICODE_NOTATION

    phi_ref = VariableRef("schema", OwnerId("test"), "phi", WFF_VARIABLE)
    psi_ref = VariableRef("schema", OwnerId("test"), "psi", WFF_VARIABLE)
    phi = LANGUAGE.variable(phi_ref)
    psi = LANGUAGE.variable(psi_ref)

    formula = Imp(Not(phi), psi)
    assert formula.constructor == IMP
    assert formula.arguments[0].constructor == NOT
    assert PRELUDE_UNICODE_NOTATION.parse(
        "-. phi -> psi",
        {"phi": phi_ref, "psi": psi_ref},
    ) == formula

    atoms = SETMM_PRELUDE_BINDING.lower(formula)
    assert [atom.token.local_name if isinstance(atom, LiteralAtom) else atom.variable.local_key for atom in atoms] == [
        "(",
        "-.",
        "phi",
        "->",
        "psi",
        ")",
    ]
    assert sum(isinstance(atom, VariableAtom) for atom in atoms) == 2

    interner = SymbolInterner()
    builtins = Builtins.ensure(interner)
    phi_token = interner.intern(
        origin_module_id="test",
        local_name="phi",
        kind="Var",
        origin_ref=None,
    )
    psi_token = interner.intern(
        origin_module_id="test",
        local_name="psi",
        kind="Var",
        origin_ref=None,
    )
    legacy = imp(builtins, wn(builtins, Wff("wff", (phi_token,))), Wff("wff", (psi_token,)))
    symbols = interner.symbol_table()
    assert [symbols[token].local_name for token in legacy.tokens] == [
        atom.token.local_name if isinstance(atom, LiteralAtom) else atom.variable.local_key
        for atom in atoms
    ]
