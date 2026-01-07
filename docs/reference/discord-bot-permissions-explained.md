# Discord Bot Permissions - Explained

**Date:** 2025-12-08  
**Purpose:** Clarify Discord bot roles vs permissions vs apps

---

## 🤔 What We Have

**SPECTRA has a Discord Application with a Bot:**

- ✅ **Application Created:** "SPECTRA Bot"
- ✅ **Application ID:** `1446503100478263368`
- ✅ **Public Key:** `9ad1cd63cde0937553ab5618d196fadea429f8d5dcd831f4de3b57fda3b4fdd`
- ✅ **Bot Token:** Exists in `.env` file

---

## 🎯 The Question: Roles vs Permissions

### **Do we need roles if we have a Discord app?**

**Short answer:** **NO - you don't need to create roles manually.**

**What you DO need:** **PERMISSIONS** (granted when bot is invited, or via server settings)

---

## 📚 How Discord Bot Permissions Work

### **1. Discord Application = Bot Container**

When you create a Discord Application and add a "Bot User" to it:
- You get a bot that can be invited to servers
- The bot automatically gets a role when invited (Discord handles this)
- The bot's permissions are set during the invite OR via server settings

### **2. Inviting the Bot (OAuth2 URL)**

**When you invite the bot, you select permissions:**

```
https://discord.com/api/oauth2/authorize?
  client_id=1446503100478263368&
  permissions=274877906944&  ← This number = permission bits
  scope=bot%20applications.commands
```

**The `permissions` parameter sets what the bot can do:**
- `274877906944` = Calculated from selected permissions
- Includes: Send Messages, Read Message History, Manage Channels, etc.

### **3. After Invite: Bot Gets Auto Role**

When the bot joins your server:
- Discord automatically creates a role for the bot (named after the bot)
- This role has the permissions you selected during invite
- **You don't need to manually create a role**

---

## ✅ What We Need for Channel Creation

### **Option 1: Re-invite Bot with Correct Permissions**

**Generate new OAuth2 URL with "Manage Channels" permission:**

1. Go to: https://discord.com/developers/applications/1446503100478263368/oauth2/url-generator
2. Select scopes:
   - ✅ `bot`
   - ✅ `applications.commands`
3. Select bot permissions:
   - ✅ **Manage Channels** (required for creating channels)
   - ✅ Send Messages
   - ✅ Read Message History
   - ✅ Use Slash Commands
4. Copy the generated URL
5. Open URL in browser and re-authorize (or kick bot and re-invite)

### **Option 2: Grant Permissions via Server Settings** (Easier)

1. Open Discord → Your Server
2. Server Settings → Roles
3. Find the bot's role (should be named "SPECTRA Bot" or similar)
4. Click on the role
5. In Permissions, enable:
   - ✅ **Manage Channels**
   - ✅ Send Messages (if not already enabled)
   - ✅ Read Message History (if not already enabled)
6. Save changes

---

## 🔍 How to Verify Bot is in Server

**Check if bot is in your server:**

1. Open Discord → Your Server
2. Member list (right sidebar)
3. Look for "SPECTRA Bot" (should have bot badge 🤖)
4. If not there, bot needs to be invited

**If bot is missing:**
- Generate OAuth2 invite URL (see Option 1 above)
- Open URL and select your server
- Authorize

---

## 🎯 For Creating Channels: What We Need

**Minimum Requirements:**

1. ✅ Bot must be invited to server
2. ✅ Bot must have "Manage Channels" permission
3. ✅ Bot token must be valid

**No need for:**
- ❌ Manually creating roles
- ❌ Assigning bot to custom roles
- ❌ Complex role hierarchies

---

## 🚨 Current Issue: 401 Unauthorized

**The 401 error likely means:**

1. **Bot not in server** - Need to invite via OAuth2 URL
2. **Bot lacks permissions** - Need to grant "Manage Channels"
3. **Invalid token** - Token may have been reset or expired

**Fix:**
1. Verify bot is in server (check member list)
2. Grant "Manage Channels" permission (Server Settings → Roles → Bot Role)
3. Verify token in `.env` matches Developer Portal

---

## 📋 Quick Checklist

- [ ] Bot is in Discord server (visible in member list)
- [ ] Bot has "Manage Channels" permission (Server Settings → Roles)
- [ ] Bot token in `.env` matches Developer Portal
- [ ] Bot has "Send Messages" permission (for notifications)
- [ ] `DISCORD_GUILD_ID` is set in `.env`

---

**Summary:** You have the Discord Application/Bot. You just need to ensure it's invited to your server and has the right permissions. No manual role creation needed - Discord handles that automatically when you invite the bot.

