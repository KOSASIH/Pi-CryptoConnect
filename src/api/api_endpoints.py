# api_endpoints.py
import os
import json
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import CryptoCurrency, User
from .utils import get_db, get_settings

app = FastAPI(title="Pi-CryptoConnect API", description="A high-tech API for cryptocurrency enthusiasts")

# Security settings
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Database connection
engine = create_engine(os.environ["DATABASE_URL"])
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Settings
settings = get_settings()

# Models
class CryptoCurrencyResponse(BaseModel):
    id: int
    name: str
    symbol: str
    price: float

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

# API Endpoints
@app.get("/cryptocurrencies/", response_class=JSONResponse)
async def get_cryptocurrencies(db: SessionLocal = Depends(get_db)):
    """Get a list of all supported cryptocurrencies"""
    cryptocurrencies = db.query(CryptoCurrency).all()
    return {"cryptocurrencies": [CryptoCurrencyResponse.from_orm(c) for c in cryptocurrencies]}

@app.get("/cryptocurrencies/{symbol}", response_class=JSONResponse)
async def get_cryptocurrency(symbol: str, db: SessionLocal = Depends(get_db)):
    """Get a specific cryptocurrency by symbol"""
    cryptocurrency = db.query(CryptoCurrency).filter_by(symbol=symbol).first()
    if not cryptocurrency:
        raise HTTPException(status_code=404, detail="Cryptocurrency not found")
    return {"cryptocurrency": CryptoCurrencyResponse.from_orm(cryptocurrency)}

@app.post("/users/", response_class=JSONResponse)
async def create_user(user: UserResponse, db: SessionLocal = Depends(get_db)):
    """Create a new user"""
    db_user = User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    return {"user": UserResponse.from_orm(db_user)}

@app.get("/users/me", response_class=JSONResponse)
async def get_user(token: str = Depends(oauth2_scheme), db: SessionLocal = Depends(get_db)):
    """Get the current user"""
    user = db.query(User).filter_by(token=token).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"user": UserResponse.from_orm(user)}

@app.post("/token", response_class=JSONResponse)
async def login(username: str, password: str, db: SessionLocal = Depends(get_db)):
    """Login and obtain a token"""
    user = db.query(User).filter_by(username=username).first()
    if not user or not user.check_password(password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = user.generate_token()
    return {"token": token}

# Error handling
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
