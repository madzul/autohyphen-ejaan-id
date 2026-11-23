# -*- coding: utf-8 -*-
"""Rakit berkas pola akhir dari keluaran patgen.

usage: python3 finalisasi.py TOOLS_DIR EVAL_DIR id.pat OUTDIR
Menghasilkan:
  OUTDIR/hyph-id-mti.pat      pola + pengecualian (TeX/LuaLaTeX, pemenggal-id)
  OUTDIR/mti-hyph-id.tex      daftar \\hyphenation untuk pdfLaTeX/XeLaTeX (koreksi pola bawaan hyph-id)
  OUTDIR/hyph_id_ID.raw       pola + pengecualian sebagai pola berbatas kata (untuk LibreOffice, sebelum substrings.pl)
  OUTDIR/laporan.txt          ringkasan uji
"""
import sys, os, re, datetime
sys.path.insert(0, sys.argv[1])
from liang import Hyph, load_tex, load_dic
from aturan_id import Analyzer
from wordfreq import top_n_list, word_frequency

TOOLS, EVAL, PAT, OUT = sys.argv[1:5]
os.makedirs(OUT, exist_ok=True)
A = Analyzer(open(os.path.join(EVAL, 'stems.txt')).read().split())
pats = [l for l in open(PAT).read().split() if l and l[0] not in '\\}']
H = Hyph(pats)

# kosakata uji: 30.000 kata Indonesia tersering + korpus pedoman + istilah TI
vocab = {}
for w in top_n_list('id', 30000):
    if w.isalpha() and w.islower() and len(w) >= 4:
        vocab[w] = word_frequency(w, 'id')
for line in open(os.path.join(EVAL, 'korpus_freq.txt')):
    c, w = line.split()
    vocab.setdefault(w, 1e-7)
for f in ('kamus-mti.txt', 'akar.txt'):
    p = os.path.join(EVAL, '..', 'kamus', f)
    if os.path.exists(p):
        for w in open(p).read().split():
            if w.isalpha() and w.islower():
                vocab.setdefault(w, 1e-7)
GOLDW = set()
# kata uji tangan (gold.txt) dan daftar uji autohyphen-id
for p in (os.path.join(EVAL, 'gold.txt'), os.path.join(EVAL, '..', 'ah', 'x', 'test_hyph.py')):
    if os.path.exists(p):
        for w in re.findall(r'[a-z][a-z-]+', open(p).read()):
            w = w.replace('-', '')
            if len(w) >= 4:
                vocab.setdefault(w, 1e-7); GOLDW.add(w)
# bentuk berimbuhan umum dari akar istilah TI
akar = os.path.join(EVAL, '..', 'kamus', 'akar.txt')
if os.path.exists(akar):
    sys.path.insert(0, EVAL)
    for r in open(akar).read().split():
        for f in (r + 'nya', 'di' + r + 'kan', r + 'kan', 'ter' + r, 'ber' + r):
            vocab.setdefault(f, 1e-8)


GOLD = {}
_gp = os.path.join(EVAL, 'gold.txt')
if os.path.exists(_gp):
    for line in open(_gp):
        if line.strip():
            h = line.split('|')[0].strip(); GOLD[h.replace('-', '')] = h


def ref(w):
    """Acuan kaidah: daftar uji tangan (gold.txt), atau penganalisis untuk kata yang akarnya dikenal kamus."""
    if w in GOLD:
        r, i = set(), 0
        for ch in GOLD[w]:
            if ch == '-': r.add(i)
            else: i += 1
        return {p for p in r if 2 <= p <= len(w) - 2}
    b = A.best(w)
    if b is None and w not in GOLDW:
        return None
    return set(A.points(w))


refs = {w: ref(w) for w in vocab}
refs = {w: r for w, r in refs.items() if r is not None}


def hy(w, pts):
    out, last = '', 0
    for p in sorted(pts):
        out += w[last:p] + '-'; last = p
    return out + w[last:]


import re as _re
def boleh(w):
    # titik yang juga sah: batas imbuhan (ber-a-da) dan di dalam ai/au/ei/oi (ba-ik, la-in)
    ok = set(refs[w]) | set(A.points(w, merge=False))
    for m in _re.finditer(r'(?=(ai|au|ei|oi))', w):
        ok.add(m.start() + 1)
    return ok
# 1) pengecualian untuk pola MTI: kata yang salah atau kehilangan >1 titik
exc_mti = {}
for w, r in refs.items():
    hp = set(H.points(w))
    if hp - boleh(w) or len(r - hp) > 0:
        exc_mti[w] = hy(w, r)

# 1b) seluruh daftar latih (kamus Hunspell + bentuk berimbuhan): kata yang dipenggal salah oleh pola
LATIH = os.environ.get('MTI_LATIH')
n_latih = 0
if LATIH and os.path.exists(LATIH):
    for line in open(LATIH, encoding='utf-8'):
        h = line.strip()
        w = h.replace('-', '')
        if not h or w in exc_mti or w in refs or re.search(r'(kah|lah|pun|tah)$', w):
            continue
        r, i = set(), 0
        for ch in h:
            if ch == '-': r.add(i)
            else: i += 1
        r = {p for p in r if 2 <= p <= len(w) - 2}
        ok = r | {m.start() + 1 for m in re.finditer(r'(?=(ai|au|ei|oi))', w)}
        hp = set(H.points(w))
        if hp - ok:
            exc_mti[w] = hy(w, r); n_latih += 1

