# -*- coding: utf-8 -*-
"""Pemenggal kata bahasa Indonesia berbasis aturan EYD Edisi V.

Dipakai untuk membangkitkan daftar kata terpenggal (data latih patgen).
- Kata dasar dipenggal per suku kata: V-KV, VK-KV (Ap-ril, put-ra), diftong ai/au/ei/oi utuh
  kecuali sebelum konsonan penutup (pan-tai, ba-ik), gabungan huruf ng/ny/sy/kh tidak dipisah,
  tiga konsonan atau lebih dipisah setelah konsonan pertama (in-stru-men, ul-tra), ks = x (eks-pe-ri-men).
- Kata berimbuhan dipenggal di antara unsur pembentuknya (ber-a-da, meng-a-na-li-sis,
  di-ha-sil-kan, ke-cer-das-an); bentuk dasar yang luluh dipenggal seperti kata dasar
  (pe-ngem-bang-an, me-ne-rap-kan, pem-ro-gram-an); akhiran -i mengikuti suku fonologis.
"""
import re
try:
    from wordfreq import word_frequency as _wf
    def _freq(w):
        return _wf(w, 'id')
except ImportError:  # tanpa wordfreq: anggap sama
    def _freq(w):
        return 0

VOW = set('aeiou')
DIGRAPH = ('ng', 'ny', 'sy', 'kh')
MUTA = {'pr', 'pl', 'br', 'bl', 'tr', 'dr', 'kr', 'kl', 'gr', 'gl', 'fr', 'fl'}
DIFTONG = ('ai', 'au', 'ei', 'oi')
ONSET_OK = {
    'pr', 'pl', 'br', 'bl', 'tr', 'dr', 'kr', 'kl', 'gr', 'gl', 'fr', 'fl', 'sk', 'sp', 'st',
    'sw', 'sl', 'sm', 'sn', 'kw', 'str', 'spr', 'skr', 'spl', 'ps', 'sr', 'tw', 'dw', 'mr', 'vr', 'fn', 'ph', 'th', 'sh', 'ch'
}


def units(w):
    """Pecah kata menjadi unit fonem: vokal/diftong (V) dan konsonan/digraf (K)."""
    out = []
    i = 0
    while i < len(w):
        two = w[i:i + 2]
        if two in DIGRAPH:
            out.append(('K', two)); i += 2; continue
        c = w[i]
        if c in VOW:
            # diftong utuh (pan-tai, pu-lau), kecuali diikuti satu konsonan penutup kata (ba-ik, la-ut, sa-ing)
            tail = w[i + 2:]
            akhir = len(tail) == 1 and tail not in VOW or tail in DIGRAPH
            if two in DIFTONG and not (i + 2 < len(w) and w[i + 2] in VOW) and not akhir:
                out.append(('V', two)); i += 2; continue
            out.append(('V', c)); i += 1; continue
        out.append(('K', c)); i += 1
    return out


ELEMEN = ('gram', 'graf', 'kras', 'krat', 'kraf')


def _elemen(u, k):
    s = ''.join(x[1] for x in u[k:k + 4])
    return s.startswith(ELEMEN)


def syllabify(w):
    """Kembalikan posisi pemenggalan (indeks huruf) untuk satu morfem/kata dasar."""
    if w.startswith('trans') and len(w) > 6 and w[5] not in VOW:
        return [5] + [5 + p for p in syllabify(w[5:])]  # trans-por-ta-si, trans-krip-si
    u = units(w)
    vidx = [i for i, (t, _) in enumerate(u) if t == 'V']
    cuts = []  # dalam indeks unit
    for a, b in zip(vidx, vidx[1:]):
        cons = [u[k][1] for k in range(a + 1, b)]
        n = len(cons)
        if n == 0:
            cut = b
        elif n == 1:
            cut = a + 1
        elif n == 2:
            # EYD V: dua konsonan di tengah kata dipisah di antaranya (Ap-ril, put-ra, ag-re-si),
            # kecuali unsur terikat serapan -gram/-graf/-krasi/-krat (di-a-gram, bi-o-gra-fi, de-mo-kra-si)
            cut = a + 1 if _elemen(u, a + 1) else a + 2
        elif cons[0] == 'k' and cons[1] == 's':
            cut = a + 3  # ks = x: eks-pe-ri-men, eks-trak-si, teks-til
        else:
            # cari awal suku terpanjang yang sah, minimal satu konsonan tertinggal di koda
            cut = b - 1
            for k in range(1, n):
                on = ''.join(cons[k:])
                if on in ONSET_OK:
                    cut = a + 1 + k
                    break
        cuts.append(cut)
    # konversi ke indeks huruf
    pos = []
    acc = 0
    starts = []
    for t, s in u:
        starts.append(acc); acc += len(s)
    for c in cuts:
        pos.append(starts[c])
    return pos


