# A.G.I-Seed-

## AGI Seed Constitutional Research Portfolio

**Status:** Research prototype • Constitutional baseline frozen • Engineering active • External validation pending

AGI Seed is a research project for governed agentic software modification. It is designed around a strict separation between **reasoning** and **authority**: models may propose, but deterministic governance decides what can be executed, verified, replayed, witnessed, and promoted.

This repository currently serves as the public home for the unified AGI Seed governance and engineering architecture.

## Start Here

Read the current master handoff:

- [AGI Seed Unified Master Handoff](docs/AGI_SEED_UNIFIED_MASTER_HANDOFF.md)

That document is the current source of truth for the portfolio architecture, evidence ladder, governance invariants, AGI Seed v0.3.1-rc1 corridor, and non-claims.

## Core Research Question

> Can an untrusted model improve software through bounded, reproducible, receipt-governed feedback while never controlling execution machinery or promoting its own authority?

AGI Seed is not framed as an autonomous software engineer. It is a governance-first research substrate for studying increasingly capable model behavior under deterministic control.

## Constitutional Principles

The current baseline freezes these invariants:

1. Reasoning never grants authority.
2. Architectural sophistication never raises evidence.
3. Execution machinery remains independent from model intent.
4. Every state transition must be observable.
5. Sufficiency precedes verification.
6. Evidence promotion requires receipts.
7. Governance must itself be reproducible.

## Five-Layer Portfolio Architecture

```text
Layer 4: Portfolio Governance
Layer 3: Constitutional Interpretation
Layer 2: Governance
Layer 1: Measurement
Layer 0: Observation
```

AGI Seed sits primarily in **Layer 2: Governance**, where it operationalizes receipt-gated, sufficiency-gated execution.

## Evidence Ladder

| Level | Meaning |
|---|---|
| E0 | Assertion |
| E1 | Internal coherence |
| E2 | Local execution |
| E3 | Independent reproduction |
| E4 | External review or adversarial validation |
| E5 | Operational adoption |

Current evidence ceiling: **E2** until independent reproduction or external review is completed.

## Current Engineering Focus

The active engineering direction is AGI Seed **v0.3.1-rc1**, a controlled patch corridor for Trial 004.

Planned corridor:

```text
Patch Proposal
    ↓
Syntax Validation
    ↓
Static Invariant Gate
    ↓
Runtime Invariant Runner
    ↓
Ephemeral Workspace
    ↓
Receipt
    ↓
Reflection Buffer
```

The first controlled task is a bounded `bubble_sort(items)` patch trial.

## Immediate Milestones

- SR Benchmark
- STEP_5_ESCALATION_OPS_PLUS
- Trial 004 controlled patch experiment
- Replay capsule
- Witness infrastructure
- External challenge

## Non-Claims

This project does **not** currently claim:

- AGI
- autonomous software engineering
- production readiness
- general code-editing safety
- production sandbox escape resistance
- externally validated governance effectiveness

Correct current description:

> AGI Seed is a research prototype for governed agentic software modification built around deterministic execution mediation, receipt-gated promotion, sufficiency checks, and constitutional separation between reasoning and authority.

## Repository Status

This repository currently contains the constitutional handoff documentation. The implementation modules, tests, replay capsule, CI, and witness artifacts are next engineering milestones.

## License

See [LICENSE](LICENSE).
