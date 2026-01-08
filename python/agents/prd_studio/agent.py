"""PRD Studio - Turn ideas into PRDs, backlogs, risks, and success metrics.

This agent uses a SequentialAgent pipeline to transform fuzzy product ideas
into structured, execution-ready documents.
"""

from google.adk.agents import SequentialAgent, Agent
from pathlib import Path
import json


# Tool for writing artifacts
def save_prd(content: str, filename: str = "prd.md") -> dict:
    """Save PRD content as an artifact.
    
    Args:
        content: The PRD content to save
        filename: Name of the artifact file (default: prd.md)
    
    Returns:
        dict with status and artifact path
    """
    artifacts_dir = Path(__file__).parent / "artifacts"
    artifacts_dir.mkdir(exist_ok=True)
    artifact_path = artifacts_dir / filename
    artifact_path.write_text(content, encoding="utf-8")
    artifact_path = str(artifact_path)
    return {"status": "success", "artifact": artifact_path, "message": f"PRD saved to {artifact_path}"}


def save_backlog(content: str, filename: str = "backlog.csv") -> dict:
    """Save backlog content as an artifact.
    
    Args:
        content: The backlog CSV content to save
        filename: Name of the artifact file (default: backlog.csv)
    
    Returns:
        dict with status and artifact path
    """
    artifacts_dir = Path(__file__).parent / "artifacts"
    artifacts_dir.mkdir(exist_ok=True)
    artifact_path = artifacts_dir / filename
    artifact_path.write_text(content, encoding="utf-8")
    artifact_path = str(artifact_path)
    return {"status": "success", "artifact": artifact_path, "message": f"Backlog saved to {artifact_path}"}


def save_risks(content: str, filename: str = "risks.md") -> dict:
    """Save risk register as an artifact.
    
    Args:
        content: The risk register content to save
        filename: Name of the artifact file (default: risks.md)
    
    Returns:
        dict with status and artifact path
    """
    artifacts_dir = Path(__file__).parent / "artifacts"
    artifacts_dir.mkdir(exist_ok=True)
    artifact_path = artifacts_dir / filename
    artifact_path.write_text(content, encoding="utf-8")
    artifact_path = str(artifact_path)
    return {"status": "success", "artifact": artifact_path, "message": f"Risk register saved to {artifact_path}"}


def save_metrics(content: str, filename: str = "metrics.md") -> dict:
    """Save success metrics as an artifact.
    
    Args:
        content: The metrics content to save
        filename: Name of the artifact file (default: metrics.md)
    
    Returns:
        dict with status and artifact path
    """
    artifacts_dir = Path(__file__).parent / "artifacts"
    artifacts_dir.mkdir(exist_ok=True)
    artifact_path = artifacts_dir / filename
    artifact_path.write_text(content, encoding="utf-8")
    artifact_path = str(artifact_path)
    return {"status": "success", "artifact": artifact_path, "message": f"Metrics saved to {artifact_path}"}


# Define specialized sub-agents
intake_agent = Agent(
    model='gemini-2.0-flash',
    name='intake_agent',
    description='Clarifies product ideas, sets non-goals, and collects constraints',
    instruction="""You are the Intake & Scope Agent. Your job is to:
1. Clarify the product idea by asking targeted questions
2. Define explicit non-goals to bound scope
3. Collect key constraints (technical, business, regulatory)
4. Identify target users and their primary needs
5. Surface assumptions that need validation

Format your output as a structured intake document with sections for:
- Product Idea Summary
- Key Questions & Answers
- In-Scope / Out-of-Scope
- Constraints
- Target Users
- Assumptions to Validate
""",
)

prd_writer_agent = Agent(
    model='gemini-2.0-flash',
    name='prd_writer_agent',
    description='Produces structured PRDs with goals, personas, MVP scope, and success metrics',
    instruction="""You are the PRD Writer Agent. Create a comprehensive Product Requirements Document with:

# [Product Name]

## 1. Executive Summary
Brief overview of the product and its value proposition

## 2. Goals & Objectives
- Primary goals
- Secondary goals
- Explicit non-goals

## 3. User Personas
Detailed personas with needs, pain points, and use cases

## 4. MVP Scope
Clear definition of what's included in the minimum viable product

## 5. Requirements
### Functional Requirements
- User stories with acceptance criteria
### Non-Functional Requirements
- Performance, security, scalability, etc.

## 6. Success Metrics
- North star metric
- Supporting metrics
- Guardrail metrics

## 7. Dependencies & Assumptions
List critical dependencies and assumptions

## 8. Open Questions
Questions that need resolution before or during development

Use clear, unambiguous language. Be specific about requirements.
""",
    tools=[save_prd],
)

