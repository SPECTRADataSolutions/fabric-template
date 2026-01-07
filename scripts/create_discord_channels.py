#!/usr/bin/env python3
"""
Create Discord Channels for SPECTRA Pipeline Notifications

Creates channels in Discord server using Discord Bot API.
Requires DISCORD_BOT_TOKEN and DISCORD_GUILD_ID environment variables.

Usage:
    python create_discord_channels.py --channel "data-zephyr-pipelines"
    python create_discord_channels.py --all  # Create all recommended channels
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any

import requests
from dotenv import load_dotenv

# Load .env from SPECTRA root
# Script is at: Data/zephyr/scripts/create_discord_channels.py
# SPECTRA root is 3 levels up: Data/zephyr/scripts -> Data/zephyr -> Data -> SPECTRA
script_dir = Path(__file__).resolve().parent
spectra_root = script_dir.parent.parent.parent  # Up to SPECTRA root
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
        raise ValueError(
            "DISCORD_BOT_TOKEN not found in environment. "
            "Set it in .env file at SPECTRA root."
        )
    # Strip quotes if present (dotenv may preserve quotes)
    token = token.strip('"\'')
    return token


def get_discord_headers() -> Dict[str, str]:
    """Get headers for Discord API requests."""
    return {
        "Authorization": f"Bot {get_bot_token()}",
        "Content-Type": "application/json",
    }


def list_bot_guilds() -> List[Dict[str, Any]]:
    """List all Discord guilds (servers) the bot belongs to."""
    url = "https://discord.com/api/v10/users/@me/guilds"
    headers = get_discord_headers()
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(
            f"Failed to list guilds: {e.response.status_code} {e.response.text}"
        ) from e


def get_guild_id() -> str:
    """Get Discord guild (server) ID from environment or auto-detect."""
    guild_id = os.getenv("DISCORD_GUILD_ID")
    
    if guild_id:
        return guild_id
    
    # Try to auto-detect if bot is in only one guild
    try:
        guilds = list_bot_guilds()
        if len(guilds) == 1:
            auto_guild_id = guilds[0]["id"]
            print(f"🔍 Auto-detected Guild ID: {auto_guild_id} ({guilds[0]['name']})")
            return auto_guild_id
        elif len(guilds) > 1:
            print("⚠️  Bot is in multiple servers. Please set DISCORD_GUILD_ID in .env file.")
            print("\nAvailable servers:")
            for i, guild in enumerate(guilds, 1):
                print(f"   {i}. {guild['name']} (ID: {guild['id']})")
            raise ValueError(
                "Multiple guilds found. Set DISCORD_GUILD_ID in .env file to specify which server to use."
            )
        else:
            raise ValueError("Bot is not in any Discord servers.")
    except (RuntimeError, ValueError) as e:
        # If auto-detection fails, provide manual instructions
        raise ValueError(
            f"{str(e)}\n\n"
            "To get your Guild ID manually:\n"
            "1. Enable Developer Mode: Discord Settings → Advanced → Developer Mode (ON)\n"
            "2. Right-click your server name → 'Copy Server ID'\n"
            "3. Add to .env: DISCORD_GUILD_ID=your_server_id_here"
        ) from e


def get_discord_headers() -> Dict[str, str]:
    """Get headers for Discord API requests."""
    return {
        "Authorization": f"Bot {get_bot_token()}",
        "Content-Type": "application/json",
    }


def create_discord_channel(
    name: str,
    channel_type: int = 0,
    category_id: Optional[str] = None,
    topic: Optional[str] = None,
) -> Dict:
    """
    Create a Discord channel in the guild.
    
    Args:
        name: Channel name (without #)
        channel_type: Channel type (0 = text, 2 = voice, 4 = category)
        category_id: Optional category ID to nest channel under
        topic: Optional channel topic/description
    
    Returns:
        Channel data from Discord API
    """
    guild_id = get_guild_id()
    url = f"https://discord.com/api/v10/guilds/{guild_id}/channels"
    
    payload = {
        "name": name,
        "type": channel_type,
    }
    
    if category_id:
        payload["parent_id"] = category_id
    
    if topic:
        payload["topic"] = topic
    
    headers = get_discord_headers()
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        error_detail = ""
        if e.response.status_code == 403:
            error_detail = " (Bot may lack 'Manage Channels' permission)"
        elif e.response.status_code == 404:
            error_detail = " (Guild ID may be incorrect)"
        elif e.response.status_code == 400:
            error_detail = " (Channel name may be invalid or already exists)"
        
        raise RuntimeError(
            f"Failed to create channel '{name}': {e.response.status_code} {e.response.text}{error_detail}"
        ) from e


def channel_exists(name: str) -> Optional[Dict]:
    """Check if a channel already exists in the guild."""
    guild_id = get_guild_id()
    url = f"https://discord.com/api/v10/guilds/{guild_id}/channels"
    
    headers = get_discord_headers()
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        channels = response.json()
        
        # Search for channel by name (case-insensitive)
        for channel in channels:
            if channel.get("name", "").lower() == name.lower():
                return channel
        return None
    except requests.exceptions.HTTPError as e:
        print(f"⚠️  Warning: Could not check for existing channels: {e}")
        return None


def create_webhook(channel_id: str, name: str, avatar_url: Optional[str] = None) -> Dict:
    """
    Create a webhook for a Discord channel.
    
    Requires "Manage Webhooks" permission for the bot.
    
    Args:
        channel_id: Discord channel ID
        name: Webhook name
        avatar_url: Optional avatar URL for webhook
    
    Returns:
        Webhook data from Discord API (includes webhook URL in 'url' field)
    """
    url = f"https://discord.com/api/v10/channels/{channel_id}/webhooks"
    
    payload = {
        "name": name,
    }
    
    if avatar_url:
        payload["avatar"] = avatar_url
    
    headers = get_discord_headers()
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        error_detail = ""
        if e.response.status_code == 403:
            error_detail = " (Bot may lack 'Manage Webhooks' permission)"
        elif e.response.status_code == 404:
            error_detail = " (Channel ID may be incorrect)"
        
        raise RuntimeError(
            f"Failed to create webhook in channel {channel_id}: {e.response.status_code} {e.response.text}{error_detail}"
        ) from e


def get_channel_webhooks(channel_id: str) -> List[Dict]:
    """List all webhooks for a channel."""
    url = f"https://discord.com/api/v10/channels/{channel_id}/webhooks"
    headers = get_discord_headers()
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"⚠️  Warning: Could not list webhooks for channel {channel_id}: {e}")
        return []


# Recommended channels from DISCORD-CHANNEL-STRUCTURE.md
RECOMMENDED_CHANNELS = [
    {
        "name": "data-zephyr-pipelines",
        "topic": "Zephyr Enterprise pipeline notifications (all stages: source, prepare, extract, clean, transform, refine, analyse)",
    },
    {
        "name": "data-jira-pipelines",
        "topic": "Jira pipeline notifications (all stages: source, prepare, extract, clean, transform, refine, analyse)",
    },
    {
        "name": "data-xero-pipelines",
        "topic": "Xero pipeline notifications (all stages: source, prepare, extract, clean, transform, refine, analyse)",
    },
    {
        "name": "data-unifi-pipelines",
        "topic": "UniFi pipeline notifications (all stages: source, prepare, extract, clean, transform, refine, analyse)",
    },
]


def create_all_recommended_channels(dry_run: bool = False) -> Dict[str, List[str]]:
    """Create all recommended pipeline channels."""
    results = {
        "created": [],
        "exists": [],
        "errors": [],
    }
    
    print("=" * 80)
    print("🚀 CREATING RECOMMENDED DISCORD CHANNELS")
    print("=" * 80)
    print(f"Guild ID: {get_guild_id()}")
    print(f"Dry Run: {dry_run}\n")
    
    for channel_config in RECOMMENDED_CHANNELS:
        name = channel_config["name"]
        topic = channel_config.get("topic", "")
        
        print(f"📋 Channel: #{name}")
        
        # Check if exists
        existing = channel_exists(name)
        if existing:
            print(f"   ⚠️  Already exists (ID: {existing.get('id')})")
            results["exists"].append(name)
            continue
        
        if dry_run:
            print(f"   🔍 Would create (dry run)")
            results["created"].append(name)
            continue
        
        try:
            channel = create_discord_channel(name=name, topic=topic)
            channel_id = channel.get('id')
            print(f"   ✅ Created (ID: {channel_id})")
            
            # Create webhook for the channel
            try:
                webhook_name = f"SPECTRA {name.replace('data-', '').replace('-pipelines', '').title()} Pipeline"
                existing_webhooks = get_channel_webhooks(channel_id)
                webhook_exists = any(w.get('name') == webhook_name for w in existing_webhooks)
                
                if not webhook_exists:
                    webhook = create_webhook(channel_id=channel_id, name=webhook_name)
                    webhook_url = webhook.get('url', '')
                    print(f"   🔗 Webhook created: {webhook_url[:50]}...")
                    print(f"      ⚠️  Copy URL immediately - won't be shown again!")
                else:
                    print(f"   🔗 Webhook already exists for this channel")
            except Exception as e:
                print(f"   ⚠️  Webhook creation skipped: {e}")
            
            results["created"].append(name)
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results["errors"].append(f"{name}: {str(e)}")
        
        print()
    
    return results


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Create Discord channels for SPECTRA pipeline notifications"
    )
    parser.add_argument(
        "--channel",
        type=str,
        help="Create a single channel by name (e.g., 'data-zephyr-pipelines')",
    )
    parser.add_argument(
        "--topic",
        type=str,
        help="Channel topic/description (only used with --channel)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Create all recommended channels from DISCORD-CHANNEL-STRUCTURE.md",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be created without actually creating",
    )
    
    args = parser.parse_args()
    
    if not args.channel and not args.all:
        parser.print_help()
        print("\n❌ Error: Must specify either --channel or --all")
        sys.exit(1)
    
    try:
        if args.all:
            results = create_all_recommended_channels(dry_run=args.dry_run)
            
            print("=" * 80)
            print("📊 SUMMARY")
            print("=" * 80)
            print(f"✅ Created: {len(results['created'])}")
            if results["created"]:
                for name in results["created"]:
                    print(f"   - #{name}")
            
            print(f"\n⚠️  Already Exists: {len(results['exists'])}")
            if results["exists"]:
                for name in results["exists"]:
                    print(f"   - #{name}")
            
            print(f"\n❌ Errors: {len(results['errors'])}")
            if results["errors"]:
                for error in results["errors"]:
                    print(f"   - {error}")
            
            if results["errors"]:
                sys.exit(1)
        else:
            # Create single channel
            name = args.channel
            topic = args.topic or ""
            
            print(f"🚀 Creating channel: #{name}")
            
            # Check if exists
            existing = channel_exists(name)
            if existing:
                channel_id = existing.get('id')
                print(f"⚠️  Channel already exists (ID: {channel_id})")
                print(f"   URL: https://discord.com/channels/{get_guild_id()}/{channel_id}")
                
                # Check for existing webhook
                try:
                    webhook_name = f"SPECTRA {name.replace('data-', '').replace('-pipelines', '').title()} Pipeline"
                    existing_webhooks = get_channel_webhooks(channel_id)
                    webhook_exists = any(w.get('name') == webhook_name for w in existing_webhooks)
                    
                    if webhook_exists:
                        print(f"\n🔗 Checking for existing webhook...")
                        for webhook in existing_webhooks:
                            if webhook.get('name') == webhook_name:
                                webhook_url = webhook.get('url', '')
                                if webhook_url:
                                    print(f"   ✅ Webhook found: {webhook_name}")
                                    print(f"   📋 Webhook URL: {webhook_url}")
                                    print(f"   ⚠️  Note: URL only visible once - if empty, create new webhook")
                                else:
                                    print(f"   ⚠️  Webhook exists but URL not available")
                                break
                    else:
                        print(f"\n🔗 No webhook found. Creating webhook...")
                        webhook = create_webhook(channel_id=channel_id, name=webhook_name)
                        webhook_url = webhook.get('url', '')
                        print(f"   ✅ Webhook created!")
                        print(f"   📋 Webhook URL: {webhook_url}")
                        print(f"   ⚠️  CRITICAL: Copy this URL now!")
                        source_system = name.replace('data-', '').replace('-pipelines', '').upper()
                        print(f"\n💡 Add to Variable Library:")
                        print(f"   DISCORD_WEBHOOK_URL_{source_system} = {webhook_url}")
                except Exception as e:
                    print(f"   ⚠️  Could not check/create webhook: {e}")
                
                sys.exit(0)
            
            if args.dry_run:
                print(f"🔍 Would create channel (dry run)")
                sys.exit(0)
            
            channel = create_discord_channel(name=name, topic=topic)
            channel_id = channel.get('id')
            print(f"✅ Channel created successfully!")
            print(f"   ID: {channel_id}")
            print(f"   URL: https://discord.com/channels/{get_guild_id()}/{channel_id}")
            
            # Create webhook for the channel
            try:
                # Generate webhook name from channel name
                webhook_name = f"SPECTRA {name.replace('data-', '').replace('-pipelines', '').title()} Pipeline"
                print(f"\n🔗 Creating webhook: {webhook_name}")
                
                # Check if webhook already exists
                existing_webhooks = get_channel_webhooks(channel_id)
                webhook_exists = any(w.get('name') == webhook_name for w in existing_webhooks)
                
                if webhook_exists:
                    print(f"   ⚠️  Webhook '{webhook_name}' already exists")
                    for webhook in existing_webhooks:
                        if webhook.get('name') == webhook_name:
                            print(f"   📋 Webhook URL: {webhook.get('url', 'N/A')}")
                            print(f"   ⚠️  Copy this URL - you won't be able to see it again!")
                            break
                else:
                    webhook = create_webhook(channel_id=channel_id, name=webhook_name)
                    webhook_url = webhook.get('url', '')
                    print(f"   ✅ Webhook created successfully!")
                    print(f"   📋 Webhook URL: {webhook_url}")
                    print(f"   ⚠️  CRITICAL: Copy this URL now - you won't be able to see it again!")
                    print(f"\n💡 Add to Variable Library:")
                    source_system = name.replace('data-', '').replace('-pipelines', '').upper()
                    print(f"   DISCORD_WEBHOOK_URL_{source_system} = {webhook_url}")
            except Exception as e:
                print(f"   ⚠️  Could not create webhook: {e}")
                print(f"   💡 You can create it manually in Discord channel settings")
            
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        sys.exit(1)
    except RuntimeError as e:
        print(f"❌ Discord API Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

