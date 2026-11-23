from hyph_id import hyphenate
GOLD = """pan-tai ke-las se-ko-lah kom-pu-ter pe-nge-ta-hu-an pe-ne-li-ti-an ba-ha-sa ma-ha-sis-wa al-go-rit-ma
in-for-ma-ti-ka tek-nik ber-bi-ca-ra bang-sa me-nya-nyi sya-rat khu-sus a-khir ikh-las res-to-ran
in-ter-na-si-o-nal ke-bu-da-ya-an a-ngin de-ngan meng-kri-tik kon-struk-si in-struk-si ek-stra
ek-spe-ri-men ap-li-ka-si sis-tem a-na-li-sis ma-in ba-ik a-ir la-ut sau-da-ra pu-lau ha-ri-mau
kon-tras put-ra sas-tra ul-tra mang-ga tang-ga ang-ka ang-gur ba-nyak pe-nya-kit mu-sya-wa-rah
pro-gram pro-fe-sor ob-yek sub-yek ab-strak per-ta-ma kar-ya trans-por-ta-si tran-sak-si
trans-for-ma-si trans-krip-si trans-pa-ran bah-wa ka-lau ker-bau bu-ah ku-at di-a mem-ba-ca
ter-ba-ca ma-kan-an mi-num-an pem-be-la-jar-an pem-ba-ngun-an pen-di-dik-an per-ban-ding-an
pe-ran-cang-an bi-lang-an ke-bu-tuh-an pe-ra-tur-an peng-em-bang-an pem-ro-gram-an
pem-be-la-jar-an-nya ber-nya-nyi pe-ngu-ji-an ke-ma-ju-an pe-ker-ja-an kom-pleks da-ta-ba-se
ma-sya-ra-kat me-ngi-kuti? bo-i-kot? boi-kot ko-in pe-nga-wa-san ke-ter-se-dia-an?
san-tai ba-ngun ma-ha-pe-ser-ta-di-dik ber-ba-ha-sa ha-ra-pan ber-ja-lan ber-sa-ma-sa-ma
pe-ngem-ba-ngan? te-lek-ko-mu-ni-ka-si ma-te-ma-ti-ka fi-lo-so-fi pe-me-rin-tah ke-per-lu-an
se-ba-gai-ma-na ung-kap-an? mo-de-ra-si ka-pa-bi-li-tas im-ple-men-ta-si im-ple-men-tas?""".split()
bad = tot = 0
for g in GOLD:
    if g.endswith("?"): continue
    tot += 1
    out = hyphenate(g.replace("-", ""), left=1, right=1)
    if out != g:
        bad += 1; print("BEDA", g, "->", out)
print(f"{tot-bad}/{tot} cocok")
