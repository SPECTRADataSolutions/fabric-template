"""
Test Fabric REST API to create lakehouse with schema support.
"""
import os
import requests
import json

# Credentials from .env
tenant_id = os.environ.get("SPECTRA_FABRIC_TENANT_ID", "89aaf206-0c55-4dd7-9147-9c95c1a0ff39")
client_id = os.environ.get("SPECTRA_FABRIC_CLIENT_ID", "2cabd8ba-fd56-43c6-8c33-cea62cd5cb49")
workspace_id = "57a80abf-0a09-441a-b69a-38b6f6f1ba7b"  # Zephyr workspace

# Get access token (you'll need client secret or interactive auth)
print("❌ Need SPECTRA_FABRIC_CLIENT_SECRET to authenticate")
print(f"Tenant: {tenant_id}")
print(f"Client: {client_id}")
print(f"Workspace: {workspace_id}")

# Fabric REST API endpoints (for when we have auth)
api_base = "https://api.fabric.microsoft.com/v1"

# Example lakehouse creation payload (we need to discover actual schema)
create_lakehouse_payload = {
    "displayName": "testLakehouse",
    "description": "Test lakehouse for schema support",
    # "enableSchemas": True,  # ← THIS IS WHAT WE NEED TO FIND
    # "properties": {
    #     "schemaSupport": True
    # }
}

print("\nTo create lakehouse via REST API:")
print(f"POST {api_base}/workspaces/{workspace_id}/lakehouses")
print(f"Payload: {json.dumps(create_lakehouse_payload, indent=2)}")

print("\n⚠️  Need to find:")
print("  1. Authentication method (client secret or interactive)")
print("  2. Correct property name for schema support (enableSchemas? schemaSupport?)")
print("  3. API endpoint documentation")

