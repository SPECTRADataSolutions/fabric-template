# Add These Variables to Fabric Variable Library

**Variable Library:** `zephyrVariables`

**Add these 4 new variables in Fabric UI:**

---

## Variables to Add

### 1. SOURCE_SYSTEM
- **Type:** String
- **Value:** `zephyr`
- **Note:** From contract.yaml sourceSystem.key

### 2. SOURCE_NAME
- **Type:** String
- **Value:** `Zephyr Enterprise`
- **Note:** From contract.yaml sourceSystem.name

### 3. STAGE
- **Type:** String
- **Value:** `source`
- **Note:** Current SPECTRA stage

### 4. NOTEBOOK_NAME
- **Type:** String
- **Value:** `sourceZephyr`
- **Note:** Notebook identifier for logging/monitoring

---

## Existing Variables (Update Names)

**IMPORTANT:** Rename these variables (remove `DXC_ZEPHYR_` prefix):

Old Name → New Name:
- `DXC_ZEPHYR_BASE_URL` → `BASE_URL`
- `DXC_ZEPHYR_BASE_PATH` → `BASE_PATH`
- `DXC_ZEPHYR_API_TOKEN` → `API_TOKEN`

**Why:** Variable Library `zephyrVariables` already provides namespace isolation.
No need for redundant prefixes inside.

---

## Steps to Add in Fabric

1. Open **Fabric** workspace
2. Navigate to **zephyrVariables** (Variable Library artifact)
3. Click **"Add variable"** for each of the 4 new variables
4. Enter Name, Type, Value, and Note as shown above
5. **Save** the Variable Library

**After adding all 4, the notebook will work!**

