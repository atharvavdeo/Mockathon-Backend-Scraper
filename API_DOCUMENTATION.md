# Fake News Detection API

A standalone REST API for detecting fake news using machine learning, natural language processing, and evidence-based verification.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd Mockathon-HackiOps
```

2. **Create and activate virtual environment**
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
cd backend
pip install -r requirements.txt
```

4. **Download NLTK data** (required for text processing)
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### Running the Server

From the project root directory:

```bash
python3 -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API Base URL**: `http://localhost:8000`
- **Interactive Docs**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## 📡 API Endpoints

### 1. Health Check

**GET /** 

Check if the API is running.

**Response:**
```json
{
  "message": "Welcome to the Fake-News Detection API",
  "endpoints": {
    "process_url": "/api/v1/process-url",
    "process_text": "/api/v1/process-text",
    "process_image": "/api/v1/process-image",
    "feedback": "/api/v1/feedback",
    "sources": "/api/v1/sources"
  }
}
```

---

### 2. Analyze URL

**POST /api/v1/process-url**

Scrape and analyze a news article from a URL.

**Request Body:**
```json
{
  "url": "https://example.com/news-article"
}
```

**Response:**
```json
{
  "processed_input": {
    "title": "Article Title",
    "body": "Processed article content...",
    "source_url": "https://example.com/news-article",
    "word_count": 250
  },
  "evidence_analysis": {
    "verdict": "FAKE",
    "confidence_value": 85,
    "explanation": "This content has been classified as FAKE NEWS with 85% confidence...",
    "evidence": {
      "sources": [
        {
          "url": "https://snopes.com/fact-check/...",
          "title": "Fact Check: Article Title",
          "snippet": "According to fact-checkers...",
          "similarity": "High"
        }
      ]
    }
  }
}
```

**Error Responses:**
- `400 Bad Request` - Invalid URL format
- `500 Internal Server Error` - Processing failed

---

### 3. Analyze Text

**POST /api/v1/process-text**

Analyze raw text content for fake news.

**Request Body:**
```json
{
  "text": "Your news article text here (minimum 100 characters)..."
}
```

**Response:**
```json
{
  "processed_input": {
    "title": "Generated Title",
    "body": "Processed text content...",
    "word_count": 180
  },
  "evidence_analysis": {
    "verdict": "REAL",
    "confidence_value": 75,
    "explanation": "This content appears to be LEGITIMATE with 75% confidence...",
    "evidence": {
      "sources": [...]
    }
  }
}
```

**Validation:**
- Minimum 100 characters required
- Must be in English
- Special characters are cleaned automatically

**Error Responses:**
- `400 Bad Request` - Text too short or invalid
- `500 Internal Server Error` - Processing failed

---

### 4. Analyze Image (OCR)

**POST /api/v1/process-image**

Extract text from an image and analyze it for fake news.

**Request:**
- Content-Type: `multipart/form-data`
- Field name: `file`
- Accepted formats: JPG, PNG, JPEG

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/process-image" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@screenshot.png"
```

**Response:**
```json
{
  "processed_input": {
    "title": "Extracted Title",
    "body": "Extracted and processed text...",
    "image_text": "Raw OCR extracted text...",
    "word_count": 150
  },
  "evidence_analysis": {
    "verdict": "UNCERTAIN",
    "confidence_value": 60,
    "explanation": "The authenticity of this content is UNCERTAIN...",
    "evidence": {
      "sources": [...]
    }
  }
}
```

**Error Responses:**
- `400 Bad Request` - Invalid file format or unreadable image
- `500 Internal Server Error` - OCR or processing failed

---

### 5. Submit Feedback

**GET /api/v1/feedback**

Submit user feedback (placeholder endpoint).

**Response:**
```json
{
  "message": "Feedback endpoint - To be implemented"
}
```

---

### 6. Get Sources

**GET /api/v1/sources**

Retrieve evidence sources (placeholder endpoint).

**Response:**
```json
{
  "message": "Sources endpoint - To be implemented"
}
```

---

## 📊 Response Schema

### Verdict Values
- `FAKE` - Content is likely false/misleading
- `REAL` - Content appears legitimate
- `UNCERTAIN` - Unable to determine with confidence

### Confidence Value
- Range: `50-95` (percentage)
- Higher values indicate stronger confidence in the verdict

### Evidence Sources
Each source includes:
- `url` - Link to verification source
- `title` - Source title
- `snippet` - Relevant excerpt
- `similarity` - Match level (High/Medium/Low)

---

## 🧪 Testing the API

### Using cURL

**Test URL Analysis:**
```bash
curl -X POST "http://localhost:8000/api/v1/process-url" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.bbc.com/news/world"}'
```

**Test Text Analysis:**
```bash
curl -X POST "http://localhost:8000/api/v1/process-text" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "BREAKING: Scientists discover shocking truth! You wont believe what they found. Doctors dont want you to know this one weird trick that changes everything!"
  }'
```

**Test Image Analysis:**
```bash
curl -X POST "http://localhost:8000/api/v1/process-image" \
  -F "file=@path/to/image.png"
```

### Using Python

```python
import requests

# Text analysis example
response = requests.post(
    "http://localhost:8000/api/v1/process-text",
    json={"text": "Your news article text here..."}
)

result = response.json()
print(f"Verdict: {result['evidence_analysis']['verdict']}")
print(f"Confidence: {result['evidence_analysis']['confidence_value']}%")
print(f"Explanation: {result['evidence_analysis']['explanation']}")
```

### Using JavaScript (Node.js)

```javascript
const fetch = require('node-fetch');

async function analyzeText(text) {
  const response = await fetch('http://localhost:8000/api/v1/process-text', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text })
  });
  
  const result = await response.json();
  console.log(`Verdict: ${result.evidence_analysis.verdict}`);
  console.log(`Confidence: ${result.evidence_analysis.confidence_value}%`);
}

analyzeText('Your news article text...');
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Server Configuration
HOST=0.0.0.0
PORT=8000

# NLTK Configuration
MAX_WORD_COUNT=500
MIN_TEXT_LENGTH=100

# OCR Configuration (Tesseract)
TESSERACT_CMD=/usr/bin/tesseract  # Adjust for your system
```

### CORS Settings

Update `backend/main.py` to specify allowed origins:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specify your domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🏗️ Architecture

### Pipeline Flow

```
Input (URL/Text/Image)
    ↓
Content Extraction & Cleaning
    ↓
Text Validation & Language Detection
    ↓
TF-IDF Summarization (Key Sentence Extraction)
    ↓
ML Model Inference (Fake/Real Prediction)
    ↓
Evidence Gathering (Web Search)
    ↓
Confidence Adjustment (Based on Evidence)
    ↓
Explanation Generation
    ↓
Final Response
```

### Key Components

- **Input Handler** (`core/input_handler.py`) - Processes and validates input
- **Web Scraper** (`services/web_scraper.py`) - Extracts content from URLs
- **OCR Service** (`services/ocr_service.py`) - Extracts text from images
- **Text Processor** (`services/text_processor.py`) - TF-IDF summarization
- **ML Inference** (`core/inference.py`) - Fake news prediction
- **Evidence Agent** (`core/evidence_agent.py`) - Gathers verification sources
- **Verdict Logic** (`core/verdict_logic.py`) - Determines final verdict
- **Explainability** (`core/explainability.py`) - Generates explanations

---

## 🐛 Troubleshooting

### Common Issues

**1. Import Error: No module named 'backend'**
```bash
# Run from project root, not backend directory
cd /path/to/Mockathon-HackiOps
python3 -m uvicorn backend.main:app --reload
```

**2. NLTK Data Not Found**
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

**3. Tesseract OCR Not Found**
```bash
# macOS
brew install tesseract

# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# Windows
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
```

**4. 422 Unprocessable Entity**
- Check request body format
- Ensure text is at least 100 characters
- Verify JSON is properly formatted

---

## 📚 API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These provide interactive documentation where you can:
- Test all endpoints directly from the browser
- View request/response schemas
- See example payloads
- Generate code snippets

---

## 🔒 Security Considerations

### For Production Deployment:

1. **Update CORS Origins**
   ```python
   allow_origins=["https://yourdomain.com"]
   ```

2. **Add Rate Limiting**
   ```bash
   pip install slowapi
   ```

3. **Enable HTTPS**
   - Use reverse proxy (Nginx, Caddy)
   - Configure SSL certificates

4. **Add Authentication**
   - API keys
   - OAuth2
   - JWT tokens

5. **Input Validation**
   - Already implemented via Pydantic models
   - Add additional sanitization if needed

6. **Monitoring & Logging**
   - Add structured logging
   - Monitor API usage
   - Track error rates

---

## 📦 Deployment

### Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

COPY backend ./backend

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t fake-news-api .
docker run -p 8000:8000 fake-news-api
```

### Cloud Deployment

**Heroku:**
```bash
heroku create fake-news-detection-api
git push heroku main
```

**AWS Lambda (with Mangum):**
```python
from mangum import Mangum
handler = Mangum(app)
```

**Google Cloud Run:**
```bash
gcloud run deploy fake-news-api --source .
```

---

## 📄 License

[Your License Here]

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📧 Support

For issues and questions:
- GitHub Issues: [Your Repo URL]
- Email: [Your Email]

---

**Version**: 1.0.0  
**Last Updated**: October 2025
