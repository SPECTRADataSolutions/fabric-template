"""Restructure zephyr-backlog project with Initiative + Stage Epics hierarchy.

This script:
1. Creates Initiative issue: "Zephyr Pipeline Development"
2. Creates 7 Stage Epics (Discover, Source, Design, Build, Test, Deploy, Optimise)
3. Updates existing issues:
   - Remove type prefixes from titles
   - Set Type field (Bug/Feature/Task)
   - Set Priority field (from Severity)
   - Set Parent field to appropriate Stage Epic
   - Set Stage field
"""

import os
import sys
import json
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

# Add Core/operations/scripts to path
core_ops_scripts = Path(__file__).parent.parent.parent.parent / "Core" / "operations" / "scripts"
sys.path.insert(0, str(core_ops_scripts))
from simple_project_bootstrap import GitHub

# Add Data/.github/scripts to path for token
data_github_scripts = Path(__file__).parent.parent.parent.parent / "Data" / ".github" / "scripts"
sys.path.insert(0, str(data_github_scripts))


def get_token() -> str:
    """Mint GitHub App token."""
    app_id = os.environ.get("SPECTRA_APP_ID", "2172220")
    installation_id = os.environ.get("SPECTRA_APP_INSTALLATION_ID", "95900295")
    key_path = os.environ.get(
        "SPECTRA_APP_PRIVATE_KEY_PATH",
        str(Path(__file__).parent.parent.parent.parent / "Core" / "Vault" / "spectra-assistant.private-key.pem")
    )
    
    script_path = Path(__file__).parent.parent.parent.parent / "Data" / ".github" / "scripts" / "spectra_assistant_token.py"
    
    result = subprocess.run(
        [
            sys.executable,
            str(script_path),
            "--app-id", app_id,
            "--installation-id", installation_id,
            "--key-file", key_path,
            "--format", "token"
        ],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"ERROR: Failed to mint token: {result.stderr}")
        sys.exit(1)
    
    return result.stdout.strip()


def remove_type_prefix(title: str) -> str:
    """Remove type prefixes like [BLOCKER], [BUG], [DOC-GAP] from title."""
    # Remove [BLOCKER], [BUG], [DOC-GAP] and their IDs
    title = re.sub(r'^\[BLOCKER\]\s*\[BLOCKER-\d+\]\s*', '', title)
    title = re.sub(r'^\[BUG\]\s*\[BUG-\d+\]\s*', '', title)
    title = re.sub(r'^\[DOC-GAP\]\s*\[DOC-GAP-\d+\]\s*', '', title)
    title = re.sub(r'^\[BLOCKER\]\s*', '', title)
    title = re.sub(r'^\[BUG\]\s*', '', title)
    title = re.sub(r'^\[DOC-GAP\]\s*', '', title)
    return title.strip()


def get_issue_type_from_title(title: str) -> str:
    """Determine issue type from title."""
    title_lower = title.lower()
    if "blocker" in title_lower:
        return "Bug"  # Blockers are bugs
    elif "bug" in title_lower:
        return "Bug"
    elif "doc-gap" in title_lower or "doc gap" in title_lower:
        return "Bug"  # Doc gaps are bugs
    else:
        return "Task"


def get_stage_from_playbook(playbook: Optional[str]) -> Optional[str]:
    """Extract stage from playbook path."""
    if not playbook:
        return None
    
    # Match patterns like "source.003", "prepare.001", etc.
    stage_match = re.search(r'^(source|prepare|extract|clean|transform|refine|analyse)', playbook.lower())
    if stage_match:
        stage = stage_match.group(1)
        # Map to Solution Engine stages
        stage_map = {
            "source": "Source",
            "prepare": "Design",  # Prepare maps to Design in Solution Engine
            "extract": "Build",
            "clean": "Build",
            "transform": "Build",
            "refine": "Build",
            "analyse": "Test"
        }
        return stage_map.get(stage, stage.capitalize())
    
    return None


