"""Generate a test image with text for OCR testing."""

from PIL import Image, ImageDraw, ImageFont
import os

def create_test_image():
    """Create a simple image with text for OCR testing."""
    
    # Create a white image
    width, height = 800, 400
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Sample text
    text = """
    Artificial Intelligence and Machine Learning
    
    This is a test image containing English text
    for Optical Character Recognition (OCR) testing.
    The text should be extracted and processed by
    our backend API endpoint.
    
    Machine learning has revolutionized technology
    and continues to advance rapidly in many fields.
    """
    
    # Try to use a default font
    try:
        # For larger text
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
    except:
        # Fallback to default font if TrueType not available
        font = ImageFont.load_default()
    
    # Draw black text on white background
    draw.text((50, 50), text.strip(), fill='black', font=font)
    
    # Save the image
    output_path = os.path.join(os.path.dirname(__file__), 'test_image.png')
    image.save(output_path)
    print(f"✅ Test image created: {output_path}")
    return output_path

if __name__ == "__main__":
    create_test_image()