PREF = [
    ('memper', ''), ('diper', ''), ('keber', ''), ('keter', ''), ('kese', ''), ('seper', ''), ('berke', ''),
    ('meng', 'k'), ('meng', ''), ('meny', 's'), ('mem', 'p'), ('mem', ''), ('men', 't'), ('men', ''), ('menge', ''), ('me', ''),
    ('peng', 'k'), ('peng', ''), ('peny', 's'), ('pem', 'p'), ('pem', ''), ('pen', 't'), ('pen', ''), ('penge', ''), ('pe', ''),
    ('per', ''), ('ber', ''), ('be', ''), ('bel', ''), ('pel', ''), ('ter', ''), ('te', ''), ('di', ''), ('ke', ''), ('se', ''),
]
# me-/pe- + akar yang huruf awalnya luluh menjadi nasal yang dipenggal bersama akarnya: me-nye-di-a-kan
NASAL_REST = [('ny', 's'), ('ng', 'k'), ('m', 'p'), ('n', 't')]
SUF = ['kan', 'an', 'i', 'nya', 'lah', 'kah', 'pun', 'ku', 'mu']


VOKAL = 'aeiou'
def alomorf_ok(p, rest, body):
    """Kecocokan alomorf awalan meN-/peN- dengan huruf awal akar (meng-ajak, bukan men-gajak)."""
    b = body[:1]
    base = p[-4:] if p.endswith(('meng', 'peng', 'meny', 'peny')) else p[-3:] if p.endswith(('mem', 'pem', 'men', 'pen')) else p
    if base in ('meng', 'peng'):
        return b in VOKAL or b in 'ghk' or rest == 'k'
    if base in ('meny', 'peny'):
        return rest == 's' and b in VOKAL
    if base in ('mem', 'pem'):
        return b in 'bfvp' or (rest == 'p' and b in VOKAL) or body[:2] in ('pr', 'pl', 'tr')
    if base in ('men', 'pen'):
        return b in 'cdjzst' or (rest == 't' and b in VOKAL) or body[:2] == 'sy'
    return True


