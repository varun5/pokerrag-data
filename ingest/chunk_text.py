from __future__ import annotations
import json, pathlib, re

TXT   = pathlib.Path("data/build/text")
CHUNK = pathlib.Path("data/build/chunks"); CHUNK.mkdir(parents=True, exist_ok=True)

def approx_tokens(s:str)->int:  # ~4 chars per token
    return max(1, len(s)//4)

def chunk_doc(text:str, target=320, overlap=60):
    paras = [p.strip() for p in re.split(r"\n{2,}", text) if p.strip()]
    chunks, cur, cur_len = [], [], 0
    for p in paras:
        t = approx_tokens(p)
        if cur_len + t <= target:
            cur.append(p); cur_len += t
        else:
            if cur: chunks.append("\n\n".join(cur))
            cur, cur_len = [p], t
    if cur: chunks.append("\n\n".join(cur))
    # naive overlap
    if overlap>0 and len(chunks)>1:
        merged=[chunks[0]]
        for i in range(1,len(chunks)):
            tail = " ".join(merged[-1].split()[-overlap*4:])
            merged.append((tail + " " + chunks[i]).strip())
        chunks=merged
    return chunks

def main():
    manifest=[]
    for txt in TXT.glob("*.txt"):
        text = txt.read_text()
        cks  = chunk_doc(text)
        out  = (CHUNK / (txt.stem + ".json"))
        out.write_text(json.dumps(cks, ensure_ascii=False))
        manifest.append({"doc_id":txt.stem,"path":str(out),"num_chunks":len(cks)})
        print(f"{txt.stem}: {len(cks)} chunks")
    (CHUNK/"manifest.json").write_text(json.dumps(manifest, indent=2))
    print("wrote manifest:", CHUNK/"manifest.json")
if __name__=="__main__":
    main()
