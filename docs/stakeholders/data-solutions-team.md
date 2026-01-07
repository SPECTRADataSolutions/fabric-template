# Data Solutions Team Structure
**Date:** 2025-01-29  
**Status:** 🟢 Documented

---

## Team Overview

4-person data solutions team providing data solutions for London Markets Account / Velenetic.

### Team Structure

```
Katie Chabvonga (Manager)
  └── Russ Dovaston (Team Lead)
        ├── User (Contractor/Consultant - SPECTRA)
        ├── Scott Read (Excel-based reporting)
        └── Lorraine (Works with user)
```

---

## Team Members

### Russ Dovaston + Scott Read
- **Current Approach:** Excel-based tactical solutions
- **Tools:** Excel, Excel formulas
- **Data Source:** Daily exports from Jira, pulled into Excel
- **Skills:** Very good at Excel formulas
- **Migration Status:** Need to learn Power BI (stuck in Excel ways, but willing to learn)
- **Working Relationship:** Work together on Excel-based reporting

### User + Lorraine Heatley
- **Current Approach:** Data solutions (Power BI, SPECTRA methodology)
- **Tools:** Power BI, Fabric, SPECTRA pipelines
- **Data Source:** Direct pipeline connections (Jira, Zephyr)
- **Skills:** 
  - User: Power BI, data modeling, SPECTRA methodology, pipeline development
  - Lorraine: Jira expert, Power BI report builder, backlog management
- **Working Relationship:** 
  - User's primary contact ("sidekick")
  - Two stand-ups per week
  - Lorraine manages backlog (JIRA project), prioritizes work
  - Lorraine builds Power BI reports using user's data sources
  - User provides data sources, Lorraine builds reports
  - Zephyr is current priority
- **Current State:**
  - Lorraine building reports on Jira and Zephyr prototypes (data flows)
  - User moved from data flows to Fabric notebooks/pipelines
  - Data flows couldn't support very big data platform
  - Jira was first pipeline implementation (not perfect)
  - Zephyr is being built properly with SPECTRA methodology

---

## Migration Path

### Current State
- **Russ & Scott:** Excel-based reporting using daily Jira exports
- **User & Lorraine:** Power BI solutions using direct pipeline connections

### Target State
- **All Team Members:** Using Jira and Zephyr models
- **Single Source of Truth:** Power BI models
- **Unified Approach:** Modular system with consistent data sources

### Migration Steps

1. **Phase 1: Excel with Models** (First Step)
   - Get Russ & Scott onto Jira and Zephyr models
   - Pull models into Excel (instead of daily exports)
   - Maintain Excel workflow but use models as source

2. **Phase 2: Power BI Adoption**
   - Russ & Scott learn Power BI
   - Move from Excel to Power BI
   - Use same models as source of truth

3. **Phase 3: Unified Platform**
   - All team members using Power BI
   - Single source of truth (Jira + Zephyr models)
   - Consistent reporting across team

---

## Key Insights

### Lorraine Heatley
- User's primary contact and "perfect sidekick"
- Expert in Jira, loves Power BI, quick learner
- Manages backlog, prioritizes work (Zephyr is current priority)
- Builds Power BI reports using user's data sources
- Very forthright, gets stuff done, doesn't take any crap
- Gets excited about Power BI work
- Has own report design style suited to users (knows what Callum likes)
- Currently using prototype data flows, will migrate to pipeline outputs

### Scott Read
- Recently asked user for advice on Power Query
- Starting to learn new approaches
- Willing to learn but currently stuck in Excel ways

### Russ Dovaston
- Very hands-off manager
- Understands user is providing a service
- Looking forward to output
- Reports progress to Katie Chabvonga

### Team Dynamics
- Russ & Scott: Excel-focused, tactical solutions
- User & Lorraine: Power BI-focused, strategic solutions
- Goal: Unify approach with models as single source of truth

---

## Success Criteria

- [ ] Russ & Scott using Jira/Zephyr models in Excel
- [ ] Russ & Scott learning Power BI
- [ ] All team members using same data models
- [ ] Single source of truth established
- [ ] Consistent reporting across team

---

**Last Updated:** 2025-01-29

