# Meeting Ops

**Transform meeting transcripts into structured summaries, decisions, action items, and follow-ups**

## What This Agent Does

Meeting Ops helps Product Managers and engineering leads run effective meetings with consistent documentation and action tracking. It processes meeting transcripts to extract decisions, action items, and discussion highlights, then generates follow-up documents and updates trackers.

The agent demonstrates:
- **Google API Toolsets** (Calendar, Gmail, Docs, Sheets) - *Note: Demo mode by default*
- **Tool Confirmation** for all write operations
- **MemoryService** for tracking team conventions and cross-meeting analysis

### Example Prompts

1. **"Here's the transcript. Extract decisions and action items; update the tracker; draft a follow-up email."**
   - Input: Meeting transcript (paste or file)
   - Output: Summary, action tracker CSV, follow-up email draft

2. **"Create an agenda for next week based on last week's open actions and unresolved topics."**
   - Input: Context from previous meeting
   - Output: Structured agenda with time allocations

3. **"What decisions did we make about launch scope across the last 3 meetings?"**
   - Input: Query about historical decisions
   - Output: Summary of relevant decisions (uses memory)

## Architecture Overview

### Agents
- **Root Agent**: Single LLM agent that orchestrates meeting analysis workflow

### Tools
- **Transcript Parser**: Parse speaker turns and structure
- **Action Item Extractor**: Identify action items with owners/dates
- **Decision Extractor**: Capture decisions with context
- **Meeting Doc Creator**: Generate Google Doc (requires confirmation in integration mode)
- **Action Tracker Updater**: Update Google Sheets (requires confirmation in integration mode)
- **Email Drafter**: Draft follow-up email via Gmail (requires confirmation in integration mode)
- **Artifact Writer**: Save all outputs locally

### Memory
- **MemoryService**: Stores team conventions, recurring attendees, decision history
- Enables cross-meeting queries like "What did we decide last month?"

### Artifacts
All outputs saved to `artifacts/`:
- `meeting_summary.md` - Full structured summary
- `action_items.csv` - Action tracker
- `followup_email.md` - Draft email
- `decisions_log.md` - Decision record

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

### 3. Optional: Google Workspace OAuth (for Docs, Sheets, Gmail)

**By default, Meeting Ops works in "demo mode"** - it saves everything as local artifacts (MD, CSV files). No Google OAuth needed!

To enable actual Google Workspace integration:

