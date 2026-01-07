"""
Create test lakehouse via Fabric REST API to discover schema property.
"""
import os
import requests

# Load from root .env manually
env_path = "C:\\Users\\markm\\OneDrive\\SPECTRA\\.env"
with open(env_path) as f:
    for line in f:
        if "=" in line and not line.startswith("#"):
            key, value = line.strip().split("=", 1)
            os.environ[key] = value.strip('"')

# Fabric credentials
tenant_id = os.environ.get("SPECTRA_FABRIC_TENANT_ID")
client_id = os.environ.get("SPECTRA_FABRIC_CLIENT_ID")
client_secret = os.environ.get("SPECTRA_FABRIC_CLIENT_SECRET")

print(f"Tenant ID: {tenant_id}")
print(f"Client ID: {client_id}")
print(f"Secret found: {'Yes' if client_secret else 'No'}")

if not all([tenant_id, client_id, client_secret]):
    print("\n❌ Missing credentials!")
    print("Need: SPECTRA_FABRIC_CLIENT_SECRET or SPECTRA_GRAPH_CLIENT_SECRET")
    exit(1)

# Get access token
print("\n🔐 Getting access token...")
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
print("✅ Access token obtained")

# Create test lakehouse
workspace_id = "16490dde-33b4-446e-8120-c12b0a68ed88"  # Zephyr workspace (verified)
api_url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/lakehouses"

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Try different property variations to enable schemas
test_payloads = [
    {"displayName": "testLakehouseA", "description": "Test A - no schema property"},
    {"displayName": "testLakehouseB", "description": "Test B - enableSchemas", "enableSchemas": True},
    {"displayName": "testLakehouseC", "description": "Test C - schemaSupport", "schemaSupport": True},
    {"displayName": "testLakehouseD", "description": "Test D - schemas enabled", "schemas": {"enabled": True}},
]

print(f"\n🧪 Testing {len(test_payloads)} payloads...\n")

for i, payload in enumerate(test_payloads, 1):
    print(f"Test {i}: {payload['displayName']}")
    print(f"  Payload: {payload}")
    
    response = requests.post(api_url, headers=headers, json=payload)
    
    if response.status_code in [200, 201]:
        result = response.json()
        lakehouse_id = result.get("id")
        print(f"  ✅ Created: {lakehouse_id}")
        print(f"  Response: {result}")
    else:
        print(f"  ❌ Failed ({response.status_code}): {response.text[:200]}")
    print()

print("🏁 Done! Check which ones succeeded and test if they support schemas.")

