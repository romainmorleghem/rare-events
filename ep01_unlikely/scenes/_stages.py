"""Layouts shared between consecutive scenes, so each scene starts on the previous one's last frame."""
from _common import *  # noqa
from manim import Axes, MathTex, Tex, VGroup, UR, DOWN, RIGHT, LEFT, UP
from common.coins import log_binom_pmf, rate
from common.style import FG, MUTED, HEADS, LLN, CLT, LDP

NS = (10, 100, 1000)
NCOL = {10: 0.35, 100: 0.55, 1000: 0.85}       # fill opacity per n (older = fainter)


def axis_cfg(**kw):
    c = {"color": MUTED, "stroke_width": 2, "include_tip": False}
    c.update(kw)
    return c


YMAX = {10: 3, 100: 9, 1000: 28}


def prop_axes(ymax=28):
    """Lens 1: x = proportion of heads, y = probability density (no y numbers: only shapes matter)."""
    ax = Axes(x_range=[0, 1, 0.25], y_range=[0, ymax, ymax / 4], x_length=10, y_length=4.3,
              axis_config=axis_cfg(), x_axis_config={"include_numbers": True, "font_size": 24,
                                                     "decimal_number_config": {"num_decimal_places": 2}},
              ).move_to([0, 0.55, 0])
    xl = Tex("proportion of heads", font_size=28, color=FG).next_to(ax.x_axis, DOWN, buff=0.5)
    return ax, xl


def spike(ax, n):
    k = np.arange(n + 1)
    p = np.exp(log_binom_pmf(n, k))
    edges = np.clip((np.arange(n + 2) - 0.5) / n, 0, 1)      # one bar per possible count k
    return steps(ax, edges, p * n, HEADS, opacity=NCOL[n], stroke=1.5)


def n_label(ax, n, poly):
    return MathTex(r"n=%d" % n, font_size=28, color=HEADS).next_to(poly, UP, buff=0.1)


def lens_one_badge():
    return lens(1, r"the proportion itself", LLN).to_corner(UR, buff=0.4)
