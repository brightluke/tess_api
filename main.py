from fastapi import FastAPI, Query
from typing import Optional
import json
import random


app = FastAPI()


# LOAD quotes FROM JSON FILE
#with open('quotes.json', 'r') as file:
def load_quotes():
    # Load the quotes from the JSON file
    with open('quotes.json', 'r') as file:
        quotes = json.load(file)
    return quotes
#the tess quotes
quotes_db = load_quotes()

def get_quotes_db():
     # Wrapper function to load and return the quotes database
    return load_quotes()


@app.get("/")
def read_root():
    return {"Message": "Welcome to the Tess Quotes API!"}

@app.get("/quote")
def get_quote(personality: Optional[str] = Query(None, title="Personality", description="The personality type to get a quote for")):
    quotes_db = get_quotes_db()
    # Check if a personality is provided
    if personality:
        personality = personality.lower()
        if personality not in quotes_db:
            return {"Error": f"Personality not found. Available personalities: " + ", ".join(quotes_db.keys())}
        quote  = random.choice(quotes_db[personality])
    else:
       # Select a random personality from the quotes database
        personality = random.choice(list(quotes_db.keys()))
# Select a random quote associated with the chosen personality
        quote = random.choice(quotes_db[personality])
    if not quote:
        return {"Error": "No quotes available for this personality."}
    return {
        "Personality": personality,
        "Quote": quote
    }
@app.get("/quote/{personality}")
def get_personality_quote(personality: str):
    personality = personality.capitalize()
    if personality not in quotes_db:
        return {"Error": f"Personality not found. Available personalities: " + ", ".join(quotes_db.keys())}
    quote = random.choice(quotes_db[personality])
    if not quote:
        return {"Error": "No quotes available for this personality."}
    return {
        "Personality": personality,
        "Quote": quote
    }#okay now we test the api