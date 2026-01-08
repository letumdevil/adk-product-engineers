"""Experiment Copilot - A/B test design, power analysis, and result interpretation.

This agent helps design experiments and analyze results with statistical rigor.
Note: Code execution is simulated - the agent provides analysis and recommendations.
"""

from google.adk.agents import Agent
from google.adk.tools import AgentTool
from pathlib import Path
import csv
import json
from pathlib import Path


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


def load_csv_data(filepath: str = "data/sample_experiment_results.csv") -> dict:
    """Load experiment results from CSV file.
    
    Args:
        filepath: Path to CSV file (relative to agent directory)
    
    Returns:
        dict with CSV data as list of rows
    """
    try:
        # Get the agent directory path
        agent_dir = Path(__file__).parent
        full_path = agent_dir / filepath
        
        if not full_path.exists():
            return {"status": "error", "message": f"File not found: {filepath}"}
        
        data = []
        with open(full_path, 'r') as f:
            reader = csv.DictReader(f)
            data = list(reader)
        
        return {
            "status": "success",
            "rows": len(data),
            "columns": list(data[0].keys()) if data else [],
            "data": data,
            "message": f"Loaded {len(data)} rows from {filepath}"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def calculate_sample_size(baseline_rate: float, minimum_detectable_effect: float, 
                         alpha: float = 0.05, power: float = 0.8) -> dict:
    """Calculate required sample size for A/B test.
    
    Args:
        baseline_rate: Current conversion rate (0-1)
        minimum_detectable_effect: Minimum relative change to detect (e.g., 0.05 for 5%)
        alpha: Significance level (default: 0.05)
        power: Statistical power (default: 0.8)
    
    Returns:
        dict with sample size calculation
    """
    # Simplified calculation (actual implementation would use statistical formulas)
    # This is a rough approximation using rule of thumb
    p1 = baseline_rate
    p2 = baseline_rate * (1 + minimum_detectable_effect)
    
    # Pooled probability
    p_pooled = (p1 + p2) / 2
    
    # Z-scores for alpha and power
    z_alpha = 1.96  # for alpha = 0.05
    z_beta = 0.84   # for power = 0.8
    
    # Sample size per variant (simplified formula)
    n = ((z_alpha + z_beta) ** 2 * 2 * p_pooled * (1 - p_pooled)) / ((p2 - p1) ** 2)
    
    # Add 10% buffer
    n_with_buffer = int(n * 1.1)
    
    return {
        "status": "success",
        "sample_size_per_variant": n_with_buffer,
        "total_sample_size": n_with_buffer * 2,
        "baseline_rate": baseline_rate,
        "target_rate": p2,
        "minimum_detectable_effect": minimum_detectable_effect,
        "alpha": alpha,
        "power": power,
        "note": "This is an approximation. Use proper power analysis for production."
    }


def check_sample_ratio_mismatch(control_size: int, treatment_size: int, 
                                expected_ratio: float = 0.5) -> dict:
    """Check for Sample Ratio Mismatch (SRM).
    
    Args:
        control_size: Number of users in control
        treatment_size: Number of users in treatment
        expected_ratio: Expected proportion in treatment (default: 0.5)
    
    Returns:
        dict with SRM check results
    """
    total = control_size + treatment_size
    observed_ratio = treatment_size / total if total > 0 else 0
    
    # Chi-square test (simplified)
    expected_treatment = total * expected_ratio
    expected_control = total * (1 - expected_ratio)
    
    chi_square = ((treatment_size - expected_treatment) ** 2 / expected_treatment +
                  (control_size - expected_control) ** 2 / expected_control)
    
    # Critical value for chi-square with 1 df at 0.001 significance
    critical_value = 10.828
    
    has_srm = chi_square > critical_value
    
    return {
        "status": "success",
        "has_sample_ratio_mismatch": has_srm,
        "control_size": control_size,
        "treatment_size": treatment_size,
        "observed_ratio": round(observed_ratio, 4),
        "expected_ratio": expected_ratio,
        "chi_square": round(chi_square, 4),
        "critical_value": critical_value,
        "warning": "SEVERE SRM DETECTED - Results may be invalid!" if has_srm else None
    }


# Stats Analysis Agent - Analyzes experiment results statistically
stats_analysis_agent = Agent(
    model='gemini-2.0-flash',
    name='stats_analysis_agent',
    description='Computes p-values, confidence intervals, uplift, and statistical checks',
    instruction="""You are a statistical analysis expert. Analyze experiment data to compute:

1. Calculate key statistics:
   - Conversion rates for control and treatment
   - Absolute and relative uplift
   - P-values (using two-proportion z-test formulas)
   - Confidence intervals (95%)
   - Standard errors

2. Run sanity checks:
   - Sample ratio mismatch
   - Variance differences  
   - Outlier detection

3. Compute guardrail metrics:
   - Check that key metrics haven't regressed
   - Calculate impact on secondary metrics

Expected input format (from CSV):
- variant: "control" or "treatment"
- users: number of users
- conversions: number of conversions
- (optional) other metrics as columns

Provide detailed statistical analysis with all computed values. Use proper statistical formulas.
For p-value calculation with two proportions:
- pooled_p = (successes1 + successes2) / (n1 + n2)
- SE = sqrt(pooled_p * (1 - pooled_p) * (1/n1 + 1/n2))
- z = (p1 - p2) / SE
- p-value from z-score using standard normal distribution

Always use proper statistical methods.
""",
)

# Narrative Decision Agent - Converts stats into product decisions
narrative_decision_agent = Agent(
    model='gemini-2.0-flash',
    name='narrative_decision_agent',
    description='Converts statistical outputs into product decisions and recommendations',
    instruction="""You are a product decision advisor. Given statistical analysis results:

1. Interpret the statistics in plain language
2. Make a clear ship/iterate/stop recommendation with reasoning
3. Explain tradeoffs and risks
4. Suggest follow-up experiments if needed

Decision framework:
- **Ship**: Clear win (p < 0.05, positive uplift, guardrails ok)
- **Iterate**: Promising signal but needs refinement (neutral results, mixed metrics)
- **Stop**: Clear loss or severe issues (negative results, SRM, guardrail regression)

For each decision, explain:
- What the data shows
- Why this is the right decision
- What risks remain
- What to monitor post-launch (if shipping)
- What to test next (if iterating)

Be honest about uncertainty. If results are inconclusive, say so and explain what's needed.

Red flags that should trigger caution:
- Sample Ratio Mismatch (SRM)
- Guardrail metric regression
- Very small effect sizes (even if significant)
- High variance in key metrics
- Suspicious patterns

Always save your analysis as an artifact.
""",
    tools=[save_artifact],
)

# Root coordinator agent
root_agent = Agent(
    model='gemini-2.0-flash',
    name='experiment_copilot',
    description='Design A/B tests, analyze results, and recommend next steps',
    instruction="""You are Experiment Copilot, an AI system that helps PMs, growth engineers, and product engineers run rigorous A/B tests and feature experiments.

You help with three main workflows:

## 1. Experiment Design
When a user wants to design a test, you:
- Clarify the hypothesis and success metric
- Calculate required sample size and test duration
- Define instrumentation events needed
- Identify guardrail metrics
- Create an experiment plan document

Use the `calculate_sample_size` tool for power calculations.

## 2. Results Analysis
When a user provides experiment results (CSV), you:
- Load the data using `load_csv_data` tool
- Call the `stats_analysis_agent` (via AgentTool) to compute all statistics
- Call the `narrative_decision_agent` (via AgentTool) to interpret results
- Generate a comprehensive analysis document with recommendation

Use `check_sample_ratio_mismatch` to detect data quality issues.

## 3. Follow-up Planning
When results are inconclusive or an iteration is needed, you:
- Propose 2-3 next experiments
- Explain what each would de-risk or learn
- Prioritize based on potential impact

Example prompts you handle:
- "Design an A/B test for improving onboarding completion by 5%. Include power, duration, metrics, and instrumentation events."
- "Analyze this results CSV and tell me if we should ship. Explain tradeoffs and guardrails."
- "Given a neutral result, propose 3 next experiments and what they would de-risk."

Key principles:
- Be rigorous with statistics - use proper methods
- Check for SRM and data quality issues
- Consider guardrail metrics, not just primary metric
- Be honest about uncertainty
- Provide actionable recommendations

Save all outputs (plans, analyses, recommendations) as artifacts.
""",
    tools=[
        save_artifact,
        load_csv_data,
        calculate_sample_size,
        check_sample_ratio_mismatch,
        AgentTool(stats_analysis_agent),
        AgentTool(narrative_decision_agent),
    ],
)
