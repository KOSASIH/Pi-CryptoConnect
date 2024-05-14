from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import databases
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Models
class Crypto(Base):
    __tablename__ = "crypto"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    name = sqlalchemy.Column(sqlalchemy.String, index=True)
    price = sqlalchemy.Column(sqlalchemy.Float)

# Pydantic models
class CryptoCreate(BaseModel):
    name: str
    price: float

class CryptoUpdate(BaseModel):
    name: str = None
    price: float = None

# FastAPI instance
app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API routes
@app.post("/crypto/", response_model=Crypto)
async def create_crypto(crypto: CryptoCreate, db: databases.Database = Depends(get_db)):
    db_crypto = Crypto(name=crypto.name, price=crypto.price)
    db.add(db_crypto)
    db.commit()
    db.refresh(db_crypto)
    return db_crypto

@app.get("/crypto/", response_model=List[Crypto])
async def read_crypto(skip: int = 0, limit: int = 10, db: databases.Database = Depends(get_db)):
    crypto = db.query(Crypto).offset(skip).limit(limit).all()
    return crypto

@app.get("/crypto/{crypto_id}", response_model=Crypto)
async def read_crypto_by_id(crypto_id: int, db: databases.Database = Depends(get_db)):
    crypto = db.query(Crypto).filter(Crypto.id == crypto_id).first()
    if not crypto:
        raise HTTPException(status_code=404, detail="Crypto not found")
    return crypto

@app.put("/crypto/{crypto_id}", response_model=Crypto)
async def update_crypto(crypto_id: int, crypto_update: CryptoUpdate, db: databases.Database = Depends(get_db)):
    db_crypto = db.query(Crypto).filter(Crypto.id == crypto_id).first()
    if not db_crypto:
        raise HTTPException(status_code=404, detail="Crypto not found")

    if crypto_update.name:
        db_crypto.name = crypto_update.name
    if crypto_update.price:
        db_crypto.price = crypto_update.price

    db.commit()
    db.refresh(db_crypto)
    return db_crypto

@app.delete("/crypto/{crypto_id}", response_model=int)
async def delete_crypto(crypto_id: int, db: databases.Database = Depends(get_db)):
    crypto = db.query(Crypto).filter(Crypto.id == crypto_id).first()
    ifnot crypto:
        raise HTTPException(status_code=404, detail="Crypto not found")

    db.delete(crypto)
    db.commit()
    return crypto.id

# Database setup
Base.metadata.create_all(bind=engine)

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
