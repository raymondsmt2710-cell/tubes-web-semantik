"""Test kualitas data museum (tugas A1 dan A4).

Berkas ini menjaga hal-hal yang mudah rusak diam-diam:

1. **Setiap museum punya cukup foto.** Galeri dengan satu foto membuat halaman
   museum terasa kosong dan tidak memberi pembaca pilihan sudut pandang.
2. **Setiap foto punya kredit dan lisensi yang sah.** Foto tanpa lisensi jelas
   adalah risiko hukum, bukan sekadar cacat tampilan. Daftar lisensi yang
   diizinkan diambil apa adanya dari tugas A1: CC0, CC BY, CC BY-SA, dan
   domain publik. Tidak ada pengecualian.
3. **Setiap museum punya minimal dua sumber.** Satu sumber berarti tidak ada
   yang bisa dipakai untuk memeriksa silang; klaim tanpa pembanding adalah
   klaim yang tidak diperiksa. Dua sumber juga yang membuat status
   ``terverifikasi`` punya arti.

Test ini memeriksa `data/museums.json` yang sebenarnya, bukan fixture. Dengan
begitu ia berfungsi sebagai gerbang: data yang melanggar aturan lisensi atau
yang sumbernya kurang tidak bisa masuk tanpa ketahuan.
"""

from __future__ import annotations

import json
from pathlib import Path

AKAR = Path(__file__).resolve().parents[2]
BERKAS_DATA = AKAR / "data" / "museums.json"
AKAR_GAMBAR = AKAR / "public"

# Daftar lisensi yang diizinkan tugas A1. Dibandingkan setelah dinormalkan
# (huruf kecil, spasi dirapatkan) supaya "CC BY-SA 4.0" dan "cc by-sa 4.0"
# diperlakukan sama.
LISENSI_DIIZINKAN = (
    "cc0",
    "cc by",
    "cc by-sa",
    "public domain",
)

MINIMAL_FOTO = 2
MINIMAL_LATAR = 220
MINIMAL_POIN = 2
MAKSIMAL_POIN = 4

# Tugas A4: setiap museum harus diperiksa terhadap minimal dua sumber.
MINIMAL_SUMBER = 2

# Pengecualian yang didokumentasikan, bukan dilonggarkan diam-diam.
#
# `museum-sisingamangaraja-xii` tidak dapat diverifikasi: tidak terdaftar di
# NPNM (19 museum Sumatera Utara), tidak punya artikel Wikipedia, tidak ada di
# indonesia.travel, museum.co.id, maupun Wikidata, dan OpenStreetMap tidak
# dapat dihubungi saat pengecekan. Satu-satunya sumber yang ada adalah artikel
# biografi Sisingamangaraja XII, yang tidak menyebut museum. Sesuai tugas A4
# ("jangan dipaksa"), record dibiarkan `perlu-verifikasi` dengan sumber
# seadanya dan dicatat sebagai temuan yang belum selesai, bukan diisi sumber
# yang tidak benar-benar mendukung klaimnya.
SUMBER_DIKECUALIKAN = {
    "museum-sisingamangaraja-xii": "tidak dapat diverifikasi dari sumber mana pun",
}


def muat() -> list[dict]:
    return json.loads(BERKAS_DATA.read_text(encoding="utf-8"))


def normal_lisensi(teks: str | None) -> str:
    return " ".join((teks or "").lower().split())


def lisensi_diizinkan(teks: str | None) -> bool:
    """Benar bila lisensi termasuk daftar A1.

    ``GFDL`` sengaja TIDAK lolos: ia tidak ada di daftar tugas A1, dan
    memasukkannya berarti melonggarkan aturan yang tertulis "tidak ada
    pengecualian".
    """
    nilai = normal_lisensi(teks)
    if not nilai:
        return False
    if "gfdl" in nilai or "gpl" in nilai:
        return False
    return any(nilai.startswith(diizinkan) for diizinkan in LISENSI_DIIZINKAN)


def galeri(record: dict) -> list[dict]:
    return record.get("gallery") or []


# ------------------------------------------------------------- jumlah foto


def test_setiap_museum_punya_minimal_dua_foto():
    kurang = [
        f"{r['slug']} ({len(galeri(r))} foto)"
        for r in muat()
        if len(galeri(r)) < MINIMAL_FOTO
    ]
    assert kurang == [], (
        f"{len(kurang)} museum punya kurang dari {MINIMAL_FOTO} foto: "
        + ", ".join(kurang)
    )


