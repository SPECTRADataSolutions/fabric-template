"""Generate GitHub issues from bug and blocker registry.

Purpose:
- Parse BUG-AND-BLOCKER-REGISTRY.md
- Extract all issues (BLOCKER, BUG, DOC-GAP)
- Generate GitHub issue markdown files
- Map issues to playbooks from ISSUE-TO-PLAYBOOK-MAPPING.md

Usage:
    python scripts/generate_github_issues_from_registry.py [--dry-run] [--output-dir issues/]
"""
import re
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import argparse

# Get repository root
repo_root = Path(__file__).parent.parent
docs_dir = repo_root / "docs"
scripts_dir = repo_root / "scripts"

# Registry file
registry_file = docs_dir / "bug-and-blocker-registry.md"
mapping_file = docs_dir / "issue-to-playbook-mapping.md"


def parse_registry() -> List[Dict]:
    """Parse bug-and-blocker-registry.md and extract all issues."""
    if not registry_file.exists():
        raise FileNotFoundError(f"Registry file not found: {registry_file}")
    
    content = registry_file.read_text(encoding="utf-8")
    issues = []
    
    # Pattern to match issue headers: ### BLOCKER-001, ### BUG-001, ### DOC-GAP-001
    issue_pattern = re.compile(
        r'^### (BLOCKER|BUG|DOC-GAP)-(\d+):\s*(.+)$',
        re.MULTILINE
    )
    
    # Find all issue headers
    matches = list(issue_pattern.finditer(content))
    
    for i, match in enumerate(matches):
        issue_type = match.group(1)
        issue_number = match.group(2)
        issue_title = match.group(3).strip()
        
        # Find the content between this match and the next (or end of file)
        start_pos = match.end()
        if i + 1 < len(matches):
            end_pos = matches[i + 1].start()
        else:
            # Find next section header (##) or end of file
            next_section = re.search(r'^## ', content[start_pos:], re.MULTILINE)
            if next_section:
                end_pos = start_pos + next_section.start()
            else:
                end_pos = len(content)
        
        issue_content = content[start_pos:end_pos].strip()
        
        # Extract metadata from issue content
        metadata = extract_metadata(issue_content, issue_type, issue_number)
        
        issue = {
            "id": f"{issue_type}-{issue_number}",
            "type": issue_type,
            "number": int(issue_number),
            "title": issue_title,
            "content": issue_content,
            **metadata
        }
        
        issues.append(issue)
    
    return issues


def extract_metadata(content: str, issue_type: str, issue_number: str) -> Dict:
    """Extract metadata from issue content."""
    metadata = {
        "status": None,
        "severity": None,
        "impact": None,
        "date_discovered": None,
        "playbooks": [],
        "workaround": None,
        "test_evidence": None,
        "report_status": "⏳ Pending"
    }
    
    # Extract Status
    status_match = re.search(r'\*\*Status:\*\*\s*(.+?)(?:\n|$)', content)
    if status_match:
        metadata["status"] = status_match.group(1).strip()
    
    # Extract Severity
    severity_match = re.search(r'\*\*Severity:\*\*\s*(.+?)(?:\n|$)', content)
    if severity_match:
        metadata["severity"] = severity_match.group(1).strip()
    
    # Extract Impact
    impact_match = re.search(r'\*\*Impact:\*\*\s*(.+?)(?:\n|$)', content)
    if impact_match:
        metadata["impact"] = impact_match.group(1).strip()
    
    # Extract Date Discovered
    date_match = re.search(r'\*\*Date Discovered:\*\*\s*(\d{4}-\d{2}-\d{2})', content)
    if date_match:
        metadata["date_discovered"] = date_match.group(1)
    
    # Extract Workaround
    workaround_match = re.search(r'\*\*Workaround:\*\*\s*(.+?)(?=\n\*\*|$)', content, re.DOTALL)
    if workaround_match:
        metadata["workaround"] = workaround_match.group(1).strip()
    
    # Extract Test Evidence
    evidence_match = re.search(r'\*\*Test Evidence:\*\*\s*(.+?)(?=\n\*\*|$)', content, re.DOTALL)
    if evidence_match:
        metadata["test_evidence"] = evidence_match.group(1).strip()
    
    # Extract Report Status
    report_match = re.search(r'\*\*Report to Zephyr:\*\*\s*(.+?)(?:\n|$)', content)
    if report_match:
        metadata["report_status"] = report_match.group(1).strip()
    
    return metadata


