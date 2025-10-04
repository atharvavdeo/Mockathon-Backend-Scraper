"""API endpoints for managing evidence sources."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/sources")
async def get_sources():
    """Placeholder endpoint for evidence sources."""
    return {"message": "Sources endpoint - To be implemented"}
