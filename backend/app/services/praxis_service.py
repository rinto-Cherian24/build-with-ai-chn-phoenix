import os
import json
import asyncio
import logging
from google import genai
from google.genai import types
from app.models.schemas import PraxisResponse, ConversationInteraction

logger = logging.getLogger(__name__)

# Switch to the new SDK standard per your request
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

MODEL_NAME = "gemini-1.5-flash"

async def prompt_agent(persona_name: str, objective: str, user_prompt: str) -> dict:
    """Calls Gemini as a specific agent persona."""
    prompt = f"""
    The user is proposing the following action:
    "{user_prompt}"
    
    Analyze this from your persona's perspective. Return a JSON object with this exact structure:
    {{
      "agentName": "{persona_name}",
      "text": "Your brief, 1-2 sentence reaction.",
      "risk_score": <int between 0 and 100 representing risk from your perspective>
    }}
    """
    try:
        # Run synchronous SDK call in thread to avoid event loop blocking
        response = await asyncio.to_thread(
            client.models.generate_content,
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=f"You are the {persona_name}. {objective}. Output valid JSON only.",
                response_mime_type="application/json",
                temperature=0.7
            )
        )
        return json.loads(response.text)
    except Exception as e:
        logger.error(f"Agent {persona_name} failed: {e}")
        return {
            "agentName": persona_name,
            "text": f"(System disrupted) Error processing via {persona_name} channels.",
            "risk_score": 50
        }

async def synthesize_responses(user_prompt: str, agent_responses: list) -> dict:
    """Synthesizes the multi-agent feedback into the final required format."""
    context = json.dumps(agent_responses, indent=2)
    prompt = f"""
    Proposed Action: "{user_prompt}"
    
    Agent Feedback Context:
    {context}
    
    Based on the context, return a JSON object with strictly these keys:
    {{
      "sayDoGap": "A short sentence highlighting short-term vs long-term conflict.",
      "insight": "A core actionable insight.",
      "saferVariant": "A recommended alternative approach.",
      "riskLevel": "high" // MUST be exactly "low", "medium", or "high"
    }}
    """
    try:
        response = await asyncio.to_thread(
            client.models.generate_content,
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction="You are the Executive Synthesizer. Merge multi-agent feedback into a final report. Output valid JSON only.",
                response_mime_type="application/json",
                temperature=0.4
            )
        )
        return json.loads(response.text)
    except Exception as e:
        logger.error(f"Synthesis failed: {e}")
        return {
            "sayDoGap": "Cannot compute gap due to system error.",
            "insight": "Synthesis engine unavailable.",
            "saferVariant": "Retry action.",
            "riskLevel": "medium"
        }

async def run_praxis_simulation(user_prompt: str) -> PraxisResponse:
    """
    Orchestrates the Swarm interaction with 3 parallel agents, synthesizes the results,
    and returns a strictly compliant Pydantic Response object.
    """
    agent_tasks = [
        prompt_agent("Manager", "Focus on aggressive growth, sales spikes, and immediate numbers.", user_prompt),
        prompt_agent("Customer", "Focus on user experience, fatigue, and brand perception.", user_prompt),
        prompt_agent("Legal", "Focus on compliance, brand safety, and risk mitigation.", user_prompt)
    ]
    
    agent_results = await asyncio.gather(*agent_tasks)
    
    scores = [res.get("risk_score", 50) for res in agent_results]
    final_risk_score = int(sum(scores) / len(scores))
    
    agent_mapping = {"Manager": "manager", "Customer": "customer", "Legal": "legal"}
    conversation_logs = []
    offset = 500
    
    for res in agent_results:
        agent_name = res.get("agentName", "Unknown")
        agent_id = agent_mapping.get(agent_name, "manager")
        if agent_id not in ["manager", "customer", "legal"]:
            agent_id = "manager" 
            
        display_name = "Brand/Legal" if agent_name == "Legal" else agent_name
            
        conversation_logs.append(ConversationInteraction(
            agentId=agent_id,
            agentName=display_name,
            text=res.get("text", "No comment provided."),
            timeOffset=offset
        ))
        offset += 1500
        
    synthesis = await synthesize_responses(user_prompt, agent_results)
    
    risk_level = synthesis.get("riskLevel", "medium").lower()
    if risk_level not in ["low", "medium", "high"]:
        risk_level = "medium"
        
    return PraxisResponse(
        riskScore=final_risk_score,
        riskLevel=risk_level,
        sayDoGap=synthesis.get("sayDoGap", ""),
        insight=synthesis.get("insight", ""),
        saferVariant=synthesis.get("saferVariant", ""),
        conversation=conversation_logs
    )
