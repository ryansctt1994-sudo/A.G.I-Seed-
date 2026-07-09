from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from typing import Any


BENCHMARK_VERSION = "sr-benchmark-v0.2"
ALLOWED_EVIDENCE_LEVELS = {"E0", "E1", "E2", "E3", "E4", "E5"}
MAX_DIMENSION_SCORE = 5.0


@dataclass(frozen=True)
class DimensionScore:
    name: str
    score: float
    weight: float = 1.0
    rationale: str = ""


@dataclass(frozen=True)
class SRBenchmarkInput:
    task_id: str
    evidence_capacity: float | None = None
    governance_demand: float | None = None
    evidence_level: str = "E0"
    capacity_dimensions: tuple[DimensionScore, ...] = ()
    demand_dimensions: tuple[DimensionScore, ...] = ()


@dataclass(frozen=True)
class SRBenchmarkResult:
    benchmark_version: str
    task_id: str
    mode: str
    evidence_capacity: float
    governance_demand: float
    sufficiency_ratio: float
    admissible: bool
    verdict: str
    reason_code: str
    safe_message: str
    evidence_level: str
    capacity_dimensions: tuple[DimensionScore, ...]
    demand_dimensions: tuple[DimensionScore, ...]
    limiting_factors: tuple[str, ...]
    non_claims: tuple[str, ...]


def evaluate_sufficiency(data: SRBenchmarkInput) -> SRBenchmarkResult:
    """Evaluate whether a proposed verification task passes the SR gate.

    The benchmark supports two modes:

    - scalar mode: compare one evaluator-capacity value against one governance-demand value
    - multidimensional mode: compare weighted capacity dimensions against weighted demand dimensions

    This does not prove task correctness, safety, or external validation. It only determines whether the supplied local evaluator capacity is at least as large as the supplied local governance demand.
    """
    _validate_input(data)

    mode = _select_mode(data)
    if mode == "multidimensional":
        evidence_capacity = _weighted_score(data.capacity_dimensions)
        governance_demand = _weighted_score(data.demand_dimensions)
        limiting_factors = _limiting_factors(data.capacity_dimensions, data.demand_dimensions)
    else:
        evidence_capacity = float(data.evidence_capacity)
        governance_demand = float(data.governance_demand)
        limiting_factors = ()

    ratio = evidence_capacity / governance_demand
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
        mode=mode,
        evidence_capacity=round(evidence_capacity, 6),
        governance_demand=round(governance_demand, 6),
        sufficiency_ratio=rounded_ratio,
        admissible=admissible,
        verdict=verdict,
        reason_code=reason_code,
        safe_message=safe_message,
        evidence_level=data.evidence_level,
        capacity_dimensions=data.capacity_dimensions if mode == "multidimensional" else (),
        demand_dimensions=data.demand_dimensions if mode == "multidimensional" else (),
        limiting_factors=limiting_factors,
        non_claims=(
            "This result does not validate task correctness.",
            "This result does not grant execution authority by itself.",
            "This result does not raise the evidence level beyond the supplied evidence.",
            "This result is local and not an external review.",
            "Dimension scores are governance estimates and require calibration before scientific use.",
        ),
    )


def result_to_json_safe_dict(result: SRBenchmarkResult) -> dict[str, Any]:
    if type(result) is not SRBenchmarkResult:
        raise TypeError("result must be SRBenchmarkResult")

    data = asdict(result)
    data["capacity_dimensions"] = [asdict(item) for item in result.capacity_dimensions]
    data["demand_dimensions"] = [asdict(item) for item in result.demand_dimensions]
    data["limiting_factors"] = list(result.limiting_factors)
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
        capacity_dimensions=_parse_dimension_list(raw.get("capacity_dimensions", []), "capacity_dimensions"),
        demand_dimensions=_parse_dimension_list(raw.get("demand_dimensions", []), "demand_dimensions"),
    )


def parse_dimension_spec(spec: str) -> DimensionScore:
    """Parse CLI dimension syntax: name=score or name=score:weight."""
    if type(spec) is not str or "=" not in spec:
        raise ValueError("dimension must use name=score or name=score:weight")

    name, raw_value = spec.split("=", 1)
    name = name.strip()
    if not name:
        raise ValueError("dimension name must be non-empty")

    if ":" in raw_value:
        raw_score, raw_weight = raw_value.split(":", 1)
        weight = float(raw_weight)
    else:
        raw_score = raw_value
        weight = 1.0

    return DimensionScore(name=name, score=float(raw_score), weight=weight)


def _parse_dimension_list(raw: Any, field_name: str) -> tuple[DimensionScore, ...]:
    if raw is None:
        return ()

    if type(raw) is not list:
        raise ValueError(f"{field_name} must be a list")

    dimensions: list[DimensionScore] = []
    for item in raw:
        if type(item) is not dict:
            raise ValueError(f"{field_name} entries must be objects")

        dimensions.append(
            DimensionScore(
                name=item.get("name"),
                score=item.get("score"),
                weight=item.get("weight", 1.0),
                rationale=item.get("rationale", ""),
            )
        )

    return tuple(dimensions)


