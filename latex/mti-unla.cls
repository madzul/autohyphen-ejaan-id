%% mti-unla.cls
%% Kelas LaTeX untuk tesis Program Studi Magister Teknik Informatika (MTI),
%% Pascasarjana Universitas Langlangbuana, mengikuti Pedoman Penulisan Tesis
%% Edisi Revisi 2026 (Bab III, IV, VI).
%%
%% Mesin yang didukung: pdfLaTeX, XeLaTeX, LuaLaTeX (dianjurkan), termasuk Overleaf.
%% Pemenggalan kata: babel bahasa Indonesia + pola MTI (LuaLaTeX) atau daftar
%% pengecualian \hyphenation (pdfLaTeX/XeLaTeX). Lihat README.
%%
%% Opsi kelas:
%%   satusisi   cetak satu muka (tepi kiri 4 cm); bawaan: bolak-balik (mirror margins)
%%   draf       tampilkan kotak hitam pada baris yang melewati batas tepi
%%   tanpapola  jangan memuat pola pemenggalan MTI (LuaLaTeX)
%%   polabaku   pakai pola autohyphen-id (hyph-id-baku.tex) alih-alih pola MTI (LuaLaTeX)
%%   tanpabiblatex  jangan memuat biblatex (bila memakai BibTeX/natbib sendiri)
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{mti-unla}[2026/11/23 v1.0 Templat tesis MTI UnLa]

\newif\if@mti@duasisi \@mti@duasisitrue
\newif\if@mti@pola    \@mti@polatrue
\newif\if@mti@bib     \@mti@bibtrue
\newif\if@mti@draf    \@mti@draffalse
\DeclareOption{satusisi}{\@mti@duasisifalse}
\DeclareOption{draf}{\@mti@draftrue}
\DeclareOption{tanpapola}{\@mti@polafalse}
\def\mti@berkaspola{hyph-id-mti.pat}
\DeclareOption{polabaku}{\def\mti@berkaspola{hyph-id-baku.tex}}
\DeclareOption{tanpabiblatex}{\@mti@bibfalse}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{report}}
\ProcessOptions\relax

\if@mti@duasisi
  \LoadClass[a4paper,12pt,twoside,openany]{report}
\else
  \LoadClass[a4paper,12pt,oneside,openany]{report}
\fi

\RequirePackage{iftex}

%% ---------------------------------------------------------------- huruf
%% Times New Roman 12. pdfLaTeX memakai newtx (bila ada) atau mathptmx;
%% XeLaTeX/LuaLaTeX memakai Times New Roman bila terpasang, selain itu TeX Gyre Termes.
\ifPDFTeX
  \RequirePackage[T1]{fontenc}
  \RequirePackage[utf8]{inputenc}
  \IfFileExists{newtxtext.sty}{%
    \RequirePackage{newtxtext}\RequirePackage{newtxmath}}{%
    \RequirePackage{mathptmx}}
\else
  \RequirePackage{unicode-math}
  \IfFontExistsTF{Times New Roman}{%
    \setmainfont{Times New Roman}}{%
    \setmainfont{TeX Gyre Termes}}
  \IfFontExistsTF{TeX Gyre Termes Math}{\setmathfont{TeX Gyre Termes Math}}{}
\fi

%% ---------------------------------------------------------------- bahasa
%% Bahasa utama Indonesia; bahasa Inggris untuk abstract dan istilah asing.
\RequirePackage[english,main=indonesian]{babel}
\RequirePackage{csquotes}
\DeclareQuoteStyle{indonesian}{\textquotedblleft}{\textquotedblright}{\textquoteleft}{\textquoteright}
%% Pemenggalan EYD V: sisa minimal dua huruf di awal dan akhir baris.
\providehyphenmins{indonesian}{22}
\babelhyphenation[indonesian]{}
\AtBeginDocument{\lefthyphenmin=2 \righthyphenmin=2 \frenchspacing}

