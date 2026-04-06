from fastapi import APIRouter, HTTPException
import os
import json
import asyncio
import logging
from pydantic import BaseModel, Field
from typing import List, Optional
from google import genai
from google.genai import types
from app.core.firebase import save_meeting_context

logger = logging.getLogger(__name__)
router = APIRouter()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# --- 1. Schemas ---
class ProcessMeetingRequest(BaseModel):
    meeting_id: str
    transcript: str

class ActionableItem(BaseModel):
    item_id: str = Field(description="A unique identifier for the item (e.g. ctx_001)")
    type: str = Field(description="MUST be exactly one of: 'task', 'decision', 'deadline', 'discussion'")
    content: str = Field(description="A concise, actionable summary of the item")
    assignee: Optional[str] = Field(None, description="The person assigned to the task, if mentioned")
    deadline: Optional[str] = Field(None, description="The deadline, if mentioned")
    proactive_suggestion: Optional[str] = Field(None, description="If this is a problem statement, a request to email someone, or a request to schedule a meeting, provide a short proactive prompt offering to execute that tool.")

class ExtractionResult(BaseModel):
    items: List[ActionableItem] = Field(
        description="A list of actionable items. MUST BE EMPTY if the transcript contains only small talk, background noise, or irrelevant chatter."
    )

SYSTEM_INSTRUCTION = """
You are a highly analytical Context Extractor listening to enterprise meeting transcripts.
Your ONLY job is to identify concrete business tasks, decisions, deadlines, AND proactive opportunities.

CRITICAL INSTRUCTIONS ON NOISE AND CHATTER:
1. IGNORING SMALL TALK: The transcript will contain background noise, casual banter, greetings, technical issues ("can you hear me?"), and loose talk. Ignore ALL of this.
2. PROACTIVE AGENT TRIGGERS: If the team mentions sending an email, scheduling a meeting, or if they are having a general hackathon/brainstorming discussion about a problem statement, set the 'proactive_suggestion' field. Examples: "✨ Would you like me to draft an email to the sponsors?", "✨ Want me to generate 3 solutions for this problem?", "✨ Shall I schedule a Google Meet?"
3. HIGH THRESHOLD: Do NOT extract an item unless it is clearly actionable, a definitive business decision, or a clear problem statement warranting AI help.
4. NO HALLUCINATION: Only use information explicitly spoken. Do not guess assignees or dates if they aren't stated.
5. EMPTY RESULTS: If the entire transcript block is just casual chat, return an empty list: {"items": []}.
"""

# --- 2. Synchronous Gemini Execution ---
def _extract_sync(transcript: str) -> dict:
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=[f"Process this transcription segment: {transcript}"],
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            response_mime_type="application/json",
            response_schema=ExtractionResult,
            temperature=0.1, 
        )
    )
    return json.loads(response.text)

# --- 3. FastAPI Route ---
@router.post("/process-meeting")
async def process_meeting(request: ProcessMeetingRequest):
    """Parses a transcript and pushes actionable items to Firebase"""
    try:
        # Offload Gemini CPU blocking call
        result_dict = await asyncio.to_thread(_extract_sync, request.transcript)
        
        # Save to DB immediately so Frontend onSnapshot catches it
        db_payload = {
            "meeting_id": request.meeting_id,
            "raw_transcript": request.transcript,
            "extracted_items": result_dict.get("items", [])
        }
        await save_meeting_context(db_payload)

        return {
            "status": "success",
            "items": db_payload["extracted_items"]
        }
    except Exception as e:
        logger.error(f"Extractor failed: {e}")
        # Graceful degradation fallback
        return {
            "status": "error",
            "message": "System disrupted",
            "items": []
        }
