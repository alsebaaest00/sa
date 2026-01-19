"""SA Platform API - FastAPI REST API"""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sa.api.routes import get_router

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="SA Platform API",
    description="AI-powered content generation platform - Generate images, videos, and audio using AI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(get_router())


@app.get("/", tags=["General"])
async def root():
    """Root endpoint"""
    return {
        "name": "SA Platform API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/api/v1/health",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
