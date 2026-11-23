import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
DATA = ROOT / "ep01_unlikely" / "data"
FACTS = json.loads((DATA / "facts.json").read_text())
CLAIMS = json.loads((DATA / "claims.json").read_text())

from common import style  # noqa: E402
style.setup()
from manim import config as _cfg  # noqa: E402
_cfg.disable_caching = True

import numpy as np  # noqa: E402
from manim import (VGroup, VMobject, Dot, Circle, Line, Rectangle, RoundedRectangle, Tex, MathTex,  # noqa: E402
                   Arc, UP, DOWN, LEFT, RIGHT, UR, PI, ManimColor)
from common.style import FG, MUTED, HEADS, TAILS, LLN, CLT, LDP, BG  # noqa: E402


def sci(log10v, digits=1):
    """LaTeX for 10**log10v as  a\\times10^{b}."""
    e = int(np.floor(log10v))
    m = 10 ** (log10v - e)
    if round(m, digits) >= 10:
        m, e = m / 10, e + 1
    return r"%.*f\times10^{%d}" % (digits, m, e)


def coin_grid(cols=40, rows=25, step=0.2, radius=0.075, center=(0, 0.35, 0), states=None):
    """A grid of coins (dots). states: boolean array (True = heads)."""
    g = VGroup()
    x0 = center[0] - (cols - 1) * step / 2
    y0 = center[1] + (rows - 1) * step / 2
    for r in range(rows):
        for c in range(cols):
            d = Dot([x0 + c * step, y0 - r * step, 0], radius=radius, color=MUTED)
            g.add(d)
    if states is not None:
        paint(g, states)
    return g


def paint(grid, states):
    for d, s in zip(grid, states):
        d.set_color(HEADS if s else TAILS)


def area(ax, xs, ys, color, opacity=0.55, stroke=2.0, base=0.0):
    """Filled region under a curve given in data coordinates."""
    pts = [ax.c2p(x, y) for x, y in zip(xs, ys)]
    poly = VMobject()
    poly.set_points_as_corners([ax.c2p(xs[0], base), *pts, ax.c2p(xs[-1], base)])
    poly.set_fill(color, opacity).set_stroke(color, stroke)
    return poly


def steps(ax, edges, heights, color, opacity=0.55, stroke=1.5, base=0.0):
    """Histogram drawn as a single filled step polygon (edges has len(heights)+1 entries)."""
    xs, ys = [edges[0]], [base]
    for i, h in enumerate(heights):
        xs += [edges[i], edges[i + 1]]
        ys += [h, h]
    xs.append(edges[-1]); ys.append(base)
    poly = VMobject()
    poly.set_points_as_corners([ax.c2p(x, y) for x, y in zip(xs, ys)])
    poly.set_fill(color, opacity).set_stroke(color, stroke)
    return poly


def curve(ax, xs, ys, color, width=3.0):
    m = VMobject()
    m.set_points_smoothly([ax.c2p(x, y) for x, y in zip(xs, ys)]) if len(xs) < 400 else \
        m.set_points_as_corners([ax.c2p(x, y) for x, y in zip(xs, ys)])
    return m.set_stroke(color, width).set_fill(opacity=0)


def lens(num, label, color, scale=1.0):
    """A small magnifying-glass badge: 'Lens 1 · label'."""
    ring = Circle(radius=0.26, color=color, stroke_width=4)
    handle = Line(ring.point_at_angle(-PI / 4), ring.point_at_angle(-PI / 4) + 0.22 * np.array([1, -1, 0]),
                  color=color, stroke_width=6)
    n = Tex(str(num), font_size=30, color=color).move_to(ring)
    t = Tex(label, font_size=30, color=color).next_to(ring, RIGHT, buff=0.25)
    return VGroup(ring, handle, n, t).scale(scale)


def card(title, body, color, width=5.6, height=2.4):
    box = RoundedRectangle(corner_radius=0.18, width=width, height=height, stroke_color=color,
                           stroke_width=2.5, fill_color=BG, fill_opacity=0.9)
    t = Tex(title, font_size=30, color=color).next_to(box.get_top(), DOWN, buff=0.3)
    b = MathTex(body, font_size=52, color=FG).move_to(box.get_center() + 0.25 * DOWN)
    return VGroup(box, t, b)