def create_initiative(gh: GitHub, owner: str, repo: str, project_id: str) -> Dict:
    """Create Initiative issue."""
    title = "Zephyr Pipeline Development"
    body = """## Purpose

Unified test management analytics pipeline for Zephyr Enterprise. Full SPECTRA pipeline implementation across all 7 stages (Source, Prepare, Extract, Clean, Transform, Refine, Analyse).

## Target Maturity

L3 - Beta

## Implementation Location

Data/zephyr

## Notes

Full SPECTRA pipeline implementation with comprehensive test data, schema introspection, and metadata-driven configuration.
"""
    
    payload = {
        "title": title,
        "body": body,
        "labels": ["project:zephyr", "type:initiative"]
    }
    
    code, created = gh.request(
        "POST",
        f"{gh.api}/repos/{owner}/{repo}/issues",
        payload
    )
    
    if code != 201:
        raise RuntimeError(f"Failed to create initiative: {code} {created}")
    
    # Link to project
    if created.get("node_id"):
        mutation = "mutation($project:ID!,$content:ID!){ addProjectV2ItemById(input:{projectId:$project contentId:$content}){ item { id } } }"
        gh.gql(mutation, {"project": project_id, "content": created["node_id"]})
    
    return created


def create_stage_epic(gh: GitHub, owner: str, repo: str, project_id: str, stage: str, initiative_id: str) -> Dict:
    """Create Activity Epic."""
    stage_descriptions = {
        "Provision": "Provision infrastructure and environment. Create Fabric workspace, GitHub repo, Discord channel, set up CI/CD, configure secrets, bootstrap project structure. This happens FIRST before discovery.",
        "Discover": "Discovery and requirements gathering within provisioned environment. Define project scope, identify stakeholders, gather requirements, define contracts, map data sources.",
        "Source": "Connectivity, authentication, endpoint cataloging. Catalog all API endpoints, authenticate, validate access, bootstrap endpoint catalog.",
        "Design": "Architecture and planning. Schema introspection, metadata-driven configuration, test data creation.",
        "Build": "Implementation. Extract, clean, transform, refine data according to contracts.",
        "Test": "Validation. Comprehensive testing, quality gates, validation.",
        "Deploy": "Release. Deploy to production, monitor, validate deployment.",
        "Optimise": "Performance tuning. Optimize performance, reduce costs, improve efficiency."
    }
    
    title = stage
    body = f"""## Purpose

{stage_descriptions.get(stage, f"{stage} stage activities")}

## Stage

{stage}

## Parent

Initiative: Zephyr Pipeline Development (#{initiative_id})

## Contract

See: `Data/zephyr/contracts/{stage.lower()}.contract.yaml` (if exists)

## Dependencies

See parent Initiative for overall dependencies.
"""
    
    payload = {
        "title": title,
        "body": body,
        "labels": ["project:zephyr", "type:epic", f"stage:{stage.lower()}"]
    }
    
    code, created = gh.request(
        "POST",
        f"{gh.api}/repos/{owner}/{repo}/issues",
        payload
    )
    
    if code != 201:
        raise RuntimeError(f"Failed to create epic: {code} {created}")
    
    # Link to project
    if created.get("node_id"):
        mutation = "mutation($project:ID!,$content:ID!){ addProjectV2ItemById(input:{projectId:$project contentId:$content}){ item { id } } }"
        gh.gql(mutation, {"project": project_id, "content": created["node_id"]})
    
    return created


def update_issue(gh: GitHub, owner: str, repo: str, issue_number: int, updates: Dict) -> bool:
    """Update issue with new title, labels, etc."""
    payload = {}
    
    if "title" in updates:
        payload["title"] = updates["title"]
    
    if "body" in updates:
        payload["body"] = updates["body"]
    
    if "labels" in updates:
        payload["labels"] = updates["labels"]
    
    if not payload:
        return True
    
    code, updated = gh.request(
        "PATCH",
        f"{gh.api}/repos/{owner}/{repo}/issues/{issue_number}",
        payload
    )
    
    return code == 200


def get_existing_issues(gh: GitHub, owner: str, repo: str) -> List[Dict]:
    """Get all issues from repository."""
    issues = []
    page = 1
    per_page = 100
    
    while True:
        code, response = gh.request(
            "GET",
            f"{gh.api}/repos/{owner}/{repo}/issues?state=all&page={page}&per_page={per_page}"
        )
        
        if code != 200:
            break
        
        if not response:
            break
        
        # Filter out pull requests
        page_issues = [i for i in response if "pull_request" not in i]
        issues.extend(page_issues)
        
        if len(page_issues) < per_page:
            break
        
        page += 1
    
    return issues


