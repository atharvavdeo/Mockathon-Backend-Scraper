"""Service for performing Optical Character Recognition (OCR) on images."""

import pytesseract
from PIL import Image
import io


def extract_text_from_image(image_bytes: bytes) -> str:
    """
    Extracts text from an image using Tesseract OCR.

    Args:
        image_bytes: The raw bytes of the image file.

    Returns:
        The extracted text as a string.

    Raises:
        ValueError: If the file cannot be processed as an image or if OCR fails.
    """
    try:
        image = Image.open(io.BytesIO(image_bytes))
        # You can add image preprocessing here if needed (e.g., grayscale, resizing)
        text = pytesseract.image_to_string(image, lang='eng')
        return text
    except Exception as e:
        # Catches errors from Pillow (e.g., invalid image format) or Tesseract
        raise ValueError(f"Failed to process image with OCR: {e}")

