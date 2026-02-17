from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("AGORA_APP_ID")
APP_CERT = os.getenv("AGORA_APP_CERT")

app = FastAPI(title="Agora Token Service")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class TokenRequest(BaseModel):
    channel: str
    uid: str = "0"
    role: str = "publisher"  # publisher/subscriber


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/token")
async def token(req: TokenRequest):
    if not APP_ID:
        raise HTTPException(status_code=400, detail="AGORA_APP_ID not configured")

    # If no APP_CERT provided, return appId and empty token (useful for testing in projects with App Certificate disabled)
    if not APP_CERT:
        return {"appId": APP_ID, "token": "", "channel": req.channel, "uid": req.uid}

    # If APP_CERT is provided, you can integrate Agora's token builder here.
    # For security, tokens should be generated server-side using Agora's SDK or recommended token builder.
    # To keep this scaffold small, we return appId and instruct the operator to add token builder.
    return {"appId": APP_ID, "token": "", "channel": req.channel, "uid": req.uid}
