"""Handles and sanitizes user input before processing."""

from pydantic import BaseModel
from fastapi import UploadFile
import validators
from ..models.detection_models import URLInput, ScrapedArticle, TextInput, ProcessedText, ModelInput
from ..services.web_scraper import scrape_article_content
from ..services.utils import clean_and_validate_text, clean_and_validate_article
from ..services.ocr_service import extract_text_from_image
from ..services.text_processor import extract_key_sentences_and_truncate


async def process_url_for_analysis(url_input: URLInput) -> ModelInput:
    """
    Process and validate a URL input for analysis.
    
    Args:
        url_input: URLInput containing the URL to process
        
    Returns:
        ModelInput ready for analysis
        
    Raises:
        ValueError: If URL is invalid or content cannot be extracted
    """
    url = url_input.url.strip()
    
    # Validate URL format
    if not url.startswith(('http://', 'https://')):
        raise ValueError("URL must start with http:// or https://")
    
    # Scrape article content
    scraped = scrape_article_content(url)
    
    # Clean and process the text
    cleaned = clean_and_validate_article(scraped)
    
    # Append source URL domain to body for analysis (helps with domain reputation)
    body_with_source = f"{cleaned.body} Source: {url}"
    
    # Calculate word count
    word_count = len(cleaned.body.split())
    
    # Validate minimum length
    if word_count < 50:
        raise ValueError("Article content is too short (minimum 50 characters)")
    
    return ModelInput(
        title=cleaned.title,
        body=body_with_source,
        source_url=url,
        word_count=word_count
    )


async def process_text_for_analysis(payload: TextInput) -> ModelInput:
    """
    Orchestrates the pipeline for direct text:
    Clean -> Extract Key Sentences -> Prepare for Model
    """
    original_text = payload.text
    cleaned_text = clean_and_validate_text(original_text)

    # Extract title from first sentence if possible
    sentences = cleaned_text.split('.')
    title = sentences[0] if len(sentences) > 1 and len(sentences[0]) < 100 else "User Submitted Text"
    body = '.'.join(sentences[1:]) if len(sentences) > 1 else cleaned_text

    # Call the TF-IDF processor
    processed_data = extract_key_sentences_and_truncate(title, body)
    
    return ModelInput(**processed_data)


async def process_image_for_analysis(file: UploadFile) -> ModelInput:
    """
    Orchestrates the full pipeline for an image:
    OCR -> Clean -> Extract Key Sentences -> Prepare for Model
    """
    if not file.content_type or not file.content_type.startswith("image/"):
        raise ValueError("Invalid file type. Please upload an image.")

    image_bytes = await file.read()
    if not image_bytes:
        raise ValueError("Image file is empty.")

    extracted_text = extract_text_from_image(image_bytes)
    cleaned_text = clean_and_validate_text(extracted_text)
    
    # Extract title from first sentence if possible
    sentences = cleaned_text.split('.')
    title = sentences[0] if len(sentences) > 1 and len(sentences[0]) < 100 else "Text from Image"
    body = '.'.join(sentences[1:]) if len(sentences) > 1 else cleaned_text

    # Call the TF-IDF processor
    processed_data = extract_key_sentences_and_truncate(title, body)

    return ModelInput(**processed_data)
