import json
from google import genai
from google.genai import types
import datetime

# --- 1. The Tool Manifest (Developer 4's Role) ---
# You design this python function interface. The Gemini SDK natively converts this into 
# a JSON Tool Schema so Gemini knows exactly what variables it needs to extract.

def create_calendar_event(title: str, start_time_iso: str, duration_minutes: int, attendees_names: list[str], needs_meet_link: bool):
    """
    Schedules a new event on Google Calendar and optionally generates a Google Meet link.
    
    Args:
        title: The subject or name of the meeting.
        start_time_iso: The precise start time in ISO 8601 format (e.g., '2026-04-09T16:00:00Z').
        duration_minutes: The length of the meeting in minutes. Assume 30 or 60 if unspecified.
        attendees_names: A list of the names or emails of people who should be invited.
        needs_meet_link: Set to true if a video conference link should be generated.
    """
    # NOTE FOR DEV 3: The actual Google Workspace API logic will go here.
    # For now, this just acts as the schema blueprint for Gemini!
    pass


# --- 2. The Execution Intent Parser ---

def parse_task_intent(user_approved_task: str):
    """Takes the string the user clicked 'Execute' on and parses it into function arguments."""
    client = genai.Client(vertexai=True, project="omni-492518", location="us-central1")
    model_name = 'gemini-2.5-flash'
    
    print(f"📥 Received Approved Task from Frontend: '{user_approved_task}'")
    
    # We pass the current time so Gemini knows what "Thursday" means!
    current_time = datetime.datetime.now().isoformat()
    system_prompt = f"The user has approved a task. Extract the parameters needed to execute it. The current time context is {current_time}."
    
    print("🧠 Gemini is mapping the sentence to the Tool variables...")
    response = client.models.generate_content(
        model=model_name,
        contents=[user_approved_task],
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[create_calendar_event],
            tool_config=types.ToolConfig(
                function_calling_config=types.FunctionCallingConfig(mode='ANY')
            ),
            temperature=0.0, 
        )
    )
    
    return response

if __name__ == "__main__":
    test_task = "Create a meeting with John about Q3 metrics this coming Thursday at 4PM."
    
    # Run our extraction protocol
    result = parse_task_intent(test_task)
    
    print("\n==========================================")
    if result.function_calls:
        print("✅ SUCCESS! Gemini fired the Tool Call!")
        for call in result.function_calls:
            print(f"Tool Triggered:  {call.name}")
            print(f"Extracted Args:  {json.dumps(call.args, indent=2)}")
            print("\n🗣️ Tell Dev 3: 'Take the args dictionary above and pass it into the actual Google API request body!'")
    else:
        print("❌ Gemini failed to trigger the tool. Here is the raw response:")
        print(result.text)
    print("==========================================")
