# Discord Bot Setup - Master Playbook

**Date:** 2025-12-08  
**Status:** 🟢 Complete Setup Guide  
**Purpose:** Complete end-to-end guide for setting up Discord bot integration for SPECTRA pipelines

---

## 📋 Overview

This playbook documents the complete process of setting up Discord bot integration for SPECTRA pipeline notifications. It covers everything from initial setup through troubleshooting and channel creation.

**What this achieves:**
- ✅ Discord bot authentication working
- ✅ Bot in Discord server with proper permissions
- ✅ Pipeline notification channels created
- ✅ Webhook integration for source stage completions

---

## 🎯 Prerequisites

- Discord account
- Access to Discord Developer Portal
- SPECTRA Bot application created
- Bot invited to Discord server

---

## 📚 Table of Contents

1. [Initial Setup](#1-initial-setup)
2. [Bot Token Configuration](#2-bot-token-configuration)
3. [Team Association](#3-team-association)
4. [Permissions Setup](#4-permissions-setup)
5. [Channel Creation](#5-channel-creation)
6. [Webhook Configuration](#6-webhook-configuration)
7. [Testing & Validation](#7-testing--validation)
8. [Troubleshooting](#8-troubleshooting)

---

## 1. Initial Setup

### 1.1 Create Discord Bot Application

1. Go to: https://discord.com/developers/applications
2. Click **"New Application"**
3. Name it: **"SPECTRA Bot"**
4. Save Application ID: `1446503100478263368`

### 1.2 Create Bot User

1. In Developer Portal, go to **"Bot"** section
2. Click **"Add Bot"**
3. Confirm bot creation
4. Username will be: **"SPECTRA Bot"**

### 1.3 Invite Bot to Server

1. Go to **"OAuth2"** → **"URL Generator"**
2. Select scopes: `bot`, `applications.commands`
3. Select permissions:
   - ✅ Manage Channels
   - ✅ Send Messages
   - ✅ Read Message History
   - ✅ View Channels
4. Copy the generated URL
5. Open URL in browser to invite bot to your server

---

## 2. Bot Token Configuration

### 2.1 Get Bot Token

1. Go to: https://discord.com/developers/applications/1446503100478263368/bot
2. Scroll to **"Token"** section
3. Click **"Reset Token"** (if token is masked)
4. **⚠️ CRITICAL:** Copy token immediately (only shown once)
5. Token format: `MTQ0NjUwMzEwMDQ3ODI2MzM2OA.xxxxx.xxxxx` (3 parts, ~70 chars)

### 2.2 Add Token to .env

**Location:** `C:\Users\markm\OneDrive\SPECTRA\.env`

```bash
DISCORD_BOT_TOKEN="your_token_here"
```

**⚠️ Important:**
- Use quotes around token in `.env` file
- No spaces before/after `=`
- Token must be on single line
- No extra characters (spaces, newlines)

### 2.3 Verify Token Format

Run diagnostic script:
```bash
cd Data\zephyr
python scripts\diagnose_discord_bot.py
```

**Expected output:**
- ✅ Token found in .env
- ✅ Token format valid
- ✅ Status Code: 200 (Success)
- ✅ Bot authenticated successfully

---

## 3. Team Association

### 3.1 Why Team Association is Required

**Critical Issue:** Bot tokens will return `401 Unauthorized` until the app belongs to a Developer Team.

Discord requires apps to belong to a team for:
- Token authentication to work properly
- App verification (required after 75-100 servers)
- Proper app ownership structure

### 3.2 Create Developer Team

1. Go to: https://discord.com/developers/applications
2. Look for **"Teams"** in sidebar (or profile menu)
3. Click **"Create Team"**
4. Name it: **"SPECTRA Development"**
5. Add team members (optional)

### 3.3 Transfer App to Team

1. Go to: https://discord.com/developers/applications/1446503100478263368/general
2. Scroll to **"OWNERSHIP"** section
3. Click **"Change Owner"** button
4. Select your team: **"SPECTRA Development"**
5. Confirm transfer

### 3.4 Verify Team Association

1. Go to: https://discord.com/developers/applications/1446503100478263368/verification-onboarding
2. Under **"Verification Qualifications"**:
   - ✅ **"Your app must belong to a Team"** should show green checkmark

### 3.5 Test Token After Team Transfer

```bash
python scripts\test_bot_token_direct.py
```

**Expected:** Status 200 (Success)

---

## 4. Permissions Setup

### 4.1 Grant Bot Permissions in Server

1. Open Discord → Your server (SPECTRA)
2. Right-click server name → **"Server Settings"**
3. Click **"Roles"** in left sidebar
4. Find **"SPECTRA Bot"** role
5. Click on the role to edit
6. Go to **"Permissions"** tab
7. Enable:
   - ✅ **Manage Channels** (required for channel creation)
   - ✅ **Send Messages**
   - ✅ **Read Message History**
   - ✅ **View Channels**
8. Click **"Save Changes"**

### 4.2 Verify Permissions

Run status check:
```bash
python scripts\check_discord_bot_status.py
```

**Expected:**
- ✅ Bot is in server
- ✅ Bot has roles assigned

---

## 5. Channel Creation

### 5.1 Channel Naming Convention

**Pattern:** `data-{source}-pipelines`

**Examples:**
- `#data-zephyr-pipelines` - Zephyr pipeline notifications
- `#data-jira-pipelines` - Jira pipeline notifications
- `#data-xero-pipelines` - Xero pipeline notifications

### 5.2 Create Channel via Script

**Single channel:**
```bash
python scripts\create_discord_channels.py --channel "data-zephyr-pipelines" --topic "All notifications for Zephyr data pipelines (Source to Analyse stages)."
```

**All recommended channels:**
```bash
python scripts\create_discord_channels.py --all
```

### 5.3 Verify Channel Created

1. Check Discord server
2. Channel should appear in channel list
3. Bot should have access to channel

---

## 6. Webhook Configuration

### 6.1 Create Webhook for Channel

1. Open Discord → Your server
2. Navigate to the pipeline channel (e.g., `#data-zephyr-pipelines`)
3. Click gear icon ⚙️ next to channel name
4. Go to **"Integrations"** → **"Webhooks"**
5. Click **"New Webhook"**
6. Name it: **"SPECTRA Zephyr Pipeline"** (or appropriate name)
7. Click **"Save Changes"**
8. **⚠️ CRITICAL:** Copy webhook URL immediately
   - Format: `https://discord.com/api/webhooks/1234567890/abcdefghijklmnop...`
   - **You won't be able to see it again!**

### 6.2 Add Webhook to Variable Library

**Location:** `Data/zephyr/zephyrVariables.VariableLibrary/variables.json`

Add variable:
```json
{
  "name": "DISCORD_WEBHOOK_URL_ZEPHYR",
  "note": "Discord webhook URL for Zephyr pipeline notifications (data-zephyr-pipelines channel)",
  "type": "String",
  "value": "https://discord.com/api/webhooks/YOUR_WEBHOOK_URL_HERE"
}
```

**SDK Webhook Resolution:**
The SDK (`spectraSDK.Notebook`) automatically looks for webhooks in this order:
1. `DISCORD_WEBHOOK_URL_{SOURCE_SYSTEM}` (e.g., `DISCORD_WEBHOOK_URL_ZEPHYR`)
2. `DISCORD_WEBHOOK_URL` (generic fallback)

### 6.3 Sync to Fabric

1. Commit Variable Library changes
2. Sync to Fabric (Git sync)
3. Verify variable is accessible in Fabric workspace

---

## 7. Testing & Validation

### 7.1 Test Bot Token

```bash
python scripts\test_bot_token_direct.py
```

**Expected:** Status 200, bot username displayed

### 7.2 Test Bot Status

```bash
python scripts\check_discord_bot_status.py
```

**Expected:**
- ✅ Bot authenticated
- ✅ Bot in target server
- ✅ Permissions verified

### 7.3 Test Webhook

```bash
python scripts\test_discord_webhook.py
```

**Expected:** Message appears in Discord channel

### 7.4 Test Source Stage Notification

1. Run `sourceZephyr` notebook in Fabric
2. Upon successful completion, check Discord channel
3. Should see notification message with:
   - ✅ Stage completion status
   - ✅ Duration
   - ✅ Capabilities enabled
   - ✅ Tables created

---

## 8. Troubleshooting

### 8.1 401 Unauthorized Errors

**Symptoms:**
- Bot token authentication fails
- Status code: 401
- Error: "Invalid bot token"

**Solutions:**

1. **Verify app belongs to team:**
   - Go to App Verification page
   - Check "belongs to a Team" shows ✅
   - If not, follow [Team Association](#3-team-association) steps

2. **Reset and verify token:**
   - Reset token in Developer Portal
   - Copy immediately
   - Update `.env` file
   - Verify no quotes issues (use quotes in `.env`)
   - Check token format: 3 parts, ~70 chars

3. **Check token in .env:**
   ```bash
   python scripts\diagnose_discord_bot.py
   ```

### 8.2 403 Missing Permissions

**Symptoms:**
- Channel creation fails
- Error: "Missing Permissions"

**Solutions:**

1. **Grant permissions:**
   - Server Settings → Roles
   - Edit "SPECTRA Bot" role
   - Enable "Manage Channels"
   - Save changes

2. **Verify bot role hierarchy:**
   - Ensure bot role is above channels
   - Check role permissions in server

### 8.3 Webhook Not Sending Messages

**Symptoms:**
- Source stage completes
- No Discord notification received

**Solutions:**

1. **Verify webhook URL in Variable Library:**
   - Check `DISCORD_WEBHOOK_URL_ZEPHYR` exists
   - Verify URL is correct (no extra spaces)
   - Sync Variable Library to Fabric

2. **Test webhook directly:**
   ```bash
   python scripts\test_discord_webhook.py
   ```

3. **Check SDK webhook resolution:**
   - SDK looks for `DISCORD_WEBHOOK_URL_{SOURCE_SYSTEM}` first
   - Falls back to `DISCORD_WEBHOOK_URL`
   - Verify variable name matches source system

### 8.4 Bot Not in Server

**Symptoms:**
- Status check shows "Bot is not in any servers"
- Cannot create channels

**Solutions:**

1. **Re-invite bot:**
   - Go to OAuth2 URL Generator
   - Generate invite URL with proper permissions
   - Use URL to invite bot to server

2. **Verify invite URL permissions:**
   - Must include `bot` scope
   - Must include "Manage Channels" permission

---

## 📁 Related Documentation

- `docs/CREATE-DISCORD-DEVELOPER-TEAM.md` - Team creation details
- `docs/RESET-BOT-TOKEN-STEP-BY-STEP.md` - Token reset guide
- `docs/GRANT-BOT-CHANNEL-PERMISSIONS.md` - Permissions setup
- `docs/CREATE-WEBHOOK-FOR-ZEPHYR-CHANNEL.md` - Webhook creation
- `docs/DISCORD-APP-STATUS-EXPLAINED.md` - App status clarification
- `docs/DISCORD-CHANNEL-STRUCTURE.md` - Channel naming conventions

---

## 🛠️ Scripts Reference

### Diagnostic Scripts

- `scripts/diagnose_discord_bot.py` - Comprehensive bot diagnostic
- `scripts/test_bot_token_direct.py` - Direct token authentication test
- `scripts/check_discord_bot_status.py` - Full bot status check

### Management Scripts

- `scripts/create_discord_channels.py` - Create pipeline notification channels
- `scripts/update_bot_token.py` - Update token in .env file
- `scripts/test_discord_webhook.py` - Test webhook URL

---

## ✅ Quick Checklist

Use this checklist when setting up Discord bot integration:

- [ ] Bot application created in Developer Portal
- [ ] Bot user created and configured
- [ ] Bot invited to Discord server
- [ ] Bot token obtained and added to `.env` (with quotes)
- [ ] Developer Team created
- [ ] App transferred to team
- [ ] Token authentication verified (Status 200)
- [ ] Bot permissions granted in server (Manage Channels, etc.)
- [ ] Pipeline notification channel created
- [ ] Webhook created for channel
- [ ] Webhook URL added to Variable Library
- [ ] Variable Library synced to Fabric
- [ ] Webhook test successful
- [ ] Source stage notification working

---

## 🎯 Key Learnings

### Critical Success Factors

1. **Team Association is Mandatory**
   - Token won't authenticate until app belongs to a team
   - This is the #1 cause of 401 errors

2. **Token Format Matters**
   - Must use quotes in `.env` file
   - No spaces, no newlines
   - 3 parts separated by dots

3. **Permissions are Channel-Level**
   - Bot needs "Manage Channels" at server level
   - Permissions must be granted in server settings

4. **Webhook URLs are Single-Use Visibility**
   - Copy immediately when created
   - Can't retrieve later if lost

### Common Mistakes to Avoid

- ❌ Not associating app with team (causes 401)
- ❌ Forgetting to copy token immediately after reset
- ❌ Not using quotes around token in `.env`
- ❌ Forgetting to grant "Manage Channels" permission
- ❌ Not copying webhook URL immediately
- ❌ Wrong variable name in Variable Library (case-sensitive)

---

## 🚀 Next Steps

After completing setup:

1. **Add more source systems:**
   - Create channels for other sources (Jira, Xero, UniFi)
   - Add webhook URLs to respective Variable Libraries

2. **Enhance notifications:**
   - Add notifications for other pipeline stages
   - Customize notification messages
   - Add error notifications

3. **Monitor and maintain:**
   - Periodically verify bot status
   - Rotate tokens if needed
   - Update permissions as needed

---

**Version:** 1.0.0  
**Last Updated:** 2025-12-08  
**Status:** 🟢 Complete Master Playbook  
**Maintainer:** SPECTRA Development Team
