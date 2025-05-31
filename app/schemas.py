from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    quantity: int
    unit_price: float
    sku: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class BillItemBase(BaseModel):
    quantity: int
    unit_price: float
    total_price: float

class BillItemCreate(BillItemBase):
    item_id: int

class BillItem(BillItemBase):
    id: int
    bill_id: int
    item_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class BillBase(BaseModel):
    bill_number: str
    bill_date: datetime
    total_amount: float
    bill_type: str
    image_path: str

class BillCreate(BillBase):
    pass

class Bill(BillBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    items: List[BillItem]

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: EmailStr
    business_name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    items: List[Item] = []
    bills: List[Bill] = []

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None 