"""Seq 2 — Lens 2: zoom by sqrt(n) -> one bell curve (coins, then dice). Typical wiggle; 700 is 12.6 sd away."""
from _common import *  # noqa
from manim import *
from common.style import FG, MUTED, HEADS, LLN, CLT
from common.narrative import Narrated
from common.coins import log_binom_pmf
from _stages import YMAX, prop_axes, spike, n_label, lens_one_badge, axis_cfg, NS, NCOL

TY = FACTS["typical"]


def zoomed(ax, n, opacity):
    """Histogram of sqrt(n) (proportion - 1/2), area 1."""
    k = np.arange(n + 1)
    p = np.exp(log_binom_pmf(n, k))
    r = np.sqrt(n)
    edges = (np.arange(n + 2) - 0.5) / n
    e = np.clip(r * (edges - 0.5), -1.75, 1.75)
    return steps(ax, e, p * n / r, HEADS, opacity=opacity, stroke=1.5)


def bell(ax, sd, color=CLT, lo=None, hi=None, width=3.5):
    lo = -ax.x_range[1] if lo is None else lo
    hi = ax.x_range[1] if hi is None else hi
    x = np.linspace(lo, hi, 300)
    return curve(ax, x, np.exp(-x**2 / (2 * sd**2)) / (sd * np.sqrt(2 * np.pi)), color, width)


def dice_hist(ax, n):
    """Distribution of the average of n dice, centred and multiplied by sqrt(n)."""
    p = np.ones(1)
    for _ in range(n):
        p = np.convolve(p, np.ones(6) / 6)
    s = np.arange(n, 6 * n + 1)                # possible sums
    r = np.sqrt(n)
    c = (s - 3.5 * n) / r                      # = sqrt(n) (average - 3.5)
    w = 1 / r
    edges = np.concatenate([c - w / 2, [c[-1] + w / 2]])
    return steps(ax, edges, p / w, HEADS, opacity=0.6, stroke=1.5)


