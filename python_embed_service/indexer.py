# indexer.py
import argparse
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import json
import os


def read_corpus(path):
    with open(path, 'r') as f:
        raw = f.read()
    docs = [d.strip() for d in raw.split('---') if d.strip()]
    out = []
    for i,d in enumerate(docs):
        lines = [l.strip() for l in d.split('\n') if l.strip()]
        text = ' '.join([l for l in lines if l.startswith('Text:')])
        if text.startswith('Text:'):
            text = text[len('Text:'):].strip()
        out.append({'id': f'doc{i+1}', 'text': text, 'raw': d})
    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', required=True)
    parser.add_argument('--out_index', default='./faiss_index')
    parser.add_argument('--model', default='all-mpnet-base-v2')
    args = parser.parse_args()

    os.makedirs(args.out_index, exist_ok=True)

    corpus = read_corpus(args.data)
    texts = [c['text'] for c in corpus]

    model = SentenceTransformer(args.model)
    embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)

    # normalize for cosine with inner product
    faiss.normalize_L2(embeddings)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    faiss.write_index(index, os.path.join(args.out_index, 'index.faiss'))

    # save metadata & embeddings
    with open(os.path.join(args.out_index, 'metadata.json'), 'w') as f:
        json.dump(corpus, f, indent=2)

    np.save(os.path.join(args.out_index, 'embeddings.npy'), embeddings)

    print('Index and metadata written to', args.out_index)
