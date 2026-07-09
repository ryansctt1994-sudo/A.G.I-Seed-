# Security Policy

AGI Seed is a research prototype for governed agentic software modification. Security reports are welcome, especially reports involving execution boundaries, model-facing feedback, receipts, replay, sandboxing, and authority escalation.

## Supported Versions

The repository is currently pre-release.

| Version | Status |
|---|---|
| v0.3.1-rc1 | Research architecture, active |
| earlier | Reference only |

No version is currently production-supported.

## Current Security Posture

AGI Seed should be treated as an experimental research system.

It does not currently claim:

- production sandbox escape resistance
- general autonomous coding safety
- externally validated governance effectiveness
- operational deployment readiness

The current security goal is narrower:

> Preserve deterministic boundaries between untrusted model proposals, verification machinery, execution environments, receipts, replay artifacts, and model-facing feedback.

## Reportable Issues

Please report issues involving:

- direct or indirect authority escalation
- execution outside the governed corridor
- unsafe file writes or path traversal
- sandbox escape or weakened sandbox configuration
- network access where none is expected
- model exposure to raw logs, stack traces, workspace paths, patch contents, or host paths
- receipt tampering or missing receipts
- replay non-determinism
- evidence promotion without validation
- bypass of sufficiency checks
- unsafe reflection memory behavior

## Non-Security Issues

General documentation edits, roadmap disagreements, speculative architecture discussion, and ordinary bugs may be filed as normal issues.

## Disclosure Process

If you believe you have found a security issue, please avoid public exploit details until it has been reviewed.

Preferred report contents:

- summary
- affected component
- reproduction steps
- expected behavior
- observed behavior
- whether model-facing information leaks
- whether authority boundaries are crossed
- suggested mitigation, if known

## Security Review Criteria

Security-sensitive changes should be reviewed against these questions:

1. Does this increase model authority?
2. Does this create a new execution path?
3. Does this bypass schema, policy, sufficiency, verification, receipt, replay, or witness gates?
4. Does this leak internal machinery into model context?
5. Does this make evidence promotion easier without raising evidence?
6. Does this preserve fail-closed behavior?

## Responsible Research Boundary

Do not run untrusted code against production systems, private infrastructure, sensitive files, or real user data using this project.

Do not treat the current sandbox model as a production security boundary.

Do not use this repository to justify deployment claims without independent reproduction and external review.

## Final Principle

Security in AGI Seed is not a single wall.

It is a chain of bounded transitions: proposal, sufficiency, verification, receipt, replay, witness, challenge, and promotion.

A break in any transition is worth reporting.
