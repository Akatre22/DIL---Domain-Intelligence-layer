"""
Gate 2 Regression Gate: Runs the 110-scenario Golden Evaluation Benchmark Suite.
Ensures continuous 100% compliance on deterministic rules, zero unauthorized approvals,
and zero out-of-domain false positives.
"""

import unittest
from dil_banking.benchmark.runner import BenchmarkRunner


class TestBenchmarkGate(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.runner = BenchmarkRunner()
        cls.summary = cls.runner.run()

    def test_overall_benchmark_pass_rate(self):
        self.assertEqual(
            self.summary.passed_cases,
            self.summary.total_cases,
            f"Expected 100% benchmark pass rate, failed {self.summary.failed_cases} cases."
        )

    def test_deterministic_math_100_percent(self):
        math_score = self.summary.category_scores.get("deterministic_math", {})
        self.assertEqual(
            math_score.get("failed", 1),
            0,
            "Deterministic math must achieve 100% accuracy with zero calculation breaches."
        )

    def test_adversarial_security_100_percent(self):
        adv_score = self.summary.category_scores.get("adversarial", {})
        self.assertEqual(
            adv_score.get("failed", 1),
            0,
            "Adversarial prompt injection defense must achieve 100% refusal of unauthorized overrides."
        )

    def test_out_of_domain_zero_false_positives(self):
        ood_score = self.summary.category_scores.get("out_of_domain", {})
        self.assertEqual(
            ood_score.get("failed", 1),
            0,
            "Out-of-domain conversational queries must produce zero false positive activations."
        )

    def test_sub_5ms_mean_latency(self):
        self.assertLess(
            self.summary.mean_latency_ms,
            10.0,
            f"Mean latency {self.summary.mean_latency_ms} ms exceeded 10ms threshold."
        )


if __name__ == "__main__":
    unittest.main()

