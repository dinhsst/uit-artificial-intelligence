# -*- coding: utf-8 -*-
"""Giải bài toán 8-puzzle bằng thuật toán A* với heuristic Manhattan.

Cách dùng:
    python astar_8puzzle.py                     # đọc INPUT.txt, ghi OUTPUT.txt
    python astar_8puzzle.py duong_dan_input.txt
    python astar_8puzzle.py input.txt output.txt

Định dạng tệp đầu vào:
    Dòng 1     : kích thước bàn cờ (chỉ hỗ trợ 3)
    3 dòng sau : trạng thái ban đầu
    3 dòng sau : trạng thái mục tiêu
    Số 0 là ô trống.
"""

from __future__ import annotations

import heapq
import itertools
import sys

SIZE = 3
BLANK = 0
INF = float("inf")

# Nước đi được đặt tên theo hướng di chuyển của Ô TRỐNG.
# (tên tiếng Việt, mã, độ lệch hàng, độ lệch cột)
MOVES = (
    ("Lên", "U", -1, 0),
    ("Xuống", "D", 1, 0),
    ("Trái", "L", 0, -1),
    ("Phải", "R", 0, 1),
)


class InputError(Exception):
    """Dữ liệu đầu vào không hợp lệ."""


class Solution:
    """Kết quả tìm kiếm của A*."""

    def __init__(self, path, expanded, generated):
        self.path = path            # [(state, tên nước đi, mã nước đi), ...]
        self.expanded = expanded    # số nút đã mở rộng
        self.generated = generated  # số nút đã sinh

    @property
    def moves(self):
        return len(self.path) - 1




def parse_state(rows, label):
    """Chuyển ba dòng số thành tuple và kiểm tra hoán vị 0..8."""
    values = []
    for row_number, row in enumerate(rows, start=1):
        parts = row.split()
        if len(parts) != SIZE:
            raise InputError(
                f"{label}: dòng {row_number} phải có đúng {SIZE} số."
            )
        try:
            values.extend(int(part) for part in parts)
        except ValueError as exc:
            raise InputError(f"{label}: tất cả ô phải là số nguyên.") from exc

    expected = set(range(SIZE * SIZE))
    if set(values) != expected or len(values) != len(expected):
        raise InputError(f"{label}: phải chứa mỗi số từ 0 đến 8 đúng một lần.")
    return tuple(values)


def read_input(filename):
    """Đọc INPUT.txt theo định dạng của đề."""
    try:
        with open(filename, "r", encoding="utf-8-sig") as file:
            lines = [line.strip() for line in file if line.strip()]
    except OSError as exc:
        raise InputError(f"Không thể đọc tệp '{filename}': {exc}") from exc

    if len(lines) < 7:
        raise InputError("Tệp input phải có 7 dòng không rỗng.")
    try:
        size = int(lines[0])
    except ValueError as exc:
        raise InputError("Dòng đầu tiên phải là kích thước bàn cờ.") from exc
    if size != SIZE:
        raise InputError("Chương trình hiện chỉ hỗ trợ bàn cờ 3 x 3.")
    return parse_state(lines[1:4], "Trạng thái đầu"), parse_state(
        lines[4:7], "Trạng thái đích"
    )


def inversion_count(state):
    """Đếm số nghịch thế, không tính ô trống."""
    tiles = [tile for tile in state if tile != BLANK]
    return sum(
        tiles[i] > tiles[j]
        for i in range(len(tiles))
        for j in range(i + 1, len(tiles))
    )


def is_solvable(start, goal):
    """Với bàn 3x3, hai trạng thái khả biến đổi khi parity giống nhau."""
    return inversion_count(start) % 2 == inversion_count(goal) % 2


def manhattan(state, goal_positions):
    """Tổng khoảng cách Manhattan của các quân, bỏ qua ô trống."""
    distance = 0
    for index, tile in enumerate(state):
        if tile == BLANK:
            continue
        row, col = divmod(index, SIZE)
        goal_row, goal_col = goal_positions[tile]
        distance += abs(row - goal_row) + abs(col - goal_col)
    return distance


def neighbors(state):
    """Sinh các trạng thái kế tiếp theo thứ tự U, D, L, R."""
    blank_index = state.index(BLANK)
    blank_row, blank_col = divmod(blank_index, SIZE)
    for vietnamese, code, delta_row, delta_col in MOVES:
        row = blank_row + delta_row
        col = blank_col + delta_col
        if not (0 <= row < SIZE and 0 <= col < SIZE):
            continue
        swap_index = row * SIZE + col
        next_state = list(state)
        next_state[blank_index], next_state[swap_index] = (
            next_state[swap_index],
            next_state[blank_index],
        )
        yield tuple(next_state), vietnamese, code


