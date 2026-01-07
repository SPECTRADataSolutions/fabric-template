# Source stage overview

The Source stage captures Zephyr Enterprise data in a predictable, contract-driven manner. It is responsible for:

- Authenticating via API token and respecting the guardrails defined in `contract.yaml`.
- Pulling the four critical object families (projects, releases, cycles, executions) before any Prepare/Extract logic runs.
- Producing evidence that autonomous builders can read (`manifest.json`, `source/source.plan.yaml`, run results).
- Recording Jira alignment notes so parity is maintained across programmes.

## Deliverables

1. **Deep Research Summary** – comprehensive research document (`docs/ZEPHYR-RESEARCH-SUMMARY.md`) following `Core/standards/SOURCE-STAGE-RESEARCH-TEMPLATE.md`. This captures complete understanding of Zephyr architecture, data model, workflows, and relationships.
2. **Contracts** – keep the contract + manifest in sync whenever the vendor changes payloads.
3. **Landing evidence** – raw JSON in Fabric along with watermarks defined in the plan.
4. **Procedures** – follow `docs/source/procedures.md` for every run. Deviations must be documented in the Chronicle.

## Tooling

- SpectraCLI (when wired) for manifest validation.
- Fabric notebooks or pipelines for scheduled execution.
- App Insights / Log Analytics for instrumentation hooks referenced in the plan.

## Dependencies

- Valid Zephyr tenant and token.
- Fabric workspace named `zephyr` (per contract).
- Jira parity artefacts where linking is required (test execution ↔ issue keys).
