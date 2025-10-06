"""Main application file for the FastAPI backend."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Use relative imports when running as a package
from .routes import detect, feedback, sources

app = FastAPI(
    title="Multi-Agent Fake-News Detection Platform",
    description="A backend system to detect fake news from various sources with URL, text, and image processing capabilities.",
    version="1.0.0",
)

# CORS Middleware - configured to allow all origins for API access
# In production, update allow_origins with specific client domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with specific origins in production (e.g., ["https://yourdomain.com"])
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
