#!/usr/bin/env python3
"""
Test Discord Webhook Notification

Tests sending a notification to Discord using webhook URL.
Webhooks don't require bot tokens - just the webhook URL.
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

def test_webhook(webhook_url: str, message: str = "🧪 Test notification from SPECTRA Zephyr pipeline"):
    """Send a test message to Discord webhook."""
    if not webhook_url:
        raise ValueError("Webhook URL is required")
    
    # Remove quotes if present
    webhook_url = webhook_url.strip('"\'')
    
    payload = {
        "content": message
    }
    
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()
        return True, "Message sent successfully"
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return False, "Webhook not found (404) - webhook may have been deleted"
        elif e.response.status_code == 401:
            return False, "Unauthorized (401) - webhook URL may be invalid"
        return False, f"HTTP {e.response.status_code}: {e.response.text}"
    except requests.exceptions.RequestException as e:
        return False, f"Request failed: {str(e)}"

def main():
    """Main entry point."""
    print("=" * 80)
    print("🧪 DISCORD WEBHOOK TEST")
    print("=" * 80)
    print()
    
    # Try DISCORD_WEBHOOK_URL_CHAT first
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL_CHAT")
    webhook_name = "DISCORD_WEBHOOK_URL_CHAT"
    
    # Fallback to generic DISCORD_WEBHOOK_URL
    if not webhook_url:
        webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
        webhook_name = "DISCORD_WEBHOOK_URL"
    
    if not webhook_url:
        print("❌ No webhook URL found in .env")
        print("\n💡 Add one of these to .env:")
        print("   DISCORD_WEBHOOK_URL_CHAT=https://discordapp.com/api/webhooks/...")
        print("   OR")
        print("   DISCORD_WEBHOOK_URL=https://discordapp.com/api/webhooks/...")
        sys.exit(1)
    
    print(f"✅ Found webhook URL: {webhook_name}")
    print(f"   URL: {webhook_url[:50]}...")
    print()
    
    # Test message
    test_message = """🧪 **SPECTRA Zephyr Pipeline - Webhook Test**

**Status:** Testing Discord webhook integration
**Pipeline:** Zephyr Source Stage
**Time:** Test notification

✅ If you see this, webhooks are working!
🚀 Ready to use for pipeline notifications."""
    
    print("📤 Sending test notification...")
    success, message = test_webhook(webhook_url, test_message)
    
    print()
    print("=" * 80)
    if success:
        print("✅ SUCCESS!")
        print(f"   {message}")
        print("\n💡 Check your Discord channel - the message should appear there.")
        print("   Webhooks are working! You can use this for pipeline notifications.")
    else:
        print("❌ FAILED")
        print(f"   {message}")
        print("\n💡 Troubleshooting:")
        print("   1. Check webhook URL is correct in .env")
        print("   2. Verify webhook hasn't been deleted in Discord")
        print("   3. Check webhook channel still exists")
        sys.exit(1)
    
    print("=" * 80)

if __name__ == "__main__":
    main()

