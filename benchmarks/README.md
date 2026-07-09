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

## Run from CLI

```bash
python benchmarks/sr_benchmark.py \
  --task-id trial_004 \
  --evidence-capacity 3 \
  --governance-demand 2 \
  --evidence-level E2
```

Example sufficient output:

```json
{
  "admissible": true,
  "reason_code": "sr_sufficient",
  "sufficiency_ratio": 1.5,
  "verdict": "sufficient"
}
```

Example insufficient run:

```bash
python benchmarks/sr_benchmark.py \
  --task-id trial_004 \
  --evidence-capacity 1 \
  --governance-demand 2
```

This exits with code `1` and emits a JSON result with `admissible: false`.

Malformed input exits with code `2`.

## Run from JSON

```json
{
  "task_id": "trial_004",
  "evidence_capacity": 3,
  "governance_demand": 2,
  "evidence_level": "E2"
}
```

```bash
python benchmarks/sr_benchmark.py --input sr_input.json
```

## Evidence Status

Current target: E2 local execution.

This benchmark is a starter implementation. It provides a deterministic gate shape and receipt-friendly output, not a validated scientific measurement model.

## Non-Claims

This benchmark does not claim:

- task correctness
- execution safety
- external validation
- production readiness
- evidence promotion by itself

It only determines whether a proposed verification should be allowed to proceed under the supplied local capacity and demand estimates.
