# Jira alignment notes

We are correcting Jira references as we expand Zephyr. Use this document to ensure fixes stay synchronised.

## Shared lessons

| Topic         | Jira action                                                                        | Zephyr counterpart                                                                          |
| ------------- | ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Watermarks    | Jira moved from in-memory cursors to Fabric control tables in Oct 2025.            | We mirror the approach via `fabric/control/zephyr/*` paths (see `source/source.plan.yaml`). |
| Pagination    | Jira forced explicit `startAt`/`maxResults` parameters to avoid silent throttling. | We pin `offset`/`maxRecords` in the manifest + plan.                                        |
| Schema drift  | Jira introduced automated JSON schema hashing (spectrafy ticket JIRA-742).         | Zephyr Source gate `contract-alignment` requires the same hashing strategy.                 |
| Observability | Jira standardised metric names (`jira_source_records`).                            | Zephyr metrics follow `zephyr_source_*` to keep dashboards uniform.                         |

## Open corrections

1. **Chronicle linkage** – ensure every Zephyr Source run references the Jira ticket used for the mirrored fix.
2. **Token lifecycle** – Jira rotates OAuth creds quarterly; Zephyr should inherit the same cadence (track under future Jira ticket once opened).
3. **Autonomous build hooks** – Jira manifest now emits `capabilities` metadata. Zephyr needs to add the same block before we declare feature parity.

Log additional lessons here before editing manifests so reviewers can see the rationale in one place.
