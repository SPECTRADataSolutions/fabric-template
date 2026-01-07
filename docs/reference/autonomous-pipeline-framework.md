# Autonomous pipeline framework (Zephyr)

Goal: allow Spectra automation to assemble, validate, and schedule the Zephyr pipeline without hand-written glue.

## Building blocks

1. **Contract** – `contract.yaml` defines the upstream interface (auth, endpoints, limits).
2. **Plan** – `source/source.plan.yaml` translates the contract into executable ingestion units and guardrails.
3. **Manifest** – `manifest.json` exposes the same information in the canonical `pipelines[].activities[]` format referenced by SpectraCLI.
4. **Procedures** – `docs/source/procedures.md` ensures human operators follow the same steps automation will execute.

## Automation hooks

- Once SpectraCLI support is wired, `spectra graph` can visualise the Zephyr pipeline straight from the manifest.
- Provisioner / Bootstrapper workflows can read `source.source.plan.yaml` to seed Fabric pipelines with the right cadence + storage paths.
- Future autonomous agents can diff `contract.yaml` vs. live responses and open Jira tickets automatically.

## Roadmap

| Milestone | Description                                                                                     | Target  |
| --------- | ----------------------------------------------------------------------------------------------- | ------- |
| M1        | Validate Source-stage manifest against a dry SpectraCLI run and publish Chronicle evidence.     | 2025-11 |
| M2        | Hook Fabric pipeline templates to read the plan + manifest (no manual cron editing).            | 2025-12 |
| M3        | Extend manifest with `capabilities` metadata similar to Jira to unlock fully autonomous builds. | 2026-01 |

## Contribution guidance

- Keep docs and configs in sync; if a field changes in one artefact, update the others before merging.
- Reference Jira alignment notes whenever a fix originated in the Jira pipeline.
- British English across docs, commit messages, and PR descriptions.
