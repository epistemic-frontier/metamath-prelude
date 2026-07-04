def test_import_prelude() -> None:
    import prelude

    assert "make_hilbert_rules" in prelude.__all__


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
