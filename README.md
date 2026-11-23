# Paket Proofing Bahasa Indonesia untuk Naskah Tesis MTI UnLa

Paket ini membantu naskah tesis yang diketik **rata kiri-kanan (justified) dengan pemenggalan kata**, sesuai Pedoman Penulisan Tesis MTI UnLa, baik di Microsoft Word dan sejenisnya maupun di LaTeX.

| Folder | Isi | Untuk |
|---|---|---|
| `word/` | `Templat-Tesis-MTI-UnLa.dotx` | Word, LibreOffice Writer |
| `pemenggal/` | `pemenggal-id.html`, `pemenggal_id.py`, `hyph-id-mti.pat`, `hyph_id_ID-baku.dic` | Word (pemenggalan bahasa Indonesia) |
| `kamus/` | `kamus-mti.dic` (Word), `kamus-mti-libreoffice.dic`, `kamus-mti.txt` | pemeriksa ejaan |
| `libreoffice/` | `pemenggalan-ejaan-id-mti.oxt` | LibreOffice (pemenggalan + ejaan) |
| `latex/` | `mti-unla.cls`, `tesis.tex`, `contoh-tesis.pdf`, dll. | pdfLaTeX, XeLaTeX, LuaLaTeX |
| `templat-latex-overleaf.zip` | isi folder `latex/` siap unggah | Overleaf |
| `zotero/` | `mti-unla.csl` | Zotero, Mendeley, pandoc |
| `pola/` | pola pemenggalan, laporan uji, skrip pembangkit, kamus asli autohyphen-id | pengembang |

---

## 1. Hal penting tentang Microsoft Word

**Word tidak dapat memenggal kata bahasa Indonesia secara otomatis.** Microsoft hanya menyediakan pemeriksa ejaan (*spelling*) untuk bahasa Indonesia, tanpa pemenggal kata (*hyphenation*) dan tanpa pemeriksa tata bahasa. Sumber:

