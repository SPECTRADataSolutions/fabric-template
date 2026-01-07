#!/usr/bin/env python3
"""
Comprehensive Discord Bot Diagnostic Tool
Checks token, configuration, and all settings
"""

import os
import sys
import json
import requests
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, Any, Optional

# Load .env from SPECTRA root
spectra_root = Path(__file__).parent.parent.parent.parent
env_path = spectra_root / ".env"
if env_path.exists():
    load_dotenv(env_path)
    print(f"✅ Loaded .env from: {env_path}")
else:
    print(f"❌ .env file not found at: {env_path}")
    sys.exit(1)

def get_bot_token() -> Optional[str]:
    """Get bot token from environment, handling quotes."""
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        return None
    # Strip quotes if present
    return token.strip('"').strip("'")

def get_guild_id() -> Optional[str]:
    """Get guild ID from environment."""
    guild_id = os.getenv("DISCORD_GUILD_ID")
    return guild_id.strip('"').strip("'") if guild_id else None

def test_token_direct(token: str) -> Dict[str, Any]:
    """Test token with direct API call."""
    url = "https://discord.com/api/v10/users/@me"
    headers = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        return {
            "status_code": response.status_code,
            "success": response.status_code == 200,
            "data": response.json() if response.text else None,
            "error": None if response.status_code == 200 else response.text
        }
    except Exception as e:
        return {
            "status_code": 0,
            "success": False,
            "data": None,
            "error": str(e)
        }

def check_token_format(token: str) -> Dict[str, Any]:
    """Check if token format is correct."""
    issues = []
    
    if not token:
        issues.append("Token is empty")
        return {"valid": False, "issues": issues}
    
    parts = token.split(".")
    if len(parts) != 3:
        issues.append(f"Token should have 3 parts separated by dots, found {len(parts)}")
    
    if len(token) < 59:
        issues.append(f"Token too short ({len(token)} chars, expected ~59-72)")
    
    if len(token) > 72:
        issues.append(f"Token too long ({len(token)} chars, expected ~59-72)")
    
    # Check for common issues
    if " " in token:
        issues.append("Token contains spaces (should be removed)")
    
    if "\n" in token or "\r" in token:
        issues.append("Token contains newlines (should be removed)")
    
    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "parts": len(parts),
        "length": len(token)
    }

def main():
    print("=" * 80)
    print("🔍 COMPREHENSIVE DISCORD BOT DIAGNOSTIC")
    print("=" * 80)
    
    # 1. Check .env file
    print("\n1️⃣ CHECKING .env FILE")
    print("-" * 80)
    
    token = get_bot_token()
    if not token:
        print("❌ DISCORD_BOT_TOKEN not found in .env file")
        print("   Please add: DISCORD_BOT_TOKEN=your_token_here")
        sys.exit(1)
    
    print(f"✅ Token found in .env")
    print(f"   Length: {len(token)} characters")
    print(f"   First 20 chars: {token[:20]}...")
    print(f"   Last 10 chars: ...{token[-10:]}")
    
    # 2. Check token format
    print("\n2️⃣ CHECKING TOKEN FORMAT")
    print("-" * 80)
    format_check = check_token_format(token)
    if format_check["valid"]:
        print(f"✅ Token format looks correct")
        print(f"   Parts: {format_check['parts']}")
        print(f"   Length: {format_check['length']}")
    else:
        print("❌ Token format issues:")
        for issue in format_check["issues"]:
            print(f"   - {issue}")
        print("\n⚠️  Fix format issues before continuing")
    
    # 3. Test token with Discord API
    print("\n3️⃣ TESTING TOKEN WITH DISCORD API")
    print("-" * 80)
    print(f"Making request to: https://discord.com/api/v10/users/@me")
    print(f"Authorization header: Bot {token[:30]}...")
    
    result = test_token_direct(token)
    
    if result["success"]:
        print("✅ Token is VALID and working!")
        bot_info = result["data"]
        print(f"   Bot Username: {bot_info.get('username')}#{bot_info.get('discriminator')}")
        print(f"   Bot ID: {bot_info.get('id')}")
        print(f"   Verified: {'Yes' if bot_info.get('verified') else 'No'}")
        print(f"   Bot: {'Yes' if bot_info.get('bot') else 'No'}")
    else:
        print(f"❌ Token authentication FAILED")
        print(f"   Status Code: {result['status_code']}")
        if result['error']:
            try:
                error_json = json.loads(result['error'])
                print(f"   Error Message: {error_json.get('message', 'Unknown error')}")
                print(f"   Error Code: {error_json.get('code', 'N/A')}")
            except:
                print(f"   Error: {result['error']}")
        
        print("\n🔍 DIAGNOSIS:")
        if result['status_code'] == 401:
            print("   401 Unauthorized typically means:")
            print("   - Token is incorrect or invalid")
            print("   - Token was reset but old one is still in use")
            print("   - Token has extra characters/spaces")
            print("   - Bot was deleted and recreated")
            print("\n   💡 ACTION: Verify token in Discord Developer Portal:")
            print("   1. Go to: https://discord.com/developers/applications/1446503100478263368/bot")
            print("   2. Check if token matches what's in .env")
            print("   3. If token shows as masked, you MUST reset it")
            print("   4. Copy new token immediately after reset")
    
    # 4. Check Guild ID
    print("\n4️⃣ CHECKING GUILD (SERVER) ID")
    print("-" * 80)
    guild_id = get_guild_id()
    if guild_id:
        print(f"✅ DISCORD_GUILD_ID found: {guild_id}")
        
        # Test if bot can see the guild
        if result["success"]:
            bot_id = result["data"].get("id")
            if bot_id:
                url = f"https://discord.com/api/v10/users/@me/guilds/{guild_id}/member"
                headers = {
                    "Authorization": f"Bot {token}",
                    "Content-Type": "application/json",
                }
                try:
                    guild_response = requests.get(url, headers=headers, timeout=10)
                    if guild_response.status_code == 200:
                        print(f"✅ Bot is a member of the server")
                    elif guild_response.status_code == 404:
                        print(f"⚠️  Bot is NOT a member of server {guild_id}")
                        print("   You may need to invite the bot to the server")
                except Exception as e:
                    print(f"⚠️  Could not verify guild membership: {e}")
    else:
        print("⚠️  DISCORD_GUILD_ID not found in .env")
        print("   This is optional for token testing but required for channel creation")
    
    # 5. Summary and Recommendations
    print("\n" + "=" * 80)
    print("📋 SUMMARY AND RECOMMENDATIONS")
    print("=" * 80)
    
    if result["success"]:
        print("✅ Bot token is working correctly!")
        print("\n✅ Next steps:")
        print("   1. Test channel creation: python scripts\\create_discord_channels.py --all")
        print("   2. Verify bot permissions in Discord server")
    else:
        print("❌ Bot token is NOT working")
        print("\n🔧 Troubleshooting steps:")
        print("   1. Go to Discord Developer Portal Bot page")
        print("   2. If token is masked (shows as dots), you MUST reset it")
        print("   3. Click 'Reset Token' and copy the NEW token immediately")
        print("   4. Update .env file: DISCORD_BOT_TOKEN=\"new_token_here\"")
        print("   5. Verify token format: 3 parts, ~70 chars, no spaces")
        print("   6. Run this diagnostic again")
        print("\n⚠️  Common issues:")
        print("   - Token copied with extra spaces/newlines")
        print("   - Old token still in .env after reset")
        print("   - Token format incorrect (missing parts)")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
