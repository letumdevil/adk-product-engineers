# Release Radar

**Analyze dependency changes, assess upgrade risk, and create migration plans**

## What This Agent Does

Release Radar helps product engineers and PMs manage dependency upgrades, migrations, and breaking changes. It scans your dependencies, identifies what needs upgrading, assesses risk, and creates actionable migration plans.

The agent demonstrates:
- **OpenAPIToolset** for generating GitHub API tools from specs
- **Tool Confirmation** for safe write operations
- **Reflect-and-Retry plugin** for handling transient API failures

### Example Prompts

1. **"Scan my repo's dependencies (requirements.txt / package.json) and tell me what upgrades are high risk."**
   - Input: Path to dependency file
   - Output: Risk-ranked upgrade report

2. **"Summarize breaking changes between vX and vY for dependency Z and propose a migration checklist."**
   - Input: Package name and version range
   - Output: Detailed migration plan

3. **"Draft a GitHub issue to track this upgrade, including tasks and owners."**
   - Input: Upgrade details
   - Output: Ready-to-paste GitHub issue draft

## Architecture Overview

### Agents
- **Root Agent**: Single LLM agent with tools for dependency analysis and report generation

### Tools
- **Dependency Parsers**: Parse `requirements.txt` (Python) and `package.json` (Node.js)
- **Artifact Writer**: Save reports, checklists, and drafts locally
- **GitHub Issue Drafter**: Create issue templates without requiring GitHub access
- **OpenAPIToolset** (optional): Generate GitHub REST API tools for reading releases and comparing versions

### Safety Features
- **Tool Confirmation**: All write operations (creating issues, PRs) require user approval
- **Reflect-and-Retry Plugin**: Automatically handles transient API failures (rate limits, timeouts)

### Memory
None (stateless - each scan is independent)

### Artifacts
All outputs saved to `artifacts/`:
- `release_risk_report.md` - Ranked upgrades with risk assessment
- `migration_checklists/[package]-upgrade.md` - Per-package migration plans
- `draft_github_issue.md` - Ready-to-paste GitHub issue

## Setup

### 1. Install Python Dependencies

```bash
# Create and activate virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Key

**Option A: Gemini API (Simple - for development/testing)**

1. Get a free API key from [Google AI Studio](https://aistudio.google.com/)
2. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
3. Edit `.env` and add your key:
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

**Option B: Vertex AI (Enterprise - for production)**

1. Set up Google Cloud project with Vertex AI enabled
2. Configure authentication:
   ```bash
   gcloud auth application-default login
   ```
3. Edit `.env`:
   ```
   GOOGLE_CLOUD_PROJECT=your-project-id
   GOOGLE_CLOUD_LOCATION=us-central1
   ```

### 3. Optional: GitHub Token (for write operations)

**By default, Release Radar works without GitHub access** - it creates local drafts you can copy-paste.

To enable actual GitHub API calls:

1. Create a Personal Access Token at https://github.com/settings/tokens
   - Select scopes: `repo` (for private repos) or `public_repo` (for public only)
2. Add to `.env`:
   ```
   GITHUB_TOKEN=your_github_token_here
   ```

**Note**: Even with a token, write operations (creating issues/PRs) require Tool Confirmation - you'll be prompted to approve each action.

## Run

### Command Line Interface

```bash
# From the release_radar directory
adk run .

# Or from the parent directory
adk run release_radar
```

Example session:
```
> Scan data/sample_requirements.txt and tell me what upgrades are available 
  and which ones are high risk.