- [Proofing tools available in Office for Mac](https://support.microsoft.com/topic/proofing-tools-available-in-office-for-mac-e175007d-193d-4efc-afce-5e27a59f1057): Indonesian hanya bertanda *Spelling*.
- [Editor's spelling, grammar, and refinement availability by language](https://support.microsoft.com/office/editor-s-spelling-grammar-and-refinement-availability-by-language-ecd60e9f-6b2e-4070-b30c-42efa6cff55a)
- [Companion proofing languages](https://learn.microsoft.com/en-us/office/2016/language/companion-proofing-languages)

Akibatnya, mengaktifkan *Hyphenation: Automatic* pada teks berbahasa Indonesia tidak menghasilkan penggalan apa pun, dan paragraf rata kiri-kanan menjadi berspasi renggang. Jalan keluarnya adalah **tanda pemenggal opsional** (*optional hyphen*, Ctrl+- di Windows, Cmd+- di Mac). Tanda ini tidak terlihat dan hanya tercetak sebagai "-" bila kata terpotong di akhir baris. Alat di folder `pemenggal/` menyisipkan tanda ini ke seluruh naskah secara otomatis.

### 1.1 Pengaturan Word (sudah terpasang di templat)

Bila tidak memakai templat, atur sendiri:

| Pengaturan | Nilai | Letak menu (Windows) |
|---|---|---|
| Bahasa naskah | Indonesian | Review → Language → Set Proofing Language |
| Perataan | Justify | Home → Paragraph |
| Pemenggalan | Automatic | Layout → Hyphenation → Automatic |
| Zona pemenggalan | 0,63 cm | Layout → Hyphenation → Hyphenation Options → Hyphenation zone |
| Batas tanda hubung berurutan | 2 | Hyphenation Options → Limit consecutive hyphens to |
| Kata berhuruf kapital | tidak dipenggal | Hyphenation Options → hapus centang *Hyphenate words in CAPS* |
| Judul, tabel, URL, kode | tidak dipenggal | Format → Paragraph → Line and Page Breaks → *Don't hyphenate* |

Di Word untuk Mac, menu pemenggalan ada di Tools → Hyphenation. *Automatic* tetap berguna untuk istilah asing yang diberi bahasa English, sedangkan teks Indonesia dipenggal oleh tanda pemenggal opsional.

Pastikan paket bahasa Indonesia untuk pemeriksa ejaan terpasang. Bila belum, pasang lewat [Language Accessory Pack](https://support.microsoft.com/en-US/office/languages/language-accessory-pack-for-microsoft-365).

### 1.2 Templat Word `Templat-Tesis-MTI-UnLa.dotx`

Klik dua kali berkas .dotx untuk membuat naskah baru. Isinya:

- A4, margin cermin (dalam 4 cm, luar/atas/bawah 3 cm), Times New Roman 12, spasi 1,5, jarak antarparagraf 18 pt, nomor halaman di tengah 1,5 cm dari tepi bawah (romawi kecil untuk bagian persiapan, angka arab untuk tubuh utama).
- Gaya judul memakai *Heading 1–3* bawaan Word dengan nama tampilan **Heading Bab** ("Bab I Pendahuluan", TNR 14 tebal, tengah), **Heading Subbab** (I.1, gantung 1,5 cm), dan **Heading Anak Subbab** (I.1.1, gantung 2 cm). Gaya bawaan dipakai agar penomoran keterangan gambar per bab (Gambar III.1) dan daftar isi berfungsi.
- Gaya **Judul Bagian** (Abstrak, Kata Pengantar, dsb.), **Judul Lampiran**, **Caption**, **Isi Tabel**, **Daftar Pustaka** (gantung), **Kutipan Panjang**, **Kode Program**, **Istilah Asing** (miring, bahasa English), serta gaya tabel **Tabel Tesis**.
- Daftar isi, daftar gambar, dan daftar tabel otomatis. Tekan F9 (atau klik kanan → Update Field) setelah naskah berubah.

### 1.3 Menyisipkan tanda pemenggal ke naskah Word

**Cara termudah, `pemenggal-id.html`:** buka berkas ini di peramban apa pun (bekerja tanpa internet, berkas tidak dikirim ke mana pun), seret naskah .docx, pilih pola pemenggalan (MTI UnLa atau autohyphen-id, lihat bagian 6), lalu klik **Proses dan unduh**. Hasilnya `…-dipenggal.docx`; naskah asli tidak diubah.

**Lewat baris perintah (Python 3.8+, tanpa pustaka tambahan):**

```
python3 pemenggal_id.py naskah.docx                    # menghasilkan naskah-dipenggal.docx
python3 pemenggal_id.py --hapus naskah-dipenggal.docx  # membuang semua tanda pemenggal opsional
python3 pemenggal_id.py --kata pembelajaran            # pem-be-la-jar-an
python3 pemenggal_id.py --pola hyph_id_ID-baku.dic naskah.docx   # memakai pola autohyphen-id
```

Yang tidak dipenggal: judul, isi tabel, teks miring (istilah asing), teks berbahasa selain Indonesia, singkatan berhuruf kapital, alamat web, kode, dan kata di bawah 5 huruf. Jalankan ulang setelah naskah banyak berubah, karena kata yang diketik kemudian belum diberi tanda. Kedua alat memberi hasil yang identik.

### 1.4 Kamus istilah untuk Word

`kamus-mti.dic` berisi 198 istilah teknik informatika berbahasa Indonesia yang belum dikenal pemeriksa ejaan (mis. *klasterisasi*, *peladen*, *pemrograman*). Cara memasang: File → Options → Proofing → **Custom Dictionaries** → **Add…** → pilih `kamus-mti.dic` → atur *Dictionary language* ke Indonesian → OK. Di Mac: Word → Preferences → Spelling & Grammar → Dictionaries.

## 2. LibreOffice Writer

1. Tools → Extension Manager → **Add…** → pilih `pemenggalan-ejaan-id-mti.oxt`, lalu mulai ulang LibreOffice. Ekstensi ini memasang pola pemenggalan MTI, kamus Hunspell bahasa Indonesia, dan kamus istilah TI.
2. Tools → Options → Language Settings → Writing Aids → Edit (pada *Available language modules*) → pilih bahasa Indonesian, pastikan *Hunspell SpellChecker* dan *Hyphenator* tercentang.
3. Teks harus berbahasa Indonesian (Tools → Language → For All Text), dan paragraf memakai Format → Paragraph → Text Flow → **Automatically** (karakter di akhir baris 2, awal baris 2, maksimum tanda hubung berurutan 2).

Dengan ekstensi ini LibreOffice memenggal sendiri, sehingga `pemenggal-id.html` tidak diperlukan. Pola ini mengalahkan pola bawaan LibreOffice bila keduanya terpasang (sudah diuji).

Templat .dotx dapat dibuka di LibreOffice, dengan satu keterbatasan: LibreOffice tidak mengulang nomor gambar/tabel di setiap bab. Bila memakai LibreOffice sebagai penyunting utama, buat keterangan dengan Insert → Caption → Options → *Numbering by chapter*, Level 1. Kamus pengguna `kamus-mti-libreoffice.dic` dapat dipakai terpisah lewat Writing Aids → User-defined dictionaries.

## 3. WPS Office dan Google Docs

Belum diuji. WPS Office dapat membuka .dotx dan .docx, dan tanda pemenggal opsional adalah bagian standar format .docx, sehingga hasil `pemenggal-id.html` seharusnya tetap berfungsi; periksa sendiri sebelum dicetak. Untuk Google Docs, kami tidak dapat memastikan tanda pemenggal opsional dipertahankan saat .docx diimpor. Untuk naskah akhir, gunakan Word, LibreOffice, atau LaTeX.

## 4. LaTeX (pdfLaTeX, XeLaTeX, LuaLaTeX, Overleaf)

`tesis.tex` adalah contoh naskah lengkap dengan kelas `mti-unla.cls`; hasilnya ada di `contoh-tesis.pdf`. Kelas ini sudah mengatur ukuran kertas, margin, huruf, spasi, judul bab ("Bab I" + judul), penomoran gambar/tabel/persamaan per bab (III.1), daftar lampiran, halaman judul, pengesahan, abstrak, dan daftar pustaka nama-tahun ("dkk.").

**Kompilator yang disarankan: LuaLaTeX.** Hanya LuaLaTeX yang dapat mengganti pola pemenggalan saat kompilasi, sehingga pola MTI dipakai penuh. Pada pdfLaTeX dan XeLaTeX, pola bawaan babel (1997) tetap dipakai, tetapi kelas memuat `mti-hyph-id.tex` yang memperbaiki sekitar 4.000 kata yang salah dipenggal pola bawaan (mis. *buk-an* → *bu-kan*, *me-la-kuk-an* → *me-la-ku-kan*). Ketiga kompilator sudah diuji tanpa galat.

```
latexmk -lualatex tesis       # atau: lualatex, biber, lualatex, lualatex
```

**Overleaf:** New Project → Upload Project → pilih `templat-latex-overleaf.zip`, lalu Menu → Compiler → **LuaLaTeX**. Biber dijalankan otomatis.

Pilihan kelas: `\documentclass[satusisi]{mti-unla}` (cetak satu muka), `draf` (tandai baris yang melewati margin), `tanpapola` (pola bawaan saja), `polabaku` (pola autohyphen-id `hyph-id-baku.tex` alih-alih pola MTI, khusus LuaLaTeX), `tanpabiblatex` (atur daftar pustaka sendiri).

Hal yang perlu diketahui:

- Istilah asing ditulis `\asing{machine learning}`: dicetak miring dan dipenggal dengan kaidah bahasa Inggris. Nama produk ditulis `\produk{Raspberry Pi}`: tegak, tidak dipenggal.
- Kata yang masih salah dipenggal diperbaiki di pembukaan naskah: `\babelhyphenation[indonesian]{Rasp-ber-ry}`. Untuk mencegah satu kata dipenggal, tulis tanpa tanda hubung: `\babelhyphenation[indonesian]{Python}`.
- Daftar pustaka memakai biblatex + biber dengan gaya pada `mti-biblatex.sty` dan istilah Indonesia pada `indonesian.lbx`. Sitasi: `\parencite{kunci}` → (Kramer dkk., 2005), `\textcite{kunci}` → Kramer dkk. (2005), `\parencite[23]{kunci}` → (Baker, 1998: 23). `\cetakdaftarpustaka` mengelompokkan pustaka utama, surat kabar, film/TV, dan situs internet. Contoh entri setiap jenis ada di `pustaka.bib`.
- Pemeriksa ejaan di penyunting LaTeX (TeXstudio, VS Code + LTeX, Overleaf) memakai kamus Hunspell bahasa Indonesia; daftar istilah di `kamus-mti.txt` dapat ditambahkan sebagai kamus pengguna.

## 5. Gaya sitasi untuk Zotero/Mendeley (`mti-unla.csl`)

Zotero: Settings → Cite → Styles → tombol **+** → pilih `mti-unla.csl`. Mendeley dan pengelola pustaka lain yang menerima berkas CSL dapat memakainya juga. pandoc: `--citeproc --csl mti-unla.csl`. Hasilnya sudah dicocokkan dengan contoh pada Lampiran Q pedoman.

## 6. Tentang pola pemenggalan

Pola bawaan yang ada untuk bahasa Indonesia banyak salah, misalnya pola TeX/babel memenggal *buk-an*, *me-la-kuk-an*, *mak-an*, dan pola bawaan LibreOffice memenggal *de-ng-an*, *me-mi-l-iki*. Paket ini menyediakan dua pola pengganti:

1. **Pola gabungan MTI UnLa** (`hyph-id-mti.pat`, `hyph_id_ID_MTI.dic`; bawaan semua alat). Pola ini menggabungkan kaidah suku kata autohyphen-id dengan analisis imbuhan. Dibangkitkan dengan `patgen` dari sekitar 1,8 juta kata (kata dasar kamus Hunspell bahasa Indonesia beserta bentuk berimbuhannya) yang dipenggal oleh penganalisis kaidah EYD Edisi V, lalu dilengkapi daftar pengecualian berisi ±12.800 kata kamus yang masih salah atau kurang dipenggal oleh pola, sehingga semua kata dalam kamus dipenggal sesuai acuan. Kaidahnya:
   - kata dasar per suku kata: *ba-ca*, *Ap-ril*, *put-ra*, *ag-re-si* (dua konsonan di tengah kata dipisah), *in-stru-men*, *ul-tra* (tiga konsonan dipisah setelah yang pertama), *eks-pe-ri-men*, *trans-por-ta-si*; diftong *ai, au, ei, oi* utuh (*pan-tai*, *pu-lau*) kecuali sebelum konsonan penutup (*ba-ik*, *la-ut*);
   - kata berimbuhan dipenggal di antara unsurnya: *ber-a-da*, *meng-a-na-li-sis*, *ma-kan-an*, *ha-rap-an*, *ke-cer-das-an*, *pem-be-la-jar-an*;
   - bentuk dasar yang luluh dipenggal seperti kata dasar (Catatan EYD V): *pe-ne-li-ti-an*, *pe-ngem-bang-an*, *me-ne-rap-kan*, *pem-ro-gram-an*.
2. **Pola autohyphen-id** (`hyph_id_ID-baku.dic`, `hyph-id-baku.tex`, berkas asli di `pola/autohyphen-id/`, lisensi CC0). Disusun dari kaidah suku kata ditambah ±30 pengecualian kata berimbuhan. Kaidah suku katanya rapi (pola MTI memperbaiki penanganan gugus konsonan berdasarkan pola ini), tetapi tanpa analisis imbuhan sehingga sebagian besar kata berakhiran *-an* dan berawalan *ber-/ter-/meng-* sebelum vokal dipenggal secara fonetis (*ha-ra-pan*, *ke-se-ha-tan*, *be-ra-da*, *te-ra-khir*). Pola ini juga memenggal *peng-em-bang-an*, padahal menurut Catatan EYD V bentuk dasar yang luluh dipenggal *pe-ngem-bang-an*.

   Untuk kasus yang berbeda konvensi, pola gabungan mengikuti EYD V. Kata berimbuhan dipenggal di antara bentuk dasar dan imbuhannya, seperti contoh EYD V *ber-ja-lan*, *di-am-bil*, dan *ma-kan-an*. Karena itu pola gabungan memakai *ha-rap-an*, *ber-a-da*, dan *peng-u-ji-an*, bukan *ha-ra-pan*, *be-ra-da*, dan *pe-ngu-ji-an*. Pengecualiannya adalah bentuk dasar yang luluh: menurut Catatan EYD V bentuk itu dipenggal seperti kata dasar, seperti contoh *me-nu-tup* dan *pe-nga-rang*. Karena itu pola gabungan memakai *pe-ngem-bang-an*, bukan *peng-em-bang-an*.

Ekstensi LibreOffice `id_hyph_baku.oxt` dari autohyphen-id dan `pemenggalan-ejaan-id-mti.oxt` sama-sama mendaftarkan pemenggal untuk bahasa Indonesia; pasang salah satu saja.

**Uji di luar sampel.** Berikut hasil pada 20.000 bentuk kata yang tidak dipakai melatih pola dan tidak termasuk 40.000 kata tersering, sebagian besar kata berimbuhan yang jarang muncul. Angkanya adalah persentase kata yang memuat sedikitnya satu titik penggalan salah, dengan pola saja tanpa daftar pengecualian. Uji ini mengukur seberapa baik pola menebak kata baru di luar kamus.

| Pola | Kata salah |
|---|---|
| Pola TeX hyph-id (bawaan babel) | 37,9% |
| Pola LibreOffice hyph_id_ID | 35,5% |
| Pola autohyphen-id | 28,7% |
| Pola MTI versi pertama (data latih ¼) | 0,55% |
| **Pola gabungan MTI** (data latih ½) | **0,48%** |

Sebagian besar sisa kesalahan berasal dari bentuk yang jarang dipakai dan ambigu, misalnya *meng-ong-kang-nya*, *per-lis-trik-an*, dan *mem-pe-ra-ngin-ku*.

**Uji pada kata tersering.** Hasil uji terhadap ±20.000 kata Indonesia tersering yang akarnya dikenal kamus, dibandingkan dengan penggalan menurut kaidah di atas (persentase kata yang memuat sedikitnya satu titik penggalan salah; bobot frekuensi = seberapa sering kata salah itu muncul dalam teks):

| Pola | Kata salah | Bobot frekuensi |
|---|---|---|
| Pola TeX hyph-id (bawaan babel) | 20,4% (4096 dari 20053) | 9,3% |
| Pola TeX hyph-id + mti-hyph-id.tex | 0,0% (0 dari 20053) | 0,0% |
| Pola LibreOffice hyph_id_ID | 10,3% (2064 dari 20053) | 5,0% |
| Pola autohyphen-id (hyph_id_ID-baku.dic) | 13,2% (2643 dari 20053) | 4,9% |
| Pola MTI tanpa pengecualian | 0,9% (176 dari 20053) | 0,3% |
| Pola MTI + pengecualian | 0,0% (0 dari 20053) | 0,0% |

Angka 0% untuk pola dengan pengecualian adalah hasil pada kata yang sama dengan yang dipakai menyusun daftar pengecualian, jadi bukan ukuran untuk kata di luar daftar itu; ukuran untuk kata di luar kamus adalah uji di luar sampel di atas. Acuan uji ini adalah penganalisis kaidah yang juga dipakai melatih pola MTI, sehingga perbandingannya menguntungkan pola MTI. Sebagai pembanding, pada daftar uji milik autohyphen-id (`pola/autohyphen-id/test_hyph.py`, 108 kata; 5 kata seperti *a-ir* dan *di-a* tidak dapat dibandingkan karena paket ini tidak menyisakan satu huruf di tepi kata) pola MTI cocok pada 97 dari 103 kata. Keenam perbedaannya adalah soal konvensi, bukan penggalan yang melanggar suku kata: *eks-tra*/*ek-stra*, *eks-pe-ri-men*/*ek-spe-ri-men*, *per-a-tur-an*/*pe-ra-tur-an*, *peng-u-ji-an*/*pe-ngu-ji-an*, *ha-rap-an*/*ha-ra-pan*, dan *pe-ngem-bang-an*/*peng-em-bang-an* (bentuk pertama adalah pola MTI). Rincian ada di `pola/laporan.txt`. Bila menemukan kata yang salah dipenggal, laporkan lewat *issue* di repositori agar dimasukkan ke daftar pengecualian.

## 7. Lisensi

- Pola pemenggalan (`hyph-id-mti.pat`, `hyph_id_ID_MTI.dic`) dan kamus istilah: LGPL-3.0, karena dibangkitkan dari kamus Hunspell bahasa Indonesia (hunspell-id, LGPL-3.0).
- Kamus Hunspell `id_ID` di dalam ekstensi LibreOffice: LGPL-3.0, dari proyek hunspell-id.
- Templat Word, kelas LaTeX, gaya biblatex, dan alat pemenggal: LGPL-3.0 (berkas `LICENSE`); bebas dipakai untuk menulis tesis tanpa kewajiban apa pun atas naskah yang dihasilkan.
- Gaya CSL: CC BY-SA 3.0, sesuai kebiasaan repositori gaya CSL.
- Kamus pemenggalan autohyphen-id (`pola/autohyphen-id/`, `hyph_id_ID-baku.dic`, `hyph-id-baku.tex`): CC0 / domain publik, sesuai kepala berkasnya.
- `pemenggal-id.html` memuat JSZip 3.10.1 (MIT).
