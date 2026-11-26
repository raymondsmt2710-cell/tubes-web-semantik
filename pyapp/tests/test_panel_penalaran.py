"""Panel putaran penalaran di /metode.

Kontrak dari Ryan F (Task 6, belum di-merge)::

    langkah_penalaran(store, batas_putaran=5) -> list[dict]
    {"putaran": int, "mentah": int, "informatif": int, "contoh": list[str]}

Halaman harus:
- menampilkan tabel putaran sampai fixpoint bila fungsinya ada,
- tidak menampilkan panel (dan tidak error) selama fungsinya belum ada,
- menghitung langkah sekali saja per store, bukan setiap kunjungan.
"""

from __future__ import annotations

import re

import pytest
from fastapi.testclient import TestClient

import main
from main import app, get_store
from semweb.store import MuseumStore

TTL = """
@prefix sdp: <https://museumsumatera.id/ontology#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
sdp:StateMuseum rdfs:subClassOf sdp:Museum .
<https://museumsumatera.id/resource/museum/aceh> a sdp:StateMuseum ;
    sdp:name "Museum Negeri Aceh"@id .
"""

# Bentuk keluaran nyata menurut pengukuran Ryan F.
LANGKAH = [
    {
        "putaran": 1,
        "mentah": 5320,
        "informatif": 375,
        "contoh": [
            "res:museum/museum-adityawarman rdf:type sdp:Museum",
            "res:museum/museum-aceh/exhibit/1 sdp:exhibitOfMuseum res:museum/museum-negeri-aceh",
        ],
    },
    {"putaran": 2, "mentah": 1346, "informatif": 0, "contoh": []},
    {"putaran": 3, "mentah": 0, "informatif": 0, "contoh": []},
]


@pytest.fixture()
def client(monkeypatch):
    def _buat(fungsi):
        store = MuseumStore.dari_turtle(data=TTL)
        monkeypatch.setattr(main, "langkah_penalaran", fungsi)
        app.dependency_overrides[get_store] = lambda: store
        return TestClient(app)

    yield _buat
    app.dependency_overrides.clear()


def _baris(html: str) -> list[list[str]]:
    tbody = re.search(r'<table class="putaran">.*?<tbody>(.*?)</tbody>', html, re.S).group(1)
    return [
        [" ".join(re.sub(r"<[^>]+>", " ", sel).split()) for sel in re.findall(r"<td>(.*?)</td>", tr, re.S)]
        for tr in re.findall(r"<tr>(.*?)</tr>", tbody, re.S)
    ]


def test_tabel_putaran_sampai_fixpoint(client):
    html = client(lambda s, batas_putaran=5: LANGKAH).get("/metode").text
    baris = _baris(html)
    assert [b[0] for b in baris] == ["1", "2", "3"]
    assert baris[0][1] == "5.320" and baris[0][2] == "375"
    assert baris[1][2] == "0"
    assert "res:museum/museum-adityawarman rdf:type sdp:Museum" in baris[0][3]
    assert "fixpoint tercapai pada putaran 3" in html


def test_menjelaskan_sifat_owlrl(client):
    html = client(lambda s, batas_putaran=5: LANGKAH).get("/metode").text
    assert "satu putaran" in html and "Mona Lisa" in html


def test_tanpa_fixpoint_dalam_batas(client):
    belum = LANGKAH[:2]
    html = client(lambda s, batas_putaran=5: belum).get("/metode").text
    assert "fixpoint tercapai" not in html
    assert "belum mencapai fixpoint" in html


def test_panel_disembunyikan_bila_fungsi_belum_ada(client):
    r = client(None).get("/metode")
    assert r.status_code == 200
    assert '<table class="putaran">' not in r.text
    assert "Putaran penalaran" not in r.text


def test_langkah_dihitung_sekali_per_store(client):
    panggilan = []

    def hitung(s, batas_putaran=5):
        panggilan.append(batas_putaran)
        return LANGKAH

    c = client(hitung)
    c.get("/metode")
    c.get("/metode")
    assert panggilan == [5]


def test_contoh_di_escape(client):
    jahat = [{"putaran": 1, "mentah": 1, "informatif": 1, "contoh": ["<script>alert(1)</script>"]}]
    html = client(lambda s, batas_putaran=5: jahat).get("/metode").text
    assert "<script>alert(1)" not in html


def test_api_metode_menyertakan_langkah(client):
    data = client(lambda s, batas_putaran=5: LANGKAH).get("/api/metode").json()
    assert data["langkah_penalaran"][0]["informatif"] == 375
    assert client(None).get("/api/metode").json()["langkah_penalaran"] is None
