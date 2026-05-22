from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from passlib.context import CryptContext
from backend.database import get_db
from backend.models.schemas import User

router = APIRouter()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Pydantic schemas ---
class UserRegister(BaseModel):
    full_name: str
    email: str
    password: str
    role: str  # "student" or "landlord"

class UserLogin(BaseModel):
    email: str
    password: str

# --- Helper functions ---
def hash_password(password: str):
    # Truncate to 72 bytes to avoid bcrypt limitation
    password = password[:72]
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    plain_password = plain_password[:72]
    return pwd_context.verify(plain_password, hashed_password)
# --- Endpoints ---
@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    new_user = User(
        full_name=user.full_name,
        email=user.email,
        hashed_password=hash_password(user.password),
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User registered successfully", "user_id": new_user.id}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    # Check if user exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    # Check password
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    return {
        "message": "Login successful",
        "user_id": db_user.id,
        "full_name": db_user.full_name,
        "role": db_user.role
    }