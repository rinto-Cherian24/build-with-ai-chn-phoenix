# Project Omni

## Problem Statement
The demand for intelligent systems capable of assisting users in decision-making, automating workflows, and managing information is rapidly increasing across domains. Existing systems often lack contextual understanding and adaptability.

Participants are tasked with developing an advanced AI assistant capable of understanding context, analyzing information, and performing meaningful actions. The solution should enhance productivity and user experience across domains such as education, business, or everyday use. 

## Project Description
Project Omni is not just a digital assistant; it is a **Cognitive Enterprise Operating System**. It bridges the massive gap between abstract strategy formulation and real-world execution by acting as a proactive, highly contextual **"Decision Time Machine."**

Omni fundamentally redesigns how organizations execute tasks through two radical innovations:

**1. The Cognitive Dashcam (Context Engine):**
Meeting notes get lost, and intent is often muddled by casual banter. Omni acts as an active listener. Using advanced LLMs, it siphons chaotic, raw meeting audio and transcripts, dynamically stripping away noise to automatically generate an undisputed, structured ledger of exact decisions, assignees, and deadlines. It transforms casual talk instantly into strict, executable code and JSON logic.

**2. The Praxis Swarm (Predictive Simulation Arena):**
Instead of just logging tasks, Omni simulates them. Before a potentially flawed decision ever touches the real world, it is intercepted by our Praxis Swarm Engine. Omni dynamically instantiates a customized, parallel multi-agent debate consisting of specialized AI Personas—such as a protective Legal Director, a Revenue-focused Manager, and a spam-sensitive Customer. These agents aggressively debate the proposed action in real time. They expose hidden frictions, calculate an aggregate predictive Risk Score, and autonomously generate safer, optimized action paths.

With Project Omni, teams no longer rely on hindsight. Every decision is battle-tested in a hyper-realistic AI simulation arena, turning defensive, reactive management into a predictive superpower. 
## Google AI Usage
### Tools / Models Used
- Google Gemini 1.5 Flash
- Google Gemini 1.5 Pro
- `google-genai` Python SDK

### How Google AI Was Used
Google AI is integrated into the core of Project Omni as the central "Brain":
1. **Context Extraction:** Gemini parses chaotic conversational transcripts, filtering out fluff and strictly outputting actionable JSON data (tasks, deadlines, decisions) using Pydantic schemas.
2. **Multi-Agent Simulation (Praxis Swarm):** We utilize Gemini to concurrently power three distinct AI personas (Customer, Finance, and Legal/Brand). When a new action is proposed, Gemini intelligently simulates a debate between these personas, synthesizing their real-time feedback into a final Risk Score and suggesting safer action variants.

## Proof of Google AI Usage

## Screenshots

![Screenshot 1](./proof/screenshot1.png)
![Screenshot 2](./proof/screenshot2.png)

## Demo Video
[Watch Demo](#) *(https://drive.google.com/drive/folders/1PIg69rjF-MnUC-JSNNcDp0YgIh59ab4B?usp=sharing)*

## Installation Steps
# Clone the repository
git clone <your-repo-link>

# Go to project folder
cd Project-Omni

# Install Backend Dependencies (requires Python 3)
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload

# In a new terminal, Install Frontend Dependencies
cd frontend
npm install

# Run the frontend project
npm run dev
