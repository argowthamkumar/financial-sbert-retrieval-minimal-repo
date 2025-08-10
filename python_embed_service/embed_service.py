# embed_service.py
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import json
import uvicorn
import os

app = FastAPI()
MODEL_NAME = 'all-mpnet-base-v2'
INDEX_DIR = './faiss_index'

print('Loading model...')
model = SentenceTransformer(MODEL_NAME)

print('Loading index...')
if not os.path.exists(INDEX_DIR):
    raise RuntimeError('Index directory not found. Run indexer.py first.')

index = faiss.read_index(os.path.join(INDEX_DIR, 'index.faiss'))
with open(os.path.join(INDEX_DIR, 'metadata.json'),'r') as f:
    metadata = json.load(f)

class Query(BaseModel):
    query: str
    top_k: int = 5

@app.post('/similarity')
def similar(q: Query):
    q_emb = model.encode([q.query], convert_to_numpy=True)
    faiss.normalize_L2(q_emb)
    D, I = index.search(q_emb, q.top_k)
    results = []
    for score, idx in zip(D[0], I[0]):
        if idx == -1:
            continue
        m = metadata[idx]
        results.append({'id': m['id'], 'text': m['text'], 'raw': m['raw'], 'score': float(score)})
    return {'query': q.query, 'results': results}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8001)
