# ADK Product Engineering - Agent Samples

**5 production-ready ADK agent projects for Product Managers and Product Engineers**

This repository contains five complete Agent Development Kit (ADK) projects that demonstrate real-world use cases for AI agents in product development. Each agent is fully functional, well-documented, and can be run immediately with just an API key.

## 🤖 The Five Agents

### 1. **PRD Studio** - Product Requirements Document Generator
**`python/agents/prd_studio/`**

Transform fuzzy product ideas into comprehensive, execution-ready documentation.

- **What it does**: Takes a brief product idea and generates a full PRD with goals, personas, MVP scope, success metrics, backlog, and risk analysis
- **Key features**: Sequential agent pipeline with specialized sub-agents, built-in PRD validator
- **Use cases**: Early product planning, requirements documentation, stakeholder alignment
- **Architecture**: `SequentialAgent` with 6 specialized sub-agents

[📖 Read the full README](python/agents/prd_studio/README.md)

**Try it:**
```bash
cd python/agents/prd_studio
adk run .
# Prompt: "Turn this into a PRD: A Chrome extension that summarizes articles using AI for busy professionals"
```

---

### 2. **Experiment Copilot** - A/B Test Design & Analysis
**`python/agents/experiment_copilot/`**

Design experiments with power analysis, then analyze results with statistical rigor.

- **What it does**: Creates experiment plans with sample size calculations, analyzes results from CSV, recommends ship/iterate/stop
- **Key features**: Demonstrates ADK's AgentTool pattern, includes eval suite with 5 test scenarios
- **Use cases**: A/B testing, feature rollouts, growth experiments
- **Architecture**: Root coordinator with specialist agents (Stats Code Agent, Narrative Decision Agent)

[📖 Read the full README](python/agents/experiment_copilot/README.md)

**Try it:**
```bash
cd python/agents/experiment_copilot
adk run .
# Prompt: "Design an A/B test to improve checkout conversion by 5%"
```

---

### 3. **Release Radar** - Dependency Upgrade Analysis
**`python/agents/release_radar/`**

Scan dependencies, assess upgrade risk, and generate migration plans.

- **What it does**: Parses requirements.txt/package.json, identifies upgrade risks, creates migration checklists
- **Key features**: OpenAPIToolset for GitHub integration, Tool Confirmation for safety, Reflect-and-Retry plugin
- **Use cases**: Dependency management, security updates, migration planning
- **Architecture**: Single LLM agent with dependency parsers and optional GitHub API tools

[📖 Read the full README](python/agents/release_radar/README.md)

**Try it:**
```bash
cd python/agents/release_radar
adk run .
# Prompt: "Scan data/sample_requirements.txt and tell me what upgrades are high risk"
```

---

### 4. **VoC Insights** - Customer Feedback Analysis
**`python/agents/voc_insights/`**

Transform customer feedback into prioritized roadmap recommendations.

- **What it does**: Ingests feedback CSV, clusters into themes, quantifies impact, generates backlog items
- **Key features**: MemoryService for trend tracking, deterministic clustering, eval suite
- **Use cases**: Product discovery, roadmap prioritization, user research synthesis
- **Architecture**: Single LLM agent with clustering tools and memory for cross-session analysis

[📖 Read the full README](python/agents/voc_insights/README.md)

**Try it:**
```bash
cd python/agents/voc_insights
adk run .
# Prompt: "Analyze data/sample_feedback.csv and show me the top themes with severity ratings"
```

---

### 5. **Meeting Ops** - Meeting Analysis & Action Tracking
**`python/agents/meeting_ops/`**

Turn meeting transcripts into summaries, decision logs, and action items.

- **What it does**: Parses transcripts, extracts decisions/actions, drafts follow-ups, updates trackers
- **Key features**: Google API toolsets (Docs, Sheets, Gmail), Tool Confirmation, cross-meeting memory
- **Use cases**: Meeting documentation, action tracking, decision logging
- **Architecture**: Single LLM agent with transcript parsing and optional Google Workspace integration

[📖 Read the full README](python/agents/meeting_ops/README.md)

**Try it:**
```bash
cd python/agents/meeting_ops
adk run .
# Prompt: "Load data/sample_transcript.txt and extract decisions, action items, and draft a follow-up email"
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+** (Python 3.12 recommended)
- **pip** package manager
- **Google Gemini API key** (free from [AI Studio](https://aistudio.google.com/))

### Installation

```bash
# Clone the repository
git clone https://github.com/addyosmani/adk-product-engineering.git
cd adk-product-engineering

# Install ADK
pip install google-adk

# Choose an agent and set up
cd python/agents/prd_studio  # or any other agent

# Install dependencies
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

### Run an Agent

**Option 1: Command Line Interface**
```bash
adk run .
```

**Option 2: Web Interface**
```bash
# From the python/agents/ directory
adk web --port 8000
```
Then open http://localhost:8000 in your browser.

**Option 3: Python SDK**
```python
from prd_studio import root_agent

result = root_agent.run("Turn this into a PRD: ...")
print(result)
```

---

## 📁 Repository Structure

