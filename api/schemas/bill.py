"""
bill.py

Pydantic models for request/response schemas.
"""
from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    item: str
    quantity: int
    price: float

class InventoryUpdateRequest(BaseModel):
    bill_type: str
    items: List[Item]
