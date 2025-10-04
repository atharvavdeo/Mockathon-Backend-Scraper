"""Handles and sanitizes user input before processing."""

from pydantic import BaseModel
from fastapi import UploadFile
import validators
from ..models.detection_models import URLInput, ScrapedArticle, TextInput, ProcessedText, ModelInput
from ..services.web_scraper import scrape_article_content
from ..services.utils import clean_and_validate_text, clean_and_validate_article
from ..services.ocr_service import extract_text_from_image
from ..services.text_processor import extract_key_sentences_and_truncate


async def process_url_for_analysis(payload: URLInput) -> ModelInput:
    """
    Orchestrates the full pipeline for a URL:
    Scrape -> Clean -> Extract Key Sentences -> Prepare for Model
    """
    url = str(payload.url)
    if not validators.url(url):
        raise ValueError("Invalid URL format provided.")

    scraped_article = scrape_article_content(url)
    validated_article = clean_and_validate_article(scraped_article)

    # Call the TF-IDF processor
    processed_data = extract_key_sentences_and_truncate(
        validated_article.title or "Untitled",
        validated_article.body
    )

    return ModelInput(
        **processed_data,
        source_url=str(validated_article.url)
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
