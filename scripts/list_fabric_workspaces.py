"""
List Fabric workspaces to find correct ID.
"""
import os
import requests

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
if response.status_code != 200:
    print(f"❌ Auth failed: {response.text}")
    exit(1)

access_token = response.json()["access_token"]
print("✅ Access token obtained\n")

# List workspaces
api_url = "https://api.fabric.microsoft.com/v1/workspaces"
headers = {"Authorization": f"Bearer {access_token}"}

print("📋 Listing workspaces...\n")
response = requests.get(api_url, headers=headers)

if response.status_code == 200:
    workspaces = response.json().get("value", [])
    print(f"Found {len(workspaces)} workspaces:\n")
    
    for ws in workspaces:
        print(f"  • {ws['displayName']}")
        print(f"    ID: {ws['id']}")
        print(f"    Type: {ws.get('type', 'N/A')}")
        print()
else:
    print(f"❌ Failed ({response.status_code}): {response.text}")

