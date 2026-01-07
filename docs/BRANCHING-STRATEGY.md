# SPECTRA Fabric Template - Branching Strategy

**Date:** 2026-01-06  
**Status:** ✅ Active Standard  
**Applies To:** Fabric workspace repositories (created from this template)

---

## 🎯 Strategy: Feature → Main (Simple, Monthly Releases)

**Branch Model:**

```
feature/* → main (production)
     ↓         ↓
  Feature   Monthly
  Branch    Release
```

**SPECTRA uses feature branches that merge directly to main, with monthly release cycles for validation and deployment.**

---

## 📋 Branch Types

### **`main`** (Protected - Production)

**Purpose:** Production-ready code  
**Fabric Workspace:** Production workspace  
**Deployment:** Production pipelines  
**Protection:**

- Requires PR from `feature/*` branches
- Requires CI checks to pass
- No direct commits
- Auto-delete head branches after merge

**Usage:**

- Production deployment
- Stable, validated code
- Monthly release cycle

---

### **`feature/*`** (Temporary)

**Purpose:** New features, enhancements, fixes  
**Examples:**

- `feature/add-extract-stage`
- `feature/improve-schema-validation`
- `feature/fix-api-timeout`
- `feature/add-refine-stage`

**Workflow:**

1. Branch from `main`
2. Make changes
3. Test in local Fabric workspace
4. Push and open PR to `main`
5. Merge to `main` (after review)
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
# Ensure main is up to date
git checkout main
git pull origin main

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

# Create PR to main (using GitHub CLI)
gh pr create \
  --base main \
  --title "feat: add extract stage implementation" \
  --body "Implements extract stage with API extraction logic. Closes #42"
```

---

### **4. Review and Merge**

**When PR approved and CI passes:**

```bash
# Merge via GitHub UI or CLI
gh pr merge --squash --delete-branch
```

**Fabric automatically:**

- Syncs to production workspace
- Runs production pipeline
- Validates changes

---

## 📅 Monthly Release Cycle

**SPECTRA uses monthly releases for validation and deployment:**

1. **Feature Development:** Work happens in `feature/*` branches
2. **Continuous Integration:** PRs merge to `main` as ready
3. **Monthly Review:** First Monday of each month
4. **Release Validation:** Review all changes, test, deploy
5. **Documentation:** Update CHANGELOG, create release notes

**See:** `Core/operations/playbooks/release/release.001-monthly-review-release.md`

---

## 🔒 Branch Protection Rules

### **`main` Branch**

**Required:**

- ✅ Pull request from `feature/*` branches only
- ✅ Status checks must pass (CI, lint, build)
- ✅ Conversation resolution (if comments exist)
- ✅ Auto-delete head branches after merge

**Allowed:**

- ✅ Auto-merge (when checks pass)
- ✅ Squash merging (default)

**Forbidden:**

- ❌ Direct commits to `main`
- ❌ Force pushes
- ❌ Deletion of `main` branch

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

| Branch      | Workspace                     | Purpose             |
| ----------- | ----------------------------- | ------------------- |
| `main`      | `{PROJECT}Prod.Workspace`     | Production          |
| `feature/*` | Local or shared dev workspace | Feature development |

### **Switching Branches in Fabric**

1. Go to Fabric workspace
2. Open Git integration
3. Switch to branch (e.g., `feature/add-extract`)
4. Sync branch to Fabric
5. Run pipeline
6. Test changes

---

## 📊 Comparison with Other SPECTRA Repos

| Repository          | Strategy                    | Reason                         |
| ------------------- | --------------------------- | ------------------------------ |
| **Portal**          | `feature/*` → `main`        | Web service, simple deployment |
| **Notifications**   | `feature/*` → `main`         | API service, simple deployment |
| **Assistant**       | `feature/*` → `main`         | API service, simple deployment |
| **Jira Pipeline**   | `feature/*` → `main`         | Monthly release cycle          |
| **Zephyr Pipeline** | `feature/*` → `main`        | Monthly release cycle          |
| **Fabric Template** | `feature/*` → `main`         | Monthly release cycle          |

**Rule:** All SPECTRA repos use simple `feature/*` → `main` strategy with monthly releases.

---

## ✅ Success Criteria

**Branching strategy is working when:**

1. ✅ All changes go through PRs
2. ✅ Feature branches merge directly to `main`
3. ✅ Monthly releases validate and deploy changes
4. ✅ CI checks pass before merge
5. ✅ Fabric workspaces sync correctly
6. ✅ No direct commits to `main`
7. ✅ Branches auto-delete after merge

---

## 📝 Related Documents

- **Monthly Release Playbook:** `Core/operations/playbooks/release/release.001-monthly-review-release.md`
- **Portal Branching:** `Core/portal/docs/reference/branching-strategy.md`
- **Git Workflow:** `Core/operations/playbooks/git/git.001-spectra-grade-pr-workflow.md`
- **Fabric Setup:** `TEMPLATE-USAGE.md`

---

**Version:** 2.0.0  
**Last Updated:** 2026-01-06  
**Owner:** SPECTRA Data Solutions Team  
**Status:** ✅ Active Standard
