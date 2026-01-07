# Send prepareZephyr pipeline ready notification

$envFile = "C:\Users\markm\OneDrive\SPECTRA\.env"
$webhookUrl = (Get-Content $envFile | Select-String "DISCORD_WEBHOOK_URL_CHAT" | ForEach-Object { $_.ToString().Split('=')[1].Trim('"') })

$message = @"
**🎉 prepareZephyr Pipeline - READY FOR TESTING!** 🚀

**Major Achievement:** Intelligence-powered Prepare stage integrated into pipeline!

**What Was Done:**
✅ Created `prepareZephyr` notebook in Fabric UI (Fabric-first workflow)
✅ Fabric generated proper `.platform` with real notebook ID
✅ Added to pipeline (runs after sourceZephyr)
✅ Pipeline updated and synced to Git

**Pipeline Flow:**
``sourceZephyr`` → ``prepareZephyr`` (intelligence-powered)

**Prepare Intelligence:**
- ``prepare._schema`` ← Loads from intelligence/schemas/*.json (genson)
- ``prepare._dependencies`` ← Loads from intelligence/dependencies.yaml (networkx)
- ``prepare._constraints`` ← Loads from intelligence/quirks.yaml

**The SPECTRA-Grade Lesson:**
**Fabric notebooks should be created in Fabric FIRST**, then committed to Git. This is the platform-designed workflow. Trying Git → Fabric causes validation/cache issues.

**Status:** ✅ Ready for pipeline test in Fabric

**Next:** Sync Fabric, run pipeline, verify prepare tables created!

**Testing guide:** ``docs/prepare/test-pipeline-quick-guide.md``
"@

$payload = @{
    content = $message
}

$body = $payload | ConvertTo-Json -Depth 10

try {
    Invoke-RestMethod -Uri $webhookUrl -Method Post -Body ([System.Text.Encoding]::UTF8.GetBytes($body)) -ContentType 'application/json; charset=utf-8'
    Write-Host "Pipeline ready notification sent to Discord!"
} catch {
    Write-Host "Failed to send Discord notification: $_"
}







