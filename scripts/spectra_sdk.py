"""
SPECTRA Fabric SDK v0.3.0

Embedded SDK for Microsoft Fabric notebooks.
Usage: Add this file to your workspace and import classes directly.

Example:
    from spectra_sdk import NotebookSession
    
    session = NotebookSession("myVariables")
    session.load_context(bootstrap=False, debug=True)
    log = session.initialize()
"""

# ══════════════════════════════════════════════════════════════════════════════
# Pipeline Class - Execution Context
# ══════════════════════════════════════════════════════════════════════════════

class Pipeline:
    """Fabric pipeline execution context."""
    
    def __init__(self, spark):
        self._spark = spark
    
    @property
    def is_active(self) -> bool:
        """Is this notebook running in a pipeline?"""
        return self.operation_type != "SessionCreation"
    
    @property
    def is_interactive(self) -> bool:
        """Is this notebook running interactively in Fabric?"""
        return self.operation_type == "SessionCreation"
    
    @property
    def is_local(self) -> bool:
        """Is this notebook running locally? (Future)"""
        workspace_id = self._spark.conf.get("trident.workspace.id", "")
        return workspace_id == ""
    
    @property
    def operation_type(self) -> str:
        """Fabric operation type (SessionCreation, PipelineRun, etc.)"""
        return self._spark.conf.get("trident.operation.type", "Unknown")
    
    @property
    def activity_id(self) -> str:
        """Unique ID for this pipeline activity."""
        return self._spark.conf.get("trident.activity.id", "")


# ══════════════════════════════════════════════════════════════════════════════
# Environment Class - Infrastructure Context
# ══════════════════════════════════════════════════════════════════════════════

class Environment:
    """Fabric workspace and lakehouse environment context."""
    
    def __init__(self, spark):
        self._spark = spark
    
    @property
    def workspace_id(self) -> str:
        """Fabric workspace UUID."""
        return self._spark.conf.get("trident.workspace.id", "")
    
    @property
    def lakehouse_id(self) -> str:
        """Attached lakehouse UUID."""
        return self._spark.conf.get("trident.lakehouse.id", "")
    
    @property
    def lakehouse_name(self) -> str:
        """Attached lakehouse display name."""
        return self._spark.conf.get("trident.lakehouse.name", "")
    
    @property
    def tenant_id(self) -> str:
        """Azure tenant UUID."""
        return self._spark.conf.get("trident.tenant.id", "")


# ══════════════════════════════════════════════════════════════════════════════
# VariableLibrary Class - Configuration Accessor
# ══════════════════════════════════════════════════════════════════════════════

class VariableLibrary:
    """Fabric Variable Library accessor."""
    
    def __init__(self, library_name: str):
        self.library_name = library_name
        self._library_obj = None
    
    def get(self, key: str, default=None, required: bool = False):
        """Get variable from library."""
        value = None
        
        # Try Fabric Variable Library
        if self.library_name:
            try:
                if self._library_obj is None:
                    from notebookutils import variableLibrary
                    self._library_obj = variableLibrary.getLibrary(self.library_name)
                
                value = getattr(self._library_obj, key, None)
            except Exception:
                pass
        
        # Fallback to environment
        if value is None:
            import os
            value = os.environ.get(key)
        
        # Handle not found
        if value is None:
            if required:
                raise ValueError(f"Required variable '{key}' not found in Variable Library '{self.library_name}'")
            return default
        
        return value
    
    def get_secret(self, key: str, required: bool = True):
        """Get secret variable (never logged)."""
        return self.get(key, required=required)
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """Get boolean variable."""
        value = self.get(key)
        if value is None:
            return default
        return str(value).lower() in ("true", "1", "yes", "on")
    
    def get_int(self, key: str, default: int = 0) -> int:
        """Get integer variable."""
        value = self.get(key)
        if value is None:
            return default
        try:
            return int(value)
        except (ValueError, TypeError):
            return default


# ══════════════════════════════════════════════════════════════════════════════
# DeltaTable Class - Delta Operations
# ══════════════════════════════════════════════════════════════════════════════

import logging

class DeltaTable:
    """Delta table operations helper."""
    
    def __init__(self, spark, log=None):
        self._spark = spark
        self._log = log or logging.getLogger(__name__)
    
    def write(self, df, table_name: str, path: str, mode: str = "overwrite", partition_by=None):
        """Write DataFrame to Delta."""
        writer = df.write.format("delta").mode(mode)
        
        # Schema handling
        if mode == "overwrite":
            writer = writer.option("overwriteSchema", "true")
        if mode == "append":
            writer = writer.option("mergeSchema", "true")
        
        if partition_by:
            writer = writer.partitionBy(*partition_by)
        
        writer.save(path)
        
        row_count = df.count()
        self._log.info(f"  ✅ Wrote {row_count} rows to {path}")


# ══════════════════════════════════════════════════════════════════════════════
# SPECTRALogger Class - Logging
# ══════════════════════════════════════════════════════════════════════════════

import logging
import sys

