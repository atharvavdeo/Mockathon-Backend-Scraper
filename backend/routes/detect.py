"""API endpoints for news content detection."""

from fastapi import APIRouter, HTTPException, Body, File, UploadFile
# Corrected: Use relative imports to find modules within the 'backend' package
from ..core.input_handler import (
    process_url_for_analysis, 
    process_text_for_analysis, 
    process_image_for_analysis
)
from ..models.detection_models import URLInput, ModelInput, TextInput

router = APIRouter()

@router.post(
    "/process-url",
    response_model=ModelInput,
    summary="Process and Scrape a News Article URL",
    description="Accepts a URL, scrapes its content, cleans it, summarizes using TF-IDF, and returns model-ready input."
)
async def process_url(payload: URLInput = Body(...)):
    """
    This endpoint takes a news article URL and performs the following steps:
    - **Scrapes**: Extracts title, body, and metadata.
    - **Cleans**: Removes HTML, extra whitespace, and special characters.
    - **Validates**: Ensures the content is in English and meets a minimum length.
    - **Summarizes**: Uses TF-IDF to extract key sentences (extractive summarization).
    - **Truncates**: Limits body to 500 words maximum.

    The returned data is ready to be sent directly to your ML model for inference.
    """
    try:
        processed_input = await process_url_for_analysis(payload)
        return processed_input
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Generic catch-all for unexpected errors
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@router.post(
    "/process-text",
    response_model=ModelInput,
    summary="Process Raw Text Input",
    description="Accepts a block of text, cleans it, validates it, summarizes using TF-IDF, and returns model-ready input."
)
async def process_text(payload: TextInput = Body(...)):
    """
    This endpoint takes a JSON object with a `text` field and processes it.
    - **Validates**: Ensures text is in English and meets minimum length.
    - **Cleans**: Removes extra whitespace and special characters.
    - **Summarizes**: Uses TF-IDF to extract key sentences.
    - **Truncates**: Limits body to 500 words maximum.
    - **Returns**: Model-ready input with title, body, and word count.
    """
    try:
        processed_input = await process_text_for_analysis(payload)
        return processed_input
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@router.post(
    "/process-image",
    response_model=ModelInput,
    summary="Process an Image (OCR)",
    description="Upload an image file, extracts text using OCR, cleans it, summarizes using TF-IDF, and returns model-ready input."
)
async def process_image(file: UploadFile = File(...)):
    """
    This endpoint accepts an image file (`jpeg`, `png`, etc.) for OCR processing.
    - **Extracts**: Uses Tesseract OCR to get raw text from the image.
    - **Validates & Cleans**: The extracted text is processed by the same pipeline.
    - **Summarizes**: Uses TF-IDF to extract key sentences.
    - **Truncates**: Limits body to 500 words maximum.
    - **Returns**: Model-ready input with title, body, and word count.
    """
    try:
        processed_input = await process_image_for_analysis(file)
        return processed_input
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
