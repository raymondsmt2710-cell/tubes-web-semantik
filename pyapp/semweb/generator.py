"""Generator Turtle dari data museum.

Data mentah (`data/museums.json`) adalah sumber kebenaran. Modul ini mengubahnya
menjadi graf RDF memakai rdflib, mengikuti pola yang diajarkan materi: satu
triple satu fakta, literal diberi tipe data atau tag bahasa, dan entitas yang
pernah muncul sebagai subjek dijadikan IRI, bukan string.
"""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import Any

from rdflib import Graph, Literal, URIRef
from rdflib.namespace import OWL, RDF, RDFS, XSD

from .namespace import BIND, RES, SDP

# ---------------------------------------------------------------- utilitas


def slugify(teks: str) -> str:
    """Ubah teks Indonesia menjadi slug IRI yang stabil.

    Contoh: "Sumatera Utara" -> "sumatera-utara", "Sejarah Alam" -> "sejarah-alam".
    """
    teks = teks.strip().lower()
    teks = re.sub(r"[^a-z0-9]+", "-", teks)
    return teks.strip("-")


def load_records(path: str | Path) -> list[dict[str, Any]]:
    """Baca `data/museums.json` sebagai daftar record museum."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Data museum harus berupa daftar.")
    return data


def _teks(nilai: str | None) -> Literal | None:
    """Literal berbahasa Indonesia; None bila kosong."""
    if nilai is None:
        return None
    teks = str(nilai).strip()
    return Literal(teks, lang="id") if teks else None


def _angka(nilai: int | float | None, datatype) -> Literal | None:
    if nilai is None:
        return None
    return Literal(nilai, datatype=datatype)


# ---------------------------------------------------------------- generator


def build_graph(records: list[dict[str, Any]]) -> Graph:
    """Rakit seluruh record menjadi satu Graph RDF.

    Melempar ValueError bila ada slug duplikat, karena dua museum dengan URI
    sama akan saling menimpa dan merusak graf.
    """
    g = Graph()
    for prefix, ns in BIND.items():
        g.bind(prefix, ns)

    _deklarasikan_ontologi(g)

    terlihat: set[str] = set()
    for record in records:
        slug = str(record.get("slug", "")).strip()
        if not slug:
            raise ValueError("Ada record museum tanpa slug.")
        if slug in terlihat:
            raise ValueError(f"Slug duplikat: {slug}")
        terlihat.add(slug)
        _tulis_museum(g, record)

    return g


def _deklarasikan_ontologi(g: Graph) -> None:
    """Deklarasikan kelas inti agar graf bisa dipakai reasoner tanpa impor luar."""
    for kelas in (
        "Museum",
        "StateMuseum",
        "SiteMuseum",
        "PrivateMuseum",
        "Province",
        "City",
        "Theme",
        "Era",
        "Chapter",
        "Collection",
        "Exhibit",
        "Image",
        "ImageDetail",
        "Source",
        "Facility",
    ):
        g.add((SDP[kelas], RDF.type, OWL.Class))

    for sub in ("StateMuseum", "SiteMuseum", "PrivateMuseum"):
        g.add((SDP[sub], RDFS.subClassOf, SDP.Museum))

    g.add((SDP.Museum, RDFS.subClassOf, OWL.Thing))


def _tulis_museum(g: Graph, record: dict[str, Any]) -> None:
    slug = record["slug"]
    museum = URIRef(f"{RES}museum/{slug}")
    g.add((museum, RDF.type, SDP.Museum))

    for tipe in record.get("types") or []:
        g.add((museum, RDF.type, SDP[tipe]))

    tambah = [
        (SDP.name, _teks(record.get("name"))),
        (SDP.description, _teks(record.get("description"))),
        (SDP.address, _teks(record.get("address"))),
        (SDP.establishedYear, _angka(record.get("establishedYear"), XSD.gYear)),
        (SDP.latitude, _angka(record.get("latitude"), XSD.decimal)),
        (SDP.longitude, _angka(record.get("longitude"), XSD.decimal)),
        (SDP.collectionSize, _angka(record.get("collectionSize"), XSD.integer)),
        (SDP.verificationStatus, _teks(record.get("verificationStatus"))),
        (SDP.admissionNote, _teks(record.get("admissionNote"))),
        (SDP.officialUrl, _uri(record.get("officialUrl"))),
    ]
    for predikat, objek in tambah:
        if objek is not None:
            g.add((museum, predikat, objek))

    # Hero image hanya bila menunjuk berkas lokal.
    gambar_utama = record.get("imageUrl")
    if gambar_utama:
        g.add((museum, SDP.imageUrl, Literal(gambar_utama, datatype=XSD.anyURI)))

    _tulis_kota(g, museum, record)
    _tulis_provinsi(g, museum, record)
    _tulis_bab(g, museum, record)

    for tema in record.get("themes") or []:
        tema_iri = _tulis_entitas_sederhana(g, "theme", tema, "Theme")
        g.add((museum, SDP.hasTheme, tema_iri))

    if record.get("era"):
        era_iri = _tulis_entitas_sederhana(g, "era", record["era"], "Era")
        g.add((museum, SDP.hasEra, era_iri))

    for kategori in record.get("collections") or []:
        koleksi = URIRef(f"{RES}collection/{slug}/{slugify(kategori)}")
        g.add((koleksi, RDF.type, SDP.Collection))
        label = _teks(kategori)
        if label is not None:
            g.add((koleksi, SDP.collectionCategory, label))
        g.add((museum, SDP.hasCollection, koleksi))

    for paragraf in record.get("history") or []:
        nilai = _teks(paragraf)
        if nilai is not None:
            g.add((museum, SDP.history, nilai))

    _tulis_pameran(g, museum, slug, record.get("exhibits") or [])
    _tulis_galeri(g, museum, slug, record.get("gallery") or [])
    _tulis_sumber(g, museum, slug, record.get("sources") or [])


def _uri(nilai: str | None) -> Literal | None:
    if not nilai:
        return None
    return Literal(nilai, datatype=XSD.anyURI)


def _tulis_kota(g: Graph, museum: URIRef, record: dict[str, Any]) -> None:
    kota = record.get("city")
    if not kota:
        return
    kota_iri = URIRef(f"{RES}city/{slugify(kota)}")
    g.add((kota_iri, RDF.type, SDP.City))
    label = _teks(kota)
    if label is not None:
        g.add((kota_iri, SDP.name, label))
    g.add((museum, SDP.locatedInCity, kota_iri))

    provinsi = record.get("province")
    if provinsi:
        provinsi_iri = URIRef(f"{RES}province/{slugify(provinsi)}")
        g.add((kota_iri, SDP.partOfProvince, provinsi_iri))


def _tulis_provinsi(g: Graph, museum: URIRef, record: dict[str, Any]) -> None:
    provinsi = record.get("province")
    if not provinsi:
        return
    provinsi_iri = URIRef(f"{RES}province/{slugify(provinsi)}")
    g.add((provinsi_iri, RDF.type, SDP.Province))
    label = _teks(provinsi)
    if label is not None:
        g.add((provinsi_iri, SDP.name, label))
    g.add((museum, SDP.locatedInProvince, provinsi_iri))


def _tulis_bab(g: Graph, museum: URIRef, record: dict[str, Any]) -> None:
    nomor = record.get("chapter")
    if nomor is None:
        return
    bab_iri = URIRef(f"{RES}chapter/{nomor}")
    g.add((bab_iri, RDF.type, SDP.Chapter))
    g.add((bab_iri, SDP.chapterIndex, Literal(nomor, datatype=XSD.integer)))
    judul = _teks(record.get("chapterTitle"))
    if judul is not None:
        g.add((bab_iri, SDP.chapterTitle, judul))
    g.add((museum, SDP.chapter, bab_iri))


def _tulis_entitas_sederhana(
    g: Graph, jenis: str, nilai: str, kelas: str
) -> URIRef:
    iri = URIRef(f"{RES}{jenis}/{slugify(nilai)}")
    g.add((iri, RDF.type, SDP[kelas]))
    label = _teks(nilai)
    if label is not None:
        g.add((iri, SDP.name, label))
    return iri


def _tulis_pameran(
    g: Graph, museum: URIRef, slug: str, pameran: list[dict[str, Any]]
) -> None:
    for nomor, item in enumerate(pameran, start=1):
        node = URIRef(f"{RES}museum/{slug}/exhibit/{nomor}")
        g.add((node, RDF.type, SDP.Exhibit))
        g.add((node, SDP.exhibitIndex, Literal(nomor, datatype=XSD.integer)))
        judul = _teks(item.get("title"))
        if judul is not None:
            g.add((node, SDP.exhibitTitle, judul))
        for kunci, predikat in (
            ("description", SDP.exhibitDescription),
            ("period", SDP.exhibitPeriod),
            ("origin", SDP.exhibitOrigin),
            ("material", SDP.exhibitMaterial),
        ):
            nilai = _teks(item.get(kunci))
            if nilai is not None:
                g.add((node, predikat, nilai))
        if item.get("highlight"):
            g.add((node, SDP.exhibitHighlight, Literal(True)))
        g.add((museum, SDP.hasExhibit, node))


def _tulis_galeri(
    g: Graph, museum: URIRef, slug: str, galeri: list[dict[str, Any]]
) -> None:
    for nomor, foto in enumerate(galeri, start=1):
        node = URIRef(f"{RES}museum/{slug}/image/{nomor}")
        g.add((node, RDF.type, SDP.Image))
        g.add((node, SDP.imageIndex, Literal(nomor, datatype=XSD.integer)))
        for kunci, predikat, datatype in (
            ("src", SDP.imageUrl, XSD.anyURI),
            ("title", SDP.imageTitle, None),
            ("background", SDP.imageBackground, None),
            ("period", SDP.imagePeriod, None),
            ("alt", SDP.imageAlt, None),
            ("caption", SDP.imageCaption, None),
            ("credit", SDP.imageCredit, None),
            ("license", SDP.imageLicense, None),
            ("licenseUrl", SDP.imageLicenseUrl, XSD.anyURI),
            ("sourceUrl", SDP.imageSource, XSD.anyURI),
        ):
            mentah = foto.get(kunci)
            if mentah is None or mentah == "":
                continue
            nilai = (
                Literal(mentah, datatype=datatype)
                if datatype is not None
                else _teks(mentah)
            )
            if nilai is not None:
                g.add((node, predikat, nilai))

        # Poin pengamatan menjadi node tersendiri supaya urutannya terjamin:
        # bila indeks disimpan sebagai properti pada foto, kueri SPARQL akan
        # menghasilkan perkalian silang dan urutan poin menjadi acak.
        for urut, poin in enumerate(foto.get("detail") or [], start=1):
            detail = URIRef(f"{RES}museum/{slug}/image/{nomor}/detail/{urut}")
            g.add((detail, RDF.type, SDP.ImageDetail))
            g.add((detail, SDP.detailIndex, Literal(urut, datatype=XSD.integer)))
            teks = _teks(poin)
            if teks is not None:
                g.add((detail, SDP.detailText, teks))
            g.add((node, SDP.imageDetail, detail))

        g.add((museum, SDP.hasImage, node))


def _tulis_sumber(
    g: Graph, museum: URIRef, slug: str, sumber: list[dict[str, Any]]
) -> None:
    for nomor, acuan in enumerate(sumber, start=1):
        node = URIRef(f"{RES}museum/{slug}/source/{nomor}")
        g.add((node, RDF.type, SDP.Source))
        g.add((node, SDP.sourceIndex, Literal(nomor, datatype=XSD.integer)))
        label = _teks(acuan.get("label"))
        if label is not None:
            g.add((node, SDP.sourceLabel, label))
        url = _uri(acuan.get("url"))
        if url is not None:
            g.add((node, SDP.sourceUrl, url))
        g.add((museum, SDP.hasSource, node))


def to_turtle(g: Graph) -> str:
    """Serialisasi graf ke Turtle — format utama proyek ini."""
    return g.serialize(format="turtle")


def to_rdfxml(g: Graph) -> str:
    """Serialisasi RDF/XML, dipakai hanya untuk membandingkan dengan Turtle."""
    return g.serialize(format="xml")


def ringkasan(records: list[dict[str, Any]]) -> dict[str, int]:
    """Hitung angka ringkas untuk dicetak skrip generator."""
    return {
        "museum": len(records),
        "provinsi": len({r.get("province") for r in records if r.get("province")}),
        "tema": len({t for r in records for t in (r.get("themes") or [])}),
        "bab": len({r.get("chapter") for r in records if r.get("chapter")}),
        "pameran": sum(len(r.get("exhibits") or []) for r in records),
        "foto": sum(len(r.get("gallery") or []) for r in records),
    }


def tulis_ttl(records: list[dict[str, Any]], tujuan: str | Path) -> Path:
    """Bangun graf lalu tulis ke berkas Turtle. Mengembalikan path hasil."""
    g = build_graph(records)
    path = Path(tujuan)
    path.parent.mkdir(parents=True, exist_ok=True)
    header = f"# Museum Sumatera — dibuat {date.today().isoformat()} oleh generator rdflib\n"
    path.write_text(header + to_turtle(g), encoding="utf-8")
    return path
