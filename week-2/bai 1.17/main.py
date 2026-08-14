from __future__ import annotations

import os
from typing import Dict, List, Set
import matplotlib.pyplot as plt
import networkx as nx

# 1. Khai báo danh sách 13 tỉnh miền Nam
REGIONS: List[str] = [
    "Long An", "Tien Giang", "Dong Thap", "Vinh Long", "Ben Tre",
    "Tra Vinh", "An Giang", "Can Tho", "Hau Giang", "Soc Trang",
    "Kien Giang", "Bac Lieu", "Ca Mau",
]

# Danh sách màu hiển thị
COLOR_NAMES: List[str] = ["Đỏ", "Xanh dương", "Xanh lá", "Vàng", "Tím", "Cam"]
COLOR_HEX: List[str] = ["#E24B4A", "#378ADD", "#639922", "#EF9F27", "#7F77DD", "#D85A30"]

# 2. Đồ thị kề giáp ranh giữa các tỉnh
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

# Tọa độ tương đối các tỉnh để vẽ sơ đồ trực quan
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
    """Thuật toán tô màu DSATUR (Độ bảo hòa)."""
    coloring: Dict[str, int] = {}
    
    # Tập hợp các màu kề với từng tỉnh
    neighbor_colors: Dict[str, Set[int]] = {region: set() for region in REGIONS}

    while len(coloring) < len(REGIONS):
        # Chọn tỉnh chưa tô có:
        # 1. Số màu kề xung quanh là NHIỀU NHẤT (Độ bảo hòa cao nhất)
        # 2. Nếu bằng nhau, chọn tỉnh có số tỉnh kề (bậc) NHIỀU NHẤT
        uncolored = [r for r in REGIONS if r not in coloring]
        next_region = max(
            uncolored,
            key=lambda r: (len(neighbor_colors[r]), len(ADJACENCY[r]))
        )

        # Tìm màu nhỏ nhất (từ 1 trở đi) chưa bị trùng với các tỉnh kề
        color = 1
        while color in neighbor_colors[next_region]:
            color += 1

        coloring[next_region] = color

        # Cập nhật thông tin màu kề cho các tỉnh xung quanh
        for neighbor in ADJACENCY[next_region]:
            neighbor_colors[neighbor].add(color)

    return coloring


def draw_graph(coloring: Dict[str, int], num_colors: int, filename: str = "ket_qua.png") -> None:
    """Vẽ đồ thị kết quả tô màu các tỉnh."""
    G = nx.Graph()
    for region, neighbors in ADJACENCY.items():
        for neighbor in neighbors:
            G.add_edge(region, neighbor)

    plt.figure(figsize=(9, 9))
    
    # Lấy danh sách màu HEX tương ứng với kết quả tô
    node_colors = [COLOR_HEX[(coloring[node] - 1) % len(COLOR_HEX)] for node in G.nodes()]

    # Vẽ cạnh và nút
    nx.draw_networkx_edges(G, POSITIONS, edge_color="#888888", width=1.5)
    nx.draw_networkx_nodes(G, POSITIONS, node_color=node_colors, node_size=2800, edgecolors="#000000")
    nx.draw_networkx_labels(G, POSITIONS, font_size=9, font_weight="bold", font_color="white")

    plt.title(f"Bài 1.17 - Tô màu 13 tỉnh miền Nam (Tổng: {num_colors} màu)", fontsize=14)
    plt.axis("off")
    plt.tight_layout()
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, filename)
    plt.savefig(output_path, dpi=150)
    print(f"\nDa luu hinh anh sơ đồ ket qua tai: {filename}")


def main() -> None:
    coloring = dsatur_coloring()
    num_colors = max(coloring.values())

    print(f"So mau it nhat can dung: {num_colors}")
    print("Ket qua to mau:")
    for region in REGIONS:
        c_idx = coloring[region] - 1
        c_name = COLOR_NAMES[c_idx] if c_idx < len(COLOR_NAMES) else f"Màu {coloring[region]}"
        print(f"- {region:<12s}: mau {coloring[region]} ({c_name})")

    try:
        draw_graph(coloring, num_colors)
    except Exception as e:
        print(f"\nKhông thể vẽ hình (cần cài networkx và matplotlib): {e}")


if __name__ == "__main__":
    main()