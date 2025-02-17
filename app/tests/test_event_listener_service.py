import logging
from fastapi import FastAPI, Request
import uvicorn

# Configure logging for the test event listener.
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("EventListenerService")

# Create FastAPI app to listen for event posts.
app = FastAPI(title="Test Event Listener Service")

@app.post("/user_created")
async def user_created(request: Request):
    """
    Endpoint to receive 'user_created' events.
    Logs the received payload and returns a success response.
    """
    payload = await request.json()
    logger.info(f"Received user_created event: {payload}")
    return {"status": "success", "message": "User created event received"}

@app.post("/user_deleted")
async def user_deleted(request: Request):
    """
    Endpoint to receive 'user_deleted' events.
    Logs the received payload and returns a success response.
    """
    payload = await request.json()
    logger.info(f"Received user_deleted event: {payload}")
    return {"status": "success", "message": "User deleted event received"}

if __name__ == "__main__":
    # Run the listener service on port 5001.
    uvicorn.run(app, host="0.0.0.0", port=5001)