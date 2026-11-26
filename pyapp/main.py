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
import re
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
from semweb.jsonld import museum_jsonld, semua_museum_jsonld
from semweb.namespace import RES, SDP
from semweb.peta import titik_museum
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
                "andalan": _benar(store.asserted.value(node, SDP.exhibitHighlight)),
            }
        )

    nama_museum = teks(SDP.name) or _nama_dari_slug(slug)

    galeri = []
    for node in _urut(store.asserted.objects(iri, SDP.hasImage), SDP.imageIndex):
        judul_foto = str(store.asserted.value(node, SDP.imageTitle) or "")
        poin = [
            str(store.asserted.value(d, SDP.detailText) or "")
            for d in _urut(store.asserted.objects(node, SDP.imageDetail), SDP.detailIndex)
        ]
        galeri.append(
            {
                "src": str(store.asserted.value(node, SDP.imageUrl) or ""),
                "judul": judul_foto,
                "alt": _alt_foto(judul_foto, store.asserted.value(node, SDP.imageAlt), nama_museum),
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
        "nama": nama_museum,
        "deskripsi": teks(SDP.description),
        "alamat": teks(SDP.address),
        "kota": store.nama(kota) if kota is not None else None,
        "provinsi": store.nama(provinsi) if provinsi is not None else None,
        "tema": store.nama(tema_node) if tema_node is not None else None,
        "era": store.nama(era_node) if era_node is not None else None,
        "tahun": _tahun_dari(tahun),
        "verifikasi": teks(SDP.verificationStatus),
        "exhibits": pameran,
        "gallery": galeri,
        "sources": sumber,
    }


def _ringkasan_turunan(fakta: list[dict[str, Any]]) -> dict[str, Any]:
    """Hitung fakta turunan per aturan dari daftar yang sama dengan tabel.

    Angka di kartu harus cocok dengan baris yang bisa ditelusuri pembaca.
    ``len(closure) - len(asserted)`` tidak dipakai di sini karena memuat
    artefak reasoner (``x owl:sameAs x``, bnode restriksi, aksioma vocabulary).
    Fakta dengan dua aturan (mis. ``rdfs2`` dan ``rdfs9``) dihitung di
    keduanya, sehingga jumlah ``per_aturan`` boleh melebihi ``informatif``.
    """
    per_aturan: dict[str, int] = {}
    jalur_ganda = 0
    for f in fakta:
        aturan = f.get("aturan") or []
        if len(aturan) > 1:
            jalur_ganda += 1
        for nama in aturan:
            per_aturan[nama] = per_aturan.get(nama, 0) + 1
    return {
        "informatif": len(fakta),
        "per_aturan": dict(sorted(per_aturan.items(), key=lambda kv: (-kv[1], kv[0]))),
        "dua_jalur_atau_lebih": jalur_ganda,
    }


def _contoh_turunan(
    fakta: list[dict[str, Any]], maks: int = 20, per_aturan: int = 5
) -> list[dict[str, Any]]:
    """Pilih contoh yang mewakili setiap aturan, bukan sekadar 20 baris pertama.

    Tanpa ini, 218 fakta ``prp-inv`` di urutan awal akan memenuhi seluruh
    contoh dan aturan lain (``rdfs9``, ``rdfs2``) tidak pernah terlihat.
    Setiap kombinasi aturan mendapat jatah dulu, sisanya diisi berurutan.
    """
    terpilih: list[int] = []
    jatah: dict[tuple[str, ...], int] = {}
    for i, f in enumerate(fakta):
        kunci = tuple(f.get("aturan") or ())
        if jatah.get(kunci, 0) < per_aturan:
            jatah[kunci] = jatah.get(kunci, 0) + 1
            terpilih.append(i)
    for i in range(len(fakta)):
        if len(terpilih) >= maks:
            break
        if i not in terpilih:
            terpilih.append(i)
    return [fakta[i] for i in sorted(terpilih[:maks])]


def _alt_foto(judul: str, alt_data: Any, nama_museum: str) -> str:
    """Teks ``alt`` yang menjelaskan isi foto, bukan asal berkasnya.

    ``imageAlt`` di data berbentuk "Museum X — foto dari Wikimedia Commons":
    itu keterangan sumber, bukan isi gambar. Judul foto ("Gedung pameran
    tetap") lebih bermakna bagi pembaca layar, jadi diutamakan.
    """
    if judul.strip():
        return f"{judul.strip()} — {nama_museum}"
    if alt_data is not None and str(alt_data).strip():
        return str(alt_data).strip()
    return f"Foto {nama_museum}"


def _nama_dari_slug(slug: str) -> str:
    """Ubah slug menjadi label yang bisa dibaca, mis. "museum-negeri-aceh".

    Menampilkan slug mentah sebagai judul halaman terasa seperti data yang belum
    jadi; ini hanya dipakai bila museum benar-benar tidak punya nama.
    """
    return slug.replace("-", " ").title() or "Museum tanpa nama"


def _tahun_dari(nilai: Any) -> int | None:
    """Ambil tahun dari literal `xsd:gYear` tanpa melempar error.

    `int("1915")` aman, tetapi `xsd:gYear` bisa berisi bentuk lain
    ("1915-01-01") pada data yang tidak bersih. Kegagalan konversi tidak boleh
    menjatuhkan seluruh halaman.
    """
    if nilai is None:
        return None
    try:
        return int(str(nilai).strip()[:4])
    except (TypeError, ValueError):
        return None


def _basis(request: Request) -> str:
    """URL dasar situs untuk tautan absolut di JSON-LD.

    ``SITUS_URL`` (mis. ``https://museum-sumatera.up.railway.app/``) dipakai bila
    diisi, karena di belakang reverse proxy ``request.base_url`` bisa berisi
    alamat internal kontainer, bukan alamat publik.
    """
    dari_env = os.environ.get("SITUS_URL", "").strip()
    basis = dari_env or str(request.base_url)
    return basis if basis.endswith("/") else basis + "/"


def _benar(nilai: Any) -> bool:
    """Baca nilai boolean dari graf tanpa terjebak truthiness Python.

    `Literal("false")` bernilai **True** di Python karena string-nya tidak
    kosong. Nilai "false"/"0"/"no" harus dibaca sebagai False.
    """
    if nilai is None:
        return False
    if isinstance(nilai, bool):
        return nilai
    teks = str(nilai).strip().lower()
    return teks not in ("false", "0", "", "no", "tidak")


# Slug hanya boleh memuat huruf kecil, angka, dan tanda hubung. Batas ini
# mencegah slug dari URL (yang bisa berisi apa saja) masuk ke `URIRef` mentah —
# rdflib akan memperingatkan IRI tidak sah untuk input seperti "'; DROP".
_SLUG_SAH = re.compile(r"^[a-z0-9][a-z0-9-]{0,119}$")


def _museum_iri(store: MuseumStore, slug: str) -> URIRef | None:
    """Cari IRI museum dari slug, atau ``None`` bila slug tidak sah/tidak ada."""
    if not slug or not _SLUG_SAH.match(slug):
        return None
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
            "jumlah_museum": len(set(store.closure.subjects(RDF.type, SDP.Museum))),
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
            "jsonld": museum_jsonld(store, slug, _basis(request)),
        },
    )


