"""Service for scraping web content."""

import requests
from bs4 import BeautifulSoup
from ..models.detection_models import ScrapedArticle
from ..config.settings import settings


def scrape_article_content(url: str) -> ScrapedArticle:
    """
    Scrapes article content from a given URL.
    
    Args:
        url: The URL of the article to scrape.
        
    Returns:
        A ScrapedArticle object with the scraped content.
        
    Raises:
        ValueError: If the URL cannot be accessed or parsed.
    """
    headers = {"User-Agent": settings.SCRAPER_USER_AGENT}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise ValueError(f"Failed to fetch URL: {e}")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract title
    title = soup.find('title')
    title_text = title.get_text().strip() if title else "No Title"
    
    # Extract body content (attempt to find article body)
    body_candidates = soup.find_all(['article', 'main', 'div'], class_=lambda x: x and ('content' in x.lower() or 'article' in x.lower()))
    
    if body_candidates:
        body_text = ' '.join([elem.get_text(separator=' ', strip=True) for elem in body_candidates])
    else:
        # Fallback to all paragraphs
        paragraphs = soup.find_all('p')
        body_text = ' '.join([p.get_text(separator=' ', strip=True) for p in paragraphs])
    
    if not body_text:
        raise ValueError("No content could be extracted from the URL.")
    
    # Extract metadata (basic example)
    author = None
    author_meta = soup.find('meta', attrs={'name': 'author'})
    if author_meta:
        author = author_meta.get('content')
    
    publish_date = None
    date_meta = soup.find('meta', attrs={'property': 'article:published_time'})
    if date_meta:
        publish_date = date_meta.get('content')
    
    return ScrapedArticle(
        url=url,
        title=title_text,
        body=body_text,
        author=author,
        publish_date=publish_date
    )

