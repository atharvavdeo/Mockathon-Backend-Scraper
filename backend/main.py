"""Main application file for the FastAPI backend."""

from fastapi import FastAPI
# Corrected: Use relative imports to make 'backend' a runnable package
from .routes import detect, feedback, sources

app = FastAPI(
    title="Multi-Agent Fake-News Detection Platform",
    description="A backend system to detect fake news from various sources with URL, text, and image processing capabilities.",
    version="1.0.0",
)

# Include the API routers from the 'routes' module
app.include_router(detect.router, prefix="/api/v1", tags=["Detection"])
app.include_router(feedback.router, prefix="/api/v1", tags=["Feedback"])
app.include_router(sources.router, prefix="/api/v1", tags=["Sources"])

@app.get("/", tags=["Root"])
async def read_root():
    """A simple root endpoint to confirm the API is running."""
    return {
        "message": "Welcome to the Fake-News Detection API",
        "endpoints": {
            "process_url": "/api/v1/process-url",
            "process_text": "/api/v1/process-text",
            "process_image": "/api/v1/process-image",
            "feedback": "/api/v1/feedback",
            "sources": "/api/v1/sources"
        }
    }
