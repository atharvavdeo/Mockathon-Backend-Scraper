"""API endpoints for news content detection."""

from fastapi import APIRouter, HTTPException, Body, File, UploadFile
# Use relative imports when running as a package
from ..core.input_handler import (
    process_url_for_analysis, 
    process_text_for_analysis, 
    process_image_for_analysis
)
from ..models.detection_models import URLInput, ModelInput, TextInput
from ..models.response_models import CompleteAnalysisResponse, ProcessedInput, EvidenceAnalysis, Evidence, EvidenceSource
from ..core.inference import predict_fake_news
from ..core.verdict_logic import determine_verdict, adjust_confidence_with_evidence
from ..core.explainability import generate_explanation, analyze_content_features, extract_warning_signals, extract_topics
from ..core.evidence_agent import search_web_evidence, calculate_evidence_agreement
import json
import os
from datetime import datetime

router = APIRouter()

async def perform_complete_analysis(model_input: ModelInput) -> CompleteAnalysisResponse:
    """
    Perform complete fake news analysis including ML inference and evidence gathering.
    
    Args:
        model_input: Processed and cleaned input ready for analysis
        
    Returns:
        Complete analysis with verdict, confidence, explanation, and evidence
    """
    # Step 1: ML Model Prediction
    confidence_score, prediction = predict_fake_news(model_input.title, model_input.body)
    
    # Step 2: Determine base verdict
    verdict, confidence_pct = determine_verdict(confidence_score, prediction)
    
    # Step 3: Gather web evidence
    evidence_sources = await search_web_evidence(model_input.title, model_input.body)
    
    # Step 4: Adjust confidence based on evidence
    evidence_agreement = calculate_evidence_agreement(evidence_sources, verdict)
    final_confidence = adjust_confidence_with_evidence(confidence_pct, len(evidence_sources), evidence_agreement)
    
    # Step 5: Analyze content features
    content_analysis = analyze_content_features(model_input.title, model_input.body)
    
    # Step 6: Extract warning signals and topics
    warning_signals = extract_warning_signals(verdict, final_confidence, content_analysis, len(evidence_sources))
    extracted_topics = extract_topics(model_input.title, model_input.body)
    
    # Step 7: Generate explanation
    explanation = generate_explanation(verdict, final_confidence, evidence_sources, content_analysis)
    
    # Step 8: Build response
    evidence_list = [
        EvidenceSource(
            url=src["url"],
            title=src["title"],
            snippet=src["snippet"],
            similarity=src.get("similarity")
        )
        for src in evidence_sources
    ]
    
    response = CompleteAnalysisResponse(
        processed_input=ProcessedInput(
            title=model_input.title,
            body=model_input.body,
            source_url=model_input.source_url,
            word_count=model_input.word_count
        ),
        evidence_analysis=EvidenceAnalysis(
            verdict=verdict,
            confidence_value=final_confidence,
            explanation=explanation,
            evidence=Evidence(sources=evidence_list),
            warning_signals=warning_signals,
            extracted_topics=extracted_topics
        )
    )
    
    # Step 9: Save to history JSON file
    save_analysis_to_history(response)
    
    return response


def save_analysis_to_history(response: CompleteAnalysisResponse):
    """
    Save analysis result to a JSON history file.
    
    Args:
        response: The complete analysis response to save
    """
    try:
        history_dir = "backend/analysis_history"
        os.makedirs(history_dir, exist_ok=True)
        
        history_file = os.path.join(history_dir, "analysis_history.json")
        
        # Load existing history
        if os.path.exists(history_file):
            with open(history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        else:
            history = {"analyses": []}
        
        # Create analysis entry
        analysis_entry = {
            "timestamp": datetime.now().isoformat(),
            "title": response.processed_input.title,
            "verdict": response.evidence_analysis.verdict,
            "confidence": response.evidence_analysis.confidence_value,
            "word_count": response.processed_input.word_count,
            "source_url": response.processed_input.source_url,
            "warning_signals": response.evidence_analysis.warning_signals,
            "topics": response.evidence_analysis.extracted_topics,
            "evidence_count": len(response.evidence_analysis.evidence.sources)
        }
        
        # Add to history
        history["analyses"].append(analysis_entry)
        
        # Keep only last 100 analyses
        if len(history["analyses"]) > 100:
            history["analyses"] = history["analyses"][-100:]
        
        # Save back to file
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
            
    except Exception as e:
        # Don't fail the request if history save fails
        print(f"Failed to save analysis history: {e}")

@router.post(
    "/process-url",
    response_model=CompleteAnalysisResponse,
    summary="Process and Analyze a News Article URL",
    description="Scrapes URL, analyzes content with ML model, gathers evidence, and returns complete verdict."
)
async def process_url(payload: URLInput = Body(...)):
    """
    Complete pipeline for URL analysis:
    - Scrapes and cleans content
    - Runs ML model for prediction
    - Gathers web evidence
    - Returns verdict with confidence and explanation
    """
    try:
        # Process input
        processed_input = await process_url_for_analysis(payload)
        
        # Perform complete analysis
        result = await perform_complete_analysis(processed_input)
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@router.post(
    "/process-text",
    response_model=CompleteAnalysisResponse,
    summary="Process and Analyze Raw Text",
    description="Analyzes text with ML model, gathers evidence, and returns complete verdict."
)
async def process_text(payload: TextInput = Body(...)):
    """
    Complete pipeline for text analysis:
    - Cleans and processes text
    - Runs ML model for prediction
    - Gathers web evidence
    - Returns verdict with confidence and explanation
    """
    try:
        # Process input
        processed_input = await process_text_for_analysis(payload)
        
        # Perform complete analysis
        result = await perform_complete_analysis(processed_input)
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@router.post(
    "/process-image",
    response_model=CompleteAnalysisResponse,
    summary="Process and Analyze Image (OCR)",
    description="Extracts text from image, analyzes with ML model, gathers evidence, and returns complete verdict."
)
async def process_image(file: UploadFile = File(...)):
    """
    Complete pipeline for image analysis:
    - Extracts text via OCR
    - Cleans and processes text
    - Runs ML model for prediction
    - Gathers web evidence
    - Returns verdict with confidence and explanation
    """
    try:
        # Process input
        processed_input = await process_image_for_analysis(file)
        
        # Add image_text field to response
        result = await perform_complete_analysis(processed_input)
        
        # Add OCR extracted text to response
        result.processed_input.image_text = processed_input.body[:200] + "..."
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
