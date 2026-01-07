# Discord Bot Complete Configuration Guide - SPECTRA Expert

**Date:** 2025-12-08  
**Purpose:** Comprehensive guide to every Discord bot setting for SPECTRA  
**Expert Level:** Complete configuration knowledge

---

## 🎯 SPECTRA Discord Bot Requirements

**What we need the bot for:**
1. ✅ **Create channels programmatically** (source-specific pipeline channels)
2. ✅ **Send notifications** (via webhooks - already working)
3. ⏳ **Slash commands** (`/chat` for AI assistant - future feature)
4. ⏳ **Manage channels** (automation)
5. ⏳ **Read messages** (for AI assistant responses)

---

## 📋 Complete Settings Breakdown

### **1. General Information** ✅ CONFIGURED

**Location:** Settings → General Information

**Status:** ✅ Already configured

**Settings:**
- ✅ **Name:** "SPECTRA Bot"
- ✅ **Description:** Set
- ✅ **Tags:** AI, Developer Tools, Notifications, Utility
- ✅ **Application ID:** `1446503100478263368`
- ✅ **Public Key:** `9ad1cd63cde0937e553ab5618d196fadea429f8d5dcd831f4de3b57fda3b4fdd`

**Action Required:** ✅ None - already good

---

### **2. Installation** ⚠️ NEEDS CONFIGURATION

**Location:** Settings → Installation

**What to Configure:**

#### **Guild Install (Server Install)**

**Scopes - CHECK THESE:**
- ✅ **`bot`** - REQUIRED (enables bot functionality)
- ✅ **`applications.commands`** - RECOMMENDED (for slash commands)

**Permissions - SELECT THESE:**
- ✅ **Manage Channels** - REQUIRED (for channel creation)
- ✅ **Send Messages** - RECOMMENDED (for notifications)
- ✅ **Read Message History** - RECOMMENDED (for reading messages)
- ✅ **View Channels** - RECOMMENDED (to see channels)
- ✅ **Use Slash Commands** - OPTIONAL (if using slash commands)

**Install Link:**
- URL is generated automatically at bottom of page
- Copy this URL to invite bot to servers

**Action Required:** ✅ Configure scopes and permissions, then invite bot

---

### **3. OAuth2** ✅ MOSTLY CONFIGURED

**Location:** Settings → OAuth2

