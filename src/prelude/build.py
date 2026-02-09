from __future__ import annotations

from skfd.api_v2 import BuildContextV2


def manifest() -> dict[str, list[str]]:
    return {"deps": []}


def build(ctx: BuildContextV2) -> None:
    mm = ctx.mm

    wff = mm.sym.const("wff")
    ph = mm.sym.var("φ")
    wph = mm.auto.floating(ph, tc=wff)
    ax1 = mm.sym.label("ax-1")
    mm.a(ax1, tc=wff, expr=[ph])

    mm.export(wff, ph, wph, ax1)
