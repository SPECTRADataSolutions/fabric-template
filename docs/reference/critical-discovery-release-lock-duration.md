# Critical Discovery: Release Lock Duration >60s

> **Discovered:** 2025-12-08  
> **Script:** `full_api_hierarchy_discovery.py`  
> **Impact:** 🔥 **CRITICAL** - Blocks automated cycle creation

---

## 🔴 Problem

**Zephyr locks releases after creation for MORE than 60 seconds.**

Even after waiting 60 seconds, attempting to create a cycle returns:
```json
{
  "errorMsg": "Operation failed. The Release with ID147 and nameDiscovery Test Release 20251208-192027 is locked. Please try again later."
}
```

---

## 🧪 Experimental Evidence

**Test Matrix:**
- 15-second delay: ❌ FAIL - "Release locked"
- 30-second delay: ❌ FAIL - "Release locked"
- 60-second delay: ❌ FAIL - "Release locked"

**Conclusion:** Lock duration is **>60 seconds**, possibly **2-5 minutes**.

---

## 💡 Implications

### For Automated Testing

**Current approach (sequential):**
1. Create release
2. Wait for unlock
3. Create cycle
4. Continue...

**Problem:** Waiting 2-5 minutes per release makes automated testing VERY slow.

---

## ✅ Solutions

### Solution 1: Use Existing Releases (RECOMMENDED)

**Instead of creating new releases, use existing ones:**

```python
# Get existing releases
response = requests.get(
    f"{BASE_URL}/release/project/{PROJECT_ID}",
    headers=headers
)
existing_releases = response.json()

# Use oldest release (most likely unlocked)
release_id = existing_releases[0]["id"]

# Now create cycle immediately (no wait needed)
```

**Advantages:**
- No waiting
- Faster testing
- Uses real release data

**Disadvantages:**
- Pollutes existing releases with test cycles
- May need cleanup after

---

### Solution 2: Pre-Create Releases in UI

**Manual setup before automation:**
1. Manually create 3-5 releases in UI
2. Note their IDs
3. Use those IDs in automation scripts

**Advantages:**
- Known good releases
- No lock issues
- Clean separation

---

### Solution 3: Accept Long Delays

**For truly autonomous operation:**
- Wait 5 minutes after each release creation
- Very slow but fully automated

---

## 📋 Recommended Approach

**For test data creation:**

1. **Check for existing releases first**
2. **If exists → use existing (no delay)**
3. **If not exists → create and wait 5 minutes**
4. **Or:** Pre-create releases manually and hardcode IDs

**For the Star Wars test dataset:**

Pre-create these releases in UI:
- "The Death Star Project - Phase 1" (ID: 131 already exists!)
- "Rebel Alliance - Scarif Mission" 
- "Operation Cinder - Contingency Protocol"

Then automation can use these IDs directly without creation or delays.

---

## 🎯 Next Steps

1. **Check existing releases in SpectraTestProject**
2. **Use existing release IDs for cycle/execution testing**
3. **Update test data builder to use existing releases**
4. **Document which releases to use**

---

**Status:** 🔴 Critical Discovery  
**Impact:** Blocks sequential automated testing  
**Workaround:** Use existing releases

