# src/prelude/build.py
from typing import Any
from skfd.builder import MMBuilder

def manifest() -> dict[str, Any]:
    return {"deps": []}

def build(mm: MMBuilder, **deps: Any) -> Any:
    # 1. Constants
    mm.c("wff")
    
    # 2. Variables
    mm.v("ph")
    
    # 3. Floating Hyps
    mm.f("wph", "wff", "ph")
    
    # 4. Axiom: |- ph
    mm.a("ax-1", "wff", "ph")
    
    # 5. Export
    exports = {
        "wff": mm._intern_const("wff"),
        "ph": mm._intern_var("ph"),
        "wph": mm._intern_label("wph"),
        "ax-1": mm._intern_label("ax-1"),
    }
    
    # Export everything needed
    mm.export("wph", "ax-1")
    
    return exports
