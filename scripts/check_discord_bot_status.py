#!/usr/bin/env python3
"""
Check Discord Bot Status and Configuration

Verifies bot is configured correctly and can access Discord API.
"""

import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

# Load .env from SPECTRA root
script_dir = Path(__file__).resolve().parent
spectra_root = script_dir.parent.parent.parent
env_path = spectra_root / ".env"
if env_path.exists():
    load_dotenv(env_path)
    print(f"✅ Loaded .env from: {env_path}")
else:
    print(f"⚠️  .env not found at: {env_path}")

def get_bot_token() -> str:
    """Get Discord bot token from environment."""
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        raise ValueError("DISCORD_BOT_TOKEN not found in .env file")
    # Strip quotes if present (dotenv may preserve quotes)
    token = token.strip('"\'')
    return token

def get_bot_info():
    """Get bot user information."""
    url = "https://discord.com/api/v10/users/@me"
    headers = {
        "Authorization": f"Bot {get_bot_token()}",
        "Content-Type": "application/json",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            raise ValueError("Invalid bot token - bot token may be expired or incorrect")
        raise RuntimeError(f"Failed to get bot info: {e.response.status_code} {e.response.text}") from e

def get_bot_guilds():
    """Get all guilds (servers) the bot is in."""
    url = "https://discord.com/api/v10/users/@me/guilds"
    headers = {
        "Authorization": f"Bot {get_bot_token()}",
        "Content-Type": "application/json",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            raise ValueError("Invalid bot token")
        elif e.response.status_code == 403:
            return []  # Bot has no guilds or lacks permission to list them
        raise RuntimeError(f"Failed to get bot guilds: {e.response.status_code} {e.response.text}") from e

def get_guild_info(guild_id: str):
    """Get information about a specific guild."""
    url = f"https://discord.com/api/v10/guilds/{guild_id}"
    headers = {
        "Authorization": f"Bot {get_bot_token()}",
        "Content-Type": "application/json",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            raise ValueError("Invalid bot token")
        elif e.response.status_code == 404:
            raise ValueError(f"Guild {guild_id} not found or bot is not in this server")
        elif e.response.status_code == 403:
            raise ValueError(f"Bot lacks permission to access guild {guild_id}")
        raise RuntimeError(f"Failed to get guild info: {e.response.status_code} {e.response.text}") from e

def get_guild_member(guild_id: str, user_id: str):
    """Get bot's member information in a guild."""
    url = f"https://discord.com/api/v10/guilds/{guild_id}/members/{user_id}"
    headers = {
        "Authorization": f"Bot {get_bot_token()}",
        "Content-Type": "application/json",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return None  # Bot is not in this server
        raise RuntimeError(f"Failed to get guild member: {e.response.status_code} {e.response.text}") from e

def main():
    """Main entry point."""
    print("=" * 80)
    print("🔍 DISCORD BOT STATUS CHECK")
    print("=" * 80)
    print()
    
    # 1. Check bot token
    try:
        token = get_bot_token()
        print("✅ Bot token found in .env")
        print(f"   Token: {token[:20]}...{token[-10:]}")
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)
    
    # 2. Get bot info
    print("\n" + "=" * 80)
    print("1️⃣ BOT INFORMATION")
    print("=" * 80)
    try:
        bot_info = get_bot_info()
        bot_id = bot_info["id"]
        bot_username = bot_info["username"]
        bot_discriminator = bot_info.get("discriminator", "0000")
        
        print(f"✅ Bot authenticated successfully")
        print(f"   Username: {bot_username}#{bot_discriminator}")
        print(f"   Bot ID: {bot_id}")
        print(f"   Avatar: {bot_info.get('avatar', 'No avatar')}")
    except (ValueError, RuntimeError) as e:
        print(f"❌ Failed to authenticate bot: {e}")
        sys.exit(1)
    
    # 3. Check bot guilds
    print("\n" + "=" * 80)
    print("2️⃣ BOT GUILDS (SERVERS)")
    print("=" * 80)
    try:
        guilds = get_bot_guilds()
        if not guilds:
            print("⚠️  Bot is not in any servers")
            print("\n💡 To invite bot to your server:")
            print("   1. Go to: https://discord.com/developers/applications/1446503100478263368/oauth2/url-generator")
            print("   2. Select scopes: bot, applications.commands")
            print("   3. Select permissions: Manage Channels, Send Messages, Read Message History")
            print("   4. Copy the generated URL and open it")
            print("   5. Select your server and authorize")
        else:
            print(f"✅ Bot is in {len(guilds)} server(s):")
            for guild in guilds:
                print(f"   - {guild['name']} (ID: {guild['id']})")
    except (ValueError, RuntimeError) as e:
        print(f"⚠️  Could not list guilds: {e}")
        guilds = []
    
    # 4. Check specific guild from .env
    print("\n" + "=" * 80)
    print("3️⃣ TARGET GUILD (FROM .ENV)")
    print("=" * 80)
    guild_id = os.getenv("DISCORD_GUILD_ID")
    if guild_id:
        print(f"   Guild ID from .env: {guild_id}")
        
        # Check if bot is in this guild
        try:
            member_info = get_guild_member(guild_id, bot_id)
            if member_info:
                print(f"✅ Bot is in this server")
                
                # Get guild info
                try:
                    guild_info = get_guild_info(guild_id)
                    print(f"   Server Name: {guild_info['name']}")
                    print(f"   Server ID: {guild_info['id']}")
                    
                    # Check bot's roles
                    member_roles = member_info.get("roles", [])
                    if member_roles:
                        print(f"   Bot Roles: {len(member_roles)} role(s)")
                    else:
                        print(f"   Bot Roles: @everyone (default)")
                    
                    # Check permissions (would need to calculate from roles)
                    print(f"\n💡 To check bot permissions:")
                    print(f"   1. Open Discord → Server: {guild_info['name']}")
                    print(f"   2. Server Settings → Roles")
                    print(f"   3. Find bot's role or @everyone")
                    print(f"   4. Enable 'Manage Channels' permission")
                except (ValueError, RuntimeError) as e:
                    print(f"   ⚠️  Could not get guild info: {e}")
            else:
                print(f"❌ Bot is NOT in this server")
                print(f"\n💡 Invite bot to server:")
                print(f"   Generate OAuth2 URL: https://discord.com/developers/applications/1446503100478263368/oauth2/url-generator")
        except (ValueError, RuntimeError) as e:
            print(f"❌ {e}")
    else:
        print("⚠️  DISCORD_GUILD_ID not set in .env")
    
    # 5. Summary
    print("\n" + "=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    
    if guild_id and member_info:
        print("✅ Bot is configured and in target server")
        print("💡 Next: Grant 'Manage Channels' permission in Discord server settings")
    elif guild_id:
        print("⚠️  Bot token is valid, but bot is not in target server")
        print("💡 Next: Invite bot to server using OAuth2 URL")
    else:
        print("⚠️  DISCORD_GUILD_ID not configured")
        print("💡 Next: Set DISCORD_GUILD_ID in .env file")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()

