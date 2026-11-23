"""Seq 6 — How does the unlikely happen? 700 heads: a streak (A) or a bias everywhere (B)? B, by far.
Then ordinary vs wild amounts forced to a large total: conspiracy vs a single culprit."""
from _common import *  # noqa
from manim import *
from scipy.special import gammaln
from common.style import FG, MUTED, HEADS, TAILS, RIGGED, TRUTH, LDP, CLT, LLN
from common.narrative import Narrated
from _stages import axis_cfg

CS = FACTS["conspiracy"]
TK = FACTS["tails_kind"]
COLS, ROWS, STEP = 50, 20, 0.118


def block_bars(states, origin, color, length=1.6, h=0.2):
    """Ten horizontal bars: proportion of heads in each block of 100 coins (two grid rows)."""
    g = VGroup()
    for b in range(10):
        p = states[100 * b:100 * (b + 1)].mean()
        y = origin[1] - (2 * b + 0.5) * STEP
        g.add(Rectangle(width=max(0.01, p * length), height=h, stroke_width=0, fill_color=color, fill_opacity=0.85)
              .move_to([origin[0] + p * length / 2, y, 0]))
    return g


def bar_chart(ax, values, color, cap=None):
    g = VGroup()
    for i, v in enumerate(values):
        top = min(v, cap) if cap else v
        r = Rectangle(width=ax.x_axis.unit_size * 0.78, height=max(1e-3, ax.y_axis.unit_size * top),
                      stroke_width=0, fill_color=color, fill_opacity=0.85)
        r.move_to(ax.c2p(i + 0.5, 0), aligned_edge=DOWN)
        g.add(r)
    return g


