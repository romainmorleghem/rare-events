"""Seq 7 — The same bowl in physics: molecules left/right of a box are coins; all on one side is a
large deviation; the second law; S = k log W."""
from _common import *  # noqa
from manim import *
from common.style import FG, MUTED, HEADS, TAILS, LDP, TRUTH, BG
from common.narrative import Narrated
from common.coins import rate
from _stages import axis_cfg

GAS = FACTS["gas"]
W, H = 6.4, 3.6
CENTER = np.array([-2.7, 0.75, 0])


class Gas(VGroup):
    """Point molecules bouncing elastically in a box (positions as triangle waves of time)."""
    def __init__(self, n, seed, speed=1.3, r=0.07):
        super().__init__()
        g = np.random.default_rng(seed)
        self.p0 = g.random((n, 2)) * [W, H]
        ang = g.random(n) * 2 * np.pi
        self.v = speed * np.c_[np.cos(ang), np.sin(ang)] * (0.6 + 0.8 * g.random((n, 1)))
        self.t = 0.0
        for _ in range(n):
            self.add(Dot(radius=r))
        self.place()
        self.add_updater(lambda m, dt: m.step(dt))

    def positions(self):
        q = self.p0 + self.v * self.t
        L = np.array([W, H])
        m = np.mod(q, 2 * L)
        return np.where(m < L, m, 2 * L - m)

    def place(self):
        P = self.positions()
        for d, (x, y) in zip(self, P):
            d.move_to(CENTER + np.array([x - W / 2, y - H / 2, 0]))
            d.set_color(HEADS if x < W / 2 else TAILS)

    def step(self, dt):
        self.t += dt
        self.place()

    def left(self):
        return int((self.positions()[:, 0] < W / 2).sum())


class Physics(Narrated):
    def construct(self):
        self.chapter(r"7 \,$\cdot$\, The same bowl, in physics")
        box = Rectangle(width=W + 0.2, height=H + 0.2, color=FG, stroke_width=3).move_to(CENTER)
        mid = DashedLine(CENTER + (H / 2 + 0.1) * UP, CENTER + (H / 2 + 0.1) * DOWN, color=MUTED, stroke_width=2)
        lt = Tex(r"left", font_size=28, color=HEADS).next_to(box, UP, buff=0.12).shift(W / 4 * LEFT)
        rt = Tex(r"right", font_size=28, color=TAILS).next_to(box, UP, buff=0.12).shift(W / 4 * RIGHT)
        gas = Gas(10, 4, r=0.11)
        cnt = Integer(gas.left(), font_size=44, color=HEADS)
        cnt.add_updater(lambda m: m.set_value(gas.left()))
        cl = Tex(r"on the left:", font_size=32, color=FG)
        of = Tex(r"out of 10", font_size=32, color=FG)
        counter = VGroup(cl, cnt, of).arrange(RIGHT, buff=0.2).move_to([3.9, 2.2, 0])
        cnt.add_updater(lambda m: m.next_to(cl, RIGHT, buff=0.2))
        of.add_updater(lambda m: m.next_to(cnt, RIGHT, buff=0.2))
        self.play(Create(box), Create(mid), FadeIn(lt), FadeIn(rt), run_time=1)
        self.add(gas)
        self.say(r"Coins are not just a toy. Put 10 molecules of gas in a box. At every instant, each one is "
                 r"either in the left half or in the right half: heads or tails.", run_time=1, extra=0.5)
        self.play(FadeIn(counter), run_time=0.6)
        self.say(r"The number on the left keeps hovering around half, just like our coins.", extra=1.0)
        p10 = MathTex(r"\text{all 10 on the left: } 2^{-10} = \tfrac{1}{1024}", font_size=34, color=TRUTH
                      ).move_to([3.9, 1.2, 0])
        self.say(r"All 10 on the left at the same time: 1 chance in 1024. Rare, but you would see it if you "
                 r"watched for a while.", anims=[FadeIn(p10)], run_time=1, extra=0.5)
        gas100 = Gas(100, 9, speed=1.1)
        of100 = Tex(r"out of 100", font_size=32, color=FG).move_to(of, aligned_edge=LEFT)
        p100 = MathTex(r"\text{all 100 on the left: } 2^{-100} \approx 10^{-30}", font_size=34, color=TRUTH
                       ).next_to(p10, DOWN, buff=0.35)
        self.remove(gas)
        self.add(gas100)
        cnt.clear_updaters()
        cnt.add_updater(lambda m: m.set_value(gas100.left()))
        cnt.add_updater(lambda m: m.next_to(cl, RIGHT, buff=0.2))
        self.say(r"With 100 molecules: 1 chance in $10^{30}$. You could watch for the age of the universe "
                 r"and never see it.", anims=[Transform(of, of100), FadeIn(p100)], run_time=1, extra=0.5)
        pb = MathTex(r"\text{a balloon, } 10^{23} \text{ molecules:}", font_size=34, color=TRUTH)
        pb2 = MathTex(r"10^{-30\,000\,000\,000\,000\,000\,000\,000}", font_size=34, color=TRUTH)
        PB = VGroup(pb, pb2).arrange(DOWN, buff=0.15).next_to(p100, DOWN, buff=0.35)
        self.say(r"A balloon holds about $10^{23}$ molecules. The chance that they all crowd into one half has "
                 r"twenty-two zeros \emph{in its exponent}.", anims=[FadeIn(PB)], run_time=1.2, extra=0.6)
        self.play(FadeOut(VGroup(p10, p100, PB)), run_time=0.6)
        ax = Axes(x_range=[0, 1, 0.5], y_range=[0, 0.75, 0.25], x_length=4.2, y_length=2.4, axis_config=axis_cfg()
                  ).move_to([3.9, 0.2, 0])
        I = curve(ax, np.linspace(0, 1, 200), rate(np.linspace(0, 1, 200)), LDP, 4)
        il = Tex(r"fraction on the left: the same bowl", font_size=26, color=LDP).next_to(ax, DOWN, buff=0.2)
        self.say(r"The fraction of molecules on the left obeys exactly the same bowl as the coins: "
                 r"same counting, same rate function.", anims=[Create(ax), Create(I), FadeIn(il)], run_time=1.5,
                 extra=0.4)
        self.say(r"So nothing \emph{forbids} the air in your room from gathering in one corner. "
                 r"It is a large deviation, with an absurdly large $n$.", extra=0.5)
        self.say(r"That is the second law of thermodynamics: disorder wins, not because order is impossible, "
                 r"but because there are overwhelmingly more ways to be disordered.", extra=0.6)
        self.play(FadeOut(VGroup(ax, I, il)), run_time=0.6)
        stone = RoundedRectangle(corner_radius=0.5, width=3.6, height=2.0, stroke_color=MUTED, stroke_width=3,
                                 fill_color="#1B2029", fill_opacity=1).move_to([3.9, 0.3, 0])
        eq = MathTex(r"S = k \log W", font_size=60, color=FG).move_to(stone)
        nm = Tex(r"Ludwig Boltzmann, 1844--1906", font_size=26, color=MUTED).next_to(stone, DOWN, buff=0.2)
        self.say(r"Ludwig Boltzmann had the idea engraved on his tombstone: the entropy $S$ is the logarithm of "
                 r"the number of ways $W$. The very count of chapter 4.",
                 anims=[FadeIn(stone), Write(eq), FadeIn(nm)], run_time=1.5, extra=0.6)
        self.unsay()
        gas100.clear_updaters()
        self.play(FadeOut(VGroup(box, mid, lt, rt, gas100, counter, of, stone, eq, nm)), run_time=1)
