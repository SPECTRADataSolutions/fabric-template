"""Update project to use Activity hierarchy instead of Stage hierarchy.

This script:
1. Renames existing "Stage Epics" to "Activity Epics"
2. Adds Provision Activity Epic
3. Updates issue titles and labels
4. Ensures proper hierarchy: Initiative → Activity → Task
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List

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


def update_issue_title(gh: GitHub, owner: str, repo: str, issue_number: int, new_title: str) -> bool:
    """Update issue title."""
    code, updated = gh.request(
        "PATCH",
        f"{gh.api}/repos/{owner}/{repo}/issues/{issue_number}",
        {"title": new_title}
    )
    return code == 200


def create_provision_activity(gh: GitHub, owner: str, repo: str, project_id: str, initiative_id: str) -> Dict:
    """Create Provision Activity Epic."""
    title = "Provision"
    body = """## Purpose

Provision infrastructure and environment. Create Fabric workspace, GitHub repo, Discord channel, set up CI/CD, configure secrets, bootstrap project structure.

## Activity

Provision

## Parent

Initiative: Zephyr Pipeline Development (#{initiative_id})

## Dependencies

Discover activity must be complete

## Tasks

- Provision Fabric workspace
- Provision GitHub repo
- Provision Discord channel
- Set up CI/CD
- Configure secrets
- Bootstrap project structure
""".format(initiative_id=initiative_id)
    
    payload = {
        "title": title,
        "body": body,
        "labels": ["project:zephyr", "type:epic", "activity:provision"]
    }
    
    code, created = gh.request(
        "POST",
        f"{gh.api}/repos/{owner}/{repo}/issues",
        payload
    )
    
    if code != 201:
        raise RuntimeError(f"Failed to create provision activity: {code} {created}")
    
    # Link to project
    if created.get("node_id"):
        mutation = "mutation($project:ID!,$content:ID!){ addProjectV2ItemById(input:{projectId:$project contentId:$content}){ item { id } } }"
        gh.gql(mutation, {"project": project_id, "content": created["node_id"]})
    
    return created


def main():
    """Update project to Activity hierarchy."""
    print("🔑 Minting GitHub App token...")
    token = get_token()
    
    gh = GitHub(token)
    owner = "SPECTRADataSolutions"
    repo = "zephyr"
    project_id = "PVT_kwDOC-uEiM4BKIra"
    
    # Find Initiative and existing Activity Epics
    print("📋 Finding Initiative and Activity Epics...")
    
    # Get issues
    code, issues = gh.request(
        "GET",
        f"{gh.api}/repos/{owner}/{repo}/issues?state=all&per_page=100"
    )
    
    if code != 200:
        print(f"❌ Failed to fetch issues: {code}")
        sys.exit(1)
    
    # Find Initiative
    initiative = None
    for issue in issues:
        if issue.get("number") == 29 or "initiative" in " ".join([l["name"] for l in issue.get("labels", [])]).lower():
            if "Zephyr Pipeline Development" in issue.get("title", ""):
                initiative = issue
                break
    
    if not initiative:
        print("❌ Initiative not found")
        sys.exit(1)
    
    print(f"   ✅ Found Initiative: #{initiative['number']}")
    
    # Find existing Activity Epics (currently named [ACTIVITY] or [STAGE])
    activity_epics = {}
    
    for issue in issues:
        title = issue.get("title", "")
        # Remove [ACTIVITY] or [STAGE] prefix if present
        clean_title = title.replace("[ACTIVITY]", "").replace("[STAGE]", "").strip()
        if clean_title in ["Discover", "Source", "Design", "Build", "Test", "Deploy", "Optimise", "Provision"]:
            activity_epics[clean_title] = issue
            print(f"   ✅ Found Activity Epic: #{issue['number']} - {title}")
    
    # Remove [ACTIVITY] prefix from titles
    print("\n🔄 Cleaning Activity Epic titles...")
    for activity, epic in activity_epics.items():
        old_title = epic["title"]
        if "[ACTIVITY]" in old_title or "[STAGE]" in old_title:
            new_title = activity  # Just the activity name
            if update_issue_title(gh, owner, repo, epic["number"], new_title):
                print(f"   ✅ Renamed #{epic['number']}: {old_title} → {new_title}")
            else:
                print(f"   ❌ Failed to rename #{epic['number']}")
    
    # Create Provision Activity if it doesn't exist
    if "Provision" not in activity_epics:
        print("\n🚀 Creating Provision Activity...")
        provision = create_provision_activity(gh, owner, repo, project_id, initiative["number"])
        print(f"   ✅ Created Provision Activity: #{provision['number']}")
    else:
        print("\n✅ Provision Activity already exists")
    
    print("\n✅ Project updated to Activity hierarchy!")
    print(f"\n📊 Summary:")
    print(f"   Initiative: #{initiative['number']}")
    print(f"   Activity Epics: {len(activity_epics) + 1}")  # +1 for Provision if created


if __name__ == "__main__":
    main()

