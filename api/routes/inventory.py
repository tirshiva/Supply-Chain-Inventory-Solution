"""
inventory.py

Defines FastAPI routes for inventory management.
"""
from fastapi import APIRouter, UploadFile, File, Form
from app.ocr import extract_text
from app.parser import parse_items
from app.inventory import update_inventory
from app.logger import setup_logger
import shutil
import os

router = APIRouter(prefix="/inventory", tags=["Inventory"])
setup_logger()

@router.post("/upload-bill/")
async def upload_bill(file: UploadFile = File(...), bill_type: str = Form(...)):
    """
    Uploads a bill image and updates inventory based on extracted data.

    Args:
        file (UploadFile): Image file of the bill.
        bill_type (str): Either "purchase" or "sale".

    Returns:
        dict: Success message with parsed items.
    """
    temp_path = f"temp/{file.filename}"
    os.makedirs("temp", exist_ok=True)
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text(temp_path)
    items = parse_items(text)
    update_inventory(items, bill_type)

    return {"message": "Inventory updated successfully", "items": items}
