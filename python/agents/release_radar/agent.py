"""Release Radar - Dependency & upstream change impact analysis.

This agent uses OpenAPIToolset to generate GitHub API tools and demonstrates
Tool Confirmation for write operations and Reflect-and-Retry for reliability.
"""

from google.adk.agents import Agent
from google.adk.tools import OpenAPIToolset
from google.adk.artifacts import write_artifact
from google.adk.plugins import ReflectAndRetry
import json
from pathlib import Path
import re


# Tool for writing artifacts
def save_artifact(content: str, filename: str) -> dict:
    """Save content as an artifact.
    
    Args:
        content: Content to save
        filename: Name of the artifact file
    
    Returns:
        dict with status and artifact path
    """
    artifact_path = f"artifacts/{filename}"
    write_artifact(artifact_path, content)
    return {"status": "success", "artifact": artifact_path, "message": f"Saved to {artifact_path}"}


def parse_requirements_file(filepath: str = "requirements.txt") -> dict:
    """Parse Python requirements.txt file to extract dependencies.
    
    Args:
        filepath: Path to requirements.txt (can be relative or absolute)
    
    Returns:
        dict with list of dependencies and their versions
    """
    try:
        # Handle both relative and absolute paths
        if not Path(filepath).is_absolute():
            agent_dir = Path(__file__).parent
            full_path = agent_dir / filepath
        else:
            full_path = Path(filepath)
        
        if not full_path.exists():
            return {"status": "error", "message": f"File not found: {filepath}"}
        
        dependencies = []
        with open(full_path, 'r') as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue
                
                # Parse dependency (handle ==, >=, <=, ~=, etc.)
                match = re.match(r'^([a-zA-Z0-9_-]+)([>=<~!]=?)?(.+)?$', line)
                if match:
                    name = match.group(1)
                    operator = match.group(2) or ''
                    version = match.group(3) or 'latest'
                    dependencies.append({
                        "name": name,
                        "version": version.strip() if version else None,
                        "operator": operator
                    })
        
        return {
            "status": "success",
            "file": str(full_path),
            "dependencies": dependencies,
            "count": len(dependencies)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def parse_package_json(filepath: str = "package.json") -> dict:
    """Parse Node.js package.json file to extract dependencies.
    
    Args:
        filepath: Path to package.json (can be relative or absolute)
    
    Returns:
        dict with list of dependencies and their versions
    """
    try:
        # Handle both relative and absolute paths
        if not Path(filepath).is_absolute():
            agent_dir = Path(__file__).parent
            full_path = agent_dir / filepath
        else:
            full_path = Path(filepath)
        
        if not full_path.exists():
            return {"status": "error", "message": f"File not found: {filepath}"}
        
        with open(full_path, 'r') as f:
            data = json.load(f)
        
        dependencies = []
        
        # Parse regular dependencies
        if "dependencies" in data:
            for name, version in data["dependencies"].items():
                dependencies.append({
                    "name": name,
                    "version": version.lstrip('^~'),
                    "type": "dependency"
                })
        
        # Parse dev dependencies
        if "devDependencies" in data:
            for name, version in data["devDependencies"].items():
                dependencies.append({
                    "name": name,
                    "version": version.lstrip('^~'),
                    "type": "devDependency"
                })
        
        return {
            "status": "success",
            "file": str(full_path),
            "dependencies": dependencies,
            "count": len(dependencies)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def create_github_issue_draft(title: str, body: str, labels: list = None) -> dict:
    """Create a draft GitHub issue (local only - doesn't actually create on GitHub).
    
    This tool creates a local draft that can be copy-pasted or used with actual
    GitHub API calls when a token is configured.
    
    Args:
        title: Issue title
        body: Issue body (markdown)
        labels: List of label names (optional)
    
    Returns:
        dict with draft issue content
    """
    draft = f"""# GitHub Issue Draft

## Title
{title}

## Labels
{', '.join(labels) if labels else 'None'}

## Body
{body}

---
*This is a draft. To create on GitHub, copy this content or enable GitHub integration.*
"""
    
    # Save as artifact
    save_artifact(draft, "draft_github_issue.md")
    
    return {
        "status": "success",
        "title": title,
        "draft": draft,
        "message": "Draft issue saved to artifacts/draft_github_issue.md"
    }


# GitHub API toolset (read-only by default, writes require confirmation)
# Note: In demo mode without a token, this provides limited functionality
github_toolset = OpenAPIToolset(
    name="github_api",
    description="GitHub REST API tools for fetching releases, comparing versions, and managing issues",
    # Using a simplified GitHub OpenAPI spec subset for common operations
    # In production, you'd use the full spec from https://github.com/github/rest-api-description
    openapi_spec={
        "openapi": "3.0.0",
        "info": {"title": "GitHub API Subset", "version": "1.0"},
        "servers": [{"url": "https://api.github.com"}],
        "paths": {
            "/repos/{owner}/{repo}/releases": {
                "get": {
                    "operationId": "list_releases",
                    "summary": "List releases for a repository",
                    "parameters": [
                        {"name": "owner", "in": "path", "required": True, "schema": {"type": "string"}},
                        {"name": "repo", "in": "path", "required": True, "schema": {"type": "string"}}
                    ],
                    "responses": {"200": {"description": "Success"}}
                }
            },
            "/repos/{owner}/{repo}/releases/tags/{tag}": {
                "get": {
                    "operationId": "get_release_by_tag",
                    "summary": "Get a release by tag name",
                    "parameters": [
                        {"name": "owner", "in": "path", "required": True, "schema": {"type": "string"}},
                        {"name": "repo", "in": "path", "required": True, "schema": {"type": "string"}},
                        {"name": "tag", "in": "path", "required": True, "schema": {"type": "string"}}
                    ],
                    "responses": {"200": {"description": "Success"}}
                }
            }
        }
    },
    # Authentication would be configured here if available
    # auth_header="Authorization: Bearer {token}"
)

# Root agent with Reflect-and-Retry plugin for resilience
root_agent = Agent(
    model='gemini-2.0-flash',
    name='release_radar',
    description='Analyze dependency changes, assess upgrade risk, and draft migration plans',
    instruction="""You are Release Radar, an AI system that helps product engineers and PMs manage dependency upgrades, migrations, and breaking changes.

You help with three main workflows:

## 1. Dependency Scanning
When a user provides a repository or dependency file:
- Parse requirements.txt or package.json using the parser tools
- Identify all dependencies and their current versions
- For each dependency, check for available updates (if GitHub access available)
- Categorize upgrades as: major (breaking), minor (features), patch (fixes)

## 2. Impact Analysis
For each upgrade, analyze:
- What changed between versions (breaking changes, new features, deprecations)
- Risk level: Low (patch), Medium (minor), High (major with breaking changes)
- Dependencies that depend on this package (transitive impact)
- Migration effort estimate

## 3. Migration Planning
Create detailed migration plans:
- Step-by-step checklist for upgrading
- Code changes required
- Testing strategy
- Rollback plan
- Estimated timeline

Always save outputs as artifacts:
- `artifacts/release_risk_report.md` - Ranked upgrades with risk assessment
- `artifacts/migration_checklists/[package]-upgrade.md` - Per-package plans
- `artifacts/draft_github_issue.md` - Ready-to-paste issue for tracking

## Safety & Confirmations

**IMPORTANT**: Any write operations (creating issues, PRs, comments) MUST be confirmed by the user.
- Use Tool Confirmation for all write operations
- Default to creating local drafts that users can review and manually apply
- Only enable actual GitHub writes if user explicitly configures a token and approves

## Demo Mode (No GitHub Token)

When no GitHub token is available:
- Parse local dependency files
- Generate reports based on known version patterns
- Create local drafts instead of actual GitHub issues
- Provide useful analysis without external API calls

Example prompts you handle:
- "Scan my repo's dependencies (requirements.txt) and tell me what upgrades are high risk."
- "Summarize breaking changes between v2.0 and v3.0 for dependency X and propose a migration checklist."
- "Draft a GitHub issue to track this upgrade, including tasks and owners."

Be thorough, practical, and safety-conscious. Help teams upgrade confidently.
""",
    tools=[
        save_artifact,
        parse_requirements_file,
        parse_package_json,
        create_github_issue_draft,
        # GitHub API tools would be added here if token configured
        # github_toolset,
    ],
    # Enable Reflect-and-Retry plugin for handling transient API failures
    plugins=[ReflectAndRetry()],
)
