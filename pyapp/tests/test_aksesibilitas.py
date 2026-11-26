"""Test aksesibilitas (tugas D2).

Pemeriksaan otomatis yang bisa dijalankan tanpa browser. Ini **bukan** pengganti
axe DevTools, tetapi menjaga agar aturan dasar tidak rusak diam-diam:

- kontras warna teks di ``style.css`` memenuhi WCAG AA (4.5:1),
- ada skip-link ke ``<main>``, ``lang`` terisi, satu ``<h1>`` per halaman,
- setiap ``<img>`` punya ``alt`` bermakna, setiap kontrol formulir berlabel,
- navigasi menandai halaman aktif dengan ``aria-current``,
- tidak ada ``tabindex`` positif yang mengacak urutan Tab.
"""

from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from main import app

CSS = (Path(__file__).resolve().parents[1] / "static" / "style.css").read_text(encoding="utf-8")

HALAMAN = [
    "/",
    "/cari",
    "/cari?q=aceh",
    "/museum/museum-negeri-aceh",
    "/tanya",
    "/tanya?q=museum+apa+saja+di+Aceh%3F",
    "/metode",
    "/peta",
    "/peta?provinsi=Aceh",
]


# --------------------------------------------------------------------- kontras


def _var(nama: str) -> str:
    cocok = re.search(rf"--{nama}:\s*(#[0-9a-fA-F]{{6}})", CSS)
    assert cocok, f"variabel --{nama} tidak ditemukan di style.css"
    return cocok.group(1)


def _luminans(hex_: str) -> float:
    kanal = [int(hex_[i : i + 2], 16) / 255 for i in (1, 3, 5)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in kanal]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def kontras(a: str, b: str) -> float:
    terang, gelap = sorted((_luminans(a), _luminans(b)), reverse=True)
    return (terang + 0.05) / (gelap + 0.05)


LATAR = ["paper", "paper-2", "accent-soft"]
TEKS = ["ink", "ink-soft", "ink-faint", "accent", "ok", "warn"]


@pytest.mark.parametrize("latar", LATAR)
@pytest.mark.parametrize("teks", TEKS)
def test_kontras_teks_wcag_aa(teks, latar):
    nilai = kontras(_var(teks), _var(latar))
    assert nilai >= 4.5, f"--{teks} di atas --{latar}: {nilai:.2f}:1 (< 4.5:1)"


def test_kontras_badge_status():
    # Pasangan warna yang ditulis langsung di CSS untuk .status.*
    for teks, latar in [("ok", "#e2efe6"), ("accent", "#f7e6dc"), ("warn", "#efeade")]:
        assert kontras(_var(teks), latar) >= 4.5


def test_batas_kontrol_formulir_terlihat():
    """WCAG 1.4.11: batas input butuh kontras 3:1 terhadap latar."""
    assert kontras(_var("rule-kuat"), _var("paper-2")) >= 3.0
    assert kontras(_var("rule-kuat"), _var("paper")) >= 3.0


def test_fokus_keyboard_terlihat():
    assert ":focus-visible" in CSS
    assert ".lompat" in CSS


# ---------------------------------------------------------------------- HTML


class _Pemeriksa(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.lang = None
        self.h1 = 0
        self.img_tanpa_alt: list[str] = []
        self.ids: set[str] = set()
        self.label_for: set[str] = set()
        self.kontrol: list[tuple[str, dict]] = []
        self.dalam_label = 0
        self.tautan_pertama: dict | None = None
        self.aria_current = 0
        self.tabindex_positif = 0
        self.blank_tanpa_rel: list[str] = []
        self.heading: list[int] = []
        self.pre_tanpa_fokus = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "h1":
            self.h1 += 1
        if re.fullmatch(r"h[1-6]", tag):
            self.heading.append(int(tag[1]))
        if tag == "pre" and a.get("tabindex") != "0":
            self.pre_tanpa_fokus += 1
        elif tag == "img":
            if not (a.get("alt") or "").strip():
                self.img_tanpa_alt.append(a.get("src", "?"))
        elif tag == "label":
            self.dalam_label += 1
            if a.get("for"):
                self.label_for.add(a["for"])
        elif tag in ("input", "select", "textarea"):
            if a.get("type") not in ("hidden", "submit", "button"):
                self.kontrol.append((tag, {**a, "_dalam_label": self.dalam_label > 0}))
        elif tag == "a":
            if self.tautan_pertama is None:
                self.tautan_pertama = a
            if a.get("aria-current") == "page":
                self.aria_current += 1
            if a.get("target") == "_blank" and "noopener" not in (a.get("rel") or ""):
                self.blank_tanpa_rel.append(a.get("href", "?"))
        ti = a.get("tabindex")
        if ti is not None and ti.lstrip("-").isdigit() and int(ti) > 0:
            self.tabindex_positif += 1

    def handle_endtag(self, tag):
        if tag == "label":
            self.dalam_label -= 1


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


@pytest.fixture(scope="module", params=HALAMAN)
def hasil(request, client):
    r = client.get(request.param)
    assert r.status_code == 200, request.param
    p = _Pemeriksa()
    p.feed(r.text)
    return request.param, p


def test_bahasa_halaman(hasil):
    _, p = hasil
    assert p.lang == "id"


def test_tepat_satu_h1(hasil):
    url, p = hasil
    assert p.h1 == 1, f"{url}: {p.h1} <h1>"


def test_skip_link_adalah_tautan_pertama(hasil):
    url, p = hasil
    assert p.tautan_pertama is not None
    target = p.tautan_pertama.get("href", "")
    assert target.startswith("#"), url
    assert target[1:] in p.ids, f"{url}: target skip-link {target} tidak ada"


def test_urutan_heading_tidak_melompat(hasil):
    """h1 -> h3 tanpa h2 membingungkan navigasi heading pembaca layar."""
    url, p = hasil
    for sebelum, sesudah in zip(p.heading, p.heading[1:]):
        assert sesudah <= sebelum + 1, f"{url}: h{sebelum} -> h{sesudah}"


def test_blok_kode_bisa_digulir_keyboard(hasil):
    """<pre> yang bisa digulir horizontal harus bisa difokus (tabindex=0)."""
    url, p = hasil
    assert p.pre_tanpa_fokus == 0, url


def test_gambar_punya_alt(hasil):
    url, p = hasil
    assert not p.img_tanpa_alt, f"{url}: {p.img_tanpa_alt}"


def test_kontrol_formulir_berlabel(hasil):
    url, p = hasil
    for tag, a in p.kontrol:
        berlabel = a["_dalam_label"] or a.get("aria-label") or a.get("id") in p.label_for
        assert berlabel, f"{url}: <{tag} name={a.get('name')}> tanpa label"


def test_navigasi_menandai_halaman_aktif(hasil):
    url, p = hasil
    assert p.aria_current <= 1, url


def test_tanpa_tabindex_positif(hasil):
    url, p = hasil
    assert p.tabindex_positif == 0, url


def test_tautan_tab_baru_aman(hasil):
    url, p = hasil
    assert not p.blank_tanpa_rel, f"{url}: {p.blank_tanpa_rel}"


def test_alt_galeri_bermakna(client):
    html = client.get("/museum/museum-negeri-aceh").text
    alt = re.findall(r'<img[^>]*alt="([^"]*)"', html)
    assert alt
    # alt tidak boleh sekadar nama berkas atau kata generik.
    for teks in alt:
        assert not re.search(r"\.(jpe?g|png|webp)$", teks, re.I)
        assert teks.lower() not in {"foto", "gambar", "image"}
