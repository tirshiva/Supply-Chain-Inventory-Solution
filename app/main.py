from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from PIL import Image
import io

from . import models, schemas
from .database import engine, get_db
from .services.ocr_service import OCRService

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Inventory Scanner")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Initialize OCR service
ocr_service = OCRService()

# Helper functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

# Authentication endpoints
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        business_name=user.business_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Bill processing endpoints
@app.post("/bills/upload/")
async def upload_bill(
    file: UploadFile = File(...),
    bill_type: str = "purchase",
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Read and process the image
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    
    # Process the bill using OCR
    bill_data = ocr_service.process_bill_image(image)
    
    # Create bill record
    db_bill = models.Bill(
        bill_number=bill_data["bill_number"] or f"BILL-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        bill_date=bill_data["bill_date"] or datetime.now(),
        total_amount=bill_data["total_amount"],
        bill_type=bill_type,
        image_path=file.filename,
        owner_id=current_user.id
    )
    db.add(db_bill)
    db.commit()
    db.refresh(db_bill)
    
    # Process items
    for item_data in bill_data["items"]:
        # Check if item exists
        db_item = db.query(models.Item).filter(
            models.Item.name == item_data["name"],
            models.Item.owner_id == current_user.id
        ).first()
        
        if not db_item:
            # Create new item
            db_item = models.Item(
                name=item_data["name"],
                quantity=item_data["quantity"],
                unit_price=item_data["price"],
                owner_id=current_user.id
            )
            db.add(db_item)
            db.commit()
            db.refresh(db_item)
        else:
            # Update existing item
            if bill_type == "purchase":
                db_item.quantity += item_data["quantity"]
            else:  # sale
                db_item.quantity -= item_data["quantity"]
            db.commit()
        
        # Create bill item record
        db_bill_item = models.BillItem(
            bill_id=db_bill.id,
            item_id=db_item.id,
            quantity=item_data["quantity"],
            unit_price=item_data["price"],
            total_price=item_data["quantity"] * item_data["price"]
        )
        db.add(db_bill_item)
    
    db.commit()
    return {"message": "Bill processed successfully", "bill_id": db_bill.id}

# Inventory endpoints
@app.get("/items/", response_model=List[schemas.Item])
def get_items(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    items = db.query(models.Item).filter(
        models.Item.owner_id == current_user.id
    ).offset(skip).limit(limit).all()
    return items

@app.get("/bills/", response_model=List[schemas.Bill])
def get_bills(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    bills = db.query(models.Bill).filter(
        models.Bill.owner_id == current_user.id
    ).offset(skip).limit(limit).all()
    return bills 