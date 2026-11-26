"""Test NL2SPARQL: skema dari graf, guard empat pemeriksaan, dan verbalisasi.

Modul `nl2sparql` sudah ada sebelum task ini; test di sini mengunci perilakunya
terhadap keempat pemeriksaan materi P13 bagian 16, bukan menguji ulang
implementasi internalnya.

Dua kelas masukan yang dijaga khusus di sini:

1. Pertanyaan yang tidak berkaitan dengan graf sama sekali ("berapa harga tiket
   pesawat?") harus dijawab tidak bisa diterjemahkan, bukan dengan hitungan
   asal-asalan.
2. Query yang dihasilkan harus hanya memakai properti yang ada di graf, supaya
   guard tidak menolak query buatan kita sendiri.
"""

from rdflib import URIRef

import pytest

from semweb.nl2sparql import (
    MAKS_LIMIT,
    aman,
    intent,
    jawab,
    ke_sparql,
    kosakata,
    prompt,
    skema_graf,
)
from semweb.store import MuseumStore

TTL = """
@prefix sdp: <https://museumsumatera.id/ontology#> .
@prefix res: <https://museumsumatera.id/resource/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://museumsumatera.id/resource/museum/aceh> a sdp:Museum ;
    sdp:name "Museum Negeri Aceh"@id ;
    sdp:locatedInProvince res:province-aceh ;
    sdp:hasTheme res:theme-etnografi ;
    sdp:establishedYear "1915"^^xsd:gYear ;
    sdp:hasExhibit res:museum-aceh-exhibit-1 .

res:museum-aceh-exhibit-1 a sdp:Exhibit ;
    sdp:exhibitTitle "Lonceng Cakra Donya"@id .

res:province-aceh a sdp:Province ; sdp:name "Aceh"@id .
res:theme-etnografi a sdp:Theme ; sdp:name "Etnografi"@id .

sdp:locatedInProvince a owl:ObjectProperty ;
    rdfs:domain sdp:Museum ; rdfs:range sdp:Province .
sdp:name a owl:DatatypeProperty ;
    rdfs:domain sdp:Museum ; rdfs:range xsd:string .
"""


@pytest.fixture
def store():
    return MuseumStore.dari_turtle(data=TTL)


# --- guard: empat pemeriksaan materi P13 -----------------------------------


def test_guard_menerima_select_dengan_limit(store):
    q = "SELECT ?s WHERE { ?s a <https://museumsumatera.id/ontology#Museum> } LIMIT 10"
    ok, pesan = aman(q, store)
    assert ok is True and pesan == "ok"


def test_guard_menolak_query_tanpa_limit(store):
    q = "SELECT ?s WHERE { ?s a <https://museumsumatera.id/ontology#Museum> }"
    ok, pesan = aman(q, store)
    assert ok is False
    assert "LIMIT" in pesan.upper()


def test_guard_menolak_limit_di_atas_maksimum(store):
    q = (
        "SELECT ?s WHERE { ?s a <https://museumsumatera.id/ontology#Museum> } "
        f"LIMIT {MAKS_LIMIT + 1}"
    )
    ok, pesan = aman(q, store)
    assert ok is False
    assert "LIMIT" in pesan.upper()


def test_guard_menolak_ask_dan_construct(store):
    for q in (
        "ASK { ?s ?p ?o }",
        "CONSTRUCT { ?s ?p ?o } WHERE { ?s ?p ?o } LIMIT 5",
    ):
        ok, pesan = aman(q, store)
        assert ok is False
        assert "SELECT" in pesan.upper()


def test_guard_menolak_insert_dan_delete(store):
    for q in (
        "INSERT DATA { <https://museumsumatera.id/resource/x> "
        "a <https://museumsumatera.id/ontology#Museum> }",
        "DELETE WHERE { ?s ?p ?o }",
    ):
        ok, _ = aman(q, store)
        assert ok is False


def test_guard_menolak_sintaks_rusak(store):
    ok, pesan = aman("SELECT ?s WHERE { ?s ?p", store)
    assert ok is False
    assert "tidak sah" in pesan.lower()


def test_guard_menolak_iri_tidak_dikenal(store):
    q = "SELECT ?s WHERE { ?s <https://museumsumatera.id/ontology#namaLengkap> ?x } LIMIT 5"
    ok, pesan = aman(q, store)
    assert ok is False
    assert "tidak dikenal" in pesan.lower()


def test_guard_menerima_query_berprefiks(store):
    """Query sah berprefiks tidak boleh ditolak.

    Guard memeriksa IRI hasil resolusi prefiks lewat `prepareQuery`, bukan teks
    mentah, sehingga `sdp:Museum` dikenali sama dengan IRI lengkapnya.
    """
    q = (
        "PREFIX sdp: <https://museumsumatera.id/ontology#>\n"
        "SELECT ?s WHERE { ?s a sdp:Museum } LIMIT 5"
    )
    ok, pesan = aman(q, store)
    assert ok is True, pesan


def test_guard_menerima_limit_huruf_kecil(store):
    q = "SELECT ?s WHERE { ?s a <https://museumsumatera.id/ontology#Museum> } limit 10"
    ok, pesan = aman(q, store)
    assert ok is True, pesan


def test_guard_menolak_query_kosong(store):
    ok, pesan = aman("   ", store)
    assert ok is False
    assert pesan


