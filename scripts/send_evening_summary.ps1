# Send evening summary to Discord

$envFile = "C:\Users\markm\OneDrive\SPECTRA\.env"
$webhookUrl = (Get-Content $envFile | Select-String "DISCORD_WEBHOOK_URL_CHAT" | ForEach-Object { $_.ToString().Split('=')[1].Trim('"') })

$message = @"
**Evening Wrap: API Intelligence Framework Created** 🌙

**Major Breakthrough:** Instead of brute-forcing Zephyr, created reusable framework for ALL source integrations!

**New Doctrine:** API Intelligence Framework (7 stages)
1. Survey → What entities exist?
2. Catalog → What endpoints exist?
3. Probe → What are the schemas?
4. Relate → What depends on what?
5. Sequence → What order works?
6. Uncover → What are the gotchas?
7. Validate → Does it work?

**Key Insight:** This IS the Prepare stage (enhanced with intelligence)

**Tools Identified:**
- genson (auto-generate schemas)
- networkx (auto-determine order)
- schemathesis (auto-generate test data!)
- apispec (export to OpenAPI)
- httpx (modern HTTP client)

**Project Status:**
- ✅ Zephyr project is clean and ready
- ✅ Issue templates created (Initiative, Activity, Task, Bug)
- ✅ Complete documentation for tomorrow
- ✅ Doctrine committed
- ✅ Lessons captured

**Tomorrow:** Implement API Intelligence for Zephyr (first proof of doctrine)

**Impact:** This framework applies to Jira, Xero, UniFi, and ALL future sources!

Good night! 🚀
"@

$payload = @{
    content = $message
}

$body = $payload | ConvertTo-Json -Depth 10

try {
    Invoke-RestMethod -Uri $webhookUrl -Method Post -Body ([System.Text.Encoding]::UTF8.GetBytes($body)) -ContentType 'application/json; charset=utf-8'
    Write-Host "Evening summary sent to Discord!"
} catch {
    Write-Host "Failed to send Discord notification: $_"
}