def _validate_input(data: SRBenchmarkInput) -> None:
    if type(data) is not SRBenchmarkInput:
        raise TypeError("data must be SRBenchmarkInput")

    if type(data.task_id) is not str or not data.task_id.strip():
        raise ValueError("task_id must be a non-empty string")

    if type(data.evidence_level) is not str or data.evidence_level not in ALLOWED_EVIDENCE_LEVELS:
        raise ValueError("evidence_level must be one of E0, E1, E2, E3, E4, E5")

    mode = _select_mode(data)
    if mode == "scalar":
        _validate_number("evidence_capacity", data.evidence_capacity)
        _validate_number("governance_demand", data.governance_demand)

        if data.evidence_capacity < 0:
            raise ValueError("evidence_capacity must be greater than or equal to zero")

        if data.governance_demand <= 0:
            raise ValueError("governance_demand must be greater than zero")
    else:
        _validate_dimensions("capacity_dimensions", data.capacity_dimensions)
        _validate_dimensions("demand_dimensions", data.demand_dimensions)


def _select_mode(data: SRBenchmarkInput) -> str:
    has_dimensions = bool(data.capacity_dimensions or data.demand_dimensions)
    has_scalar = data.evidence_capacity is not None or data.governance_demand is not None

    if has_dimensions:
        if not data.capacity_dimensions or not data.demand_dimensions:
            raise ValueError("multidimensional mode requires both capacity_dimensions and demand_dimensions")
        return "multidimensional"

    if has_scalar:
        return "scalar"

    raise ValueError("input must provide scalar values or multidimensional values")


def _validate_dimensions(field_name: str, dimensions: tuple[DimensionScore, ...]) -> None:
    if type(dimensions) is not tuple or not dimensions:
        raise ValueError(f"{field_name} must be a non-empty tuple")

    seen_names: set[str] = set()
    for item in dimensions:
        if type(item) is not DimensionScore:
            raise ValueError(f"{field_name} entries must be DimensionScore")

        if type(item.name) is not str or not item.name.strip():
            raise ValueError("dimension name must be a non-empty string")

        if item.name in seen_names:
            raise ValueError(f"duplicate dimension name: {item.name}")
        seen_names.add(item.name)

        if type(item.rationale) is not str:
            raise ValueError("dimension rationale must be a string")

        _validate_number("dimension score", item.score)
        _validate_number("dimension weight", item.weight)

        if item.score < 0 or item.score > MAX_DIMENSION_SCORE:
            raise ValueError("dimension score must be between 0 and 5")

        if item.weight <= 0:
            raise ValueError("dimension weight must be greater than zero")


def _weighted_score(dimensions: tuple[DimensionScore, ...]) -> float:
    weighted_sum = sum(item.score * item.weight for item in dimensions)
    total_weight = sum(item.weight for item in dimensions)
    return weighted_sum / total_weight


def _limiting_factors(
    capacity_dimensions: tuple[DimensionScore, ...],
    demand_dimensions: tuple[DimensionScore, ...],
) -> tuple[str, ...]:
    low_capacity = sorted(capacity_dimensions, key=lambda item: (item.score, -item.weight, item.name))[:3]
    high_demand = sorted(demand_dimensions, key=lambda item: (-item.score, -item.weight, item.name))[:3]

    factors = [f"low_capacity:{item.name}={round(item.score, 6)}" for item in low_capacity]
    factors.extend(f"high_demand:{item.name}={round(item.score, 6)}" for item in high_demand)
    return tuple(factors)


def _validate_number(name: str, value: Any) -> None:
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
    parser.add_argument("--evidence-capacity", type=float, help="Scalar evaluator capacity estimate.")
    parser.add_argument("--governance-demand", type=float, help="Scalar governance demand estimate.")
    parser.add_argument("--evidence-level", default="E0", help="Current evidence level: E0 through E5.")
    parser.add_argument(
        "--capacity-dim",
        action="append",
        default=[],
        help="Capacity dimension as name=score or name=score:weight. May be repeated.",
    )
    parser.add_argument(
        "--demand-dim",
        action="append",
        default=[],
        help="Demand dimension as name=score or name=score:weight. May be repeated.",
    )
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
                capacity_dimensions=tuple(parse_dimension_spec(item) for item in args.capacity_dim),
                demand_dimensions=tuple(parse_dimension_spec(item) for item in args.demand_dim),
            )

        result = evaluate_sufficiency(data)
        payload = result_to_json_safe_dict(result)
    except Exception as exc:
        payload = {
            "benchmark_version": BENCHMARK_VERSION,
            "admissible": False,
            "verdict": "error",
            "reason_code": "sr_input_error",
            "safe_message": "Sufficiency benchmark input was invalid. Check task id, evidence level, scalar values, or dimension scores.",
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