class SPECTRALogger:
    """SPECTRA-grade logger."""
    
    @staticmethod
    def create(name: str, level: str = "INFO", notebook_name=None, workspace_id=None, stage=None):
        """Create SPECTRA logger."""
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, level.upper()))
        logger.handlers.clear()
        
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(getattr(logging, level.upper()))
        
        format_parts = ["%(asctime)s", "%(levelname)-8s"]
        if notebook_name:
            format_parts.append(f"[{notebook_name}]")
        if stage:
            format_parts.append(f"({stage})")
        format_parts.append("%(message)s")
        
        formatter = logging.Formatter(" - ".join(format_parts), datefmt="%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False
        
        return logger
    
    @staticmethod
    def get_default_level(is_interactive: bool = False, debug_override: bool = False) -> str:
        """Smart debug mode."""
        if debug_override:
            return "DEBUG"
        if is_interactive:
            return "DEBUG"
        return "INFO"


# ══════════════════════════════════════════════════════════════════════════════
# NotebookSession Class - Main Orchestrator
# ══════════════════════════════════════════════════════════════════════════════

from datetime import datetime

class NotebookSession:
    """Manages complete notebook lifecycle with 7-stage pattern."""
    
    def __init__(self, variable_library_name: str):
        self.variable_library_name = variable_library_name
        self.ctx = {}
        self.params = {}
        self.log = None
        self.debug = False
        self.start_time = None
        self.result = {"status": "Success", "capabilities": []}
        
        # Specialized components
        self.pipeline = None
        self.environment = None
        self.variables = None
        self.delta = None
    
    def load_context(self, bootstrap=False, backfill=False, preview=False, debug=False, **kwargs):
        """Stage 2: Load Fabric context + Variable Library."""
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.getOrCreate()
        
        # Initialize components
        self.pipeline = Pipeline(spark)
        self.environment = Environment(spark)
        self.variables = VariableLibrary(self.variable_library_name)
        self.delta = DeltaTable(spark, self.log)
        
        # Load config
        source_system = self.variables.get("SOURCE_SYSTEM", required=True)
        source_name = self.variables.get("SOURCE_NAME", required=True)
        stage = self.variables.get("STAGE", required=True)
        notebook_name = self.variables.get("NOTEBOOK_NAME", required=True)
        base_url = self.variables.get("BASE_URL")
        base_path = self.variables.get("BASE_PATH")
        full_url = f"{base_url}{base_path}" if base_url and base_path else base_url
        
        # Store context
        self.ctx = {
            "workspace_id": self.environment.workspace_id,
            "lakehouse_id": self.environment.lakehouse_id,
            "lakehouse_name": self.environment.lakehouse_name,
            "tenant_id": self.environment.tenant_id,
            "source_system": source_system,
            "source_name": source_name,
            "stage": stage,
            "notebook_name": notebook_name,
            "base_url": base_url,
            "base_path": base_path,
            "full_url": full_url,
            "in_pipeline": self.pipeline.is_active,
            "in_interactive": self.pipeline.is_interactive,
        }
        
        # Validate parameters
        self.params = {
            "bootstrap": bootstrap,
            "backfill": backfill,
            "preview": preview,
            "debug": debug,
            **kwargs
        }
        
        # Auto-enable debug in interactive
        if self.ctx["in_interactive"] and not self.params["debug"]:
            self.params["debug"] = True
    
    def initialize(self):
        """Stage 3: Initialize logger and start timer."""
        self.debug = self.params["debug"]
        level = SPECTRALogger.get_default_level(self.ctx["in_interactive"], self.debug)
        
        log = SPECTRALogger.create(
            name=self.ctx['notebook_name'],
            level=level,
            notebook_name=self.ctx['notebook_name'],
            workspace_id=self.ctx['workspace_id'],
            stage=self.ctx['stage']
        )
        
        # Update DeltaTable logger
        if self.delta:
            self.delta._log = log
        
        self.start_time = datetime.utcnow()
        
        # Startup banner
        log.info("=" * 80)
        log.info(f"🚀 {self.ctx['notebook_name']} | {self.ctx['stage']}")
        log.info("=" * 80)
        log.info(f"Source: {self.ctx['source_name']} ({self.ctx['source_system']})")
        log.info(f"Workspace: {self.ctx['lakehouse_name']} ({self.ctx['workspace_id']})")
        log.info(f"Mode: {'Interactive' if self.ctx['in_interactive'] else 'Pipeline'}")
        log.info(f"Parameters: bootstrap={self.params['bootstrap']}, backfill={self.params['backfill']}, preview={self.params['preview']}, debug={self.params['debug']}")
        log.info("=" * 80)
        
        self.log = log
        return log
    
    def add_capability(self, capability: str, **metadata):
        """Add capability to result."""
        self.result["capabilities"].append(capability)
        if metadata:
            self.result[capability] = metadata
    
    def mark_failed(self, error_msg: str):
        """Mark execution as failed."""
        self.result["status"] = "Failed"
        self.result["error"] = error_msg
        self.log.error(f"❌ {error_msg}")
    
    def validate(self):
        """Stage 5: Validate execution."""
        if self.result["status"] == "Success":
            self.log.info("✅ Validation passed")
        else:
            self.log.error("❌ Validation failed")
            raise RuntimeError(f"Execution failed: {self.result.get('error', 'Unknown error')}")
    
    def record(self):
        """Stage 6: Record activity (placeholder)."""
        self.log.info("📝 Activity recorded")
    
    def finalise(self):
        """Stage 7: Finalise execution and send notifications."""
        duration = (datetime.utcnow() - self.start_time).total_seconds()
        
        self.log.info("=" * 80)
        self.log.info(f"✅ {self.ctx['notebook_name']} Complete")
        self.log.info(f"Duration: {duration:.2f}s")
        self.log.info(f"Status: {self.result['status']}")
        self.log.info(f"Capabilities: {self.result['capabilities']}")
        self.log.info("=" * 80)

