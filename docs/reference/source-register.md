# Zephyr Enterprise Source Documentation Register
**Date:** 2025-01-29  
**Status:** 🟢 Active  
**Last Updated:** 2025-01-29

---

## Purpose

This register catalogs all documentation sources for the Zephyr Enterprise source system. All documentation links should be maintained here and referenced in the contract/manifest.

---

## Primary Documentation Sources

### API Documentation

- **API Reference (Apiary):** https://zephyrenterprisev3.docs.apiary.io
  - **Purpose:** REST API endpoint documentation
  - **Status:** ✅ Scraped (228 endpoints identified)
  - **Scraped Output:** `docs/endpoints.json`
  - **Last Scraped:** 2025-01-29

### Support Documentation

- **Support Portal:** https://support.smartbear.com/zephyr-enterprise/
  - **Purpose:** Official Zephyr Enterprise support documentation
  - **Includes:**
    - Installation and upgrade guides
    - Administration guides
    - User guides
    - REST API documentation
    - Troubleshooting
  - **Status:** ✅ Active

### Welcome/Overview Documentation

- **Welcome to Zephyr Enterprise:** https://support.smartbear.com/zephyr-enterprise/docs/en/welcome-to-zephyr-enterprise.html
  - **Purpose:** Overview, concepts, system architecture, roles
  - **Status:** ✅ Active

---

## Documentation Categories

### Installation & Setup

- **Installation Guides:** https://support.smartbear.com/zephyr-enterprise/docs/en/zephyr-installation-and-upgrade-guides.html
- **System Requirements:** https://support.smartbear.com/zephyr-enterprise/docs/en/zephyr-system-requirements.html
- **Trial Installation:** https://support.smartbear.com/zephyr-enterprise/docs/en/zephyr-enterprise-trial.html

### Administration

- **Administration Guides:** https://support.smartbear.com/zephyr-enterprise/docs/en/zephyr-administration-guides.html
- **System Setup:** https://support.smartbear.com/zephyr-enterprise/docs/en/system-setup.html
- **Authentication:** https://support.smartbear.com/zephyr-enterprise/docs/en/authentication.html
- **Jira Integration:** https://support.smartbear.com/zephyr-enterprise/docs/en/jira-integration.html

### User Guides

- **User Guide:** https://support.smartbear.com/zephyr-enterprise/docs/en/zephyr-user-guide.html
- **Release Setup:** https://support.smartbear.com/zephyr-enterprise/docs/en/release-setup.html
- **Requirements:** https://support.smartbear.com/zephyr-enterprise/docs/en/requirements.html
- **Test Repository:** https://support.smartbear.com/zephyr-enterprise/docs/en/test-repository.html
- **Test Planning:** https://support.smartbear.com/zephyr-enterprise/docs/en/test-planning.html
- **Test Execution:** https://support.smartbear.com/zephyr-enterprise/docs/en/test-execution.html
- **Reporting and Dashboards:** https://support.smartbear.com/zephyr-enterprise/docs/en/reporting-and-dashboards.html

### REST API

- **REST API Documentation:** https://support.smartbear.com/zephyr-enterprise/docs/en/zephyr-rest-api.html
- **API Reference (Apiary):** https://zephyrenterprisev3.docs.apiary.io
- **Create and Manage API Tokens:** https://support.smartbear.com/zephyr-enterprise/docs/en/create-and-manage-api-tokens-in-zephyr.html

### Integration & Migration

- **Jira Integration:** https://support.smartbear.com/zephyr-enterprise/docs/en/jira-integration.html
- **Migration Guides:** https://support.smartbear.com/zephyr-enterprise/docs/en/migrating-zephyr-enterprise-to-qmetry.html

### Support & Troubleshooting

- **Support Portal:** https://support.smartbear.com/zephyr-enterprise/
- **Troubleshooting:** Various guides under support portal
- **Status Page:** https://status.smartbear.com/

---

## Contract References

### Current Contract Values

From `contract.yaml`:
- **documentationUrl:** `https://zephyrenterprisev3.docs.apiary.io` (API reference)
- **supportUrl:** `https://support.smartbear.com/zephyr-enterprise/` (Support portal)

### Recommended Updates

The contract should reference this register for comprehensive documentation links. Consider adding:
- `documentationRegisterUrl`: Link to this register
- `apiDocumentationUrl`: API reference (Apiary)
- `userDocumentationUrl`: User guides
- `adminDocumentationUrl`: Administration guides

---

## Documentation Status

| Category | Status | Last Verified | Notes |
|----------|--------|---------------|-------|
| API Reference | ✅ Active | 2025-01-29 | Scraped, 228 endpoints |
| Support Portal | ✅ Active | 2025-01-29 | Comprehensive docs |
| Installation | ✅ Active | 2025-01-29 | Available |
| Administration | ✅ Active | 2025-01-29 | Available |
| User Guides | ✅ Active | 2025-01-29 | Available |
| REST API | ✅ Active | 2025-01-29 | Available |

---

## Maintenance

- **Owner:** Mark Maconnachie (SPECTRA)
- **Review Frequency:** Quarterly or when major Zephyr updates occur
- **Update Trigger:** When new documentation sources are discovered or URLs change

---

## Related Documents

- **Contract:** `contract.yaml`
- **Endpoints:** `docs/endpoints.json`
- **Discovery Session:** `DISCOVERY-SESSION-2025-01-29.md`
- **API Discovery:** `docs/api-discovery/pagination-rate-limits.md`

---

**Last Updated:** 2025-01-29

