from __future__ import annotations

from skfd.api_v2 import BuildContextV2

from prelude.formula import Builtins, GLOBAL_PRELUDE_MODULE_ID


def build(ctx: BuildContextV2) -> None:
    mm = ctx.mm

    b = Builtins.ensure(mm.interner, origin_ref=0)

    wff = mm.interner.intern(
        origin_module_id=GLOBAL_PRELUDE_MODULE_ID,
        local_name="wff",
        kind="Const",
        origin_ref=0,
    )
    provable = mm.interner.intern(
        origin_module_id=GLOBAL_PRELUDE_MODULE_ID,
        local_name="|-",
        kind="Const",
        origin_ref=0,
    )

    ph = mm.interner.intern(
        origin_module_id=GLOBAL_PRELUDE_MODULE_ID,
        local_name=ctx.names.canonicalize("Var", "φ"),
        kind="Var",
        origin_ref=0,
    )
    ps = mm.interner.intern(
        origin_module_id=GLOBAL_PRELUDE_MODULE_ID,
        local_name=ctx.names.canonicalize("Var", "ψ"),
        kind="Var",
        origin_ref=0,
    )
    ch = mm.interner.intern(
        origin_module_id=GLOBAL_PRELUDE_MODULE_ID,
        local_name=ctx.names.canonicalize("Var", "χ"),
        kind="Var",
        origin_ref=0,
    )

    wph = mm.auto.floating(ph, tc=wff)
    wps = mm.auto.floating(ps, tc=wff)
    wch = mm.auto.floating(ch, tc=wff)

    wn = mm.sym.label("wn")
    wi = mm.sym.label("wi")
    wa = mm.sym.label("wa")

    mm.a(wn, tc=wff, expr=[b.neg, ph])
    mm.a(wi, tc=wff, expr=[b.lp, ph, b.imp, ps, b.rp])
    mm.a(wa, tc=wff, expr=[b.lp, ph, b.and_, ps, b.rp])

    mm.export(provable, wff, ph, ps, ch, wph, wps, wch, wn, wi, wa)
