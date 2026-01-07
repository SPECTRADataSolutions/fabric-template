# Multi-Runner Coordination - Quick Start

**Date:** 2025-12-06  
**Status:** 🚀 Ready to Use

---

## 🎯 The SPECTRA-Grade Pattern

**Core Concept:** GitHub Issues as contracts + self-selection + autonomous coordination

---

## 📋 How It Works

### 1. **Create GitHub Issues** (Contracts)

Each feature branch gets a GitHub Issue with:
- ✅ Clear acceptance criteria
- ✅ Definition of Done
- ✅ Implementation notes
- ✅ Branch information
- ✅ Label: `status:available`

### 2. **Runners Claim Work** (Self-Selection)

**Autonomous workflow:**
1. Runner sees issue labeled `status:available`
2. Assigns themselves to the issue
3. Changes label: `status:available` → `status:in-progress`
4. Comments: "Claiming this feature. Starting work on `feature/[name]`."
5. Checks out branch and starts working

### 3. **Work in Parallel** (Isolated)

- Each runner on their own branch
- No conflicts (isolated changes)
- Progress tracked via commits and issue comments
- Test independently in Fabric

### 4. **Completion & Review** (Evidence-Based)

- Update issue with progress
- Create PR linking to issue
- Human reviews and merges
- Issue auto-closes when PR merges

---

## ✅ Benefits

1. **No Conflicts** - Separate branches = no merge conflicts
2. **Clear Ownership** - Self-assignment shows who's working on what
3. **Progress Visibility** - Issues show status of all features
4. **Autonomous** - Runners choose work independently
5. **Self-Organizing** - No central coordinator needed
6. **Evidence-Based** - Commits, PRs, tests prove completion

---

## 🚀 Quick Commands

### For Runners (Claiming Work)

```bash
# 1. List available issues (on GitHub)
# Filter: label:status:available

# 2. Claim by self-assigning (on GitHub UI)
# Assign yourself → Change label to status:in-progress

# 3. Checkout branch
git checkout feature/[name]

# 4. Work and commit
git commit -m "feat: implement [feature] (#[issue-number])"
git push

# 5. Update issue with progress (on GitHub)
# Comment with status updates, test results

# 6. When complete
# Create PR → Change label to status:ready-for-review
```

---

## 📚 Full Documentation

- **Strategy:** `docs/MULTI-RUNNER-COORDINATION.md` - Complete pattern and workflow
- **Setup Guide:** `docs/GITHUB-ISSUES-SETUP.md` - Create all issues
- **Feature Plan:** `docs/FEATURE-BRANCH-PLAN.md` - Feature details

---

## 🎯 Next Steps

1. **Create GitHub Issues** using the templates in `docs/GITHUB-ISSUES-SETUP.md`
2. **Label them** `status:available`
3. **Runners claim** by self-assigning
4. **Work in parallel** on isolated branches
5. **Review and merge** when complete

---

**Version:** 1.0.0  
**Date:** 2025-12-06

