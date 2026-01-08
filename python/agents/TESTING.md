# ADK Agent Projects - Testing Guide

This document explains how to test each of the 5 agents.

## Prerequisites

1. Install ADK:
```bash
pip install google-adk
```

2. Set up API key in each agent's directory:
```bash
cd python/agents/[agent_name]
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

## Testing Each Agent

### 1. PRD Studio

```bash
cd python/agents/prd_studio
export GOOGLE_API_KEY="your_key_here"
adk run .
```

**Test prompt:**
```
Turn this into a PRD: A Chrome extension that uses AI to summarize long articles for busy professionals who need to read lots of content quickly.
```

**Expected output:**
- Comprehensive PRD with goals, personas, MVP scope
- Backlog CSV with user stories
- Risk register
- Success metrics document
- All saved as artifacts in `artifacts/` directory

---

### 2. Experiment Copilot

```bash
cd python/agents/experiment_copilot
export GOOGLE_API_KEY="your_key_here"
adk run .
```

**Test prompt:**
```
Design an A/B test to improve our checkout conversion rate from 12% to 14%. We have 100,000 monthly users. Include sample size calculation and timeline.
```

**Expected output:**
- Experiment plan with power analysis
- Sample size calculation
- Timeline estimate
- Instrumentation recommendations

---

### 3. Release Radar

```bash
cd python/agents/release_radar
export GOOGLE_API_KEY="your_key_here"
adk run .
```

**Test prompt:**
```
Parse data/sample_requirements.txt and identify which dependencies need upgrades. Assess the risk level for each upgrade.
```

**Expected output:**
- List of dependencies with current versions
- Risk assessment (high/medium/low) for each
- Upgrade recommendations
- Migration checklist saved as artifact

---

### 4. VoC Insights

```bash
cd python/agents/voc_insights
export GOOGLE_API_KEY="your_key_here"
adk run .
```

**Test prompt:**
```
Analyze data/sample_feedback.csv and show me the top 5 themes with severity ratings and recommended actions.
```

**Expected output:**
- Top themes identified (Performance, UI/UX, Bugs, etc.)
- Severity ratings
- Example quotes for each theme
- Prioritized recommendations
- Artifacts: voc_summary.md, themes.json, recommendations.csv

---

### 5. Meeting Ops

```bash
cd python/agents/meeting_ops
export GOOGLE_API_KEY="your_key_here"
adk run .
```

**Test prompt:**
```
Load data/sample_transcript.txt and extract: 1) All decisions made, 2) Action items with owners and due dates, 3) Draft a follow-up email summarizing the meeting.
```

**Expected output:**
- Meeting summary with decisions
- Action items CSV with owners and dates
- Draft follow-up email
- All saved as artifacts

---

## Using the Web UI

To test all agents in the web interface:

```bash
cd python/agents
export GOOGLE_API_KEY="your_key_here"
adk web --port 8000
```

Then open http://localhost:8000 and select an agent from the list.

---

## Troubleshooting

**"No API key found"**: Make sure you've set `GOOGLE_API_KEY` environment variable or created a `.env` file.

**"Agent not found"**: Make sure you're running from the correct directory (the agent's directory or with the correct path).

**"Import errors"**: Install dependencies with `pip install -r requirements.txt`.

**Agents work but artifacts not created**: Check that the `artifacts/` directory is created. It should be auto-created by the agents.

---

## Validation Checklist

For each agent, verify:
- [ ] Agent loads without errors
- [ ] Can process a simple prompt
- [ ] Generates expected artifacts
- [ ] Artifacts are saved in `artifacts/` directory
- [ ] Output is coherent and useful
- [ ] Tools are called correctly (check logs)

---

## Notes

- All agents work in "demo mode" without external integrations
- Artifacts are saved locally using the file system
- Memory features are commented out but can be enabled with proper session service configuration
- Tool confirmations are not currently active but would prompt user approval in production
