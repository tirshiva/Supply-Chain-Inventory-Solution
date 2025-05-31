"""
ocr.py

Handles OCR processing using pytesseract.
"""
import pytesseract
from PIL import Image

def extract_text(image_path: str) -> str:
    """
    Extracts text from a given image using Tesseract OCR.

    Args:
        image_path (str): Path to the bill image.

    Returns:
        str: Extracted text.
    """
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)
