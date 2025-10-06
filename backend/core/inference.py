"""Performs inference using the pre-trained fake news detection model."""

import joblib
import os
import numpy as np
from typing import Tuple

# Path to the model file
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model", "model.pkl")

def load_model():
    """Load the pre-trained model."""
    if os.path.exists(MODEL_PATH):
        try:
            return joblib.load(MODEL_PATH)
        except Exception as e:
            print(f"Error loading model: {e}")
            return None
    return None

def predict_fake_news(title: str, body: str) -> Tuple[float, str]:
    """
    Predict if the news is fake or real.
    
    Args:
        title: Article title
        body: Article body text
        
    Returns:
        Tuple of (confidence_score, prediction)
        confidence_score: 0.0-1.0 reliability score (higher = more reliable)
        prediction: "REAL" or "FAKE"
    """
    model = load_model()
    
    # If model doesn't exist, use heuristic analysis
    if model is None:
        return heuristic_analysis(title, body)
    
    try:
        # Prepare input for model
        combined_text = f"{title} {body}"
        
        # Model prediction (assuming it returns probability)
        # You may need to adjust based on your actual model structure
        prediction = model.predict([combined_text])[0]
        proba = model.predict_proba([combined_text])[0]
        
        # Get confidence (probability of predicted class)
        confidence = float(max(proba))
        
        # Map prediction to label
        result = "REAL" if prediction == 1 else "FAKE"
        
        return confidence, result
        
    except Exception as e:
        print(f"Model prediction error: {e}")
        return heuristic_analysis(title, body)

def heuristic_analysis(title: str, body: str) -> Tuple[float, str]:
    """
    Fallback heuristic analysis when model is unavailable.
    Uses enhanced text analysis patterns.
    """
    text = f"{title} {body}".lower()
    title_lower = title.lower()
    
    # Enhanced fake news indicators
    fake_indicators = [
        'breaking', 'shocking', 'unbelievable', 'you won\'t believe',
        'must see', 'urgent', 'warning', 'exposed', 'revealed',
        'doctors hate', 'they don\'t want you to know', 'miracle',
        'secret', 'banned', 'censored', 'conspiracy', 'coverup',
        'explosive', 'bombshell', 'leaked', 'insider'
    ]
    
    # Enhanced credibility indicators
    credible_indicators = [
        'study', 'research', 'university', 'according to',
        'expert', 'professor', 'data shows', 'published',
        'journal', 'institute', 'analysis', 'report',
        'official', 'government', 'agency', 'department'
    ]
    
    # Check for URL patterns (trusted sources)
    trusted_domains = ['bbc', 'reuters', 'apnews', 'nytimes', 'theguardian', 
                      'washingtonpost', 'economist', 'npr', 'pbs']
    has_trusted_source = any(domain in text for domain in trusted_domains)
    
    # Calculate scores
    fake_score = sum(1 for indicator in fake_indicators if indicator in text)
    credible_score = sum(1 for indicator in credible_indicators if indicator in text)
    
    # Check for excessive punctuation (!!!, ???)
    excessive_punctuation = text.count('!!!') + text.count('???')
    if excessive_punctuation > 0:
        fake_score += excessive_punctuation
    
    # Check for ALL CAPS in title (common in clickbait)
    caps_words = sum(1 for word in title.split() if word.isupper() and len(word) > 2)
    if caps_words > 2:
        fake_score += 1
    
    # Adjust for trusted sources
    if has_trusted_source:
        credible_score += 2
    
    # Calculate confidence and prediction
    total_indicators = fake_score + credible_score
    
    if total_indicators == 0:
        # No strong indicators - lean slightly toward real for neutral content
        confidence = 0.65
        prediction = "REAL"
    elif fake_score > credible_score + 1:  # Clear fake signals
        confidence = min(0.60 + (fake_score * 0.05), 0.88)
        prediction = "FAKE"
    elif credible_score > fake_score + 1:  # Clear credibility signals
        confidence = min(0.65 + (credible_score * 0.05), 0.90)
        prediction = "REAL"
    else:  # Mixed signals
        confidence = 0.55 + (abs(credible_score - fake_score) * 0.02)
        prediction = "UNCERTAIN"
    
    return confidence, prediction
