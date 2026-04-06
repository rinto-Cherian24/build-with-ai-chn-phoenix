# Project Omni - AI Brain (Prompt Engineering)

Welcome to the AI engineering hub for **Project Omni**! 

This folder is dedicated to developing the "AI Brain" of our context-aware intelligence assistant. Our goal is to nail down the prompt engineering, data structuring, and multi-agent simulation logic before handing it off to the backend for integration.

---

## 🎯 Our Role & Objectives

We are responsible for **Prompt Engineering and AI Orchestration**. We will build and refine two core pillars of the AI system, operating primarily in a prototype environment (Jupyter Notebooks / Python scripts) using the **Gemini API**.

### Pillar A: Context Extractor (The Cognitive Dashcam)
Taking raw, messy conversational transcripts and extracting structured facts using strict JSON schemas.

### Pillar B: Praxis Swarm (The Decision Simulation)
Building a 3-agent orchestration (Customer, Finance, Legal personas) that takes proposed actions and simulates risk, feedback, and alternative suggestions.

---

## 🛠️ Stack & Tooling

To keep things lightweight, iterative, and hackathon-friendly, our immediate stack for this folder will be:
- **Language:** Python 3
- **Environment:** Jupyter Notebooks / Python Scripts (`.ipynb` / `.py`)
- **LLM Provider:** Google Gemini Pro / Flash APIs (via `google-genai` SDK)
- **Agent Orchestration:** Minimal custom Python loops or CrewAI (if we want to go heavier). *Recommendation: Let's start with a custom loop for complete control over the JSON outputs.*
- **Data Handling:** `pydantic` heavily used to enforce Gemini's structured output matching our Firebase contract.

---

## 📅 Roadmap & Execution Plan

### Phase 1: Context Extractor (Hours 1-12)
**Goal:** Force Gemini to parse messy text into our strict Firebase JSON schema.
- [ ] Set up the Google Gemini SDK and API keys.
- [ ] Define the `Pydantic` schema matching the `extracted_context` Firebase collection.
- [ ] Write the system instructions that instruct the model to ignore fluff and only extract actionable tasks, decisions, and deadlines.
- [ ] Test with a dummy raw transcript: *"AWS budget capped at 800 USD. John needs the Q3 metrics report by Thursday 4 PM."*
- [ ] Validate that the output perfectly matches the schema.

### Phase 2: Praxis Swarm (Hours 12-24)
**Goal:** Build the multi-agent decision simulation engine.
- [ ] Define the System Prompts for our 3 personas:
  - 🧍 **Customer Persona:** Focuses on value, spam sensitivity, and trust. Let's make them easily annoyed by pop-ups and high-churn risks.
  - 💼 **Finance/Manager Persona:** Focuses on short-term conversion, revenue, and budget limits.
  - ⚖️ **Brand/Legal Persona (Optional but good):** Focuses on reputation, compliance, and long-term brand equity.
- [ ] Establish the scoring logic and JSON output schema for the swarm's response.
- [ ] Build the "orchestrator" function: send the proposed action and recent context to each agent, gather their JSON feedback, and use a final prompt to synthesize the `risk_score` and `recommendation`.
- [ ] Test with demo scenarios: *"Launch a 50% discount for 24h via pop-ups and push notifications."*

### Phase 3: Handoff & Demo Data (Hours 24-36)
**Goal:** Hand off the brain to the backend and build the wow-factor data.
- [ ] Package the extraction and simulation logic into clean Python functions.
- [ ] Provide the FastAPI team (Backend) with our tested API calls, schemas, and prompts.
- [ ] Generate 10-15 hyper-realistic, diverse transcripts mimicking real enterprise meetings to pre-populate our database for a killer, realistic live demo.

---

## 📝 API & Data Contracts Reference

### 1. Extractor Output Schema (Context)
```json
{
  "item_id": "string",
  "meeting_id": "string",
  "type": "task | decision | deadline",
  "content": "string",
  "assignee": "string (optional)",
  "deadline": "string (optional)"
}
```

### 2. Praxis Simulation Output Schema
```json
{
  "risk_score": 0-100,
  "risk_level": "Low | Medium | High",
  "agents": [
    { "persona": "Customer", "score": 0-100, "feedback": "string" },
    { "persona": "Finance", "score": 0-100, "feedback": "string" }
  ],
  "recommendation": "string"
}
```

---

## 🚀 Next Steps

We should start with **Phase 1: Context Extractor**. 
Let's spin up a Python script or notebook, define our Pydantic schemas, and write our first prompt to extract the demo transcript. 

*Are you ready to start writing the schema and extraction logic?*
