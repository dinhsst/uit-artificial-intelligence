from __future__ import annotations

import os
from typing import Dict, List, Set

REGIONS: List[str] = [
    "Long An", "Tien Giang", "Dong Thap", "Vinh Long", "Ben Tre",
    "Tra Vinh", "An Giang", "Can Tho", "Hau Giang", "Soc Trang",
    "Kien Giang", "Bac Lieu", "Ca Mau",
]

COLOR_NAMES: List[str] = ["Đỏ", "Xanh dương", "Xanh lá", "Vàng", "Tím", "Cam"]
COLOR_HEX: List[str] = ["#E24B4A", "#378ADD", "#639922", "#EF9F27", "#7F77DD", "#D85A30"]

ADJACENCY: Dict[str, Set[str]] = {
    "Long An": {"Tien Giang", "Dong Thap"},
    "Tien Giang": {"Long An", "Dong Thap", "Vinh Long", "Ben Tre"},
    "Dong Thap": {"Long An", "Tien Giang", "Vinh Long", "An Giang", "Can Tho"},
    "Vinh Long": {"Tien Giang", "Dong Thap", "Ben Tre", "Tra Vinh", "Can Tho", "Soc Trang"},
    "Ben Tre": {"Tien Giang", "Vinh Long", "Tra Vinh"},
    "Tra Vinh": {"Vinh Long", "Ben Tre", "Soc Trang"},
    "An Giang": {"Dong Thap", "Can Tho", "Kien Giang"},
    "Can Tho": {"Dong Thap", "Vinh Long", "An Giang", "Hau Giang", "Kien Giang"},
    "Hau Giang": {"Can Tho", "Soc Trang", "Kien Giang", "Bac Lieu"},
    "Soc Trang": {"Vinh Long", "Tra Vinh", "Hau Giang", "Bac Lieu"},
    "Kien Giang": {"An Giang", "Can Tho", "Hau Giang", "Bac Lieu", "Ca Mau"},
    "Bac Lieu": {"Hau Giang", "Soc Trang", "Kien Giang", "Ca Mau"},
    "Ca Mau": {"Kien Giang", "Bac Lieu"},
}

POSITIONS: Dict[str, tuple[float, float]] = {
    "Long An": (0.78, 1.00), "Tien Giang": (0.78, 0.80),
    "Dong Thap": (0.36, 0.92), "Vinh Long": (0.60, 0.62),
    "Ben Tre": (0.98, 0.62), "Tra Vinh": (0.88, 0.40),
    "An Giang": (0.12, 0.72), "Can Tho": (0.44, 0.56),
    "Hau Giang": (0.42, 0.38), "Soc Trang": (0.70, 0.24),
    "Kien Giang": (0.08, 0.34), "Bac Lieu": (0.46, 0.10),
    "Ca Mau": (0.20, -0.06),
}


def dsatur_coloring() -> Dict[str, int]:
    coloring: Dict[str, int] = {}
    neighbor_colors: Dict[str, Set[int]] = {region: set() for region in REGIONS}

    while len(coloring) < len(REGIONS):
        uncolored = [region for region in REGIONS if region not in coloring]
        region = max(uncolored, key=lambda item: (len(neighbor_colors[item]), len(ADJACENCY[item])))
        color = 1
        while color in neighbor_colors[region]:
            color += 1
        coloring[region] = color
        for neighbor in ADJACENCY[region]:
            neighbor_colors[neighbor].add(color)

    return coloring


def validate_coloring(coloring: Dict[str, int]) -> None:
    if set(coloring) != set(REGIONS):
        raise ValueError("Chưa tô đủ tất cả tỉnh.")
    for region, neighbors in ADJACENCY.items():
        for neighbor in neighbors:
            if coloring[region] == coloring[neighbor]:
                raise ValueError(f"{region} và {neighbor} đang cùng màu.")


def is_k_colorable(max_colors: int) -> bool:
    coloring: Dict[str, int] = {}

    def backtrack() -> bool:
        if len(coloring) == len(REGIONS):
            return True

        uncolored = [region for region in REGIONS if region not in coloring]
        region = max(
            uncolored,
            key=lambda item: (len({coloring[n] for n in ADJACENCY[item] if n in coloring}), len(ADJACENCY[item])),
        )
        used_colors = {coloring[neighbor] for neighbor in ADJACENCY[region] if neighbor in coloring}
        for color in range(1, max_colors + 1):
            if color not in used_colors:
                coloring[region] = color
                if backtrack():
                    return True
                del coloring[region]
        return False

    return backtrack()


def draw_graph(coloring: Dict[str, int], num_colors: int, filename: str = "ket_qua.png") -> None:
    import matplotlib.pyplot as plt
    import networkx as nx

    graph = nx.Graph()
    for region, neighbors in ADJACENCY.items():
        for neighbor in neighbors:
            graph.add_edge(region, neighbor)

    plt.figure(figsize=(9, 9))
    node_colors = [COLOR_HEX[(coloring[node] - 1) % len(COLOR_HEX)] for node in graph.nodes()]
    nx.draw_networkx_edges(graph, POSITIONS, edge_color="#888888", width=1.5)
    nx.draw_networkx_nodes(graph, POSITIONS, node_color=node_colors, node_size=2800, edgecolors="#000000")
    nx.draw_networkx_labels(graph, POSITIONS, font_size=9, font_weight="bold", font_color="white")
    plt.title(f"Bài 1.17 - Tô màu 13 tỉnh miền Nam (Tổng: {num_colors} màu)", fontsize=14)
    plt.axis("off")
    plt.tight_layout()
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"\nĐã lưu hình ảnh sơ đồ kết quả tại: {output_path}")


def main() -> None:
    coloring = dsatur_coloring()
    validate_coloring(coloring)
    if is_k_colorable(2) or not is_k_colorable(3):
        raise RuntimeError("Không thể xác nhận sắc số của đồ thị.")

    num_colors = max(coloring.values())
    print("Sắc số tối ưu: 3 màu")
    print("Kết quả tô màu:")
    for region in REGIONS:
        color = coloring[region]
        print(f"- {region:<12}: màu {color} ({COLOR_NAMES[color - 1]})")

    try:
        draw_graph(coloring, num_colors)
    except ImportError:
        print("\nĐã in lời giải. Cài 'networkx' và 'matplotlib' để xuất ảnh: pip install networkx matplotlib")
    except Exception as error:
        print(f"\nKhông thể vẽ hình: {error}")


if __name__ == "__main__":
    main()
