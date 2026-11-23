"""Seq 3 — Lens 3: log scale (the dome), the bell's parabola drifts away, divide by n -> the bowl I(x).
Then the unifying picture: bottom point (lens 1), curvature (lens 2), whole bowl (lens 3)."""
from _common import *  # noqa
from manim import *
from common.style import FG, MUTED, HEADS, LLN, CLT, LDP, TRUTH
from common.narrative import Narrated
from common.coins import log_binom_pmf, log_bell_pmf, rate, LN10
from _stages import axis_cfg

N = 1000
K = np.arange(N + 1)
LP = log_binom_pmf(N, K)                       # natural log of P(k heads)
T = FACTS["tails"]


def ylabels(ax, values, fmt, size=24):
    return VGroup(*[MathTex(fmt(v), font_size=size, color=MUTED).next_to(ax.c2p(0, v), LEFT, buff=0.15)
                    for v in values])


class LensThree(Narrated):
    def construct(self):
        self.chapter(r"3 \,$\cdot$\, How rare is rare?")
        # --- A. linear scale: the 700 bar is invisible
        lin = Axes(x_range=[0, 1000, 250], y_range=[0, 0.03, 0.01], x_length=10.5, y_length=4.3,
                   axis_config=axis_cfg(), x_axis_config={"include_numbers": True, "font_size": 24}
                   ).move_to([0.3, 0.55, 0])
        xl = Tex(r"number of heads, out of 1000 coins", font_size=28, color=FG).next_to(lin.x_axis, DOWN, buff=0.5)
        dome_lin = area(lin, K, np.exp(LP), HEADS, opacity=0.6)
        self.play(Create(lin), FadeIn(xl), FadeIn(dome_lin), run_time=1.2)
        d700 = Dot(lin.c2p(700, 0), color=TRUTH, radius=0.07)
        arrow = Arrow(lin.c2p(700, 0.012), lin.c2p(700, 0.0012), color=TRUTH, buff=0, stroke_width=3)
        t700 = Tex(r"700 heads", font_size=28, color=TRUTH).next_to(arrow, UP, buff=0.1)
        self.say(r"The probabilities we care about are hiding here, in the flat part. "
                 r"The bar for exactly 700 heads is not zero\ldots",
                 anims=[GrowArrow(arrow), FadeIn(t700), FadeIn(d700)], run_time=1)
        self.say(r"\ldots but it is $10^{35.7}$ times shorter than the peak. If the peak were 30\,cm tall, "
                 r"that bar would be shorter than the Planck length, the smallest scale in physics.", extra=0.6)
        self.say(r"To see it, we need a different kind of ruler.")

        # --- B. log scale: the dome
        LO = -310
        log = Axes(x_range=[0, 1000, 250], y_range=[0, -LO, 50], x_length=10.5, y_length=4.3,
                   axis_config=axis_cfg(), x_axis_config={"include_numbers": True, "font_size": 24}
                   ).move_to(lin)
        ticks = VGroup(*[MathTex(r"10^{%d}" % v if v else "1", font_size=24, color=MUTED
                                 ).next_to(log.c2p(0, v - LO), LEFT, buff=0.15) for v in (0, -100, -200, -300)])
        badge = lens(3, r"logarithmic ruler", LDP).to_corner(UR, buff=0.4)
        dome = area(log, K, LP / LN10 - LO, HEADS, opacity=0.6, base=0)
        self.play(FadeOut(VGroup(arrow, t700, d700)), run_time=0.4)
        self.say(r"Lens 3 starts with a \emph{logarithmic} ruler: each step down divides the probability by ten.",
                 anims=[FadeIn(badge, shift=0.2 * LEFT)], run_time=1)
        self.say(r"Now every bar is visible. The spike becomes a smooth dome.",
                 anims=[Transform(lin, log), Transform(dome_lin, dome), FadeIn(ticks)], run_time=3, extra=0.3)
        z = Dot(log.c2p(0, LP[0] / LN10 - LO), color=TRUTH, radius=0.07)
        zt = MathTex(r"\text{0 heads: } 2^{-1000} \approx 10^{-301}", font_size=28, color=TRUTH
                     ).next_to(z, RIGHT, buff=0.2).shift(0.3 * UP)
        self.say(r"At the edges: zero heads out of 1000 has probability $2^{-1000}$, a 1 in 300 digits.",
                 anims=[FadeIn(z), FadeIn(zt)], run_time=1)
        self.play(FadeOut(VGroup(z, zt)), run_time=0.4)

        # --- C. the bell curve on this ruler: a parabola
        bell = curve(log, K, log_bell_pmf(N, K) / LN10 - LO, CLT, 3.5)
        self.say(r"And the bell curve? On this ruler, it becomes a parabola.", anims=[Create(bell)], run_time=2)
        self.say(r"Near the middle, the parabola and the dome agree perfectly: that is the central limit theorem "
                 r"at work. But the farther out we go, the more they drift apart.", extra=0.3)
        y_ex, y_be = LP[900] / LN10, log_bell_pmf(N, 900) / LN10
        gap = DoubleArrow(log.c2p(900, y_ex - LO), log.c2p(900, y_be - LO), buff=0, color=CLT, stroke_width=3,
                          tip_length=0.18)
        gt = MathTex(r"\times 10^{%d}" % int(y_be - y_ex), font_size=40, color=CLT
                     ).move_to(log.c2p(965, y_be - LO + 70))
        gp = Line(gt.get_bottom() + 0.05 * DOWN, gap.get_top(), color=CLT, stroke_width=1.5)
        self.say(r"At 900 heads, the parabola sits twenty steps above the dome: twenty factors of ten. "
                 r"That is the error we saw at the very beginning.",
                 anims=[GrowFromCenter(gap), FadeIn(gt), Create(gp)], run_time=1.2, extra=0.4)
        self.play(FadeOut(VGroup(gap, gt, gp, bell)), run_time=0.6)

        # --- D. divide by n: the bowl
        bowl_ax = Axes(x_range=[0, 1, 0.25], y_range=[0, 0.75, 0.25], x_length=10.5, y_length=4.3,
                       axis_config=axis_cfg(), x_axis_config={"include_numbers": True, "font_size": 24,
                                                              "decimal_number_config": {"num_decimal_places": 2}},
                       y_axis_config={"include_numbers": True, "font_size": 24,
                                      "decimal_number_config": {"num_decimal_places": 2}}).move_to(log)
        bxl = Tex(r"proportion of heads, $x$", font_size=28, color=FG).move_to(xl)
        byl = MathTex(r"-\tfrac{1}{n}\ln P", font_size=32, color=FG).next_to(bowl_ax.y_axis.get_top(), RIGHT, buff=0.3)
        badge2 = lens(3, r"log ruler, then divide by $n$", LDP).to_corner(UR, buff=0.4)
        x = K / N
        line1000 = curve(bowl_ax, x, -LP / N, HEADS, 3)
        dome_line = curve(log, K, LP / LN10 - LO, HEADS, 3)
        self.say(r"Final step of the lens: divide by $n$, the number of coins. "
                 r"(And flip the picture over, so that rarer means higher.)", extra=0.2)
        self.add(dome_line)
        self.play(FadeOut(dome_lin), run_time=0.5)
        self.play(Transform(lin, bowl_ax), FadeOut(ticks), FadeTransform(xl, bxl), FadeIn(byl),
                  Transform(dome_line, line1000), FadeTransform(badge, badge2), run_time=3)
        curves = {}
        for n, op in ((10, 0.5), (100, 0.75)):
            kk = np.arange(n + 1)
            yy = -log_binom_pmf(n, kk) / n
            if n == 10:
                curves[n] = VGroup(*[Dot(bowl_ax.c2p(a, b), radius=0.06, color=HEADS).set_opacity(op)
                                     for a, b in zip(kk / n, yy)])
            else:
                curves[n] = curve(bowl_ax, kk / n, yy, HEADS, 2).set_stroke(opacity=op)
        labs = VGroup(MathTex(r"n=10", font_size=26, color=HEADS).set_opacity(0.6),
                      MathTex(r"n=100", font_size=26, color=HEADS).set_opacity(0.8),
                      MathTex(r"n=1000", font_size=26, color=HEADS)).arrange(DOWN, aligned_edge=LEFT, buff=0.12
                                                                             ).move_to(bowl_ax.c2p(0.5, 0.6))
        self.say(r"Do the same with 10 coins, with 100 coins, with 1000 coins\ldots",
                 anims=[FadeIn(curves[10]), Create(curves[100]), FadeIn(labs)], run_time=2)
        I = curve(bowl_ax, np.linspace(0, 1, 400), rate(np.linspace(0, 1, 400)), LDP, 5)
        self.say(r"\ldots and they all pile up on the same curve: a \emph{bowl}. "
                 r"Mathematicians call it the \emph{rate function}, $I(x)$.", anims=[Create(I)], run_time=2,
                 extra=0.4)
        self.play(FadeOut(VGroup(curves[10], curves[100], dome_line, labs)), run_time=0.6)
        formula = MathTex(r"P\big(\text{proportion} \approx x\big) \;\approx\; e^{-\,n\, I(x)}",
                          font_size=46, color=LDP)
        box = SurroundingRectangle(formula, color=LDP, buff=0.22, corner_radius=0.12,
                                   fill_color=BG, fill_opacity=0.92)
        fb = VGroup(box, formula).move_to(bowl_ax.c2p(0.5, 0.55))
        self.say(r"Read the bowl like this. The probability of seeing a proportion $x$ shrinks exponentially "
                 r"with $n$, and the bowl gives the speed:", anims=[FadeIn(fb, shift=0.2 * DOWN)], run_time=1.2,
                 extra=0.3)
        i7 = rate(0.7)
        d7 = Dot(bowl_ax.c2p(0.7, i7), color=TRUTH, radius=0.08)
        v7 = DashedLine(bowl_ax.c2p(0.7, 0), bowl_ax.c2p(0.7, i7), color=TRUTH, stroke_width=2)
        t7 = MathTex(r"I(0.7) = %.3f" % i7, font_size=32, color=TRUTH).move_to(bowl_ax.c2p(0.5, 0.36))
        p7 = DashedLine(t7.get_bottom() + 0.08 * DOWN, d7.get_center(), color=TRUTH, stroke_width=1.5, buff=0.1)
        self.say(r"For 70\%% heads, $I = %.3f$. Each extra coin multiplies the probability by "
                 r"$e^{-%.3f} = 1/%.3f$: you lose about 8\%% per coin." % (i7, i7, np.exp(i7)),
                 anims=[Create(v7), FadeIn(d7), FadeIn(t7), Create(p7)], run_time=1, extra=0.3)
        pw = MathTex(r"1.086^{1000} \approx 10^{%.1f}" % (N * i7 / LN10), font_size=40, color=TRUTH
                     ).move_to(bowl_ax.c2p(0.5, 0.36))
        self.say(r"Harmless for one coin. Crushing for a thousand: the losses compound, like interest.",
                 anims=[FadeOut(VGroup(t7, p7)), Write(pw)], run_time=1.2, extra=0.4)
        self.play(FadeOut(VGroup(fb, d7, v7, pw)), run_time=0.6)

        # --- E. the unifying picture
        self.chapter(r"3 \,$\cdot$\, Three lenses, one bowl")
        b1 = Dot(bowl_ax.c2p(0.5, 0), color=LLN, radius=0.11)
        l1 = lens(1, r"the bottom: where the average goes", LLN, scale=0.8).move_to(bowl_ax.c2p(0.47, 0.7))
        a1 = Arrow(l1.get_bottom() + 0.1 * DOWN, b1.get_top(), buff=0.1, color=LLN, stroke_width=3)
        self.say(r"Now the three lenses fit together. The bowl touches zero at only one point, $x = 1/2$. "
                 r"Everywhere else, probabilities vanish as $n$ grows.", anims=[FadeIn(b1, scale=2)], run_time=1)
        self.say(r"So the average must end up at the bottom of the bowl: that is lens 1, the law of large numbers.",
                 anims=[FadeIn(l1), GrowArrow(a1)], run_time=1, extra=0.3)
        par = curve(bowl_ax, np.linspace(0, 1, 200), 2 * (np.linspace(0, 1, 200) - 0.5)**2, CLT, 3.5)
        l2 = lens(2, r"the curvature at the bottom: the bell curve", CLT, scale=0.8)
        l2.next_to(l1, DOWN, buff=0.15).align_to(l1, LEFT)
        self.say(r"Zoom on the bottom. Any smooth bowl looks like a parabola there, and that parabola "
                 r"\emph{is} the bell curve on a log ruler. Lens 2 only sees the bottom of the bowl.",
                 anims=[FadeOut(a1), FadeIn(l2), Create(par)], run_time=1.5, extra=0.3)
        l3 = lens(3, r"the whole bowl: how rare is rare", LDP, scale=0.8)
        l3.next_to(l2, DOWN, buff=0.15).align_to(l1, LEFT)
        g = DoubleArrow(bowl_ax.c2p(0.9, 2 * 0.4**2), bowl_ax.c2p(0.9, rate(0.9)), buff=0, color=CLT,
                        stroke_width=3, tip_length=0.15)
        gt = MathTex(r"%.3f\ \text{per coin}" % (rate(0.9) - 0.32), font_size=28, color=CLT
                     ).next_to(g, LEFT, buff=0.15)
        self.say(r"Lens 3 sees the whole bowl. Far from the bottom, the bowl bends away from the parabola.",
                 anims=[FadeIn(l3)], run_time=1.2)
        self.say(r"At 90\%% heads the gap is only $%.3f$ per coin. But over 1000 coins it compounds: "
                 r"$e^{1000 \times %.3f} \approx 10^{21}$. The twenty zeros again." % (rate(0.9) - 0.32,
                                                                                       rate(0.9) - 0.32),
                 anims=[GrowFromCenter(g), FadeIn(gt)], run_time=1.2, extra=0.5)
        self.say(r"So the bell curve is not wrong. It is the bottom of the bowl. "
                 r"The mistake is to use it for rare events, far from the bottom.", extra=0.6)
        self.unsay()
        self.play(FadeOut(VGroup(g, gt, par, l1, l2, l3, b1, I, lin, bxl, byl, badge2)), run_time=1)
