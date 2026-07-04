# set.mm Prelude (Lines 1–648)

This document records the historical source mapping from `set.mm` (first 700
lines) to the current `metamath-prelude` package.

## Boundary (precise line numbers)

Using [set.mm](file:///Users/mingli/MetaMath/set.mm/set.mm) line numbers:
- **Foundation prelude**: the ambient frame in `set.mm` lines `1–648`
  (constants, variables, floating hypotheses, `wn`, `wi`)
- **Logic**: starts with ordinary logic content, including the helper theorems
  `idi` / `a1ii` from the same historical prefix and the later `ax-mp` block.

Rationale:
- Up to line 648, the file defines *tokens, variables, floating hypotheses, and
  the recursive syntax of wffs* (`wn`, `wi`) plus a couple of proof-development
  helper inferences (`idi`, `a1ii`).
- ProofScaffold now treats `metamath-prelude` as the global foundation scope.
  Therefore `idi` and `a1ii` are documented here for source alignment, but are
  emitted by `metamath-logic`.
- From line 649 onward, the database introduces the *provability-layer axioms/rules* of propositional calculus (`ax-mp`, `ax-1..ax-3`) which are the natural start of `logic`.

## What is migrated into `metamath-prelude`

### 1) Core constant tokens
Source:
- Primitive constants for propositional calculus: [set.mm:L362-L370](file:///Users/mingli/MetaMath/set.mm/set.mm#L362-L370)

Implementation:
- Builtin token interning is centralized in [formula.py](file:///Users/mingli/MetaMath/metamath-prelude/src/prelude/formula.py) (`Builtins.ensure`).
- `wff` and `|-` are explicitly interned as global-stable Const symbols in [build.py](file:///Users/mingli/MetaMath/metamath-prelude/src/prelude/build.py).
- `GLOBAL_PRELUDE_MODULE_ID="__prelude__"` is the canonical foundation symbol
  namespace. Downstream packages may reuse it through `Builtins.ensure(...)` for
  stable vocabulary `SymbolId`s; theorem labels and proof dependencies still
  flow through package exports and linker checks.

Note:
- set.mm also declares typographical constants `&` and `=>` ([set.mm:L388-L393](file:///Users/mingli/MetaMath/set.mm/set.mm#L388-L393)). These are *comment-only* symbols in set.mm; we preserve them in documentation, but we do not currently force emission of unused `$c` declarations in generated `.mm`.

### 2) Wff variable pool (`$v`) and floating hypotheses (`$f`)
Source:
- Variable declarations: [set.mm:L394-L409](file:///Users/mingli/MetaMath/set.mm/set.mm#L394-L409)
- Floating hypotheses: [set.mm:L410-L437](file:///Users/mingli/MetaMath/set.mm/set.mm#L410-L437)

Implementation:
- Variables `ph ps ch th ta et ze si rh mu la ka` are interned under the global prelude module id in [build.py](file:///Users/mingli/MetaMath/metamath-prelude/src/prelude/build.py).
- Floating hypotheses are emitted explicitly using `mm.f(...)` with set.mm labels:
  `wph wps wch wth wta wet wze wsi wrh wmu wla wka`.

### 3) Wff recursive syntax (`wn`, `wi`)
Source:
- Negation syntax axiom `wn`: [set.mm:L561-L575](file:///Users/mingli/MetaMath/set.mm/set.mm#L561-L575)
- Implication syntax axiom `wi`: [set.mm:L576-L616](file:///Users/mingli/MetaMath/set.mm/set.mm#L576-L616)

Implementation:
- Emitted as `$a` with `tc=wff` in [build.py](file:///Users/mingli/MetaMath/metamath-prelude/src/prelude/build.py).
- Token shapes are constructed using the builtin constants from [formula.py](file:///Users/mingli/MetaMath/metamath-prelude/src/prelude/formula.py).

### 4) Proof-development helper inferences (`idi`, `a1ii`)
Source:
- Helper inferences section: [set.mm:L440-L518](file:///Users/mingli/MetaMath/set.mm/set.mm#L440-L518)

Implementation:
- These labels are now emitted by `metamath-logic`, not by
  `metamath-prelude`. They are ordinary proof helpers with local `$e`
  hypotheses, not foundation-scope mechanics.

## Verification expectation (sanity check)

After building `metamath-prelude`, the generated monolith should contain:
- `$c ... wff |- $.`
- `$v ph ps ch th ta et ze si rh mu la ka $.`
- `$f` declarations for all the above variables
- `wn $a wff -. ph $.`
- `wi $a wff ( ph -> ps ) $.`
- no `wo`, `wtru`, `wfal`, `idi`, or `a1ii` labels; those are emitted by
  `metamath-logic`
