"""
Main FastAPI application entry point.
"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1 import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events."""
    # Create tables on startup
    Base.metadata.create_all(bind=engine)
    yield
    # Cleanup on shutdown if needed


app = FastAPI(
    title="PRATT - IDCC Requirements Assistant",
    description="Requirements intake and analytics application",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Include API router
app.include_router(api_router, prefix="/api/v1")

# Include web UI routes
from app.web.routes import web_router
app.include_router(web_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "PRATT - IDCC Requirements Assistant API", "version": "0.1.0"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


