"""Reusable comprehensive test data builder - template-driven for any source system.

SPECTRA-Grade: Generic builder that works for any REST API by using templates.
Uses SDK SchemaDiscoveryHelpers for generic entity creation and response capture.

Purpose:
- Create entities with ALL fields populated (from template)
- Test enum variations
- Discover data structures (scalar, record, array)
- Capture API responses for schema analysis

Usage:
    python build_comprehensive_test_data_reusable.py --template scripts/data/zephyr_comprehensive_test_data.yaml
"""
import json
import yaml
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any
import time
import os
import sys

# Try to import yaml, fallback to json if not available
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False
    print("⚠️ PyYAML not installed. Will try to load YAML as JSON or create default templates.")


class ComprehensiveTestDataBuilder:
    """Template-driven test data builder - works for any source system."""
    
    def __init__(self, template_path: Path, variable_resolver: Optional[Dict[str, str]] = None):
        """Initialize builder with template configuration.
        
        Args:
            template_path: Path to YAML template file
            variable_resolver: Optional dict to resolve ${VAR} placeholders in template
        """
        self.template_path = template_path
        self.template = self._load_template()
        self.variable_resolver = variable_resolver or {}
        self.config = self._resolve_config()
        self.created_entities = {}
        
    def _load_template(self) -> Dict[str, Any]:
        """Load template file (YAML or JSON)."""
        if not self.template_path.exists():
            raise FileNotFoundError(f"Template file not found: {self.template_path}")
        
        if HAS_YAML:
            with open(self.template_path, "r") as f:
                return yaml.safe_load(f)
        else:
            try:
                with open(self.template_path, "r") as f:
                    return json.load(f)
            except Exception as e:
                raise ValueError(f"Could not load template: {e}. Install PyYAML: pip install pyyaml")
    
    def _resolve_config(self) -> Dict[str, Any]:
        """Resolve template configuration and variables."""
        config = self.template.copy()
        
        # Resolve variable placeholders (${VAR})
        def resolve_vars(value):
            if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                var_name = value[2:-1]
                return self.variable_resolver.get(var_name, value)
            elif isinstance(value, dict):
                return {k: resolve_vars(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [resolve_vars(item) for item in value]
            return value
        
        config = resolve_vars(config)
        return config
    
    def _build_headers(self) -> Dict[str, str]:
        """Build HTTP headers from auth configuration."""
        auth_config = self.config.get("auth", {})
        auth_type = auth_config.get("type", "bearer")
        
        headers = {"Content-Type": "application/json"}
        
        if auth_type == "bearer":
            token = self.variable_resolver.get(auth_config.get("token_var", "API_TOKEN"), "")
            header_name = auth_config.get("header", "Authorization")
            prefix = auth_config.get("prefix", "Bearer")
            headers[header_name] = f"{prefix} {token}"
        elif auth_type == "basic":
            # Future: Support basic auth
            pass
        
        return headers
    
    def _get_base_url(self) -> str:
        """Get full API base URL."""
        base_url = self.config.get("base_url", "")
        base_path = self.config.get("base_path", "")
        
        if base_path:
            return f"{base_url.rstrip('/')}{base_path}"
        return base_url
    
    def build_all_entities(
        self,
        output_dir: Path,
        logger=None
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Build all entities from template - generic process.
        
        Args:
            output_dir: Directory to save captured responses
            logger: Optional logger (can be print-based for scripts)
        
        Returns:
            Dict of created entities by type
        """
        base_url = self._get_base_url()
        headers = self._build_headers()
        entities_created = {}
        
        # Import SDK helpers (if in notebook context)
        # For standalone script, we'll use requests directly but follow SDK patterns
        try:
            # Try to import from SDK (if running in notebook/Fabric)
            from SchemaDiscoveryHelpers import SchemaDiscoveryHelpers
            use_sdk = True
        except ImportError:
            # Standalone script - use local implementation
            use_sdk = False
            SchemaDiscoveryHelpers = None
        
        # Process each entity type in template
        for entity_type, entity_templates in self.config.items():
            if entity_type in ["source_system", "base_url", "base_path", "auth", "test_project"]:
                continue
            
            if not isinstance(entity_templates, list):
                continue
            
            if logger:
                logger(f"\n{'='*80}")
                logger(f"Creating {entity_type} entities...")
                logger(f"{'='*80}")
            else:
                print(f"\n{'='*80}")
                print(f"Creating {entity_type} entities...")
                print(f"{'='*80}")
            
            entities_created[entity_type] = []
            
            for template in entity_templates:
                # Resolve relationships and variables in template
                payload = self._resolve_payload(template, entities_created)
                
                if not payload:
                    continue
                
                # Get endpoint from template or use entity type
                endpoint = template.get("endpoint", f"/{entity_type}")
                
                # Create entity
                if use_sdk and SchemaDiscoveryHelpers:
                    entity_data, entity_id, error = SchemaDiscoveryHelpers.create_entity_comprehensively(
                        base_url=base_url,
                        endpoint=endpoint,
                        payload=payload,
                        headers=headers,
                        logger=logger,
                        timeout=30,
                        save_response_path=str(output_dir / f"{entity_type}_{template.get('name', 'unknown')}_response.json")
                    )
                else:
                    # Standalone script implementation
                    entity_data, entity_id, error = self._create_entity_standalone(
                        base_url=base_url,
                        endpoint=endpoint,
                        payload=payload,
                        headers=headers,
                        output_dir=output_dir,
                        entity_name=f"{entity_type}: {template.get('name', 'unknown')}"
                    )
                
                if entity_id:
                    entities_created[entity_type].append({
                        "id": entity_id,
                        "name": template.get("name", ""),
                        "payload": payload,
                        "data": entity_data
                    })
                    time.sleep(1)  # Rate limiting
        
        return entities_created
    
    def _resolve_payload(self, template: Dict[str, Any], created_entities: Dict) -> Optional[Dict[str, Any]]:
        """Resolve payload from template, replacing relationship placeholders."""
        payload = template.copy()
        
        # Remove metadata fields
        payload.pop("name", None)
        payload.pop("endpoint", None)
        payload.pop("description", None)
        
        # Resolve relationship placeholders
        # e.g., parentId: "ROOT" -> actual ID
        # e.g., releaseId: "PARENT_RELEASE" -> actual release ID
        
        # Check for test_project ID
        if "projectId" in payload:
            project_id_var = self.config.get("test_project", {}).get("id_var", "TEST_PROJECT_ID")
            project_id = self.variable_resolver.get(project_id_var)
            if project_id:
                payload["projectId"] = int(project_id)
        
        # Resolve parent/relationship IDs
        for key, value in list(payload.items()):
            if isinstance(value, str) and value in ["ROOT", "PARENT", "SUB1"]:
                # Try to resolve from created entities
                # This is source-specific logic - could be enhanced
                payload[key] = None  # Placeholder - would need source-specific resolver
        
        return payload
    
    def _create_entity_standalone(
        self,
        base_url: str,
        endpoint: str,
        payload: Dict[str, Any],
        headers: Dict[str, str],
        output_dir: Path,
        entity_name: str
    ) -> tuple[Optional[Dict], Optional[int], Optional[str]]:
        """Standalone entity creation (for scripts outside notebook context)."""
        import requests
        
        url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        print(f"🚀 Creating {entity_name}...")
        print(f"   Endpoint: POST {endpoint}")
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            created_entity = response.json()
            
            # Extract entity ID (handle wrapped responses)
            entity_data = created_entity
            entity_id = None
            
            if isinstance(created_entity, dict):
                for key in ["dto", "data", "result", "entity", "item"]:
                    if key in created_entity:
                        entity_data = created_entity[key]
                        break
                    # Check for source-specific wrappers (e.g., releaseDto)
                    for wrapper_key in created_entity.keys():
                        if wrapper_key.endswith("Dto") or wrapper_key.endswith("DTO"):
                            entity_data = created_entity[wrapper_key]
                            break
                
                entity_id = entity_data.get("id") if isinstance(entity_data, dict) else None
            
            # Save response
            response_file = output_dir / f"{entity_name.lower().replace(' ', '_')}_response.json"
            response_file.parent.mkdir(parents=True, exist_ok=True)
            with open(response_file, "w") as f:
                json.dump(created_entity, f, indent=2)
            print(f"   💾 Saved response to: {response_file}")
            print(f"   ✅ Created successfully! ID: {entity_id}\n")
            
            return entity_data, entity_id, None
            
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP {e.response.status_code}: {e.response.text[:500]}"
            print(f"   ❌ Creation failed: {error_msg}\n")
            
            # Save error
            error_file = output_dir / f"{entity_name.lower().replace(' ', '_')}_error_{e.response.status_code}.json"
            try:
                error_data = {
                    "status_code": e.response.status_code,
                    "payload": payload,
                    "error": e.response.text
                }
                with open(error_file, "w") as f:
                    json.dump(error_data, f, indent=2)
            except:
                pass
            
            return None, None, error_msg
        except Exception as e:
            error_msg = str(e)
            print(f"   ❌ Error: {error_msg}\n")
            return None, None, error_msg


def resolve_variables_from_env_or_varlib(variable_names: List[str], var_lib_path: Optional[Path] = None) -> Dict[str, str]:
    """Resolve variables from environment or Variable Library - generic."""
    resolved = {}
    
    for var_name in variable_names:
        # Try environment first
        env_value = os.getenv(var_name) or os.getenv(f"SPECTRA_{var_name}")
        if env_value:
            resolved[var_name] = env_value
            continue
        
        # Try Variable Library
        if var_lib_path and var_lib_path.exists():
            with open(var_lib_path, "r") as f:
                var_lib = json.load(f)
                for var in var_lib.get("variables", []):
                    if var.get("name") == var_name:
                        resolved[var_name] = var.get("value", "")
                        break
    
    return resolved


def main():
    """Main entry point for standalone script."""
    parser = argparse.ArgumentParser(description="Build comprehensive test data from template")
    parser.add_argument(
        "--template",
        type=str,
        required=True,
        help="Path to template YAML file (e.g., scripts/data/zephyr_comprehensive_test_data.yaml)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output directory for captured responses (default: docs/schemas/discovered/comprehensive)"
    )
    parser.add_argument(
        "--var-lib",
        type=str,
        default=None,
        help="Path to Variable Library JSON file (for variable resolution)"
    )
    
    args = parser.parse_args()
    
    template_path = Path(args.template)
    if not template_path.is_absolute():
        # Relative to script directory
        template_path = Path(__file__).parent / template_path
    
    # Resolve variables
    spectra_root = Path(__file__).parent.parent.parent.parent
    env_file = spectra_root / ".env"
    
    # Load variables from .env
    variables = {}
    if env_file.exists():
        with open(env_file, "r") as f:
            for line in f:
                if "=" in line and not line.strip().startswith("#"):
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    variables[key] = value
    
    # Load from Variable Library if provided
    var_lib_path = None
    if args.var_lib:
        var_lib_path = Path(args.var_lib)
    else:
        # Try default location
        var_lib_path = Path(__file__).parent.parent / "zephyrVariables.VariableLibrary" / "variables.json"
    
    if var_lib_path and var_lib_path.exists():
        with open(var_lib_path, "r") as f:
            var_lib = json.load(f)
            for var in var_lib.get("variables", []):
                var_name = var.get("name")
                var_value = var.get("value", "")
                variables[var_name] = var_value
    
    # Resolve common variable names
    variable_resolver = {
        "BASE_URL": variables.get("BASE_URL") or variables.get("ZEPHYR_BASE_URL", ""),
        "BASE_PATH": variables.get("BASE_PATH") or variables.get("ZEPHYR_BASE_PATH", ""),
        "API_TOKEN": variables.get("API_TOKEN") or variables.get("ZEPHYR_API_TOKEN", ""),
        "TEST_PROJECT_ID": variables.get("TEST_PROJECT_ID", "45")
    }
    
    # Output directory
    if args.output:
        output_dir = Path(args.output)
    else:
        output_dir = Path(__file__).parent.parent / "docs" / "schemas" / "discovered" / "comprehensive"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 80)
    print("🚀 COMPREHENSIVE TEST DATA BUILDER (Reusable)")
    print("=" * 80)
    print(f"📄 Template: {template_path}")
    print(f"💾 Output: {output_dir}")
    print(f"🔗 Base URL: {variable_resolver.get('BASE_URL', '')}")
    print()
    
    # Build entities
    builder = ComprehensiveTestDataBuilder(template_path, variable_resolver)
    created_entities = builder.build_all_entities(output_dir)
    
    # Save summary
    summary = {
        "template": str(template_path),
        "source_system": builder.config.get("source_system", "unknown"),
        "created_entities": {k: len(v) for k, v in created_entities.items()},
        "entities": created_entities
    }
    
    summary_file = output_dir / "creation_summary.json"
    with open(summary_file, "w") as f:
        json.dump(summary, f, indent=2)
    
    print("\n" + "=" * 80)
    print("✅ COMPREHENSIVE TEST DATA CREATION COMPLETE")
    print("=" * 80)
    
    total_created = sum(len(v) for v in created_entities.values())
    print(f"📊 Total entities created: {total_created}")
    for entity_type, entities in created_entities.items():
        if entities:
            print(f"   ✅ {entity_type}: {len(entities)}")
    
    print(f"\n💾 All responses saved to: {output_dir}")
    print(f"📋 Summary saved to: {summary_file}")
    print(f"\n🔍 Next: Run discover_schema_from_comprehensive_data.py to analyze responses")


if __name__ == "__main__":
    main()

