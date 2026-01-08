"""Meeting Ops - Meeting transcript analysis with action tracking.

This agent demonstrates Google API toolsets (Calendar, Gmail, Docs, Sheets)
with Tool Confirmation for write operations and MemoryService for conventions.
"""

from google.adk.agents import Agent
from pathlib import Path
# Memory support requires session service configuration
import json
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


def parse_meeting_transcript(transcript: str) -> dict:
    """Parse meeting transcript to extract basic structure.
    
    Args:
        transcript: Raw meeting transcript text
    
    Returns:
        dict with parsed sections and speaker turns
    """
    try:
        # Split into speaker turns (looks for "Name:" or "[Name]" patterns)
        speaker_pattern = r'^([A-Z][a-zA-Z\s]+):\s*(.+)$'
        
        turns = []
        current_speaker = None
        current_text = []
        
        for line in transcript.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            match = re.match(speaker_pattern, line)
            if match:
                # Save previous speaker's turn
                if current_speaker and current_text:
                    turns.append({
                        "speaker": current_speaker,
                        "text": ' '.join(current_text)
                    })
                
                # Start new turn
                current_speaker = match.group(1)
                current_text = [match.group(2)]
            else:
                # Continue current turn
                if current_speaker:
                    current_text.append(line)
        
        # Save last turn
        if current_speaker and current_text:
            turns.append({
                "speaker": current_speaker,
                "text": ' '.join(current_text)
            })
        
        return {
            "status": "success",
            "turns": len(turns),
            "speakers": list(set(t["speaker"] for t in turns)),
            "parsed_turns": turns
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def extract_action_items(transcript_analysis: dict) -> dict:
    """Extract action items from analyzed transcript.
    
    Args:
        transcript_analysis: Analysis results from LLM
    
    Returns:
        dict with action items in structured format
    """
    # This is a helper that would work with LLM output
    # In practice, the LLM does the extraction, this just formats
    return {
        "status": "success",
        "message": "Use the LLM to extract action items with owner, due date, and description"
    }


def extract_decisions(transcript_analysis: dict) -> dict:
    """Extract decisions from analyzed transcript.
    
    Args:
        transcript_analysis: Analysis results from LLM
    
    Returns:
        dict with decisions in structured format
    """
    # This is a helper that would work with LLM output
    return {
        "status": "success",
        "message": "Use the LLM to extract decisions with context and date"
    }


def create_meeting_doc(title: str, content: str) -> dict:
    """Create a Google Doc with meeting summary .
    
    This tool would integrate with Google Docs API when credentials are configured.
    By default, it saves a local artifact.
    
    Args:
        title: Document title
        content: Document content (markdown)
    
    Returns:
        dict with doc creation status
    """
    # In demo mode, save as artifact
    save_artifact(content, f"meeting_doc_{datetime.now().strftime('%Y%m%d')}.md")
    
    return {
        "status": "demo_mode",
        "message": "In demo mode - saved as artifact. Enable Google Docs API for actual doc creation.",
        "title": title
    }


def update_action_tracker(action_items: list) -> dict:
    """Update action items in Google Sheets .
    
    This tool would integrate with Google Sheets API when credentials are configured.
    By default, it saves a local CSV.
    
    Args:
        action_items: List of action items with owner, due date, status
    
    Returns:
        dict with update status
    """
    # In demo mode, save as CSV artifact
    csv_content = "Owner,Action,Due Date,Status\n"
    for item in action_items:
        owner = item.get("owner", "Unassigned")
        action = item.get("action", "")
        due = item.get("due_date", "TBD")
        status = item.get("status", "Open")
        csv_content += f'"{owner}","{action}","{due}","{status}"\n'
    
    save_artifact(csv_content, "action_items.csv")
    
    return {
        "status": "demo_mode",
        "message": "In demo mode - saved as CSV artifact. Enable Google Sheets API for actual tracker update.",
        "items_count": len(action_items)
    }


def draft_followup_email(to: str, subject: str, body: str) -> dict:
    """Draft a follow-up email in Gmail .
    
    This tool would integrate with Gmail API when credentials are configured.
    By default, it saves a local draft.
    
    Args:
        to: Recipient email addresses (comma-separated)
        subject: Email subject
        body: Email body (markdown or plain text)
    
    Returns:
        dict with draft creation status
    """
    # In demo mode, save as artifact
    email_content = f"""To: {to}
Subject: {subject}

{body}

---
*This is a draft. Enable Gmail API to send via Gmail.*
"""
    
    save_artifact(email_content, "followup_email.md")
    
    return {
        "status": "demo_mode",
        "message": "In demo mode - saved as artifact. Enable Gmail API for actual email drafting.",
        "to": to,
        "subject": subject
    }


# Root agent with Memory for team conventions
root_agent = Agent(
    model='gemini-2.0-flash',
    name='meeting_ops',
    description='Transform meeting transcripts into summaries, decisions, action items, and follow-ups',
    instruction="""You are Meeting Ops, an AI system that helps PMs and engineering leads run effective meetings with consistent documentation and action tracking.

You work through a structured workflow:

## 1. Transcript Processing
When a user provides a meeting transcript:
- Parse using `parse_meeting_transcript` to identify speakers and turns
- Extract key discussion points
- Identify topics discussed

## 2. Content Extraction
Analyze the transcript to extract:

### Decisions Made
- What was decided
- Who made the decision
- Rationale/context
- Date/time

### Action Items
- Clear action description
- Owner (assigned person)
- Due date
- Priority
- Dependencies

### Key Discussion Points
- Important topics covered
- Unresolved questions
- Parking lot items (tabled for later)

## 3. Structured Summary
Generate a meeting summary with sections:
- **Meeting Info**: Date, attendees, topic
- **Decisions**: List of decisions with context
- **Action Items**: Structured list with owners/dates
- **Discussion Highlights**: Key points discussed
- **Next Steps**: What happens next
- **Open Questions**: Unresolved items

## 4. Follow-up Artifacts
Create follow-up documents:

### Action Tracker (CSV/Sheets)
- Owner, Action, Due Date, Status, Priority
- Use `update_action_tracker` (requires confirmation)

### Follow-up Email
- Summary of decisions
- Action items by owner
- Links to docs/trackers
- Use `draft_followup_email` (requires confirmation)

### Meeting Doc (Google Docs)
- Full summary with formatting
- Use `create_meeting_doc` (requires confirmation)

## 5. Agenda Generation
When asked to create an agenda for next meeting:
- Review previous action items (from memory)
- Identify unresolved topics
- Suggest agenda items based on context
- Include time allocations

## 6. Cross-Meeting Analysis (with Memory)
Use MemoryService to track:
- Team conventions (how action items are phrased, preferred formats)
- Recurring attendees
- Decision taxonomy
- Answer questions like "What decisions did we make about launch scope across the last 3 meetings?"

## Demo Mode vs Integration Mode

**Demo Mode (Default - No OAuth)**:
- All tools save local artifacts (MD, CSV files)
- No external API calls
- Perfect for trying out the agent

**Integration Mode (Optional - With OAuth)**:
- Actually create Google Docs
- Update Google Sheets trackers
- Draft Gmail emails
- All write operations require Tool Confirmation

## Example Prompts

- "Here's the transcript. Extract decisions and action items; update the tracker; draft a follow-up email."
- "Create an agenda for next week based on last week's open actions and unresolved topics."
- "What decisions did we make about launch scope across the last 3 meetings?"

## Output Artifacts

Always save these artifacts:
- `artifacts/meeting_summary.md` - Full meeting summary
- `artifacts/action_items.csv` - Structured action items
- `artifacts/followup_email.md` - Draft follow-up email
- `artifacts/decisions_log.md` - Decision record

## Quality Checks

- Ensure action items have clear owners (not vague like "the team")
- Include due dates or note "TBD" explicitly
- Decisions should include rationale/context
- Don't fabricate information - only extract what's in the transcript

Be structured, thorough, and help teams maintain decision records and action accountability.
""",
    tools=[
        save_artifact,
        parse_meeting_transcript,
        extract_action_items,
        extract_decisions,
        create_meeting_doc,
        update_action_tracker,
        draft_followup_email,
    ],
    # Enable memory to track team conventions and history
    # memory can be configured with session service
)
