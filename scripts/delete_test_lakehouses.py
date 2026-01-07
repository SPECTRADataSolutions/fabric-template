"""
Delete test lakehouses (none supported schemas).
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
access_token = response.json()["access_token"]
print("✅ Access token obtained\n")

workspace_id = "16490dde-33b4-446e-8120-c12b0a68ed88"
headers = {"Authorization": f"Bearer {access_token}"}

# Delete test lakehouses
test_lakehouses = [
    ("testLakehouseA", "089b7bad-de56-4b5a-9840-d9983efe2515"),
    ("testLakehouseB", "85f13ac1-141b-444e-b385-0efdaf6dcb37"),
    ("testLakehouseC", "45c692d0-58ea-40b3-818f-ae7fd017320a"),
    ("testLakehouseD", "d37b2ab0-dbe9-403d-bb25-9397255d8192"),
]

print("🗑️  Deleting test lakehouses...\n")

for name, lakehouse_id in test_lakehouses:
    api_url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/lakehouses/{lakehouse_id}"
    response = requests.delete(api_url, headers=headers)
    
    if response.status_code in [200, 204]:
        print(f"✅ Deleted: {name}")
    else:
        print(f"❌ Failed to delete {name} ({response.status_code}): {response.text[:100]}")

print("\n🏁 Cleanup complete!")

