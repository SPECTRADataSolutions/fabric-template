# Send Discord notification about hierarchy discovery completion

$envFile = "C:\Users\markm\OneDrive\SPECTRA\.env"
$webhookUrl = (Get-Content $envFile | Select-String "DISCORD_WEBHOOK_URL_CHAT" | ForEach-Object { $_.ToString().Split('=')[1].Trim('"') })

$message = @"
**Zephyr API Hierarchy Discovery Complete!** ✅

**Method:** Autonomous systematic experimentation
**Status:** Full hierarchy mapped

**Success Rate:** 4/8 entities working (50%)

**Working (Level 0):**
- ✅ Release (use existing to avoid >60s lock)
- ✅ Requirement Folder

**Working (Level 1):**
- ✅ Requirement (via /requirementtree/add + parentId)
- ✅ Cycle (with existing release ID 131)

**Blocked:**
- ❌ Testcase Folder (BLOCKER-002 - API broken)
- ⏸️ Testcase, Execution, Allocation (blocked by folder failure)

**Key Discoveries:**
1. Releases lock for >60s after creation
2. Use existing releases (ID 131) - works immediately
3. Folder creation API is broken (HTTP 400)
4. Manual folder creation workaround required

**Reports:** validation-reports/hierarchy-discovery-summary.md
**Next:** Create folders in UI, then continue automation
"@

$body = @{ content = $message } | ConvertTo-Json

Invoke-RestMethod -Uri $webhookUrl -Method Post -Body $body -ContentType 'application/json'

Write-Host "Notification sent to Discord!"

