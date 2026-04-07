# Project Omni

## Problem Statement
Abstract decision-making in large organizations often lacks immediate visibility into real-world implications, risks, and brand impacts. Teams frequently struggle to balance short-term gains (e.g., a fast sales spike) with long-term brand trust without undergoing extensive, slow manual reviews. 

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
Attach screenshots in a `/proof` folder:

![AI Proof](./proof/ai-proof.png)

## Screenshots

![Screenshot 1](./proof/screenshot1.png)
![Screenshot 2](./proof/screenshot2.png)

## Demo Video
[Watch Demo](#) *(Upload your demo video to Google Drive and paste the shareable link here)*

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
