# Discord Channel Structure - SPECTRA-Grade Design

**Date:** 2025-12-08  
**Status:** 🟢 Proposal  
**Purpose:** Define standard Discord channel naming and organization for pipeline notifications

---

## 🎯 SPECTRA-Grade Channel Strategy

**Principle:** _"One channel per source system, all stages, all priorities."_

### Recommended Structure

**Channel Naming Pattern:**
```
#data-{source}-pipelines
```

**Examples:**
- `#data-zephyr-pipelines` - All Zephyr pipeline notifications
- `#data-jira-pipelines` - All Jira pipeline notifications
- `#data-xero-pipelines` - All Xero pipeline notifications
- `#data-unifi-pipelines` - All UniFi pipeline notifications

---

## ✅ Why This Structure?

### 1. **Source System Ownership**

Each source system has clear ownership and responsibility:
- All notifications for Zephyr go to one place
- Easy to find all activity for a specific source
- Clear separation of concerns

### 2. **Scalability**

- Adding new source systems = add one new channel
- No need to create multiple channels per source
- Works for any number of sources

### 3. **Stage Visibility**

All stages (source, prepare, extract, clean, transform, refine, analyse) appear in the same channel:
- See complete pipeline lifecycle in one place
- Understand dependencies between stages
- Track progression from source → analyse

### 4. **Priority Differentiation**

Use Discord message formatting to differentiate:
- ✅ **Success** - Green emoji, normal priority
- ⚠️ **Warning** - Yellow emoji, normal priority
- ❌ **Failure** - Red emoji, high priority
- 🔥 **Critical** - Red emoji, @mentions for alerts

### 5. **Notification Filtering**

