import os
from pydantic import BaseModel, Field
from typing import List, Optional
from google import genai
from google.genai import types

# --- 1. Define the Strict Data Contract (Pydantic) ---
class ActionableItem(BaseModel):
    item_id: str = Field(description="A unique identifier for the item")
    type: str = Field(description="MUST be exactly one of: 'task', 'decision', 'deadline'")
    content: str = Field(description="A concise, actionable summary of the item")
    assignee: Optional[str] = Field(None, description="The person assigned to the task, if mentioned")
    deadline: Optional[str] = Field(None, description="The deadline, if mentioned")

# Notice we wrap it so Gemini can return both the transcript and the extracted items!
class ExtractionResult(BaseModel):
    raw_transcript: str = Field(description="The full transcription of the audio.")
    items: List[ActionableItem] = Field(
        description="A list of actionable items. MUST BE EMPTY if the audio contains only small talk, background noise, or irrelevant chatter."
    )

# --- 2. The System Prompt (Audio-Aware) ---
SYSTEM_INSTRUCTION = """
You are a highly analytical Context Extractor listening to enterprise meeting audio.
Your job is to transcribe the audio AND identify concrete business tasks, decisions, and deadlines.

CRITICAL INSTRUCTIONS ON NOISE AND CHATTER:
1. IGNORING SMALL TALK: The audio will contain background noise, casual banter, greetings, technical issues ("can you hear me?"), and loose talk. Ignore ALL of this when extracting items.
2. HIGH THRESHOLD: Do NOT extract an item unless it is clearly actionable or a definitive business decision. If people are just brainstorming without concluding, do not extract.
3. NO HALLUCINATION: Only use information explicitly spoken. Do not guess assignees or dates if they aren't stated.
4. EMPTY RESULTS: If the entire audio is just casual chat, return an empty list for 'items'.
"""

def extract_from_audio(audio_file_path: str, meeting_id: str) -> str:
    """
    Takes an audio file, sends it to Gemini 1.5 Flash, and returns the strict JSON contract.
    """
    # 1. Initialize client via Vertex AI using your Project ID
    client = genai.Client(vertexai=True, project="omni-492518", location="us-central1")
    
    # 2. Upload the audio file to Gemini
    print(f"Uploading {audio_file_path} to Gemini...")
    audio_file = client.files.upload(file=audio_file_path)
    
    # 3. Call the model
    print("Analyzing audio for tasks and decisions...")
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=[
            audio_file, 
            f"Process this meeting audio for meeting_id: {meeting_id}. Please transcribe it and extract the context."
        ],
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            response_mime_type="application/json",
            response_schema=ExtractionResult,
            temperature=0.1, 
        )
    )
    
    return response.text

if __name__ == "__main__":
    print("To test this, provide a path to a real .mp3 or .wav file!")
    # Example usage:
    # json_output = extract_from_audio("sample_meeting.mp3", "m_12345")
    # print(json_output)
