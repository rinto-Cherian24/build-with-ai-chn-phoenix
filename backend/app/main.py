from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import praxis, meetings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Omni Copilot API",
    description="Server mapping Gemini AI simulations to Firebase RTDB for frontend consumption.",
    version="1.0.0"
)

# Set up CORS so your frontend can communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Ensure you lock this down in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers we just built
app.include_router(praxis.router, prefix="/api", tags=["Praxis Swarm Simulation"])
app.include_router(meetings.router, prefix="/api", tags=["Meeting Process"])

@app.get("/health")
def health_check():
    return {"status": "backend_is_live"}
