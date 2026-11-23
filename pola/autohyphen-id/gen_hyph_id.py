#!/usr/bin/env python3
"""Generator pola pemenggalan kata Bahasa Indonesia (PUEBI/EYD, algoritma Liang).
Keluaran: hyph-id-baku.tex (LaTeX), hyph_id_ID.dic (LibreOffice/libhyphen)."""
V = "aeiou"
C = "bcdfghjklmnpqrstvwxyz"
DIG = ["ng", "ny", "sy", "kh"]          # gabungan huruf konsonan = satu bunyi
pats = {}
class _P(dict):
    pass
def _parse(p):
    letters, vals, pend = "", [], 0
    for ch in p:
        if ch.isdigit(): pend = int(ch)
        else: vals.append(pend); pend = 0; letters += ch
    vals.append(pend)
    return letters, vals
def _add(p):
    l, v = _parse(p)
    old = pats.get(l)
    pats[l] = v if old is None else [max(a, b) for a, b in zip(old, v)]
class _Set:
    add = staticmethod(_add)
_pset = _Set()

# 1. Deretan vokal: pisah di antara dua vokal (ba-ik, bu-ah, di-a, ma-in)
for a in V:
    for b in V:
        _pset.add(f"{a}1{b}")
# 2. Diftong ai, au, oi, eu tidak dipisah (pan-tai, pu-lau, sau-da-ra, boi-kot) ...
for d in ("ai", "au", "oi", "eu"):
    _pset.add(f"{d[0]}2{d[1]}")
    # ... kecuali bila diikuti satu konsonan di akhir kata (ba-ik, ma-in, a-ir, la-ut)
    for c in C:
        _pset.add(f"{d[0]}3{d[1]}{c}.")
# 3. V-KV: pemenggalan sebelum konsonan tunggal/digraf (ba-ca, ba-nyak, a-khir)
for a in V:
    for c in list(C) + DIG:
        for b in V:
            _pset.add(f"{a}1{c}{b}")
# 4. Digraf tidak boleh dipisah
for d in DIG:
    _pset.add(f"{d[0]}2{d[1]}")
# 5. V-KK(K): pemenggalan setelah konsonan pertama (pan-tai, ang-ka, mang-ga, in-struk-si)
for a in V:
    for c in list(C) + DIG:
        for d in C:
            if c + d in DIG:
                continue
            _pset.add(f"{a}{c}1{d}")
# 5b. Gugus konsonan di akhir kata tidak dipenggal (teks, bank, kom-pleks)
for c in list(C):
    for d in C:
        if c + d not in DIG:
            _pset.add(f"{c}2{d}.")
# 6. Awalan serapan trans- (trans-por-ta-si, trans-krip-si) ; trans+vokal tetap tran-sak-si
for c in C:
    _pset.add(f".tran6s5{c}")

# 7. Pengecualian morfologis (PUEBI: imbuhan -an/-kan dipenggal pada batas morfem)
EXC = """ma-kan-an mi-num-an tu-lis-an pem-be-la-jar-an pem-ba-ngun-an pen-di-dik-an
per-ban-ding-an pe-ran-cang-an bi-lang-an ke-hi-lang-an ke-bu-tuh-an ke-se-lu-ruh-an
pe-ne-rap-an pe-ngu-kur-an pe-ra-tur-an ke-gi-at-an peng-um-pul-an peng-em-bang-an
pe-nyim-pan-an pem-ro-gram-an pe-ngo-lah-an pe-mi-kir-an pe-ma-ham-an pe-man-fa-at-an
pro-gram pe-nu-lis-an ke-ru-sak-an ke-sa-lah-an ke-ku-rang-an pe-nye-bar-an""".split()
def exc_pattern(w):
    parts = w.split("-")
    s = "."
    for i, p in enumerate(parts):
        s += p
        if i < len(parts) - 1:
            s += "9"
        # tanpa digit lain: pola level 9 mengalahkan pola umum pada posisi itu
    # posisi non-hyphen dipaksa tidak putus (level 8)
    plain = "".join(parts)
    cuts = set(); pos = 0
    for p in parts[:-1]:
        pos += len(p); cuts.add(pos)
    out = "."
    for i, ch in enumerate(plain, 1):
        out += ch
        if i < len(plain):
            out += "9" if i in cuts else "8"
    return out
for w in EXC:
    _pset.add(exc_pattern(w))

def render(l, v):
    out = ""
    for k, ch in enumerate(l):
        if v[k]: out += str(v[k])
        out += ch
    if v[len(l)]: out += str(v[len(l)])
    return out
P = sorted(render(l, v) for l, v in pats.items())
if __name__ == "__main__":
    hdr = "Pola pemenggalan kata Bahasa Indonesia baku (PUEBI/EYD). Dibuat dengan gen_hyph_id.py"
    with open("hyph-id-baku.tex", "w") as f:
        f.write(f"% {hdr}\n% Lisensi: CC0 / domain publik\n\\message{{Indonesian (baku) hyphenation patterns 1.0}}\n")
        f.write("\\patterns{\n" + "\n".join(P) + "\n}\n\\endinput\n")
    with open("hyph_id_ID.dic", "w") as f:
        f.write("UTF-8\nLEFTHYPHENMIN 2\nRIGHTHYPHENMIN 2\nCOMPOUNDLEFTHYPHENMIN 2\nCOMPOUNDRIGHTHYPHENMIN 2\n")
        f.write("\n".join(P) + "\n")
    print(len(P), "pola")
