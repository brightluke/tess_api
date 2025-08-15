from sqlalchemy import Column, Integer, String, Float, create_engine, DateTime, Boolean
from sqlalchemy.types import JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///./tessapi.db"

Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    api_key = Column(String, unique=True, index=True)
    
    

class Quote(Base):
    __tablename__ = 'quotes'
    
    id = Column(Integer, primary_key=True)
    text = Column(String(500), nullable=False)
    personality = Column(String(50), index=True)
    intensity = Column(Float, default=7.5)
    paradox_index = Column(Float)
    is_ai_generated = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    tags = Column(JSON)  # For categorical filtering
    # If you want to store an array of strings for tags, use JSON type as you have.
    # Alternatively, you could use a separate association table for tags if you need advanced querying.
    # For most cases, keeping tags as a JSON array is effective and cost efficient.    
    # BMK24 Metrics
    distortion_factor = Column(Float)
    quantum_signature = Column(String(50))
