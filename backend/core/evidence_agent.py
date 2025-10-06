"""Manages the LLM-based web evidence search for uncertain results."""

import httpx
from typing import List, Dict
from bs4 import BeautifulSoup
import asyncio

async def search_web_evidence(title: str, body: str, max_sources: int = 5) -> List[Dict]:
    """
    Search the web for evidence about the claim.
    
    Args:
        title: Article title
        body: Article body (first 200 chars used for search)
        max_sources: Maximum number of sources to return
        
    Returns:
        List of evidence dictionaries with url, title, snippet
    """
    # Mock implementation - in production, integrate with Google Custom Search API or similar
    evidence_sources = []
    
    # Extract key terms for search
    search_query = title[:100]  # Use title as search query
    
    try:
        # Simulate web search (in production, use actual search API)
        # For now, return mock credible sources
        mock_sources = [
            {
                "url": "https://www.snopes.com",
                "title": "Fact Check: " + title[:50],
                "snippet": "According to fact-checkers, this claim has been verified through multiple sources...",
                "similarity": "High"
            },
            {
                "url": "https://www.factcheck.org",
                "title": "Analysis: " + title[:50],
                "snippet": "Our investigation found evidence supporting/refuting these claims...",
                "similarity": "Medium"
            },
            {
                "url": "https://apnews.com",
                "title": "AP News Coverage",
                "snippet": "Associated Press reporting indicates...",
                "similarity": "Medium"
            },
            {
                "url": "https://www.reuters.com",
                "title": "Reuters Fact Check",
                "snippet": "Reuters fact-checking team examined this story...",
                "similarity": "High"
            },
            {
                "url": "https://www.bbc.com/news",
                "title": "BBC Verification",
                "snippet": "BBC News verification unit reviewed the available evidence...",
                "similarity": "Medium"
            }
        ]
        
        evidence_sources = mock_sources[:max_sources]
        
    except Exception as e:
        print(f"Error searching for evidence: {e}")
    
    return evidence_sources

def calculate_evidence_agreement(evidence: List[Dict], predicted_verdict: str) -> float:
    """
    Calculate how much evidence agrees with the predicted verdict.
    
    Args:
        evidence: List of evidence sources
        predicted_verdict: \"FAKE\", \"REAL\", or \"UNCERTAIN\"
        
    Returns:
        Agreement score 0.0-1.0
    """
    if not evidence:
        return 0.5  # Neutral when no evidence
    
    # Analyze evidence snippets and similarity scores
    high_similarity_count = sum(1 for e in evidence if e.get('similarity') == 'High')
    total_count = len(evidence)
    
    # Calculate agreement based on similarity and verdict
    if predicted_verdict == "FAKE":
        # If predicting fake, high similarity means contradicting sources
        agreement = 0.3 + (high_similarity_count / total_count) * 0.5
    elif predicted_verdict == "REAL":
        # If predicting real, high similarity means supporting sources
        agreement = 0.5 + (high_similarity_count / total_count) * 0.4
    else:  # UNCERTAIN
        # Mixed evidence for uncertain
        agreement = 0.5 + ((high_similarity_count % 2) * 0.1)
    
    return min(agreement, 0.9)

