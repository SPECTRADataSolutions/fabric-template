# Create Discord Developer Team and Add App

**Date:** 2025-12-08  
**Purpose:** Create a Developer Team and add SPECTRA Bot to it (required for app verification)

---

## 🎯 Why Create a Team?

Discord requires apps to belong to a **Developer Team** for:
- App verification (required after 75-100 servers)
- Team collaboration on apps
- Proper app ownership structure
- Resolving 401 authentication issues

---

## 📋 Step-by-Step Instructions

### Step 1: Create a Developer Team

1. **Go to Discord Developer Portal:**
   - Navigate to: https://discord.com/developers/applications
   - Log in with your Discord account

2. **Access Team Settings:**
   - Look for a **"Teams"** section in the left sidebar (may be at the bottom)
   - OR click on your profile icon/name in the top right
   - Look for **"Create Team"** or **"Teams"** option

3. **Create Team:**
   - Click **"Create Team"** button
   - Enter team name: **"SPECTRA Development"** (or your preferred name)
   - Select team members (optional - you can add members later)
   - Click **"Create Team"**

4. **Team Created:**
   - You'll be redirected to the team dashboard
   - Note the Team ID (if visible)

---

### Step 2: Add Application to Team

1. **Navigate to Application:**
   - Go back to: https://discord.com/developers/applications
   - Click on **"SPECTRA Bot"** (Application ID: `1446503100478263368`)

2. **Go to General Information:**
   - In the left sidebar, click **"General Information"**

3. **Transfer Ownership/Add to Team:**
   - Look for an **"Ownership"** or **"Team"** section
   - There should be an option to:
     - **"Transfer to Team"** OR
     - **"Add to Team"** OR
     - **"Change Owner"** → Select your team
   
   - **If you see "OWNERSHIP" showing your username:**
     - Click **"Change Owner"** button
     - Select your team from the dropdown
     - Confirm the transfer

4. **Alternative Path (If transfer option not visible):**
   - Go to your **Team dashboard**
   - Look for **"Apps"** or **"Applications"** section
   - Click **"Add Application"** or **"Transfer Application"**
   - Select **"SPECTRA Bot"** from the list
   - Confirm the transfer

---

### Step 3: Verify Team Association

1. **Check Application Settings:**
   - Go back to: https://discord.com/developers/applications/1446503100478263368/general
   - Under **"General Information"**, verify:
     - **OWNERSHIP** should now show your team name (e.g., "SPECTRA Development")
     - NOT your personal username

2. **Check App Verification Page:**
   - Navigate to: https://discord.com/developers/applications/1446503100478263368/verification-onboarding
   - Under **"Verification Qualifications"**:
     - ✅ **"Your app must belong to a Team"** should now show a **green checkmark** instead of a warning

---

### Step 4: Test Bot Token Again

After adding the app to a team:

1. **Reset Bot Token (if still having issues):**
   - Go to: https://discord.com/developers/applications/1446503100478263368/bot
   - Scroll to **"Token"** section
   - Click **"Reset Token"**
   - Copy the new token immediately

2. **Update .env file:**
   ```bash
   python scripts\update_bot_token.py
   ```
   Or manually update:
   ```
   DISCORD_BOT_TOKEN="new_token_here"
   ```

3. **Test token:**
   ```bash
   python scripts\test_bot_token_direct.py
   ```

---

## 🔍 Troubleshooting

### If "Create Team" is not visible:

- **Check if you already have a team:**
  - Look for "Teams" in the sidebar
  - You might already be in a team

- **Check permissions:**
  - You must be logged in with a Discord account that can create teams
  - Some accounts may have restrictions

### If "Transfer to Team" is not visible:

- **Try the Team dashboard:**
  - Go to your team page
  - Look for "Apps" or "Applications" section
  - Use "Add Application" from there

- **Check app ownership:**
  - If app is already owned by a team, you may need team admin permissions

### If token still doesn't work after team transfer:

- **Wait a few minutes:** Team association may take a moment to propagate
- **Reset token again:** New ownership may require token reset
- **Check bot permissions:** Ensure bot still has necessary permissions in the server

---

## ✅ Success Indicators

You'll know it worked when:

1. ✅ App shows team name in "OWNERSHIP" field (not your username)
2. ✅ App Verification page shows green checkmark for "belongs to a Team"
3. ✅ Bot token authenticates successfully (200 status code)
4. ✅ Bot can access Discord API endpoints

---

## 📚 Reference Links

- [Discord Developer Portal Teams](https://discord.com/developers/docs/topics/teams)
- [Discord App Verification Requirements](https://discord.com/developers/docs/topics/gateway#verification-requirement)

---

**Version:** 1.0.0  
**Date:** 2025-12-08  
**Status:** 🟢 Step-by-Step Guide
