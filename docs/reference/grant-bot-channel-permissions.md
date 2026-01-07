# Grant Bot "Manage Channels" Permission

**Date:** 2025-12-08  
**Purpose:** Grant SPECTRA Bot permission to create channels

---

## 🎯 Quick Steps

1. **Open Discord** and go to your **SPECTRA** server

2. **Server Settings:**
   - Right-click on server name → **"Server Settings"**
   - OR click the server name at top → **"Server Settings"**

3. **Go to Roles:**
   - In left sidebar, click **"Roles"**

4. **Find Bot Role:**
   - Look for **"SPECTRA Bot"** role
   - OR find **"@everyone"** role (if bot uses default permissions)
   - OR check what role the bot was assigned when invited

5. **Edit Permissions:**
   - Click on the bot's role (or @everyone)
   - Scroll to **"Advanced Permissions"**
   - Find **"Manage Channels"**
   - Toggle it **ON** ✅

6. **Save:**
   - Click **"Save Changes"**

---

## 🔍 Alternative: Check Bot's Current Role

If you're not sure which role the bot has:

1. Go to your Discord server
2. Click **"Members"** in the right sidebar
3. Find **"SPECTRA Bot"**
4. See what role(s) it has
5. Edit that role's permissions

---

## ✅ After Granting Permission

Once "Manage Channels" is enabled, run:

```bash
python scripts\create_discord_channels.py --channel "data-zephyr-pipelines" --topic "All notifications for Zephyr data pipelines (Source to Analyse stages)."
```

---

**Version:** 1.0.0  
**Date:** 2025-12-08  
**Status:** 🟢 Quick Guide
