"""
Main FastAPI Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import (
    APP_NAME,
    APP_VERSION,
)

from app.routes import router


app = FastAPI(

    title=APP_NAME,

    version=APP_VERSION,

    description="AI Automotive Diagnostic Assistant API"

)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)


# --------------------------------------------------
# Routes
# --------------------------------------------------

app.include_router(router)


# --------------------------------------------------
# Startup
# --------------------------------------------------

@app.on_event("startup")
async def startup_event():

    print("=" * 60)
    print(APP_NAME)
    print(f"Version : {APP_VERSION}")
    print("Backend Started Successfully")
    print("=" * 60)


# --------------------------------------------------
# Shutdown
# --------------------------------------------------

@app.on_event("shutdown")
async def shutdown_event():

    print("Backend Stopped")


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/health")
async def health():

    return {

        "success": True,

        "status": "healthy",

        "application": APP_NAME,

        "version": APP_VERSION

    }