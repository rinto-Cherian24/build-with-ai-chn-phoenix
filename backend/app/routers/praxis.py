from fastapi import APIRouter, HTTPException
from app.models.schemas import PraxisRequest, PraxisResponse
from app.services.praxis_service import run_praxis_simulation
from app.core.firebase import save_praxis_session
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/simulate-praxis", response_model=PraxisResponse)
async def simulate_praxis(request: PraxisRequest):
    """
    Initiates a multi-agent debate using Gemini Flash regarding the proposed user prompt.
    Writes the resulting session to Firebase and securely returns the exact schema mapping.
    """
    try:
        # Run AI Swarm logic
        simulation_result: PraxisResponse = await run_praxis_simulation(request.prompt)
        
        # Log to RTDB Firebase (Phase 2 constraint)
        # We model dump the final output along with the original trigger prompt
        db_payload = {
            "prompt": request.prompt,
            "response": simulation_result.model_dump()
        }
        await save_praxis_session(db_payload)
        
        return simulation_result
        
    except Exception as e:
        logger.error(f"Error in simulate_praxis endpoint: {e}")
        # Standardize external crash reporting
        raise HTTPException(status_code=500, detail="Internal Simulation Engine Error")
