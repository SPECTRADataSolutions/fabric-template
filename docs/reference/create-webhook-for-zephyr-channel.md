# Create Webhook for Zephyr Pipeline Channel

**Date:** 2025-12-08  
**Purpose:** Set up Discord webhook for `#data-zephyr-pipelines` channel

---

## 📋 Steps to Create Webhook

1. **Go to the Channel:**
   - Open Discord → SPECTRA server
   - Navigate to `#data-zephyr-pipelines` channel

2. **Open Channel Settings:**
   - Click the gear icon ⚙️ next to the channel name (top right)
   - OR right-click channel name → "Edit Channel"

3. **Go to Integrations:**
   - In the left sidebar, click **"Integrations"**
   - Then click **"Webhooks"**

4. **Create Webhook:**
   - Click **"New Webhook"** button
   - Give it a name: **"SPECTRA Zephyr Pipeline"**
   - Optionally, set an avatar/icon
   - Click **"Save Changes"**

5. **Copy Webhook URL:**
   - The webhook URL will be displayed
   - It looks like: `https://discord.com/api/webhooks/1234567890/abcdefghijklmnopqrstuvwxyz...`
   - Click **"Copy Webhook URL"**
   - **⚠️ Save this immediately - you won't be able to see it again!**

6. **Add to Variable Library:**
   - Add to `zephyrVariables.VariableLibrary/variables.json`:
   ```json
   {
     "name": "DISCORD_WEBHOOK_URL_ZEPHYR",
     "note": "Discord webhook URL for Zephyr pipeline notifications (data-zephyr-pipelines channel)",
     "type": "String",
     "value": "https://discord.com/api/webhooks/YOUR_WEBHOOK_URL_HERE"
   }
   ```

---

## ✅ After Adding Webhook

Once the webhook URL is in the Variable Library:
1. Sync to Fabric (Git sync)
2. Run `sourceZephyr` notebook
3. The source stage will automatically send a completion notification to Discord!

---

## 🔍 SDK Webhook Resolution

The SDK will look for webhook URLs in this order:
1. `DISCORD_WEBHOOK_URL_ZEPHYR` (source-specific)
2. `DISCORD_WEBHOOK_URL` (generic fallback)

So if you add `DISCORD_WEBHOOK_URL_ZEPHYR`, it will be used automatically!

---

**Version:** 1.0.0  
**Date:** 2025-12-08  
**Status:** 🟢 Quick Guide
