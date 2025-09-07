from pathlib import Path
import json
import numpy as np

BUILD = Path("data/build"); BUILD.mkdir(parents=True, exist_ok=True)

# Placeholder chunks (Phase 1 will replace with real poker docs)
chunks = [
    "STRING BET: placing chips in multiple motions can be ruled as not a single raise.",
    "STOP-AND-GO: call preflop, then shove on the flop facing a continuation bet."
]
meta = [{"doc": "rules"}, {"doc": "strategy"}]

# Dummy embeddings just to prove the flow; real ones come in Phase 1
np.save(BUILD / "embeddings.npy", np.zeros((len(chunks), 384), dtype=np.float32))
with open(BUILD / "metadata.json", "w") as f:
    json.dump({"chunks": chunks, "meta": meta}, f)

print("Wrote placeholder data/build/embeddings.npy and metadata.json (replace in Phase 1)")
