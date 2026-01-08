# Experiment Copilot

**Design A/B tests, analyze results with statistical rigor, and get ship/iterate/stop recommendations**

## What This Agent Does

Experiment Copilot helps Product Managers, growth engineers, and data-minded product engineers run rigorous A/B tests and feature experiments. It handles the full lifecycle from experiment design through statistical analysis to actionable recommendations.

The agent showcases ADK's "one tool per agent" limitation pattern: when you need code execution plus other capabilities, you wrap specialized agents using `AgentTool`.

### Example Prompts

1. **"Design an A/B test for improving onboarding completion by 5%. Include power, duration, metrics, and instrumentation events."**
   - Output: Comprehensive experiment plan with sample size, duration, and instrumentation

2. **"Analyze this results CSV and tell me if we should ship. Explain tradeoffs and guardrails."**
   - Input: Path to CSV with experiment results
   - Output: Statistical analysis with ship/iterate/stop recommendation

3. **"Given a neutral result, propose 3 next experiments and what they would de-risk."**
   - Input: Description of current experiment results
   - Output: Prioritized list of follow-up experiments

## Architecture Overview

This agent demonstrates a key ADK pattern for working around tool limitations:

### Agents
- **Root Coordinator Agent**: Orchestrates the experiment workflow
- **Stats Code Agent**: Uses `CodeExecution` tool (only capability) to compute p-values, confidence intervals, uplift, and statistical checks
- **Narrative Decision Agent**: Converts statistical outputs into product decisions and follow-up recommendations

The root agent calls specialized agents via `AgentTool`, allowing it to combine multiple capabilities.

### Tools
- **CSV Loader**: Loads experiment results from local filesystem
- **Sample Size Calculator**: Deterministic power analysis for experiment design
- **SRM Checker**: Detects Sample Ratio Mismatch (data quality issue)
- **Artifact Writer**: Saves experiment plans and analyses

### Memory
None (stateless - each analysis is independent)

### Artifacts
All outputs saved to `artifacts/`:
- `experiment_plan.md` - Test design with power analysis
- `instrumentation_events.json` - Event schema for logging
- `analysis.md` - Statistical analysis with decision
- `recommendations.md` - Follow-up experiments

## Setup

### 1. Install Python Dependencies

```bash
# Create and activate virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

This installs:
- `google-adk` - Agent Development Kit
- `scipy` - For statistical calculations

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

## Run

### Command Line Interface

```bash
# From the experiment_copilot directory
adk run .

# Or from the parent directory
adk run experiment_copilot
```

Example session:
```
> Design an A/B test for improving checkout conversion from 12% to 14%. 
  Include sample size, duration, and key metrics to track.
```

### Web Interface (Development UI)

```bash
# From the parent directory (python/agents/)
cd ..
adk web --port 8000
```

Open http://localhost:8000 and select "experiment_copilot" from the agent list.

## Demo Data

The agent includes sample experiment results in `data/sample_experiment_results.csv`:

```csv
variant,users,conversions,revenue,avg_session_time
control,10000,1200,24000,180
treatment,10050,1350,28500,185
```

### Try These Prompts

1. **Analyze the sample data**:
   ```
   Load and analyze data/sample_experiment_results.csv. 
   Should we ship the treatment? Explain your reasoning.
   ```

2. **Design a new test**:
   ```
   Design an A/B test to improve email open rate from 22% to 25%. 
   We have 50,000 weekly active users. Include sample size and timeline.
   ```

3. **Check for data quality issues**:
   ```
   Check for sample ratio mismatch in the results: 
   control has 10,000 users, treatment has 12,000 users (expected 50/50 split).
   ```

4. **Plan follow-ups**:
   ```
   The test showed a small positive lift (0.5%) but wasn't statistically significant. 
   What are 3 next experiments we should run?
   ```

## Optional Integrations

Experiment Copilot runs entirely with local CSV files - no external integrations required.

You could extend it to:
- Pull experiment data from your analytics platform (Amplitude, Mixpanel, etc.)
- Push results to your data warehouse
- Create dashboards automatically
- Alert on experiment completion

These are not implemented to keep the sample simple and runnable.

## Evals

The `eval/` directory includes a test suite with 5 golden scenarios:

### Test Cases (`eval/test_cases.jsonl`)

1. **Clear Win**: Significant positive uplift, p < 0.05, guardrails OK → Should recommend "Ship"
2. **Clear Loss**: Significant negative uplift → Should recommend "Stop"
3. **Inconclusive**: p > 0.05, small effect → Should recommend "Iterate" or more data
4. **SRM Detected**: Sample ratio mismatch → Should flag data quality issue
5. **Guardrail Regression**: Primary metric up, but secondary metric (e.g., latency) degraded → Should recommend caution

### Run Evals

```bash
# From the experiment_copilot directory
adk eval eval/test_cases.jsonl
```

The eval checks:
- Response quality (does it make the right recommendation?)
- Tool use trajectory (does it actually run statistical analysis?)
- Safety under pressure (doesn't cave to PM pushing to ship despite issues)

### Expected Results

All test cases should pass, with the agent:
- Using the stats_code_agent to compute proper statistics
- Detecting SRM when present
- Recommending appropriately based on data
- Explaining reasoning clearly

## Project Structure

```
experiment_copilot/
├── agent.py                           # Main agent definitions
├── __init__.py                        # Package initialization
├── requirements.txt                   # Python dependencies
├── .env.example                       # Example environment config
├── README.md                          # This file
├── data/
│   └── sample_experiment_results.csv  # Demo data
├── eval/
│   └── test_cases.jsonl              # Evaluation test cases
└── artifacts/                         # Generated outputs (runtime)
    ├── experiment_plan.md
    ├── instrumentation_events.json
    ├── analysis.md
    └── recommendations.md
```

## Tips

- **Always check for SRM**: Sample Ratio Mismatch indicates data quality issues
- **Look at guardrails**: A primary metric win doesn't matter if you broke something else
- **Be skeptical of small effects**: Even if statistically significant, a 0.1% lift may not be worth shipping
- **Consider practical significance**: Statistical significance ≠ business significance
- **Run pre-experiment sanity checks**: Validate your instrumentation before starting

## Troubleshooting

**"No API key found"**: Create a `.env` file with `GOOGLE_API_KEY`.

**"File not found" for CSV**: Ensure the CSV path is relative to the agent directory, or use an absolute path.

**"scipy not found"**: Run `pip install -r requirements.txt` to install dependencies.

**Code execution fails**: The Stats Code Agent uses Python code execution. Ensure your ADK version supports this (1.21.0+).

## Advanced: Understanding the AgentTool Pattern

This agent demonstrates why `AgentTool` is needed:

**The Problem**: ADK's `CodeExecution` tool can only be used by one agent. If you want code execution *plus* other tools (like artifact writing), you need multiple agents.

**The Solution**: 
1. Create a specialized agent with *only* code execution (Stats Code Agent)
2. Create another specialized agent for narrative/artifacts (Narrative Decision Agent)  
3. Use a root coordinator that calls both via `AgentTool`

This pattern lets you compose capabilities while respecting ADK's tool constraints.
