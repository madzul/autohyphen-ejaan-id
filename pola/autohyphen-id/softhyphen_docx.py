#!/usr/bin/env python3
"""Sisipkan 'optional hyphen' (U+00AD) ke kata Bahasa Indonesia di berkas .docx
memakai pola hyph_id_ID.dic, supaya MS Word memenggal kata sesuai kaidah baku.
Pakai:  python softhyphen_docx.py masuk.docx keluar.docx [--min 6] [--remove]
Word hanya menampilkan tanda hubung itu bila kata jatuh di ujung baris."""
import argparse, re
from docx import Document
from hyph_id import hyphenate

SHY = "\u00ad"
WORD = re.compile(r"(?<![\w@/\\.:-])([A-Za-z]+)(?![\w@/\\])")

def process_text(t, minlen, remove):
    if remove:
        return t.replace(SHY, "")
    def f(m):
        w = m.group(1)
        if len(w) < minlen: return w
        return hyphenate(w, sep=SHY)
    return WORD.sub(f, t)

def runs_in(par):
    for r in par.runs: yield r

def paragraphs(doc):
    def walk(container):
        for p in container.paragraphs: yield p
        for t in getattr(container, "tables", []):
            for row in t.rows:
                for cell in row.cells: yield from walk(cell)
    yield from walk(doc)
    for s in doc.sections:
        for part in (s.header, s.footer, s.first_page_header, s.first_page_footer):
            yield from walk(part)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("dst")
    ap.add_argument("--min", type=int, default=6, help="panjang kata minimum (default 6)")
    ap.add_argument("--remove", action="store_true", help="hapus semua optional hyphen")
    a = ap.parse_args()
    doc = Document(a.src); n = 0
    for p in paragraphs(doc):
        for r in p.runs:
            new = process_text(r.text, a.min, a.remove)
            if new != r.text: r.text = new; n += 1
    doc.save(a.dst); print(f"{n} run diubah -> {a.dst}")
