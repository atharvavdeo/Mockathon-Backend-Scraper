"""Configuration settings for the application."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Manages application-wide settings."""
    
    # Web Scraper Settings
    SCRAPER_USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    
    # TF-IDF Extractive Summarizer Settings
    NUM_SUMMARY_SENTENCES: int = 5  # The target number of sentences for the summary
    MAX_BODY_WORDS: int = 500       # The absolute maximum word count for the final body text

    class Config:
        env_file = ".env"


settings = Settings()

# --- NLTK Data Download ---
# Download required NLTK data on first run
import nltk
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt_tab')
    nltk.data.find('corpora/stopwords')
except LookupError:
    print("Downloading required NLTK data (punkt, punkt_tab, stopwords)...")
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    nltk.download('stopwords', quiet=True)
    print("NLTK data downloaded successfully.")