```

### Web Interface (Development UI)

```bash
# From the parent directory (python/agents/)
cd ..
adk web --port 8000
```

Open http://localhost:8000 and select "release_radar" from the agent list.

## Demo Data

The agent includes sample dependency files in `data/`:

**Python dependencies** (`data/sample_requirements.txt`):
```
flask==2.0.1
requests>=2.28.0
numpy==1.21.0
pandas>=1.3.0
pytest==7.1.0
```

**Node.js dependencies** (`data/sample_package.json`):
```json
{
  "dependencies": {
    "express": "^4.17.1",
    "lodash": "^4.17.20",
    "axios": "^0.21.1"
  },
  "devDependencies": {
    "jest": "^27.0.0",
    "eslint": "^7.32.0"
  }
}
```

### Try These Prompts

1. **Scan Python dependencies**:
   ```
   Parse data/sample_requirements.txt and identify which packages have major 
   updates available. Assess the risk of upgrading each one.
   ```

2. **Analyze Node.js dependencies**:
   ```
   Scan data/sample_package.json and create a risk report for all dependencies. 
   Focus on any security vulnerabilities or breaking changes.
   ```

3. **Create migration plan**:
   ```
   Create a detailed migration checklist for upgrading Flask from 2.0.1 to 3.0.0. 
   Include breaking changes, code changes needed, and testing strategy.
   ```

4. **Draft GitHub issue**:
   ```
   Draft a GitHub issue to track upgrading all dependencies in sample_requirements.txt. 
   Include tasks, priority, and effort estimates.
   ```

## Optional Integrations

### No GitHub Token (Default - "Demo Mode")

Without a GitHub token, Release Radar:
- Parses local dependency files ✓
- Generates risk reports ✓
- Creates migration checklists ✓
- Saves local drafts of GitHub issues ✓
- Cannot fetch actual release data from GitHub ✗
- Cannot create actual GitHub issues/PRs ✗

**This is perfect for trying it out or using as a planning tool.**

### With GitHub Token ("Integration Mode")

With a configured GitHub token, Release Radar can also:
- Fetch actual release notes and changelogs from GitHub
- Compare version diffs
- Read existing issues and PRs
- Create actual GitHub issues/PRs (with Tool Confirmation)

To enable:
1. Add `GITHUB_TOKEN` to `.env`
2. The agent will prompt for confirmation before any write operation
3. You can review and approve/deny each action

## Optional Integrations

Release Radar works entirely with local files by default. You could extend it to:

- **Automated Security Scanning**: Integrate with Snyk, Dependabot, or GitHub Security Advisories
- **Automated PR Creation**: Generate pull requests with dependency updates (behind confirmation)
- **Slack/Email Notifications**: Alert teams when high-risk upgrades are detected
- **Dependency Graph Analysis**: Visualize transitive dependencies and their upgrade impacts

These are not implemented to keep the sample simple and runnable.

## Project Structure

```
release_radar/
├── agent.py                      # Main agent definition
├── __init__.py                   # Package initialization
├── requirements.txt              # Python dependencies
├── .env.example                  # Example environment config
├── README.md                     # This file
├── data/
│   ├── sample_requirements.txt   # Demo Python dependencies
│   └── sample_package.json       # Demo Node.js dependencies
└── artifacts/                    # Generated outputs (runtime)
    ├── release_risk_report.md
    ├── migration_checklists/
    │   └── [package]-upgrade.md
    └── draft_github_issue.md
```

## Tips

- **Start with low-risk upgrades**: Patch versions are usually safe
- **Read changelogs**: Always review breaking changes before upgrading
- **Test thoroughly**: Upgrade dev dependencies first, then production
- **Use version ranges wisely**: `^` and `~` can auto-update but may introduce breaks
- **Monitor transitive dependencies**: Your dependency's dependencies matter too

## Troubleshooting

**"No API key found"**: Create a `.env` file with `GOOGLE_API_KEY`.

**"File not found" when parsing**: Ensure the path is correct (relative to agent directory or absolute).

**GitHub API rate limit**: Without authentication, GitHub limits to 60 requests/hour. With a token, you get 5,000/hour.

**OpenAPI tool errors**: If you see OpenAPI-related errors, ensure your ADK version is 1.21.0+ and supports OpenAPIToolset.

## Advanced: Understanding the OpenAPIToolset Pattern

This agent demonstrates how to use `OpenAPIToolset` to automatically generate tools from OpenAPI/Swagger specs:

```python
github_toolset = OpenAPIToolset(
    name="github_api",
    description="GitHub REST API tools",
    openapi_spec={...},  # OpenAPI 3.0 spec
    auth_header="Authorization: Bearer {token}"
)
```

Benefits:
- No manual tool writing for each API endpoint
- Type-safe API calls with validation
- Automatic retry logic (with Reflect-and-Retry plugin)
- Easy to update when API changes

You can use this pattern with any REST API that has an OpenAPI spec!
