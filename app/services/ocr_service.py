import easyocr
import cv2
import numpy as np
from PIL import Image
import io
import re
from datetime import datetime
from typing import List, Dict, Tuple

class OCRService:
    def __init__(self):
        self.reader = easyocr.Reader(['en'])
        
    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        # Convert PIL Image to numpy array
        img_array = np.array(image)
        
        # Convert to grayscale
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        
        # Apply thresholding
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Noise removal
        denoised = cv2.fastNlMeansDenoising(thresh)
        
        return denoised

    def extract_text(self, image: Image.Image) -> List[Tuple[str, float]]:
        # Preprocess the image
        processed_image = self.preprocess_image(image)
        
        # Perform OCR
        results = self.reader.readtext(processed_image)
        return results

    def parse_bill_data(self, ocr_results: List[Tuple[str, float]]) -> Dict:
        bill_data = {
            "items": [],
            "total_amount": 0.0,
            "bill_date": None,
            "bill_number": None
        }
        
        # Regular expressions for matching
        price_pattern = r'\$\s*\d+\.?\d*|\d+\.?\d*\s*\$'
        date_pattern = r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}'
        bill_number_pattern = r'(?:Bill|Invoice|Receipt)\s*(?:#|No\.?)?\s*[:#]?\s*(\d+)'
        
        for text, confidence in ocr_results:
            text = text.strip()
            
            # Extract bill number
            if not bill_data["bill_number"]:
                bill_match = re.search(bill_number_pattern, text, re.IGNORECASE)
                if bill_match:
                    bill_data["bill_number"] = bill_match.group(1)
            
            # Extract date
            if not bill_data["bill_date"]:
                date_match = re.search(date_pattern, text)
                if date_match:
                    try:
                        date_str = date_match.group()
                        bill_data["bill_date"] = datetime.strptime(date_str, "%m/%d/%Y")
                    except ValueError:
                        pass
            
            # Extract total amount
            if "total" in text.lower():
                amount_match = re.search(price_pattern, text)
                if amount_match:
                    amount_str = amount_match.group().replace("$", "").strip()
                    try:
                        bill_data["total_amount"] = float(amount_str)
                    except ValueError:
                        pass
            
            # Extract items and prices
            if re.search(price_pattern, text):
                # This is likely an item line
                item_data = {
                    "name": text,
                    "price": 0.0,
                    "quantity": 1
                }
                
                # Extract price
                price_match = re.search(price_pattern, text)
                if price_match:
                    price_str = price_match.group().replace("$", "").strip()
                    try:
                        item_data["price"] = float(price_str)
                    except ValueError:
                        continue
                
                # Extract quantity if present
                quantity_match = re.search(r'x\s*(\d+)', text, re.IGNORECASE)
                if quantity_match:
                    try:
                        item_data["quantity"] = int(quantity_match.group(1))
                    except ValueError:
                        pass
                
                bill_data["items"].append(item_data)
        
        return bill_data

    def process_bill_image(self, image: Image.Image) -> Dict:
        """
        Process a bill image and return structured data
        """
        # Extract text from image
        ocr_results = self.extract_text(image)
        
        # Parse the extracted text into structured data
        bill_data = self.parse_bill_data(ocr_results)
        
        return bill_data 