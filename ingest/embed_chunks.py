from __future__ import annotations
import json, numpy as np, pathlib
from sentence_transformers import SentenceTransformer

CHUNK = pathlib.Path("data/build/chunks")
BUILD = pathlib.Path("data/build"); BUILD.mkdir(parents=True, exist_ok=True)

def load_all_chunks():
    all_chunks=[]; meta=[]
    manifest = json.loads((CHUNK/"manifest.json").read_text())
    for item in manifest:
        arr = json.loads(pathlib.Path(item["path"]).read_text())
        for i, ch in enumerate(arr):
            all_chunks.append(ch)
            meta.append({
                "doc_id": item["doc_id"],
                "chunk_id": f"{item['doc_id']}#{i}"
            })
    return all_chunks, meta

def main():
    chunks, meta = load_all_chunks()
    print("total chunks:", len(chunks))
    model = SentenceTransformer("all-MiniLM-L6-v2")  # 384-dim
    X = model.encode(chunks, batch_size=64, normalize_embeddings=True, show_progress_bar=True)
    X = X.astype("float32")
    np.save(BUILD/"embeddings.npy", X)
    (BUILD/"metadata.json").write_text(json.dumps({"chunks":chunks,"meta":meta}))
    print("wrote:", BUILD/"embeddings.npy", BUILD/"metadata.json")
if __name__=="__main__":
    main()
