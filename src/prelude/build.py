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

    ph = mm.interner.intern(origin_module_id=GLOBAL_PRELUDE_MODULE_ID, local_name="ph", kind="Var", origin_ref=0)
    ps = mm.interner.intern(origin_module_id=GLOBAL_PRELUDE_MODULE_ID, local_name="ps", kind="Var", origin_ref=0)
    ch = mm.interner.intern(origin_module_id=GLOBAL_PRELUDE_MODULE_ID, local_name="ch", kind="Var", origin_ref=0)
    th = mm.interner.intern(origin_module_id=GLOBAL_PRELUDE_MODULE_ID, local_name="th", kind="Var", origin_ref=0)
    ta = mm.interner.intern(origin_module_id=GLOBAL_PRELUDE_MODULE_ID, local_name="ta", kind="Var", origin_ref=0)
    et = mm.interner.intern(origin_module_id=GLOBAL_PRELUDE_MODULE_ID, local_name="et", kind="Var", origin_ref=0)
    ze = mm.interner.intern(origin_module_id=GLOBAL_PRELUDE_MODULE_ID, local_name="ze", kind="Var", origin_ref=0)
    si = mm.interner.intern(origin_module_id=GLOBAL_PRELUDE_MODULE_ID, local_name="si", kind="Var", origin_ref=0)
    rh = mm.interner.intern(origin_module_id=GLOBAL_PRELUDE_MODULE_ID, local_name="rh", kind="Var", origin_ref=0)
    mu = mm.interner.intern(origin_module_id=GLOBAL_PRELUDE_MODULE_ID, local_name="mu", kind="Var", origin_ref=0)
    la = mm.interner.intern(origin_module_id=GLOBAL_PRELUDE_MODULE_ID, local_name="la", kind="Var", origin_ref=0)
    ka = mm.interner.intern(origin_module_id=GLOBAL_PRELUDE_MODULE_ID, local_name="ka", kind="Var", origin_ref=0)

    wph = mm.f(mm.sym.label("wph"), tc=wff, var=ph)
    wps = mm.f(mm.sym.label("wps"), tc=wff, var=ps)
    wch = mm.f(mm.sym.label("wch"), tc=wff, var=ch)
    wth = mm.f(mm.sym.label("wth"), tc=wff, var=th)
    wta = mm.f(mm.sym.label("wta"), tc=wff, var=ta)
    wet = mm.f(mm.sym.label("wet"), tc=wff, var=et)
    wze = mm.f(mm.sym.label("wze"), tc=wff, var=ze)
    wsi = mm.f(mm.sym.label("wsi"), tc=wff, var=si)
    wrh = mm.f(mm.sym.label("wrh"), tc=wff, var=rh)
    wmu = mm.f(mm.sym.label("wmu"), tc=wff, var=mu)
    wla = mm.f(mm.sym.label("wla"), tc=wff, var=la)
    wka = mm.f(mm.sym.label("wka"), tc=wff, var=ka)

    wn = mm.sym.label("wn")
    wi = mm.sym.label("wi")

    mm.a(wn, tc=wff, expr=[b.neg, ph])
    mm.a(wi, tc=wff, expr=[b.lp, ph, b.imp, ps, b.rp])

    with mm.block():
        mm.e(mm.sym.label("idi.1"), tc=provable, expr=[ph])
        mm.p(mm.sym.label("idi"), tc=provable, expr=[ph], proof=[mm.sym.label("idi.1")])

    with mm.block():
        mm.e(mm.sym.label("a1ii.1"), tc=provable, expr=[ph])
        mm.e(mm.sym.label("a1ii.2"), tc=provable, expr=[ps])
        mm.p(mm.sym.label("a1ii"), tc=provable, expr=[ph], proof=[mm.sym.label("a1ii.1")])

    mm.export(
        provable,
        wff,
        ph,
        ps,
        ch,
        th,
        ta,
        et,
        ze,
        si,
        rh,
        mu,
        la,
        ka,
        wph,
        wps,
        wch,
        wth,
        wta,
        wet,
        wze,
        wsi,
        wrh,
        wmu,
        wla,
        wka,
        wn,
        wi,
        mm.sym.label("idi"),
        mm.sym.label("a1ii"),
    )
