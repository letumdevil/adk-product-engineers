# Voice of Customer Insights

**Transform customer feedback into actionable product insights and roadmap priorities**

## What This Agent Does

Voice of Customer (VoC) Insights helps Product Managers analyze customer feedback at scale. It ingests feedback from multiple channels, clusters it into themes, quantifies impact, and generates prioritized roadmap recommendations with supporting data.

The agent demonstrates:
- **MemoryService** for tracking themes across sessions (trend detection)
- **Deterministic clustering** for reproducible results
- **Data quality checks** (deduplication, validation)
- **Eval suite** for ensuring consistency

### Example Prompts

1. **"Ingest this feedback CSV and give me the top themes, with severity and suggested fixes."**
   - Input: Path to feedback CSV
   - Output: Executive summary with ranked themes and recommendations

2. **"What changed vs last week? Which themes are trending up/down?"**
   - Input: New feedback data
   - Output: Trend analysis comparing to previous run (uses memory)

3. **"Turn the top 3 themes into backlog items with acceptance criteria."**
   - Input: Theme analysis results
   - Output: Structured backlog items ready for sprint planning

## Architecture Overview

### Agents
- **Root Agent**: Single LLM agent that orchestrates the feedback analysis workflow

### Tools
- **CSV Loader**: Load feedback from CSV files
- **Cleaner/Deduper**: Remove duplicates and invalid entries
- **Theme Clusterer**: Group feedback into themes using keyword-based approach
- **Artifact Writer**: Save summaries, themes, and recommendations

### Memory
- **MemoryService**: Stores previous run's themes to enable trend detection
- In-memory by default (resets on restart)
- Can be configured with persistent backend for production use

### Artifacts
All outputs saved to `artifacts/`:
- `voc_summary.md` - Executive summary with key insights
- `themes.json` - Structured theme data with examples
- `recommendations.csv` - Prioritized backlog items

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

## Run

### Command Line Interface

```bash
# From the voc_insights directory
adk run .

# Or from the parent directory
adk run voc_insights
```

Example session:
```
> Load data/sample_feedback.csv and analyze the top themes. 
  Give me severity ratings and actionable recommendations.
```

### Web Interface (Development UI)

```bash
# From the parent directory (python/agents/)
cd ..
adk web --port 8000
```

Open http://localhost:8000 and select "voc_insights" from the agent list.

## Demo Data

The agent includes sample feedback in `data/sample_feedback.csv` with 20 entries covering common themes:

```csv
timestamp,channel,user_segment,text,severity
2024-01-15T10:30:00Z,email,enterprise,"The app is very slow...",high
2024-01-15T11:45:00Z,chat,free,"Love the new search feature!",low
...
```

### CSV Format

Expected columns:
- **timestamp**: ISO 8601 date/time (e.g., `2024-01-15T10:30:00Z`)
- **channel**: Source of feedback (email, chat, review, survey, etc.)
- **user_segment**: User type (free, paid, enterprise, etc.)
- **text**: The actual feedback content
- **severity** (optional): User-reported severity (low/medium/high)

### Try These Prompts

1. **Basic analysis**:
   ```
   Analyze data/sample_feedback.csv and show me the top 5 themes 
   with examples and severity ratings.
   ```

2. **Segment-specific insights**:
   ```
   What are enterprise customers complaining about most? 
   Focus on high-severity feedback.
   ```

3. **Backlog creation**:
   ```
   Take the top 3 themes and create user stories with acceptance criteria 
   and priority recommendations.
   ```

4. **Trend detection** (requires multiple runs):
   ```
   # First run
   Analyze data/sample_feedback.csv and save themes to memory.
   
   # Second run (with new data)
   Analyze data/new_feedback.csv and compare to last week. 
   What themes are trending up?
   ```

## Optional Integrations

VoC Insights runs entirely with local CSV files - no external integrations required.

