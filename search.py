from elasticsearch import Elasticsearch
import os

# Define the Quote class if not imported from elsewhere
class Quote:
    def __init__(self, id, text, personality, intensity, tags, quantum_signature):
        self.id = id
        self.text = text
        self.personality = personality
        self.intensity = intensity
        self.tags = tags
        self.quantum_signature = quantum_signature

es = Elasticsearch([os.getenv('ES_HOST', 'localhost')])

def index_quote(quote: Quote):
    es.index(
        index='quotes',
        id=quote.id,
        body={
            'text': quote.text,
            'personality': quote.personality,
            'intensity': quote.intensity,
            'tags': quote.tags,
            'quantum_signature': quote.quantum_signature
        }
    )

def search_quotes(query: str, personality: str = None):
    search_body = {
        "query": {
            "bool": {
                "must": [{"match": {"text": query}}],
                "filter": []
            }
        }
    }
    
    if personality:
        search_body['query']['bool']['filter'].append(
            {"term": {"personality": personality}}
        )
    
    return es.search(index='quotes', body=search_body)