# ----------------------------------------------------------------- lisensi


def test_semua_foto_berlisensi_diizinkan():
    """Hanya CC0, CC BY, CC BY-SA, dan domain publik yang boleh dipakai."""
    pelanggar = []
    for r in muat():
        for i, foto in enumerate(galeri(r), start=1):
            if not lisensi_diizinkan(foto.get("license")):
                pelanggar.append(
                    f"{r['slug']} foto ke-{i}: lisensi {foto.get('license')!r}"
                )
    assert pelanggar == [], "lisensi di luar daftar A1: " + "; ".join(pelanggar)


def test_setiap_foto_punya_kredit_lisensi_dan_tautan_sumber():
    """Kredit tidak boleh kosong dan tautan sumber wajib ada.

    Untuk foto domain publik ``licenseUrl`` boleh kosong karena tidak ada
    halaman lisensi yang bisa ditautkan, tetapi ``license`` dan ``credit``
    tetap wajib diisi.
    """
    pelanggar = []
    for r in muat():
        for i, foto in enumerate(galeri(r), start=1):
            for bidang in ("credit", "license", "sourceUrl"):
                if not str(foto.get(bidang) or "").strip():
                    pelanggar.append(f"{r['slug']} foto ke-{i}: {bidang} kosong")
            # Foto berlisensi CC wajib punya halaman lisensi yang bisa dibuka.
            if lisensi_diizinkan(foto.get("license")) and "public domain" not in normal_lisensi(
                foto.get("license")
            ):
                if not str(foto.get("licenseUrl") or "").strip():
                    pelanggar.append(
                        f"{r['slug']} foto ke-{i}: licenseUrl kosong padahal lisensinya "
                        f"{foto.get('license')!r}"
                    )
    assert pelanggar == [], "; ".join(pelanggar)


def test_tautan_sumber_memakai_http():
    pelanggar = [
        f"{r['slug']} foto ke-{i}: {foto.get('sourceUrl')!r}"
        for r in muat()
        for i, foto in enumerate(galeri(r), start=1)
        if not str(foto.get("sourceUrl") or "").startswith("http")
    ]
    assert pelanggar == [], "sourceUrl bukan URL http: " + "; ".join(pelanggar)


# ------------------------------------------------------------ kedalaman isi


def test_setiap_foto_punya_latar_belakang_cukup_panjang():
    pelanggar = []
    for r in muat():
        for i, foto in enumerate(galeri(r), start=1):
            panjang = len(str(foto.get("background") or "").strip())
            if panjang < MINIMAL_LATAR:
                pelanggar.append(f"{r['slug']} foto ke-{i}: {panjang} karakter")
    assert pelanggar == [], (
        f"latar belakang kurang dari {MINIMAL_LATAR} karakter: " + "; ".join(pelanggar)
    )


def test_setiap_foto_punya_dua_sampai_empat_poin_pengamatan():
    pelanggar = []
    for r in muat():
        for i, foto in enumerate(galeri(r), start=1):
            jumlah = len(foto.get("detail") or [])
            if not MINIMAL_POIN <= jumlah <= MAKSIMAL_POIN:
                pelanggar.append(f"{r['slug']} foto ke-{i}: {jumlah} poin")
    assert pelanggar == [], (
        f"jumlah poin pengamatan harus {MINIMAL_POIN}–{MAKSIMAL_POIN}: "
        + "; ".join(pelanggar)
    )


# --------------------------------------------------------- berkas gambarnya


def test_berkas_foto_lokal_benar_benar_ada():
    """Setiap ``src`` lokal harus menunjuk berkas yang ada di ``public/``.

    Rujukan ke berkas yang tidak ada akan tampil sebagai gambar rusak di
    halaman museum, dan tidak ada test lain yang menangkapnya.
    """
    hilang = []
    for r in muat():
        for i, foto in enumerate(galeri(r), start=1):
            src = str(foto.get("src") or "")
            if not src.startswith("/"):
                continue  # URL absolut, tidak diperiksa di sini
            if not (AKAR_GAMBAR / src.lstrip("/")).exists():
                hilang.append(f"{r['slug']} foto ke-{i}: {src}")
    assert hilang == [], "berkas gambar tidak ditemukan: " + "; ".join(hilang)


