# Episode 1 — The Mathematics of the Unlikely (large deviations)

Same production style as *Routes to Chaos*: Manim CE 0.22.1, dark palette (`common/style.py`), LaTeX,
captions via `Narrated.say()`, no voice-over, English. Target ≈ 14 min.
**Audience: no background needed.** Only coins, histograms and "how many ways". No Legendre transform,
no Chernoff bound, no theorem names beyond LLN / CLT / "rate function". Every number comes from
`compute/facts.py` (→ `data/facts.json`).

## The original angle
LLN and CLT are heavily covered on YouTube. What is missing: **the three classic results are three
ways of rescaling the same histogram**, and the third one (large deviations) is the one that answers
questions about rare events.

| Lens | What we plot | What we see | Level |
|---|---|---|---|
| 1 | proportion of heads | a spike at 1/2 | law of large numbers |
| 2 | zoom by √n around 1/2 | a fixed bell curve | central limit theorem |
| 3 | −(1/n)·log P | a fixed bowl I(x) | large deviations |

Unifying picture (used at the end of s03 and in the recap): **the bowl I(x)**. Its lowest point is
where the average goes (lens 1); its curvature at the bottom is the bell curve (lens 2); the whole
bowl gives rare events (lens 3). Using the bell curve far away = using the bottom of the bowl
where the bowl has already bent away.

## Colour code
gold = heads / exact histogram, blue = tails, green = lens 1, pink = bell curve (lens 2),
violet = bowl / rate function (lens 3), orange = rigged coin, cream = exact values.

## Sequences
- **s00 Cold open** — a grid of 1000 coins flips; ≈ 500 heads, again and again. Question: P(≥ 700 heads)?
  Bell curve 8.5·10⁻³⁷, truth 8.8·10⁻³⁸ (×10). 900 heads: wrong by ×10²⁰·⁷. Title card.
- **s01 Lens 1 — where does the average go?** Running proportion of heads, one path then 60 paths
  (a funnel to 1/2). Then the histogram of the proportion for n = 10, 100, 1000: it collapses to a spike.
- **s02 Lens 2 — how much does it wiggle?** Zoom by √n: the three spikes become one bell.
  Same with averages of dice (n = 1, 2, 3, 10). For 1000 coins: ±16 heads typical, 95 % in [469, 531].
  700 heads is 12.6 standard deviations away: is the bell still valid out there?
- **s03 Lens 3 — how rare is rare?** The 700 bar is 10⁻³⁵·⁷ of the peak (if the peak is 30 cm, the bar
  is shorter than the Planck length). Switch to a log axis: the histogram becomes a dome; the bell
  becomes a parabola that drifts away (×10²⁰ at 900). Divide by n: n = 10, 100, 1000 collapse onto
  the bowl I(x). Each extra coin costs the same factor (1.086 for 70 %): P ≈ e^{−n I(x)}.
  Unifying picture: bottom point / curvature / whole bowl.
- **s04 Where does the bowl come from? Counting.** The 16 sequences of 4 coins sorted 1-4-6-4-1.
  For 1000 coins: 10³⁰¹ sequences, 10²⁹⁹ with 500 heads, 10²⁶⁴ with 700, 10¹⁴⁰ with 900.
  log(number of ways)/n → the entropy dome H(x); the bowl is ln 2 − H(x): "how many ways you lose".
- **s05 Seeing the invisible — the rigged coin.** A million simulated experiments: record 572 heads,
  zero hits. Cheat with a 70 % coin (half the experiments hit), then weight each hit by how much
  less likely it was with the fair coin (×0.714 per head, ×1.667 per tail). 10⁴ rigged experiments:
  8.5·10⁻³⁸ ± 4 % (exact 8.8·10⁻³⁸). Same for 900 heads: 10⁻¹⁶¹. Importance sampling.
- **s06 How does the unlikely happen?** Given 700 heads: no miracle streak (longest run ≈ 17), every
  block of 100 coins has 63–77 % heads: a conspiracy of all coins, exactly the rigged coin.
  "The unlikely happens in the least unlikely way." Then light vs heavy tails: 100 claims of mean 1,
  total forced to 200. Ordinary claims: all bars rise (largest ≈ 10). Wild claims (Pareto 2.5): one
  bar ≈ 136, the others normal. Probabilities 10⁻¹⁴·⁷ vs 3·10⁻⁴. Conspiracy vs culprit.
- **s07 The same bowl in physics.** Molecules in a box; fraction on the left; all on one side:
  2⁻¹⁰, 10⁻³⁰, 10^(−3·10²²). The second law as a large deviation (S = k log W).
- **s08 Recap & history.** The bowl with its three readings. Cramér (1938, insurance), Varadhan
  (Abel 2007). Uses: insurance, networks, climate extremes, chemistry. Website card.

## Website (web/ep1)
1. Three lenses: slider n, toggle lens 1/2/3 on the exact histogram, bell and bowl overlays.
2. The rigged coin: threshold slider, naive vs rigged simulation run live, estimate vs exact.
3. Conspiracy or culprit: light vs heavy claims, force the total, see the bars.
