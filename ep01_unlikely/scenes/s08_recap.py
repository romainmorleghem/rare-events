"""Seq 8 — Recap (three lenses, one bowl), a little history, where it is used, end card."""
from _common import *  # noqa
from manim import *
from common.style import FG, MUTED, HEADS, LLN, CLT, LDP, TRUTH
from common.narrative import Narrated
from common.coins import rate
from _stages import axis_cfg


class Recap(Narrated):
    def construct(self):
        self.chapter(r"Recap")
        ax = Axes(x_range=[0, 1, 0.25], y_range=[0, 0.75, 0.25], x_length=10.5, y_length=4.3,
                  axis_config=axis_cfg(), x_axis_config={"include_numbers": True, "font_size": 24,
                                                         "decimal_number_config": {"num_decimal_places": 2}}
                  ).move_to([0.3, 0.55, 0])
        xs = np.linspace(0, 1, 400)
        I = curve(ax, xs, rate(xs), LDP, 5)
        par = curve(ax, xs, 2 * (xs - 0.5)**2, CLT, 3.5)
        b = Dot(ax.c2p(0.5, 0), color=LLN, radius=0.11)
        l1 = lens(1, r"the bottom: where the average goes", LLN, scale=0.8).move_to(ax.c2p(0.47, 0.7))
        l2 = lens(2, r"the curvature at the bottom: the bell curve", CLT, scale=0.8)
        l2.next_to(l1, DOWN, buff=0.15).align_to(l1, LEFT)
        l3 = lens(3, r"the whole bowl: how rare is rare", LDP, scale=0.8)
        l3.next_to(l2, DOWN, buff=0.15).align_to(l1, LEFT)
        self.play(Create(ax), Create(I), run_time=1.5)
        self.say(r"One histogram, three lenses. Lens 1, the law of large numbers: the average goes to the "
                 r"bottom of the bowl.", anims=[FadeIn(b, scale=2), FadeIn(l1)], run_time=1, extra=0.3)
        self.say(r"Lens 2, the central limit theorem: near the bottom, the bowl is a parabola, and the "
                 r"wiggles are bell-shaped.", anims=[Create(par), FadeIn(l2)], run_time=1.2, extra=0.3)
        self.say(r"Lens 3, large deviations: the whole bowl. Rare events are exponentially rare, "
                 r"$P \approx e^{-n I(x)}$, and the bell curve can be wrong by twenty orders of magnitude.",
                 anims=[FadeIn(l3)], run_time=1, extra=0.4)
        self.say(r"Underneath, it is all counting. And when the unlikely happens, it happens in the least unlikely "
                 r"way: a conspiracy of small deviations, unless the randomness is wild.", extra=0.5)
        self.play(FadeOut(VGroup(ax, I, par, b, l1, l2, l3)), run_time=1)

        self.chapter(r"A little history")
        h1 = VGroup(Tex(r"\textbf{Harald Cram\'er}, 1938", font_size=36, color=FG),
                    Tex(r"Swedish mathematician and insurance actuary.\\ How likely is an insurance company to go bankrupt?",
                        font_size=28, color=MUTED)).arrange(DOWN, buff=0.15)
        h2 = VGroup(Tex(r"\textbf{S. R. Srinivasa Varadhan}, from the 1960s", font_size=36, color=FG),
                    Tex(r"turned the idea into a general theory of large deviations.\\ Abel Prize, 2007.",
                        font_size=28, color=MUTED)).arrange(DOWN, buff=0.15)
        VGroup(h1, h2).arrange(DOWN, buff=0.7).move_to([0, 0.8, 0])
        self.say(r"The first large-deviation theorem came from insurance: Harald Cram\'er wanted to know how "
                 r"likely an insurer is to be ruined by an unlucky run of claims.", anims=[FadeIn(h1, shift=0.2 * UP)],
                 run_time=1.2, extra=0.4)
        self.say(r"Decades later, Varadhan built the general theory, for which he received the Abel Prize, "
                 r"the highest award in mathematics alongside the Fields Medal.", anims=[FadeIn(h2, shift=0.2 * UP)],
                 run_time=1.2, extra=0.4)
        self.play(FadeOut(VGroup(h1, h2)), run_time=0.8)

        self.chapter(r"Where it is used")
        items = [(r"Insurance and finance", r"ruin probabilities, extreme losses"),
                 (r"Telecommunications", r"buffer overflows, decoding errors"),
                 (r"Climate", r"simulating heat waves more extreme than any observed"),
                 (r"Chemistry and physics", r"molecules crossing energy barriers, the second law")]
        rows = VGroup()
        for i, (a, b2) in enumerate(items):
            d = Dot(radius=0.09, color=[HEADS, CLT, LLN, LDP][i])
            t = Tex(r"\textbf{%s}: %s" % (a, b2), font_size=32, color=FG)
            rows.add(VGroup(d, t).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to([0, 0.7, 0])
        self.say(r"Today, the same ideas (the bowl, the rigged coin, the least unlikely way) are used wherever "
                 r"rare events matter.", anims=[FadeIn(rows, lag_ratio=0.3)], run_time=2.5, extra=0.8)
        self.unsay()
        self.play(FadeOut(rows), FadeOut(self.chapter_tag), run_time=0.8)
        self.chapter_tag = None

        title = Tex(r"The Mathematics of the Unlikely", font_size=56, color=FG)
        line = Line(LEFT * 4, RIGHT * 4, color=LDP, stroke_width=2)
        web = Tex(r"Play with the coins, the bowl and the rigged coin:\\ "
                  r"\texttt{romainmorleghem.github.io/rare-events}", font_size=30, color=MUTED)
        code = Tex(r"Every number in this video is computed in the companion code.", font_size=26, color=MUTED)
        end = VGroup(title, line, web, code).arrange(DOWN, buff=0.4)
        self.play(Write(title), GrowFromCenter(line), run_time=1.5)
        self.play(FadeIn(web, shift=0.1 * UP), FadeIn(code), run_time=1)
        self.wait(4)
        self.play(FadeOut(end), run_time=1.2)
