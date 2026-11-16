#!/usr/bin/env python3
"""
Restyled solar charts modelled on the "reality vs. IEA predictions" graphs.

Two looks, each in linear and log versions:
  - "tall": thick teal Reality line ending in an arrowhead, thin yellow
    Predictions with small dots, portrait layout.
  - "wide": black Reality line with big dots, thick yellow Predictions with
    big dots at the predicted values, landscape layout, bold title.

Both use a right-hand y-axis, horizontal gridlines only and a bare baseline.
Same data selection as plot_actual_solar.py (cur rows, 2023 WEO excluded).

Outputs (in graphs/):
  solar_generation_styled.png      solar_generation_styledLog.png
  solar_generation_styledWide.png  solar_generation_styledWideLog.png
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# Actuals that are part-year extrapolations, not final figures
# (2026: full-year 2025 x Ember Jan-Sep 2026 / Jan-Sep 2025)
ESTIMATED_YEARS = {2026}

PROJ_COLS = ["2020", "2025", "2030", "2035", "2040", "2050"]
GRID = "#E3E3E3"
AXIS_TEXT = "#8A8A8A"
TEXT = "#222222"

STYLES = {
    "tall": dict(
        figsize=(8, 10), suffix="",
        reality_color="#16807F", pred_color="#F5C400",
        reality_lw=3.5, reality_dot=28, pred_lw=1.6, pred_dot=14,
        arrow=True,
        title="Solar generation keeps exceeding predictions",
        title_kw=dict(fontsize=20, fontweight="normal"),
        subtitle=None,
        legend_loc=("upper left", (-0.01, 1.0)), legend_order=("Reality", "Predictions"),
        axis_text="#8A8A8A",
        margins=dict(left=0.04, right=0.88, top=0.93, bottom=0.07),
        title_xy=(0.04, 0.97),
    ),
    "wide": dict(
        figsize=(15, 7.5), suffix="Wide",
        reality_color="#111111", pred_color="#F6C21C",
        reality_lw=3.5, reality_dot=130, pred_lw=3.5, pred_dot=170,
        arrow=False,
        title="Actual solar generation keeps outstripping\n"
              "the International Energy Agency's predictions",
        # matplotlib only sees the regular face of Helvetica Neue on macOS; Avenir Next has bold
        title_kw=dict(fontsize=24, fontweight="bold", family=["Avenir Next", "DejaVu Sans"]),
        subtitle="Solar PV generation, terawatt-hours",
        legend_loc=("lower left", (0.0, 0.04)), legend_order=("Predictions", "Reality"),
        axis_text="#333333",
        margins=dict(left=0.02, right=0.93, top=0.97, bottom=0.11),
        title_xy=(0.015, 0.975),
    ),
}

plt.rcParams["font.family"] = ["Helvetica Neue", "Helvetica", "DejaVu Sans"]


def load_data(project_root: Path):
    df = pd.read_csv(project_root / "solar_report_filled.csv")
    df.columns = df.columns.str.strip()
    actual = df[df["Actually got"].notna()][["Year", "Actually got"]].sort_values("Year")
    cur = df[(df["pol"].str.strip().str.lower() == "cur") & (df["Year"] != 2023)]
    return actual, cur


def prediction_lines(actual, cur):
    """Each WEO line starts at the actual value in its publication year."""
    actual_by_year = dict(zip(actual["Year"], actual["Actually got"]))
    lines = []
    for _, row in cur.iterrows():
        pts = [(int(c), float(row[c])) for c in PROJ_COLS if pd.notna(row[c])]
        if not pts:
            continue
        # start from the actual in the publication year, or the latest actual before it
        # (e.g. WEO 2026 is published before any 2026 actual exists)
        earlier = [yr for yr in actual_by_year if yr <= row["Year"]]
        if earlier:
            start = max(earlier)
            pts = [(int(start), actual_by_year[start])] + pts
        lines.append(pts)
    return lines


def draw(actual, lines, style, log=False):
    s = STYLES[style]
    fig, ax = plt.subplots(figsize=s["figsize"])
    fig.patch.set_facecolor("white")
    fig.subplots_adjust(**s["margins"])

    # --- axes styling: right-hand y-axis, horizontal grid only, bare baseline
    for side in ("top", "left", "right"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color("#555555")
    ax.yaxis.tick_right()
    ax.tick_params(axis="both", length=0, colors=s["axis_text"],
                   labelsize=13 if style == "wide" else 11, pad=8)
    ax.grid(axis="y", color=GRID, lw=0.9)
    ax.grid(axis="x", visible=False)
    ax.set_axisbelow(True)
    ax.set_xlim(2008.5, 2051)
    ax.set_xticks(range(2010, 2051, 5))

    if log:
        ax.set_yscale("log")
        ax.set_ylim(10, 25000)
        ticks = [10, 100, 1000, 10000]
        ax.minorticks_off()
    else:
        # fit the highest prediction, ticks every 5,000 TWh
        top = max(v for pts in lines for _, v in pts)
        ax.set_ylim(0, top * 1.04)
        ticks = list(range(0, int(top) + 1, 5000))
    ax.set_yticks(ticks)
    ax.set_yticklabels([f"{t:,}" for t in ticks])
    if style == "wide":
        # labels sit just above their gridline, as in the reference
        for lbl in ax.get_yticklabels():
            lbl.set_verticalalignment("bottom")
    else:
        ax.annotate("TWh", xy=(1, ticks[-1]), xycoords=("axes fraction", "data"),
                    xytext=(8, 6), textcoords="offset points", ha="left",
                    va="bottom", color=AXIS_TEXT, fontsize=11)

    # --- predictions (behind reality)
    for pts in lines:
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=s["pred_color"], lw=s["pred_lw"], zorder=2,
                solid_capstyle="round")
        # dots on predicted values only (not on the starting actual)
        ax.scatter(xs[1:], ys[1:], color=s["pred_color"], s=s["pred_dot"],
                   zorder=2, linewidths=0)

    # --- reality (years in ESTIMATED_YEARS are drawn dashed and labelled)
    x, y = actual["Year"].to_numpy(), actual["Actually got"].to_numpy()
    n_final = sum(1 for yr in x if yr not in ESTIMATED_YEARS)
    ax.plot(x[:n_final], y[:n_final], color=s["reality_color"], lw=s["reality_lw"],
            zorder=4, solid_capstyle="round")
    if n_final < len(x):
        ax.plot(x[n_final - 1:], y[n_final - 1:], color=s["reality_color"],
                lw=s["reality_lw"] * 0.8, zorder=4, ls=(0, (2, 1.5)))
        ax.annotate(f"{int(x[-1])} (estimate)", xy=(x[-1], y[-1]), xytext=(-10, 4),
                    textcoords="offset points", ha="right", va="bottom",
                    fontsize=10, color=s["reality_color"], zorder=7)
    if s["arrow"]:
        ax.scatter(x[:-1], y[:-1], color=s["reality_color"], s=s["reality_dot"],
                   zorder=5, linewidths=0)
        # filled head only (lw=0 hides the shaft; the line is already drawn)
        ax.annotate("", xy=(x[-1], y[-1]), xytext=(x[-2], y[-2]), zorder=6,
                    arrowprops=dict(arrowstyle="-|>,head_length=1.1,head_width=0.38",
                                    facecolor=s["reality_color"], lw=0,
                                    shrinkA=0, shrinkB=0, mutation_scale=16))
    else:
        ax.scatter(x[:n_final], y[:n_final], color=s["reality_color"],
                   s=s["reality_dot"], zorder=5, linewidths=0)
        ax.scatter(x[n_final:], y[n_final:], facecolor="white",
                   edgecolor=s["reality_color"], s=s["reality_dot"], lw=2.5, zorder=5)

    # --- title, legend, footer
    fig.text(*s["title_xy"], s["title"], color=TEXT, ha="left", va="top",
             linespacing=1.3, **s["title_kw"])
    handles = {
        "Reality": plt.Line2D([], [], color=s["reality_color"], lw=s["reality_lw"] + 1),
        "Predictions": plt.Line2D([], [], color=s["pred_color"], lw=s["pred_lw"] + 1),
    }
    order = s["legend_order"]
    loc, anchor = s["legend_loc"]
    leg = ax.legend([handles[k] for k in order], order, loc=loc, bbox_to_anchor=anchor,
                    frameon=False, fontsize=14 if style == "wide" else 12,
                    handlelength=1.6 if style == "wide" else 2.2, labelcolor=TEXT,
                    title=s["subtitle"], alignment="left",
                    title_fontproperties=dict(weight="bold", size=14))
    if s["subtitle"]:
        leg._legend_box.sep = 14  # gap between subtitle and entries
    leg.set_zorder(10)

    fig.text(0.015 if style == "wide" else 0.04, 0.012,
             "World solar PV generation vs. IEA WEO "
             "(Current Policies) predictions, WEO 2009–2025"
             + (" · log scale" if log else ""),
             fontsize=9, color=AXIS_TEXT, ha="left", va="bottom")
    fig.text(0.985 if style == "wide" else 0.96, 0.012, "by @iamredave",
             fontsize=9.5, color=AXIS_TEXT, style="italic", ha="right", va="bottom")
    return fig


def main():
    project_root = Path(__file__).resolve().parent.parent
    graphs_dir = project_root / "graphs"
    graphs_dir.mkdir(exist_ok=True)
    actual, cur = load_data(project_root)
    lines = prediction_lines(actual, cur)

    for style in STYLES:
        for log in (False, True):
            fig = draw(actual, lines, style, log=log)
            out = graphs_dir / f"solar_generation_styled{STYLES[style]['suffix']}{'Log' if log else ''}.png"
            fig.savefig(out, dpi=200)
            plt.close(fig)
            print("Saved", out)


if __name__ == "__main__":
    main()
