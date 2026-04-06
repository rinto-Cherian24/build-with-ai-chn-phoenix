# Project Omni - Backend Handover Document

**GitHub Collaborator:** `athulkrishnans`

Welcome! You are taking over the Omni Copilot Backend codebase. 
This FastAPI server handles the AI Swarm debates (using Gemini 1.5 Flash via the new `google-genai` SDK) and writes the results to our Firebase Realtime Database.

## Current State of Development
- Project architecture is scaffolded inside `/app`.
- The `app/models/schemas.py` rigidly enforces our strict UI payload.
- `app/services/praxis_service.py` runs three simulated AI personas in parallel and synthesizes their debate.
- `app/core/firebase.py` points to our Firebase RTDB.
- A `.env` file exists with the relevant `GEMINI_API_KEY` and `FIREBASE_DATABASE_URL` (ensure this does not get leaked to public repos!).

## Immediate Next Steps for the New Developer

**The previous machine did not have Python installed. You must set up the runtime environment.**

### 1. Install Python
If you are on Windows, download Python (3.10+) from python.org. **IMPORTANT**: Make sure to check the box that says "Add Python to PATH" during installation.

### 2. Install Python Dependencies
Open your terminal inside this `backend/` directory and run:
```bash
python -m pip install -r requirements.txt
```
*(This installs FastAPI, Pydantic, the Google GenAI SDK, Firebase-Admin, etc.)*

### 3. Log In to Firebase (Local Development)
Because the codebase writes to our live Firebase RTDB using Application Default Credentials, you must authenticate your machine with Google locally.
1. Install the tools: `npm install -g firebase-tools`
2. Login: `firebase login`

### 4. Start the Server
Once everything is downloaded, run the application:
```bash
python -m uvicorn app.main:app --reload
```
You should see: `Application startup complete.`

### 5. Test the Endpoints
FastAPI automatically generates an interactive testing dashboard. Once your server is running, go to:
**http://127.0.0.1:8000/docs**
From here, you can click on `POST /api/simulate-praxis` and send a test payload (like testing a new marketing strategy) to watch the AI Swarm work fully end-to-end to generate your JSON!
