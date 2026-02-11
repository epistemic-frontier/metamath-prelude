# metamath-prelude

`metamath-prelude` is a small Python package that exports the “prelude” layer used by ProofScaffold-based Metamath projects.
It provides the core constants, variables, and a minimal set of foundational statements that downstream packages can depend on and link against.

## Versioning

- Package version: `0.0.1`
- ProofScaffold dependency: `proof-scaffold==0.0.4`

## What this package contains

- A ProofScaffold `build.py` entrypoint that emits the prelude statements as a linkable unit.
- Authoring helpers for the Hilbert-style propositional fragment (rule bundle used by downstream proof scripts).
- A documented alignment with the early part of `set.mm`.

## Verification

This repository uses `uv` for reproducible installs and runs `skfd verify --level 1` as the primary correctness gate.

From the `metamath-prelude/` directory:

```bash
uv sync --locked --dev
uv run --frozen ruff check .
uv run --frozen mypy .
uv run --frozen python -m pytest
uv run --frozen skfd verify --level 1 metamath-prelude
```

`skfd verify` builds the package into a verification monolith (under `target/`) and checks it with the configured verifiers.

## set.mm alignment

- Milestone boundary (within the first ~700 lines): prelude = `set.mm` lines 1–648; propositional logic starts at line 649 (the `ax-mp` block).
- Mapping notes and migrated comments: [`docs/SETMM_PRELUDE_1_648.md`](docs/SETMM_PRELUDE_1_648.md)