# 2) pengecualian untuk pola bawaan TeX hyph-id (pdfLaTeX/XeLaTeX)
tp, te = load_tex('/usr/share/texlive/texmf-dist/tex/generic/hyph-utf8/patterns/tex/hyph-id.tex')
T = Hyph(tp, te)
exc_tex = {}
for w, r in sorted(refs.items(), key=lambda x: -vocab[x[0]]):
    tp_ = set(T.points(w))
    if tp_ - boleh(w):
        exc_tex[w] = hy(w, r)

today = datetime.date.today().isoformat()
with open(os.path.join(OUT, 'hyph-id-mti.pat'), 'w', encoding='utf-8') as f:
    f.write(f"""% hyph-id-mti.pat — pola pemenggalan kata bahasa Indonesia, Program Studi MTI UnLa ({today})
% Dibangkitkan dengan patgen dari {len(pats)} pola atas daftar kata Hunspell id_ID (LGPL-3.0)
% yang dipenggal dengan kaidah EYD Edisi V (kata dasar per suku kata; imbuhan sebagai satu kesatuan).
% Lisensi: LGPL-3.0. Hyphenmin: kiri 2, kanan 2.
\\patterns{{
""")
    for i in range(0, len(pats), 12):
        f.write(' '.join(pats[i:i + 12]) + '\n')
    f.write('}\n\\hyphenation{\n')
    items = sorted(exc_mti.values())
    for i in range(0, len(items), 8):
        f.write(' '.join(items[i:i + 8]) + '\n')
    f.write('}\n')

with open(os.path.join(OUT, 'mti-hyph-id.tex'), 'w', encoding='utf-8') as f:
    f.write(f"""%% mti-hyph-id.tex — pengecualian pemenggalan kata bahasa Indonesia ({today})
%% Untuk pdfLaTeX dan XeLaTeX: memperbaiki kata-kata yang salah dipenggal oleh pola
%% bawaan hyph-id (1997), misalnya "buk-an", "me-la-kuk-an". {len(exc_tex)} kata,
%% dipilih dari 30.000 kata Indonesia tersering dan istilah teknik informatika.
%% Dimuat otomatis oleh mti-unla.cls; pada LuaLaTeX pola MTI lengkap dipakai.
\\babelhyphenation[indonesian]{{%
""")
    items = list(exc_tex.values())
    for i in range(0, len(items), 8):
        f.write(' '.join(items[i:i + 8]) + '\n')
    f.write('}\n\\endinput\n')

# 3) LibreOffice: pengecualian -> pola berbatas kata bernilai tinggi
with open(os.path.join(OUT, 'hyph_id_ID.raw'), 'w', encoding='utf-8') as f:
    for p in pats:
        f.write(p + '\n')
    for w, h in sorted(exc_mti.items()):
        s, i = '.', 0
        brk = set(); k = 0
        for ch in h:
            if ch == '-': brk.add(k)
            else: k += 1
        for k, ch in enumerate(w):
            if k > 0:
                s += '9' if k in brk else '8'
            s += ch
        f.write(s + '.\n')


OK = {w: boleh(w) for w in refs}
def stat(name, h):
    bad = [w for w in refs if set(h.points(w)) - OK[w]]
    tot = sum(vocab[w] for w in refs)
    bt = sum(vocab[w] for w in bad)
    ex = sorted(bad, key=lambda w: -vocab[w])[:10]
    return f'{name}: {len(bad)} dari {len(refs)} kata ({100*len(bad)/len(refs):.1f}%), bobot frekuensi {100*bt/tot:.1f}%; contoh: ' + ', '.join(h.hyph(w) for w in ex)


Hx = Hyph(pats, list(exc_mti.values()))
dp, _, _ = load_dic('/usr/share/hyphen/hyph_id_ID.dic')
BAKU = os.path.join(EVAL, '..', 'ah', 'x', 'hyph_id_ID.dic')
lap = ['Uji pemenggalan terhadap acuan kaidah EYD V (kata yang memuat titik penggalan salah)', '',
       stat('Pola TeX hyph-id (bawaan babel)', T),
       stat('Pola TeX hyph-id + mti-hyph-id.tex', Hyph(tp, te + list(exc_tex.values()))),
       stat('Pola LibreOffice hyph_id_ID', Hyph(dp)),
       *([stat('Pola autohyphen-id (hyph_id_ID-baku.dic)', Hyph(load_dic(BAKU)[0]))] if os.path.exists(BAKU) else []),
       stat('Pola MTI tanpa pengecualian', H),
       stat('Pola MTI + pengecualian', Hx), '',
       f'pola: {len(pats)}, pengecualian MTI: {len(exc_mti)} (termasuk {n_latih} dari daftar kata kamus), pengecualian pdfLaTeX: {len(exc_tex)}']
open(os.path.join(OUT, 'laporan.txt'), 'w').write('\n'.join(lap) + '\n')
print('\n'.join(lap))
