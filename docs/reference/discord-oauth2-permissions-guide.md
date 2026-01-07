# Discord OAuth2 Permissions - What to Select

**Location:** Discord Developer Portal → OAuth2 → URL Generator  
**Purpose:** Configure what permissions your bot gets when invited to servers

---

## ✅ Required Settings for Channel Creation

### **Scopes (Keep Both)**

✅ **`bot`** - Required  
- Enables bot functionality
- Must be selected

✅ **`applications.commands`** - Optional but Recommended  
- Allows slash commands
- Good to have for future features

### **Permissions (Select These)**

✅ **Manage Channels** - **REQUIRED**  
- This is what we need for creating channels
- Without this, bot cannot create channels

**Optional but Recommended:**
- ✅ **Send Messages** - For sending notifications
- ✅ **Read Message History** - For reading channel history
- ✅ **View Channels** - For seeing channels
- ✅ **Use Slash Commands** - If using slash commands

---

## 🎯 Minimal Setup (Just Channel Creation)

**Scopes:**
- ✅ `bot`

**Permissions:**
- ✅ **Manage Channels**

This is the absolute minimum to create channels.

---

## 🚀 Recommended Setup (Full Functionality)

**Scopes:**
- ✅ `bot`
- ✅ `applications.commands`

**Permissions:**
- ✅ **Manage Channels** (required for channel creation)
- ✅ **Send Messages** (for notifications)
- ✅ **Read Message History** (for reading messages)
- ✅ **View Channels** (to see channels)
- ✅ **Use Slash Commands** (for future slash commands)

---

## 📋 Step-by-Step in Discord Portal

1. **Go to:** https://discord.com/developers/applications/1446503100478263368/oauth2/url-generator

2. **Under "Scopes":**
   - Ensure `bot` is selected
   - Ensure `applications.commands` is selected (optional)

3. **Under "Permissions":**
   - Click "Select" dropdown
   - Search for "Manage Channels"
   - ✅ Check "Manage Channels"
   - (Optional) Check other permissions as needed

4. **Copy the generated URL** (appears at bottom of page)

5. **Open URL in browser** and select your server

---

## 🔍 How to Find "Manage Channels" Permission

**In the Permissions dropdown:**
- Scroll down to find "Manage Channels"
- OR search for "Manage"
- OR look under "General Permissions" section

**Full name:** "Manage Channels"  
**Description:** Allows bot to create, edit, or delete channels

---

## ✅ After Selecting Permissions

The page will show a generated URL at the bottom like:
```
https://discord.com/api/oauth2/authorize?client_id=1446503100478263368&permissions=16&scope=bot%20applications.commands
```

**Copy this URL and open it in your browser to invite the bot!**

---

## 🎯 Quick Answer

**Do you need to set all this stuff?**

**Minimum required:**
- ✅ Scopes: `bot`
- ✅ Permissions: **Manage Channels**

**Recommended:**
- ✅ Scopes: `bot` + `applications.commands`
- ✅ Permissions: **Manage Channels** + Send Messages + Read Message History

**Just select "Manage Channels" under Permissions, and you're good to go!**