# --- skema dari graf ------------------------------------------------------


def test_skema_diambil_dari_graf_bukan_dikarang(store):
    """`Skema` memetakan IRI properti -> range; kelas IRI -> nama lokal."""
    s = skema_graf(store)
    kelas = " ".join(s.kelas.values())
    properti = " ".join(s.objek.keys())
    assert "Museum" in kelas
    assert "locatedInProvince" in properti


def test_kosakata_memuat_iri_graf_dan_kosakata_baku(store):
    k = kosakata(store)
    assert str(URIRef("https://museumsumatera.id/resource/museum/aceh")) in k
    assert "http://www.w3.org/1999/02/22-rdf-syntax-ns#type" in k


def test_prompt_memuat_skema_atribut_dan_pertanyaan(store):
    p = prompt("Museum apa yang ada di Aceh?", store)
    assert "KELAS" in p
    assert "LIMIT" in p
    assert "Museum apa yang ada di Aceh?" in p


def test_prompt_tidak_melempar_keyerror_karena_kurung_sparql(store):
    """`.format()` akan gagal pada kurawal SPARQL; `replace()` tidak."""
    p = prompt("Berapa museum?", store)
    assert p


# --- intent ---------------------------------------------------------------


def test_intent_mengenali_pertanyaan_daftar(store):
    i = intent("museum apa saja di Aceh?", store)
    assert i.jenis == "daftar"
    assert i.topik == "museum"


def test_intent_mengenali_pertanyaan_hitung(store):
    i = intent("ada berapa museum?", store)
    assert i.jenis == "hitung"


def test_intent_mengenali_pertanyaan_pameran(store):
    i = intent("pameran apa saja di Museum Negeri Aceh?", store)
    assert i.topik == "pameran"


def test_intent_menemukan_jangkar_museum(store):
    i = intent("kapan Museum Negeri Aceh berdiri?", store)
    assert i.jangkar is not None
    assert "museum/aceh" in i.jangkar


def test_intent_menandai_pertanyaan_di_luar_domain(store):
    """Pertanyaan yang tidak menyebut kosakata graf bukan permintaan hitung."""
    i = intent("berapa harga tiket pesawat?", store)
    assert i.jenis == "tidak_dikenal"


# --- terjemahan: hanya properti yang ada di graf ---------------------------


def test_ke_sparql_menghasilkan_query_yang_lolos_guard(store):
    q = ke_sparql("museum apa saja di Aceh?", store)
    assert "SELECT" in q.upper()
    ok, pesan = aman(q, store)
    assert ok is True, pesan


def test_ke_sparql_tidak_memakai_located_in_city_bila_tidak_ada(store):
    """Graph fixture tidak punya `locatedInCity`; query tidak boleh memakainya."""
    q = ke_sparql("museum apa saja di Aceh?", store)
    assert "locatedInCity" not in q


def test_ke_sparql_hitung_memakai_count(store):
    q = ke_sparql("ada berapa museum?", store)
    assert "COUNT" in q.upper()
    assert aman(q, store)[0] is True


def test_ke_sparql_pertanyaan_di_luar_domain_menghasilkan_query_kosong(store):
    q = ke_sparql("berapa harga tiket pesawat?", store)
    assert q == ""


# --- jawaban --------------------------------------------------------------


def test_jawab_pertanyaan_di_luar_domain_tidak_menjawab_angka(store):
    hasil = jawab("berapa harga tiket pesawat?", store)
    teks = hasil.jawaban.lower()
    assert "tiket" in teks or "tidak" in teks
    assert "entitas" not in teks


def test_jawab_museum_di_aceh_mengembalikan_nama(store):
    hasil = jawab("museum apa saja di Aceh?", store)
    assert hasil.lolos is True, hasil.pesan
    assert "Museum Negeri Aceh" in hasil.jawaban


def test_jawab_pameran_menyebut_judul_pameran(store):
    hasil = jawab("pameran apa saja di Museum Negeri Aceh?", store)
    assert hasil.lolos is True, hasil.pesan
    assert "Lonceng" in hasil.jawaban


def test_jawab_jumlah_museum(store):
    """Hitungan memakai closure, jadi `rdfs:domain` ikut memberi tipe.

    Fixture mendeklarasikan `sdp:locatedInProvince rdfs:domain sdp:Museum`,
    sehingga reasoner menyimpulkan provinsi dan tema juga bertipe `sdp:Museum`.
    Inilah contoh materi P12: domain bukan validasi, melainkan pemberi tipe.
    Karena itu jumlahnya 3, bukan 1.
    """
    hasil = jawab("ada berapa museum?", store)
    assert hasil.lolos is True, hasil.pesan
    assert "3" in hasil.jawaban
    assert "museum" in hasil.jawaban


def test_jumlah_museum_sama_dengan_anggota_kelas_di_closure(store):
    from rdflib.namespace import RDF

    from semweb.namespace import SDP

    di_closure = len(list(store.closure.subjects(RDF.type, SDP.Museum)))
    hasil = jawab("ada berapa museum?", store)
    assert str(di_closure) in hasil.jawaban


def test_jawab_menyertakan_query_yang_bisa_diperiksa(store):
    hasil = jawab("museum apa saja di Aceh?", store)
    assert hasil.query
    assert aman(hasil.query, store)[0] is True
