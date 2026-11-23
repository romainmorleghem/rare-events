# Rare Events

A video series (YouTube, no voice-over, captions only) and an interactive companion website on
**how unlikely "unlikely" is, and how rare events actually happen**. No background needed: coins,
histograms and counting.

Website: <https://romainmorleghem.github.io/rare-events/> (each episode: the video + interactive widgets).

| Ep | Title | Length | Video | Web page |
|----|-------|--------|-------|----------|
| 1 | The Mathematics of the Unlikely: three lenses on coin flips | ≈ 18 min | `web/ep1/ep01_1080p.mp4` | [ep1](https://romainmorleghem.github.io/rare-events/ep1/) |

---

## Episode 1 in a nutshell: one histogram, three lenses

Flip 1000 coins. P(at least 700 heads)? The bell curve says 8.5·10⁻³⁷, the truth is 8.8·10⁻³⁸ (×10).
For 900 heads the bell curve is wrong by a factor 10²⁰. Why?

The three classic results of probability are three ways of rescaling **the same histogram**:

| Lens | What we plot | What we see | Result |
|---|---|---|---|
| 1 | the proportion of heads | a spike at 1/2 | law of large numbers |
| 2 | zoom by √n around 1/2 | a fixed bell curve | central limit theorem |
| 3 | −(1/n)·ln P | a fixed bowl I(x) | large deviations: P ≈ e^(−n I(x)) |

The unifying picture is **the bowl**: its lowest point is where the average goes (lens 1), its curvature at
the bottom is the bell curve (lens 2), the whole bowl gives rare events (lens 3). Using the bell curve for
rare events means using the bottom of the bowl where the bowl has already bent away: at 90 % heads the gap is
0.048 per coin, i.e. e^48 ≈ 10²¹ over 1000 coins.

Then:
- **Counting.** The bowl is missing entropy, I(x) = ln 2 − H(x): rare outcomes are rare because few
  sequences produce them (10²⁹⁹ sequences with 500 heads, 10²⁶⁴ with 700).
- **The rigged coin.** A million fair simulations never reach 700 heads (record 572). Flip a coin rigged to
  70 % and weight each run by (0.5/0.7)^heads (0.5/0.3)^tails: 10⁴ runs give 8.5·10⁻³⁸ ± 4 %
  (importance sampling). Same for 900 heads: 6.4·10⁻¹⁶² vs 6.7·10⁻¹⁶².
- **How the unlikely happens.** Given 700 heads, every block of 100 coins has 63–77 % heads and the longest
  streak is ≈ 17: a conspiracy of all coins, exactly the rigged coin. With heavy-tailed ("wild") amounts it is
  the opposite: a large total comes from a single culprit (P = 3·10⁻⁴ instead of 1.8·10⁻¹⁵).
- **Physics.** Molecules left/right of a box are coins: the second law as a large deviation, S = k log W.
- **History.** Cramér (1938, insurance ruin), Varadhan (general theory, Abel Prize 2007).

Every number in the video is computed from scratch in `ep01_unlikely/compute/facts.py`.

---

## Repository layout
```
common/                  shared style (palette, LaTeX), narration helper, exact coin maths (coins.py)
ep01_unlikely/compute/   facts.py -> ep01_unlikely/data/facts.json, claims.json (committed)
ep01_unlikely/scenes/    Manim Community scenes, one file per sequence (sNN_*.py)
ep01_unlikely/render.py  renders all sequences and concatenates them
ep01_unlikely/storyboard.md  plan of the episode
web/                     static website: index + one page per episode (canvas + ES modules, KaTeX)
web/data/ep1.json        the fact sheet, for the page
media/                   render outputs (not published)
```

## Setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt   # Manim needs LaTeX + pango/cairo system libraries
```

## Render the episode
```bash
cd ep01_unlikely
python compute/facts.py           # regenerate data/facts.json and data/claims.json (≈ 1 min)
python render.py                  # 480p preview -> media/ep01/ep01_480p15.mp4
python render.py -q f             # 1080p30      -> media/ep01/ep01_1080p30.mp4
python render.py --only s03       # re-render one sequence and re-assemble
```
On a modest machine, the 480p preview of one sequence takes 20–60 s. Caption reading speed is set by
`WORDS_PER_SECOND` in `common/narrative.py` (3.0 words/s; raise it to shorten the episode).
Videos published on the site must stay under ~95 MB (GitHub's 100 MB file limit).

## Website
Static, no build step. Modules need HTTP, not `file://`:
```bash
cd web && python -m http.server 8000     # open http://localhost:8000
```
GitHub Pages: `.github/workflows/pages.yml` deploys `web/` on every push to `main`
(enable it once in the repository settings: Pages → Source: GitHub Actions).
