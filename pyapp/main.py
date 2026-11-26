"""Semantic Search Engine Museum Sumatera — aplikasi web FastAPI.

Seluruh logika domain ada di paket ``semweb``; berkas ini hanya menyambungkan
graf ke halaman dan API JSON. Pembagian itu disengaja: modul domain bisa diuji
tanpa server, dan setiap route tinggal memilih jawaban mana yang ditampilkan.

Peta ke materi kuliah:

- P6/P7  RDF dan Turtle       -> ``semweb.generator``, ``semweb.store``
- P9-P11 SPARQL SELECT/CONSTRUCT -> ``semweb.search``, ``semweb.relations``
- P12    Inferensi & reasoning -> ``semweb.reasoning``
- P13    GraphRAG & NL2SPARQL  -> ``semweb.graphrag``, ``semweb.nl2sparql``
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Iterator

from fastapi import Depends, FastAPI, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from rdflib import URIRef
from rdflib.namespace import RDF

from semweb.construct import subkelas_museum, verifikasi_hierarki
from semweb.generator import load_records, tulis_ttl
from semweb.graphrag import ambil_konteks
from semweb.namespace import RES, SDP
from semweb.nl2sparql import jawab, ke_sparql, skema_graf
from semweb.reasoning import cek_konsistensi, fakta_turunan, jelaskan_tipe, perbandingan
from semweb.relations import benang_merah
from semweb.search import cari_museum, daftar_era, daftar_provinsi, daftar_tema
from semweb.store import MuseumStore

AKAR = Path(__file__).resolve().parents[1]
DATA_TTL = AKAR / "data" / "museum-sumatera.ttl"
DATA_JSON = AKAR / "data" / "museums.json"
TEMPLATES = Path(__file__).resolve().parent / "templates"
STATIC = Path(__file__).resolve().parent / "static"

app = FastAPI(title="Semantic Search Engine Museum Sumatera", docs_url="/api/docs")

if STATIC.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC)), name="static")

# Gambar museum dilayani dari folder publik aplikasi lama agar tidak digandakan.
GAMBAR = AKAR / "public"
if GAMBAR.exists():
    app.mount("/images", StaticFiles(directory=str(GAMBAR / "images")), name="images")

templates = Jinja2Templates(directory=str(TEMPLATES))


# ------------------------------------------------------------------ store


_store: MuseumStore | None = None


def muat_store() -> MuseumStore:
    """Muat graf sekali; hasilkan Turtle dulu bila berkasnya belum ada.

    Closure OWL-RL mahal, jadi store disimpan sebagai singleton proses.
    """
    global _store
    if _store is not None:
        return _store

    if not DATA_TTL.exists():
        if not DATA_JSON.exists():
            raise FileNotFoundError(
                f"Data museum tidak ditemukan di {DATA_JSON}. "
                "Jalankan scripts/generate.py lebih dulu."
            )
        tulis_ttl(load_records(DATA_JSON), DATA_TTL)

    _store = MuseumStore.dari_turtle(DATA_TTL)
    return _store


def get_store() -> MuseumStore:
    """Dependency FastAPI, bisa dioverride di test."""
    return muat_store()


# --------------------------------------------------------------- pembantu


def _museum_dto(store: MuseumStore, iri: URIRef) -> dict[str, Any]:
    """Rakit satu museum beserta pameran, galeri, dan sumbernya dari graf."""
    slug = str(iri).rsplit("/", 1)[-1]
    nilai = lambda p: store.asserted.value(iri, p)  # noqa: E731
    teks = lambda p: str(nilai(p)) if nilai(p) is not None else None  # noqa: E731

    def _urut(nodes, predikat_index):
        return sorted(
            nodes,
            key=lambda n: int(store.asserted.value(n, predikat_index) or 0),
        )

    pameran = []
    for node in _urut(store.asserted.objects(iri, SDP.hasExhibit), SDP.exhibitIndex):
        pameran.append(
            {
                "judul": str(store.asserted.value(node, SDP.exhibitTitle) or ""),
                "deskripsi": str(store.asserted.value(node, SDP.exhibitDescription) or ""),
                "periode": str(store.asserted.value(node, SDP.exhibitPeriod) or ""),
                "asal": str(store.asserted.value(node, SDP.exhibitOrigin) or ""),
                "bahan": str(store.asserted.value(node, SDP.exhibitMaterial) or ""),
                "andalan": bool(store.asserted.value(node, SDP.exhibitHighlight)),
            }
        )

    galeri = []
    for node in _urut(store.asserted.objects(iri, SDP.hasImage), SDP.imageIndex):
        poin = [
            str(store.asserted.value(d, SDP.detailText) or "")
            for d in _urut(store.asserted.objects(node, SDP.imageDetail), SDP.detailIndex)
        ]
        galeri.append(
            {
                "src": str(store.asserted.value(node, SDP.imageUrl) or ""),
                "judul": str(store.asserted.value(node, SDP.imageTitle) or ""),
                "latar": str(store.asserted.value(node, SDP.imageBackground) or ""),
                "periode": str(store.asserted.value(node, SDP.imagePeriod) or ""),
                "kredit": str(store.asserted.value(node, SDP.imageCredit) or ""),
                "lisensi": str(store.asserted.value(node, SDP.imageLicense) or ""),
                "lisensi_url": str(store.asserted.value(node, SDP.imageLicenseUrl) or ""),
                "sumber_url": str(store.asserted.value(node, SDP.imageSource) or ""),
                "poin": [p for p in poin if p],
            }
        )

    sumber = [
        {
            "label": str(store.asserted.value(node, SDP.sourceLabel) or ""),
            "url": str(store.asserted.value(node, SDP.sourceUrl) or ""),
        }
        for node in _urut(store.asserted.objects(iri, SDP.hasSource), SDP.sourceIndex)
    ]

    kota = nilai(SDP.locatedInCity)
    provinsi = nilai(SDP.locatedInProvince)
    tema_node = store.asserted.value(iri, SDP.hasTheme)
    era_node = store.asserted.value(iri, SDP.hasEra)
    tahun = nilai(SDP.establishedYear)

    return {
        "iri": str(iri),
        "slug": slug,
        "nama": teks(SDP.name) or slug,
        "deskripsi": teks(SDP.description),
        "alamat": teks(SDP.address),
        "kota": store.nama(kota) if kota is not None else None,
        "provinsi": store.nama(provinsi) if provinsi is not None else None,
        "tema": store.nama(tema_node) if tema_node is not None else None,
        "era": store.nama(era_node) if era_node is not None else None,
        "tahun": int(tahun) if tahun is not None else None,
        "verifikasi": teks(SDP.verificationStatus),
        "exhibits": pameran,
        "gallery": galeri,
        "sources": sumber,
    }


def _museum_iri(store: MuseumStore, slug: str) -> URIRef | None:
    iri = URIRef(f"{RES}museum/{slug}")
    if (iri, RDF.type, None) in store.asserted:
        return iri
    return None


# ------------------------------------------------------------------ halaman


@app.get("/", response_class=HTMLResponse)
def beranda(request: Request, store: MuseumStore = Depends(get_store)):
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "ringkasan": perbandingan(store),
            "provinsi": daftar_provinsi(store),
            "tema": daftar_tema(store),
            "era": daftar_era(store),
            "jumlah_museum": len(list(store.asserted.subjects(RDF.type, SDP.Museum))),
            "subkelas": subkelas_museum(store),
        },
    )


@app.get("/cari", response_class=HTMLResponse)
def halaman_cari(
    request: Request,
    q: str = "",
    provinsi: str = "",
    tema: str = "",
    era: str = "",
    tahun_min: str = "",
    urut: str = "nama",
    store: MuseumStore = Depends(get_store),
):
    tahun = None
    if tahun_min.strip():
        try:
            tahun = int(tahun_min)
        except ValueError:
            tahun = None

    hasil = cari_museum(
        store,
        q=q or None,
        provinsi=provinsi or None,
        tema=tema or None,
        era=era or None,
        tahun_min=tahun,
        urut=urut,
    )
    return templates.TemplateResponse(
        request,
        "cari.html",
        {
            "hasil": hasil,
            "q": q,
            "provinsi": provinsi,
            "tema": tema,
            "era": era,
            "tahun_min": tahun_min,
            "urut": urut,
            "daftar_provinsi": daftar_provinsi(store),
            "daftar_tema": daftar_tema(store),
            "daftar_era": daftar_era(store),
        },
    )


@app.get("/museum/{slug}", response_class=HTMLResponse)
def halaman_museum(slug: str, request: Request, store: MuseumStore = Depends(get_store)):
    iri = _museum_iri(store, slug)
    if iri is None:
        return templates.TemplateResponse(request, "tidak_ada.html", {}, status_code=404)

    return templates.TemplateResponse(
        request,
        "museum.html",
        {
            "museum": _museum_dto(store, iri),
            "benang": benang_merah(store, slug, maks=6),
            "rantai_tipe": jelaskan_tipe(store, slug),
        },
    )


@app.get("/tanya", response_class=HTMLResponse)
def halaman_tanya(request: Request, q: str = "", store: MuseumStore = Depends(get_store)):
    hasil = jawab(q, store) if q.strip() else None
    konteks = ambil_konteks(store, q, hop=1, batas=12) if q.strip() else None
    return templates.TemplateResponse(
        request,
        "tanya.html",
        {"q": q, "hasil": hasil, "konteks": konteks},
    )


@app.get("/metode", response_class=HTMLResponse)
def halaman_metode(request: Request, store: MuseumStore = Depends(get_store)):
    skema = skema_graf(store)
    return templates.TemplateResponse(
        request,
        "metode.html",
        {
            "perbandingan": perbandingan(store),
            "turunan": fakta_turunan(store, batas=20),
            "jumlah_turunan": len(fakta_turunan(store, batas=10_000)),
            "rantai": jelaskan_tipe(store, "museum-negeri-aceh"),
            "konsistensi": cek_konsistensi(store),
            "kelas": sorted(skema.kelas.values()),
            "objek": sorted(skema.objek.keys()),
            "data": sorted(skema.data.values()),
            "subkelas": subkelas_museum(store),
            "verifikasi": verifikasi_hierarki(store),
        },
    )


# ------------------------------------------------------------------ JSON API


@app.get("/api/cari")
def api_cari(
    q: str = "",
    provinsi: str = "",
    tema: str = "",
    era: str = "",
    tahun_min: str = "",
    urut: str = "nama",
    store: MuseumStore = Depends(get_store),
):
    tahun = None
    if tahun_min.strip():
        try:
            tahun = int(tahun_min)
        except ValueError:
            tahun = None
    hasil = cari_museum(
        store,
        q=q or None,
        provinsi=provinsi or None,
        tema=tema or None,
        era=era or None,
        tahun_min=tahun,
        urut=urut,
    )
    return {"jumlah": len(hasil), "museum": hasil}


@app.get("/api/museum/{slug}")
def api_museum(slug: str, store: MuseumStore = Depends(get_store)):
    iri = _museum_iri(store, slug)
    if iri is None:
        return JSONResponse(
            status_code=404, content={"error": "Museum tidak ditemukan."}
        )
    return {
        "museum": _museum_dto(store, iri),
        "benang_merah": benang_merah(store, slug, maks=6),
        "rantai_tipe": jelaskan_tipe(store, slug),
    }


@app.get("/api/tanya")
def api_tanya(
    q: str = Query(..., description="Pertanyaan bahasa Indonesia"),
    store: MuseumStore = Depends(get_store),
):
    return jawab(q, store).as_dict()


@app.get("/api/metode")
def api_metode(store: MuseumStore = Depends(get_store)):
    return {
        "perbandingan": perbandingan(store),
        "jumlah_fakta_turunan": len(fakta_turunan(store, batas=10_000)),
        "fakta_turunan": fakta_turunan(store, batas=20),
        "konsistensi": cek_konsistensi(store),
        "subkelas": subkelas_museum(store),
    }


@app.get("/api/kesehatan")
def api_kesehatan(store: MuseumStore = Depends(get_store)):
    """Ringkas untuk memastikan server benar-benar menyajikan graf."""
    return {
        "status": "ok",
        "triple_asserted": len(store.asserted),
        "triple_closure": len(store.closure),
        "museum": len(list(store.asserted.subjects(RDF.type, SDP.Museum))),
    }
