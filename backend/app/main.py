"""
DataScientist Arena - FastAPI Backend
Main application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path

from app.core.config import settings
from app.api import datasets, analysis, experiments, verification, results, users, personalization

# Initialize FastAPI app
app = FastAPI(
    title="DataScientist Arena API",
    description="AI Reliability & Data Science Benchmarking Platform",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
# Authentication & User Management
app.include_router(users.router, prefix="/api/v1", tags=["authentication"])

# Personalization
app.include_router(personalization.router, prefix="/api/v1", tags=["personalization"])

# Data Science Features
app.include_router(datasets.router, prefix="/api/v1", tags=["datasets"])
app.include_router(analysis.router, prefix="/api/v1", tags=["analysis"])
app.include_router(experiments.router, prefix="/api/v1", tags=["experiments"])
app.include_router(verification.router, prefix="/api/v1", tags=["verification"])
app.include_router(results.router, prefix="/api/v1", tags=["results"])

# Root endpoint
@app.get("/", tags=["root"])
async def read_root():
    """Root endpoint - API information"""
    return {
        "service": "DataScientist Arena",
        "version": "1.0.0",
        "status": "running",
        "docs": "/api/docs",
        "api_base": "/api/v1"
    }

@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "message": "DataScientist Arena is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
