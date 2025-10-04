"""Test script to demonstrate the new API endpoints."""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

# Sample long English text (more than 100 characters and 50 words)
SAMPLE_TEXT = """
Artificial intelligence has revolutionized the way we interact with technology in modern society. 
Machine learning algorithms are now being used in various applications, from healthcare diagnostics 
to financial forecasting and autonomous vehicles. The advancement of neural networks has enabled 
computers to perform complex tasks that were once thought to be exclusively human capabilities. 
As we continue to develop more sophisticated AI systems, it is crucial to consider the ethical 
implications and ensure that these technologies are used responsibly for the benefit of humanity.
"""


def test_process_text():
    """Test the /process-text endpoint."""
    print("\n" + "="*60)
    print("Testing POST /api/process-text")
    print("="*60)
    
    payload = {"text": SAMPLE_TEXT}
    
    try:
        response = requests.post(f"{BASE_URL}/process-text", json=payload)
        response.raise_for_status()
        
        result = response.json()
        print(f"✅ Status Code: {response.status_code}")
        print(f"Original char count: {result['original_char_count']}")
        print(f"Cleaned char count: {result['cleaned_char_count']}")
        print(f"Cleaned text preview: {result['cleaned_text'][:100]}...")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")


def test_process_image():
    """Test the /process-image endpoint (requires an image file)."""
    print("\n" + "="*60)
    print("Testing POST /api/process-image")
    print("="*60)
    
    # You would need to provide an actual image file path
    # For demonstration, this shows the structure
    print("⚠️  To test image processing, you need to:")
    print("   1. Have an image file with English text")
    print("   2. Replace 'path/to/image.jpg' with your actual image path")
    print("   3. Uncomment the code below")
    
    # Uncomment and modify this when you have an image:
    # try:
    #     with open("path/to/image.jpg", "rb") as f:
    #         files = {"file": ("image.jpg", f, "image/jpeg")}
    #         response = requests.post(f"{BASE_URL}/process-image", files=files)
    #         response.raise_for_status()
    #         
    #         result = response.json()
    #         print(f"✅ Status Code: {response.status_code}")
    #         print(f"Original char count: {result['original_char_count']}")
    #         print(f"Cleaned char count: {result['cleaned_char_count']}")
    #         print(f"Extracted text preview: {result['cleaned_text'][:100]}...")
    # except Exception as e:
    #     print(f"❌ Error: {e}")


def test_root():
    """Test the root endpoint."""
    print("\n" + "="*60)
    print("Testing GET /")
    print("="*60)
    
    try:
        response = requests.get("http://127.0.0.1:8000/")
        response.raise_for_status()
        
        result = response.json()
        print(f"✅ Status Code: {response.status_code}")
        print(f"Response: {json.dumps(result, indent=2)}")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")


def test_error_handling():
    """Test error handling with invalid input."""
    print("\n" + "="*60)
    print("Testing Error Handling (short text)")
    print("="*60)
    
    payload = {"text": "This text is too short."}
    
    try:
        response = requests.post(f"{BASE_URL}/process-text", json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
    except requests.exceptions.RequestException as e:
        print(f"Expected error (text too short): {e}")


if __name__ == "__main__":
    print("\n🚀 Starting API Endpoint Tests")
    print("Make sure the server is running: uvicorn main:app --reload")
    print("\nPress Ctrl+C to exit")
    
    input("\nPress Enter to start tests...")
    
    test_root()
    test_process_text()
    test_error_handling()
    test_process_image()
    
    print("\n" + "="*60)
    print("✅ Tests Complete!")
    print("="*60)
