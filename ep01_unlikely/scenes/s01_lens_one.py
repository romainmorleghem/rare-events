"""Seq 1 — Lens 1: the running proportion of heads settles at 1/2; its histogram collapses to a spike."""
from _common import *  # noqa
from manim import *
from common.style import FG, MUTED, HEADS, TAILS, LLN
from common.narrative import Narrated
from _stages import YMAX, prop_axes, spike, n_label, lens_one_badge, axis_cfg, NS


class LensOne(Narrated):
    def construct(self):
        self.chapter(r"1 \,$\cdot$\, Where does the average go?")
        rng = np.random.default_rng(11)
        # --- running proportion, log-scaled number of flips
        ax = Axes(x_range=[0, 4, 1], y_range=[0, 1, 0.25], x_length=10.5, y_length=4.2,
                  axis_config=axis_cfg(), y_axis_config={"include_numbers": True, "font_size": 24,
                                                         "decimal_number_config": {"num_decimal_places": 2}},
                  ).move_to([0.3, 0.55, 0])
        xt = VGroup(*[MathTex(str(10 ** e), font_size=24, color=MUTED).next_to(ax.c2p(e, 0), DOWN, buff=0.2)
                      for e in range(5)])
        xl = Tex("number of flips (log scale)", font_size=28, color=FG).next_to(ax.x_axis, DOWN, buff=0.55)
        yl = Tex("proportion of heads so far", font_size=28, color=FG).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        half = DashedLine(ax.c2p(0, 0.5), ax.c2p(4, 0.5), color=FG, stroke_width=2, dash_length=0.08)
        hl = MathTex(r"\tfrac12", font_size=34, color=FG).next_to(half, RIGHT, buff=0.12)
        self.play(Create(ax), FadeIn(xt), FadeIn(xl), FadeIn(yl), run_time=1.2)
        grid = np.unique(np.round(np.logspace(0, 4, 360)).astype(int))

        def path(seed_flips, color, width, opacity=1.0):
            p = np.cumsum(seed_flips) / np.arange(1, len(seed_flips) + 1)
            m = VMobject().set_points_as_corners([ax.c2p(np.log10(i), p[i - 1]) for i in grid])
            return m.set_stroke(color, width, opacity=opacity)

        first = path(rng.random(10**4) < 0.5, HEADS, 3)
        self.say(r"Flip a coin over and over, and keep track of the proportion of heads so far.",
                 anims=[Create(first, rate_func=linear)], run_time=6, wait=0.5)
        self.say(r"At first it jumps around wildly: after one flip it is either 0 or 1. "
                 r"Then it calms down, and settles near one half.", anims=[Create(half), FadeIn(hl)], run_time=1)
        many = VGroup(*[path(rng.random(10**4) < 0.5, LLN, 1.6, 0.45) for _ in range(60)])
        self.say(r"Here are sixty people doing the same thing. Every path ends up at one half: a funnel.",
                 anims=[Create(many, lag_ratio=0.02, rate_func=linear)], run_time=5, extra=0.5)
        law = Tex(r"\textbf{Law of large numbers:} the average settles on the expected value.",
                  font_size=34, color=LLN).next_to(ax, UP, buff=0.15)
        self.say(r"This is the \emph{law of large numbers}, the first and most famous result of probability "
                 r"(Jacob Bernoulli, 1713).", anims=[FadeOut(yl), FadeIn(law)], run_time=1)
        self.unsay()
        self.play(FadeOut(VGroup(ax, xt, xl, law, half, hl, first, many)), run_time=1)

        # --- the histogram view: lens 1 (the vertical scale zooms out as the spike grows)
        ax, xl = prop_axes(YMAX[10])
        yl = Tex("how likely", font_size=28, color=FG).next_to(ax.y_axis.get_top(), RIGHT, buff=0.2)
        badge = lens_one_badge()
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=1)
        self.say(r"Another way to see it. Flip $n$ coins, and draw how likely each possible proportion is.")
        polys, labels = [], []
        for n in NS:
            if n == 10:
                P = spike(ax, n)
                L = n_label(ax, n, P)
                self.say(r"With $n = 10$ coins, the proportion can be anything from $0$ to $1$, "
                         r"in steps of $0.1$. Five heads is the most likely, but far from certain.",
                         anims=[FadeIn(P, shift=0.2 * UP), FadeIn(L)], run_time=1.2)
            else:
                nax, _ = prop_axes(YMAX[n])
                old = [spike(nax, m).set_fill(opacity=0.22).set_stroke(opacity=0.5) for m in NS if m < n]
                P = spike(nax, n)
                L = n_label(nax, n, P)
                self.say(r"With $n = 100$ coins, the hump gets narrower and taller (we zoom out "
                         r"vertically to keep it on screen)." if n == 100 else
                         r"With $n = 1000$: a narrow spike.", anims=[
                    Transform(ax, nax), *[Transform(a, b) for a, b in zip(polys, old)],
                    FadeIn(P, shift=0.3 * UP), *[FadeOut(l) for l in labels], FadeIn(L)], run_time=1.8)
            polys.append(P); labels.append(L)
        self.say(r"As $n$ grows, everything piles up on one point: one half. That is the law of large "
                 r"numbers again, seen through a first lens.", anims=[FadeIn(badge, shift=0.2 * LEFT)], run_time=1)
        self.say(r"Lens 1 looks at the proportion itself. It tells us \emph{where} the average goes. "
                 r"But a spike hides all the details: how much does the proportion wiggle?", extra=0.4)
        self.unsay()
        self.play(FadeOut(labels[-1]), run_time=0.4)
