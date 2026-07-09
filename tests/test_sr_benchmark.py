import json
import subprocess
import sys
import unittest

from benchmarks.sr_benchmark import (
    SRBenchmarkInput,
    evaluate_sufficiency,
    result_to_json_safe_dict,
)


class SRBenchmarkTests(unittest.TestCase):
    def test_sufficient_result_is_admissible(self):
        result = evaluate_sufficiency(
            SRBenchmarkInput(
                task_id="trial_004",
                evidence_capacity=3,
                governance_demand=2,
                evidence_level="E2",
            )
        )

        self.assertTrue(result.admissible)
        self.assertEqual(result.verdict, "sufficient")
        self.assertEqual(result.reason_code, "sr_sufficient")
        self.assertEqual(result.sufficiency_ratio, 1.5)

    def test_insufficient_result_blocks_verification(self):
        result = evaluate_sufficiency(
            SRBenchmarkInput(
                task_id="trial_004",
                evidence_capacity=1,
                governance_demand=2,
            )
        )

        self.assertFalse(result.admissible)
        self.assertEqual(result.verdict, "insufficient")
        self.assertEqual(result.reason_code, "sr_insufficient")

    def test_zero_governance_demand_is_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_sufficiency(
                SRBenchmarkInput(
                    task_id="bad",
                    evidence_capacity=1,
                    governance_demand=0,
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

    def test_cli_returns_zero_for_sufficient(self):
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

    def test_cli_returns_one_for_insufficient(self):
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


if __name__ == "__main__":
    unittest.main()
