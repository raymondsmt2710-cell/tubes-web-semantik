from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDF, XSD
from semweb.generator import build_graph
from semweb.namespace import SDP, RES


def record_minimal() -> dict:
    return {
        "slug": "museum-uji",
        "name": "Museum Uji",
        "city": "Banda Aceh",
        "province": "Aceh",
        "themes": ["etnografi"],
        "era": "kolonial",
        "establishedYear": 1915,
        "address": "Jl. Uji",
        "latitude": 5.5,
        "longitude": 95.3,
        "description": "Deskripsi.",
        "imageUrl": None,
        "officialUrl": None,
        "admissionNote": None,
        "chapter": 1,
        "verificationStatus": "perlu-verifikasi",
        "history": ["Paragraf pertama."],
        "exhibits": [
            {
                "title": "Lonceng",
                "description": "Deskripsi panjang.",
                "period": "abad ke-15",
                "origin": "Pasai",
                "material": "perunggu",
                "highlight": True,
            }
        ],
        "sources": [{"label": "Sumber", "url": "https://contoh.id"}],
        "gallery": [
            {
                "src": "/images/museums/museum-uji/1.jpg",
                "alt": "Foto",
                "caption": "Keterangan",
                "title": "Judul foto",
                "background": "Latar belakang foto.",
                "period": "1915",
                "detail": ["Poin pertama", "Poin kedua"],
                "credit": "Seseorang",
                "license": "CC BY-SA 4.0",
                "licenseUrl": "https://creativecommons.org/licenses/by-sa/4.0",
                "sourceUrl": "https://commons.wikimedia.org/wiki/File:X.jpg",
            }
        ],
        "types": ["StateMuseum"],
        "collections": ["etnografika"],
        "collectionSize": 100,
    }


def test_museum_tertulis_sebagai_subjek_dengan_tipe():
    g = build_graph([record_minimal()])
    museum = URIRef(f"{RES}museum/museum-uji")
    # Tipe spesifik ditulis; `sdp:Museum` diturunkan reasoner (lihat test khusus).
    assert (museum, RDF.type, SDP.StateMuseum) in g


def test_established_year_memakai_datatype_gYear():
    g = build_graph([record_minimal()])
    museum = URIRef(f"{RES}museum/museum-uji")
    tahun = g.value(museum, SDP.establishedYear)
    assert tahun == Literal("1915", datatype=XSD.gYear)


def test_isi_pameran_menulis_metadata_kedalaman():
    g = build_graph([record_minimal()])
    exhibit = URIRef(f"{RES}museum/museum-uji/exhibit/1")
    assert g.value(exhibit, SDP.exhibitPeriod) == Literal("abad ke-15", lang="id")
    assert g.value(exhibit, SDP.exhibitOrigin) == Literal("Pasai", lang="id")
    assert g.value(exhibit, SDP.exhibitMaterial) == Literal("perunggu", lang="id")
    assert g.value(exhibit, SDP.exhibitHighlight) == Literal(True)


def test_poin_galeri_menjadi_node_tersendiri_dengan_urutan():
    g = build_graph([record_minimal()])
    image = URIRef(f"{RES}museum/museum-uji/image/1")
    detail = URIRef(f"{RES}museum/museum-uji/image/1/detail/2")
    assert (image, SDP.imageDetail, detail) in g
    assert g.value(detail, SDP.detailIndex) == Literal(2, datatype=XSD.integer)
    assert g.value(detail, SDP.detailText) == Literal("Poin kedua", lang="id")


def test_graf_bisa_diserialisasi_ke_turtle_dan_dibaca_ulang():
    g = build_graph([record_minimal()])
    ttl = g.serialize(format="turtle")
    assert "@prefix" in ttl or "PREFIX" in ttl.upper()
    g2 = Graph().parse(data=ttl, format="turtle")
    assert len(g2) == len(g)


def test_slug_duplikat_ditolak():
    satu = record_minimal()
    dua = record_minimal()
    try:
        build_graph([satu, dua])
    except ValueError as e:
        assert "duplikat" in str(e).lower()
    else:
        raise AssertionError("slug duplikat seharusnya ditolak")


def test_museum_bertipe_spesifik_tidak_ditulis_sebagai_museum_umum():
    """Tipe `Museum` harus DITURUNKAN, bukan ditulis.

    Materi P12 memakai contoh persis ini: `Student rdfs:subClassOf Person` +
    `andi a Student` menghasilkan `andi a Person` tanpa ada yang menulisnya.
    Bila generator menulis keduanya, penalaran tidak punya apa pun untuk
    diturunkan dan halaman metode kehilangan contohnya.
    """
    from semweb.store import MuseumStore

    g = build_graph([record_minimal()])
    museum = URIRef(f"{RES}museum/museum-uji")
    tipe_tertulis = {t for t in g.objects(museum, RDF.type)}
    assert SDP.StateMuseum in tipe_tertulis
    assert SDP.Museum not in tipe_tertulis

    store = MuseumStore(g)
    tipe_closure = {t for t in store.closure.objects(museum, RDF.type)}
    assert SDP.Museum in tipe_closure, "reasoner harus menurunkan tipe Museum"


def test_museum_tanpa_tipe_spesifik_tetap_ditulis_sebagai_museum():
    """Tanpa tipe spesifik, tidak ada yang bisa diturunkan — tulis langsung."""
    record = record_minimal()
    record["types"] = []
    g = build_graph([record])
    museum = URIRef(f"{RES}museum/museum-uji")
    assert SDP.Museum in set(g.objects(museum, RDF.type))


def test_fakta_turunan_pada_data_generator_tidak_kosong():
    """Data contoh harus menghasilkan setidaknya satu tipe turunan nyata."""
    from semweb.reasoning import fakta_turunan
    from semweb.store import MuseumStore

    store = MuseumStore(build_graph([record_minimal()]))
    turunan = fakta_turunan(store)
    assert turunan, "harus ada fakta turunan yang bisa ditampilkan"
    ada_tipe_museum = any(
        f["predikat"].endswith("#type") and f["objek"].endswith("#Museum")
        for f in turunan
    )
    assert ada_tipe_museum
