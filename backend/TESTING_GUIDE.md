# Testing Guide for Content Processing API

## Prerequisites

1. **Tesseract OCR** is installed (already done ✅)
   ```bash
   brew install tesseract
   ```

2. **Python dependencies** are installed (already done ✅)
   ```bash
   pip install -r requirements.txt
   ```

## Quick Start Testing

### 1. Start the Server

Open a terminal and run:
```bash
cd /Users/atharvadeo/Desktop/PROF/Hackies/Mockathon-HackiOps/backend
uvicorn main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### 2. Access Interactive API Documentation

Open your browser and go to:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

---

## Testing Each Endpoint

### A. Test Root Endpoint

**Browser:**
```
http://127.0.0.1:8000/
```

**cURL:**
```bash
curl http://127.0.0.1:8000/
```

**Expected Response:**
```json
{
  "message": "Content Processing API",
  "endpoints": {
    "process_url": "/api/process-url",
    "process_text": "/api/process-text",
    "process_image": "/api/process-image"
  }
}
```

---

### B. Test Text Processing Endpoint

**cURL:**
```bash
curl -X POST "http://127.0.0.1:8000/api/process-text" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Artificial intelligence has revolutionized the way we interact with technology in modern society. Machine learning algorithms are now being used in various applications, from healthcare diagnostics to financial forecasting and autonomous vehicles. The advancement of neural networks has enabled computers to perform complex tasks that were once thought to be exclusively human capabilities. As we continue to develop more sophisticated AI systems, it is crucial to consider the ethical implications."
  }'
```

**Expected Response:**
```json
{
  "cleaned_text": "Artificial intelligence has revolutionized...",
  "original_char_count": 456,
  "cleaned_char_count": 440
}
```

**Validation Rules:**
- Minimum 100 characters
- Minimum 50 words
- Must be in English
- Special characters are cleaned

**Test Error Handling (Short Text):**
```bash
curl -X POST "http://127.0.0.1:8000/api/process-text" \
  -H "Content-Type: application/json" \
  -d '{"text": "This is too short."}'
```

**Expected Error:**
```json
{
  "detail": "Text content is too short. Minimum 50 words required."
}
```

---

### C. Test Image OCR Processing Endpoint

**Step 1: Generate a test image**
```bash
cd /Users/atharvadeo/Desktop/PROF/Hackies/Mockathon-HackiOps/backend
python generate_test_image.py
```

This creates `test_image.png` with English text.

**Step 2: Test with cURL**
```bash
curl -X POST "http://127.0.0.1:8000/api/process-image" \
  -H "accept: application/json" \
  -F "file=@test_image.png"
```

**Expected Response:**
```json
{
  "cleaned_text": "Artificial Intelligence and Machine Learning...",
  "original_char_count": 285,
  "cleaned_char_count": 275
}
```

**Test with your own image:**
```bash
curl -X POST "http://127.0.0.1:8000/api/process-image" \
  -F "file=@/path/to/your/image.jpg"
```

---

### D. Run Automated Test Script

We've created a Python test script for you:

```bash
# In a NEW terminal (keep the server running in the first one)
cd /Users/atharvadeo/Desktop/PROF/Hackies/Mockathon-HackiOps/backend
python test_endpoints.py
```

This will test:
- ✅ Root endpoint
- ✅ Text processing
- ✅ Error handling
- ⚠️ Image processing (instructions provided)

---

## Testing with Swagger UI (Recommended)

1. Go to http://127.0.0.1:8000/docs
2. You'll see all endpoints with interactive documentation
3. Click on any endpoint to expand it
4. Click "Try it out"
5. Fill in the parameters
6. Click "Execute"
7. See the response below

### Example: Testing `/api/process-text` via Swagger

1. Expand `POST /api/process-text`
2. Click "Try it out"
3. Paste this in the request body:
```json
{
  "text": "Artificial intelligence has revolutionized the way we interact with technology in modern society. Machine learning algorithms are now being used in various applications, from healthcare diagnostics to financial forecasting and autonomous vehicles. The advancement of neural networks has enabled computers to perform complex tasks that were once thought to be exclusively human capabilities. As we continue to develop more sophisticated AI systems, it is crucial to consider the ethical implications and ensure that these technologies are used responsibly."
}
```
4. Click "Execute"
5. View the response

### Example: Testing `/api/process-image` via Swagger

1. Expand `POST /api/process-image`
2. Click "Try it out"
3. Click "Choose File" and select `test_image.png` (or any image with text)
4. Click "Execute"
5. View the OCR results

---

## Common Issues & Solutions

### Issue 1: "Import could not be resolved"
**Solution:** This is just a linting issue. The packages are installed and will work at runtime.

### Issue 2: Tesseract not found
**Solution:** 
```bash
brew reinstall tesseract
```

### Issue 3: Port already in use
**Solution:** 
```bash
# Kill the process using port 8000
lsof -ti:8000 | xargs kill -9
# Then restart the server
uvicorn main:app --reload
```

### Issue 4: OCR returns empty text
**Solution:**
- Ensure the image has clear, readable text
- Try increasing text size or contrast
- Verify Tesseract is properly installed: `tesseract --version`

---

## API Endpoint Summary

| Endpoint | Method | Description | Request Body |
|----------|--------|-------------|--------------|
| `/` | GET | Root/Info | None |
| `/api/process-url` | POST | Process URL (future) | `{"url": "..."}` |
| `/api/process-text` | POST | Process raw text | `{"text": "..."}` |
| `/api/process-image` | POST | Process image (OCR) | Form file upload |

---

## Next Steps

1. ✅ Test all endpoints using Swagger UI
2. ✅ Generate and test with `test_image.png`
3. ✅ Try with different text samples
4. ✅ Test error handling with invalid inputs
5. 🔄 Implement the URL processing pipeline (if needed)

---

## Need Help?

- Check FastAPI docs: https://fastapi.tiangolo.com/
- Check Tesseract docs: https://github.com/tesseract-ocr/tesseract
- View server logs in the terminal where you ran `uvicorn`