You could extend it to:
- **Pull feedback automatically** from Zendesk, Intercom, Salesforce, App Store reviews
- **Real-time monitoring** with alerts when new themes emerge
- **Sentiment analysis** using ML models for more accurate severity
- **Advanced clustering** with embeddings (OpenAI, Vertex AI) instead of keywords
- **Dashboard visualization** with charts and graphs

These are not implemented to keep the sample simple and runnable.

## Evals

The `eval/` directory includes test cases to ensure quality and consistency.

### What the Eval Tests

1. **Theme stability**: Top theme labels don't randomly change between runs
2. **No quote fabrication**: Agent only uses actual quotes from feedback
3. **Recommendation quality**: Backlog items match extracted themes
4. **Trajectory consistency**: Agent follows the correct workflow (load → clean → cluster → synthesize)

### Run Evals

```bash
# From the voc_insights directory
adk eval eval/test_cases.jsonl
```

### Expected Results

All test cases should pass, with the agent:
- Identifying consistent themes (Performance, UI/UX, Bugs, etc.)
- Including real examples from the data
- Generating actionable recommendations
- Following the structured workflow

## Project Structure

```
voc_insights/
├── agent.py                  # Main agent definition
├── __init__.py               # Package initialization
├── requirements.txt          # Python dependencies
├── .env.example              # Example environment config
├── README.md                 # This file
├── data/
│   └── sample_feedback.csv   # Demo feedback data
├── eval/
│   └── test_cases.jsonl     # Evaluation test cases
└── artifacts/                # Generated outputs (runtime)
    ├── voc_summary.md
    ├── themes.json
    └── recommendations.csv
```

## Understanding Memory

VoC Insights uses ADK's `MemoryService` to track themes over time:

### How Memory Works

1. **First Run**: Agent analyzes feedback, identifies themes, saves to memory
2. **Subsequent Runs**: Agent can compare new themes to previous themes
3. **Trend Detection**: "Performance complaints increased 30% vs last week"

### Memory Modes

**In-Memory (Default)**:
- Stores data in RAM
- Lost when agent restarts
- Good for: Single session analysis, testing

**Persistent Backend (Optional)**:
- Stores data in database or file
- Survives agent restarts
- Good for: Weekly reports, long-term tracking

To enable persistent memory, configure in agent initialization:
```python
memory = MemoryService(backend="file", path="./memory.json")
```

## Tips

- **Clean your data**: Remove test feedback, internal notes, etc. before analysis
- **Use consistent segments**: Keep user_segment values standardized (free/paid/enterprise)
- **Include severity**: When available, severity ratings improve prioritization
- **Regular analysis**: Run weekly/monthly for trend detection
- **Combine with metrics**: Feedback + usage data = better decisions

## Troubleshooting

**"No API key found"**: Create a `.env` file with `GOOGLE_API_KEY`.

**"File not found" for CSV**: Ensure the path is correct (relative to agent directory or absolute).

**Memory not persisting**: Default in-memory mode resets on restart. Configure persistent backend if needed.

**Themes seem random**: Keyword-based clustering is simplified. For production, use embeddings + k-means.

**No trend detection**: Trends require multiple runs. Memory is empty on first run.

## Advanced: Improving Clustering

The demo uses keyword-based clustering (simple, deterministic, no ML dependencies). For production, consider:

### Option 1: Embeddings + K-Means
```python
from openai import OpenAI
from sklearn.cluster import KMeans

# Generate embeddings for each feedback
embeddings = [get_embedding(f['text']) for f in feedback]

# Cluster with k-means
kmeans = KMeans(n_clusters=5)
labels = kmeans.fit_predict(embeddings)
```

### Option 2: Topic Modeling (LDA)
```python
from sklearn.decomposition import LatentDirichletAllocation

# Extract topics from feedback
lda = LatentDirichletAllocation(n_components=10)
topics = lda.fit_transform(vectorized_feedback)
```

### Option 3: Let the LLM Cluster
```python
# Pass all feedback to LLM and ask it to identify themes
# Pro: Understands context, nuance
# Con: Non-deterministic, expensive
```

The current implementation balances simplicity, speed, and reproducibility.
