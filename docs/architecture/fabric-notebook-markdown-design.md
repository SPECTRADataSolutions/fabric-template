# Fabric Notebook Markdown Design Guide

**Date:** 2025-12-08  
**Purpose:** Cool markdown formatting techniques that work in Microsoft Fabric notebooks

---

## 🎨 Design Principles

Based on research and SPECTRA standards:

- Pure markdown preferred (readable by agents and humans)
- Clean, minimal, professional
- Visual appeal through structure, not decoration
- Consistent across all notebooks

---

## ✨ Cool Markdown Features That Work in Fabric

### 1. Tables with Alignment & Emojis

```markdown
| Stage      |   Status    |    Count |
| :--------- | :---------: | -------: |
| ✅ Source  |  Complete   | 4 tables |
| ⏳ Prepare | In Progress | 2 tables |
| ⚠️ Extract |   Blocked   | 0 tables |
```

**Result:** Clean, aligned data with visual indicators

---

### 2. Task Lists for Progress Tracking

```markdown
## ✅ Stage Completion

- [x] Authentication validated
- [x] Endpoints catalog bootstrapped
- [x] Portfolio table created
- [ ] Schema introspection (Prepare stage)
- [ ] Data extraction (Extract stage)
```

**Result:** Interactive checkboxes showing progress

---

### 3. Blockquotes for Emphasis

```markdown
> **Note:** This stage requires API authentication.
> Ensure `API_TOKEN` is set in Variable Library.

> **Warning:** Resource access validation is non-critical.
> Failures will be logged but won't stop execution.
```

**Result:** Visual callouts for important information

---

### 4. Code Blocks with Syntax Highlighting

````markdown
**Example Output:**

```python
df = spark.table("source.portfolio")
df.show(truncate=False)
```
````

````

**Result:** Syntax-highlighted code examples

---

### 5. Nested Lists with Emojis

```markdown
## 📊 Output Tables

- **Metadata Tables:**
  - `source.portfolio` - Source system overview
  - `source.config` - Configuration settings
  - `source.credentials` - Authentication details (masked)
- **Catalog Tables:**
  - `source.endpoints` - Complete API endpoint catalog (224 endpoints)
````

**Result:** Hierarchical structure with visual grouping

---

### 6. Horizontal Rules for Section Separation

```markdown
# Main Title

---

## Section One

Content here

---

## Section Two

More content
```

**Result:** Clear visual separation between sections

---

### 7. Emphasis Combinations

```markdown
**Bold text** for importance  
_Italic text_ for subtle emphasis  
**_Bold and italic_** for strong emphasis  
`Code` for technical terms  
~~Strikethrough~~ for deprecated items
```

**Result:** Multiple text styling options

---

### 8. Emoji Lists for Quick Scanning

```markdown
## 🎯 Key Features

🔐 **Authentication** - Validated via API token  
📚 **Endpoint Catalog** - 224 endpoints discovered  
📊 **Portfolio** - Dashboard-ready metrics  
✅ **Validation** - Automated quality checks
```

**Result:** Scannable, visual feature list

---

### 9. Definition-Style Lists

```markdown
## 📋 Configuration

**Variable Library:** `zephyrVariables`  
**Contract Version:** `3.0.0`  
**Source System:** `Zephyr Enterprise`  
**Lakehouse:** `zephyrLakehouse`
```

**Result:** Clean key-value pairs

---

### 10. Status Badges (Text-Based)

```markdown
## Pipeline Status

**Status:** ✅ `Success` | ⚠️ `Warning` | ❌ `Failed`

**Execution Mode:** `Interactive` | `Pipeline`

**Validation:** ✅ `All tests passed` | ❌ `2 errors detected`
```

**Result:** Visual status indicators using emojis and code formatting

---

## 🎨 SPECTRA-Grade Header Templates

### Template 1: Simple & Clean

```markdown
# 📡 Source Stage — Zephyr Enterprise

**Purpose:**  
Establishes connectivity, validates authentication, and catalogs all available API endpoints.

---

## 📊 Outputs

- `source.portfolio`
- `source.config`
- `source.credentials`
- `source.endpoints`
```

### Template 2: Status-Focused

```markdown
# 📡 Source Stage — Zephyr Enterprise

**Status:** ✅ Active  
**Contract:** `3.0.0`  
**Purpose:** Establishes connectivity, validates authentication, and catalogs all available API endpoints.

---

## 📊 Outputs

| Table                | Purpose                    |
| -------------------- | -------------------------- |
| `source.portfolio`   | Source system overview     |
| `source.config`      | Configuration settings     |
| `source.credentials` | Authentication (masked)    |
| `source.endpoints`   | API endpoint catalog (224) |
```

### Template 3: Feature-Rich

```markdown
# 📡 Source Stage — Zephyr Enterprise

**Purpose:**  
Establishes connectivity, validates authentication, and catalogs all available API endpoints for downstream pipeline stages.

---

## 🎯 Capabilities

- ✅ Authentication validated
- ✅ 224 endpoints catalogued
- ✅ Portfolio metrics generated
- ✅ Validation tests automated

## 📊 Outputs

- `source.portfolio` - Dashboard-ready metrics
- `source.config` - Configuration settings
- `source.credentials` - Masked authentication
- `source.endpoints` - Complete API catalog
```

### Template 4: Minimal SPECTRA (Recommended)

```markdown
# 📡 Source Stage — Zephyr Enterprise

**Purpose:**  
Establishes connectivity, validates authentication, and catalogs all available API endpoints for downstream pipeline stages.

---

## 📊 Outputs

- `source.portfolio`
- `source.config`
- `source.credentials`
- `source.endpoints`
```

---

## 💡 Advanced Tips

### Combining Elements

```markdown
## 🔍 Validation Results

> **Summary:** All checks passed ✅

| Check             | Status | Details                      |
| ----------------- | :----: | ---------------------------- |
| Portfolio table   |   ✅   | 1 row, all fields present    |
| Endpoints catalog |   ✅   | 224 endpoints, no duplicates |
| Config table      |   ✅   | 6 configuration keys         |
| Credentials table |   ✅   | Token masked (\*\*\*\_XYZ)   |
```

### Status Indicators

```markdown
**Execution Status:**  
✅ `Success` | ⚠️ `Warning` | ❌ `Failed` | ⏳ `In Progress`

**Validation:**

- [x] Portfolio validated
- [x] Endpoints validated
- [x] Config validated
- [ ] Credentials validated (skipped)
```

### Callout Boxes Using Blockquotes

```markdown
> **📌 Important:**  
> This stage must complete successfully before Prepare stage can run.

> **💡 Tip:**  
> Query `source.portfolio` for dashboard-ready metrics.

> **⚠️ Warning:**  
> Resource access failures are non-critical and logged as warnings.
```

---

## 🎯 Recommended SPECTRA Header (Final)

Based on research and SPECTRA standards, this is the recommended format:

```markdown
# 📡 Source Stage — Zephyr Enterprise

**Purpose:**  
Establishes connectivity, validates authentication, and catalogs all available API endpoints for downstream pipeline stages.

---

## 📊 Outputs

- `source.portfolio`
- `source.config`
- `source.credentials`
- `source.endpoints`
```

**Why this works:**

- ✅ Clean, minimal, professional
- ✅ Uses SPECTRA emoji conventions (📡 for source)
- ✅ Structured with horizontal rule
- ✅ Scannable outputs list
- ✅ Pure markdown (no HTML)
- ✅ Consistent with SPECTRA doc style

---

**Last Updated:** 2025-12-08
