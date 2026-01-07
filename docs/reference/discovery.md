# Discovery (initial pipeline intake)

Purpose: capture the first-pass discovery outputs so the contract can be fully populated before any playbook runs. Fill this document during the intake call; no placeholders should remain once complete. Make it conversational and human—this is an agile “shape the work” session, not an interrogation.

## How to run the session
- Attendees: source owner, Fabric/Spectra owner, security/ops (if auth/network topics arise).
- Inputs to bring: vendor docs, API samples, tenancy/host info, repo/workspace naming rules, capacity options.
- Output: this `discovery.md` plus an updated `contract.yaml` with every required field filled.

## Facilitation script (AI/human guide)
Use these prompts to steer the conversation and capture answers directly into the **Capture log** table.

1) Warm-up (2 mins)
- "What do you call this system (include the edition/variant) and why does it matter to us?" (value, success criteria)
- Admins (Spectra default): mark@spectradatasolutions.com and alana@spectradatasolutions.com (add others only if source-specific)

2) Identity & endpoints (5 mins)
- "Open the system in your browser and copy/paste the web address up to the .com/.net (e.g., https://velonetic.yourzephyr.com). What is it?" *(domain)*
- "Where do you go to see the API documentation? Paste that link." *(docs link)*
- "If an engineer asked for the API root URL (host + path you call), what would you give them? Paste it." *(base API URL)*
  - Helpers: 
    - Repo-local: `python scripts/scrape_apiary.py`
    - Framework (agnostic): `python ../framework/scripts/docs/scrape_api_docs.py --url <docs-url>` (auto-detects OpenAPI/Apiary/HTML; force handler with --handler). Use `rootPath` from output and prepend the discovered host to set `baseUrl`.
- "Can you provide a downloadable API spec (OpenAPI/Swagger or Apiary blueprint) so we can capture methods + paths? If yes, fetch it and save to `docs/endpoints.json`."

3) Auth & guardrails (5 mins)
- "What auth method are we using?"
- If API token:
  - "In OneNote: Notebook `Data` → Section `Zephyr` → Subsection named after the client (e.g., `DXC`). Lock that subsection."
  - "Generate the token and add to local `.env` (git-ignored) using tenant + source naming (e.g., `DXC_ZEPHYR_API_TOKEN`)."
- If OAuth:
  - "Capture client ID/secret, scopes, and redirect URIs; store secrets in the locked OneNote subsection and `.env` with tenant + source naming."
- "Where should we stash the secret so only the right people/pipelines can use it? (If TBD, say so.)"
- "When something fails, is there a tracking ID in the response that support asks for? What is it called?"
- "Is there a status page we should watch? Paste the link."

4) Objects & volume (8 mins)
- "List the things we need to pull (e.g., projects, releases, cycles, executions)."
- "How often should we fetch each thing?"
- "Roughly how many records per fetch/run?"
  - Zephyr core candidates (from API spec): projects, releases, cycles/cycle phases, executions/schedules/teststep results, testcases/teststeps/testcase trees, requirements/requirement trees, users/groups/roles. Optional: defects, admin/license/server info (usually not daily ingest).
  - Note: full sampling per endpoint (responses/schema/volume) will happen in Prepare via a batch sampler; discovery only catalogs the endpoints and objects.

5) Limits & retries (3 mins)
- "When grabbing lots of records, how do we ask for the next chunk? (e.g., offset + limit names)"
- "How many requests can we make before the vendor slows us down? (burst/ongoing) (If unknown, mark TBD and test during Prepare.)"
- "If a call fails, how many times should we retry and with what delay? (Spectra default: 3 retries, exponential backoff ~1s/2s/4s; 30s timeout.)"

6) Storage & topology (5 mins)
- "Where should raw files land? (path/URI)"
- "How long should we keep raw data?"
- "What encryption do we need?"
- "Do we need a shortcut/link to external storage? If yes, where?"
- "Which GitHub org should host the repo?"
- "What should the repo be called?"
- "What visibility should the repo use? (internal/private/public)"
- "What should the Fabric workspace be called?"
- "What should the Fabric workspace description say?"
- "Which Fabric capacity should we use?"
- "What should the lakehouse be called?"

7) Environment & tooling (3 mins)
- "What should we call the runtime environment package? (e.g., SpectraFramework_<source>)"
- "Where should it live in Fabric (path)?"
- "Any specific framework version or tools we must pin?"

8) Ops & governance (3 mins)
- "How often should we run by default?" (Agreed: hourly for Zephyr)
- "Who owns this pipeline?"
- "What status do we start with? (draft/active)"
- "How do we log/audit runs?"

9) Risks & assumptions (3 mins)
- "What could block us?"
- "What assumptions are we making?"

10) Close (2 mins)
- "Is anything missing that future-you would want to see here?"
- Confirm next action: update `contract.yaml` immediately with captured values.

## Capture log (copy/paste into contract fields)
- **System identity**: name, key, variant, description.
- **Endpoints**: host, baseUrl pattern, docs/support URLs.
- **Auth**: method, token/OAuth details, vault path/secret names.
- **Interface limits**: pagination style + params, rate limits (burst/sustained), retry expectations, request ID header, status page.
- **Objects** (one row per object): name, endpoint, method, primary key, supportsIncremental?, incrementalField, description, expected volume/cadence.
- **Storage**: landing zone URI, retention, encryption, shortcuts (if any).
- **Repo**: org, repo name, visibility, description, gitignore, licence, topics.
- **Fabric workspace**: name, description, capacity name, admins (UPNs), git integration target (repo/branch).
- **Environment**: framework environment name/description/path; expected version; ID (fill after import).
- **Lakehouse**: name, description; ID (fill after creation); planned shortcuts (if any).
- **Operations**: default cadence, allowed windows, blackout triggers, checksum/hash requirements, schema contract enforcement, audit logging location.
- **Governance**: owner, status, created/lastUpdated timestamps.
- **Risks/assumptions**: anything unresolved that could block automation.

## Completion checklist (must be true before playbooks)
- All fields above populated in `contract.yaml` (no empty strings/placeholders).
- Scraper run completed and endpoints saved to `docs/endpoints.md` (include docs URL, handler, rootPath, base recomposition).
- Capacity name confirmed and reachable.
- Admin UPNs confirmed.
- Repo/org agreed.
- Landing zone/shortcut location agreed.
- Risks/assumptions logged with owners.

## Definition of Done (discovery)
- Contract updated with host, baseUrl (host + scraped rootPath), auth method, storage, repo/workspace/lakehouse/environment metadata, ops/governance.
- API docs URL captured; endpoints scraped and saved to `docs/endpoints.md`.
- Secrets plan recorded (store location or explicit TODO with owner/date).
- Missing items have action owners and due dates noted in the capture log.
- Next steps agreed (e.g., run playbooks 001-004) and noted.
