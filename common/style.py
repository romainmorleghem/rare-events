"""Shared visual identity for *Rare Events* (same dark look as Routes to Chaos)."""
from manim import config, TexTemplate, ManimColor

BG = ManimColor("#0E1116")
FG = ManimColor("#E6E6E6")
MUTED = ManimColor("#7A8291")
GRID = ManimColor("#262D38")

HEADS = ManimColor("#F2B544")    # a coin showing heads, the exact histogram
TAILS = ManimColor("#3F7FC8")    # a coin showing tails
LLN = ManimColor("#6CCB8B")      # level 1: the law of large numbers
CLT = ManimColor("#E85D75")      # level 2: the bell curve
LDP = ManimColor("#C792EA")      # level 3: the rate function
RIGGED = ManimColor("#FF8A4C")   # the rigged coin
TRUTH = ManimColor("#FFF4D6")    # exact values

TEX = TexTemplate()
TEX.add_to_preamble(r"\usepackage{amsmath,amssymb}")


def setup():
    config.background_color = BG
    config.tex_template = TEX
