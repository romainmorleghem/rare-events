"""Seq 5 — Seeing the invisible: a million fair experiments never reach 700; a rigged coin + weights
estimates 10^-37 (and 10^-161) from 10 000 experiments. Importance sampling."""
from _common import *  # noqa
from manim import *
from common.style import FG, MUTED, HEADS, TAILS, RIGGED, TRUTH, LDP, CLT, LLN
from common.narrative import Narrated
from _stages import axis_cfg

NV = FACTS["naive"]
IMP = FACTS["importance"]
T = FACTS["tails"]


def coin_icon(text, color, r=0.55):
    c = Circle(radius=r, color=color, fill_color=color, fill_opacity=0.25, stroke_width=4)
    t = Tex(text, font_size=30, color=color).move_to(c)
    return VGroup(c, t)


class RiggedCoin(Narrated):
    def construct(self):
        self.chapter(r"5 \,$\cdot$\, Seeing the invisible")
        ax = Axes(x_range=[400, 750, 50], y_range=[0, 30000, 10000], x_length=10.5, y_length=4.1,
                  axis_config=axis_cfg(), x_axis_config={"include_numbers": True, "font_size": 24}
                  ).move_to([0.3, 0.45, 0])
        xl = Tex(r"number of heads, out of 1000", font_size=28, color=FG).next_to(ax.x_axis, DOWN, buff=0.5)
        self.say(r"In real life there is rarely a formula. To estimate the risk of a flood or a blackout, engineers "
                 r"simulate. So let us simulate our coins.", anims=[Create(ax), FadeIn(xl)], run_time=1.5, extra=0.3)
        rng = np.random.default_rng(2026)          # same stream as compute/facts.py
        heads = rng.binomial(1000, 0.5, size=NV["experiments"])
        checkpoints = np.unique(np.round(np.logspace(1, 6, 90)).astype(int))
        hists = [np.bincount(heads[:m], minlength=1001)[400:751] for m in checkpoints]
        edges = np.arange(400, 752) - 0.5
        t = ValueTracker(0)
        idx = lambda: min(len(checkpoints) - 1, int(t.get_value()))
        hist = always_redraw(lambda: steps(ax, edges, hists[idx()], HEADS, opacity=0.65, stroke=1.2))
        cnt = Integer(0, font_size=36, color=FG, group_with_commas=True)
        cnt.add_updater(lambda m: m.set_value(checkpoints[idx()]))
        cl = Tex(r"experiments:", font_size=30, color=MUTED)
        counter = VGroup(cl, cnt).arrange(RIGHT, buff=0.2).move_to([-3.0, 2.75, 0])
        cnt.add_updater(lambda m: m.next_to(cl, RIGHT, buff=0.2))
        m700 = DashedLine(ax.c2p(700, 0), ax.c2p(700, 26000), color=TRUTH, stroke_width=2.5)
        t700 = Tex(r"700", font_size=30, color=TRUTH).next_to(m700, UP, buff=0.1)
        self.add(hist, counter)
        self.play(Create(m700), FadeIn(t700), run_time=0.6)
        self.say(r"A computer flips 1000 coins, counts the heads, and starts again. A million times.",
                 anims=[t.animate(rate_func=linear).set_value(len(checkpoints) - 1)], run_time=8, wait=0.3)
        hist.clear_updaters()
        rec = Line(ax.c2p(NV["max_heads"], 0), ax.c2p(NV["max_heads"], 9000), color=CLT, stroke_width=3)
        rt = Tex(r"record: %d" % NV["max_heads"], font_size=28, color=CLT).next_to(rec, UP, buff=0.1)
        self.say(r"The record after a million tries: %d heads. Not a single experiment reached 700." % NV["max_heads"],
                 anims=[Create(rec), FadeIn(rt)], run_time=1, extra=0.3)
        years = 10 ** (-T["700"]["exact"]) / 1e9 / 3.156e7
        self.say(r"To see it even once, you would need about $10^{37}$ experiments. At a billion per second, "
                 r"that is $10^{%d}$ years: ten billion times the age of the universe." % int(np.log10(years)),
                 extra=0.4)
        self.play(FadeOut(VGroup(hist, rec, rt, counter)), run_time=0.8)

        # --- the rigged coin
        rig = coin_icon(r"70\%", RIGGED).move_to([-3.6, 2.55, 0])
        rl = Tex(r"rigged coin", font_size=26, color=RIGGED).next_to(rig, RIGHT, buff=0.2)
        self.say(r"The trick: cheat, then correct for the cheating. Flip a \emph{rigged} coin, "
                 r"one that lands heads 70\% of the time.", anims=[FadeIn(rig, scale=0.5), FadeIn(rl)], run_time=1)
        rh = np.random.default_rng(5).binomial(1000, 0.7, size=10**4)
        rcount = np.bincount(rh, minlength=1001)[400:751] * (30000 / 400)
        rax_lab = Tex(r"10\,000 experiments with the rigged coin", font_size=26, color=RIGGED
                      ).move_to([1.2, 2.75, 0])
        rhist = steps(ax, edges, rcount, RIGGED, opacity=0.6, stroke=1.2)
        hit = steps(ax, edges[300:], rcount[300:], RIGGED, opacity=0.95, stroke=1.5)
        self.say(r"Now 700 heads is ordinary: about half of the experiments reach it.",
                 anims=[FadeIn(rhist, shift=0.2 * UP), FadeIn(rax_lab), FadeIn(hit)], run_time=1.5, extra=0.3)
        self.play(FadeOut(VGroup(ax, xl, rhist, hit, m700, t700, rax_lab)), run_time=0.8)

        # --- the weights
        w = IMP["700"]
        h_, t_ = 703, 297
        lw = h_ * w["weight_per_head_log10"] + t_ * w["weight_per_tail_log10"]
        l1 = MathTex(r"\text{each head: } \times \frac{0.5}{0.7} = 0.714", font_size=38, color=HEADS)
        l2 = MathTex(r"\text{each tail: } \times \frac{0.5}{0.3} = 1.667", font_size=38, color=TAILS)
        l3 = MathTex(r"\text{703 heads, 297 tails: weight} = 0.714^{703}\times 1.667^{297} \approx %s" % sci(lw),
                     font_size=38, color=FG)
        VGroup(l1, l2, l3).arrange(DOWN, buff=0.4).move_to([0, 0.5, 0])
        self.say(r"But each of these results is \emph{more} likely with the rigged coin than with the fair one. "
                 r"So we give each one a weight that undoes the cheat.", extra=0.3)
        self.say(r"Every head was cheated in: multiply by $0.5/0.7$. Every tail was cheated out: multiply by "
                 r"$0.5/0.3$.", anims=[FadeIn(l1), FadeIn(l2)], run_time=1.2, extra=0.3)
        self.say(r"For a run with 703 heads, the weight is tiny: it says how rare that run really is with a fair coin.",
                 anims=[Write(l3)], run_time=1.5, extra=0.4)
        self.play(FadeOut(VGroup(l1, l2, l3)), run_time=0.6)
        est = card(r"Estimate from 10\,000 rigged experiments", sci(w["estimate_log10"]) +
                   r"\ \pm %d\%%" % round(100 * w["rel_error"]), RIGGED, width=6.0).move_to([-3.4, 0.6, 0])
        ex = card(r"Exact", sci(T["700"]["exact"]), TRUTH, width=4.6).move_to([3.6, 0.6, 0])
        self.say(r"Average the weights over all experiments (the misses count as zero), and out comes the probability:",
                 anims=[FadeIn(est, shift=0.2 * UP)], run_time=1.2, extra=0.3)
        self.say(r"Spot on. Ten thousand experiments instead of $10^{37}$.",
                 anims=[FadeIn(ex, shift=0.2 * UP)], run_time=1.2, extra=0.3)
        w9 = IMP["900"]
        est9 = card(r"Estimate, coin rigged to 90\%", sci(w9["estimate_log10"]) +
                    r"\ \pm %d\%%" % round(100 * w9["rel_error"]), RIGGED, width=6.0).move_to(est)
        ex9 = card(r"Exact", sci(T["900"]["exact"]), TRUTH, width=4.6).move_to(ex)
        self.say(r"900 heads? Rig the coin to 90\% instead. Again ten thousand experiments suffice.",
                 anims=[Transform(est, est9), Transform(ex, ex9),
                        Transform(rig, coin_icon(r"90\%", RIGGED).move_to(rig))], run_time=1.5, extra=0.4)
        self.say(r"This trick is called \emph{importance sampling}. It is how the probabilities of very rare "
                 r"failures are computed in engineering, finance and physics.", extra=0.3)
        self.say(r"Notice which coin we chose: the one that makes the rare event \emph{typical}. 70\% for 700 heads. "
                 r"Keep that in mind: it is not just a trick.", extra=0.5)
        self.unsay()
        self.play(FadeOut(VGroup(est, ex, rig, rl)), run_time=0.8)
