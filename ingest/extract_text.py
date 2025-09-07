from __future__ import annotations
import json, pathlib, re
from pypdf import PdfReader
from bs4 import BeautifulSoup
from markdownify import markdownify as md

RAW  = pathlib.Path("data/raw")
TXT  = pathlib.Path("data/build/text"); TXT.mkdir(parents=True, exist_ok=True)

def pdf_to_text(path: pathlib.Path) -> str:
    text = []
    reader = PdfReader(str(path))
    for p in reader.pages:
        try: text.append(p.extract_text() or "")
        except Exception: text.append("")
    return "\n".join(text)

def html_to_text(path: pathlib.Path) -> str:
    html = path.read_text(errors="ignore")
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script","style","noscript"]): tag.decompose()
    return md(str(soup))

def normalize(s:str)->str:
    s = re.sub(r"[ \t]+"," ", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()

def main():
    items = json.load(open("ingest/sources.json"))
    for it in items:
        suffix = ".pdf" if it["type"]=="pdf" else ".html"
        raw = RAW / f"{it['id']}{suffix}"
        out = TXT / f"{it['id']}.txt"
        if it["type"]=="pdf":
            text = pdf_to_text(raw)
        else:
            text = html_to_text(raw)
        out.write_text(normalize(text))
        print("wrote:", out, f"({len(text)} chars)")
if __name__=="__main__":
    main()