class Analyzer:
    def __init__(self, roots, extra_roots=()):
        self.roots = set(roots) | set(extra_roots)
        self.cache = {}

    def is_root(self, r):
        return len(r) >= 3 and r in self.roots

    def split_suffix(self, w, depth=0):
        """Daftar (stem, [akhiran]) yang mungkin."""
        res = [(w, [])]
        if depth >= 3:
            return res
        for s in SUF:
            if w.endswith(s) and len(w) - len(s) >= 3:
                for stem, sfx in self.split_suffix(w[:-len(s)], depth + 1):
                    res.append((stem, sfx + [s]))
        return res

    def analyses(self, w, depth=0):
        """Hasilkan (morfem-list, panjang-akar). Morfem awalan ditandai 'P:', akhiran 'S:'."""
        out = []
        for stem, sfx in self.split_suffix(w):
            sm = ['S:' + s for s in sfx]
            if self.is_root(stem):
                out.append((['R:' + stem] + sm, len(stem)))
            if depth < 2:
                for p, rest in PREF:
                    if stem.startswith(p) and len(stem) > len(p) + 2:
                        body = stem[len(p):]
                        if not alomorf_ok(p, rest, body):
                            continue
                        cand = rest + body
                        if rest and self.is_root(cand):
                            # konsonan luluh: nasal ikut suku akar (pe-ne-li-ti, me-ngi-rim)
                            nas = p[2:]
                            out.append((['P:' + p[:2], 'N:' + nas + body] + sm, len(cand)))
                        elif not rest:
                            if self.is_root(body):
                                out.append((['P:' + p, 'R:' + body] + sm, len(body)))
                            else:
                                for sub, rl in self.analyses(body, depth + 1):
                                    if sub[-1].startswith('S:') and sm:
                                        continue
                                    out.append((['P:' + p] + sub + sm, rl))
                        if p in ('me', 'pe'):
                            for nas, orig in NASAL_REST:
                                if body.startswith(nas) and self.is_root(orig + body[len(nas):]):
                                    out.append((['P:' + p, 'N:' + body] + sm, len(body)))
                            # pemrograman: pe + mrogram (program)
        return out

    def best(self, w):
        if w in self.cache:
            return self.cache[w]
        an = self.analyses(w)
        if not an:
            self.cache[w] = None
            return None
        # akar terpanjang, lalu imbuhan paling sedikit
        def pen(m):
            # utamakan akhiran -kan daripada akar berakhiran k + -an (me-nya-ta-kan, bukan me-nya-tak-an)
            for i, x in enumerate(m):
                if x == 'S:an' and i > 0 and m[i - 1][2:].endswith('k') and len(m[i - 1]) > 3:
                    r = m[i - 1][2:-1]
                    var = lambda z: [z] + ([c + z[2:] for c in 'sk'] if z[:2] in ('ny', 'ng') else [c + z[1:] for c in 'pt'] if z[:1] in 'mn' else [])
                    cands = var(r)
                    alt = [x for x in cands if self.is_root(x)]
                    if alt:
                        full = m[i - 1][2:]
                        fulls = var(full)
                        f_full = max((_freq(x) for x in fulls if self.is_root(x)), default=0)
                        if max(_freq(x) for x in alt) >= f_full:
                            return 1
            # be- + akar ber-r (be-rada) vs ber- + akar vokal (ber-ada): pilih yang lebih lazim
            for i, x in enumerate(m[:-1]):
                if x in ('P:be', 'P:pe', 'P:te') and m[i + 1].startswith('R:r'):
                    r = m[i + 1][2:]
                    if self.is_root(r[1:]) and _freq(r[1:]) > _freq(r):
                        return 1
            return 0
        def rootfreq(m):
            r = [x[2:] for x in m if x[:2] in ('R:', 'N:')]
            return -_freq(r[0]) if r and r[0] in self.roots else 0
        an.sort(key=lambda x: (pen(x[0]), sum(m[:2] == 'P:' for m in x[0]), -x[1], len(x[0]), rootfreq(x[0])))
        self.cache[w] = an[0][0]
        return an[0][0]

    def points(self, w, left=2, right=2, unknown='syll', merge=False):
        w = w.lower()
        if not re.fullmatch(r'[a-z]+', w):
            return None
        morphs = self.best(w)
        if morphs is None:
            if unknown == 'syll':
                pos = syllabify(w)
            else:
                return None
        else:
            # gabungkan akhiran -i ke morfem sebelumnya (dipenggal fonologis)
            segs = []
            prev_kind = None
            for m in morphs:
                kind, s = m.split(':', 1)
                if kind == 'N' and segs:
                    # bentuk dasar luluh: dipenggal seperti kata dasar (pe-ne-li-ti, pem-ro-gram-an)
                    segs[-1] = segs[-1] + s
                elif kind == 'S' and s == 'i' and segs:
                    segs[-1] = segs[-1] + s
                elif kind == 'R' and segs and prev_kind == 'P' and s[0] in VOW and (
                        segs[-1] in ('bel', 'pel') or (merge and segs[-1][-1] not in VOW)):
                    # bel-/pel- + ajar: be-la-jar, pe-la-jar-an. Awalan lain + akar berawal vokal
                    # dipenggal di batas morfem (ber-a-da, meng-a-na-li-sis, di-am-bil) sesuai EYD V
                    segs[-1] = segs[-1] + s
                else:
                    segs.append(s)
                prev_kind = kind
            pos = []
            off = 0
            for i, s in enumerate(segs):
                if i > 0:
                    pos.append(off)
                pos += [off + p for p in syllabify(s)]
                off += len(s)
        return sorted(p for p in set(pos) if left <= p <= len(w) - right)

    def hyph(self, w, sep='-', **kw):
        ps = self.points(w, **kw)
        if ps is None:
            return None
        out, last = '', 0
        for p in ps:
            out += w[last:p] + sep; last = p
        return out + w[last:]
