# Text Processing Pipeline with Summarization

## 🎯 Overview

The backend now includes a complete text processing pipeline that:
1. **Cleans** and validates input text
2. **Summarizes** long texts using BART model
3. **Truncates** to fit within 512-token limit
4. Returns **model-ready input** for Hugging Face inference

## 📦 New Components

### 1. Text Processor Service (`services/text_processor.py`)
Handles the summarization and tokenization pipeline using Hugging Face transformers.

**Key Features:**
- Lazy initialization of models (loaded only when first used)
- Token counting with BART tokenizer
- Automatic summarization for texts exceeding 512 tokens
- Fallback truncation if summary still exceeds limit

### 2. ModelInput Pydantic Model
New response model representing model-ready input:

```python
{
  "text": "The final, tokenized text (max 512 tokens)",
  "token_count": 487,
  "was_summarized": true,
  "was_truncated": false
}
```

### 3. Configuration Settings
Added to `config/settings.py`:
- `SUMMARIZATION_MODEL`: "facebook/bart-large-cnn"
- `MAX_INPUT_TOKENS`: 512
- `MAX_SUMMARY_LENGTH`: 150
- `MIN_SUMMARY_LENGTH`: 50

## 🚀 Installation

### Install New Dependencies

```bash
cd /Users/atharvadeo/Desktop/PROF/Hackies/Mockathon-HackiOps/backend
pip install transformers torch sentencepiece
```

**Note:** The first time you run the server and call an endpoint, the BART model (~1.6GB) will be downloaded automatically. This only happens once.

## 🔄 How It Works

### Processing Pipeline

```
Raw Input
    ↓
1. Clean & Validate (English, 50+ words)
    ↓
2. Count Tokens
    ↓
3. If > 512 tokens → Summarize with BART
    ↓
4. If still > 512 tokens → Truncate
    ↓
5. Return ModelInput (ready for HF model)
```

### Example Flow

**Input Text:** 2000 tokens of article content

**Step 1 - Cleaning:**
- Removes special characters
- Validates English language
- Checks minimum word count

**Step 2 - Summarization:**
- BART model generates concise summary
- Reduces to ~150 tokens (configurable)

**Step 3 - Verification:**
- Recounts tokens in summary
- If still > 512, applies hard truncation

**Step 4 - Output:**
```json
{
  "text": "Summarized and tokenized content...",
  "token_count": 148,
  "was_summarized": true,
  "was_truncated": false
}
```

## 📡 Updated API Endpoints

All three endpoints now return `ModelInput` instead of their previous models:

### 1. POST /api/v1/process-text

**Request:**
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/process-text" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your long article text here... (can be thousands of tokens)"
  }'
```

**Response:**
```json
{
  "text": "AI revolutionizes technology through machine learning...",
  "token_count": 142,
  "was_summarized": true,
  "was_truncated": false
}
```

### 2. POST /api/v1/process-image

**Request:**
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/process-image" \
  -F "file=@test_image.png"
```

**Response:**
```json
{
  "text": "OCR extracted and summarized text...",
  "token_count": 256,
  "was_summarized": false,
  "was_truncated": false
}
```

### 3. POST /api/v1/process-url

**Request:**
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/process-url" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/news-article"
  }'
```

**Response:**
```json
{
  "text": "Scraped article content, summarized and ready...",
  "token_count": 398,
  "was_summarized": true,
  "was_truncated": false
}
```

## 🧪 Testing

### 1. Start the Server

```bash
cd /Users/atharvadeo/Desktop/PROF/Hackies/Mockathon-HackiOps
uvicorn backend.main:app --reload --port 8000
```

**First time:** The BART model will download (1-2 minutes)

### 2. Test with Short Text (No Summarization)

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/process-text" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Artificial intelligence continues to transform industries worldwide. Machine learning models process vast amounts of data to identify patterns with remarkable accuracy. However, questions about ethics and privacy remain important for society to address."
  }'
```

**Expected:** `was_summarized: false` (text is already short)

### 3. Test with Long Text (Triggers Summarization)

Create a file `long_text.json`:
```json
{
  "text": "Paste a very long article here... (1000+ words)"
}
```

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/process-text" \
  -H "Content-Type: application/json" \
  -d @long_text.json
```

**Expected:** `was_summarized: true`, `token_count` <= 512

### 4. Test via Swagger UI

1. Go to http://127.0.0.1:8000/docs
2. Try `/api/v1/process-text`
3. Paste a long article
4. See the summarized output

## 📊 Understanding the Response

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `text` | string | The final processed text, ready for your model |
| `token_count` | integer | Number of tokens (will be ≤ 512) |
| `was_summarized` | boolean | `true` if BART summarization was applied |
| `was_truncated` | boolean | `true` if truncation was needed after summarization |

### Scenarios

**Scenario 1: Short Input**
- Input: 100 tokens
- Result: `was_summarized: false`, `was_truncated: false`
- Output: Original cleaned text

**Scenario 2: Long Input (Summarization Enough)**
- Input: 1000 tokens
- After summarization: 150 tokens
- Result: `was_summarized: true`, `was_truncated: false`
- Output: Summarized text

**Scenario 3: Very Long Input (Summarization + Truncation)**
- Input: 5000 tokens
- After summarization: 600 tokens (still too long)
- After truncation: 512 tokens
- Result: `was_summarized: true`, `was_truncated: true`
- Output: Summarized + truncated text

## 🔧 Configuration

You can adjust these settings in `backend/config/settings.py`:

```python
# Change the summarization model
SUMMARIZATION_MODEL = "facebook/bart-large-cnn"  # or "t5-small", "pegasus-xsum"

# Adjust token limits
MAX_INPUT_TOKENS = 512  # Your model's max context
MAX_SUMMARY_LENGTH = 150  # Target summary length
MIN_SUMMARY_LENGTH = 50  # Minimum summary length
```

## 🎯 Next Steps: Sending to Hugging Face Model

The `ModelInput` response is designed to be sent directly to your Hugging Face model:

```python
import requests

# Get processed input from your backend
response = requests.post(
    "http://127.0.0.1:8000/api/v1/process-text",
    json={"text": "Your article..."}
)
model_input = response.json()

# Send directly to Hugging Face inference
hf_response = requests.post(
    "https://api-inference.huggingface.co/models/your-model",
    headers={"Authorization": f"Bearer {HF_TOKEN}"},
    json={"inputs": model_input["text"]}
)

prediction = hf_response.json()
```

## ⚡ Performance Notes

- **First request:** Slow (~30s) due to model download and initialization
- **Subsequent requests:** Fast (~1-2s per request)
- **Model size:** ~1.6GB (cached locally after first download)
- **Memory usage:** ~2GB RAM when model is loaded

## 🎉 Success!

Your backend now includes:
- ✅ Automatic text summarization (BART)
- ✅ Token counting and validation
- ✅ Intelligent truncation fallback
- ✅ Model-ready output format
- ✅ Complete processing pipeline

All three endpoints (`/process-text`, `/process-image`, `/process-url`) now return standardized `ModelInput` that's ready for your Hugging Face model inference!
