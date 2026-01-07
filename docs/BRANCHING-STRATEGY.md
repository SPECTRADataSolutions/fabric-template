# SPECTRA Fabric Template - Branching Strategy

**Date:** 2026-01-06  
**Status:** ✅ Active Standard  
**Applies To:** Fabric workspace repositories (created from this template)

---

## 🎯 Strategy: Feature → Dev → Test → Main (Multi-Stage)

**Branch Model:**

```
feature/* → dev → test → main (production)
     ↓        ↓      ↓       ↓
  Fabric   Fabric  Fabric  Fabric
  Workspace Workspace Workspace Workspace
```

**Fabric workspaces require multi-stage strategy for data validation and workspace integration.**

---

## 📋 Branch Types

### **`main`** (Protected - Production)

**Purpose:** Production-ready code  
**Fabric Workspace:** Production workspace  
**Deployment:** Production pipelines  
**Protection:**

- Requires PR from `test`
- Requires CI checks to pass
- Requires test stage validation
- No direct commits

**Usage:**
- Final production deployment
- Stable, validated code only
- All 7 SPECTRA stages complete and tested

---

### **`test`** (Pre-Production Validation)

**Purpose:** Pre-production testing and validation  
**Fabric Workspace:** Test workspace  
**Deployment:** Test pipelines  

**Workflow:**
1. Merge from `dev` when ready for testing
2. Run full pipeline validation
3. Test all 7 SPECTRA stages
4. Validate data quality
5. Merge to `main` when validated

**Usage:**
- Final validation before production
- End-to-end testing
- Data quality checks
- Performance validation

---

### **`dev`** (Development)

**Purpose:** Active development and Fabric workspace integration  
**Fabric Workspace:** Development workspace  
**Deployment:** Development pipelines  

**Workflow:**
1. Merge from `feature/*` branches
2. Continuous integration testing
3. Fabric workspace sync
4. Stage-by-stage development
5. Merge to `test` when ready

**Usage:**
- Active development
- Fabric workspace integration
- Stage implementation
- SDK updates

---

### **`feature/*`** (Temporary)

**Purpose:** New features, enhancements, fixes  
**Examples:**

- `feature/add-extract-stage`
- `feature/improve-schema-validation`
- `feature/fix-api-timeout`
- `feature/add-refine-stage`

**Workflow:**

1. Branch from `dev` (or `main` for hotfixes)
2. Make changes
3. Test in local Fabric workspace
4. Push and open PR to `dev`
5. Merge to `dev`
6. Branch auto-deleted

**Usage:**
- Isolated feature development
- Bug fixes
- Stage implementations
- SDK enhancements

---

## 🚀 Standard Workflow

### **1. Create Feature Branch**

```bash
# Ensure dev is up to date
git checkout dev
git pull origin dev

# Create feature branch
git checkout -b feature/add-extract-stage
```

---

### **2. Develop and Test**

```bash
# Make your changes
# ... edit notebooks, add stages ...

# Commit with conventional commit message
git add .
git commit -m "feat: add extract stage implementation

- Implement extract stage notebook
- Add API extraction logic
- Add error handling
- Update pipeline configuration

Closes #42"
```

---

### **3. Push and Create PR**

```bash
# Push branch
git push -u origin feature/add-extract-stage

# Create PR to dev (using GitHub CLI)
gh pr create \
  --base dev \
  --title "feat: add extract stage implementation" \
  --body "Implements extract stage with API extraction logic. Closes #42"
```

---

### **4. Merge to Dev**

**When PR approved and CI passes:**

```bash
# Merge via GitHub UI or CLI
gh pr merge --squash --delete-branch
```

**Fabric automatically:**
- Syncs to dev workspace
- Runs dev pipeline
- Validates changes

---

### **5. Promote to Test**

**When dev is stable:**

```bash
# Create PR from dev to test
gh pr create \
  --base test \
  --head dev \
  --title "Promote dev to test" \
  --body "Dev branch is stable and ready for pre-production validation"
```

**After merge:**
- Syncs to test workspace
- Runs full validation pipeline
- Tests all 7 stages

---

### **6. Promote to Main (Production)**

**When test validation passes:**

```bash
# Create PR from test to main
gh pr create \
  --base main \
  --head test \
  --title "Release to production" \
  --body "Test validation complete. Ready for production deployment."
```

