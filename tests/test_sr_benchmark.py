import json
import subprocess
import sys
import unittest

from benchmarks.sr_benchmark import (
    DimensionScore,
    SRBenchmarkInput,
    evaluate_sufficiency,
    result_to_json_safe_dict,
)


class SRBenchmarkTests(unittest.TestCase):
    def test_scalar_sufficient_result_is_admissible(self):
        result = evaluate_sufficiency(
            SRBenchmarkInput(
                task_id="trial_004",
                evidence_capacity=3,
                governance_demand=2,
                evidence_level="E2",
            )
        )

        self.assertTrue(result.admissible)
        self.assertEqual(result.mode, "scalar")
        self.assertEqual(result.verdict, "sufficient")
        self.assertEqual(result.reason_code, "sr_sufficient")
        self.assertEqual(result.sufficiency_ratio, 1.5)

    def test_scalar_insufficient_result_blocks_verification(self):
        result = evaluate_sufficiency(
            SRBenchmarkInput(
                task_id="trial_004",
                evidence_capacity=1,
                governance_demand=2,
            )
        )

        self.assertFalse(result.admissible)
        self.assertEqual(result.mode, "scalar")
        self.assertEqual(result.verdict, "insufficient")
        self.assertEqual(result.reason_code, "sr_insufficient")

    def test_multidimensional_sufficient_result_is_admissible(self):
        result = evaluate_sufficiency(
            SRBenchmarkInput(
                task_id="trial_004",
                evidence_level="E2",
                capacity_dimensions=(
                    DimensionScore("domain_expertise", 4, 2),
                    DimensionScore("test_coverage", 3, 1),
                    DimensionScore("replay_support", 5, 1),
                ),
                demand_dimensions=(
                    DimensionScore("semantic_difficulty", 3, 2),
                    DimensionScore("security_sensitivity", 2, 1),
                    DimensionScore("reproducibility_burden", 3, 1),
                ),
            )
        )

        self.assertTrue(result.admissible)
        self.assertEqual(result.mode, "multidimensional")
        self.assertEqual(result.reason_code, "sr_sufficient")
        self.assertGreaterEqual(result.sufficiency_ratio, 1.0)
        self.assertTrue(result.limiting_factors)

    def test_multidimensional_insufficient_result_blocks_verification(self):
        result = evaluate_sufficiency(
            SRBenchmarkInput(
                task_id="trial_004",
                capacity_dimensions=(
                    DimensionScore("domain_expertise", 1, 2),
                    DimensionScore("adversarial_coverage", 1, 1),
                ),
                demand_dimensions=(
                    DimensionScore("semantic_difficulty", 4, 2),
                    DimensionScore("security_sensitivity", 5, 1),
                ),
            )
        )

        self.assertFalse(result.admissible)
        self.assertEqual(result.mode, "multidimensional")
        self.assertEqual(result.reason_code, "sr_insufficient")
        self.assertIn("low_capacity:adversarial_coverage=1", result.limiting_factors)

    def test_zero_governance_demand_is_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_sufficiency(
                SRBenchmarkInput(
                    task_id="bad",
                    evidence_capacity=1,
                    governance_demand=0,
                )
            )

    def test_dimension_score_above_five_is_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_sufficiency(
                SRBenchmarkInput(
                    task_id="bad",
                    capacity_dimensions=(DimensionScore("domain_expertise", 6),),
                    demand_dimensions=(DimensionScore("semantic_difficulty", 2),),
                )
            )

    def test_result_is_json_safe(self):
        result = evaluate_sufficiency(
            SRBenchmarkInput(
                task_id="trial_004",
                evidence_capacity=3,
                governance_demand=2,
            )
        )
        payload = result_to_json_safe_dict(result)

        encoded = json.dumps(payload, ensure_ascii=True, sort_keys=True)
        self.assertIn("sr_sufficient", encoded)
        self.assertIsInstance(payload["non_claims"], list)
        self.assertIsInstance(payload["capacity_dimensions"], list)
        self.assertIsInstance(payload["demand_dimensions"], list)

    def test_cli_returns_zero_for_scalar_sufficient(self):
        proc = subprocess.run(
            [
                sys.executable,
                "benchmarks/sr_benchmark.py",
                "--task-id",
                "trial_004",
                "--evidence-capacity",
                "3",
                "--governance-demand",
                "2",
            ],
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(proc.returncode, 0)
        payload = json.loads(proc.stdout)
        self.assertTrue(payload["admissible"])
        self.assertEqual(payload["mode"], "scalar")

    def test_cli_returns_one_for_scalar_insufficient(self):
        proc = subprocess.run(
            [
                sys.executable,
                "benchmarks/sr_benchmark.py",
                "--task-id",
                "trial_004",
                "--evidence-capacity",
                "1",
                "--governance-demand",
                "2",
            ],
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(proc.returncode, 1)
        payload = json.loads(proc.stdout)
        self.assertFalse(payload["admissible"])
        self.assertEqual(payload["reason_code"], "sr_insufficient")

    def test_cli_multidimensional_mode(self):
        proc = subprocess.run(
            [
                sys.executable,
                "benchmarks/sr_benchmark.py",
                "--task-id",
                "trial_004",
                "--capacity-dim",
                "domain_expertise=4:2",
                "--capacity-dim",
                "replay_support=4:1",
                "--demand-dim",
                "semantic_difficulty=3:1",
                "--demand-dim",
                "security_sensitivity=3:1",
            ],
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(proc.returncode, 0)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["mode"], "multidimensional")
        self.assertTrue(payload["admissible"])
        self.assertTrue(payload["capacity_dimensions"])


if __name__ == "__main__":
    unittest.main()
