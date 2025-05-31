"""
parser.py

Parses extracted text into structured inventory data.
"""
import re

def parse_items(text: str):
    """
    Parses raw OCR text to extract item data.

    Args:
        text (str): OCR extracted text.

    Returns:
        list: List of dicts with item, quantity, and price.
    """
    lines = text.strip().split("\n")
    items = []
    for line in lines:
        match = re.match(r"(\w+)\s+(\d+)\s+(\d+\.\d+)", line)
        if match:
            item, qty, price = match.groups()
            items.append({
                "item": item,
                "quantity": int(qty),
                "price": float(price)
            })
    return items
