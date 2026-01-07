#!/usr/bin/env python3
"""Create webhook for a Discord channel using bot token."""

import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load .env
spectra_root = Path(__file__).parent.parent.parent.parent
env_path = spectra_root / ".env"
load_dotenv(env_path)

# Get credentials
token = os.getenv("DISCORD_BOT_TOKEN", "").strip('"\'')
channel_id = "1447577489231577188"  # data-zephyr-pipelines channel ID from earlier

if not token:
    print("❌ DISCORD_BOT_TOKEN not found")
    sys.exit(1)

# Test token first
print("🔍 Testing bot token...")
headers = {"Authorization": f"Bot {token}", "Content-Type": "application/json"}
test_response = requests.get("https://discord.com/api/v10/users/@me", headers=headers, timeout=10)
if test_response.status_code != 200:
    print(f"❌ Token test failed: {test_response.status_code} {test_response.text}")
    sys.exit(1)
print(f"✅ Token works! Bot: {test_response.json().get('username')}")

# Create webhook
print(f"\n🔗 Creating webhook for channel {channel_id}...")
webhook_url = f"https://discord.com/api/v10/channels/{channel_id}/webhooks"
payload = {"name": "SPECTRA Zephyr Pipeline"}

webhook_response = requests.post(webhook_url, json=payload, headers=headers, timeout=10)
if webhook_response.status_code == 200:
    webhook_data = webhook_response.json()
    webhook_url_value = webhook_data.get("url", "")
    print(f"✅ Webhook created!")
    print(f"📋 Webhook URL: {webhook_url_value}")
    print(f"\n💡 Add to Variable Library:")
    print(f'   "name": "DISCORD_WEBHOOK_URL_ZEPHYR",')
    print(f'   "value": "{webhook_url_value}"')
else:
    print(f"❌ Failed: {webhook_response.status_code} {webhook_response.text}")
    sys.exit(1)