@app.get("/peta", response_class=HTMLResponse)
def halaman_peta(request: Request, provinsi: str = "", store: MuseumStore = Depends(get_store)):
    titik = titik_museum(store, provinsi or None)
    return templates.TemplateResponse(
        request,
        "peta.html",
        {
            "titik": titik,
            "provinsi": provinsi,
            "daftar_provinsi": daftar_provinsi(store),
            # Hanya museum berkoordinat yang bisa dijadikan penanda peta.
            "penanda": [t for t in titik if t["lat"] is not None and t["lng"] is not None],
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
    semua_turunan = fakta_turunan(store, batas=10_000)
    return templates.TemplateResponse(
        request,
        "metode.html",
        {
            "perbandingan": perbandingan(store),
            "turunan": _contoh_turunan(semua_turunan),
            "jumlah_turunan": len(semua_turunan),
            "ringkasan_turunan": _ringkasan_turunan(semua_turunan),
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


# Route .jsonld didaftarkan SEBELUM /api/museum/{slug}: FastAPI mencocokkan
# route sesuai urutan, dan slug berisi titik akan ditolak validasi slug.
_JSONLD = "application/ld+json"


@app.get("/api/museum.jsonld")
def api_semua_jsonld(request: Request, store: MuseumStore = Depends(get_store)):
    """Seluruh museum sebagai JSON-LD schema.org (``@graph``)."""
    return JSONResponse(semua_museum_jsonld(store, _basis(request)), media_type=_JSONLD)


@app.get("/api/museum/{slug}.jsonld")
def api_museum_jsonld(slug: str, request: Request, store: MuseumStore = Depends(get_store)):
    """Satu museum sebagai JSON-LD schema.org (materi P3)."""
    doc = museum_jsonld(store, slug, _basis(request))
    if doc is None:
        return JSONResponse(status_code=404, content={"error": "Museum tidak ditemukan."})
    return JSONResponse(doc, media_type=_JSONLD)


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
    semua_turunan = fakta_turunan(store, batas=10_000)
    return {
        "perbandingan": perbandingan(store),
        "jumlah_fakta_turunan": len(semua_turunan),
        "ringkasan_turunan": _ringkasan_turunan(semua_turunan),
        "fakta_turunan": _contoh_turunan(semua_turunan),
        "konsistensi": cek_konsistensi(store),
        "subkelas": subkelas_museum(store),
    }


@app.get("/api/kesehatan")
def api_kesehatan(store: MuseumStore = Depends(get_store)):
    """Ringkas untuk memastikan server benar-benar menyajikan graf.

    Jumlah museum dibaca dari **closure**, bukan dari graf asserted: tipe umum
    `sdp:Museum` kini diturunkan reasoner dari tipe spesifik (`StateMuseum` dan
    sejenisnya), jadi di graf asserted jumlahnya nol.
    """
    return {
        "status": "ok",
        "triple_asserted": len(store.asserted),
        "triple_closure": len(store.closure),
        "museum": len(set(store.closure.subjects(RDF.type, SDP.Museum))),
    }
