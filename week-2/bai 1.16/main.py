from __future__ import annotations

from typing import Dict, List, Optional, Set, Tuple


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


def main() -> None:
    num_colors, coloring = find_minimum_coloring()

    print(f"So mau it nhat can dung: {num_colors}")
    print("Ket qua to mau:")
    for region in REGIONS:
        print(f"- {region}: mau {coloring[region]}")


if __name__ == "__main__":
    main()