#### **Client Information:**
- ✅ **Client ID:** `1446503100478263368` (auto-generated)
- ✅ **Client Secret:** Hidden (for OAuth2 flows - not needed for bot)
- ⚠️ **Public Client:** Keep OFF (we're using bot, not public client)

#### **Redirects:**
- ⚠️ **Not needed for bot functionality**
- Only needed if using OAuth2 for user authentication
- **Action:** Leave empty for now

#### **OAuth2 URL Generator:**
- ✅ Same as Installation → Guild Install
- Use this to generate invite URLs

**Action Required:** ✅ None - already configured correctly

---

### **4. Bot** 🔴 CRITICAL - NEEDS CONFIGURATION

**Location:** Settings → Bot

**Critical Settings:**

#### **Token:**
- ⚠️ **RESET AND COPY** - Current token invalid
- Click "Reset Token" → Copy immediately
- Update `.env` file with new token (no quotes)

#### **Privileged Gateway Intents:**
- ✅ **MESSAGE CONTENT INTENT** - REQUIRED (for reading message content)
- ✅ **SERVER MEMBERS INTENT** - RECOMMENDED (for user info)
- ⚠️ **PRESENCE INTENT** - NOT NEEDED (optional)

**Why Intents:**
- Bot needs to read message content for `/chat` commands
- Required for AI assistant functionality

#### **Bot Permissions (Server-Level):**
- Set when inviting bot (covered in Installation section)
- Can be adjusted per-server after invite

**Action Required:** 🔴 **RESET TOKEN AND ENABLE INTENTS**

---

### **5. Webhooks** ✅ ALREADY WORKING

**Location:** Settings → Webhooks

**Status:** ✅ Working - we use webhooks for notifications

**Current Setup:**
- `DISCORD_WEBHOOK_URL_CHAT` configured and working
- Webhooks created per-channel as needed

**Action Required:** ✅ None - webhooks work without bot token

---

### **6. Rich Presence** ❌ NOT NEEDED

**Location:** Settings → Rich Presence

**Purpose:** For games/applications showing activity status

**For SPECTRA:** ❌ Not needed (we're not a game)

**Action Required:** ✅ Skip - not relevant

---

### **7. App Testers** ⏳ OPTIONAL

**Location:** Settings → App Testers

**Purpose:** Add testers before public release

**For SPECTRA:** ⏳ Optional - can add testers later

**Action Required:** ✅ Skip for now

---

### **8. App Verification** ❌ NOT NEEDED YET

**Location:** Settings → App Verification

**Purpose:** Required for bots with 100+ servers

**Current Status:** 
- ✅ Bot is temporarily approved
- ✅ Can use Privileged Intents until 100 servers
- ❌ Verification not needed until scaling

**Action Required:** ✅ Skip until bot joins 100+ servers

---

## 🔴 CRITICAL CONFIGURATION CHECKLIST

### **Immediate (For Channel Creation):**

- [ ] **Bot Tab → Reset Token** - Get fresh token
- [ ] **Bot Tab → Enable MESSAGE CONTENT INTENT** - For message reading
- [ ] **Bot Tab → Enable SERVER MEMBERS INTENT** - Recommended
- [ ] **Installation → Configure Scopes:**
  - [ ] ✅ `bot` (required)
  - [ ] ✅ `applications.commands` (for slash commands)
- [ ] **Installation → Configure Permissions:**
  - [ ] ✅ **Manage Channels** (required)
  - [ ] ✅ Send Messages
  - [ ] ✅ Read Message History
  - [ ] ✅ View Channels
- [ ] **Installation → Copy Invite URL** - Invite bot to server
- [ ] **Update .env** - Add bot token (no quotes)

### **Already Done:**

- ✅ General Information configured
- ✅ OAuth2 Client ID/Secret set
- ✅ Webhooks working
- ✅ Bot invited to server

---

## 🎯 Recommended Configuration Summary

### **Scopes (OAuth2 / Installation):**
```
✅ bot
✅ applications.commands
```

### **Permissions (When Inviting Bot):**
```
✅ Manage Channels (REQUIRED)
✅ Send Messages
✅ Read Message History
✅ View Channels
✅ Use Slash Commands
```

### **Bot Intents (Bot Tab):**
```
✅ MESSAGE CONTENT INTENT (REQUIRED)
✅ SERVER MEMBERS INTENT (RECOMMENDED)
❌ PRESENCE INTENT (NOT NEEDED)
```

---

## 📋 Step-by-Step Configuration Order

### **Step 1: Bot Tab (Most Important)**

1. Go to: https://discord.com/developers/applications/1446503100478263368/bot

2. **Reset Token:**
   - Click "Reset Token"
   - Copy token immediately
   - Update `.env`: `DISCORD_BOT_TOKEN=new_token_here` (no quotes)

3. **Enable Intents:**
   - Scroll to "Privileged Gateway Intents"
   - ✅ Enable "MESSAGE CONTENT INTENT"
   - ✅ Enable "SERVER MEMBERS INTENT"
   - Click "Save Changes"

### **Step 2: Installation Tab (OAuth2 URL Generator)**

1. Go to: https://discord.com/developers/applications/1446503100478263368/installation

2. **Configure Scopes:**
   - ✅ Check `bot`
   - ✅ Check `applications.commands`

3. **Configure Permissions:**
   - Click "Select" dropdown
   - ✅ Check "Manage Channels"
   - ✅ Check "Send Messages"
   - ✅ Check "Read Message History"
   - ✅ Check "View Channels"

4. **Copy Generated URL** (at bottom of page)

5. **Open URL in browser** → Select server → Authorize

### **Step 3: Verify Everything Works**

```bash
# Test bot token
python scripts\test_bot_token_direct.py

# Check bot status
python scripts\check_discord_bot_status.py

# Test channel creation
python scripts\create_discord_channels.py --all --dry-run
```

---

## ✅ Settings You Can Ignore (For Now)

- ❌ **Rich Presence** - Not a game
- ❌ **App Verification** - Only needed at 100+ servers
- ❌ **App Testers** - Optional
- ❌ **OAuth2 Redirects** - Not using OAuth2 user auth
- ❌ **Public Client** - Keep OFF

---

## 🎯 Summary: What Needs Configuring

**Critical (Must Do):**
1. 🔴 **Bot Tab → Reset Token** (get fresh token)
2. 🔴 **Bot Tab → Enable MESSAGE CONTENT INTENT**
3. 🔴 **Installation → Select Permissions** (Manage Channels, etc.)
4. 🔴 **Update .env** with new token

**Recommended (Should Do):**
5. ✅ **Installation → Enable applications.commands scope**
6. ✅ **Bot Tab → Enable SERVER MEMBERS INTENT**
7. ✅ **Installation → Select additional permissions** (Send Messages, etc.)

**Optional (Can Skip):**
- App Verification
- App Testers
- Rich Presence
- OAuth2 Redirects

---

**Focus on the Bot Tab and Installation Tab - those are the critical ones!**

