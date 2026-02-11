def test_import_prelude() -> None:
    import prelude

    assert "make_hilbert_rules" in prelude.__all__

