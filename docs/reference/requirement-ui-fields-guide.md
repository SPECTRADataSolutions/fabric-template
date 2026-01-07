# Zephyr Requirement UI Fields - Fill-Out Guide

**Purpose:** Guide for filling out requirement fields in Zephyr UI for comprehensive test data and schema discovery.

---

## ✅ Required Fields (Fill These)

### **1. Requirement Name** ✅ (Already Done)
- **Value:** `REQ-DS-001: Planet Destruction Capability`
- **Status:** ✅ Completed

### **2. Description** ⭐ **CRITICAL - FILL THIS**
- **Purpose:** Tests description field, used for schema discovery
- **Value:** 
  ```
  Death Star must be capable of destroying entire planets with single superlaser blast. The superlaser must achieve sufficient power output to completely disintegrate planet-sized targets (diameter up to 20,000 km) in a single firing sequence. Power generation systems must maintain stable output during charging and firing phases.
  ```
- **Why:** Comprehensive description helps with schema introspection and provides context

### **3. Priority** ⭐ **IMPORTANT - FILL THIS**
- **Purpose:** Tests priority enum values
- **Value:** `P1` (highest priority) - or P2, P3, P4, P5 (test different values)
- **Why:** Tests enum field, helps discover valid priority values
- **Note:** Zephyr uses P1-P5 scale (P1 = highest priority)

---

## 📋 Optional Fields (Fill for Comprehensive Coverage)

### **4. ALT ID** (Optional but Recommended)
- **Purpose:** Tests alternative identifier field
- **Value:** `REQ-DS-001` (matches requirement name prefix)
- **Why:** Tests if ALT ID field exists and how it's used

### **5. LINK** (Optional)
- **Purpose:** Tests external link field
- **Value:** Leave empty for now (or add a test URL if you want)
- **Why:** Tests link field structure

---

## 🎯 Recommended Fill-Out for REQ-DS-001

**For Maximum Schema Discovery:**

1. **Description:** ✅ Fill with comprehensive text (see above)
2. **Priority:** ✅ Set to `P1` (highest priority for critical requirement)
3. **ALT ID:** ✅ Set to `REQ-DS-001`
4. **LINK:** ⏭️ Leave empty (optional)

---

## 📝 For Next Requirements

**REQ-DS-002: Thermal Exhaust Port Security**
- **Description:** "Thermal exhaust port must be protected from small fighter attacks. Port must be secured against proton torpedo strikes from single-seat fighters. Security measures must prevent access to the 2-meter diameter exhaust port that leads directly to the main reactor."
- **Priority:** `P2` (high priority)
- **ALT ID:** `REQ-DS-002`

**REQ-DS-003: Core Reactor Stability**
- **Description:** "The Death Star's core reactor must maintain stable power output of 1.08 x 10^32 watts without thermal fluctuations exceeding 0.1%. The reactor must sustain continuous operation for a minimum of 72 standard hours at full capacity. All safety protocols must be validated before operational deployment."
- **Priority:** `P1` (critical - highest priority)
- **ALT ID:** `REQ-DS-003`

---

## 🔍 Schema Discovery Benefits

**Filling out all fields helps discover:**
- Field types (string, integer, enum, date, etc.)
- Field lengths (description max length)
- Enum values (priority options)
- Required vs optional fields
- Field relationships

**After filling out, we can:**
- Capture the full requirement object via API
- Analyze all fields and their types
- Document the complete schema
- Use for testcase allocation testing

---

## ✅ Next Steps After Filling Out

1. **Save the requirement** in UI
2. **Capture via API:** `GET /requirement/6455` (or whatever endpoint works)
3. **Document the schema** in `ZEPHYR-API-DISCOVERIES.md`
4. **Proceed to next requirement** or testcase creation

