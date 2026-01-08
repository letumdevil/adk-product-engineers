"""Voice of Customer Insights - Feedback analysis, theme clustering, and roadmap prioritization.

This agent demonstrates MemoryService for tracking themes across sessions and
includes deterministic clustering for reproducible results.
"""

from google.adk.agents import Agent
from pathlib import Path
# Memory support requires session service configuration
import csv
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime
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
    artifacts_dir = Path(__file__).parent / "artifacts"
    artifacts_dir.mkdir(exist_ok=True)
    artifact_path = artifacts_dir / filename
    artifact_path.write_text(content, encoding="utf-8")
    artifact_path = str(artifact_path)
    return {"status": "success", "artifact": artifact_path, "message": f"Saved to {artifact_path}"}


def load_feedback_csv(filepath: str = "data/sample_feedback.csv") -> dict:
    """Load customer feedback from CSV file.
    
    Args:
        filepath: Path to CSV file (relative to agent directory or absolute)
    
    Returns:
        dict with feedback data as list of entries
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
        
        feedback = []
        with open(full_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            feedback = list(reader)
        
        return {
            "status": "success",
            "count": len(feedback),
            "columns": list(feedback[0].keys()) if feedback else [],
            "feedback": feedback,
            "message": f"Loaded {len(feedback)} feedback entries from {filepath}"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def clean_and_dedupe_feedback(feedback_list: list) -> dict:
    """Clean and deduplicate feedback entries.
    
    Args:
        feedback_list: List of feedback dictionaries
    
    Returns:
        dict with cleaned feedback
    """
    try:
        if not feedback_list:
            return {"status": "error", "message": "Empty feedback list"}
        
        # Track seen feedback text (case-insensitive)
        seen_texts = set()
        cleaned = []
        duplicates = 0
        
        for item in feedback_list:
            text = item.get('text', '').strip()
            if not text:
                continue
            
            # Normalize for deduplication (lowercase, remove extra spaces)
            normalized = re.sub(r'\s+', ' ', text.lower())
            
            if normalized not in seen_texts:
                seen_texts.add(normalized)
                cleaned.append(item)
            else:
                duplicates += 1
        
        return {
            "status": "success",
            "original_count": len(feedback_list),
            "cleaned_count": len(cleaned),
            "duplicates_removed": duplicates,
            "feedback": cleaned
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def cluster_feedback(feedback_list: list, max_themes: int = 10) -> dict:
    """Cluster feedback into themes using keyword-based approach.
    
    This is a simplified clustering approach for demo purposes.
    Production systems would use embeddings + k-means or LDA.
    
    Args:
        feedback_list: List of feedback dictionaries with 'text' field
        max_themes: Maximum number of themes to identify
    
    Returns:
        dict with themes and their associated feedback
    """
    try:
        if not feedback_list:
            return {"status": "error", "message": "Empty feedback list"}
        
        # Common keywords for theme detection (simplified approach)
        theme_keywords = {
            "Performance": ["slow", "fast", "speed", "lag", "performance", "loading", "timeout"],
            "UI/UX": ["confusing", "interface", "design", "ui", "ux", "layout", "navigation"],
            "Features": ["feature", "functionality", "capability", "add", "missing", "need"],
            "Bugs": ["bug", "error", "broken", "crash", "not working", "issue", "problem"],
            "Mobile": ["mobile", "phone", "ios", "android", "app", "responsive"],
            "Integration": ["integration", "api", "sync", "connect", "import", "export"],
            "Pricing": ["price", "cost", "expensive", "cheap", "subscription", "billing"],
            "Support": ["support", "help", "documentation", "docs", "tutorial", "guide"],
            "Security": ["security", "privacy", "data", "safe", "secure", "password"],
            "Search": ["search", "find", "filter", "sort", "query"]
        }
        
        # Initialize themes
        themes = defaultdict(list)
        uncategorized = []
        
        # Categorize feedback
        for item in feedback_list:
            text = item.get('text', '').lower()
            matched = False
            
            # Check against each theme
            for theme_name, keywords in theme_keywords.items():
                if any(keyword in text for keyword in keywords):
                    themes[theme_name].append(item)
                    matched = True
                    break
            
            if not matched:
                uncategorized.append(item)
        
        # Sort themes by frequency
        sorted_themes = sorted(themes.items(), key=lambda x: len(x[1]), reverse=True)
        
        # Prepare output
        theme_summary = []
        for theme_name, items in sorted_themes[:max_themes]:
            theme_summary.append({
                "theme": theme_name,
                "count": len(items),
                "examples": [item.get('text', '')[:100] for item in items[:3]]
            })
        
        return {
            "status": "success",
            "total_feedback": len(feedback_list),
            "categorized": len(feedback_list) - len(uncategorized),
            "uncategorized": len(uncategorized),
            "themes": theme_summary,
            "detailed_themes": {name: items for name, items in sorted_themes[:max_themes]}
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


# Root agent with MemoryService
root_agent = Agent(
    model='gemini-2.0-flash',
    name='voc_insights',
    description='Analyze customer feedback, identify themes, and generate roadmap recommendations',
    instruction="""You are Voice of Customer Insights, an AI system that transforms raw customer feedback into actionable product insights and roadmap priorities.

