# Zephyr Requirement Tree Structure

**Issue:** Requirements created under wrong folder location.

---

## 🎯 Current Structure (Incorrect)

```
Project Requirements (root)
├── REQ-001: Core Reactor Stabilit... (Folder ID: 698)
│   └── REQ-DS-001: Planet Destruction Capability (ID: 6455)
│   └── REQ-DS-002: Thermal Exhaust Port Security (ID: 6456)
│   └── REQ-DS-003: Core Reactor Stability (ID: 6457)
└── The Death Star Project... (Folder - should contain requirements)
```

**Problem:** Requirements are under "REQ-001: Core Reactor Stabilit..." folder, but should be under "The Death Star Project" folder.

---

## ✅ Desired Structure (Correct)

```
Project Requirements (root)
├── REQ-001: Core Reactor Stabilit... (Folder ID: 698 - can be removed or kept as category)
└── The Death Star Project... (Folder - should contain all Death Star requirements)
    ├── REQ-DS-001: Planet Destruction Capability (ID: 6455)
    ├── REQ-DS-002: Thermal Exhaust Port Security (ID: 6456)
    └── REQ-DS-003: Core Reactor Stability (ID: 6457)
```

---

## 🔍 Understanding Requirement Tree Structure

**From API Schema (requirement_6455_schema.json):**
```json
{
  "requirementTreeIds": [698]  // Array of folder/tree node IDs
}
```

**Key Insight:**
- `requirementTreeIds` is an **array** - requirements can belong to multiple folders
- Requirements are linked to folders via `requirementTreeIds`
- To move a requirement, we need to update this array

---

## 🛠️ Solutions

### **Option 1: Move Requirements via UI**
1. In Zephyr UI, select the requirement
2. Look for "Move" or "Change Folder" option
3. Move to "The Death Star Project" folder

### **Option 2: Update via API (if endpoint exists)**
- Try `PUT /requirement/{id}` with updated `requirementTreeIds`
- Or try `PUT /requirementtree/move` or similar endpoint

### **Option 3: Recreate Requirements in Correct Location**
- Delete current requirements
- Create new ones under "The Death Star Project" folder

---

## 📋 Next Steps

1. **Check UI for move option** - Look for drag-and-drop or context menu
2. **Try API update** - Test if `PUT /requirement/{id}` can update `requirementTreeIds`
3. **Document folder structure** - Understand how folders relate to requirements

---

## 🔗 Related

- **Requirement Schema:** `docs/schemas/discovered/requirements/requirement_6455_schema.json`
- **API Discoveries:** `docs/ZEPHYR-API-DISCOVERIES.md`
- **Folder Structure:** Need to understand folder hierarchy better

