#!/usr/bin/env python3
"""Mesin pemenggalan (Liang) memakai hyph_id_ID.dic. Dipakai: from hyph_id import hyphenate"""
import os, re
_here = os.path.dirname(os.path.abspath(__file__))
def load(path=os.path.join(_here, "hyph_id_ID.dic")):
    T = {}
    for ln in open(path, encoding="utf-8").read().splitlines()[1:]:
        if not ln or ln[0].isupper() and " " in ln: continue
        letters, vals, pend = "", [], 0
        for ch in ln:
            if ch.isdigit(): pend = int(ch)
            else: vals.append(pend); pend = 0; letters += ch
        vals.append(pend); T[letters] = vals
    return T
_T = None
def positions(word, left=2, right=2):
    """Indeks (1..n-1) tempat kata boleh dipenggal."""
    global _T
    if _T is None: _T = load()
    w = "." + word.lower() + "."
    v = [0] * (len(w) + 1)
    for i in range(len(w)):
        for j in range(i + 1, min(len(w), i + 20) + 1):
            p = _T.get(w[i:j])
            if p:
                for k, x in enumerate(p):
                    if x > v[i + k]: v[i + k] = x
    n = len(word)
    return [i for i in range(left, n - right + 1) if v[i + 1] % 2 == 1]
def hyphenate(word, sep="-", left=2, right=2):
    ps = set(positions(word, left, right))
    return "".join(c + (sep if i in ps else "") for i, c in enumerate(word, 1)).rstrip(sep)
if __name__ == "__main__":
    import sys
    for w in sys.argv[1:]: print(hyphenate(w))
