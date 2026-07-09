from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from typing import Any


BENCHMARK_VERSION = "sr-benchmark-v0.1"
ALLOWED_EVIDENCE_LEVELS = {"E0", "E1", "E2", "E3", "E4", "E5"}


@dataclass(frozen=True)
class SRBenchmarkInput:
    task_id: str
    evidence_capacity: float
    governance_demand: float
    evidence_level: str = "E0"


@dataclass(frozen=True)
class SRBenchmarkResult:
    benchmark_version: str
    task_id: str
    evidence_capacity: float
    governance_demand: float
    sufficiency_ratio: float
    admissible: bool
    verdict: str
    reason_code: str
    safe_message: str
    evidence_level: str
    non_claims: tuple[str, ...]


def evaluate_sufficiency(data: SRBenchmarkInput) -> SRBenchmarkResult:
    """Evaluate whether a proposed verification task passes the SR gate.

    This benchmark is intentionally minimal. It does not prove that a task is
    safe, correct, or externally validated. It only determines whether the
    supplied evaluator-capacity estimate is at least as large as the supplied
    governance-demand estimate.
    """
    _validate_input(data)

    ratio = data.evidence_capacity / data.governance_demand
    rounded_ratio = round(ratio, 6)
    admissible = ratio >= 1.0

    if admissible:
        verdict = "sufficient"
        reason_code = "sr_sufficient"
        safe_message = "Sufficiency check passed. Verification may proceed under the stated scope."
    else:
        verdict = "insufficient"
        reason_code = "sr_insufficient"
        safe_message = "Sufficiency check failed. Verification is blocked until evaluator capacity improves or governance demand is reduced."

    return SRBenchmarkResult(
        benchmark_version=BENCHMARK_VERSION,
        task_id=data.task_id,
        evidence_capacity=float(data.evidence_capacity),
        governance_demand=float(data.governance_demand),
        sufficiency_ratio=rounded_ratio,
        admissible=admissible,
        verdict=verdict,
        reason_code=reason_code,
        safe_message=safe_message,
        evidence_level=data.evidence_level,
        non_claims=(
            "This result does not validate task correctness.",
            "This result does not grant execution authority by itself.",
            "This result does not raise the evidence level beyond the supplied evidence.",
            "This result is local and not an external review.",
        ),
    )


def result_to_json_safe_dict(result: SRBenchmarkResult) -> dict[str, Any]:
    if type(result) is not SRBenchmarkResult:
        raise TypeError("result must be SRBenchmarkResult")

    data = asdict(result)
    data["non_claims"] = list(result.non_claims)
    return data


def parse_input_file(path: str) -> SRBenchmarkInput:
    with open(path, "r", encoding="utf-8") as handle:
        raw = json.load(handle)

    if type(raw) is not dict:
        raise ValueError("input JSON must be an object")

    return SRBenchmarkInput(
        task_id=raw.get("task_id", "unspecified"),
        evidence_capacity=raw.get("evidence_capacity"),
        governance_demand=raw.get("governance_demand"),
        evidence_level=raw.get("evidence_level", "E0"),
    )


def _validate_input(data: SRBenchmarkInput) -> None:
    if type(data) is not SRBenchmarkInput:
        raise TypeError("data must be SRBenchmarkInput")

    if type(data.task_id) is not str or not data.task_id.strip():
        raise ValueError("task_id must be a non-empty string")

    if type(data.evidence_level) is not str or data.evidence_level not in ALLOWED_EVIDENCE_LEVELS:
        raise ValueError("evidence_level must be one of E0, E1, E2, E3, E4, E5")

    _validate_number("evidence_capacity", data.evidence_capacity)
    _validate_number("governance_demand", data.governance_demand)

    if data.evidence_capacity < 0:
        raise ValueError("evidence_capacity must be greater than or equal to zero")

    if data.governance_demand <= 0:
        raise ValueError("governance_demand must be greater than zero")


def _validate_number(name: str, value: float) -> None:
    if type(value) not in (int, float):
        raise ValueError(f"{name} must be a number")

    if value != value:
        raise ValueError(f"{name} must not be NaN")

    if value in (float("inf"), float("-inf")):
        raise ValueError(f"{name} must be finite")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the AGI Seed Sufficiency Ratio benchmark.")
    parser.add_argument("--input", help="Path to JSON input file.")
    parser.add_argument("--task-id", default="unspecified", help="Task or milestone identifier.")
    parser.add_argument("--evidence-capacity", type=float, help="Evaluator capacity estimate.")
    parser.add_argument("--governance-demand", type=float, help="Governance demand estimate.")
    parser.add_argument("--evidence-level", default="E0", help="Current evidence level: E0 through E5.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.input:
            data = parse_input_file(args.input)
        else:
            data = SRBenchmarkInput(
                task_id=args.task_id,
                evidence_capacity=args.evidence_capacity,
                governance_demand=args.governance_demand,
                evidence_level=args.evidence_level,
            )

        result = evaluate_sufficiency(data)
        payload = result_to_json_safe_dict(result)
    except Exception as exc:
        payload = {
            "benchmark_version": BENCHMARK_VERSION,
            "admissible": False,
            "verdict": "error",
            "reason_code": "sr_input_error",
            "safe_message": "Sufficiency benchmark input was invalid.",
            "error_type": type(exc).__name__,
        }
        sys.stdout.write(json.dumps(payload, ensure_ascii=True, sort_keys=True, separators=(",", ":")))
        sys.stdout.write("\n")
        return 2

    sys.stdout.write(json.dumps(payload, ensure_ascii=True, sort_keys=True, separators=(",", ":")))
    sys.stdout.write("\n")
    return 0 if result.admissible else 1


if __name__ == "__main__":
    raise SystemExit(main())
