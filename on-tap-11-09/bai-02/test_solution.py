import unittest

from solution import (
    Candidate,
    build_llm_context,
    build_rules,
    build_semantic_network,
    infer,
    validate_recommendations,
)


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
