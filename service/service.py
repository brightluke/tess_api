# services/quote_service.py
import uuid
import json
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models import Quote  # Use relative import if models.py is in the parent package

# Import or define gen_cache_key
from ..utils import gen_cache_key  # Adjust the import path as needed

# Import or define get_cached_quote and cache_quote
from ..utils import get_cached_quote, cache_quote  # Adjust the import path as needed

class QuoteService:
    def __init__(self, db: Session):
        self.db = db
        
    def get_quote(self, personality: str, filters: dict) -> Quote:
        # Check cache first
        if cached := get_cached_quote(personality, filters):
            return json.loads(cached)
            
        # DB query with advanced filtering
        query = self.db.query(Quote)
        if personality:
            query = query.filter(Quote.personality == personality)
        if min_intensity := filters.get('min_intensity'):
            query = query.filter(Quote.intensity >= min_intensity)
        # ... other filters
        
        quote = query.order_by(func.random()).first()
        
        # Cache result
        if quote:
            cache_quote(gen_cache_key(personality, filters), quote.to_dict())
        
        return quote

    def create_quote(self, quote_data: dict) -> Quote:
        new_quote = Quote(**quote_data)
        
        # BMK24 Reality Metrics
        new_quote.distortion_factor = abs(
            quote_data.get('intensity', 7.5) - 7.5
        ) * (quote_data.get('paradox_index', 0.5))
        
        new_quote.quantum_signature = f"BMK24-R1-{uuid.uuid4().hex[:8]}"
        
        self.db.add(new_quote)
        self.db.commit()
        return new_quote