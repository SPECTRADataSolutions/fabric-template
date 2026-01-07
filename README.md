# SPECTRA Fabric Workspace Template

[![SPECTRA-Grade](https://img.shields.io/badge/SPECTRA-Grade-brightgreen.svg)](https://github.com/SPECTRADataSolutions/spectra-fabric-template)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

**SPECTRA-grade template for Microsoft Fabric workspaces** following the proven 7-stage SPECTRA methodology.

## 🎯 What This Template Provides

A complete, production-ready Fabric workspace structure with:

- ✅ **7-stage pipeline methodology** (Source → Prepare → Extract → Clean → Transform → Refine → Analyse)
- ✅ **Minimal, clean notebooks** following the 7-call pattern
- ✅ **Metadata-driven architecture** (contracts, manifests, intelligence)
- ✅ **SPECTRA Fabric SDK** embedded and ready to use
- ✅ **Git integration** configured for Fabric sync
- ✅ **Variable Library** structure
- ✅ **Pipeline** wired with dependencies
- ✅ **Testing framework** setup

## 🚀 Quick Start

### 1. Create Repository from Template

Click **"Use this template"** on GitHub to create your new repository.

### 2. Clone and Customize

```bash
git clone https://github.com/YOUR_ORG/YOUR_PROJECT.git
cd YOUR_PROJECT
```

### 3. Run Setup Script

```powershell
.\scripts\setup-new-project.ps1 -ProjectName "yourproject" -SourceSystem "YourSourceSystem"
```

This will:
- Replace all `{PROJECT}` placeholders with your project name
- Update Variable Library names
- Update lakehouse references
- Generate initial contract files

### 4. Configure Fabric Workspace

1. Create workspace in Fabric UI
2. Create lakehouse (enable Schema Support!)
3. Connect workspace to Git
4. Sync notebooks

### 5. Configure Variables

Add to Fabric Variable Library (`{PROJECT}Variables`):
- `BASE_URL` - API base URL
- `BASE_PATH` - API path prefix
- `API_TOKEN` - Authentication token (secret)
- `SOURCE_SYSTEM` - Source system identifier
- `SOURCE_NAME` - Source system display name

### 6. Run Source Stage

Execute `source{PROJECT}.Notebook` to:
- Validate connectivity
- Catalog endpoints
- Create portfolio tables

## 📋 The 7 Stages

| Stage | Purpose | Notebook | Status |
|-------|---------|----------|--------|
| **1. Source** | Connectivity, authentication, endpoint catalog | `source{PROJECT}.Notebook` | ✅ Template ready |
| **2. Prepare** | Schema intelligence, metadata configuration | `prepare{PROJECT}Config.Notebook` | ✅ Template ready |
| **3. Extract** | Field promotion, data extraction | `extract{PROJECT}Sample.Notebook` | ✅ Template ready |
| **4. Clean** | Data cleaning, standardization | `clean{PROJECT}.Notebook` | ⏳ Skeleton |
| **5. Transform** | Dimensional modeling | `transform{PROJECT}.Notebook` | ⏳ Skeleton |
| **6. Refine** | Business enrichment | `refine{PROJECT}.Notebook` | ⏳ Skeleton |
| **7. Analyse** | Final presentation layer | `analyse{PROJECT}.Notebook` | ⏳ Skeleton |

## 🏗️ Structure

```
{PROJECT}/
├── 1-source/
│   └── source{PROJECT}.Notebook/
│       ├── .platform
│       └── notebook_content.py
├── 2-prepare/
│   └── prepare{PROJECT}Config.Notebook/
├── 3-extract/
│   └── extract{PROJECT}Sample.Notebook/
├── 4-clean/
├── 5-transform/
├── 6-refine/
├── 7-analyse/
├── {PROJECT}Intelligence.Notebook/  # Service-specific intelligence
├── spectraSDK.Notebook/              # Generic SPECTRA SDK
├── {PROJECT}Pipeline.DataPipeline/
├── {PROJECT}Variables.VariableLibrary/
├── {PROJECT}Environment.Environment/
├── {PROJECT}Lakehouse.Lakehouse/
├── config/
│   ├── contracts/
│   └── manifests/
└── scripts/
    └── setup-new-project.ps1
```

## 📚 Documentation

- [SPECTRA Methodology](https://spectra.ai/methodology)
- [Fabric SDK Documentation](https://github.com/SPECTRADataSolutions/fabric-sdk)
- [7-Stage Pipeline Guide](docs/7-STAGE-PIPELINE-GUIDE.md)

## 🎓 SPECTRA-Grade Standards

This template follows SPECTRA-grade standards:

- ✅ Zero tech debt
- ✅ Perfect standards compliance
- ✅ Comprehensive testing framework
- ✅ Metadata-driven architecture
- ✅ No secrets in tracked files
- ✅ Complete documentation

## 🤝 Contributing

This is a template repository. To contribute improvements:

1. Fork the template
2. Make improvements
3. Submit PR with clear description
4. Ensure SPECTRA-grade compliance

## 📄 License

[Your License Here]

## 🔗 Related

- [SPECTRA Framework](https://github.com/SPECTRADataSolutions/spectra)
- [Fabric SDK](https://github.com/SPECTRADataSolutions/fabric-sdk)
- [SPECTRA Documentation](https://spectra.ai/docs)
