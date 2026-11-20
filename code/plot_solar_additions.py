#!/usr/bin/env python3
"""
Solar capacity added each year (GW/yr): actual vs. what each IEA WEO implied.

Same look as plot_solar_styled.py (teal Reality, yellow Predictions).

Predictions: for each edition, the average annual additions implied between
consecutive benchmark years (edition's own base year -> first projection year,
then projection -> projection), plotted at the end of each period. Each line
starts at the actual additions in the latest year <= the edition year.

Data:
  solar_capacity_predictions.csv  cumulative GW by edition (base + projections)
  solar_capacity_actual.csv       IEA cumulative GW (latest WEO reporting each year)

Outputs (in graphs/):
  solar_additions_styled.png  solar_additions_styledWide.png
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from plot_solar_styled import AXIS_TEXT, GRID, STYLES, TEXT

TITLES = {
    "tall": "Solar installations keep exceeding predictions",
    "wide": "Actual solar installations keep outstripping\n"
            "the International Energy Agency's predictions",
}


def load(project_root: Path):
    act = pd.read_csv(project_root / "solar_capacity_actual.csv")
    act = act[act["iea_added_gw"].notna()][["year", "iea_added_gw"]]
    pred = pd.read_csv(project_root / "solar_capacity_predictions.csv")
    return act, pred


def prediction_lines(act, pred):
    added = dict(zip(act["year"], act["iea_added_gw"]))
    lines = []
    for ed, g in pred.groupby("edition"):
        g = g.sort_values("year")
        yrs, gws = g["year"].tolist(), g["gw"].tolist()
        pts = [(y1, (c1 - c0) / (y1 - y0))
               for y0, c0, y1, c1 in zip(yrs, gws, yrs[1:], gws[1:])]
        start = max(y for y in added if y <= ed)
        lines.append((ed, [(start, added[start])] + pts))
    return lines


def draw(act, lines, style):
    s = dict(STYLES[style])
    if style == "wide":
        s["margins"] = dict(s["margins"], top=0.80)  # room between title and the 2035 peak
    fig, ax = plt.subplots(figsize=s["figsize"])
    fig.patch.set_facecolor("white")
    fig.subplots_adjust(**s["margins"])

    for side in ("top", "left", "right"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color("#555555")
    ax.yaxis.tick_right()
    ax.tick_params(axis="both", length=0, colors=s["axis_text"],
                   labelsize=13 if style == "wide" else 11, pad=8)
    ax.grid(axis="y", color=GRID, lw=0.9)
    ax.grid(axis="x", visible=False)
    ax.set_axisbelow(True)
    ax.set_xlim(2007.5, 2051)
    ax.set_xticks(range(2010, 2051, 5))

    top = max(max(v for _, v in pts) for _, pts in lines)
    top = max(top, act["iea_added_gw"].max())
    ax.set_ylim(0, top * 1.06)
    ticks = list(range(0, int(top) + 1, 200))
    ax.set_yticks(ticks)
    # unit on the top tick, e.g. "600 GW"
    ax.set_yticklabels([f"{t:,}" + (" GW" if t == ticks[-1] else "") for t in ticks])
    if style == "wide":
        for lbl in ax.get_yticklabels():
            lbl.set_verticalalignment("bottom")

    for ed, pts in lines:
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=s["pred_color"], lw=s["pred_lw"], zorder=2,
                solid_capstyle="round")
        ax.scatter(xs[1:], ys[1:], color=s["pred_color"], s=s["pred_dot"],
                   zorder=2, linewidths=0)

    # label the newest edition at its 2040 point, where it is clear of the other lines
    ed, pts = lines[-1]
    ax.annotate(f"WEO {ed}", xy=pts[-2], xytext=(8, 8), textcoords="offset points",
                ha="left", va="bottom", fontsize=11 if style == "wide" else 9.5,
                color="#8A6D00", zorder=7)

    x, y = act["year"].to_numpy(), act["iea_added_gw"].to_numpy()
    ax.plot(x, y, color=s["reality_color"], lw=s["reality_lw"], zorder=4,
            solid_capstyle="round")
    if s["arrow"]:
        ax.scatter(x[:-1], y[:-1], color=s["reality_color"], s=s["reality_dot"],
                   zorder=5, linewidths=0)
        ax.annotate("", xy=(x[-1], y[-1]), xytext=(x[-2], y[-2]), zorder=6,
                    arrowprops=dict(arrowstyle="-|>,head_length=1.1,head_width=0.38",
                                    facecolor=s["reality_color"], lw=0,
                                    shrinkA=0, shrinkB=0, mutation_scale=16))
    else:
        ax.scatter(x, y, color=s["reality_color"], s=s["reality_dot"],
                   zorder=5, linewidths=0)
    ax.annotate(f"{int(x[-1])}: {int(y[-1])} GW", xy=(x[-1], y[-1]), xytext=(-14, -6),
                textcoords="offset points", ha="right", va="top",
                fontsize=11 if style == "wide" else 9.5, color=s["reality_color"], zorder=7)

    fig.text(*s["title_xy"], TITLES[style], color=TEXT, ha="left", va="top",
             linespacing=1.3, **s["title_kw"])
    handles = {
        "Reality": plt.Line2D([], [], color=s["reality_color"], lw=s["reality_lw"] + 1),
        "Predictions": plt.Line2D([], [], color=s["pred_color"], lw=s["pred_lw"] + 1),
    }
    order = s["legend_order"]
    loc, anchor = s["legend_loc"]
    if style == "wide":
        anchor = (0.0, 0.30)  # sit above the dense bundle of early predictions
    leg = ax.legend([handles[k] for k in order], order, loc=loc, bbox_to_anchor=anchor,
                    frameon=False, fontsize=14 if style == "wide" else 12,
                    handlelength=1.6 if style == "wide" else 2.2, labelcolor=TEXT,
                    title="Solar PV capacity added each year, gigawatts" if s["subtitle"] else None,
                    alignment="left", title_fontproperties=dict(weight="bold", size=14))
    if s["subtitle"]:
        leg._legend_box.sep = 14
    leg.set_zorder(10)

    fig.text(0.015 if style == "wide" else 0.04, 0.012,
             "World solar PV capacity additions (IEA) vs. average annual additions implied by "
             + ("\n" if style == "tall" else "")
             + "each WEO, 2009–2026 (Current/Stated Policies)",
             fontsize=9, color=AXIS_TEXT, ha="left", va="bottom")
    fig.text(0.985 if style == "wide" else 0.96, 0.012, "by @iamredave",
             fontsize=9.5, color=AXIS_TEXT, style="italic", ha="right", va="bottom")
    return fig


def main():
    project_root = Path(__file__).resolve().parent.parent
    graphs_dir = project_root / "graphs"
    act, pred = load(project_root)
    lines = prediction_lines(act, pred)
    for ed, pts in lines:
        print(ed, [(y, round(v)) for y, v in pts])
    for style in STYLES:
        fig = draw(act, lines, style)
        out = graphs_dir / f"solar_additions_styled{STYLES[style]['suffix']}.png"
        fig.savefig(out, dpi=200)
        plt.close(fig)
        print("Saved", out)


if __name__ == "__main__":
    main()