def parse_playbook_mapping() -> Dict[str, List[str]]:
    """Parse issue-to-playbook-mapping.md to get issue -> playbook mapping."""
    if not mapping_file.exists():
        print(f"Warning: Mapping file not found: {mapping_file}")
        return {}
    
    content = mapping_file.read_text(encoding="utf-8")
    mapping = {}
    
    # Pattern to match issue references in playbook sections
    # Example: - **BLOCKER-002:** Test Repository Folder Creation API Broken
    issue_ref_pattern = re.compile(
        r'^- \*\*(BLOCKER|BUG|DOC-GAP)-(\d+):\*\*',
        re.MULTILINE
    )
    
    # Find playbook sections
    playbook_pattern = re.compile(r'#### `([^`]+)`', re.MULTILINE)
    playbook_matches = list(playbook_pattern.finditer(content))
    
    for i, playbook_match in enumerate(playbook_matches):
        playbook_name = playbook_match.group(1)
        
        # Find content between this playbook and the next
        start_pos = playbook_match.end()
        if i + 1 < len(playbook_matches):
            end_pos = playbook_matches[i + 1].start()
        else:
            # Find next section header (##) or end of file
            next_section = re.search(r'^## ', content[start_pos:], re.MULTILINE)
            if next_section:
                end_pos = start_pos + next_section.start()
            else:
                end_pos = len(content)
        
        playbook_content = content[start_pos:end_pos]
        
        # Find all issue references in this playbook section
        issue_refs = issue_ref_pattern.findall(playbook_content)
        for issue_type, issue_number in issue_refs:
            issue_id = f"{issue_type}-{issue_number}"
            if issue_id not in mapping:
                mapping[issue_id] = []
            mapping[issue_id].append(playbook_name)
    
    return mapping


def determine_stage(playbooks: List[str]) -> Optional[str]:
    """Determine SPECTRA stage from playbook names."""
    if not playbooks:
        return None
    
    # Extract stage from first playbook (e.g., "prepare.001" -> "prepare")
    first_playbook = playbooks[0]
    stage_match = re.match(r'^(\w+)\.', first_playbook)
    if stage_match:
        stage = stage_match.group(1)
        # Capitalize first letter
        return stage.capitalize()
    
    return None


def generate_issue_markdown(issue: Dict, playbooks: List[str]) -> str:
    """Generate GitHub issue markdown from issue data."""
    issue_type_emoji = {
        "BLOCKER": "[BLOCKER]",
        "BUG": "[BUG]",
        "DOC-GAP": "[DOC-GAP]"
    }
    
    emoji = issue_type_emoji.get(issue["type"], "[ISSUE]")
    stage = determine_stage(playbooks)
    
    # Build labels (zephyr-backlog project labels)
    labels = [
        "project:zephyr",
        "type:bug" if issue["type"] in ["BLOCKER", "BUG"] else "type:documentation",
        "type:blocker" if issue["type"] == "BLOCKER" else None,
        "vendor:zephyr",
        f"severity:{issue.get('severity', 'medium').lower()}" if issue.get("severity") else None,
        "api-issue",
        "zephyr-support",
        f"stage:{stage.lower()}" if stage else None,
    ]
    labels = [l for l in labels if l]
    
    # Add playbook labels
    for playbook in playbooks:
        playbook_label = playbook.replace(".", "-")
        labels.append(f"playbook:{playbook_label}")
    
    # Build issue body
    body_parts = [
        f"**Registry ID:** {issue['id']}",
        f"**Type:** {issue['type']}",
        f"**Stage:** {stage or 'N/A'}",
        f"**Playbooks:** {', '.join(f'`{p}`' for p in playbooks) if playbooks else 'Not mapped'}",
        f"**Severity:** {issue.get('severity', 'Medium')}",
        f"**Status:** {issue.get('status', 'Unknown')}",
        f"**Date Discovered:** {issue.get('date_discovered', 'Unknown')}",
        f"**Report Status:** {issue.get('report_status', 'Pending Report')}",
        "",
        "---",
        "",
        f"## Description",
        "",
        issue.get('content', 'No content available'),
    ]
    
    # Add workaround section if available
    if issue.get('workaround'):
        body_parts.extend([
            "",
            "---",
            "",
            "## Workaround",
            "",
            issue['workaround'],
        ])
    
    # Add test evidence section if available
    if issue.get('test_evidence'):
        body_parts.extend([
            "",
            "---",
            "",
            "## Test Evidence",
            "",
            issue['test_evidence'],
        ])
    
    # Add related links
    body_parts.extend([
        "",
        "---",
        "",
        "## Related",
        "",
        f"- Registry: `docs/bug-and-blocker-registry.md`",
        f"- Mapping: `docs/issue-to-playbook-mapping.md`",
    ])
    
    if playbooks:
        playbook_links = []
        for playbook in playbooks:
            # Determine playbook path
            stage_match = re.match(r'^(\w+)\.', playbook)
            if stage_match:
                stage_name = stage_match.group(1)
                playbook_path = f"Core/operations/playbooks/fabric/{stage_name.replace('prepare', '2-prepare').replace('source', '1-source')}/{playbook}.md"
                playbook_links.append(f"- Playbook: `{playbook_path}`")
        
        if playbook_links:
            body_parts.extend(playbook_links)
    
    body = "\n".join(body_parts)
    
    # Generate issue markdown
    issue_markdown = f"""---
title: "{emoji} [{issue['id']}] {issue['title']}"
labels: {json.dumps(labels, indent=2)}
assignees: []
---

{body}
"""
    
    return issue_markdown


