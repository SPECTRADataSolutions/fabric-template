"""
Check if zephyrLakehouse is fully deleted and name is available.
"""
import os
import requests
import time

# Load from root .env
env_path = "C:\\Users\\markm\\OneDrive\\SPECTRA\\.env"
with open(env_path) as f:
    for line in f:
        if "=" in line and not line.startswith("#"):
            key, value = line.strip().split("=", 1)
            os.environ[key] = value.strip('"')

tenant_id = os.environ["SPECTRA_FABRIC_TENANT_ID"]
client_id = os.environ["SPECTRA_FABRIC_CLIENT_ID"]
client_secret = os.environ["SPECTRA_FABRIC_CLIENT_SECRET"]

# Get access token
print("🔐 Getting access token...")
token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
token_data = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret,
    "scope": "https://api.fabric.microsoft.com/.default"
}

response = requests.post(token_url, data=token_data)
access_token = response.json()["access_token"]
print("✅ Access token obtained\n")

workspace_id = "16490dde-33b4-446e-8120-c12b0a68ed88"
headers = {"Authorization": f"Bearer {access_token}"}

# List all lakehouses
print("📋 Checking lakehouses in zephyr workspace...\n")
api_url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/lakehouses"
response = requests.get(api_url, headers=headers)

if response.status_code == 200:
    lakehouses = response.json().get("value", [])
    
    print(f"Found {len(lakehouses)} lakehouse(s):\n")
    
    zephyr_exists = False
    for lh in lakehouses:
        print(f"  • {lh['displayName']}")
        print(f"    ID: {lh['id']}")
        if lh['displayName'] == 'zephyrLakehouse':
            zephyr_exists = True
            print(f"    ⚠️  zephyrLakehouse still exists!")
            print(f"    Delete URL: /workspaces/{workspace_id}/lakehouses/{lh['id']}")
        print()
    
    if not zephyr_exists:
        print("✅ 'zephyrLakehouse' name is available!")
        print("You can recreate it now with 'Enable Schemas' checked.")
    else:
        print("❌ 'zephyrLakehouse' still exists - delete it first!")
        print("\nTo force delete via API:")
        print(f"  DELETE https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/lakehouses/{{id}}")
else:
    print(f"❌ Failed to list lakehouses: {response.status_code}")
    print(response.text)

