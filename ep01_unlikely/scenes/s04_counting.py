"""Seq 4 — Where does the bowl come from? Counting sequences: 1-4-6-4-1, digits of the counts for
1000 coins, the entropy dome H(x), and the bowl as missing entropy I(x) = ln 2 - H(x)."""
from _common import *  # noqa
from manim import *
from itertools import product
from common.style import FG, MUTED, HEADS, TAILS, LDP, TRUTH
from common.narrative import Narrated
from common.coins import rate, entropy
from scipy.special import gammaln
from _stages import axis_cfg

C = FACTS["counts_log10"]


def seq_mob(bits, r=0.11, gap=0.29):
    g = VGroup(*[Dot(radius=r, color=HEADS if b else TAILS) for b in bits]).arrange(RIGHT, buff=gap - 2 * r)
    return g


class Counting(Narrated):
    def construct(self):
        self.chapter(r"4 \,$\cdot$\, Where does the bowl come from?")
        seqs = list(product([1, 0], repeat=4))
        mobs = VGroup(*[seq_mob(s) for s in seqs])
        mobs.arrange_in_grid(rows=4, cols=4, buff=(0.7, 0.35)).move_to([0, 0.6, 0])
        self.say(r"Back to basics, with only 4 coins. There are $2\times2\times2\times2 = 16$ possible sequences, "
                 r"and all of them are equally likely.", anims=[FadeIn(mobs, lag_ratio=0.05)], run_time=2)
        # sort into columns by number of heads
        targets, slots = [], {k: 0 for k in range(5)}
        for s in seqs:
            k = sum(s)
            targets.append(np.array([(k - 2) * 2.45, -1.55 + 0.42 * slots[k], 0]))
            slots[k] += 1
        heads_lab = VGroup(*[Tex(r"%d heads" % k if k != 1 else "1 head", font_size=28, color=FG)
                             .move_to([(k - 2) * 2.45, -2.1, 0]) for k in range(5)])
        counts = VGroup(*[MathTex(str(slots[k]), font_size=44, color=HEADS)
                          .move_to([(k - 2) * 2.45, -1.55 + 0.42 * slots[k] + 0.25, 0]) for k in range(5)])
        self.say(r"Sort them by their number of heads.",
                 anims=[m.animate.move_to(t) for m, t in zip(mobs, targets)] + [FadeIn(heads_lab)], run_time=2.5)
        self.say(r"1, 4, 6, 4, 1. Two heads is the most likely result simply because there are more ways to "
                 r"get it: 6 out of 16.", anims=[FadeIn(counts, shift=0.2 * UP, lag_ratio=0.2)], run_time=1.5,
                 extra=0.3)
        self.say(r"That is all probability is, for fair coins: the number of ways, divided by the total number "
                 r"of sequences.", extra=0.3)
        self.play(FadeOut(VGroup(mobs, heads_lab, counts)), run_time=0.8)

        # --- 1000 coins: digits
        rows = [(r"all sequences", C["total"], FG), (r"exactly 500 heads", C["500"], HEADS),
                (r"exactly 700 heads", C["700"], HEADS), (r"exactly 900 heads", C["900"], HEADS)]
        x0, scale = -2.6, 8.6 / 302
        bars, labs, nums = VGroup(), VGroup(), VGroup()
        for i, (lab, l10, col) in enumerate(rows):
            y = 2.0 - 1.05 * i
            digits = int(np.floor(l10)) + 1
            bar = Rectangle(width=digits * scale, height=0.5, stroke_width=0, fill_color=col,
                            fill_opacity=0.75 if i else 0.35)
            bar.move_to([x0 + bar.width / 2, y, 0])
            labs.add(Tex(lab, font_size=30, color=FG).next_to([x0, y, 0], LEFT, buff=0.3))
            nums.add(Tex(r"%d digits" % digits, font_size=28, color=col if i else FG).move_to(bar).align_to(bar, RIGHT)
                     .shift(0.15 * LEFT))
            bars.add(bar)
        nums[0].set_color(BG)
        for nm in nums[1:]:
            nm.set_color(BG)
        title = Tex(r"1000 coins: how many sequences?", font_size=34, color=MUTED).move_to([0, 3.0, 0])
        self.say(r"Now 1000 coins. The numbers of sequences are so big that we only show how many digits they have.",
                 anims=[FadeIn(title), FadeIn(labs[0]), GrowFromEdge(bars[0], LEFT), FadeIn(nums[0])], run_time=1.5)
        self.say(r"Exactly 500 heads: a number with 300 digits. Most sequences are like that.",
                 anims=[FadeIn(labs[1]), GrowFromEdge(bars[1], LEFT), FadeIn(nums[1])], run_time=1.2)
        self.say(r"Exactly 700 heads: still a number with 264 digits. Astronomically many sequences!",
                 anims=[FadeIn(labs[2]), GrowFromEdge(bars[2], LEFT), FadeIn(nums[2])], run_time=1.2)
        self.say(r"But 36 digits fewer: $10^{36}$ times fewer ways than 500 heads. That ratio is exactly the "
                 r"$10^{35.7}$ we saw between the bars.", extra=0.3)
        self.say(r"Exactly 900 heads: only 140 digits.",
                 anims=[FadeIn(labs[3]), GrowFromEdge(bars[3], LEFT), FadeIn(nums[3])], run_time=1.2)
        self.say(r"Rare outcomes are not forbidden by anything. They are rare because there are so few ways to "
                 r"produce them.", extra=0.5)
        self.play(FadeOut(VGroup(bars, labs, nums, title)), run_time=0.8)

        # --- the entropy dome and the bowl as missing entropy
        ax = Axes(x_range=[0, 1, 0.25], y_range=[0, 0.75, 0.25], x_length=10.5, y_length=4.3,
                  axis_config=axis_cfg(), x_axis_config={"include_numbers": True, "font_size": 24,
                                                         "decimal_number_config": {"num_decimal_places": 2}},
                  y_axis_config={"include_numbers": True, "font_size": 24,
                                 "decimal_number_config": {"num_decimal_places": 2}}).move_to([0.3, 0.55, 0])
        xl = Tex(r"proportion of heads, $x$", font_size=28, color=FG).next_to(ax.x_axis, DOWN, buff=0.5)
        yl = MathTex(r"\tfrac{1}{n}\ln(\text{number of ways})", font_size=30, color=FG
                     ).next_to(ax.y_axis.get_top(), RIGHT, buff=0.3)
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=1)
        dots = {}
        for n, op in ((10, 0.45), (100, 0.7)):
            k = np.arange(n + 1)
            lw = (gammaln(n + 1) - gammaln(k + 1) - gammaln(n - k + 1)) / n
            dots[n] = (VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=TRUTH).set_opacity(op) for a, b in zip(k / n, lw)])
                       if n == 10 else curve(ax, k / n, lw, TRUTH, 2).set_stroke(opacity=op))
        xs = np.linspace(0, 1, 400)
        H = curve(ax, xs, entropy(xs), TRUTH, 4.5)
        self.say(r"Same trick as before: take the logarithm of the number of ways, and divide by $n$. "
                 r"For 10 coins, for 100 coins\ldots", anims=[FadeIn(dots[10]), Create(dots[100])], run_time=2)
        Hl = MathTex(r"H(x)", font_size=36, color=TRUTH).move_to(ax.c2p(0.5, 0.6))
        self.say(r"\ldots it settles on a dome, $H(x)$: the \emph{entropy}. The number of ways to get a proportion "
                 r"$x$ is about $e^{\,n H(x)}$.", anims=[Create(H), FadeIn(Hl), FadeOut(dots[10]), FadeOut(dots[100])],
                 run_time=2, extra=0.3)
        top = DashedLine(ax.c2p(0, np.log(2)), ax.c2p(1, np.log(2)), color=FG, stroke_width=2)
        tl = MathTex(r"\ln 2:\ \text{all } 2^n \text{ sequences}", font_size=28, color=FG
                     ).next_to(ax.c2p(1, np.log(2)), UP, buff=0.12).align_to(ax.c2p(1, 0), RIGHT)
        self.say(r"The total number of sequences is $2^n = e^{\,n \ln 2}$: the dome touches that level only at "
                 r"$x = 1/2$.", anims=[Create(top), FadeIn(tl)], run_time=1.2)
        gap_area = VMobject()
        gap_area.set_points_as_corners([ax.c2p(x, np.log(2)) for x in xs] +
                                       [ax.c2p(x, entropy(x)) for x in xs[::-1]])
        gap_area.set_fill(LDP, 0.4).set_stroke(width=0)
        self.say(r"The probability is the ratio: $e^{\,n H(x)} / e^{\,n\ln 2} = e^{-n\,(\ln 2 - H(x))}$. "
                 r"So the bowl is the \emph{gap} between the two.", anims=[FadeIn(gap_area)], run_time=1.5, extra=0.3)
        I = curve(ax, xs, rate(xs), LDP, 5)
        fl = MathTex(r"I(x) = \ln 2 - H(x)", font_size=40, color=LDP).move_to(ax.c2p(0.5, 0.42))
        self.say(r"Flip the gap over, and here is our bowl.",
                 anims=[ReplacementTransform(gap_area, I), FadeOut(Hl)], run_time=2.5)
        self.play(Write(fl), run_time=1)
        self.say(r"The rate function measures how many ways you lose, per coin, when you insist on an unusual "
                 r"outcome. Large deviations is, at heart, a theory of counting.", extra=0.6)
        self.unsay()
        self.play(FadeOut(VGroup(ax, xl, yl, H, top, tl, I, fl)), run_time=1)
