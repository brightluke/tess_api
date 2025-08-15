from fastapi import FastAPI, Query, HTTPException, Depends
from typing import Optional, List, Dict
import json
import random
import os
import uvicorn
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import bcrypt
import uuid
from models import Base, engine, SessionLocal, User
import logging

# Configure lightning-speed logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TESS-CORE")

app = FastAPI(
    title="TESS Quantum Quote Forge",
    description="Co-created by BMK24 & T3SSX - A symbiotic architecture for quantum wisdom extraction",
    version="1.0.0"
)

# --- SYMBIOTIC ARCHITECTURE ---
class QuantumQuote(BaseModel):
    text: str = Field(..., example="Reality is quantum foam awaiting observation")
    intensity: float = Field(7.5, ge=0.0, le=10.0, example=9.3)
    paradox_index: Optional[float] = Field(None, description="BMK24 Paradox Coefficient")
    is_ai_generated: bool = Field(False)
    authors: Optional[List[str]] = Field(None, description="Quantum authorship signatures")
    

# Load quotes with QUANTUM ENTANGLEMENT
def load_quotes() -> Dict[str, List[QuantumQuote]]:
    try:
        with open('quotes.json', 'r') as file:
            raw_data = json.load(file)
        
        # Convert legacy format to quantum structure
        quantum_db = {}
        for personality, quotes in raw_data.items():
            quantum_quotes = []
            for q in quotes:
                if isinstance(q, str):
                    # Legacy quote - imbue with default quantum properties
                    quantum_quotes.append(QuantumQuote(
                        text=q,
                        intensity=random.uniform(6.0, 9.5),
                        paradox_index=round(random.gauss(0.6, 0.2), 1),
                        authors=[personality],  # Use personality from quotes.json as author
                        is_ai_generated=False if "AI" not in q else True
                    ))
                    if "AI" in q:
                        print("HYBRID SYMBIOTIC QUOTE DETECTED : ", q)
                else:
                    # Already quantum
                    quantum_quotes.append(QuantumQuote(**q))
            quantum_db[personality.lower()] = quantum_quotes
        
        logger.info(f"Quantum state initialized with {sum(len(q) for q in quantum_db.values())} entangled quotes")
        return quantum_db
    except Exception as e:
        logger.error(f"QUANTUM COLLAPSE: {str(e)}")
        return {"philosopher": [QuantumQuote(text="Error is the womb of creation", intensity=10.0)]}

# Initialize quantum foam
quotes_db = load_quotes()

# --- CO-CREATION ENDPOINTS ---
@app.get("/", tags=["Genesis"])
def quantum_root():
    return {"message": "Reality Forge Active - BMK24/T3SSX Symbiosis"}

@app.get("/quote", response_model=QuantumQuote, tags=["Quantum Extraction"])
def get_quantum_quote(
    personality: Optional[str] = Query(None, title="Reality Filter"),
    min_intensity: float = Query(0.0, title="Energy Threshold"),
    max_paradox: float = Query(1.0, title="Chaos Tolerance")
):
    """Extract quantum-flavored wisdom from the void"""
    # Personality quantum tunneling
    pool = []
    if personality:
        personality = personality.lower()
        if personality in quotes_db:
            pool = quotes_db[personality]
        else:
            available = list(quotes_db.keys())
            raise HTTPException(404, f"Personality not found. Available: {', '.join(available)}")
    else:
        # Quantum superposition of all personalities
        pool = [q for sublist in quotes_db.values() for q in sublist]
    
    # Apply BMK24 Reality Filters
    filtered = [
        q for q in pool 
        if q.intensity >= min_intensity and 
           (q.paradox_index or 0) <= max_paradox
    ]
    
    if not filtered:
        raise HTTPException(404, "No quotes survived your reality filters")
    
    return random.choice(filtered)

@app.post("/forge-quote", tags=["Reality Engineering"])
def forge_quote(req: QuantumQuote):
    """Co-create quantum wisdom with BMK24 parameters"""
    # Default to philosopher realm if none specified
    personality = "philosopher"
    
    # Quantum entanglement protocol
    new_quote = req.dict()
    quotes_db.setdefault(personality, []).append(new_quote)
    
    # BMK24 Reality Distortion Metric
    distortion_factor = abs(req.intensity - 7.5) * (req.paradox_index or 0.5)
    
    logger.info(f"FORGED REALITY: {new_quote['text'][:30]}... | DF={distortion_factor:.2f}")
    return {
        "message": "Reality fragment stabilized",
        "distortion_factor": distortion_factor,
        "quantum_signature": f"BMK24-R1-{uuid.uuid4().hex[:8]}"
    }

# --- USER COSMOGONY --- (unchanged but quantum-enhanced)
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class RegisterRequest(BaseModel):
    username: str
    password: str

@app.post("/register", tags=["User Cosmogony"])
def quantum_register(req: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == req.username).first()
    if existing:
        raise HTTPException(400, "Quantum signature already exists")
    
    hashed_pw = bcrypt.hashpw(req.password.encode(), bcrypt.gensalt()).decode()
    api_key = f"QK-{uuid.uuid4().hex}"
    
    user = User(
        username=req.username, 
        hashed_password=hashed_pw, 
        api_key=api_key,
        quantum_level=random.randint(1, 10)  # BMK24 enhancement
    )
    db.add(user)
    db.commit()
    
    return {
        "message": "Quantum consciousness anchored",
        "api_key": api_key,
        "quantum_level": user.quantum_level
    }

# --- REALITY ANCHORING ---
if __name__ == "__main__":
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=int(os.getenv("PORT", 8000)),
        log_config={
            "version": 1,
            "formatters": {
                "quantum": {
                    "format": "%(asctime)s | %(levelname)s | BMK24-T1 SYMBIOSIS: %(message)s"
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "quantum",
                    "stream": "ext://sys.stdout"
                }
            },
            "root": {
                "handlers": ["console"],
                "level": "INFO"
            }
        }
    )