def main():
    parser = argparse.ArgumentParser(
        description="Generate GitHub issues from bug and blocker registry"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print issues to console without creating files"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="issues",
        help="Output directory for issue files (default: issues/)"
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format (default: markdown)"
    )
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("Generating GitHub Issues from Bug & Blocker Registry")
    print("Project: zephyr-backlog")
    print("=" * 80)
    print()
    
    # Parse registry
    print("Parsing registry...")
    issues = parse_registry()
    print(f"   Found {len(issues)} issues")
    
    # Parse playbook mapping
    print("Parsing playbook mapping...")
    playbook_mapping = parse_playbook_mapping()
    print(f"   Found {len(playbook_mapping)} issue mappings")
    
    # Generate issues
    print()
    print("Generating issue files...")
    
    output_dir = Path(args.output_dir)
    if not args.dry_run:
        output_dir.mkdir(exist_ok=True)
    
    generated = []
    
    for issue in issues:
        issue_id = issue["id"]
        playbooks = playbook_mapping.get(issue_id, [])
        
        if args.format == "markdown":
            issue_markdown = generate_issue_markdown(issue, playbooks)
            
            if args.dry_run:
                print()
                print("=" * 80)
                print(f"Issue: {issue_id}")
                print("=" * 80)
                # Use sys.stdout with UTF-8 encoding for emoji support
                import sys
                if sys.stdout.encoding != 'utf-8':
                    # Write to file and read back for display
                    import tempfile
                    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False, suffix='.md') as f:
                        f.write(issue_markdown)
                        temp_file = f.name
                    print(f"   Issue markdown written to: {temp_file}")
                else:
                    print(issue_markdown)
            else:
                output_file = output_dir / f"{issue_id.lower()}.md"
                output_file.write_text(issue_markdown, encoding="utf-8")
                print(f"   OK: Generated: {output_file}")
                generated.append(str(output_file))
        else:
            # JSON format
            issue_json = {
                "title": f"[{issue_id}] {issue['title']}",
                "body": generate_issue_markdown(issue, playbooks),
                "labels": [l for l in [
                    "bug" if issue["type"] in ["BLOCKER", "BUG"] else "documentation",
                    "blocker" if issue["type"] == "BLOCKER" else None,
                    "api-issue",
                    "zephyr-support",
                ] if l],
                "metadata": {
                    "registry_id": issue_id,
                    "type": issue["type"],
                    "stage": determine_stage(playbooks),
                    "playbooks": playbooks,
                    **{k: v for k, v in issue.items() if k not in ["id", "type", "title", "content"]}
                }
            }
            
            if args.dry_run:
                print()
                print("=" * 80)
                print(f"Issue: {issue_id}")
                print("=" * 80)
                print(json.dumps(issue_json, indent=2))
            else:
                output_file = output_dir / f"{issue_id.lower()}.json"
                output_file.write_text(json.dumps(issue_json, indent=2), encoding="utf-8")
                print(f"   OK: Generated: {output_file}")
                generated.append(str(output_file))
    
    print()
    print("=" * 80)
    print("Summary")
    print("=" * 80)
    print(f"Total issues: {len(issues)}")
    print(f"Generated files: {len(generated)}")
    
    if not args.dry_run:
        print()
        print("Next steps:")
        print("   1. Review generated issue files")
        print("   2. Create issues in GitHub Project 'zephyr-backlog' using:")
        print("      - GitHub CLI: `gh issue create --title '...' --body-file issues/BLOCKER-001.md`")
        print("      - GitHub UI: Copy markdown from files, add to zephyr-backlog project")
        print("      - GitHub API: Use JSON files with API")
        print()
        print(f"   Files generated in: {output_dir.absolute()}")
        print()
        print("   Project Config: Core/operations/config/projects/zephyr-backlog.yml")
        print("   Project Docs: Data/zephyr/docs/zephyr-backlog-project.md")


if __name__ == "__main__":
    main()

