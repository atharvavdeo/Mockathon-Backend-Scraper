"""Utility functions for data cleaning and validation."""

import re
import logging
from langdetect import detect, LangDetectException
from ..models.detection_models import ScrapedArticle


def _clean_text(text: str) -> str:
    """A helper function to remove noise from text."""
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)  # Collapse whitespace
    text = re.sub(r'[^A-Za-z0-9.,;!?\'"()$%\s]+', '', text)  # Remove strange characters
    return text.strip()


def clean_and_validate_article(article: ScrapedArticle) -> ScrapedArticle:
    """
    Cleans the text of a scraped article and validates its content.

    - Ensures the language is English.
    - Removes extra whitespace and non-standard characters.
    - Checks if the article body meets a minimum word count.

    Args:
        article: The ScrapedArticle object to clean.

    Returns:
        The cleaned ScrapedArticle object.

    Raises:
        ValueError: If the article fails validation checks.
    """
    # 1. Clean title and body
    cleaned_title = _clean_text(article.title or "")
    cleaned_body = _clean_text(article.body)

    if not cleaned_body:
        raise ValueError("Article body is empty after cleaning.")

    # 2. Validate language
    try:
        if detect(cleaned_body) != "en":
            raise ValueError("Article is not in English.")
    except LangDetectException:
        raise ValueError("Language could not be detected for the article.")

    # 3. Validate content length
    if len(cleaned_body.split()) < 50:  # Minimum 50 words
        raise ValueError("Article content is too short to be reliable for analysis.")

    article.title = cleaned_title
    article.body = cleaned_body
    
    return article


def clean_and_validate_text(text: str) -> str:
    """
    Cleans a raw string and validates its content.

    - Ensures the language is English.
    - Removes extra whitespace and non-standard characters.
    - Checks if the text meets a minimum word count.

    Args:
        text: The raw string to clean and validate.

    Returns:
        The cleaned text.

    Raises:
        ValueError: If the text fails any validation check.
    """
    if not text:
        raise ValueError("Input text cannot be empty.")

    # 1. Clean text using the existing helper
    cleaned_text = _clean_text(text)
    if not cleaned_text:
        raise ValueError("Text is empty after cleaning.")

    # 2. Validate language
    try:
        if detect(cleaned_text) != "en":
            raise ValueError("Text is not in English.")
    except LangDetectException:
        # This can happen on very short or ambiguous text
        raise ValueError("Language could not be reliably detected.")

    # 3. Validate content length
    MINIMUM_WORD_COUNT = 50
    if len(cleaned_text.split()) < MINIMUM_WORD_COUNT:
        raise ValueError(f"Text content is too short. Minimum {MINIMUM_WORD_COUNT} words required.")

    return cleaned_text

