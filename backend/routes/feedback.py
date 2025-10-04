"""API endpoints for collecting user feedback."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/feedback")
async def get_feedback():
    """Placeholder endpoint for feedback collection."""
    return {"message": "Feedback endpoint - To be implemented"}
