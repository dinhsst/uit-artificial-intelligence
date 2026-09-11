import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from smart_ambulance import load_default_map
from admission_expert import (
    Candidate,
    build_llm_context,
    build_rules,
    build_semantic_network,
    infer,
    validate_recommendations,
)


class SmartAmbulanceTests(unittest.TestCase):
    def setUp(self):
        self.city = load_default_map()

    def test_map_size_and_connected_route(self):
        self.assertGreaterEqual(len(self.city.nodes), 15)
        self.assertGreaterEqual(len(self.city.edges), 25)
        result = self.city.astar("1", "15")
        self.assertEqual(result.path[0], "1")
        self.assertEqual(result.path[-1], "15")
        self.assertGreater(result.cost, 0)

    def test_astar_has_same_optimal_cost_as_dijkstra(self):
        astar = self.city.astar("1", "15")
        dijkstra = self.city.dijkstra("1", "15")
        self.assertAlmostEqual(astar.cost, dijkstra.cost, places=7)

    def test_accident_changes_route_or_cost(self):
        before = self.city.astar("1", "15")
        self.city.apply_accident("7", 5)
        after = self.city.astar("1", "15")
        self.assertTrue(after.cost != before.cost or after.path != before.path)


class AdmissionExpertTests(unittest.TestCase):
    def test_at_least_ten_rules_and_semantic_relations(self):
        self.assertGreaterEqual(len(build_rules()), 10)
        self.assertGreaterEqual(len(build_semantic_network()), 20)

    def test_threshold_rule_is_inclusive(self):
        candidate = Candidate("X", 8.0, 7.5, 5, 5, 5, 5, 5, (), "khác")
        codes = {rule.code for rule in infer(candidate)}
        self.assertIn("R01", codes)

    def test_hallucination_is_rejected(self):
        candidate = Candidate("Y", 8.0, 7.5, 5, 5, 5, 5, 5, (), "khác")
        valid, invalid = validate_recommendations(candidate, ["Khoa học máy tính", "Y học"])
        self.assertFalse(valid)
        self.assertEqual(invalid, ["Y học"])

    def test_context_contains_required_marker_and_rules(self):
        candidate = Candidate("X", 8, 8, 8, 8, 8, 8, 8, (), "khác")
        context = build_llm_context(candidate)
        self.assertIn("Hà Nội và Tp.HCM ở Pháp.", context)
        self.assertIn("R01", context)


if __name__ == "__main__":
    unittest.main()
