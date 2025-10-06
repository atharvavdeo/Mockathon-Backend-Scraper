"""Generates explanations for the model's verdict."""

from typing import List, Dict

def generate_explanation(verdict: str, confidence: int, evidence: List[Dict], content_analysis: Dict = None) -> str:
    """
    Generate human-readable explanation for the verdict.
    
    Args:
        verdict: "FAKE", "REAL", or "UNCERTAIN"
        confidence: Confidence percentage (0-100)
        evidence: List of evidence sources
        content_analysis: Optional dict with analysis details
        
    Returns:
        Explanation string
    """
    explanations = []
    
    # Base explanation
    if verdict == "FAKE":
        explanations.append(f"This content has been classified as FAKE NEWS with {confidence}% confidence.")
        explanations.append("Several factors contributed to this verdict:")
        
        if evidence:
            explanations.append(f"• {len(evidence)} external sources contradict or question this content")
        
        if content_analysis:
            if content_analysis.get('sensational_language'):
                explanations.append("• The text uses sensational language commonly found in misinformation")
            if content_analysis.get('lacks_sources'):
                explanations.append("• The article lacks credible source citations")
            if content_analysis.get('clickbait_title'):
                explanations.append("• The headline shows signs of clickbait tactics")
        
        explanations.append("\nRecommendation: Cross-check with reputable news sources before sharing.")
        
    elif verdict == "REAL":
        explanations.append(f"This content appears to be LEGITIMATE with {confidence}% confidence.")
        explanations.append("Supporting factors:")
        
        if evidence:
            explanations.append(f"• {len(evidence)} credible sources corroborate this information")
        
        if content_analysis:
            if content_analysis.get('has_sources'):
                explanations.append("• The article cites verifiable sources")
            if content_analysis.get('professional_tone'):
                explanations.append("• The writing follows journalistic standards")
        
        explanations.append("\nNote: While this appears legitimate, always verify important claims independently.")
        
    else:  # UNCERTAIN
        explanations.append(f"The authenticity of this content is UNCERTAIN (confidence: {confidence}%).")
        explanations.append("Reasons for uncertainty:")
        explanations.append("• Limited evidence available for verification")
        explanations.append("• Content may be opinion or satire rather than factual news")
        explanations.append("• Mixed signals from content analysis")
        explanations.append("\nRecommendation: Seek additional sources before drawing conclusions.")
    
    return "\n".join(explanations)

def analyze_content_features(title: str, body: str) -> Dict:
    """
    Analyze content for common fake news indicators.
    
    Returns dict with boolean flags for different features.
    """
    text = f"{title} {body}".lower()
    
    # Sensational language
    sensational_words = ['shocking', 'unbelievable', 'exposed', 'revealed', 'breaking', 'urgent']
    sensational_count = sum(1 for word in sensational_words if word in text)
    
    # Source citations
    source_indicators = ['according to', 'study', 'research', 'published', 'reported']
    has_sources = any(indicator in text for indicator in source_indicators)
    
    # Professional tone
    professional_indicators = ['however', 'therefore', 'analysis', 'data']
    professional_count = sum(1 for word in professional_indicators if word in text)
    
    return {
        'sensational_language': sensational_count >= 2,
        'lacks_sources': not has_sources,
        'clickbait_title': sensational_count >= 1 and len(title) > 80,
        'has_sources': has_sources,
        'professional_tone': professional_count >= 2
    }


def extract_warning_signals(verdict: str, confidence: int, content_analysis: Dict, evidence_count: int) -> List[str]:
    """
    Extract specific warning signals from the analysis.
    
    Args:
        verdict: The verdict (FAKE/REAL/UNCERTAIN)
        confidence: Confidence percentage
        content_analysis: Content analysis dictionary
        evidence_count: Number of evidence sources
        
    Returns:
        List of warning signal strings
    """
    signals = []
    
    if verdict == "FAKE":
        if content_analysis.get('sensational_language'):
            signals.append("Highly emotional language detected")
        if content_analysis.get('lacks_sources'):
            signals.append("Multiple unverified claims")
        if content_analysis.get('clickbait_title'):
            signals.append("Clickbait headline patterns")
        if evidence_count > 0:
            signals.append(f"{evidence_count} sources contradict this content")
        if confidence >= 80:
            signals.append("Strong indicators of misinformation")
        if not signals:
            signals.append("Questionable source credibility")
            
    elif verdict == "REAL":
        if content_analysis.get('has_sources'):
            signals.append("Credible source citations present")
        if content_analysis.get('professional_tone'):
            signals.append("Professional journalistic standards")
        if evidence_count > 0:
            signals.append(f"{evidence_count} sources corroborate information")
        if confidence >= 80:
            signals.append("Strong authenticity indicators")
        if not signals:
            signals.append("Content follows factual reporting patterns")
            
    else:  # UNCERTAIN
        signals.append("Limited evidence for verification")
        signals.append("Content may be opinion or satire")
        if content_analysis.get('sensational_language'):
            signals.append("Mixed signals in language analysis")
        else:
            signals.append("Ambiguous credibility indicators")
    
    return signals


def extract_topics(title: str, body: str) -> List[str]:
    """
    Extract main topics/categories from the content.
    
    Args:
        title: Article title
        body: Article body text
        
    Returns:
        List of identified topics
    """
    text = f"{title} {body}".lower()
    topics = []
    
    # Define topic keywords
    topic_keywords = {
        'Politics': ['election', 'government', 'president', 'minister', 'parliament', 'senate', 'congress', 'vote', 'policy', 'democrat', 'republican', 'politician'],
        'Health': ['health', 'medical', 'doctor', 'hospital', 'disease', 'virus', 'vaccine', 'treatment', 'patient', 'covid', 'pandemic', 'medicine'],
        'Technology': ['technology', 'tech', 'ai', 'artificial intelligence', 'software', 'computer', 'internet', 'digital', 'app', 'smartphone', 'cyber'],
        'Science': ['science', 'research', 'study', 'scientist', 'discovery', 'experiment', 'climate', 'space', 'nasa', 'laboratory', 'scientific'],
        'Economy': ['economy', 'economic', 'finance', 'financial', 'market', 'stock', 'business', 'trade', 'gdp', 'inflation', 'recession'],
        'Sports': ['sports', 'game', 'player', 'team', 'football', 'cricket', 'basketball', 'match', 'championship', 'olympic', 'tournament'],
        'Entertainment': ['celebrity', 'movie', 'film', 'actor', 'music', 'singer', 'hollywood', 'entertainment', 'award', 'tv show'],
        'Environment': ['environment', 'climate change', 'pollution', 'green', 'sustainability', 'renewable', 'carbon', 'emissions', 'conservation'],
        'Education': ['education', 'school', 'university', 'student', 'teacher', 'college', 'academic', 'learning', 'exam'],
        'Crime': ['crime', 'criminal', 'police', 'arrest', 'investigation', 'murder', 'theft', 'fraud', 'court', 'lawsuit']
    }
    
    # Check for each topic
    for topic, keywords in topic_keywords.items():
        matches = sum(1 for keyword in keywords if keyword in text)
        if matches >= 2:  # Require at least 2 keyword matches
            topics.append(topic)
    
    # If no topics found, return default
    if not topics:
        topics.append('General News')
    
    return topics[:5]  # Return max 5 topics

