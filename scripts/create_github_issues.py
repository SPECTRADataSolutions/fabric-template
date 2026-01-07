"""Create GitHub issues from generated markdown files."""

import os
import sys
import json
import re
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


def parse_issue_file(file_path: Path) -> Dict:
    """Parse issue markdown file and extract title, body, labels."""
    content = file_path.read_text(encoding="utf-8")
    
    # Check for YAML frontmatter
    title = None
    labels = []
    body_start = 0
    
    if content.startswith("---"):
        # Parse YAML frontmatter
        frontmatter_end = content.find("---", 3)
        if frontmatter_end > 0:
            frontmatter = content[3:frontmatter_end].strip()
            body_start = frontmatter_end + 3
            
            # Extract title from frontmatter
            title_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', frontmatter, re.MULTILINE)
            if title_match:
                title = title_match.group(1).strip()
            
            # Extract labels from frontmatter
            labels_match = re.search(r'^labels:\s*\[(.+?)\]', frontmatter, re.MULTILINE | re.DOTALL)
            if labels_match:
                labels_str = labels_match.group(1)
                # Parse labels (handle both quoted and unquoted)
                labels = [l.strip().strip('"\'') for l in labels_str.split(",") if l.strip()]
    
    # Fallback: extract title from first # header
    if not title:
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("# ") and not title:
                title = line[2:].strip()
                if body_start == 0:
                    body_start = i + 1
                break
    
    # Final fallback
    if not title:
        title = file_path.stem.replace("-", " ").title()
    
    # Extract body (everything after frontmatter or title)
    body = content[body_start:].strip()
    
    # If labels weren't extracted from frontmatter, extract from body
    if not labels:
        if "type:blocker" in content.lower() or "blocker" in file_path.stem.lower():
            labels.append("type:blocker")
        elif "type:bug" in content.lower() or "bug" in file_path.stem.lower():
            labels.append("type:bug")
        elif "doc-gap" in file_path.stem.lower():
            labels.append("type:documentation")
        
        # Extract stage from body
        if "**Stage:**" in content:
            lines = content.split("\n")
            stage_match = [line for line in lines if "**Stage:**" in line]
            if stage_match:
                stage = stage_match[0].split("**Stage:**")[1].strip()
                if stage:
                    labels.append(f"stage:{stage.lower()}")
        
        # Extract severity
        if "**Severity:**" in content:
            lines = content.split("\n")
            severity_match = [line for line in lines if "**Severity:**" in line]
            if severity_match:
                severity = severity_match[0].split("**Severity:**")[1].strip()
                if severity:
                    labels.append(f"severity:{severity.lower()}")
        
        # Add default labels
        labels.extend(["project:zephyr", "zephyr-backlog"])
    
    return {
        "title": title,
        "body": body,
        "labels": labels
    }


def create_issue(gh: GitHub, owner: str, repo: str, issue_data: Dict, project_id: str = None) -> Dict:
    """Create GitHub issue."""
    payload = {
        "title": issue_data["title"],
        "body": issue_data["body"],
        "labels": issue_data["labels"]
    }
    
    code, created = gh.request(
        "POST",
        f"{gh.api}/repos/{owner}/{repo}/issues",
        payload
    )
    
    if code != 201:
        raise RuntimeError(f"Failed to create issue: {code} {created}")
    
    # Link to project if project_id provided
    if project_id and created.get("node_id"):
        try:
            mutation = "mutation($project:ID!,$content:ID!){ addProjectV2ItemById(input:{projectId:$project contentId:$content}){ item { id } } }"
            gh.gql(mutation, {"project": project_id, "content": created["node_id"]})
            print(f"   ✅ Linked to project")
        except Exception as e:
            print(f"   ⚠️  Failed to link to project: {e}")
    
    return created


def main():
    """Create all issues from markdown files."""
    print("🔑 Minting GitHub App token...")
    token = get_token()
    
    gh = GitHub(token)
    owner = "SPECTRADataSolutions"
    repo = "zephyr"
    project_id = "PVT_kwDOC-uEiM4BKIra"  # Zephyr Pipeline Backlog project ID
    
    issues_dir = Path(__file__).parent.parent / "issues"
    if not issues_dir.exists():
        print(f"❌ Issues directory not found: {issues_dir}")
        print(f"   Run: python scripts/generate_github_issues_from_registry.py --output-dir issues")
        sys.exit(1)
    
    issue_files = sorted(issues_dir.glob("*.md"))
    if not issue_files:
        print(f"❌ No issue files found in {issues_dir}")
        sys.exit(1)
    
    print(f"📋 Found {len(issue_files)} issue files")
    print(f"🚀 Creating issues in {owner}/{repo}...\n")
    
    created = []
    failed = []
    
    for issue_file in issue_files:
        print(f"📝 Processing {issue_file.name}...")
        try:
            issue_data = parse_issue_file(issue_file)
            issue = create_issue(gh, owner, repo, issue_data, project_id)
            created.append({
                "file": issue_file.name,
                "number": issue["number"],
                "url": issue["html_url"],
                "title": issue["title"]
            })
            print(f"   ✅ Created issue #{issue['number']}: {issue['title']}")
            print(f"   🔗 {issue['html_url']}")
        except Exception as e:
            failed.append({
                "file": issue_file.name,
                "error": str(e)
            })
            print(f"   ❌ Failed: {e}")
        print()
    
    print("=" * 80)
    print("Summary")
    print("=" * 80)
    print(f"✅ Created: {len(created)}")
    print(f"❌ Failed: {len(failed)}")
    
    if created:
        print(f"\n✅ Created issues:")
        for item in created:
            print(f"   #{item['number']}: {item['title']}")
            print(f"      {item['url']}")
    
    if failed:
        print(f"\n❌ Failed issues:")
        for item in failed:
            print(f"   {item['file']}: {item['error']}")


if __name__ == "__main__":
    main()

