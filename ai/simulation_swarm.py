import json
from pydantic import BaseModel, Field
from typing import List, Literal, Optional
from google import genai
from google.genai import types

# --- 1. Define the Pydantic Output Contracts ---

# Turn 0: Dynamic Role Allocation
class SwarmRoles(BaseModel):
    manager_role_name: str = Field(description="Name of the Proponent persona (e.g. 'VP of Sales', 'Engineering Lead')")
    manager_instructions: str = Field(description="Instructions on what this persona cares about.")
    
    customer_role_name: str = Field(description="Name of the Skeptic/User persona (e.g. 'Angry Client', 'Junior Dev')")
    customer_instructions: str = Field(description="Instructions for the skeptical persona.")
    
    legal_role_name: str = Field(description="Name of the Risk persona (e.g. 'PR Director', 'Security Officer')")
    legal_instructions: str = Field(description="Instructions for the risk-averse persona.")

# Turn 1-3: Agent chat
class AgentResponse(BaseModel):
    text: str = Field(description="What the agent says in the chat.")

# Turn 4: Final orchestrator synthesis
class OrchestratorSynthesis(BaseModel):
    riskScore: int = Field(description="The final aggregated risk score (0-100).")
    riskLevel: str = Field(description="MUST be exactly one of: 'low', 'medium', 'high'")
    sayDoGap: str = Field(description="One sentence summarizing the Say-Do gap.")
    insight: str = Field(description="Core behavioral insight or prediction.")
    saferVariant: str = Field(description="A rewrite or recommendation to make this action safer/better.")

# The Final API Payload matches the Frontend requirements
class PraxisSimulationResult(BaseModel):
    riskScore: int
    riskLevel: str
    sayDoGap: str
    insight: str
    saferVariant: str
    conversation: List[dict]

# --- 2. The Dynamic Multi-Agent Chat Sequence ---

def simulate_praxis_action(proposed_action: str) -> dict:
    client = genai.Client(vertexai=True, project="omni-492518", location="us-central1")
    model_name = 'gemini-2.5-flash'
    
    conversation_log = []
    print(f"🎬 Initializing Dynamic Swarm for: '{proposed_action}'\n")

    # === TURN 0: ROLE ALLOCATOR (Context-Aware Persona Generation) ===
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
    print(f"✅ Resources Allocated: {roles['manager_role_name']} | {roles['customer_role_name']} | {roles['legal_role_name']}\n")

    # === TURN 1: PROPONENT (Manager Slot) ===
    manager_prompt = f"""
    You are the {roles['manager_role_name']}. 
    Your instructions: {roles['manager_instructions']}
    You want to execute this action: '{proposed_action}'.
    Output your statement advocating for this action. Be confident.
    """
    m_resp = client.models.generate_content(
        model=model_name,
        contents=[manager_prompt],
        config=types.GenerateContentConfig(response_mime_type="application/json", response_schema=AgentResponse)
    )
    m_text = json.loads(m_resp.text)["text"]
    conversation_log.append({
        "agentId": "manager", # UI enforcement
        "agentName": roles['manager_role_name'],
        "text": m_text,
        "timeOffset": 500
    })
    print(f"{roles['manager_role_name']}: {m_text}")

    # === TURN 2: REACTION (Customer Slot) ===
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
        config=types.GenerateContentConfig(response_mime_type="application/json", response_schema=AgentResponse)
    )
    c_text = json.loads(c_resp.text)["text"]
    conversation_log.append({
        "agentId": "customer", # UI enforcement
        "agentName": roles['customer_role_name'],
        "text": c_text,
        "timeOffset": 2000
    })
    print(f"{roles['customer_role_name']}: {c_text}")

    # === TURN 3: WARNING (Legal Slot) ===
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
        config=types.GenerateContentConfig(response_mime_type="application/json", response_schema=AgentResponse)
    )
    l_text = json.loads(l_resp.text)["text"]
    conversation_log.append({
        "agentId": "legal", # UI enforcement
        "agentName": roles['legal_role_name'],
        "text": l_text,
        "timeOffset": 3500
    })
    print(f"{roles['legal_role_name']}: {l_text}")

    # === TURN 4: ORCHESTRATOR SYNTHESIS ===
    print("\n🔍 Synthesizing debate into final API payload...")
    orchestrator_prompt = f"""
    You are evaluating this action: '{proposed_action}'.
    A debate occurred:
    {roles['manager_role_name']}: "{m_text}"
    {roles['customer_role_name']}: "{c_text}"
    {roles['legal_role_name']}: "{l_text}"
    
    Synthesize this debate and output the strict risk metrics.
    Remember to use lowercased 'low', 'medium', or 'high' for riskLevel!
    """
    final_resp = client.models.generate_content(
        model=model_name,
        contents=[orchestrator_prompt],
        config=types.GenerateContentConfig(response_mime_type="application/json", response_schema=OrchestratorSynthesis)
    )
    synthesis_data = json.loads(final_resp.text)
    
    # === ASSEMBLE FINAL API PAYLOAD ===
    final_api_response = {
        "riskScore": synthesis_data["riskScore"],
        "riskLevel": synthesis_data["riskLevel"],
        "sayDoGap": synthesis_data["sayDoGap"],
        "insight": synthesis_data["insight"],
        "saferVariant": synthesis_data["saferVariant"],
        "conversation": conversation_log
    }
    return final_api_response

if __name__ == "__main__":
    # Test with an engineering-focused prompt to prove the dynamic roles work
    test_action = "Fire the entire QA team and rely entirely on AI testing tools starting Monday."
    result = simulate_praxis_action(test_action)
    
    print("\n=== FINAL API PAYLOAD FOR FRONTEND ===")
    print(json.dumps(result, indent=2))
