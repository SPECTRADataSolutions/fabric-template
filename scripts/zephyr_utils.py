"""Shared utilities for Zephyr scripts.

SPECTRA-grade: Environment configuration from Variable Library.
"""
from pathlib import Path


def get_test_project_id() -> int:
    """Get TEST_PROJECT_ID from Variable Library (SPECTRA-grade pattern).
    
    Returns:
        int: Test project ID (defaults to 45 if not found)
    """
    var_lib_path = Path(__file__).parent.parent / "zephyrVariables.VariableLibrary" / "variables.json"
    if var_lib_path.exists():
        import json
        with open(var_lib_path, "r") as f:
            var_lib = json.load(f)
            for var in var_lib.get("variables", []):
                if var.get("name") == "TEST_PROJECT_ID":
                    return int(var.get("value", "45"))
    return 45  # Fallback to locked default


def get_api_credentials():
    """Get API credentials from .env or Variable Library.
    
    Returns:
        tuple: (api_token, base_url, base_path, full_url)
    """
    import json
    
    # Try .env first
    spectra_root = Path(__file__).parent.parent.parent.parent
    env_file = spectra_root / ".env"
    
    api_token = None
    if env_file.exists():
        with open(env_file, "r") as f:
            for line in f:
                if line.startswith("ZEPHYR_API_TOKEN=") or line.startswith("SPECTRA_ZEPHYR_API_TOKEN="):
                    api_token = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    
    # Fallback to Variable Library
    if not api_token:
        var_lib_path = Path(__file__).parent.parent / "zephyrVariables.VariableLibrary" / "variables.json"
        if var_lib_path.exists():
            with open(var_lib_path, "r") as f:
                var_lib = json.load(f)
                for var in var_lib.get("variables", []):
                    if var.get("name") == "API_TOKEN":
                        api_token = var.get("value")
                        break
                    elif var.get("name") == "BASE_URL":
                        base_url = var.get("value", "https://velonetic.yourzephyr.com")
                    elif var.get("name") == "BASE_PATH":
                        base_path = var.get("value", "/flex/services/rest/latest")
    
    if not api_token:
        raise ValueError("API token not found in .env or Variable Library")
    
    # Get base_url and base_path from Variable Library
    var_lib_path = Path(__file__).parent.parent / "zephyrVariables.VariableLibrary" / "variables.json"
    base_url = "https://velonetic.yourzephyr.com"
    base_path = "/flex/services/rest/latest"
    
    if var_lib_path.exists():
        with open(var_lib_path, "r") as f:
            var_lib = json.load(f)
            for var in var_lib.get("variables", []):
                if var.get("name") == "BASE_URL":
                    base_url = var.get("value")
                elif var.get("name") == "BASE_PATH":
                    base_path = var.get("value")
    
    full_url = f"{base_url}{base_path}"
    
    return api_token, base_url, base_path, full_url

