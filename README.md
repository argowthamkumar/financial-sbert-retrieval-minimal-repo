# Financial SBERT Retrieval — Minimal Repo

This repo demonstrates a minimal retrieval pipeline:
- ingest a small EDGAR-like document (scripted)
- embed passages using `sentence-transformers` (SBERT)
- build a FAISS index and persist it
- serve similarity via FastAPI
- Rust API proxies requests to Python service
- Streamlit frontend to query

Requirements (dev): Python 3.10+, Rust toolchain, Docker optional.

### Quickstart (local, no Docker)
1. Create a Python venv and install deps:
   ```bash
   cd python_embed_service
   python -m venv .venv
   source .venv/bin/activate
   for powershell- .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
2. Ingest sample EDGAR and build index:
   ```bash
   python ingest_edgar.py --out ../sample_data/sample_edgar.txt
   python indexer.py --data ../sample_data/sample_edgar.txt --out_index ./faiss_index
   ```
3. Start the embedding/search service:
   ```bash
   python embed_service.py
   ```
4. Run Rust API (from repo root):
   ```bash
   cd ../rust_api
   cargo run
   ```
5. Run Streamlit app (from repo root):
   ```bash
   cd ../streamlit_frontend
   streamlit run app.py
   ```

Notes:

- The example uses `all-mpnet-base-v2`. For low-latency swap to `all-MiniLM-L6-v2` in `indexer.py` & `embed_service.py`.
- FAISS index is persisted to disk in `python_embed_service/faiss_index.*`.
