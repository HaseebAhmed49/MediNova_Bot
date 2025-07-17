from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from auth.model import User, SessionLocal
from auth.utility import hash_password, verify_password
from auth.jwt import create_access_token, verify_access_token
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload["sub"]

@router.post("/register")
def register_user(username: str = Form(...),
    password: str = Form(...), db: Session = Depends(get_db)):
    hashed_pw = hash_password(password)
    user = User(username=username, hashed_password=hashed_pw)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User registered successfully"}

@router.post("/login")
def login_user(username: str = Form(...),
    password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/ai_doctor", tags=["AI Doctor"])
def ai_doctor_route(current_user: str = Depends(get_current_user)):
    return {"message": f"Welcome to AI Doctor, {current_user}!"}