# PokerRag Data (Phase 0)

Holds datasets, build artifacts (embeddings, metadata), and evaluation code.

## Layout
- `data/raw/`   : downloaded source docs (Phase 1)
- `data/build/` : built artifacts (embeddings, metadata, faiss index)
- `ingest/`     : scripts to build artifacts
- `eval/`       : evaluation datasets & scripts (Phase 5)

## Try the placeholder ingest
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python ingest/poker_ingest.py
ls -l data/build
```