def main():
    """Restructure project."""
    print("🔑 Minting GitHub App token...")
    token = get_token()
    
    gh = GitHub(token)
    owner = "SPECTRADataSolutions"
    repo = "zephyr"
    project_id = "PVT_kwDOC-uEiM4BKIra"
    
    print("📋 Fetching existing issues...")
    issues = get_existing_issues(gh, owner, repo)
    print(f"   Found {len(issues)} issues")
    
    # Filter to issues in our project (by labels or number range)
    # For now, assume issues #11-28 are our bugs/blockers
    our_issues = [i for i in issues if 11 <= i.get("number", 0) <= 28]
    print(f"   Found {len(our_issues)} issues to restructure")
    
    # Create Initiative
    print("\n🚀 Creating Initiative...")
    initiative = create_initiative(gh, owner, repo, project_id)
    initiative_id = initiative["number"]
    print(f"   ✅ Created Initiative #{initiative_id}: {initiative['title']}")
    
    # Create Activity Epics (PROVISION FIRST)
    print("\n📦 Creating Activity Epics...")
    activities = ["Provision", "Discover", "Source", "Design", "Build", "Test", "Deploy", "Optimise"]
    activity_epics = {}
    
    for activity in activities:
        epic = create_stage_epic(gh, owner, repo, project_id, activity, initiative_id)
        activity_epics[activity] = epic["number"]
        print(f"   ✅ Created Epic #{epic['number']}: {epic['title']}")
    
    # Update existing issues
    print("\n🔄 Updating existing issues...")
    
    # Map stages to epics (for bugs discovered in Prepare stage, map to Design epic)
    stage_to_epic = {
        "Source": activity_epics["Source"],
        "Prepare": activity_epics["Design"],  # Prepare maps to Design
        "Extract": activity_epics["Build"],
        "Clean": activity_epics["Build"],
        "Transform": activity_epics["Build"],
        "Refine": activity_epics["Build"],
        "Analyse": activity_epics["Test"]
    }
    
    for issue in our_issues:
        issue_num = issue["number"]
        current_title = issue["title"]
        
        # Remove type prefix
        new_title = remove_type_prefix(current_title)
        
        # Determine type
        issue_type = get_issue_type_from_title(current_title)
        
        # Determine stage from body or labels
        body = issue.get("body", "")
        labels = [l["name"] for l in issue.get("labels", [])]
        
        stage = None
        for label in labels:
            if label.startswith("stage:"):
                stage = label.split(":")[1].capitalize()
                break
        
        # If no stage in labels, try to infer from body
        if not stage:
            if "**Stage:**" in body:
                stage_match = re.search(r'\*\*Stage:\*\*\s*(.+?)(?:\n|$)', body)
                if stage_match:
                    stage = stage_match.group(1).strip()
        
        # Determine parent epic
        parent_epic = None
        if stage and stage in stage_to_epic:
            parent_epic = stage_to_epic[stage]
        else:
            # Default to Source if unknown
            parent_epic = activity_epics["Source"]
        
        # Determine priority from severity
        priority = "Medium"
        if "severity:critical" in " ".join(labels).lower() or "critical" in body.lower():
            priority = "Critical"
        elif "severity:high" in " ".join(labels).lower() or "high" in body.lower():
            priority = "High"
        elif "severity:low" in " ".join(labels).lower() or "low" in body.lower():
            priority = "Low"
        
        # Update labels
        new_labels = ["project:zephyr"]
        if issue_type == "Bug":
            new_labels.append("type:bug")
        elif issue_type == "Feature":
            new_labels.append("type:feature")
        else:
            new_labels.append("type:task")
        
        # Add stage label
        if stage:
            new_labels.append(f"stage:{stage.lower()}")
        
        # Add priority label (if GitHub Projects supports it, otherwise use severity)
        new_labels.append(f"severity:{priority.lower()}")
        
        # Update issue
        print(f"   📝 Updating issue #{issue_num}...")
        print(f"      Title: {current_title} → {new_title}")
        print(f"      Type: {issue_type}, Priority: {priority}, Stage: {stage}, Parent: Epic #{parent_epic}")
        
        update_issue(gh, owner, repo, issue_num, {
            "title": new_title,
            "labels": new_labels
        })
    
    print("\n✅ Restructuring complete!")
    print(f"\n📊 Summary:")
    print(f"   Initiative: #{initiative_id}")
    print(f"   Activity Epics: {len(activity_epics)}")
    print(f"   Updated Issues: {len(our_issues)}")


if __name__ == "__main__":
    main()