```
adk-product-engineering/
├── README.md                          # This file
└── python/
    └── agents/
        ├── prd_studio/                # PRD generation agent
        │   ├── agent.py               # Agent definition
        │   ├── __init__.py
        │   ├── requirements.txt
        │   ├── .env.example
        │   └── README.md
        ├── experiment_copilot/        # A/B test analysis agent
        │   ├── agent.py
        │   ├── data/
        │   │   └── sample_experiment_results.csv
        │   ├── eval/
        │   │   └── test_cases.jsonl
        │   └── README.md
        ├── release_radar/             # Dependency analysis agent
        │   ├── agent.py
        │   ├── data/
        │   │   ├── sample_requirements.txt
        │   │   └── sample_package.json
        │   └── README.md
        ├── voc_insights/              # Feedback analysis agent
        │   ├── agent.py
        │   ├── data/
        │   │   └── sample_feedback.csv
        │   ├── eval/
        │   │   └── test_cases.jsonl
        │   └── README.md
        └── meeting_ops/               # Meeting analysis agent
            ├── agent.py
            ├── data/
            │   └── sample_transcript.txt
            └── README.md
```

---

## 🎯 What Makes These Agents Different?

These aren't just toy examples - they're production-ready agents that demonstrate ADK's real capabilities:

### 1. **Multi-Agent Architectures**
- **PRD Studio**: Sequential pipeline with 6 specialized sub-agents
- **Experiment Copilot**: AgentTool pattern for combining capabilities

### 2. **Tool Integration Patterns**
- **OpenAPIToolset**: Auto-generate tools from API specs (Release Radar)
- **Tool Confirmation**: Safe write operations with user approval
- **Custom Tools**: Domain-specific functions for each agent

### 3. **Memory & State**
- **MemoryService**: Track themes and conventions across sessions (VoC Insights, Meeting Ops)
- **Cross-session queries**: "What changed vs last week?"

### 4. **Artifacts & Outputs**
- All agents save structured outputs (MD, CSV, JSON)
- Downloadable, version-controlled, ready to use

### 5. **Safety & Reliability**
- **Tool Confirmation**: Approve before writing
- **Reflect-and-Retry**: Handle transient failures gracefully
- **Demo Mode**: Work without external accounts

### 6. **Evaluation**
- **Built-in evals**: Test quality, consistency, safety (Experiment Copilot, VoC Insights)
- **Regression testing**: Ensure behavior doesn't degrade

---

## 🏗️ ADK Patterns Demonstrated

Each agent showcases different ADK capabilities:

| Agent | Sequential Agents | AgentTool | OpenAPIToolset | Memory | Confirmations | Plugins | Evals |
|-------|------------------|-----------|----------------|--------|---------------|---------|-------|
| **PRD Studio** | ✅ | | | | | | |
| **Experiment Copilot** | | ✅ | | | | | ✅ |
| **Release Radar** | | | ✅ | | ✅ | ✅ | |
| **VoC Insights** | | | | ✅ | | | ✅ |
| **Meeting Ops** | | | | ✅ | ✅ | | |

---

## 🔑 Authentication Options

All agents support two authentication methods:

### Option A: Gemini API (Simple)
- **Best for**: Development, testing, personal use
- **Setup**: Get free API key from [Google AI Studio](https://aistudio.google.com/)
- **Config**: Add `GOOGLE_API_KEY` to `.env`

### Option B: Vertex AI (Enterprise)
- **Best for**: Production, team use, enterprise features
- **Setup**: Enable Vertex AI in Google Cloud
- **Config**: Set `GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_LOCATION`

---

## 📚 Learning Path

**New to ADK?** Start here:

1. **Run PRD Studio** (simplest agent, clear workflow)
2. **Try Experiment Copilot** (learn AgentTool pattern)
3. **Explore Release Radar** (OpenAPIToolset + plugins)
4. **Test VoC Insights** (memory and evals)
5. **Use Meeting Ops** (Tool Confirmation + Google APIs)

**Each agent's README includes**:
- What the agent does (with example prompts)
- Architecture overview
- Complete setup instructions
- Demo data for offline use
- Tips and troubleshooting

---

## 🛠️ Development Tips

### Running Multiple Agents

Use the web interface to switch between agents:
```bash
cd python/agents
adk web --port 8000
```

### Using Your Own Data

All agents accept custom file paths:
```
> Load my_feedback.csv and analyze themes
> Parse /path/to/requirements.txt and check for upgrades
```

### Enabling Optional Integrations

Most agents work offline by default (demo mode). To enable integrations:

1. **Release Radar**: Add `GITHUB_TOKEN` for actual API calls
2. **Meeting Ops**: Configure Google OAuth for Docs/Sheets/Gmail

See each agent's README for detailed integration instructions.

### Running Evals

For agents with eval suites:
```bash
cd python/agents/experiment_copilot
adk eval eval/test_cases.jsonl
```

---

## 🤝 Contributing

Found a bug? Want to add a new agent? Contributions welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-agent`)
3. Follow the existing agent structure
4. Add comprehensive README
5. Include demo data
6. Submit a pull request

---

## 📖 Additional Resources

- **ADK Documentation**: https://google.github.io/adk-docs/
- **ADK Samples**: https://github.com/google/adk-samples
- **Gemini API**: https://ai.google.dev/
- **Vertex AI**: https://cloud.google.com/vertex-ai

---

## 📄 License

This project is provided as-is for educational and commercial use.

---

## 🙏 Acknowledgments

Built with Google's Agent Development Kit (ADK). Inspired by real product development workflows and the awesome-llm-apps collection.

---

**Ready to get started?** Pick an agent, follow the README, and start building! ��
