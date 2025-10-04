"""Service for extractive text summarization using TF-IDF."""

import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from ..config.settings import settings


def extract_key_sentences_and_truncate(title: str, body: str) -> dict:
    """
    Extracts the most important sentences from the body using TF-IDF scoring,
    then truncates the result to fit within the configured word limit.

    This is a lightweight, classical NLP approach that:
    1. Tokenizes the body into sentences
    2. Calculates TF-IDF scores for each sentence
    3. Selects the top N sentences (based on settings.NUM_SUMMARY_SENTENCES)
    4. Reorders them to maintain original flow
    5. Truncates to settings.MAX_BODY_WORDS if needed

    Args:
        title: The article title
        body: The cleaned article body text

    Returns:
        A dictionary with:
            - title: str (cleaned title)
            - body: str (summarized and truncated body)
            - word_count: int (number of words in final body)
    """
    # Clean the title
    cleaned_title = title.strip()
    if not cleaned_title:
        cleaned_title = "Untitled"

    # If body is empty, return minimal result
    if not body or len(body.strip()) < 50:
        return {
            "title": cleaned_title,
            "body": body.strip() if body else "",
            "word_count": len(body.split()) if body else 0
        }

    # Step 1: Tokenize body into sentences
    try:
        sentences = sent_tokenize(body)
    except Exception as e:
        print(f"Sentence tokenization failed: {e}. Falling back to simple split.")
        sentences = [s.strip() + '.' for s in body.split('.') if s.strip()]

    # If there are very few sentences, just truncate by words
    if len(sentences) <= settings.NUM_SUMMARY_SENTENCES:
        truncated_body = _truncate_to_word_limit(body, settings.MAX_BODY_WORDS)
        return {
            "title": cleaned_title,
            "body": truncated_body,
            "word_count": len(truncated_body.split())
        }

    # Step 2: Calculate TF-IDF scores for each sentence
    try:
        # Get English stopwords
        stop_words = set(stopwords.words('english'))
        
        # Create TF-IDF vectorizer
        vectorizer = TfidfVectorizer(
            stop_words=list(stop_words),
            max_features=1000,
            ngram_range=(1, 2)
        )
        
        # Fit and transform sentences
        tfidf_matrix = vectorizer.fit_transform(sentences)
        
        # Calculate sentence scores (sum of TF-IDF values for all words in sentence)
        sentence_scores = tfidf_matrix.sum(axis=1).A1
        
    except Exception as e:
        print(f"TF-IDF calculation failed: {e}. Using simple sentence extraction.")
        # Fallback: just take first N sentences
        summary_sentences = sentences[:settings.NUM_SUMMARY_SENTENCES]
        summary_body = ' '.join(summary_sentences)
        truncated_body = _truncate_to_word_limit(summary_body, settings.MAX_BODY_WORDS)
        return {
            "title": cleaned_title,
            "body": truncated_body,
            "word_count": len(truncated_body.split())
        }

    # Step 3: Select top N sentences by score
    num_sentences_to_extract = min(settings.NUM_SUMMARY_SENTENCES, len(sentences))
    
    # Get indices of top-scoring sentences
    top_sentence_indices = sentence_scores.argsort()[-num_sentences_to_extract:][::-1]
    
    # Step 4: Sort indices to maintain original order
    top_sentence_indices_sorted = sorted(top_sentence_indices)
    
    # Extract the selected sentences in original order
    summary_sentences = [sentences[i] for i in top_sentence_indices_sorted]
    summary_body = ' '.join(summary_sentences)
    
    # Step 5: Apply final word-based truncation if needed
    truncated_body = _truncate_to_word_limit(summary_body, settings.MAX_BODY_WORDS)
    
    return {
        "title": cleaned_title,
        "body": truncated_body,
        "word_count": len(truncated_body.split())
    }


def _truncate_to_word_limit(text: str, max_words: int) -> str:
    """
    Truncates text to a maximum number of words.

    Args:
        text: The text to truncate
        max_words: Maximum number of words to keep

    Returns:
        The truncated text
    """
    words = text.split()
    if len(words) <= max_words:
        return text
    
    # Truncate and add ellipsis
    truncated = ' '.join(words[:max_words])
    
    # Try to end on a sentence boundary
    if '.' in truncated:
        # Find the last period and truncate there
        last_period = truncated.rfind('.')
        if last_period > len(truncated) * 0.7:  # Only if it's not too far back
            truncated = truncated[:last_period + 1]
    else:
        # No period found, just add ellipsis
        truncated += '...'
    
    return truncated
