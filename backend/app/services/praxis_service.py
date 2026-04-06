import os
import json
import asyncio
import logging
from pydantic import BaseModel, Field
from typing import List
from google import genai
from google.genai import types
from app.models.schemas import PraxisResponse, ConversationInteraction

logger = logging.getLogger(__name__)

# --- 1. The Pydantic Contracts from our AI Brain ---

class SwarmRoles(BaseModel):
    manager_role_name: str = Field(description="Name of the Proponent persona (e.g. 'VP of Sales', 'Engineering Lead')")
    manager_instructions: str = Field(description="Instructions on what this persona cares about.")
    
    customer_role_name: str = Field(description="Name of the Skeptic/User persona (e.g. 'Angry Client', 'Junior Dev')")
    customer_instructions: str = Field(description="Instructions for the skeptical persona.")
    
    legal_role_name: str = Field(description="Name of the Risk persona (e.g. 'PR Director', 'Security Officer')")
    legal_instructions: str = Field(description="Instructions for the risk-averse persona.")

class AgentResponseModel(BaseModel):
    text: str = Field(description="What the agent says in the chat.")

class OrchestratorSynthesis(BaseModel):
    riskScore: int = Field(description="The final aggregated risk score (0-100).")
    riskLevel: str = Field(description="MUST be exactly one of: 'low', 'medium', 'high'")
    sayDoGap: str = Field(description="One sentence summarizing the Say-Do gap.")
    insight: str = Field(description="Core behavioral insight or prediction.")
    saferVariant: str = Field(description="A rewrite or recommendation to make this action safer/better.")


# --- 2. The Sequential Synchronous Generation Logic ---

def _sync_simulate_praxis(proposed_action: str) -> dict:
    """The synchronous AI logic copied directly from AI Brain's simulation_swarm.py"""
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    model_name = 'gemini-2.5-flash'
    
    conversation_log = []
    
    # === TURN 0: ROLE ALLOCATOR ===
    allocation_prompt = f"""
    A user wants to simulate the impact of this action: '{proposed_action}'.
    Define the 3 best agent personas to debate this action. 
    You must map them to our system anchors:
    1. Manager Slot: The proponent of the idea (focuses on short-term wins/goals).
    2. Customer Slot: The receiver/skeptic (focuses on friction, trust, or frustration).
    3. Legal Slot: The risk/compliance officer (focuses on brand, security, or legal fallout).
    """
    role_resp = client.models.generate_content(
        model=model_name,
        contents=[allocation_prompt],
        config=types.GenerateContentConfig(response_mime_type="application/json", response_schema=SwarmRoles)
    )
    roles = json.loads(role_resp.text)
    
    # === TURN 1: PROPONENT (Manager) ===
    manager_prompt = f"""
    You are the {roles['manager_role_name']}. 
    Your instructions: {roles['manager_instructions']}
    You want to execute this action: '{proposed_action}'.
    Output your statement advocating for this action. Be confident.
    """
    m_resp = client.models.generate_content(
        model=model_name,
        contents=[manager_prompt],
        config=types.GenerateContentConfig(response_mime_type="application/json", response_schema=AgentResponseModel)
    )
    m_text = json.loads(m_resp.text)["text"]
    conversation_log.append({
        "agentId": "manager",
        "agentName": roles['manager_role_name'],
        "text": m_text,
        "timeOffset": 500
    })

    # === TURN 2: REACTION (Customer) ===
    customer_prompt = f"""
    You are the {roles['customer_role_name']}.
    Your instructions: {roles['customer_instructions']}
    Action proposed: '{proposed_action}'.
    {roles['manager_role_name']} said: "{m_text}"
    React directly to them conversationally. Focus on resistance, friction, or loss of trust.
    """
    c_resp = client.models.generate_content(
        model=model_name,
        contents=[customer_prompt],
        config=types.GenerateContentConfig(response_mime_type="application/json", response_schema=AgentResponseModel)
    )
    c_text = json.loads(c_resp.text)["text"]
    conversation_log.append({
        "agentId": "customer",
        "agentName": roles['customer_role_name'],
        "text": c_text,
        "timeOffset": 2000
    })

    # === TURN 3: WARNING (Legal) ===
    legal_prompt = f"""
    You are the {roles['legal_role_name']}.
    Your instructions: {roles['legal_instructions']}
    Action proposed: '{proposed_action}'.
    {roles['manager_role_name']} said: "{m_text}"
    {roles['customer_role_name']} reacted: "{c_text}"
    React to both of them. Warn about long term systemic risks or compliance issues.
    """
    l_resp = client.models.generate_content(
        model=model_name,
        contents=[legal_prompt],
        config=types.GenerateContentConfig(response_mime_type="application/json", response_schema=AgentResponseModel)
    )
    l_text = json.loads(l_resp.text)["text"]
    conversation_log.append({
        "agentId": "legal",
        "agentName": roles['legal_role_name'],
        "text": l_text,
        "timeOffset": 3500
    })

    # === TURN 4: ORCHESTRATOR SYNTHESIS ===
    orchestrator_prompt = f"""
    You are evaluating this action: '{proposed_action}'.
    A debate occurred:
    {roles['manager_role_name']}: "{m_text}"
    {roles['customer_role_name']}: "{c_text}"
    {roles['legal_role_name']}: "{l_text}"
    
    Synthesize this debate and output the strict risk metrics.
    """
    final_resp = client.models.generate_content(
        model=model_name,
        contents=[orchestrator_prompt],
        config=types.GenerateContentConfig(response_mime_type="application/json", response_schema=OrchestratorSynthesis)
    )
    synthesis_data = json.loads(final_resp.text)
    
    return {
        "riskScore": synthesis_data["riskScore"],
        "riskLevel": synthesis_data["riskLevel"],
        "sayDoGap": synthesis_data["sayDoGap"],
        "insight": synthesis_data["insight"],
        "saferVariant": synthesis_data["saferVariant"],
        "conversation": conversation_log
    }

# --- 3. The Async FastAPI Route Wrapper ---

async def run_praxis_simulation(user_prompt: str) -> PraxisResponse:
    """
    Runs the sequential persona logic in a thread to prevent blocking Uvicorn,
    then formats it safely into the UI's contract.
    """
    try:
        # Offload the Google GenAI generation to a background thread
        result_dict = await asyncio.to_thread(_sync_simulate_praxis, user_prompt)
        
        # Format the interaction objects
        final_logs = []
        for log in result_dict["conversation"]:
            final_logs.append(ConversationInteraction(
                agentId=log["agentId"],
                agentName=log["agentName"],
                text=log["text"],
                timeOffset=log["timeOffset"]
            ))
            
        return PraxisResponse(
            riskScore=result_dict["riskScore"],
            riskLevel=result_dict["riskLevel"],
            sayDoGap=result_dict["sayDoGap"],
            insight=result_dict["insight"],
            saferVariant=result_dict["saferVariant"],
            conversation=final_logs
        )
    except Exception as e:
        logger.error(f"AI Swarm Crash: {e}")
        # Fallback dummy data if generation fails
        return PraxisResponse(
            riskScore=100,
            riskLevel="high",
            sayDoGap="System integration failure.",
            insight=f"Error: {str(e)}",
            saferVariant="Please check backend logs.",
            conversation=[
                ConversationInteraction(
                    agentId="manager", 
                    agentName="System Monitor", 
                    text=f"API connection failed: {str(e)}", 
                    timeOffset=0
                )
            ]
        )
