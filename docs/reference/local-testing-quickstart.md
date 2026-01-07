# Local Testing Quick Start
**Date:** 2025-01-29

---

## 🚀 Quick Start (2 minutes)

### 1. Create `.env` file

Create `Data/zephyr/.env` (gitignored):

```bash
DXC_ZEPHYR_BASE_URL=https://velonetic.yourzephyr.com
DXC_ZEPHYR_BASE_PATH=/flex/services/rest/latest
DXC_ZEPHYR_API_TOKEN=your_actual_token_here
```

### 2. Run tests

```powershell
cd Data/zephyr
.\scripts\test-local.ps1
```

**That's it!** The script will:
- Load environment variables from `.env`
- Test all 4 endpoints (`/project`, `/release`, `/cycle`, `/execution`)
- Test with both active projects (40, 44)
- Test pagination (`firstresult`/`maxresults`)
- Show summary of results

---

## 📋 What Gets Tested

### Quick Test (4 core endpoints)
- ✅ `/project` endpoint
- ✅ `/release` endpoint (for Project 40 and 44)
- ✅ `/cycle` endpoint (for Project 40 and 44)
- ✅ `/execution` endpoint (for Project 40 and 44)
- ✅ Pagination (`firstresult`/`maxresults`)

### Comprehensive Test (all endpoints)
```powershell
python scripts/test_all_endpoints.py --category all
```

This tests **all 76+ GET endpoints** for data extraction, including:
- Core endpoints (projects, releases, cycles, executions)
- Test case endpoints
- Requirement endpoints
- Execution/test step endpoints
- User/team endpoints
- Attachment endpoints

---

## 🔧 Manual Testing

If you prefer to test manually:

```powershell
# Load environment variables
Get-Content .env | Where-Object { $_ -notmatch '^[\s#]' -and $_ -match '=' } | ForEach-Object { 
    $k,$v = $_ -split '=',2; 
    Set-Item -Path ('Env:' + $k.Trim()) -Value $v.Trim() 
}

# Run test script
python scripts/test_source_local.py
```

---

## 📚 Full Guide

See `docs/development/local-testing-guide.md` for:
- Multiple testing methods
- Mock testing
- Local Spark setup
- Troubleshooting

---

**Last Updated:** 2025-01-29

