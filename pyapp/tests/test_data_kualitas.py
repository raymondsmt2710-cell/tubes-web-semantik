"""Test kualitas data museum (tugas A1).

Berkas ini menjaga dua hal yang mudah rusak diam-diam:

1. **Setiap museum punya cukup foto.** Galeri dengan satu foto membuat halaman
   museum terasa kosong dan tidak memberi pembaca pilihan sudut pandang.
2. **Setiap foto punya kredit dan lisensi yang sah.** Foto tanpa lisensi jelas
   adalah risiko hukum, bukan sekadar cacat tampilan. Daftar lisensi yang
   diizinkan diambil apa adanya dari tugas A1: CC0, CC BY, CC BY-SA, dan
   domain publik. Tidak ada pengecualian.

Test ini memeriksa `data/museums.json` yang sebenarnya, bukan fixture. Dengan
begitu ia berfungsi sebagai gerbang: data yang melanggar aturan lisensi tidak
bisa masuk tanpa ketahuan.
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
