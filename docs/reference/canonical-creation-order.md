# Canonical API Creation Order - Experimentally Discovered

> **Discovered:** 2025-12-08T19:22:32.960187  
> **Method:** Systematic experimentation with minimal payloads  
> **Success Rate:** 3/8 (37.5%)  

---

## ✅ Working Creation Order

1. **release** (ID: 147) → independent
2. **requirement_folder** (ID: 706) → independent
3. **requirement** (ID: 707) → depends on: requirement_folder

## ❌ Blockers

- **testcase_folder:** All attempts failed - API broken

## 🌳 Dependency Graph

```
[independent] → release
[independent] → requirement_folder
requirement_folder → requirement
```
