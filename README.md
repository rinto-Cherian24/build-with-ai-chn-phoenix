# Project Omni

## Problem Statement
The demand for intelligent systems capable of assisting users in decision-making, automating workflows, and managing information is rapidly increasing across domains. Existing systems often lack contextual understanding and adaptability.

Participants are tasked with developing an advanced AI assistant capable of understanding context, analyzing information, and performing meaningful actions. The solution should enhance productivity and user experience across domains such as education, business, or everyday use. 

## Project Description
Project Omni is an advanced, context-aware intelligence assistant and AI Copilot designed for high-stakes enterprise scenarios. Our solution bridges the gap between raw ideas and safe execution. It leverages multi-agent simulation to automatically extract precise context from raw meeting transcripts. It then runs predictive simulations (a "Praxis Swarm") to anticipate risks, gauge dynamic feedback, and propose safer alternatives before a decision is finalized. This acts as a cognitive dashcam and real-time simulator to map out action consequences.

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
