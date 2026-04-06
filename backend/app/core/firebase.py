import os
import firebase_admin
from firebase_admin import credentials, db
import logging

logger = logging.getLogger(__name__)

# Initialize Firebase App
def init_firebase():
    if not firebase_admin._apps:
        # Assumes GOOGLE_APPLICATION_CREDENTIALS is set in env
        # Or alternatively pass a path directly
        cred = credentials.ApplicationDefault()
        
        # Pull the DB URL from environment variables
        database_url = os.getenv("FIREBASE_DATABASE_URL", "https://your-project.firebaseio.com")
        
        firebase_admin.initialize_app(cred, {
            'databaseURL': database_url
        })
        logger.info("Firebase Admin SDK initialized for RTDB.")

init_firebase()

async def save_praxis_session(data: dict):
    """
    Pushes a new record to the /praxis_sessions path in the Realtime Database.
    """
    try:
        ref = db.reference('/praxis_sessions')
        # push() generates a unique ID automatically
        new_session_ref = ref.push(data)
        logger.info(f"Successfully saved praxis session: {new_session_ref.key}")
        return new_session_ref.key
    except Exception as e:
        logger.error(f"Failed to save to Firebase RTDB: {e}")
        # Not throwing here so we don't break the main API response if DB logging fails
        return None

async def save_meeting_context(data: dict):
    """
    Pushes a new record to the /extracted_context path in the Realtime Database.
    """
    try:
        ref = db.reference('/extracted_context')
        new_ref = ref.push(data)
        logger.info(f"Successfully saved meeting context: {new_ref.key}")
        return new_ref.key
    except Exception as e:
        logger.error(f"Failed to save context to Firebase RTDB: {e}")
        return None
