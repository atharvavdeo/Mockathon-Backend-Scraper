/**
 * API Service for Fake News Detection Backend
 * Base URL: Configured via environment variable
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export interface ProcessedInput {
  title: string;
  body: string;
  image_text: string | null;
  source_url: string | null;
  word_count: number;
}

export interface EvidenceSource {
  url: string;
  title: string;
  snippet: string;
  similarity: 'High' | 'Medium' | 'Low';
}

export interface EvidenceAnalysis {
  verdict: 'FAKE' | 'REAL' | 'UNCERTAIN';
  confidence_value: number;
  explanation: string;
  evidence: {
    sources: EvidenceSource[];
  };
  warning_signals: string[];
  extracted_topics: string[];
}

export interface CompleteAnalysisResponse {
  processed_input: ProcessedInput;
  evidence_analysis: EvidenceAnalysis;
}

/**
 * Analyze raw text for fake news detection
 * @param text - Article text (minimum 100 characters)
 * @returns Complete analysis with verdict, confidence, explanation, and evidence
 */
export const analyzeText = async (text: string): Promise<CompleteAnalysisResponse> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/process-text`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error analyzing text:', error);
    throw error;
  }
};

/**
 * Analyze article from URL (scrapes and analyzes)
 * @param url - Article URL
 * @returns Complete analysis with verdict, confidence, explanation, and evidence
 */
export const analyzeURL = async (url: string): Promise<CompleteAnalysisResponse> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/process-url`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error analyzing URL:', error);
    throw error;
  }
};

/**
 * Analyze image (OCR extraction and analysis)
 * @param imageFile - Image file (PNG, JPG, etc.)
 * @returns Complete analysis with verdict, confidence, explanation, and evidence
 */
export const analyzeImage = async (imageFile: File): Promise<CompleteAnalysisResponse> => {
  try {
    const formData = new FormData();
    formData.append('file', imageFile);

    const response = await fetch(`${API_BASE_URL}/api/v1/process-image`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error analyzing image:', error);
    throw error;
  }
};

/**
 * Submit user feedback
 * @param feedback - Feedback text
 * @param rating - Rating (1-5)
 */
export const submitFeedback = async (feedback: string, rating: number): Promise<any> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/feedback`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ feedback, rating }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error submitting feedback:', error);
    throw error;
  }
};

/**
 * Get evidence sources for a query
 * @param query - Search query
 */
export const getEvidenceSources = async (query: string): Promise<any> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/sources?query=${encodeURIComponent(query)}`, {
      method: 'GET',
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error getting evidence sources:', error);
    throw error;
  }
};
