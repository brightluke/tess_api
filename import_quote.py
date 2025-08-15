# import_quotes.py
from services import QuoteService
from db import SessionLocal

with open('quotes.json') as f:
    quotes_data = json.load(f)

db = SessionLocal()
service = QuoteService(db)

for personality, quotes in quotes_data.items():
    for text in quotes:
        service.create_quote({
            'text': text,
            'personality': personality,
            'is_ai_generated': False
        })