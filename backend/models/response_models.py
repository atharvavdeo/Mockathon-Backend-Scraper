"""Response models for API endpoints."""

from pydantic import BaseModel, Field
from typing import List, Optional

class EvidenceSource(BaseModel):
    """Single evidence source."""
    url: str
    title: str
    snippet: str
    similarity: Optional[str] = None

class Evidence(BaseModel):
    """Collection of evidence sources."""
    sources: List[EvidenceSource] = []

class EvidenceAnalysis(BaseModel):
    """Complete evidence-based analysis."""
    verdict: str = Field(..., description="FAKE, REAL, or UNCERTAIN")
    confidence_value: int = Field(..., description="Confidence percentage 0-100")
    explanation: str = Field(..., description="Human-readable explanation")
    evidence: Evidence = Field(default_factory=lambda: Evidence(sources=[]))
    warning_signals: List[str] = Field(default_factory=list, description="List of warning signals detected")
    extracted_topics: List[str] = Field(default_factory=list, description="List of topics extracted from content")

class ProcessedInput(BaseModel):
    """The processed input data."""
    title: str
    body: str
    image_text: Optional[str] = None
    source_url: Optional[str] = None
    word_count: int

class CompleteAnalysisResponse(BaseModel):
    """Complete response with processed input and analysis."""
    processed_input: ProcessedInput
    evidence_analysis: EvidenceAnalysis
