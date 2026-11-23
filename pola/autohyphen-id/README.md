# Kamus Pemenggalan Kata Bahasa Indonesia (baku)

Pola pemenggalan algoritma Liang (3.800+ pola) berdasarkan kaidah PUEBI/EYD, dibuat oleh `gen_hyph_id.py`.

| Berkas | Untuk |
|---|---|
| `hyph-id-baku.tex` | LaTeX (pdfTeX, XeTeX, LuaTeX) |
| `hyph_id_ID.dic` | LibreOffice (format libhyphen), Pyphen, Scribus, dll. |
| `id_hyph_baku.oxt` | Ekstensi LibreOffice siap pasang (berisi `hyph_id_ID.dic`) |
| `softhyphen_docx.py` + `hyph_id.py` | MS Word: menyisipkan optional hyphen ke .docx |
| `gen_hyph_id.py`, `test_hyph.py` | Generator dan uji (108 kata uji, semua cocok) |

## Kaidah yang dikodekan
1. Dua vokal berurutan dipisah: ba-ik, bu-ah, ma-in, a-ir.
2. Diftong ai, au, oi, eu tidak dipisah: pan-tai, pu-lau, sau-da-ra, kecuali diikuti satu konsonan akhir (ba-ik, la-ut).
3. Satu konsonan di antara vokal: ba-ca, ka-ta.
4. ng, ny, sy, kh = satu konsonan: ba-ngun, ba-nyak, a-khir, mu-sya-wa-rah.
5. Dua konsonan dipisah di antaranya: pan-tai, put-ra, sas-tra, ikh-las, mang-ga.
6. Tiga konsonan atau lebih dipisah setelah konsonan pertama: in-struk-si, ul-tra, meng-kri-tik.
7. Awalan trans- : trans-por-ta-si, tran-sak-si.
8. ~30 pengecualian morfologis (batas imbuhan -an): ma-kan-an, pem-be-la-jar-an, pem-ba-ngun-an, pen-di-dik-an, dst.

## Pemasangan
**LibreOffice**: Tools > Extension Manager > Add > `id_hyph_baku.oxt`, restart. Lalu: Tools > Options > Language Settings > Writing Aids > pilih "Indonesian hyphenation" pada Hyphenation; atur bahasa teks ke Indonesian; Format > Paragraph > Text Flow > Hyphenation > Automatically.

**LaTeX** (butuh TeX Live): salin `hyph-id-baku.tex` ke `texmf-local/tex/generic/hyph-id/`, tambahkan baris
`indonesianbaku hyph-id-baku.tex` ke `language.dat.lua`/`language.dat` lokal, jalankan `fmtutil-sys --all`, lalu di dokumen:
`\usepackage[indonesian]{babel}` + `\babelprovide[hyphenrules=indonesianbaku]{indonesian}`.
(Pola sudah diuji memuat tanpa galat di pdfTeX; integrasi babel bergantung pada instalasi Anda.)

**MS Word**: Word tidak bisa memuat kamus pemenggalan pihak ketiga. Gunakan:
`python softhyphen_docx.py tesis.docx tesis_hyph.docx` (hapus kembali dengan `--remove`, atau di Word: Find `^-` > Replace kosong).
Jalankan sebagai langkah terakhir sebelum cetak/PDF karena teks diedit lagi akan membuat pemenggalan lama kedaluwarsa.

## Batasan
- Pola ini fonetis; tanpa leksikon, kata berimbuhan -an tak dikenali otomatis kecuali yang ada pada daftar pengecualian (tambahkan sendiri di `EXC` pada `gen_hyph_id.py`, lalu jalankan ulang).
- Untuk dua konsonan serapan (pr, gr, br, dst.) pola mengikuti kaidah PUEBI "pisah di antaranya": ag-re-si, put-ra (KBBI kadang a-gre-si). Hanya "pro-gram" yang dikecualikan; tambahkan lainnya di `EXC`.
- Hanya huruf a-z (tanpa é, è, ê).
- Batas minimum 2 huruf di kiri dan kanan (menghindari "a-" atau "-i" sendirian di ujung baris).
