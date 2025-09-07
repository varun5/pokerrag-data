from __future__ import annotations
import json, pathlib, requests
RAW = pathlib.Path("data/raw"); RAW.mkdir(parents=True, exist_ok=True)

def fetch_one(item):
    suffix = ".pdf" if item["type"]=="pdf" else ".html"
    out = RAW / f"{item['id']}{suffix}"
    if out.exists():
        return out
    r = requests.get(item["url"], timeout=60)
    r.raise_for_status()
    out.write_bytes(r.content)
    return out

def main():
    items = json.load(open("ingest/sources.json"))
    for it in items:
        p = fetch_one(it)
        print("saved:", p)

if __name__ == "__main__":
    main()
