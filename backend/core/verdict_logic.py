"""Applies threshold-based logic to map reliability scores to verdicts."""

from typing import Tuple

def determine_verdict(confidence: float, prediction: str) -> Tuple[str, int]:
    """
    Convert model output to final verdict with confidence percentage.
    
    Args:
        confidence: 0.0-1.0 confidence score from model
        prediction: "REAL", "FAKE", or "UNCERTAIN"
        
    Returns:
        Tuple of (verdict, confidence_percentage)
    """
    # Convert to percentage
    confidence_pct = int(confidence * 100)
    
    # Apply thresholds
    if prediction == "UNCERTAIN" or confidence < 0.60:
        return "UNCERTAIN", max(50, confidence_pct)
    elif prediction == "FAKE":
        return "FAKE", confidence_pct
    else:
        return "REAL", confidence_pct

def adjust_confidence_with_evidence(base_confidence: int, evidence_count: int, evidence_agreement: float) -> int:
    """
    Adjust confidence based on external evidence.
    
    Args:
        base_confidence: Base confidence percentage (0-100)
        evidence_count: Number of evidence sources found
        evidence_agreement: 0.0-1.0 how much evidence agrees with verdict
        
    Returns:
        Adjusted confidence percentage
    """
    if evidence_count == 0:
        return base_confidence
    
    # Boost or reduce confidence based on evidence
    evidence_boost = int(evidence_agreement * 10)  # Up to 10% adjustment
    adjusted = base_confidence + evidence_boost
    
    # Cap between 50-95%
    return max(50, min(95, adjusted))

