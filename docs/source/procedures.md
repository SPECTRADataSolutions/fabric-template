# Source stage procedures

This runbook keeps Source executions auditable and repeatable. Follow the steps sequentially; capture deviations in `Core/memory` and link to Jira wherever relevant.

## 1. Pre-flight

1. Confirm the Zephyr token is valid and stored in Vault; reference `contract.yaml` for auth rules.
2. Validate network reachability to `https://velonetic.yourzephyr.com/flex/services/rest/latest`.
3. Run a dry Spectra manifest validation (`spectra validate --manifest manifest.json`) once SpectraCLI is wired in this repo.
4. Check Fabric landing zones listed in `source/source.plan.yaml` are accessible and empty/ready.
5. Review Jira parity notes in `docs/source/jira-alignment.md` for any hot fixes that must be mirrored.

## 2. Execution

1. Trigger the ingestion units in order: projects → releases → cycles → executions.
2. Honour the cron cadence defined in the plan (15 minute spacing) when scheduling automated runs.
3. Persist raw payloads plus control metadata (watermarks, checksums) to Fabric paths exactly as specified.
4. Emit telemetry to App Insights using the metric names declared in the plan.

## 3. Validation

1. Compare record counts against the previous run (alert if delta >±5%).
2. Reconcile schema hashes against `contract.yaml` (`contract-alignment` gate).
3. Verify watermarks advanced for each incremental object; log anomalies in Jira + Chronicle.
4. Update `contract.yaml` `lastUpdatedAt` whenever structure or limits change.

## 4. Evidence + comms

1. Attach run metadata + metric snapshots to the daily Chronicle entry.
2. If `.spectra` evidence is produced, store it under `.spectra/evidence/zephyr/source/<date>`.
3. Raise Sev1/Sev2 escalations per the plan if the vendor API is degraded for more than two runs.

## 5. Recovery scenarios

| Scenario         | Response                                                                                    |
| ---------------- | ------------------------------------------------------------------------------------------- |
| Token revoked    | Mint a new token, update Vault, and re-run the full Source chain.                           |
| Pagination stall | Reduce `maxRecords`, resume from stored offset, and file a Jira task referencing the stall. |
| Schema drift     | Freeze downstream runs, update contract + manifest, capture spectrafy evidence.             |

Keep this document current; if a step changes, update the table and notate the change in the Chronicle.
