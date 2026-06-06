import os
from fastapi import FastAPI, HTTPException, Header, BackgroundTasks
from pydantic import BaseModel
from dotenv import load_dotenv
from pipeline.s3_uploader import stream_video_to_s3

load_dotenv()

app = FastAPI(title="Tavus AI Interview Cloud Pipeline")

class TavusWebhookPayload(BaseModel):
    event: str
    session_id: str
    video_url: str

@app.post("/api/v1/tavus-webhook")
async def handle_tavus_webhook(
    payload: TavusWebhookPayload, 
    background_tasks: BackgroundTasks,
    x_tavus_signature: str = Header(None)
):
    if os.getenv("TAVUS_WEBHOOK_SECRET") and not x_tavus_signature:
        raise HTTPException(status_code=401, detail="Unauthorized request source.")

    if payload.event != "session.completed":
        return {"status": "ignored", "reason": "Event type is not session.completed"}

    background_tasks.add_task(stream_video_to_s3, payload.video_url, payload.session_id)
    
    return {"status": "queued", "message": "Secure cloud transfer initiated."}
