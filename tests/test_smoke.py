def test_import_prelude() -> None:
    import prelude

    assert "make_hilbert_rules" in prelude.__all__


def test_builtins_do_not_intern_predicate_tokens() -> None:
    from prelude.formula import Builtins
    from skfd.core.symbols import SymbolInterner

    interner = SymbolInterner()
    b = Builtins.ensure(interner, origin_ref=0)

    assert not hasattr(b, "forall")
    assert not hasattr(b, "exist")
    assert not hasattr(b, "eq")
    assert not hasattr(b, "elem")

    names = {d.local_name for d in interner.symbol_table().values()}
    assert "A." not in names
    assert "E." not in names
    assert "=" not in names
    assert "e." not in names
