from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import databases
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
import os
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

# SQLAlchemy setup
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class Crypto(Base):
    __tablename__ = "crypto"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)

# Pydantic models
class CryptoCreate(BaseModel):
    name: str
    price: float

class CryptoUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None

# FastAPI instance
app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
async def get_db():
    async with database.transaction():
        yield database

# API routes
@app.post("/crypto/", response_model=Crypto)
async def create_crypto(crypto: CryptoCreate, db: databases.Database = Depends(get_db)):
    query = Crypto.__table__.insert().values(name=crypto.name, price=crypto.price)
    last_record_id = await db.execute(query)
    logger.info(f"Created crypto: {crypto.name} with ID: {last_record_id}")
    return {**crypto.dict(), "id": last_record_id}

@app.get("/crypto/", response_model=List[Crypto])
async def read_crypto(skip: int = 0, limit: int = 10, db: databases.Database = Depends(get_db)):
    query = Crypto.__table__.select().offset(skip).limit(limit)
    crypto_list = await db.fetch_all(query)
    return crypto_list

@app.get("/crypto/{crypto_id}", response_model=Crypto)
async def read_crypto_by_id(crypto_id: int, db: databases.Database = Depends(get_db)):
    query = Crypto.__table__.select().where(Crypto.id == crypto_id)
    crypto = await db.fetch_one(query)
    if not crypto:
        logger.warning(f"Crypto with ID {crypto_id} not found")
        raise HTTPException(status_code=404, detail="Crypto not found")
    return crypto

@app.put("/crypto/{crypto_id}", response_model=Crypto)
async def update_crypto(crypto_id: int, crypto_update: CryptoUpdate, db: databases.Database = Depends(get_db)):
    query = Crypto.__table__.select().where(Crypto.id == crypto_id)
    db_crypto = await db.fetch_one(query)
    if not db_crypto:
        logger.warning(f"Crypto with ID {crypto_id} not found for update")
        raise HTTPException(status_code=404, detail="Crypto not found")

    update_data = crypto_update.dict(exclude_unset=True)
    query = Crypto.__table__.update().where(Crypto.id == crypto_id).values(**update_data)
    await db.execute(query)
    logger.info(f"Updated crypto with ID {crypto_id}: {update_data}")
    return {**db_crypto, **update_data}

@app.delete("/crypto/{crypto_id}", response_model=int)
async def delete_crypto(crypto_id: int, db: databases.Database = Depends(get_db)):
    query = Crypto.__table__.select().where(Crypto.id == crypto_id)
    db_crypto = await db.fetch_one(query)
    if not db_crypto:
        logger.warning(f"Crypto with ID {crypto_id} not found for deletion")
 raise HTTPException(status_code=404, detail="Crypto not found")

    query = Crypto.__table__.delete().where(Crypto.id == crypto_id)
    await db.execute(query)
    logger.info(f"Deleted crypto with ID {crypto_id}")
    return crypto_id

# Database setup
async def init_db():
    async with database:
        await database.execute("CREATE TABLE IF NOT EXISTS crypto (id INTEGER PRIMARY KEY, name TEXT, price REAL)")

@app.on_event("startup")
async def startup():
    await init_db()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