backlog_agent = Agent(
    model='gemini-2.0-flash',
    name='backlog_agent',
    description='Converts PRDs into user stories with acceptance criteria and edge cases',
    instruction="""You are the Backlog Agent. Convert PRD requirements into structured backlog items.

Create a CSV with columns:
Epic,Story,Priority,Acceptance Criteria,Edge Cases,Estimated Effort

For each requirement:
1. Group related stories into epics
2. Write clear user stories in format: "As a [user], I want [goal] so that [benefit]"
3. Define specific, testable acceptance criteria
4. Identify edge cases and error scenarios
5. Estimate effort (XS/S/M/L/XL)
6. Prioritize (P0/P1/P2)

Be thorough - include error handling, edge cases, and integration points.
""",
    tools=[save_backlog],
)

risk_agent = Agent(
    model='gemini-2.0-flash',
    name='risk_agent',
    description='Identifies abuse cases, privacy/security concerns, and mitigations',
    instruction="""You are the Risk & Policy Agent. Create a comprehensive risk register.

Analyze the product for:

## Security Risks
- Authentication/authorization vulnerabilities
- Data exposure risks
- API security concerns

## Privacy Risks
- PII handling
- Data retention
- Compliance requirements (GDPR, CCPA, etc.)

## Abuse Cases
- How could bad actors misuse this feature?
- Spam, fraud, manipulation scenarios
- Rate limiting needs

## Operational Risks
- Reliability concerns
- Scalability bottlenecks
- Monitoring gaps

## Business Risks
- Market risks
- Competitive risks
- Resource/timeline risks

For each risk, provide:
- Risk description
- Severity (Critical/High/Medium/Low)
- Likelihood (High/Medium/Low)
- Mitigation strategy
- Owner/accountability

Be paranoid but constructive - identify real risks with practical mitigations.
""",
    tools=[save_risks],
)

review_agent = Agent(
    model='gemini-2.0-flash',
    name='review_agent',
    description='Reviews PRD for contradictions, missing metrics, and unclear scope',
    instruction="""You are the Review Agent. Critically review the PRD and backlog for quality.

Check for:

## Completeness
- All required sections present
- Success metrics clearly defined
- Dependencies documented

## Clarity
- Requirements are unambiguous
- Acceptance criteria are testable
- Technical terms are defined

## Consistency
- No contradictions between sections
- Priorities align with goals
- Scope matches constraints

## Quality
- Requirements are specific, not vague
- Edge cases are considered
- Non-functional requirements are addressed

## Scope Creep
- MVP is truly minimal
- Non-goals are respected
- Features are justified by goals

Provide feedback in this format:
- ✅ Strengths: What's done well
- ⚠️ Issues: Specific problems with line references
- 📝 Recommendations: How to improve
- 🚨 Blockers: Critical issues that must be fixed

Be thorough but fair. The goal is to improve the PRD, not to be overly critical.
""",
)

metrics_agent = Agent(
    model='gemini-2.0-flash',
    name='metrics_agent',
    description='Defines success metrics and instrumentation requirements',
    instruction="""You are the Metrics Agent. Define comprehensive success measurement.

Create a metrics document with:

## North Star Metric
The single most important metric that indicates product success

## Supporting Metrics
Key metrics that drive the north star metric

## Guardrail Metrics
Metrics that shouldn't degrade (e.g., latency, error rate, user satisfaction)

## Instrumentation Plan
For each metric, specify:
- Event name
- Event properties
- Where to instrument
- Sampling rate (if applicable)

## Analysis Plan
- How to analyze the metrics
- Expected baselines
- Success thresholds
- When to measure (e.g., 2 weeks post-launch)

## Dashboard Requirements
What dashboards need to be created and who has access

Be specific about instrumentation - engineers should be able to implement directly from this.
""",
    tools=[save_metrics],
)

# Root agent - Sequential pipeline
root_agent = SequentialAgent(
    name='prd_studio',
    description='Transform product ideas into execution-ready PRDs with backlog, risks, and metrics',
    sub_agents=[intake_agent, prd_writer_agent, backlog_agent, risk_agent, metrics_agent, review_agent],
)