def test_tidak_ada_src_ganda_dalam_satu_museum():
    """Dua entri galeri dengan berkas sama berarti satu foto dihitung dua kali."""
    ganda = []
    for r in muat():
        terlihat = set()
        for i, foto in enumerate(galeri(r), start=1):
            src = str(foto.get("src") or "")
            if src in terlihat:
                ganda.append(f"{r['slug']} foto ke-{i}: {src}")
            terlihat.add(src)
    assert ganda == [], "src ganda: " + "; ".join(ganda)


# ------------------------------------------------------------- sumber (A4)


def sumber(record: dict) -> list[dict]:
    return record.get("sources") or []


def test_setiap_museum_punya_minimal_dua_sumber():
    """Tugas A4: satu sumber tidak bisa diperiksa silang, dua bisa.

    Pengecualian hanya yang tercatat di ``SUMBER_DIKECUALIKAN``; daftar itu
    ikut diuji supaya tidak menjadi tempat menyembunyikan museum yang lupa
    dilengkapi.
    """
    kurang = [
        f"{r['slug']} ({len(sumber(r))} sumber)"
        for r in muat()
        if len(sumber(r)) < MINIMAL_SUMBER
        and r["slug"] not in SUMBER_DIKECUALIKAN
    ]
    assert kurang == [], (
        f"{len(kurang)} museum punya kurang dari {MINIMAL_SUMBER} sumber: "
        + ", ".join(kurang)
    )


def test_pengecualian_sumber_masih_relevan():
    """Daftar pengecualian tidak boleh menyimpan museum yang sudah lengkap.

    Bila sebuah museum kelak berhasil diverifikasi, entri pengecualiannya harus
    dihapus. Kalau tidak, pengecualian itu berubah dari catatan jujur menjadi
    celah yang tidak disadari.
    """
    slugs = {r["slug"]: r for r in muat()}
    usang = [
        slug
        for slug in SUMBER_DIKECUALIKAN
        if slug in slugs and len(sumber(slugs[slug])) >= MINIMAL_SUMBER
    ]
    assert usang == [], "pengecualian sudah tidak perlu: " + ", ".join(usang)
    hilang = [slug for slug in SUMBER_DIKECUALIKAN if slug not in slugs]
    assert hilang == [], "pengecualian menunjuk museum yang tidak ada: " + ", ".join(hilang)


def test_setiap_sumber_punya_label_dan_url_http():
    """Sumber tanpa label atau tanpa URL tidak bisa dibuka pembaca."""
    pelanggar = []
    for r in muat():
        for i, s in enumerate(sumber(r), start=1):
            if not str(s.get("label") or "").strip():
                pelanggar.append(f"{r['slug']} sumber ke-{i}: label kosong")
            if not str(s.get("url") or "").startswith("http"):
                pelanggar.append(f"{r['slug']} sumber ke-{i}: url {s.get('url')!r}")
    assert pelanggar == [], "; ".join(pelanggar)


def test_tidak_ada_url_sumber_ganda_dalam_satu_museum():
    """Dua entri dengan URL sama bukan dua sumber; ia satu sumber dihitung dua kali."""
    ganda = []
    for r in muat():
        terlihat = set()
        for i, s in enumerate(sumber(r), start=1):
            url = str(s.get("url") or "").strip().rstrip("/")
            if url in terlihat:
                ganda.append(f"{r['slug']} sumber ke-{i}: {url}")
            terlihat.add(url)
    assert ganda == [], "URL sumber ganda: " + "; ".join(ganda)


def test_status_verifikasi_hanya_nilai_yang_dikenal():
    """Status di luar dua nilai yang dikenal akan tampil sebagai badge kosong."""
    dikenal = {"terverifikasi", "perlu-verifikasi"}
    pelanggar = [
        f"{r['slug']}: {r['verificationStatus']!r}"
        for r in muat()
        if r.get("verificationStatus") not in dikenal
    ]
    assert pelanggar == [], "; ".join(pelanggar)


def test_museum_terverifikasi_punya_tahun_berdiri():
    """Museum yang statusnya ``terverifikasi`` sudah diperiksa tahun berdirinya.

    Bila tahunnya tetap kosong, status itu tidak bisa dipertanggungjawabkan:
    tahun berdiri termasuk bidang yang wajib diperiksa pada tugas A4.
    """
    pelanggar = [
        r["slug"]
        for r in muat()
        if r.get("verificationStatus") == "terverifikasi"
        and not isinstance(r.get("establishedYear"), int)
    ]
    assert pelanggar == [], (
        "museum terverifikasi tanpa tahun berdiri: " + "; ".join(pelanggar)
    )