%% Istilah asing: miring dan dipenggal dengan kaidah bahasa Inggris.
\newcommand{\asing}[1]{\foreignlanguage{english}{\textit{#1}}}
%% Nama produk, merek, bahasa pemrograman: tegak, tidak dipenggal.
\newcommand{\produk}[1]{\mbox{#1}}

%% ---------------------------------------------------------------- tata letak
%% A4; tepi dalam 4 cm, atas/luar/bawah 3 cm; nomor halaman 1,5 cm dari tepi bawah.
\RequirePackage[a4paper,inner=4cm,outer=3cm,top=3cm,bottom=3cm,
  footskip=1.5cm,headheight=15pt,headsep=0.5cm]{geometry}
\RequirePackage{setspace}
\onehalfspacing
\setlength{\parindent}{0pt}
\setlength{\parskip}{18pt plus 2pt minus 1pt}
\widowpenalty=10000
\clubpenalty=10000
\brokenpenalty=10000 % kata terakhir pada dasar halaman tidak dipenggal
\doublehyphendemerits=900000 % hindari pemenggalan pada dua baris berturut-turut
\finalhyphendemerits=50000
\emergencystretch=1.5em
\tolerance=600
\if@mti@draf \overfullrule=5pt \fi

%% microtype: protrusion untuk semua mesin; expansion untuk pdfLaTeX dan LuaLaTeX.
\ifXeTeX
  \RequirePackage[protrusion=true,expansion=false]{microtype}
\else
  \RequirePackage[protrusion=true,expansion=true,tracking=false,
    stretch=15,shrink=15,step=1]{microtype}
\fi

%% Nomor halaman di tengah bawah, Times 12.
\RequirePackage{emptypage}
\RequirePackage{fancyhdr}
\fancypagestyle{plain}{\fancyhf{}\fancyfoot[C]{\normalsize\thepage}%
  \renewcommand{\headrulewidth}{0pt}\renewcommand{\footrulewidth}{0pt}}
\pagestyle{plain}

%% ---------------------------------------------------------------- judul bab
%% "Bab I Pendahuluan": Times 14 tebal, rata tengah, 1,5 spasi, tepat di batas atas.
%% Subbab "I.1", anak subbab "I.1.1": Times 12 tebal, rata kiri, nomor diikuti tab.
\newlength{\mti@babatas}\setlength{\mti@babatas}{-40pt}
\renewcommand{\thechapter}{\Roman{chapter}}
\renewcommand{\thesection}{\thechapter.\arabic{section}}
\renewcommand{\thesubsection}{\thesection.\arabic{subsection}}
\setcounter{secnumdepth}{2}
\setcounter{tocdepth}{2}
\RequirePackage{titlesec}
\titleformat{\chapter}[block]
  {\centering\fontsize{14}{21}\selectfont\bfseries\nohyphens}
  {\chaptertitlename\ \thechapter\ }{0pt}{}
\titleformat{name=\chapter,numberless}[block]
  {\centering\fontsize{14}{21}\selectfont\bfseries\nohyphens}{}{0pt}{}
\titlespacing*{\chapter}{0pt}{\mti@babatas}{18pt}
\titleformat{\section}[hang]{\normalsize\bfseries\raggedright\nohyphens}
  {\makebox[1.5cm][l]{\thesection}}{0pt}{}
\titlespacing*{\section}{0pt}{0pt}{0pt}
\titleformat{\subsection}[hang]{\normalsize\bfseries\raggedright\nohyphens}
  {\makebox[2cm][l]{\thesubsection}}{0pt}{}
\titlespacing*{\subsection}{0pt}{0pt}{0pt}
\newcommand{\nohyphens}{\hyphenpenalty=10000\exhyphenpenalty=10000\relax}
\addto\captionsindonesian{%
  \renewcommand{\chaptername}{Bab}%
  \renewcommand{\appendixname}{Lampiran}%
  \renewcommand{\contentsname}{DAFTAR ISI}%
  \renewcommand{\listfigurename}{DAFTAR GAMBAR DAN ILUSTRASI}%
  \renewcommand{\listtablename}{DAFTAR TABEL}%
  \renewcommand{\bibname}{DAFTAR PUSTAKA}%
  \renewcommand{\figurename}{Gambar}%
  \renewcommand{\tablename}{Tabel}%
  \renewcommand{\abstractname}{ABSTRAK}}

%% Judul bagian tanpa nomor (ABSTRAK, KATA PENGANTAR, DAFTAR PUSTAKA, ...),
%% dimasukkan ke daftar isi.
\newcommand{\judulbagian}[1]{%
  \clearpage\phantomsection\addcontentsline{toc}{chapter}{#1}%
  \chapter*{#1}}
\newcommand{\judulbagiantanpaisi}[1]{\clearpage\chapter*{#1}}

%% ---------------------------------------------------------------- gambar, tabel, rumus
%% Nomor berbasis bab: Gambar III.1, Tabel III.1, (III.1).
\RequirePackage{graphicx}
\RequirePackage{booktabs,array,longtable}
\RequirePackage{amsmath}
\renewcommand{\thefigure}{\thechapter.\arabic{figure}}
\renewcommand{\thetable}{\thechapter.\arabic{table}}
\renewcommand{\theequation}{\thechapter.\arabic{equation}}
\RequirePackage{caption}
%% Judul gambar/tabel 1 spasi; satu baris rata tengah, lebih dari satu baris
%% rata kiri-kanan dengan indentasi gantung; tanpa pemenggalan.
\DeclareCaptionFont{mti}{\setstretch{1}\nohyphens}
\captionsetup{font={normalsize,mti},labelsep=space,format=hang,justification=justified,
  singlelinecheck=true,skip=6pt}
\captionsetup[figure]{position=bottom}
\captionsetup[table]{position=top}
\AtBeginEnvironment{tabular}{\singlespacing\nohyphens\raggedright}
\AtBeginEnvironment{longtable}{\singlespacing\nohyphens}
\RequirePackage{etoolbox}

%% Kutipan langsung lebih dari empat baris: 1 spasi, menjorok.
\renewenvironment{quote}{\list{}{\leftmargin=1.27cm\rightmargin=1.27cm}\item\relax\singlespacing}{\endlist}

%% Kode program: tidak dipenggal, huruf mesin tik.
\RequirePackage{listings}
\lstset{basicstyle=\ttfamily\small\singlespacing,columns=fullflexible,breaklines=true,
  keepspaces=true,showstringspaces=false,frame=single,framerule=0.4pt}

%% Daftar butir
\RequirePackage{enumitem}
\setlist{itemsep=0pt,topsep=0pt,parsep=0pt}

%% Daftar isi
\RequirePackage{tocloft}
\renewcommand{\cfttoctitlefont}{\hfill\fontsize{14}{21}\selectfont\bfseries}
\renewcommand{\cftaftertoctitle}{\hfill}
\renewcommand{\cftloftitlefont}{\hfill\fontsize{14}{21}\selectfont\bfseries}
\renewcommand{\cftafterloftitle}{\hfill}
\renewcommand{\cftlottitlefont}{\hfill\fontsize{14}{21}\selectfont\bfseries}
\renewcommand{\cftafterlottitle}{\hfill}
\setlength{\cftbeforetoctitleskip}{-\topskip}
\setlength{\cftbeforeloftitleskip}{-\topskip}
\setlength{\cftbeforelottitleskip}{-\topskip}
\setlength{\cftaftertoctitleskip}{18pt}
\setlength{\cftafterloftitleskip}{18pt}
\setlength{\cftafterlottitleskip}{18pt}
\renewcommand{\cftchappresnum}{\chaptername\ }
\renewcommand{\cftchapaftersnum}{}
\setlength{\cftchapnumwidth}{3.2em}
\renewcommand{\cftchapfont}{\normalfont}
\renewcommand{\cftchappagefont}{\normalfont}
\renewcommand{\cftchapleader}{\cftdotfill{\cftdotsep}}
\setlength{\cftsecindent}{1.5cm}\setlength{\cftsecnumwidth}{1.5cm}
\setlength{\cftsubsecindent}{3cm}\setlength{\cftsubsecnumwidth}{1.5cm}
\renewcommand{\cftfigpresnum}{\figurename\ }
\renewcommand{\cfttabpresnum}{\tablename\ }
\setlength{\cftfignumwidth}{6em}\setlength{\cfttabnumwidth}{5em}
\setlength{\cftfigindent}{0pt}\setlength{\cfttabindent}{0pt}
\setlength{\cftbeforechapskip}{6pt}
\AtBeginDocument{\addtocontents{toc}{\protect\singlespacing}%
  \addtocontents{lof}{\protect\singlespacing}\addtocontents{lot}{\protect\singlespacing}}

%% ---------------------------------------------------------------- lampiran
%% "Lampiran A Judul": Times 12 tebal, rata kiri; daftar lampiran terpisah.
\newcommand{\listappendixname}{DAFTAR LAMPIRAN}
\newlistof[chapter]{lampiran}{loa}{\listappendixname}
\renewcommand{\cftloatitlefont}{\hfill\fontsize{14}{21}\selectfont\bfseries}
\renewcommand{\cftafterloatitle}{\hfill}
\setlength{\cftbeforeloatitleskip}{-\topskip}
\setlength{\cftafterloatitleskip}{18pt}
\newcommand{\halamanlampiran}{%
  \clearpage\phantomsection\addcontentsline{toc}{chapter}{LAMPIRAN}%
  \thispagestyle{plain}\null\vfill
  \begin{center}\fontsize{14}{21}\selectfont\bfseries LAMPIRAN\end{center}\vfill\clearpage
  \appendix
  \renewcommand{\thechapter}{\Alph{chapter}}%
  \titleformat{\chapter}[block]{\raggedright\normalsize\bfseries\nohyphens}
    {\appendixname\ \thechapter}{0.5em}{}%
  \titlespacing*{\chapter}{0pt}{-\topskip}{12pt}%
  \renewcommand{\thesection}{\thechapter.\arabic{section}}%
  \renewcommand{\thefigure}{\thechapter.\arabic{figure}}%
  \renewcommand{\thetable}{\thechapter.\arabic{table}}}
\newcommand{\lampiran}[1]{%
  \refstepcounter{chapter}\clearpage\phantomsection
  \addcontentsline{loa}{lampiran}{\appendixname\ \thechapter\quad #1}%
  \addcontentsline{toc}{chapter}{\appendixname\ \thechapter\quad #1}%
  {\raggedright\normalsize\bfseries\nohyphens\singlespacing \appendixname\ \thechapter\ #1\par}%
  \vspace{6pt}}

%% ---------------------------------------------------------------- tautan
\RequirePackage{xurl}
\RequirePackage[hidelinks,unicode,bookmarksnumbered]{hyperref}
\urlstyle{same}

%% ---------------------------------------------------------------- pustaka
%% Sistem nama-tahun (Bab VI pedoman): (Hill, 2007), Gao dan Zhao (2009),
%% (Kramer dkk., 2005), (Baker dkk., 1998: 23–25), (Culver dkk., 2003a, 2003b).
\if@mti@bib
  \RequirePackage[backend=biber,style=authoryear-comp,maxcitenames=2,mincitenames=1,
    maxbibnames=99,giveninits=true,uniquename=false,uniquelist=false,dashed=false,
    sorting=nyt,date=year,urldate=long,isbn=false,eprint=false,language=autobib]{biblatex}
  \RequirePackage{mti-biblatex}
\fi

%% ---------------------------------------------------------------- data tesis
\newcommand{\@judul}{JUDUL TESIS}\newcommand{\judul}[1]{\renewcommand{\@judul}{#1}}
\newcommand{\@judulinggris}{Thesis Title}\newcommand{\judulinggris}[1]{\renewcommand{\@judulinggris}{#1}}
\newcommand{\@penulis}{Nama Lengkap}\newcommand{\penulis}[1]{\renewcommand{\@penulis}{#1}}
\newcommand{\@npm}{L2509xxxxx}\newcommand{\npm}[1]{\renewcommand{\@npm}{#1}}
\newcommand{\@bulantahun}{Bulan Tahun}\newcommand{\bulantahun}[1]{\renewcommand{\@bulantahun}{#1}}
\newcommand{\@pembimbingsatu}{Nama Pembimbing Pertama}\newcommand{\pembimbingsatu}[1]{\renewcommand{\@pembimbingsatu}{#1}}
\newcommand{\@pembimbingdua}{}\newcommand{\pembimbingdua}[1]{\renewcommand{\@pembimbingdua}{#1}}
\newcommand{\@lambang}{logo-unla}\newcommand{\lambang}[1]{\renewcommand{\@lambang}{#1}}

%% Halaman judul (sampul dalam), Lampiran A pedoman.
\newcommand{\buathalamanjudul}{%
  \begin{titlepage}\singlespacing\centering\nohyphens
  {\fontsize{14}{17}\selectfont\bfseries\MakeUppercase{\@judul}\par}
  \vspace{1.6cm}
  {\fontsize{14}{17}\selectfont\bfseries TESIS\par}
  \vspace{0.8cm}
  {\bfseries Karya tulis sebagai salah satu syarat\\untuk memperoleh gelar Magister dari\\Universitas Langlangbuana\par}
  \vspace{1.2cm}
  {\bfseries Oleh\par}\vspace{0.3cm}
  {\fontsize{14}{17}\selectfont\bfseries\MakeUppercase{\@penulis}\\NPM: \@npm\\(Program Studi Magister Teknik Informatika)\par}
  \vfill
  \IfFileExists{\@lambang}{\includegraphics[height=3.5cm]{\@lambang}}{\IfFileExists{\@lambang.png}{\includegraphics[height=3.5cm]{\@lambang}}{\fbox{\parbox[c][3.5cm][c]{3.5cm}{\centering Lambang UnLa}}}}\par
  \vfill
  {\fontsize{14}{17}\selectfont\bfseries UNIVERSITAS LANGLANGBUANA\\\@bulantahun\par}
  \end{titlepage}%
  \setcounter{page}{2}}

%% Abstrak (Lampiran B pedoman); lingkungan abstrak dan abstract.
\newenvironment{abstrak}{%
  \judulbagian{ABSTRAK}\begin{singlespace}\setlength{\parskip}{12pt}
  \begin{center}\nohyphens{\fontsize{14}{17}\selectfont\bfseries \@judul\par}\vspace{6pt}
  Oleh\par\vspace{6pt}{\fontsize{14}{17}\selectfont\bfseries \@penulis\\NPM: \@npm\\(Program Studi Magister Teknik Informatika)\par}\end{center}
  \vspace{24pt}}{\end{singlespace}}
\newenvironment{abstract*}{%
  \judulbagian{ABSTRACT}\begin{otherlanguage}{english}\begin{singlespace}\setlength{\parskip}{12pt}\itshape
  \begin{center}\nohyphens{\fontsize{14}{17}\selectfont\bfseries \@judulinggris\par}\vspace{6pt}
  \upshape by\par\vspace{6pt}{\fontsize{14}{17}\selectfont\bfseries \@penulis\\NPM: \@npm\\(Master's Program in Informatics Engineering)\par}\end{center}
  \vspace{24pt}}{\end{singlespace}\end{otherlanguage}}
\newcommand{\katakunci}[1]{\par\textbf{Kata kunci:} #1\par}
\newcommand{\keywords}[1]{\par\textbf{Keywords:} #1\par}

%% Halaman pengesahan (Lampiran F pedoman).
\newcommand{\buatpengesahan}{%
  \clearpage\thispagestyle{plain}\begin{singlespace}\centering\nohyphens
  {\fontsize{14}{17}\selectfont\bfseries\MakeUppercase{\@judul}\par}\vspace{0.8cm}
  Oleh\par\vspace{0.3cm}
  \textbf{\@penulis}\\\textbf{NPM: \@npm}\\\textbf{(Program Studi Magister Teknik Informatika)}\par\vspace{0.3cm}
  \textbf{Universitas Langlangbuana}\par\vspace{1.2cm}
  Menyetujui\\\ifx\@pembimbingdua\@empty Pembimbing\else Tim Pembimbing\fi\par\vspace{0.4cm}
  Tanggal \makebox[5cm]{\dotfill}\par\vspace{0.8cm}
  \ifx\@pembimbingdua\@empty
    \vspace{2cm}\rule{6cm}{0.4pt}\\(\@pembimbingsatu)\par
  \else
    \begin{tabular}{@{}c@{\hspace{1.5cm}}c@{}}
    Pembimbing Pertama & Pembimbing Kedua\\[2.5cm]
    \rule{5.5cm}{0.4pt} & \rule{5.5cm}{0.4pt}\\
    (\@pembimbingsatu) & (\@pembimbingdua)
    \end{tabular}\par
  \fi
  \end{singlespace}\clearpage}

%% Tanda tangan rata kiri di sisi kanan
\newenvironment{tandatangan}{\par\begin{singlespace}\hspace*{8cm}\begin{minipage}[t]{\dimexpr\textwidth-8cm}\raggedright}{\end{minipage}\end{singlespace}\par}

%% ---------------------------------------------------------------- pemenggalan
%% Daftar pengecualian kata (semua mesin) dan pola MTI (LuaLaTeX).
\InputIfFileExists{mti-hyph-id.tex}{}{\ClassWarningNoLine{mti-unla}{Berkas mti-hyph-id.tex tidak ditemukan}}
\if@mti@pola
  \ifLuaTeX
    \directlua{dofile(kpse.find_file('mti-pola.lua'))}
    \AtBeginDocument{\selectlanguage{indonesian}\directlua{mti_pola(\the\l@indonesian, '\mti@berkaspola')}}
  \fi
\fi

\endinput