class HowItHappens(Narrated):
    def construct(self):
        self.chapter(r"6 \,$\cdot$\, How does the unlikely happen?")
        rng = np.random.default_rng(3)
        # story A: a streak of 400 heads in rows 6..13, 300 heads scattered among the other 600 coins
        A = np.zeros(1000, bool)
        A[300:700] = True
        rest = np.r_[0:300, 700:1000]
        A[rng.choice(rest, 300, replace=False)] = True
        B = np.zeros(1000, bool)
        B[rng.choice(1000, 700, replace=False)] = True
        gA = coin_grid(COLS, ROWS, STEP, 0.045, center=(-0.6, 1.7, 0), states=A)
        gB = coin_grid(COLS, ROWS, STEP, 0.045, center=(-0.6, -1.0, 0), states=B)
        lA = Tex(r"Story A", font_size=34, color=FG).next_to(gA, LEFT, buff=0.35).shift(0.2 * UP)
        sA = Tex(r"a miracle streak", font_size=26, color=MUTED).next_to(lA, DOWN, buff=0.1).align_to(lA, RIGHT)
        lB = Tex(r"Story B", font_size=34, color=FG).next_to(gB, LEFT, buff=0.35).shift(0.2 * UP)
        sB = Tex(r"a bias everywhere", font_size=26, color=MUTED).next_to(lB, DOWN, buff=0.1).align_to(lB, RIGHT)
        colA = [d.get_color() for d in gA]
        colB = [d.get_color() for d in gB]
        for d in [*gA, *gB]:
            d.set_color(MUTED)
        self.say(r"Suppose it really happened: 700 heads out of 1000. What did the sequence look like?",
                 anims=[FadeIn(gA), FadeIn(gB)], run_time=1, extra=0.3)
        self.say(r"Story A: a normal-looking run, with a miraculous streak of 400 heads in a row.",
                 anims=[LaggedStart(*[d.animate.set_color(c) for d, c in zip(gA, colA)], lag_ratio=0.002),
                        FadeIn(lA), FadeIn(sA)], run_time=2)
        self.say(r"Story B: no streak at all, just a few more heads than usual, everywhere.",
                 anims=[LaggedStart(*[d.animate.set_color(c) for d, c in zip(gB, colB)], lag_ratio=0.002),
                        FadeIn(lB), FadeIn(sB)], run_time=2)
        lc = lambda n, k: (gammaln(n + 1) - gammaln(k + 1) - gammaln(n - k + 1)) / np.log(10)
        ratio = lc(1000, 700) - np.log10(601) - lc(600, 300)
        self.say(r"Both contain exactly 700 heads. But count the sequences: those like B outnumber those with a "
                 r"400-head streak by a factor of more than $10^{%d}$." % (10 * int(ratio // 10)), extra=0.4)
        oA = gA.get_right() + 0.4 * RIGHT + 0.5 * gA.height * UP
        oB = gB.get_right() + 0.4 * RIGHT + 0.5 * gB.height * UP
        bA = block_bars(A, oA, MUTED)
        bB = block_bars(B, oB, RIGGED)
        refA = DashedLine(oA + 0.7 * 1.6 * RIGHT, oA + 0.7 * 1.6 * RIGHT + gA.height * DOWN, color=FG, stroke_width=1.5)
        refB = DashedLine(oB + 0.7 * 1.6 * RIGHT, oB + 0.7 * 1.6 * RIGHT + gB.height * DOWN, color=FG, stroke_width=1.5)
        tl = MathTex(r"70\%", font_size=24, color=FG).next_to(refA, UP, buff=0.08)
        bt = Tex(r"heads per block of 100", font_size=22, color=MUTED).next_to(tl, UP, buff=0.06)
        self.say(r"Measure the proportion of heads in each block of 100 coins. Story A: some blocks at 50\%, "
                 r"some at 100\%. Story B: every block close to 70\%.",
                 anims=[FadeIn(bA, lag_ratio=0.1), FadeIn(bB, lag_ratio=0.1), Create(refA), Create(refB),
                        FadeIn(tl), FadeIn(bt)], run_time=2, extra=0.4)
        self.say(r"Real samples with 700 heads all look like B: every block of 100 between about %d\%% and %d\%% heads, "
                 r"and the longest streak typically only %d heads long."
                 % (round(100 * CS["window100_min_mean"]), round(100 * CS["window100_max_mean"]),
                    round(CS["longest_run_mean"])), extra=0.4)
        self.play(FadeOut(VGroup(gA, lA, sA, bA, refA, tl, bt)), VGroup(gB, lB, sB, bB, refB).animate.shift(2.7 * UP),
                  run_time=1.2)
        principle = Tex(r"When the unlikely happens,\\ it happens in the least unlikely way.", font_size=44,
                        color=LDP)
        pbox = SurroundingRectangle(principle, color=LDP, buff=0.3, corner_radius=0.15)
        P = VGroup(pbox, principle).move_to([0, -1.1, 0])
        self.say(r"This is a general principle of large deviations:", anims=[FadeIn(P, shift=0.2 * UP)], run_time=1.2,
                 extra=0.6)
        self.say(r"Here, the least unlikely way: every coin behaves as if rigged to 70\%. "
                 r"The rigged coin of chapter 5 was not just a trick: it is what actually happens.", extra=0.6)
        self.play(FadeOut(VGroup(gB, lB, sB, bB, refB, P)), run_time=1)

        # --- ordinary vs wild
        self.chapter(r"6 \,$\cdot$\, Conspiracy or culprit?")
        axL = Axes(x_range=[0, 100, 100], y_range=[0, 12, 4], x_length=5.8, y_length=3.5,
                   axis_config=axis_cfg(), y_axis_config={"include_numbers": True, "font_size": 22}
                   ).move_to([-3.45, 0.2, 0])
        axR = axL.copy().move_to([3.55, 0.2, 0])
        tL = Tex(r"\textbf{Ordinary} amounts", font_size=32, color=TAILS).next_to(axL, UP, buff=0.5)
        eL = Tex(r"(like the cost of car accidents)", font_size=24, color=MUTED).next_to(tL, DOWN, buff=0.08)
        tR = Tex(r"\textbf{Wild} amounts", font_size=32, color=CLT).next_to(axR, UP, buff=0.5)
        eR = Tex(r"(like the damage of storms or earthquakes)", font_size=24, color=MUTED).next_to(tR, DOWN, buff=0.08)
        r2 = np.random.default_rng(14)
        free_L = r2.exponential(1.0, 100)
        free_R = (r2.pareto(TK["alpha"], 100) + 1) * TK["xm"]
        bL = bar_chart(axL, free_L, TAILS)
        bR = bar_chart(axR, free_R, CLT)
        self.say(r"Not all randomness behaves like coins. Here are two kinds of random amounts, 100 of each. "
                 r"Both average exactly 1.",
                 anims=[Create(axL), Create(axR), FadeIn(tL), FadeIn(eL), FadeIn(tR), FadeIn(eR),
                        FadeIn(bL, lag_ratio=0.01), FadeIn(bR, lag_ratio=0.01)], run_time=2, extra=0.3)
        self.say(r"Ordinary amounts never stray very far. Wild amounts are usually small, but every now and then "
                 r"one is enormous.", extra=0.3)
        self.say(r"Now force a rare event: the 100 amounts add up to 200 instead of the usual 100. "
                 r"How does that happen?", extra=0.3)
        L, R = np.array(CLAIMS["light"]), np.array(CLAIMS["heavy"])
        R = np.roll(R, 62 - int(np.argmax(R)))      # the amounts are i.i.d.: put the big one mid-panel
        cL = bar_chart(axL, L, TAILS)
        cR = bar_chart(axR, R, CLT, cap=11.6)
        one = DashedLine(axL.c2p(0, 1), axL.c2p(100, 1), color=FG, stroke_width=1.5)
        two = DashedLine(axL.c2p(0, 2), axL.c2p(100, 2), color=TAILS, stroke_width=2)
        self.say(r"Ordinary: every amount is a bit bigger, about twice the usual. A \emph{conspiracy}, just like "
                 r"the coins.", anims=[Transform(bL, cL), Create(two)], run_time=2, extra=0.3)
        big = int(np.argmax(R))
        top = axR.c2p(big + 0.5, 11.6)
        zig = VMobject(stroke_color=FG, stroke_width=3).set_points_as_corners(
            [top + 0.22 * LEFT, top + 0.1 * LEFT + 0.08 * UP, top + 0.1 * RIGHT + 0.08 * DOWN, top + 0.22 * RIGHT])
        bigl = MathTex(r"%d" % round(R.max()), font_size=34, color=CLT).next_to(top, RIGHT, buff=0.35)
        self.say(r"Wild: one single gigantic amount, here %d, while the 99 others look perfectly normal. "
                 r"A single \emph{culprit}." % round(R.max()),
                 anims=[Transform(bR, cR), FadeIn(zig), FadeIn(bigl, shift=0.2 * UP)], run_time=2, extra=0.4)
        pl = MathTex(r"P \approx %s" % sci(TK["light"]["prob_log10"]), font_size=34, color=TAILS
                     ).next_to(axL, DOWN, buff=0.35)
        pr = MathTex(r"P \approx %s" % sci(np.log10(TK["heavy"]["prob"])), font_size=34, color=CLT
                     ).next_to(axR, DOWN, buff=0.35)
        self.say(r"And the odds are worlds apart. For ordinary amounts, a doubled total is a large deviation, "
                 r"exponentially rare. For wild ones, it happens 3 times in 10\,000.",
                 anims=[FadeIn(pl), FadeIn(pr)], run_time=1.2, extra=0.5)
        self.say(r"With wild randomness, one big jump is enough: there is no bowl to climb. "
                 r"Insurers treat earthquakes and car accidents very differently.", extra=0.6)
        self.unsay()
        self.play(FadeOut(VGroup(axL, axR, tL, eL, tR, eR, bL, bR, two, zig, bigl, pl, pr)), run_time=1)
