"""Seq 0 — Cold open: 1000 coins, always ~500 heads. The bell curve fails on 700 and 900 heads."""
from _common import *  # noqa
from manim import *
from common.style import FG, MUTED, HEADS, TAILS, CLT, TRUTH, LDP
from common.narrative import Narrated

T = FACTS["tails"]
COLS, ROWS = 40, 25


def flip_wave(scene, grid, states, counter, run_time=1.6):
    cols = COLS
    col_of = np.arange(len(grid)) % cols
    cum = np.array([states[col_of < c].sum() for c in range(cols + 1)])

    def upd(g, a):
        c = int(round(a * cols))
        for i in np.nonzero(col_of < c)[0]:
            g[i].set_color(HEADS if states[i] else TAILS)
        counter.set_value(cum[c])
    for d in grid:
        d.set_color(MUTED)
    scene.play(UpdateFromAlphaFunc(grid, upd), run_time=run_time, rate_func=linear)


class ColdOpen(Narrated):
    def construct(self):
        rng = np.random.default_rng(7)
        grid = coin_grid(COLS, ROWS, step=0.19, radius=0.07, center=(-1.3, 0.45, 0))
        legend = VGroup(Dot(color=HEADS, radius=0.09), Tex("heads", font_size=28, color=FG),
                        Dot(color=TAILS, radius=0.09), Tex("tails", font_size=28, color=FG)
                        ).arrange(RIGHT, buff=0.15).next_to(grid, UP, buff=0.25)
        legend[2].shift(0.3 * RIGHT); legend[3].shift(0.3 * RIGHT)
        count = Integer(0, font_size=44, color=HEADS)
        lab = Tex("heads:", font_size=34, color=FG)
        counter = VGroup(lab, count).arrange(RIGHT, buff=0.2).move_to([5.2, 2.4, 0])
        count.add_updater(lambda m: m.next_to(lab, RIGHT, buff=0.2))
        self.play(FadeIn(grid, lag_ratio=0.002), FadeIn(legend), run_time=1.5)
        self.add(counter)
        self.say(r"Flip a thousand coins and count the heads.", wait=0.2)
        results = VGroup()
        s = rng.random(COLS * ROWS) < 0.5
        flip_wave(self, grid, s, count)
        first = Integer(int(s.sum()), font_size=34, color=HEADS).move_to([5.2, 1.5, 0])
        results.add(first)
        self.play(FadeIn(first, shift=0.2 * DOWN), run_time=0.5)
        self.say(r"About five hundred. No surprise. Again, and again, and again\ldots", wait=0.1)
        for j in range(4):
            s = rng.random(COLS * ROWS) < 0.5
            flip_wave(self, grid, s, count, run_time=1.0)
            r = Integer(int(s.sum()), font_size=34, color=HEADS).next_to(results[-1], DOWN, buff=0.22)
            results.add(r)
            self.play(FadeIn(r, shift=0.2 * DOWN), run_time=0.35)
        self.say(r"Always close to 500, give or take a few dozen.")
        self.say(r"Now a question that sounds just as innocent:", wait=0.6)
        q = MathTex(r"P\big(\text{700 heads or more}\big) \;=\; ?", font_size=60, color=FG).move_to([0, 0.6, 0])
        self.play(FadeOut(VGroup(grid, legend, counter, results)), run_time=0.8)
        self.play(Write(q), run_time=1.5)
        self.say(r"Most people (and most software) reach for the famous bell curve.")
        bell = card(r"Bell curve (usual approximation)", sci(T["700"]["bell"]), CLT, width=4.6).move_to([-3.9, -0.9, 0])
        exact = card(r"Exact answer", sci(T["700"]["exact"]), TRUTH, width=4.6).move_to([3.9, -0.9, 0])
        self.play(q.animate.move_to([0, 2.5, 0]), FadeIn(bell, shift=0.2 * UP), run_time=1.2)
        self.say(r"It answers: about $8.5\times10^{-37}$. A tiny number, so who cares?")
        self.play(FadeIn(exact, shift=0.2 * UP), run_time=1.0)
        f700 = 10 ** T["700"]["bell_over_exact"]
        ratio = MathTex(r"\times\,%d" % round(f700), font_size=60, color=CLT).move_to([0, -0.9, 0])
        self.say(r"But the exact answer is ten times smaller: the approximation is off by a factor of %d."
                 % round(f700), anims=[FadeIn(ratio, scale=1.4)], run_time=1.0)
        q9 = MathTex(r"P\big(\text{900 heads or more}\big) \;=\; ?", font_size=60, color=FG).move_to(q)
        b9 = card(r"Bell curve (usual approximation)", sci(T["900"]["bell"]), CLT, width=4.6).move_to(bell)
        e9 = card(r"Exact answer", sci(T["900"]["exact"]), TRUTH, width=4.6).move_to(exact)
        r9 = MathTex(r"\times\,10^{%d}" % int(T["900"]["bell_over_exact"]), font_size=66, color=CLT).move_to(ratio)
        self.say(r"Ask about 900 heads instead\ldots",
                 anims=[TransformMatchingTex(q, q9), Transform(bell, b9), Transform(exact, e9), FadeOut(ratio)],
                 run_time=1.2)
        self.play(FadeIn(r9, scale=1.6), run_time=1.0)
        self.say(r"\ldots and it is wrong by a factor of a hundred billion billion. "
                 r"Twenty zeros.", extra=0.5)
        self.say(r"Floods, market crashes, an insurer going bankrupt: when the question is about "
                 r"\emph{rare} events, the bell curve can be spectacularly wrong.", extra=0.5)
        self.say(r"There is a branch of probability that gets these numbers right. "
                 r"To meet it, we will look at the same coins through three lenses.", extra=0.3)
        self.unsay()
        self.play(FadeOut(VGroup(q9, bell, exact, r9)), run_time=0.8)
        title = Tex(r"The Mathematics of the Unlikely", font_size=64, color=FG)
        sub = Tex(r"Large deviations, from coin flips to the arrow of time", font_size=34, color=MUTED)
        VGroup(title, sub).arrange(DOWN, buff=0.45)
        line = Line(LEFT * 4, RIGHT * 4, color=LDP, stroke_width=2).next_to(title, DOWN, buff=0.22)
        self.play(Write(title), run_time=1.6)
        self.play(GrowFromCenter(line), FadeIn(sub, shift=0.1 * UP), run_time=1.0)
        self.wait(2.5)
        self.play(FadeOut(VGroup(title, sub, line)), run_time=1.0)
