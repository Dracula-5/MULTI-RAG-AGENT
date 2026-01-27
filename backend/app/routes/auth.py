from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from ..database import SessionLocal
from ..models import User
from ..auth import decode_token, hash_pw, verify, create_token

router = APIRouter(prefix="/auth", tags=["Auth"])

security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(data: dict, db: Session = Depends(get_db)):
    user = User(username=data["username"], password=hash_pw(data["password"]))
    db.add(user)
    db.commit()
    return {"message": "User registered"}

@router.post("/login")
def login(data: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data["username"]).first()
    if not user or not verify(data["password"], user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"sub": user.username})
    return {"access_token": token}
@router.get("/me")
def me(credentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    payload = decode_token(token)
    username = payload.get("sub")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"username": user.username}


