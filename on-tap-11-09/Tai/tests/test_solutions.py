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
from historical_guessing import GuessingGame, SemanticNetwork, run_five_games


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


class HistoricalGuessingTests(unittest.TestCase):
    def setUp(self):
        self.network = SemanticNetwork.default()
        self.game = GuessingGame(self.network)

    def test_network_meets_entity_and_relation_requirements(self):
        self.assertGreaterEqual(len(self.network.characters), 10)
        self.assertGreaterEqual(len(self.network.relations), 30)

    def test_question_selection_splits_candidates(self):
        candidates = [character.name for character in self.network.characters]
        question = self.game.choose_question(candidates, set())
        yes = sum(self.network.has_property(name, question) for name in candidates)
        no = len(candidates) - yes
        self.assertGreater(yes, 0)
        self.assertGreater(no, 0)

    def test_five_simulated_games_guess_all_secrets(self):
        results = run_five_games()
        self.assertEqual(len(results), 5)
        self.assertTrue(all(result.guessed == result.secret for result in results))
        self.assertTrue(all(result.questions <= 10 for result in results))


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
