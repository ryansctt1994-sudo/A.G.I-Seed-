# SR Benchmark

The Sufficiency Ratio benchmark is the first executable Layer 1 measurement tool in the AGI Seed portfolio.

It asks a narrow question:

> Is the current evaluator capacity sufficient for the governance demand of this proposed verification?

It does not prove task correctness, safety, deployment readiness, or external validation.

## Formula

```text
SR = E / G
```

Where:

- `E` is evaluator capacity.
- `G` is governance demand.

Verification is admissible only when:

```text
SR >= 1
```

## Modes

### Scalar mode

Scalar mode compares one evaluator-capacity value against one governance-demand value.

```bash
python benchmarks/sr_benchmark.py \
  --task-id trial_004 \
  --evidence-capacity 3 \
  --governance-demand 2 \
  --evidence-level E2
```

### Multidimensional mode

Multidimensional mode compares weighted capacity dimensions against weighted demand dimensions.

Dimension syntax:

```text
name=score
name=score:weight
```

Scores must be between `0` and `5`. Weights must be greater than `0`.

Example:

```bash
python benchmarks/sr_benchmark.py \
  --task-id trial_004 \
  --evidence-level E2 \
  --capacity-dim domain_expertise=4:2 \
  --capacity-dim test_coverage=3:1 \
  --capacity-dim replay_support=5:1 \
  --demand-dim semantic_difficulty=3:2 \
  --demand-dim security_sensitivity=2:1 \
  --demand-dim reproducibility_burden=3:1
```

Example output fields:

```json
{
  "admissible": true,
  "mode": "multidimensional",
  "reason_code": "sr_sufficient",
  "sufficiency_ratio": 1.454545,
  "verdict": "sufficient"
}
```

## Exit Codes

```text
0 = sufficient, verification may proceed under the stated scope
1 = insufficient, verification is blocked
2 = malformed input
```

## Run from JSON

Scalar input:

```json
{
  "task_id": "trial_004",
  "evidence_capacity": 3,
  "governance_demand": 2,
  "evidence_level": "E2"
}
```

Multidimensional input:

```json
{
  "task_id": "trial_004",
  "evidence_level": "E2",
  "capacity_dimensions": [
    {"name": "domain_expertise", "score": 4, "weight": 2},
    {"name": "test_coverage", "score": 3, "weight": 1},
    {"name": "replay_support", "score": 5, "weight": 1}
  ],
  "demand_dimensions": [
    {"name": "semantic_difficulty", "score": 3, "weight": 2},
    {"name": "security_sensitivity", "score": 2, "weight": 1},
    {"name": "reproducibility_burden", "score": 3, "weight": 1}
  ]
}
```

```bash
python benchmarks/sr_benchmark.py --input sr_input.json
```

## Suggested Dimension Families

Evaluator capacity examples:

- domain expertise
- test coverage
- adversarial coverage
- replay support
- historical calibration
- tool reliability

Governance demand examples:

- semantic difficulty
- security sensitivity
- reproducibility burden
- authority impact
- ambiguity level
- external dependency risk

These dimensions are governance estimates. They must be calibrated before they can be treated as scientific measurements.

## Evidence Status

Current target: E2 local execution.

This benchmark provides a deterministic gate shape and receipt-friendly output, not a validated scientific measurement model.

## Non-Claims

This benchmark does not claim:

- task correctness
- execution safety
- external validation
- production readiness
- evidence promotion by itself
- scientific validity of the dimension weights

It only determines whether a proposed verification should be allowed to proceed under the supplied local capacity and demand estimates.
