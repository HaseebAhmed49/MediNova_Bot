from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from backend.auth.model import User, SessionLocal
from backend.auth.utility import hash_password, verify_password
from backend.auth.jwt import create_access_token, verify_access_token

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register_user(username: str = Form(...),
    password: str = Form(...), db: Session = Depends(get_db)):
    print(f"Registering user: {username}")
    print(f"Password: {password}")
    hashed_pw = hash_password(password)
    user = User(username=username, hashed_password=hashed_pw)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User registered successfully"}

@router.post("/login")
def login_user(username: str = Form(...),
    password: str = Form(...), db: Session = Depends(get_db)):
    print(f"Logging in user: {username}")
    print(f"Password: {password}")
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}