1. Create OAuth credentials at [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
   - Enable APIs: Google Docs, Sheets, Gmail
   - Create OAuth 2.0 Client ID
   - Add authorized scopes: `docs`, `sheets`, `gmail.compose`

2. Add to `.env`:
   ```
   GOOGLE_OAUTH_CLIENT_ID=your_client_id
   GOOGLE_OAUTH_CLIENT_SECRET=your_client_secret
   ```

3. First run will prompt for OAuth consent

**Note**: Even with OAuth, all write operations require Tool Confirmation - you'll be asked to approve each action.

## Run

### Command Line Interface

```bash
# From the meeting_ops directory
adk run .

# Or from the parent directory
adk run meeting_ops
```

Example session:
```
> I have a meeting transcript. Here it is:
  [paste transcript]
  Extract decisions, action items, and draft a follow-up email.
```

### Web Interface (Development UI)

```bash
# From the parent directory (python/agents/)
cd ..
adk web --port 8000
```

Open http://localhost:8000 and select "meeting_ops" from the agent list.

### API Server Mode

For teams who want to integrate Meeting Ops into another UI:

```bash
# From the meeting_ops directory
adk serve --port 8080

# View interactive API docs at:
# http://localhost:8080/docs
```

You can then call the agent via REST API:
```bash
curl -X POST http://localhost:8080/run \
  -H "Content-Type: application/json" \
  -d '{"input": "Analyze this transcript: ..."}'
```

## Demo Data

The agent includes a sample meeting transcript in `data/sample_transcript.txt`:

```
Sarah (PM): Good morning everyone. Thanks for joining today's product review...
John (Engineering): Before we get into roadmap, I wanted to flag...
...
```

### Transcript Format

The parser recognizes common transcript formats:

**Format 1: "Name: Text"**
```
John: I think we should prioritize the mobile app.
Sarah: Agreed. Let's make it a Q1 goal.
```

**Format 2: "[Name] Text"**
```
[John] I think we should prioritize the mobile app.
[Sarah] Agreed. Let's make it a Q1 goal.
```

**Format 3: Plain paragraphs** (LLM will infer structure)

### Try These Prompts

1. **Basic analysis**:
   ```
   Load data/sample_transcript.txt and extract:
   - All decisions made
   - Action items with owners and due dates
   - Key discussion points
   ```

2. **Full workflow**:
   ```
   Analyze the transcript in data/sample_transcript.txt. Create:
   1. Meeting summary
   2. Action items tracker (CSV)
   3. Follow-up email to all attendees
   ```

3. **Agenda generation**:
   ```
   Based on the sample transcript, create an agenda for next week's meeting. 
   Include: open action items, unresolved questions, and suggested new topics.
   ```

4. **Decision search** (requires memory from previous runs):
   ```
   What decisions have we made about mobile app priority across our meetings?
   ```

## Optional Integrations

### Demo Mode (Default - No OAuth)

Without Google OAuth, Meeting Ops:
- Parses transcripts ✓
- Extracts decisions and action items ✓
- Generates summaries ✓
- Saves everything as local artifacts (MD, CSV) ✓
- Cannot create actual Google Docs ✗
- Cannot update actual Google Sheets ✗
- Cannot draft actual Gmail emails ✗

**This is perfect for trying it out or using as a documentation tool.**

### Integration Mode (Optional - With OAuth)

With Google OAuth configured, Meeting Ops can:
- Create actual Google Docs with meeting summaries
- Update actual Google Sheets action trackers
- Draft actual Gmail follow-up emails
- All write operations require Tool Confirmation (you approve each action)

To enable:
1. Set up OAuth credentials (see Setup section)
2. Tools will prompt: "Create a Google Doc with meeting summary? [Yes/No]"
3. Approve or deny each action

## Project Structure

```
meeting_ops/
├── agent.py                    # Main agent definition
├── __init__.py                 # Package initialization
├── requirements.txt            # Python dependencies
├── .env.example                # Example environment config
├── README.md                   # This file
├── data/
│   └── sample_transcript.txt   # Demo meeting transcript
└── artifacts/                  # Generated outputs (runtime)
    ├── meeting_summary.md
    ├── action_items.csv
    ├── followup_email.md
    └── decisions_log.md
```

## Understanding Memory

Meeting Ops uses ADK's `MemoryService` to learn and track:

### What Gets Stored in Memory

1. **Team Conventions**: 
   - How your team phrases action items
   - Preferred formats for summaries
   - Common abbreviations or jargon

2. **Recurring Context**:
   - Who attends regularly
   - What topics come up repeatedly
   - Ongoing projects or initiatives

3. **Decision History**:
   - Previous decisions for cross-meeting queries
   - Decision taxonomy

### Cross-Meeting Queries

After running a few meetings through the agent:
```
> What did we decide about the mobile app across our last 3 product reviews?

> How many times has the performance issue been discussed?

> Who owns the most action items?
```

Memory persists for the session (in-memory mode) or across sessions (with persistent backend).

## Tips

- **Clean transcripts**: Remove filler words, cross-talk for better analysis
- **Name consistency**: Use the same names/titles for speakers
- **Be explicit**: When assigning actions, say "John owns this" vs "let's do this"
- **Review before sending**: Always review generated emails/docs before sending
- **Regular cadence**: Run weekly meetings through the agent to build up memory

## Troubleshooting

**"No API key found"**: Create a `.env` file with `GOOGLE_API_KEY`.

**"File not found" for transcript**: Ensure the path is correct (relative to agent directory or absolute).

**OAuth errors**: In demo mode (default), you don't need OAuth. Only needed for actual Google integration.

**Tool confirmation not working**: Ensure your ADK version is 1.21.0+ and supports `ToolConfirmation`.

**Memory not persisting**: Default in-memory mode resets on restart. Configure persistent backend for long-term memory.

## Advanced: Understanding Tool Confirmation

This agent demonstrates `ToolConfirmation` for safe write operations:

```python
@ToolConfirmation(
    confirmation_message="Create a Google Doc with meeting summary?",
    denial_message="Skipping Google Doc creation. Summary saved as local artifact."
)
def create_meeting_doc(title: str, content: str) -> dict:
    # This function only runs if user approves
    ...
```

**How it works**:
1. Agent decides to call `create_meeting_doc`
2. User sees: "Create a Google Doc with meeting summary? [Yes/No]"
3. If Yes → Function executes, doc created
4. If No → Denial message shown, local artifact saved instead

This pattern is critical for:
- Write operations (create, update, delete)
- External API calls that cost money
- Actions that can't be easily undone
- Production systems where safety matters

Use `ToolConfirmation` for any tool that modifies external state!

## Advanced: Running as a Service

For teams integrating Meeting Ops into their workflow:

### Option 1: REST API Server

```bash
adk serve --port 8080
```

Then call via HTTP:
```python
import requests

response = requests.post("http://localhost:8080/run", json={
    "input": "Analyze this transcript: ...",
    "session_id": "weekly-product-review"  # Optional: for memory persistence
})

summary = response.json()
```

### Option 2: Python SDK

```python
from meeting_ops import root_agent

result = root_agent.run(
    "Analyze this transcript and extract action items: ...",
    session_id="weekly-product-review"
)

print(result.output)
```

### Option 3: Slack Integration

You could build a Slack bot that:
1. Joins meetings and records transcripts
2. Posts transcript to Meeting Ops agent
3. Posts summary + action items back to Slack channel
4. Updates team's action tracker (with confirmation)

The agent's REST API makes this straightforward!
