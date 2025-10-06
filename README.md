# Fake News Detection API

🔍 **A production-ready REST API for detecting fake news using AI and evidence-based verification.**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### 2. Run the Server

```bash
# From project root
python3 -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Test the API

Open your browser: **http://localhost:8000/docs**

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/api/v1/process-url` | Analyze news article URL |
| POST | `/api/v1/process-text` | Analyze raw text |
| POST | `/api/v1/process-image` | OCR and analyze image |

### Example Request

```bash
curl -X POST "http://localhost:8000/api/v1/process-text" \
  -H "Content-Type: application/json" \
  -d '{"text": "Your news article text here..."}'
```

### Example Response

```json
{
  "evidence_analysis": {
    "verdict": "FAKE",
    "confidence_value": 85,
    "explanation": "Detected sensational language and lack of credible sources...",
    "evidence": {
      "sources": [
        {
          "url": "https://snopes.com/...",
          "title": "Fact Check",
          "snippet": "...",
          "similarity": "High"
        }
      ]
    }
  }
}
```

---

## 🎯 Features

- ✅ **URL Analysis** - Scrape and analyze news articles
- ✅ **Text Analysis** - Direct text verification
- ✅ **Image OCR** - Extract and analyze text from images
- ✅ **ML Detection** - Trained model + heuristic fallback
- ✅ **Evidence Gathering** - Web-based source verification
- ✅ **Confidence Scoring** - 50-95% reliability scores
- ✅ **Detailed Explanations** - Human-readable reasoning
- ✅ **CORS Enabled** - Ready for client integration
- ✅ **Auto Documentation** - Interactive Swagger UI

---

## 📚 Documentation

- **Full API Documentation**: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- **Interactive Docs**: http://localhost:8000/docs (when server is running)
- **ReDoc**: http://localhost:8000/redoc

---

## 🏗️ Project Structure

```
backend/
├── main.py              # FastAPI application entry point
├── routes/              # API endpoints
│   ├── detect.py       # Main detection endpoints
│   ├── feedback.py     # User feedback
│   └── sources.py      # Evidence sources
├── core/               # Core logic
│   ├── inference.py    # ML model inference
│   ├── verdict_logic.py # Verdict determination
│   ├── explainability.py # Explanation generation
│   └── evidence_agent.py # Web evidence gathering
├── services/           # Utility services
│   ├── web_scraper.py  # URL content extraction
│   ├── ocr_service.py  # Image text extraction
│   └── text_processor.py # TF-IDF summarization
└── models/             # Pydantic data models
    ├── detection_models.py
    └── response_models.py
```

---

## 🧪 Testing

```bash
# Test with fake news indicators
curl -X POST "http://localhost:8000/api/v1/process-text" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "BREAKING: Shocking discovery! Doctors dont want you to know this one weird trick that changes everything! You wont believe what scientists found!"
  }'

# Expected: Verdict = FAKE, Confidence ~70-85%
```

---

## 🔧 Configuration

### Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- NLTK
- scikit-learn
- Tesseract OCR (for image processing)

### Install Tesseract

```bash
# macOS
brew install tesseract

# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# Windows
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
```

---

## 🌐 Deployment

### Docker

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
COPY backend ./backend
EXPOSE 8000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Settings

Update `backend/main.py`:

```python
# Specify allowed origins
allow_origins=["https://yourdomain.com"]
```

---

## 📊 How It Works

```
Input → Content Extraction → Text Cleaning → 
ML Analysis → Evidence Gathering → 
Confidence Adjustment → Explanation → Result
```

### Detection Logic

**Fake News Indicators:**
- Sensational language ("shocking", "breaking", "you won't believe")
- Lack of credible sources
- Clickbait patterns
- Emotional manipulation

**Credibility Indicators:**
- Academic citations ("study", "research", "university")
- Professional tone
- Source attribution
- Verifiable claims

---

## 🛠️ Development

### Setup Development Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

### Run in Development Mode

```bash
python3 -m uvicorn backend.main:app --reload
```

### Add New Endpoints

1. Create route in `backend/routes/`
2. Add logic in `backend/core/`
3. Include router in `backend/main.py`

---

## 🔒 Security

- ✅ Input validation via Pydantic
- ✅ CORS configuration
- ✅ Error handling
- ⚠️ Add rate limiting for production
- ⚠️ Add authentication for sensitive operations
- ⚠️ Use HTTPS in production

---

## 📝 License

MIT License - feel free to use for your projects!

---

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

---

## 📧 Support

- **Documentation**: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- **Issues**: GitHub Issues
- **Email**: [Your Email]

---

## 🎯 Roadmap

- [ ] Real ML model integration
- [ ] Live web search API
- [ ] User authentication
- [ ] Rate limiting
- [ ] Analytics dashboard
- [ ] Batch processing
- [ ] Webhook notifications

---

**Made with ❤️ using FastAPI**
