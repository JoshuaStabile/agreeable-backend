from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse
from claude_client import call_claude
from messages.agreeable_message import AgreeeableMessage
from rate_manager import RateManager
import config
import os

from app_logger import get_logger

logger = get_logger()
logger.info("Agreeable backend started")

usage_tracker = RateManager(
    per_ext_max=config.MAX_EXTENSION_REQUESTS,
    global_max=config.MAX_GLOBAL_REQUESTS,
    window=config.WINDOW,
)

app = FastAPI()

@app.get("/health")
def health():
    logger.info("Health check requested")
    return {"status": "active"}

@app.get("/eula")
def eula():
    path = os.path.join("static", "eula.html")
    return FileResponse(path, media_type="text/html")

@app.get("/privacy")
def privacy():
    path = os.path.join("static", "privacy.html")
    return FileResponse(path, media_type="text/html")

@app.post("/review_document")
async def review_document(request: Request):
    data = await request.json()

    document_text = data.get("text", "")
    custom_prompt = data.get("customPrompt", "")
    extension_id = data.get("extensionId", "unknown")
    
    logger.info(f"Received request from extension: {extension_id}, text length: {len(document_text)}")
    
    if not document_text:
        logger.warning(f"Request missing 'text' field from extension: {extension_id}")
        raise HTTPException(status_code=400, detail="No 'text' field provided")

    allowed = usage_tracker.update(extension_id)
    if not allowed:
        logger.warning(f"Rate limit exceeded for extension: {extension_id}")
        raise HTTPException(
            status_code=429,  # 429 Too Many Requests
            detail="Rate limit exceeded. Retry again in a few minutes."
        )

    user_msg = AgreeeableMessage(document_text, custom_prompt)
    try:
        result = call_claude([user_msg])
        logger.info(f"Processed request for extension: {extension_id}")
    except Exception as e:
        logger.error(f"Error processing request for extension {extension_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

    return result