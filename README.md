# metamath-prelude

`metamath-prelude` is a small Python package that exports the “prelude” layer used by ProofScaffold-based Metamath projects.
It provides the core constants, variables, and a minimal set of foundational statements that downstream packages can depend on and link against.

## Versioning

- Package version: `0.0.7`
- ProofScaffold dependency: `proof-scaffold==0.0.13`

## Installation

This package is published on PyPI: https://pypi.org/project/metamath-prelude/

With `uv`:

```bash
uv add metamath-prelude
```

## What this package contains

- A ProofScaffold `build.py` entrypoint that emits the foundation frame as a linkable unit.
- Authoring helpers for foundation syntax only (`wi` / `wn`).
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

- Foundation boundary: prelude emits only the ambient frame (`wff`, `|-`, schema variables and `$f`, `wn`, `wi`).
- Logic-owned helpers and syntax such as `mp`, `wa`, `wo`, `wb`, `wtru`,
  `wfal`, `idi`, and `a1ii` live in `metamath-logic`.
- Mapping notes and migrated comments: [`docs/SETMM_PRELUDE_1_648.md`](docs/SETMM_PRELUDE_1_648.md)
