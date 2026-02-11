# set.mm Prelude (Lines 1–648)

This document records the *source-of-truth mapping* from `set.mm` (first 700 lines) to the current `metamath-prelude` package.

## Boundary (precise line numbers)

Using [set.mm](file:///Users/mingli/MetaMath/set.mm/set.mm) line numbers:
- **Prelude**: `1–648` (inclusive)
- **Logic**: starts at **line 649** (`${ ... ax-mp ... $}` block begins)

Rationale:
- Up to line 648, the file defines *tokens, variables, floating hypotheses, and the recursive syntax of wffs* (`wn`, `wi`) plus a couple of proof-development helper inferences (`idi`, `a1ii`).
- From line 649 onward, the database introduces the *provability-layer axioms/rules* of propositional calculus (`ax-mp`, `ax-1..ax-3`) which are the natural start of `logic`.

## What is migrated into `metamath-prelude`

### 1) Core constant tokens
Source:
- Primitive constants for propositional calculus: [set.mm:L362-L370](file:///Users/mingli/MetaMath/set.mm/set.mm#L362-L370)

Implementation:
- Builtin token interning is centralized in [formula.py](file:///Users/mingli/MetaMath/metamath-prelude/src/prelude/formula.py) (`Builtins.ensure`).
- `wff` and `|-` are explicitly interned as global-stable Const symbols in [build.py](file:///Users/mingli/MetaMath/metamath-prelude/src/prelude/build.py).

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
- Both are emitted as theorems with `tc="|-"` in [build.py](file:///Users/mingli/MetaMath/metamath-prelude/src/prelude/build.py) using the simplest possible proofs:
  - `idi`: proof is just the hypothesis `idi.1`
  - `a1ii`: proof is just the hypothesis `a1ii.1` (second hypothesis exists for proof-workflow compatibility, matching set.mm intent)

## Verification expectation (sanity check)

After building `metamath-prelude`, the generated monolith should contain:
- `$c ... wff |- $.`
- `$v ph ps ch th ta et ze si rh mu la ka $.`
- `$f` declarations for all the above variables
- `wn $a wff -. ph $.`
- `wi $a wff ( ph -> ps ) $.`
- `idi` and `a1ii` as `|-` theorems

