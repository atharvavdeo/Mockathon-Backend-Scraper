"""Pydantic models for detection-related data structures."""

from pydantic import BaseModel, Field
from typing import Optional


# Pydantic model for URL input
class URLInput(BaseModel):
    url: str = Field(..., description="The URL of the article to be analyzed.")


# Pydantic model for scraped article content
class ScrapedArticle(BaseModel):
    url: str
    title: Optional[str] = None
    body: str  # Changed from 'content' to 'body' for consistency
    author: Optional[str] = None
    publish_date: Optional[str] = None


# NEW: Pydantic model for direct text input
class TextInput(BaseModel):
    text: str = Field(..., min_length=100, description="The raw text to be analyzed (minimum 100 characters).")


# NEW: A standardized response model for pipelines that return cleaned text
class ProcessedText(BaseModel):
    cleaned_text: str
    original_char_count: int
    cleaned_char_count: int


# NEW: Final model-ready input for inference
class ModelInput(BaseModel):
    """
    The final, processed data structure ready to be sent to the ML model.
    The body has been summarized via sentence extraction and truncated to a max word count.
    """
    title: str = Field(..., description="The article title or generated heading.")
    body: str = Field(..., description="The summarized and truncated article body (max 500 words).")
    source_url: Optional[str] = Field(None, description="The source URL if available.")
    word_count: int = Field(..., description="The number of words in the processed body text.")
