"""Graf premis: ontologi dimuat terpisah, `asserted` tidak berubah arti."""

from pathlib import Path

import pytest
from rdflib import Graph
from rdflib.namespace import RDF, RDFS

from semweb.namespace import SDP
from semweb.store import MuseumStore

from store_bersama import store_data

AKAR = Path(__file__).resolve().parent.parent.parent
DATA_TTL = AKAR / "data" / "museum-sumatera.ttl"
ONTO_TTL = AKAR / "ontology" / "museum-sumatera.ttl"

TTL_DATA = """
@prefix sdp: <https://museumsumatera.id/ontology#> .

<https://museumsumatera.id/resource/museum/a> a sdp:StateMuseum ;
    sdp:name "Museum A"@id ;
    sdp:hasExhibit <https://museumsumatera.id/resource/museum/a/exhibit/1> .

<https://museumsumatera.id/resource/museum/a/exhibit/1> a sdp:Exhibit .
"""

TTL_ONTO = """
@prefix sdp: <https://museumsumatera.id/ontology#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

sdp:StateMuseum rdfs:subClassOf sdp:Museum .
sdp:hasExhibit rdfs:domain sdp:Museum ;
    owl:inverseOf sdp:exhibitOfMuseum .
"""


def test_data_saja_tidak_memuat_ontologi():
    store = MuseumStore.dari_turtle(data=TTL_DATA)
    assert len(store.ontologi) == 0
    assert len(store.premis) == len(store.asserted)


def test_ontologi_eksplisit_menambah_premis_tanpa_mengubah_asserted():
    onto = Graph()
    onto.parse(data=TTL_ONTO, format="turtle")
    store = MuseumStore.dari_turtle(data=TTL_DATA, ontologi=onto)
    assert len(store.asserted) == 4
    assert len(store.ontologi) == 3
    assert len(store.premis) == 7


def test_closure_dihitung_atas_premis():
    onto = Graph()
    onto.parse(data=TTL_ONTO, format="turtle")
    store = MuseumStore.dari_turtle(data=TTL_DATA, ontologi=onto)
    museum = next(store.asserted.subjects(RDF.type, SDP.StateMuseum))
    assert (museum, RDF.type, SDP.Museum) in store.closure


def test_ontologi_none_string_mematikan_pemuatan():
    """`ontologi="none"` tidak boleh membaca berkas, jadi cukup graf mini."""
    store = MuseumStore.dari_turtle(data=TTL_DATA, ontologi="none")
    assert len(store.ontologi) == 0
    assert store.ontologi_path is None


def test_berkas_ontologi_hilang_tidak_melempar():
    """Repo tanpa folder ontology/ harus tetap jalan — berkas hilang bukan error."""
    store = MuseumStore.dari_turtle(
        data=TTL_DATA, ontologi=AKAR / "ontology" / "tidak-ada.ttl"
    )
    assert len(store.ontologi) == 0
    assert store.ontologi_path is None


def test_data_penuh_memuat_ontologi_otomatis():
    """Deteksi otomatis memuat ontologi dari folder di samping `data/`.

    Jumlah triple tidak diikat ke angka mati: data museum terus dilengkapi, dan
    angka mati akan gagal bukan karena deteksinya salah. Yang diuji adalah
    hubungan antar-graf: `premis` = `asserted` ∪ `ontologi`, dan closure
    menghitung penalaran atas premis sehingga lebih besar dari keduanya.
    """
    if not ONTO_TTL.exists():
        pytest.skip("ontology/ tidak ada — deteksi otomatis tidak terverifikasi")
    store = store_data()
    assert len(store.asserted) > 0
    assert len(store.ontologi) > 0
    assert len(store.premis) >= len(store.asserted)
    assert len(store.premis) >= len(store.ontologi)
    assert len(store.closure) > len(store.premis), "closure harus memuat fakta turunan"
    assert store.ontologi_path == ONTO_TTL


def test_ontologi_berupa_path_memuat_berkasnya():
    """Cabang `ontologi=<path>` yang berkasnya ADA; cabang berkas hilang sudah diuji."""
    if not ONTO_TTL.exists():
        pytest.skip("ontology/ tidak ada")
    store = store_data(ONTO_TTL)
    assert len(store.ontologi) > 0
    assert store.ontologi_path == ONTO_TTL


def test_ringkasan_melaporkan_premis_dan_ontologi():
    onto = Graph()
    onto.parse(data=TTL_ONTO, format="turtle")
    r = MuseumStore.dari_turtle(data=TTL_DATA, ontologi=onto).ringkasan()
    assert r["ontologi_dimuat"] is True
    assert r["premis"] == 7
    assert r["asserted"] == 4


def test_asserted_tidak_kena_ontologi():
    """Kalau ontologi bocor ke asserted, guard NL2SPARQL & jangkar GraphRAG melonggar.

    Lima modul lain membaca `store.asserted`; tidak satu pun dari 188 test lama akan
    gagal bila ontologi bocor ke sana, karena semuanya memakai `data=`. Test ini
    satu-satunya jaring pengamannya.

    Jumlah triple tidak ditulis sebagai angka mati: `data/museums.json` berubah saat
    museum dilengkapi, dan angka mati akan gagal bukan karena logika salah. Yang
    diuji adalah sifatnya — aksioma ontologi tidak boleh muncul di `asserted`.
    """
    if not ONTO_TTL.exists():
        pytest.skip("ontology/ tidak ada")
    store = store_data()
    assert len(store.asserted) > 0
    assert (SDP.hasExhibit, RDFS.domain, SDP.Museum) not in store.asserted
    assert len(list(store.asserted.triples((None, RDFS.domain, None)))) == 0
    # `premis` justru harus memuatnya — kalau tidak, ontologi gagal dimuat.
    assert len(list(store.premis.triples((None, RDFS.domain, None)))) > 0


def test_skema_graf_dan_cari_iri_sama_dengan_tanpa_ontologi():
    """Angka ini dipakai guard NL2SPARQL (Ryan D) dan GraphRAG (Ryan D)."""
    if not ONTO_TTL.exists():
        pytest.skip("ontology/ tidak ada")
    from semweb.nl2sparql import skema_graf

    dengan = store_data()
    tanpa = store_data("none")

    sk_dengan, sk_tanpa = skema_graf(dengan), skema_graf(tanpa)
    assert set(sk_dengan.kelas) == set(sk_tanpa.kelas)
    assert set(sk_dengan.objek) == set(sk_tanpa.objek)

    assert set(dengan.cari_iri("provinsi")) == set(tanpa.cari_iri("provinsi"))
    assert set(dengan.cari_iri("museum")) == set(tanpa.cari_iri("museum"))
