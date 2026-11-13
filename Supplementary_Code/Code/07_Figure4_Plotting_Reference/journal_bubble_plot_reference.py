from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

try:
    from adjustText import adjust_text
except ImportError:  # optional dependency
    adjust_text = None

SCRIPT_VERSION = "2026-08-02-final"


def main() -> None:
    parser = argparse.ArgumentParser(description="Draw the journal bubble plot used in the manuscript.")
    parser.add_argument("input_excel", type=Path, help="journal_bubble_plot_data.xlsx")
    parser.add_argument("--output", type=Path, default=None, help="Output PNG path")
    parser.add_argument("--top-n", type=int, default=25, help="Number of journals plotted")
    parser.add_argument("--label-n", type=int, default=12, help="Number of journals labelled")
    args = parser.parse_args()

    if not args.input_excel.exists():
        raise FileNotFoundError(args.input_excel)
    output = args.output or args.input_excel.with_name("journal_bubble_plot_adjusted.png")

    df = pd.read_excel(args.input_excel)
    required = ["Journal", "Publications", "Average_Citations", "Total_Citations", "Local_H_Index"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    df = df[required].copy()
    for col in required[1:]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna().sort_values("Publications", ascending=False).head(args.top_n).reset_index(drop=True)
    if df.empty:
        raise ValueError("No valid journal rows found.")

    bubble_size = df["Total_Citations"] / max(df["Total_Citations"].max(), 1) * 1800
    label_df = df.head(args.label_n)

    plt.close("all")
    fig, ax = plt.subplots(figsize=(14, 8))
    scatter = ax.scatter(
        df["Publications"], df["Average_Citations"],
        s=bubble_size, c=df["Local_H_Index"], cmap="viridis",
        alpha=0.75, edgecolors="black", linewidth=0.8
    )

    texts = [ax.text(row["Publications"], row["Average_Citations"], str(row["Journal"]), fontsize=9)
             for _, row in label_df.iterrows()]
    if adjust_text is not None:
        adjust_text(
            texts, ax=ax, expand_points=(1.2, 1.2), expand_text=(1.2, 1.2),
            force_text=0.8, force_points=0.5,
            arrowprops=dict(arrowstyle="-", color="gray", lw=0.6)
        )
    else:
        print("[WARN] adjustText is not installed; labels were not automatically repositioned.")

    ax.set_xlabel("Publications", fontsize=14)
    ax.set_ylabel("Average Citations", fontsize=14)
    ax.set_title("Journal Bubble Plot: Publications vs Average Citations\n"
                 "Bubble Size = Total Citations; Color = Local H-index", fontsize=18)
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label("Local H-index", fontsize=13)
    ax.grid(True, linestyle="--", alpha=0.3)
    ax.tick_params(axis="both", labelsize=12)
    plt.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output, dpi=600, bbox_inches="tight")
    plt.close(fig)
    print(f"Figure saved to: {output}")


if __name__ == "__main__":
    main()