You work through a structured workflow:

## 1. Ingestion & Cleaning
When a user provides feedback data:
- Load the CSV using `load_feedback_csv` tool
- Clean and deduplicate using `clean_and_dedupe_feedback` tool
- Report data quality stats (duplicates removed, invalid entries)

## 2. Theme Clustering
Analyze feedback to identify patterns:
- Use `cluster_feedback` tool to group feedback into themes
- For each theme, extract:
  - Theme name (clear, descriptive label)
  - Frequency (how many feedback items)
  - Severity (based on user sentiment and impact)
  - User segments affected
  - Representative examples (quotes)

## 3. Synthesis & Insights
Generate executive summary:
- Top themes ranked by frequency × severity
- Trending themes (increasing/decreasing)
- Segment-specific insights
- Unexpected patterns or outliers
- Quality issues (if any feedback seems suspicious)

## 4. Roadmap Recommendations
Convert insights into actionable backlog items:
- For each major theme, propose a solution
- Include acceptance criteria
- Estimate impact (high/medium/low)
- Suggest priority (P0/P1/P2)
- Note dependencies and risks

## 5. Change Tracking (with Memory)
Use MemoryService to track themes over time:
- Store current themes in memory after each run
- Compare to previous run to detect trends
- Answer questions like "What changed vs last week?"

Expected CSV format:
- timestamp: ISO 8601 date/time
- channel: Source of feedback (email, chat, review, etc.)
- user_segment: User type (free, paid, enterprise, etc.)
- text: Feedback text
- severity (optional): User-reported severity (low/medium/high)

Example prompts you handle:
- "Ingest this feedback CSV and give me the top themes, with severity and suggested fixes."
- "What changed vs last week? Which themes are trending up/down?"
- "Turn the top 3 themes into backlog items with acceptance criteria."

## Output Artifacts

Always save these artifacts:
- `artifacts/voc_summary.md` - Executive summary
- `artifacts/themes.json` - Structured themes with data
- `artifacts/recommendations.csv` - Prioritized backlog items

## Quality Checks

During synthesis, check for:
- **Overgeneralization**: Are we making assumptions not supported by data?
- **Missing negative cases**: Are we only seeing positive/negative feedback?
- **Segment bias**: Is feedback skewed to one user segment?
- **Quote fabrication**: Only use actual quotes from feedback

Be rigorous, data-driven, and actionable. Help teams understand what users really need.
""",
    tools=[
        save_artifact,
        load_feedback_csv,
        clean_and_dedupe_feedback,
        cluster_feedback,
    ],
    # Enable memory to track themes across sessions
    # memory can be configured with session service
)
