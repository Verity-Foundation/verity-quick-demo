"""
Docstring for src.services.verifier.main
"""
import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from src.core.constants import (ADDHOST, VERIFYPORT)
from .verifier import setup_verification_app

app = FastAPI(
    title="Verity Protocol Demo",
    description="Cryptographic provenance for election integrity",
    version="1.0.0"
)

# Setup verification routes and UI
setup_verification_app(app)

# Mount static files
# app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    """Redirect to verification interface."""
    return RedirectResponse(url="/verify")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "verity-demo",
        "version": "1.0.0",
        "endpoints": ["/verify", "/verify/claim/{id}"]
    }

def start():
    """
    Docstring for start
    """
    uvicorn.run(
        app,
        host=ADDHOST,
        port=VERIFYPORT
    )
