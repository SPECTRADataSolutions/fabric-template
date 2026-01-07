# Discord Bot Invite URL - Complete with Permissions

**Application ID:** `1446503100478263368`  
**Server ID:** `1445090868506923030`

---

## ✅ Complete Invite URL (With All Required Permissions)

**For Channel Creation:**
```
https://discord.com/api/oauth2/authorize?client_id=1446503100478263368&permissions=16&scope=bot%20applications.commands
```

**Permissions Breakdown:**
- `permissions=16` = **Manage Channels** permission (required for creating channels)
- `scope=bot` = Bot scope (required)
- `scope=applications.commands` = Slash commands scope (optional but recommended)

---

## 🎯 Full Permissions (Recommended)

**If you want more permissions (Send Messages, Read History, etc.):**
```
https://discord.com/api/oauth2/authorize?client_id=1446503100478263368&permissions=274877906944&scope=bot%20applications.commands
```

**Permission Bits:**
- `274877906944` includes:
  - Manage Channels (16)
  - Send Messages (2048)
  - Read Message History (65536)
  - Use Slash Commands (2147483648)
  - And more...

---

## 📋 How to Use

1. **Copy the complete URL above** (with permissions)
2. **Paste in your browser**
3. **Select your Discord server** (ID: `1445090868506923030`)
4. **Click "Authorize"**
5. **Complete CAPTCHA if prompted**

Bot will appear in your server with the required permissions.

---

## 🔍 Generate Custom URL

**Manual Generation:**
1. Go to: https://discord.com/developers/applications/1446503100478263368/oauth2/url-generator
2. Select scopes:
   - ✅ `bot`
   - ✅ `applications.commands` (optional)
3. Select bot permissions:
   - ✅ **Manage Channels** (required for channel creation)
   - ✅ Send Messages
   - ✅ Read Message History
4. Copy the generated URL from the bottom

---

## ✅ After Inviting Bot

1. **Verify bot is in server:**
   ```bash
   python scripts\check_discord_bot_status.py
   ```
   Should show: ✅ Bot is in target server

2. **Check permissions:**
   - Discord → Your Server → Server Settings → Roles
   - Find bot's role
   - Verify "Manage Channels" is enabled

3. **Test channel creation:**
   ```bash
   python scripts\create_discord_channels.py --all --dry-run
   ```

---

**Use the complete URL above (with permissions) to invite the bot properly!**

