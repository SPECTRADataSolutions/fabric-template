# Discord Bot Configuration Checklist - SPECTRA

**Date:** 2025-12-08  
**Status:** Complete configuration guide for SPECTRA Discord bot

---

## 🎯 What SPECTRA Uses Discord For

1. **Pipeline Notifications** (webhooks) - ✅ Working
2. **Channel Creation** (bot token) - ⏳ In progress
3. **Slash Commands** (`/chat` for AI assistant) - ⏳ Planned
4. **AI Assistant Integration** - ⏳ Planned

---

## ✅ Configuration Checklist

### **1. General Information** ✅ CONFIGURED

- [x] **Name:** "SPECTRA Bot"
- [x] **Description:** Set
- [x] **Tags:** AI, Developer Tools, Notifications, Utility
- [x] **Application ID:** `1446503100478263368`
- [x] **Public Key:** `9ad1cd63cde0937e553ab5618d196fadea429f8d5dcd831f4de3b57fda3b4fdd`

**✅ Action:** None needed - already configured

---

### **2. Bot Tab** 🔴 CRITICAL - DO THIS

**Location:** https://discord.com/developers/applications/1446503100478263368/bot

**Required Actions:**

- [ ] **Reset Token:**
  - Click "Reset Token" button
  - Copy token immediately
  - Update `.env`: `DISCORD_BOT_TOKEN=new_token_here` (NO QUOTES)
  
- [ ] **Enable Privileged Gateway Intents:**
  - ✅ **MESSAGE CONTENT INTENT** - REQUIRED
    - Why: Bot needs to read message content for `/chat` commands
    - Without this: Bot cannot read what users type
  - ✅ **SERVER MEMBERS INTENT** - RECOMMENDED
    - Why: Access to server member information
    - Without this: Limited user info access
  - ❌ **PRESENCE INTENT** - NOT NEEDED
    - Only for showing online/offline status
    - Skip this one

**✅ Action:** Reset token and enable intents

---

### **3. Installation (OAuth2 URL Generator)** 🔴 CRITICAL - DO THIS

**Location:** https://discord.com/developers/applications/1446503100478263368/installation

**Or via:** OAuth2 → URL Generator (same thing)

**Required Actions:**

#### **Scopes Section:**
- [ ] ✅ **`bot`** - REQUIRED (must be checked)
  - Enables bot functionality
  - Without this, bot won't work
  
- [ ] ✅ **`applications.commands`** - RECOMMENDED (check this)
  - Enables slash commands (`/chat`, etc.)
  - Required for future AI assistant features

#### **Permissions Section:**
Click "Select" dropdown and check:

- [ ] ✅ **Manage Channels** - REQUIRED
  - Why: Create channels programmatically
  - Without this: Cannot create channels
  
- [ ] ✅ **Send Messages** - RECOMMENDED
  - Why: Send notifications and responses
  - Without this: Cannot send messages
  
- [ ] ✅ **Read Message History** - RECOMMENDED
  - Why: Read messages for AI assistant
  - Without this: Cannot read channel history
  
- [ ] ✅ **View Channels** - RECOMMENDED
  - Why: See channels in server
  - Without this: Limited visibility
  
- [ ] ✅ **Use Slash Commands** - OPTIONAL
  - Why: For slash command functionality
  - Without this: Slash commands won't work

**After selecting:**
- Copy the generated URL at bottom of page
- Open URL in browser
- Select your Discord server
- Click "Authorize"

**✅ Action:** Select scopes + permissions, invite bot

---

### **4. General Information → Interactions Endpoint** ⏳ FOR SLASH COMMANDS

**Location:** Settings → General Information → Interactions Endpoint URL

**Current:** `https://nice-example.local/api/interactions` (placeholder)

**Should be:** `https://webhooks-production-631e.up.railway.app/webhook/discord`

**Purpose:** Where Discord sends slash command interactions (for `/chat` command)

**Status:** ⏳ Only needed if using slash commands

**Action:**
- [ ] Update to webhooks service URL
- [ ] Click "Save Changes"
- [ ] Discord will verify (green checkmark = success)

**✅ Action:** Update if you want slash commands working

---

### **5. OAuth2 → Redirects** ❌ NOT NEEDED

**Location:** Settings → OAuth2 → Redirects

**Purpose:** For OAuth2 user authentication flows

**For SPECTRA:** ❌ Not using OAuth2 user auth (using bot only)

**Action:** ✅ Skip - leave empty

---

### **6. OAuth2 → Client Secret** ✅ ALREADY SET

**Location:** Settings → OAuth2 → Client Information

**Status:** ✅ Already configured (auto-generated)

**Action:** ✅ None needed

---

### **7. Webhooks** ✅ ALREADY WORKING

**Location:** Settings → Webhooks

**Status:** ✅ Working - webhooks don't need bot configuration

**Action:** ✅ None needed

---

### **8. App Verification** ❌ NOT NEEDED YET

**Location:** Settings → App Verification

**Status:** 
- ✅ Temporarily approved
- ✅ Can use until 100 servers
- ❌ Not required for current use

**Action:** ✅ Skip until bot reaches 100+ servers

---

## 🎯 Quick Action Summary

### **Do Right Now (For Channel Creation):**

1. **Bot Tab:**
   - [ ] Reset token → Copy → Update `.env`
   - [ ] Enable MESSAGE CONTENT INTENT
   - [ ] Enable SERVER MEMBERS INTENT

2. **Installation Tab:**
   - [ ] Check `bot` scope
   - [ ] Check `applications.commands` scope
   - [ ] Select "Manage Channels" permission
   - [ ] Select other recommended permissions
   - [ ] Copy generated URL
   - [ ] Open URL → Select server → Authorize

3. **Verify:**
   ```bash
   python scripts\check_discord_bot_status.py
   python scripts\create_discord_channels.py --all --dry-run
   ```

### **Do Later (For Slash Commands):**

4. **General Information:**
   - [ ] Update Interactions Endpoint URL
   - [ ] Verify endpoint (green checkmark)

---

## 📊 Configuration Priority

**🔴 Critical (Must Do Now):**
- Bot token reset
- Privileged Gateway Intents
- OAuth2 Scopes (`bot`, `applications.commands`)
- OAuth2 Permissions (`Manage Channels`, etc.)
- Invite bot to server

**🟡 Important (Do Soon):**
- Interactions Endpoint URL (for slash commands)
- Additional permissions (Send Messages, Read History)

**🟢 Optional (Can Skip):**
- App Verification (until 100+ servers)
- OAuth2 Redirects (not using)
- Rich Presence (not a game)
- App Testers (optional)

---

## ✅ Configuration Order (Recommended)

1. **Bot Tab** → Reset token, enable intents
2. **Installation** → Configure scopes/permissions, invite bot
3. **Test** → Verify bot works, test channel creation
4. **Later** → Interactions Endpoint URL (for slash commands)

---

## 🎯 Bottom Line

**For Channel Creation (What You Need Now):**
- ✅ Bot token (reset it)
- ✅ Privileged Gateway Intents (enable them)
- ✅ OAuth2 Scopes (`bot`, `applications.commands`)
- ✅ OAuth2 Permissions (`Manage Channels`, etc.)
- ✅ Invite bot to server

**Everything else can wait or skip!**

---

**Focus on Bot Tab and Installation Tab - those are the only critical ones right now!**

