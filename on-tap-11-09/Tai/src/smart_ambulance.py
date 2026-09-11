"""Bài 1: định tuyến xe cứu thương bằng A* và Dijkstra."""
from __future__ import annotations

import heapq
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


@dataclass(frozen=True)
class Edge:
    start: str
    end: str
    base_minutes: float
    traffic_factor: float

    @property
    def cost(self) -> float:
        return self.base_minutes * self.traffic_factor


@dataclass
class PathResult:
    path: List[str]
    cost: float
    expanded: int


class CityMap:
    def __init__(self, nodes: Dict[str, List[float]], edges: Iterable[Edge]):
        self.nodes = {str(k): (float(v[0]), float(v[1])) for k, v in nodes.items()}
        self.edges = list(edges)
        self.adjacency: Dict[str, List[Tuple[str, float]]] = {
            node: [] for node in self.nodes
        }
        for edge in self.edges:
            self.adjacency[edge.start].append((edge.end, edge.cost))
            self.adjacency[edge.end].append((edge.start, edge.cost))

    @classmethod
    def from_json(cls, path: str | Path) -> "CityMap":
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
        edges = [
            Edge(
                start=item["from"],
                end=item["to"],
                base_minutes=float(item["base_minutes"]),
                traffic_factor=float(item["traffic_factor"]),
            )
            for item in raw["edges"]
        ]
        return cls(raw["nodes"], edges)

    def apply_accident(self, node: str, multiplier: float = 5.0) -> None:
        """Tăng chi phí các đường kề nút gặp sự cố và xây lại danh sách kề."""
        updated = []
        for edge in self.edges:
            if edge.start == node or edge.end == node:
                updated.append(
                    Edge(edge.start, edge.end, edge.base_minutes, edge.traffic_factor * multiplier)
                )
            else:
                updated.append(edge)
        self.edges = updated
        self.adjacency = {key: [] for key in self.nodes}
        for edge in self.edges:
            self.adjacency[edge.start].append((edge.end, edge.cost))
            self.adjacency[edge.end].append((edge.start, edge.cost))

    def _heuristic_scale(self) -> float:
        ratios = []
        for edge in self.edges:
            distance = math.dist(self.nodes[edge.start], self.nodes[edge.end])
            if distance > 0:
                ratios.append(edge.cost / distance)
        return min(ratios) if ratios else 0.0

    def heuristic(self, node: str, goal: str) -> float:
        return math.dist(self.nodes[node], self.nodes[goal]) * self._heuristic_scale()

    def shortest_path(self, start: str, goal: str, use_heuristic: bool) -> PathResult:
        queue = [(self.heuristic(start, goal) if use_heuristic else 0.0, 0.0, start)]
        distances = {start: 0.0}
        previous: Dict[str, str] = {}
        expanded = 0
        while queue:
            _, cost_so_far, current = heapq.heappop(queue)
            if cost_so_far > distances.get(current, math.inf) + 1e-9:
                continue
            expanded += 1
            if current == goal:
                break
            for neighbor, edge_cost in self.adjacency[current]:
                candidate = cost_so_far + edge_cost
                if candidate < distances.get(neighbor, math.inf):
                    distances[neighbor] = candidate
                    previous[neighbor] = current
                    priority = candidate + (self.heuristic(neighbor, goal) if use_heuristic else 0.0)
                    heapq.heappush(queue, (priority, candidate, neighbor))
        if goal not in distances:
            raise ValueError(f"Không có đường đi từ {start} đến {goal}")
        path = [goal]
        while path[-1] != start:
            path.append(previous[path[-1]])
        path.reverse()
        return PathResult(path, distances[goal], expanded)

    def astar(self, start: str, goal: str) -> PathResult:
        return self.shortest_path(start, goal, use_heuristic=True)

    def dijkstra(self, start: str, goal: str) -> PathResult:
        return self.shortest_path(start, goal, use_heuristic=False)


def load_default_map() -> CityMap:
    return CityMap.from_json(Path(__file__).resolve().parent.parent / "data" / "city_map.json")


def format_result(label: str, result: PathResult) -> str:
    return f"{label}: {' -> '.join(result.path)} | {result.cost:.2f} phút | mở rộng {result.expanded} nút"


def run_demo() -> str:
    city = load_default_map()
    before_astar = city.astar("1", "15")
    before_dijkstra = city.dijkstra("1", "15")
    city.apply_accident("7", multiplier=5.0)
    after_astar = city.astar("1", "15")
    lines = [
        "BÀI 1 - ĐỊNH TUYẾN XE CỨU THƯƠNG",
        format_result("A* trước sự cố", before_astar),
        format_result("Dijkstra trước sự cố", before_dijkstra),
        "Sự kiện: nút 7 xảy ra tai nạn, chi phí các cạnh kề nút tăng 5 lần.",
        format_result("A* sau sự cố", after_astar),
        f"Kiểm tra chi phí A* = Dijkstra: {before_astar.cost:.2f} = {before_dijkstra.cost:.2f}",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(run_demo())
