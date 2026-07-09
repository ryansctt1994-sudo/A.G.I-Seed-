# Contributing to AGI Seed

Thank you for helping improve AGI Seed.

This project is a research prototype for governed agentic software modification. Contributions are welcome, but they must preserve the project doctrine: reasoning is not authority, evidence is not rhetoric, and every meaningful transition must be reproducible.

## Source of Truth

Before contributing, read:

- [README.md](README.md)
- [AGI Seed Unified Master Handoff](docs/AGI_SEED_UNIFIED_MASTER_HANDOFF.md)

The handoff document defines the current constitutional baseline.

## Contribution Principles

All contributions should preserve these rules:

1. Do not grant authority to model output directly.
2. Do not raise evidence claims through architecture alone.
3. Do not bypass sufficiency checks, receipts, replay, or review.
4. Do not introduce hidden state transitions.
5. Do not weaken the separation between proposal, verification, execution, and promotion.
6. Do not describe the project as AGI, production-ready, or externally validated unless the evidence ladder supports it.

## Evidence Expectations

Use the project evidence ladder when describing changes:

| Level | Meaning |
|---|---|
| E0 | Assertion |
| E1 | Internal coherence |
| E2 | Local execution |
| E3 | Independent reproduction |
| E4 | External review or adversarial validation |
| E5 | Operational adoption |

A pull request may improve architecture, documentation, or implementation, but it must not claim evidence promotion without receipts, replay, and the required validation stage.

## Preferred Pull Request Structure

Every pull request should include:

- Purpose
- Changed files
- Evidence level claimed
- Tests or checks run
- Known limitations
- Whether authority boundaries changed
- Whether model-facing information changed
- Whether receipts, replay, or witness artifacts are affected

Suggested template:

```markdown
## Purpose

## Changes

## Evidence Level

## Tests / Checks

## Governance Impact

## Security / Safety Impact

## Known Limitations
```

## Code Contributions

For implementation work:

- Keep model output separate from execution machinery.
- Prefer schemas, typed data, and deterministic policy gates.
- Treat all model-generated content as untrusted input.
- Keep raw logs, traces, workspace paths, and execution details out of model-facing feedback.
- Emit receipts for meaningful transitions.
- Fail closed when validation is incomplete or ambiguous.

## Documentation Contributions

Documentation should be clear, evidence-calibrated, and free of hype.

Avoid claims such as:

- production-ready
- autonomous software engineer
- AGI
- fully safe
- externally validated

unless the evidence ladder supports them.

## Security-Sensitive Changes

Changes touching execution, sandboxing, path handling, receipts, model feedback, or authority boundaries require extra review.

Examples:

- command execution
- file writes
- networking
- container configuration
- sandbox limits
- reflection memory
- receipt schemas
- promotion logic

These changes should include explicit threat analysis and failure modes.

## Governance Fidelity

The project target is:

```text
GF = governed authority transitions / all authority transitions = 1.0
```

Any contribution that creates an authority transition outside the governance pipeline should be rejected or redesigned.

## Final Rule

A contribution is not accepted because it is clever.

It is accepted because it is bounded, reviewable, reproducible, and honest about what it proves.
