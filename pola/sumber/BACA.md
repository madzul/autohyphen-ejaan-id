# Membangkitkan ulang pola MTI

Kebutuhan: Python 3, `patgen` (TeX Live), kamus Hunspell bahasa Indonesia (`id_ID.aff`, `id_ID.dic`, paket `hunspell-id`), `unmunch` (paket `hunspell-tools`), pustaka Python `wordfreq` (opsional, untuk memilih *-kan* atau *-an*), dan `substrings.pl` dari libhyphen (untuk berkas LibreOffice).

1. **Daftar kata.**
   - `stems.txt`: kata dasar dari `id_ID.dic`, tanpa penanda imbuhan, huruf kecil, satu kata per baris.
   - `forms_clean.txt`: hasil `unmunch id_ID.dic id_ID.aff`, huruf kecil a-z saja.
   - `gen_forms.txt`: bentuk berimbuhan tambahan, dibuat dengan `python3 gen.py > gen_forms.txt`.
2. **Daftar latih.** Jalankan `python3 mkset.py .` untuk memenggal semua kata dengan `aturan_id.py`, yaitu penganalisis kaidah EYD V. Hasilnya `latih.txt`.
3. **Pola.** Siapkan sampel seperempat kata dan latih polanya:
   ```
   grep -v -E '(kah|lah|pun|tah)$' latih.txt | awk 'NR%4==0' > sampel.txt
   touch kosong.pat
   patgen sampel.txt kosong.pat id.pat id.tra < p3.txt
   ```
   Jalankan pada seluruh daftar bila waktu cukup.
4. **Berkas akhir.** Jalankan `python3 finalisasi.py . . id.pat keluaran/`. Perintah ini menghasilkan:
   - `hyph-id-mti.pat`: pola dan pengecualian;
   - `mti-hyph-id.tex`: koreksi untuk pdfLaTeX;
   - `hyph_id_ID.raw`: bahan berkas LibreOffice;
   - `laporan.txt`: hasil uji.
5. **Berkas LibreOffice.** Jalankan `perl substrings.pl keluaran/hyph_id_ID.raw hyph_id_ID_MTI.dic UTF-8 2 2`.

Pada `finalisasi.py`, jalur berkas uji (`korpus_freq.txt`, `gold.txt`, kamus istilah) disesuaikan dengan susunan folder Anda.