class LensTwo(Narrated):
    def construct(self):
        # --- start exactly on the last frame of s01
        self.chapter(r"1 \,$\cdot$\, Where does the average go?", animate=False)
        ax, xl = prop_axes(YMAX[1000])
        yl = Tex("how likely", font_size=28, color=FG).next_to(ax.y_axis.get_top(), RIGHT, buff=0.2)
        polys = [spike(ax, n) for n in NS]
        for p in polys[:-1]:
            p.set_fill(opacity=0.22).set_stroke(opacity=0.5)
        badge1 = lens_one_badge()
        self.add(ax, xl, yl, *polys, badge1)
        self.yl = yl
        self.chapter(r"2 \,$\cdot$\, How much does it wiggle?")

        # --- lens 2: zoom by sqrt(n)
        zax = Axes(x_range=[-1.75, 1.75, 0.5], y_range=[0, 0.9, 0.3], x_length=10, y_length=4.3,
                   axis_config=axis_cfg()).move_to(ax)
        zax.y_axis.set_opacity(0)
        zxl = MathTex(r"\sqrt{n}\,\big(\text{proportion} - \tfrac12\big)", font_size=32, color=FG
                      ).next_to(zax.x_axis, DOWN, buff=0.4)
        zero = MathTex("0", font_size=26, color=MUTED).next_to(zax.c2p(0, 0), DOWN, buff=0.15)
        badge2 = lens(2, r"zoom in by $\sqrt{n}$", CLT).to_corner(UR, buff=0.4)
        self.say(r"Lens 2: zoom in on the middle. The spike for $n$ coins has a width of about "
                 r"$1/\sqrt{n}$, so we stretch it horizontally by $\sqrt{n}$.")
        zs = [zoomed(zax, n, NCOL[n]) for n in NS]
        self.say(r"(And squash it vertically by the same factor, so the total stays the same.)",
                 anims=[Transform(ax, zax), FadeTransform(xl, zxl), FadeIn(zero), FadeOut(yl),
                        *[Transform(a, b) for a, b in zip(polys, zs)], FadeTransform(badge1, badge2)],
                 run_time=3)
        b = bell(zax, 0.5)
        self.say(r"Surprise: after zooming, the three histograms have the same shape. "
                 r"As $n$ grows, they hug one smooth curve\ldots", extra=0.3)
        self.say(r"\ldots the famous \emph{bell curve}, or Gaussian.", anims=[Create(b)], run_time=1.5)
        clt = Tex(r"\textbf{Central limit theorem:} zoomed by $\sqrt{n}$, wiggles are bell-shaped.",
                  font_size=30, color=CLT).move_to([-1.6, 3.0, 0])
        self.say(r"This is the \emph{central limit theorem}. Its magic is that it does not care about the coin.",
                 anims=[FadeIn(clt)], run_time=1)
        self.play(FadeOut(VGroup(*polys, b, zero)), run_time=0.8)

        # --- universality: dice
        dax = Axes(x_range=[-4.5, 4.5, 1], y_range=[0, 0.3, 0.1], x_length=10, y_length=4.3,
                   axis_config=axis_cfg()).move_to(zax)
        dax.y_axis.set_opacity(0)
        dxl = MathTex(r"\sqrt{n}\,\big(\text{average of } n \text{ dice} - 3.5\big)", font_size=32, color=FG
                      ).move_to(zxl)
        db = bell(dax, np.sqrt(35 / 12))
        h = dice_hist(dax, 1)
        lab = MathTex(r"n = 1", font_size=34, color=HEADS).move_to(dax.c2p(3.2, 0.25))
        self.play(Transform(ax, dax), FadeTransform(zxl, dxl), run_time=1)
        self.say(r"Roll dice instead. One die: all six faces are equally likely, a flat histogram.",
                 anims=[FadeIn(h, shift=0.2 * UP), FadeIn(lab)], run_time=1)
        for n in (2, 3, 10):
            self.say({2: r"The average of two dice: a triangle.",
                      3: r"Three dice: the corners are already rounding off.",
                      10: r"Ten dice: the same bell curve, once again."}[n],
                     anims=[Transform(h, dice_hist(dax, n)),
                            Transform(lab, MathTex(r"n = %d" % n, font_size=34, color=HEADS).move_to(lab))],
                     run_time=1.5)
            if n == 3:
                self.play(Create(db), run_time=1)
        self.say(r"Heights, measurement errors, exam scores: anything made of many small independent "
                 r"pieces ends up bell-shaped. That is why the bell curve is everywhere.", extra=0.3)
        self.play(FadeOut(VGroup(h, lab, db, clt)), run_time=0.8)

        # --- back to 1000 coins, counted in heads
        hax = Axes(x_range=[400, 600, 50], y_range=[0, 0.03, 0.01], x_length=10, y_length=4.3,
                   axis_config=axis_cfg(), x_axis_config={"include_numbers": True, "font_size": 24}
                   ).move_to(zax)
        hxl = Tex(r"number of heads, out of 1000 coins", font_size=30, color=FG).move_to(dxl)
        k = np.arange(400, 751)                      # same points as the 400-750 view, clipped at 600
        pk = np.exp(log_binom_pmf(1000, k))
        hh = steps(hax, np.clip(np.append(k - 0.5, 750.5), 400, 600), pk, HEADS, opacity=0.6, stroke=1.2)
        sd = TY["sd"]
        xs = np.linspace(400, 750, 500)
        gauss = np.exp(-(xs - 500)**2 / (2 * sd**2)) / (sd * np.sqrt(2 * np.pi))
        hb = curve(hax, np.clip(xs, 400, 600), gauss, CLT, 3)
        self.play(Transform(ax, hax), FadeTransform(dxl, hxl), run_time=1)
        self.say(r"Back to our 1000 coins, now counting heads.", anims=[FadeIn(hh), Create(hb)], run_time=1.5)
        lo, hi = TY["lo95"], TY["hi95"]
        band = hax.get_area(hax.plot(lambda x: np.exp(-(x - 500)**2 / (2 * sd**2)) / (sd * np.sqrt(2 * np.pi)),
                                     x_range=[lo, hi]), x_range=[lo, hi], color=CLT, opacity=0.35)
        br = BraceBetweenPoints(hax.c2p(lo, 0), hax.c2p(hi, 0), DOWN, color=CLT).shift(0.45 * DOWN)
        bt = MathTex(r"%d \text{ to } %d" % (lo, hi), font_size=30, color=CLT).next_to(br, DOWN, buff=0.08)
        self.play(FadeOut(hxl), run_time=0.3)
        self.say(r"The typical wiggle (the \emph{standard deviation}) is about $\pm 16$ heads. "
                 r"95\%% of the time, you get between %d and %d heads." % (lo, hi),
                 anims=[FadeIn(band), GrowFromCenter(br), FadeIn(bt)], run_time=1.5, extra=0.5)
        self.play(FadeOut(VGroup(band, br, bt)), run_time=0.6)

        # --- now look out to 700
        wax = Axes(x_range=[400, 750, 50], y_range=[0, 0.03, 0.01], x_length=10, y_length=4.3,
                   axis_config=axis_cfg(), x_axis_config={"include_numbers": True, "font_size": 24}
                   ).move_to(zax)
        hh2 = steps(wax, np.append(k - 0.5, 750.5), pk, HEADS, opacity=0.6, stroke=1.2)
        hb2 = curve(wax, xs, gauss, CLT, 3)
        self.say(r"But our question was about 700 heads. Let us look that far.",
                 anims=[Transform(ax, wax), Transform(hh, hh2), Transform(hb, hb2)], run_time=2)
        m700 = DashedLine(wax.c2p(700, 0), wax.c2p(700, 0.027), color=FG, stroke_width=2.5)
        t700 = Tex(r"700", font_size=30, color=FG).next_to(m700, UP, buff=0.1)
        arr = DoubleArrow(wax.c2p(500, 0.022), wax.c2p(700, 0.022), color=CLT, buff=0, stroke_width=3,
                          tip_length=0.2)
        at = Tex(r"%.1f standard deviations" % TY["sigmas_700"], font_size=30, color=CLT).next_to(arr, UP, buff=0.1)
        self.say(r"700 is 200 heads away from 500: more than twelve typical wiggles.",
                 anims=[Create(m700), FadeIn(t700), GrowFromCenter(arr), FadeIn(at)], run_time=1.5)
        self.say(r"Out there, both curves are flat zero on screen. The central limit theorem describes "
                 r"\emph{typical} fluctuations. Does the bell shape still hold that far out? Nothing promises it.",
                 extra=0.5)
        self.say(r"We need a lens that can see probabilities like $10^{-37}$.", extra=0.3)
        self.unsay()
        self.play(FadeOut(VGroup(arr, at, m700, t700, hh, hb, ax, badge2)), run_time=1)
