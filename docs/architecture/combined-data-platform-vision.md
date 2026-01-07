# Combined Data Platform Vision
**Date:** 2025-01-29  
**Status:** 🟡 Vision Documented - Architecture to be Designed

---

## Overview

The Zephyr pipeline is part of a larger vision for a combined data platform that integrates Zephyr and Jira data for comprehensive reporting and analytics.

---

## Architecture Vision

### Three-Workspace Model

1. **Zephyr Workspace (Fabric)**
   - Zephyr pipeline (Source → Prepare → Extract → Clean → Transform → Refine → Analyse)
   - Zephyr data model
   - Zephyr Power BI reports

2. **Jira Workspace (Fabric)**
   - Jira pipeline (already built)
   - Jira data model
   - Jira Power BI reports

3. **SPECTRA Workspace (Fabric)**
   - Takes output from both Zephyr and Jira workspaces
   - Combined data model
   - Unified Power BI reports showing integrated view

---

## Integration Points

### Zephyr ↔ Jira Integration

- **Native Integration:** Zephyr and Jira have an existing integration
- **Power BI Exposure:** Need to expose this integration in Power BI reports
- **Use Case:** Report on tests that have Jira tickets raised against them
- **Cross-Model Reporting:** Report across the whole model (Zephyr + Jira)

### Key Integration Scenarios

1. **Test → Jira Ticket Linkage**
   - When a test has a Jira ticket raised against it
   - Report on test status and associated Jira issue
   - Track test execution against Jira work items

2. **Work Stream Visibility**
   - Dev → Build (Jira)
   - Test (Zephyr)
   - Combined view of entire work stream

3. **Requirement Traceability**
   - Business scenarios (requirements) in Zephyr
   - Jira issues/epics
   - Cross-reference and traceability

---

## Business Drivers

### Decision Makers

- **Bob James** - Wants standardized reporting, loves Power BI work
- **Callum Gibson** - Wants to be informed of testing progress, frustrated with project slowness

### Key Requirements

1. **Standardized Reporting**
   - No more Excel spreadsheets
   - Auto-refreshing reports
   - Consistent figures across all stakeholders

2. **Combined Visibility**
   - See testing progress (Zephyr)
   - See development/build progress (Jira)
   - Integrated view of entire Blueprint 2 program

3. **Cost Justification**
   - Decision makers need to justify spending
   - Save money where possible
   - Show value of data platform investment

---

## Current State

- **Jira Pipeline:** ✅ Built (prototype, being refined)
- **Zephyr Pipeline:** 🟡 In progress (Source stage)
- **SPECTRA Combined Workspace:** ⏳ Planned

---

## Future State

### Zephyr Workspace
- Complete Zephyr pipeline with all 7 stages
- Zephyr data model (dimensional)
- Zephyr Power BI reports (including "Bob's Mosaic")

### Jira Workspace
- Refined Jira pipeline (aligned with perfected Zephyr methodology)
- Jira data model
- Jira Power BI reports

### SPECTRA Combined Workspace
- Ingests from both Zephyr and Jira workspaces
- Combined dimensional model
- Unified Power BI reports
- Exposes Zephyr ↔ Jira integration
- Cross-model analytics and reporting

---

## Technical Considerations

### Data Integration

- How to link Zephyr tests to Jira tickets (use existing Zephyr-Jira integration)
- Schema alignment between Zephyr and Jira models
- Incremental refresh strategies for both pipelines
- Data freshness requirements

### Reporting Requirements

- "Bob's Mosaic" - Requirements × Cycles matrix with traffic lights
- Test execution status
- Jira ticket linkage
- Combined work stream visibility
- Cost/justification metrics

---

## Next Steps

1. Complete Zephyr Source stage (current focus)
2. Build out Zephyr pipeline through all 7 stages
3. Design Zephyr data model
4. Build Zephyr Power BI reports
5. Refine Jira pipeline to match Zephyr methodology
6. Design SPECTRA combined workspace architecture
7. Implement combined data model
8. Build unified Power BI reports

## Team Migration Path

### Data Solutions Team Adoption

**Current State:**
- Russ Dovaston & Scott Read: Excel-based reporting using daily Jira exports
- User & Lorraine: Power BI solutions using direct pipeline connections

**Migration Strategy:**
1. **Phase 1:** Get Russ & Scott onto Jira and Zephyr models, pull into Excel (first step)
2. **Phase 2:** Russ & Scott learn Power BI, move from Excel to Power BI
3. **Phase 3:** All team members using Power BI with single source of truth

**Goal:** Unified approach with models as single source of truth, moving away from Excel exports

**See:** `docs/stakeholders/data-solutions-team.md` for team structure details

---

**Last Updated:** 2025-01-29