Discord allows:
- Channel-level muting (if you don't want Zephyr notifications)
- Threads for related notifications (optional enhancement)
- Role-based mentions (@data-team for critical failures)

---

## 🔄 Alternative Structures Considered

### Option 1: One Channel Per Stage (❌ Rejected)

**Structure:** `#source-stage`, `#prepare-stage`, `#extract-stage`

**Problems:**
- ❌ Loses source system context (which source is failing?)
- ❌ Hard to track pipeline progression
- ❌ More channels to manage
- ❌ Doesn't scale well (7 stages × N sources = many channels)

### Option 2: One Channel Per Source-Stage (❌ Rejected)

**Structure:** `#zephyr-source`, `#zephyr-prepare`, `#jira-source`

**Problems:**
- ❌ Too many channels (7 stages × N sources)
- ❌ Hard to see pipeline progression
- ❌ Notification fatigue (too many channels)

### Option 3: Single Channel for All (❌ Rejected)

**Structure:** `#spectra-pipelines`

**Problems:**
- ❌ Noisy (all sources mixed together)
- ❌ Hard to filter by source system
- ❌ Can't mute specific sources

### Option 4: Channels by Priority (❌ Rejected)

**Structure:** `#pipeline-success`, `#pipeline-warnings`, `#pipeline-failures`

**Problems:**
- ❌ Loses source system context
- ❌ Can't see stage progression
- ❌ Hard to track specific source issues

---

## 📊 Recommended Structure (✅ Selected)

### Primary Channels

```
#data-zephyr-pipelines    - Zephyr Enterprise pipeline notifications
#data-jira-pipelines      - Jira pipeline notifications
#data-xero-pipelines      - Xero pipeline notifications
#data-unifi-pipelines     - UniFi pipeline notifications
```

### Optional: Central Operations Channel

```
#spectra-pipeline-alerts  - Critical failures across all sources (optional)
```

**Purpose:** High-severity alerts that need immediate attention across all sources.

---

## 🎨 Message Format

### Standard Success Notification

```
✅ **Zephyr Source Stage Finalised**

**Stage:** Source  
**Status:** Success  
**Duration:** 38.3s  
**Workspace:** zephyrLakehouse  
**Capabilities:** authVerified, bootstrapped, tablesRegistered  

**Tables Created:**
- `source.portfolio` - Source system dashboard metadata
- `source.config` - Runtime configuration snapshot
- `source.credentials` - Authentication validation status
- `source.endpoints` - Complete endpoint catalog

**Next Stage:** Prepare (schema introspection)
```

### Failure Notification

```
❌ **Zephyr Source Stage Failed**

**Stage:** Source  
**Status:** Failed  
**Error:** Authentication failed: Invalid API token  
**Duration:** 2.1s  
**Workspace:** zephyrLakehouse  

**Action Required:** Check API token in Variable Library
```

### Critical Alert (with @mention)

```
🔥 **CRITICAL: Zephyr Pipeline Failure**

**Stage:** Extract  
**Status:** Failed  
**Error:** Connection timeout - Zephyr API unavailable  
**Duration:** 120.0s  
**Workspace:** zephyrLakehouse  

**Impact:** Data pipeline stopped, downstream stages blocked

@data-team - Immediate attention required
```

---

## 🔧 Implementation

### Variable Library Configuration

**Variable Name:** `DISCORD_WEBHOOK_URL_{SOURCE}`

**Examples:**
- `DISCORD_WEBHOOK_URL_ZEPHYR` - Webhook for `#data-zephyr-pipelines`
- `DISCORD_WEBHOOK_URL_JIRA` - Webhook for `#data-jira-pipelines`

**SDK Auto-Detection:**
```python
# SDK infers webhook variable name from source system
source_system = session.ctx["source_system"]  # "zephyr"
webhook_var = f"DISCORD_WEBHOOK_URL_{source_system.upper()}"  # "DISCORD_WEBHOOK_URL_ZEPHYR"
webhook_url = session.variables.get(webhook_var, required=False)
```

### SDK Helper Update

**Current:**
```python
webhook_url = session.variables.get("DISCORD_WEBHOOK_URL", required=False)
```

**Proposed:**
```python
# Auto-detect webhook variable based on source system
source_system = session.ctx["source_system"].upper()
webhook_var = f"DISCORD_WEBHOOK_URL_{source_system}"
webhook_url = session.variables.get(webhook_var, required=False)

# Fallback to generic DISCORD_WEBHOOK_URL if source-specific not found
if not webhook_url:
    webhook_url = session.variables.get("DISCORD_WEBHOOK_URL", required=False)
```

---

## ✅ Benefits

1. **Clear Ownership** - One channel per source system
2. **Scalable** - Easy to add new sources
3. **Complete Visibility** - All stages in one place per source
4. **Filterable** - Can mute specific sources if needed
5. **SPECTRA-Grade** - Consistent, reusable, maintainable

---

## 📋 Next Steps

1. ✅ **Design approved** (this document)
2. ✅ **Script created** - `scripts/create_discord_channels.py`
3. ⏳ **Create Discord channels** - Run script or create manually
4. ⏳ **Configure webhooks** for each channel
5. ⏳ **Add webhook URLs** to Variable Libraries:
   - `zephyrVariables` → `DISCORD_WEBHOOK_URL_ZEPHYR`
   - `jiraVariables` → `DISCORD_WEBHOOK_URL_JIRA`
   - etc.
6. ✅ **Update SDK** to auto-detect source-specific webhook variables
7. ⏳ **Test** with Zephyr source stage notification

---

## 🛠️ Creating Channels

### Option 1: Automated Script

**Script:** `scripts/create_discord_channels.py`

**Prerequisites:**
- `DISCORD_BOT_TOKEN` in `.env` file at SPECTRA root
- `DISCORD_GUILD_ID` in `.env` file (your Discord server ID)

**Usage:**
```bash
# Create all recommended channels
python scripts/create_discord_channels.py --all

# Create single channel
python scripts/create_discord_channels.py --channel "data-zephyr-pipelines" --topic "Zephyr pipeline notifications"

# Dry run (preview without creating)
python scripts/create_discord_channels.py --all --dry-run
```

**Bot Permissions Required:**
- `Manage Channels` - To create channels

### Option 2: Manual Creation

1. Open Discord server
2. Right-click server → "Create Channel"
3. Channel name: `data-zephyr-pipelines` (or other source name)
4. Channel type: Text Channel
5. Set topic (optional): Description of what the channel is for
6. Repeat for each source system

---

**Version:** 1.0.0  
**Date:** 2025-12-08  
**Status:** 🟢 Recommended Structure