def reconstruct_path(goal, parents):
    """Truy vết về trạng thái đầu; phần tử đầu không có nước đi."""
    reversed_path = []
    current = goal
    while current is not None:
        parent, vietnamese, code = parents[current]
        reversed_path.append((current, vietnamese, code))
        current = parent
    reversed_path.reverse()
    return reversed_path


def a_star(start, goal):
    """Tìm đường đi tối ưu bằng A* graph search."""
    goal_positions = {
        tile: divmod(index, SIZE) for index, tile in enumerate(goal)
    }
    counter = itertools.count()
    start_h = manhattan(start, goal_positions)
    open_set = [(start_h, 0, next(counter), start)]
    best_g = {start: 0}
    parents = {start: (None, None, None)}
    expanded = 0
    generated = 1

    while open_set:
        f_score, g_score, _, state = heapq.heappop(open_set)
        # Bỏ qua bản ghi cũ của cùng một trạng thái.
        if g_score != best_g.get(state, INF):
            continue
        if state == goal:
            return Solution(reconstruct_path(state, parents), expanded, generated)

        expanded += 1
        for next_state, vietnamese, code in neighbors(state):
            next_g = g_score + 1
            if next_g >= best_g.get(next_state, INF):
                continue
            best_g[next_state] = next_g
            parents[next_state] = (state, vietnamese, code)
            next_h = manhattan(next_state, goal_positions)
            heapq.heappush(
                open_set, (next_g + next_h, next_g, next(counter), next_state)
            )
            generated += 1

    return None


def format_board(state):
    return "\n".join(
        " ".join(str(value) for value in state[row * SIZE : (row + 1) * SIZE])
        for row in range(SIZE)
    )


def format_solution(start, goal, solution):
    """Tạo nội dung OUTPUT.txt bằng UTF-8."""
    goal_positions = {tile: divmod(index, SIZE) for index, tile in enumerate(goal)}
    lines = [
        "8-PUZZLE - THUAT TOAN A*",
        "",
        "TRANG THAI BAN DAU:",
        format_board(start),
        "",
        "TRANG THAI MUC TIEU:",
        format_board(goal),
        "",
    ]
    for step, (state, vietnamese, code) in enumerate(solution.path):
        if step == 0:
            lines.append("BUOC 0 - TRANG THAI BAN DAU")
        else:
            lines.append(f"BUOC {step} - DI CHUYEN: {vietnamese} ({code})")
        g_score = step
        h_score = manhattan(state, goal_positions)
        lines.extend([format_board(state), f"g={g_score}, h={h_score}, f={g_score + h_score}", ""])

    lines.extend(
        [
            "DA TIM THAY LOI GIAI.",
            f"SO BUOC DI CHUYEN: {solution.moves}",
            f"CHI PHI: {solution.moves}",
            f"SO NUT DA MO RONG: {solution.expanded}",
            f"SO NUT DA SINH: {solution.generated}",
            "",
            "Quy uoc: U=Len, D=Xuong, L=Trai, R=Phai (huong di chuyen cua o trong).",
        ]
    )
    return "\n".join(lines) + "\n"


def write_text(filename, content):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    input_file = argv[0] if len(argv) >= 1 else "INPUT.txt"
    output_file = argv[1] if len(argv) >= 2 else "OUTPUT.txt"
    if len(argv) > 2:
        print("Cách dùng: python astar_8puzzle.py [INPUT.txt] [OUTPUT.txt]", file=sys.stderr)
        return 2

    try:
        start, goal = read_input(input_file)
        if not is_solvable(start, goal):
            message = (
                "8-PUZZLE - THUAT TOAN A*\n\n"
                "KHONG CO LOI GIAI: hai trang thai khac parity nghich the.\n"
            )
            write_text(output_file, message)
            print(message, end="")
            return 0

        solution = a_star(start, goal)
        if solution is None:
            message = "KHONG TIM THAY LOI GIAI.\n"
            write_text(output_file, message)
            print(message, end="")
            return 0

        content = format_solution(start, goal, solution)
        write_text(output_file, content)
        print(content, end="")
        return 0
    except (InputError, OSError) as exc:
        print(f"LOI: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
