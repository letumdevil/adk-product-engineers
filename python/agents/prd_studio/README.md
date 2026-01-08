# PRD Studio

**Transform product ideas into execution-ready PRDs with backlog, risks, and success metrics**

## What This Agent Does

PRD Studio is an AI-powered system that helps Product Managers and product engineers turn fuzzy product ideas into structured, comprehensive documentation. It uses a sequential pipeline of specialized agents to create:

- **Product Requirements Document (PRD)** with goals, personas, MVP scope, and requirements
- **Backlog** with user stories, acceptance criteria, and edge cases
- **Risk Register** covering security, privacy, abuse cases, and mitigations
- **Success Metrics** with instrumentation plan and analysis approach
- **Quality Review** to ensure consistency and completeness

### Example Prompts

1. **"Here's a 2-sentence product idea. Turn it into a PRD with goals/non-goals, personas, MVP scope, and success metrics."**
   - Input: "We want to build a Chrome extension that summarizes long articles using AI. Target users are busy professionals."
   - Output: Complete PRD, backlog, risk analysis, and metrics

2. **"Convert this PRD into user stories with acceptance criteria and edge cases."**
   - Input: Existing PRD document
   - Output: Structured backlog CSV with epics, stories, and acceptance criteria

3. **"Create a launch readiness checklist and a risk register (privacy, reliability, abuse cases)."**
   - Input: Product description
   - Output: Comprehensive risk analysis with mitigations

## Architecture Overview

### Agents
- **Root Agent**: `SequentialAgent` that orchestrates the entire pipeline
- **Intake & Scope Agent**: Clarifies ideas, sets non-goals, collects constraints
- **PRD Writer Agent**: Produces structured PRD with all required sections
- **Backlog Agent**: Converts requirements into user stories with acceptance criteria
- **Risk & Policy Agent**: Identifies security, privacy, abuse, and operational risks
- **Metrics Agent**: Defines north star metric, supporting metrics, and instrumentation
- **Review Agent**: Validates completeness, clarity, consistency, and quality

### Tools
- **Artifact Writing Tools**: Save PRD, backlog, risks, and metrics as downloadable artifacts
- Built-in PRD template validator (via Review Agent)

### Memory
None (stateless - each run is independent)

### Artifacts
All outputs are saved as artifacts in the `artifacts/` directory:
- `prd.md` - Product Requirements Document
- `backlog.csv` - User stories and acceptance criteria
- `risks.md` - Risk register with mitigations
- `metrics.md` - Success metrics and instrumentation plan

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

You have two options for authentication:

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
3. Edit `.env` and set:
   ```
   GOOGLE_CLOUD_PROJECT=your-project-id
   GOOGLE_CLOUD_LOCATION=us-central1
   ```

## Run

### Command Line Interface

Run the agent interactively from the command line:

```bash
# From the prd_studio directory
adk run .

# Or from the parent directory
adk run prd_studio
```

You'll see a prompt where you can enter your product idea:

```
> Here's a 2-sentence product idea. Turn it into a PRD with goals/non-goals, personas, MVP scope, and success metrics.

We want to build a Chrome extension that summarizes long articles using AI. Target users are busy professionals who read a lot of content online.
```

### Web Interface (Development UI)

Launch the interactive web UI:

```bash
# From the parent directory (python/agents/)
cd ..
adk web --port 8000
```

Then open http://localhost:8000 in your browser. You'll see a chat interface where you can interact with PRD Studio.

### Run from Python

You can also import and use the agent programmatically:

```python
from prd_studio import root_agent

response = root_agent.run(
    "Turn this into a PRD: A mobile app that helps people track their daily water intake with smart reminders."
)
print(response)
```

## Demo Data

PRD Studio works entirely with text input - no external systems required. Just provide a product idea or description, and it will generate all documentation.

### Sample Prompts to Try

1. **Simple idea → Full PRD**:
   ```
   Create a PRD for a Slack bot that automatically summarizes long threads. 
   Target users are engineering managers who need to stay updated on discussions 
   but don't have time to read everything.
   ```

2. **Clarification questions**:
   ```
   What are the top 10 questions you need answered before engineering starts 
   on a feature that lets users schedule posts in advance?
   ```

3. **Risk analysis**:
   ```
   Create a risk register for a payment feature that stores credit card information. 
   Focus on security, privacy, and compliance.
   ```

4. **Backlog generation**:
   ```
   Convert this PRD into user stories: [paste PRD content]
   ```

## Optional Integrations

PRD Studio runs entirely locally with no external integrations enabled by default. 

You could extend it to:
- Create JIRA/Linear tickets from the backlog (would require Tool Confirmation)
- Fetch existing PRDs from Google Docs or Confluence
- Generate diagrams using Mermaid or similar tools

These are not implemented to keep the sample simple and runnable without accounts.

## Evals

Currently, PRD Studio includes a built-in Review Agent that validates:
- Completeness (all required sections present)
- Clarity (requirements are unambiguous)
- Consistency (no contradictions)
- Quality (specific, testable requirements)
- Scope creep prevention

To add formal regression tests, you could create an `eval/` directory with test cases.

## Project Structure

```
prd_studio/
├── agent.py              # Main agent definitions
├── __init__.py           # Package initialization
├── requirements.txt      # Python dependencies
├── .env.example          # Example environment configuration
├── README.md             # This file
└── artifacts/            # Generated outputs (created at runtime)
    ├── prd.md
    ├── backlog.csv
    ├── risks.md
    └── metrics.md
```

## Tips

- **Start small**: Begin with a 2-3 sentence product idea and let the agent expand it
- **Be specific**: The more context you provide, the better the output
- **Iterate**: Use the Review Agent's feedback to refine your PRD
- **Save artifacts**: All outputs are saved as artifacts you can download and edit
- **Ask questions**: Use prompts like "What questions do you need answered?" to identify gaps

## Troubleshooting

**"No API key found"**: Make sure you've created a `.env` file with `GOOGLE_API_KEY` set.

**"Agent not found"**: Ensure you're running from the correct directory or using the correct path.

**"Import errors"**: Make sure you've installed dependencies with `pip install -r requirements.txt`.

**Long response times**: PRD generation can take 30-60 seconds as it runs through multiple agents. This is normal.