**After merge:**
- Syncs to production workspace
- Deploys to production
- All stages live

---

## 🔒 Branch Protection Rules

### **`main` Branch**

**Required:**
- ✅ Pull request from `test` only
- ✅ Status checks must pass (CI, lint, build)
- ✅ Test stage validation complete
- ✅ Conversation resolution (if comments exist)
- ✅ Auto-delete head branches after merge

**Allowed:**
- ✅ Auto-merge (when checks pass)
- ✅ Squash merging (default)

**Forbidden:**
- ❌ Direct commits to `main`
- ❌ Force pushes
- ❌ Deletion of `main` branch
- ❌ PRs from `dev` or `feature/*` (must go through `test`)

---

### **`test` Branch**

**Required:**
- ✅ Pull request from `dev` only
- ✅ Status checks must pass
- ✅ Auto-delete head branches after merge

**Allowed:**
- ✅ Direct commits (for test fixes)
- ✅ Squash merging

---

### **`dev` Branch**

**Required:**
- ✅ Pull request from `feature/*` branches
- ✅ Status checks must pass

**Allowed:**
- ✅ Direct commits (for quick fixes)
- ✅ Squash merging

---

## 🎨 Commit Message Convention

**Format:**

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature or stage
- `fix`: Bug fix
- `docs`: Documentation update
- `refactor`: Code refactoring
- `test`: Add/update tests
- `chore`: Maintenance tasks

**Examples:**

```bash
# Feature
git commit -m "feat(extract): add extract stage implementation

- Implement extract stage notebook
- Add API extraction logic
- Add error handling"

# Bug fix
git commit -m "fix(source): resolve authentication timeout

The OAuth token was expiring too quickly.
Now refreshes automatically before expiry.

Closes #123"
```

---

## 🔄 Fabric Workspace Integration

### **Branch → Workspace Mapping**

| Branch | Workspace | Purpose |
|--------|-----------|---------|
| `main` | `{PROJECT}Prod.Workspace` | Production |
| `test` | `{PROJECT}Test.Workspace` | Pre-production |
| `dev` | `{PROJECT}Dev.Workspace` | Development |
| `feature/*` | Local or shared dev workspace | Feature development |

### **Switching Branches in Fabric**

1. Go to Fabric workspace
2. Open Git integration
3. Switch to branch (e.g., `dev`, `test`, `feature/add-extract`)
4. Sync branch to Fabric
5. Run pipeline
6. Test changes

---

## 📊 Comparison with Other SPECTRA Repos

| Repository          | Strategy                              | Reason                         |
| ------------------- | ------------------------------------- | ------------------------------ |
| **Portal**          | `feature/*` → `main`                  | Web service, simple deployment |
| **Notifications**   | `feature/*` → `main`                  | API service, simple deployment |
| **Assistant**       | `feature/*` → `main`                  | API service, simple deployment |
| **Jira Pipeline**   | `feature/*` → `dev` → `test` → `main` | Fabric workspace integration   |
| **Zephyr Pipeline** | `feature/*` → `dev` → `test` → `main` | Fabric workspace integration   |
| **Fabric Template** | `feature/*` → `dev` → `test` → `main` | Fabric workspace integration   |

**Rule:** Web services use simple strategy, Fabric pipelines use multi-stage.

---

## ✅ Success Criteria

**Branching strategy is working when:**

1. ✅ All changes go through PRs
2. ✅ Feature branches merge to `dev`
3. ✅ `dev` promotes to `test` after validation
4. ✅ `test` promotes to `main` after full validation
5. ✅ CI checks pass at each stage
6. ✅ Fabric workspaces sync correctly
7. ✅ No direct commits to `main`
8. ✅ Branches auto-delete after merge

---

## 📝 Related Documents

- **Portal Branching:** `Core/portal/docs/reference/branching-strategy.md`
- **Git Workflow:** `Core/operations/playbooks/git/git.001-spectra-grade-pr-workflow.md`
- **Fabric Setup:** `TEMPLATE-USAGE.md`

---

**Version:** 1.0.0  
**Last Updated:** 2026-01-06  
**Owner:** SPECTRA Data Solutions Team  
**Status:** ✅ Active Standard

