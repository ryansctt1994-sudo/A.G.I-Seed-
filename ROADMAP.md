# AGI Seed Roadmap

This roadmap tracks the current engineering and governance path for AGI Seed.

The roadmap does not raise the evidence level. Evidence only advances through execution, reproduction, external review, or operational adoption.

## Current Status

| Area | Status |
|---|---|
| Constitutional baseline | Frozen |
| Public documentation | Active |
| Governance hygiene | Active |
| Engineering implementation | Starting |
| Highest earned evidence | E2 |
| Independent reproduction | Pending |
| External validation | Pending |
| Deployment | Not authorized |

## Governing Pipeline

```text
Proposal
    ↓
Sufficiency Check
    ↓
Verification
    ↓
Receipt
    ↓
Replay
    ↓
Independent Witness
    ↓
External Challenge
    ↓
Evidence Promotion
```

## Active Milestones

| Priority | Issue | Milestone | Layer | Evidence Target |
|---|---:|---|---|---|
| P0 | #1 | Define and implement SR Benchmark | Layer 1 | E2 |
| P0.5 | #2 | Implement STEP_5_ESCALATION_OPS_PLUS | Layer 2 | E2 |
| P1 | #3 | Execute Trial 004 controlled patch corridor | Layer 2 | E2 |
| P2 | #4 | Build replay capsule for Trial 004 | Layer 2 | E2 to E3 readiness |
| P3 | #5 | Define witness infrastructure | Layer 2 | E3 readiness |
| P4 | #6 | Prepare external challenge package | Layer 3 / 4 | E4 readiness |
| Hygiene | #7 | Verify docs-check GitHub Actions workflow | Layer 4 | no evidence promotion |
| Hygiene | #8 | Add repository roadmap | Layer 4 | no evidence promotion |

## Dependency Graph

```text
Documentation Baseline
    ↓
Docs CI Verification
    ↓
SR Benchmark
    ↓
Sufficiency Lock
    ↓
STEP_5_ESCALATION_OPS_PLUS
    ↓
Trial 004 Controlled Patch Corridor
    ↓
Replay Capsule
    ↓
Witness Infrastructure
    ↓
External Challenge
    ↓
Evidence Promotion
```

## Immediate Next Step

The next substantive engineering milestone is **P0: Define and implement SR Benchmark**.

Reason:

The constitutional baseline requires sufficiency before verification. Trial 004 should not become the first code milestone until the repository has a minimal way to express whether a verification task is admissible.

## Guardrails

Do not claim:

- AGI
- production readiness
- autonomous software engineering
- external validation
- general code-editing safety

Do claim:

> AGI Seed is a research prototype for governed agentic software modification built around deterministic execution mediation, receipt-gated promotion, sufficiency checks, and constitutional separation between reasoning and authority.

## Review Cadence

Update this roadmap when:

- an issue is closed
- a replay capsule is produced
- an independent witness reproduces a result
- an external reviewer submits findings
- the evidence level changes through admissible evidence
