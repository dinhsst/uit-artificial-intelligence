from __future__ import annotations

import os
from typing import Dict, List, Optional, Set, Tuple

import matplotlib

matplotlib.use("Agg")
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D



# Danh sách 5 khu vực Tây Nguyên theo sơ đồ đề bài.
REGIONS: List[str] = [
    "Kon Tum",
    "Gia Lai",
    "Dak Lak",
    "Dak Nong",
    "Lam Dong",
]

# Đồ thị kề được suy ra từ bản đồ trong đề.
# Hai vùng chung biên giới thì không được tô cùng màu.
ADJACENCY: Dict[str, Set[str]] = {
    "Kon Tum": {"Gia Lai"},
    "Gia Lai": {"Kon Tum", "Dak Lak"},
    "Dak Lak": {"Gia Lai", "Dak Nong", "Lam Dong"},
    "Dak Nong": {"Dak Lak", "Lam Dong"},
    "Lam Dong": {"Dak Lak", "Dak Nong"},
}


def is_safe(region: str, color: int, assignment: Dict[str, int]) -> bool:
    for neighbor in ADJACENCY[region]:
        if assignment.get(neighbor) == color:
            return False
    return True


def choose_next_region(assignment: Dict[str, int]) -> Optional[str]:
    uncolored = [region for region in REGIONS if region not in assignment]
    if not uncolored:
        return None
    return max(uncolored, key=lambda region: len(ADJACENCY[region]))


def backtrack(max_colors: int, assignment: Dict[str, int]) -> bool:
    region = choose_next_region(assignment)
    if region is None:
        return True

    for color in range(1, max_colors + 1):
        if is_safe(region, color, assignment):
            assignment[region] = color
            if backtrack(max_colors, assignment):
                return True
            del assignment[region]

    return False


def find_minimum_coloring() -> Tuple[int, Dict[str, int]]:
    for max_colors in range(1, len(REGIONS) + 1):
        assignment: Dict[str, int] = {}
        if backtrack(max_colors, assignment):
            return max_colors, assignment
    raise RuntimeError("Khong tim duoc cach to mau hop le.")


def draw_coloring_result(coloring: Dict[str, int]) -> None:
    positions: Dict[str, Tuple[float, float]] = {
        "Kon Tum": (0, 2),
        "Gia Lai": (2, 2),
        "Dak Lak": (4, 1),
        "Dak Nong": (6, 1.8),
        "Lam Dong": (8, 1),
    }

    palette: Dict[int, str] = {
        1: "#ff6b6b",
        2: "#4dabf7",
        3: "#69db7c",
        4: "#ffd43b",
        5: "#b197fc",
        6: "#ffa8a8",
    }

    fig, ax = plt.subplots(figsize=(10, 5))

    for region_a, neighbors in ADJACENCY.items():
        x1, y1 = positions[region_a]
        for region_b in neighbors:
            if region_a < region_b:
                x2, y2 = positions[region_b]
                ax.plot([x1, x2], [y1, y2], color="#495057", linewidth=2)

    for region in REGIONS:
        x, y = positions[region]
        color_id = coloring[region]
        ax.scatter(
            x,
            y,
            s=2600,
            color=palette.get(color_id, "#ced4da"),
            edgecolors="black",
            linewidths=1.5,
            zorder=3,
        )
        ax.text(x, y, region, ha="center", va="center", fontsize=9, color="black", zorder=4)

    unique_colors = sorted(set(coloring.values()))
    legend_handles = [
        Line2D(
            [0],
            [0],
            marker="o",
            linestyle="",
            markersize=10,
            markerfacecolor=palette.get(color_id, "#ced4da"),
            markeredgecolor="black",
            label=f"Mau {color_id}",
        )
        for color_id in unique_colors
    ]
    ax.legend(handles=legend_handles, loc="upper right", frameon=True)

    ax.set_xlim(-1, 10)
    ax.set_ylim(0, 3.5)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.tight_layout()
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "ket_qua_to_mau.png")
    fig.savefig(output_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    print(f"\nHinh ket qua da duoc luu tai: {output_path}")


def main() -> None:
    num_colors, coloring = find_minimum_coloring()

    print(f"So mau it nhat can dung: {num_colors}")
    print("Ket qua to mau:")
    for region in REGIONS:
        print(f"- {region}: mau {coloring[region]}")

    draw_coloring_result(coloring)


if __name__ == "__main__":
    main()
