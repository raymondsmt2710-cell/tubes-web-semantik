"""Test guard untuk klausa dataset dan federasi.

Tiga bentuk yang dikunci, masing-masing dengan dua varian:

===============  ==========================  ============================
Klausa           IRI asing                    Variabel
===============  ==========================  ============================
``FROM``         ditolak: IRI tak dikenal     tidak berlaku (FROM wajib IRI)
``GRAPH``        ditolak: IRI tak dikenal     **ditolak: variabel**
``SERVICE``      ditolak: IRI tak dikenal     **ditolak: variabel**
===============  ==========================  ============================

Dua baris tebal adalah celah yang ditutup di sini. Sebelumnya ``GRAPH ?g`` dan
``SERVICE ?v`` **lolos** guard: tidak ada IRI asing untuk ditolak, sehingga
pemeriksaan keempat tidak menangkapnya. ``SERVICE ?v`` paling berbahaya karena
variabel bisa terikat ke endpoint luar, dan query akan menghubungi server lain
di luar kendali.

Yang juga dikunci: ``FROM`` dengan IRI prefiks proyek sendiri harus **diterima**.
Sebelumnya ditolak sebagai "IRI tidak dikenal" karena prefiks namespace tidak
muncul sebagai triple di graf — itu positif palsu.
"""

from __future__ import annotations

import pytest

from semweb.nl2sparql import aman
from semweb.store import MuseumStore

TTL = """
@prefix sdp: <https://museumsumatera.id/ontology#> .
@prefix res: <https://museumsumatera.id/resource/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://museumsumatera.id/resource/museum/aceh> a sdp:Museum ;
    sdp:name "Museum Negeri Aceh"@id ;
    sdp:locatedInProvince res:province-aceh .

res:province-aceh a sdp:Province ; sdp:name "Aceh"@id .

sdp:locatedInProvince a owl:ObjectProperty ;
    rdfs:domain sdp:Museum ; rdfs:range sdp:Province .
sdp:name a owl:DatatypeProperty ;
    rdfs:domain sdp:Museum ; rdfs:range xsd:string .
"""


@pytest.fixture
def store():
    return MuseumStore.dari_turtle(data=TTL)


# ------------------------------------------------------------ FROM


def test_from_dengan_iri_asing_ditolak(store):
    q = "SELECT ?s FROM <http://jahat.example/x> WHERE { ?s ?p ?o } LIMIT 5"
    ok, pesan = aman(q, store)
    assert ok is False
    assert "tidak dikenal" in pesan


def test_from_named_dengan_iri_asing_ditolak(store):
    q = (
        "SELECT ?s FROM NAMED <http://jahat.example/x> "
        "WHERE { GRAPH ?g { ?s ?p ?o } } LIMIT 5"
    )
    ok, pesan = aman(q, store)
    assert ok is False
    assert "tidak dikenal" in pesan


def test_from_dengan_iri_prefiks_proyek_diterima(store):
    """Prefiks namespace bukan triple, tetapi sah dipakai di FROM."""
    q = (
        "SELECT ?s FROM <https://museumsumatera.id/ontology#> "
        "WHERE { ?s ?p ?o } LIMIT 5"
    )
    ok, pesan = aman(q, store)
    assert ok is True, pesan


# ----------------------------------------------------------- GRAPH


def test_graph_dengan_iri_asing_ditolak(store):
    q = "SELECT ?s WHERE { GRAPH <http://jahat.example/g> { ?s ?p ?o } } LIMIT 5"
    ok, pesan = aman(q, store)
    assert ok is False
    assert "tidak dikenal" in pesan


def test_graph_dengan_variabel_ditolak(store):
    """GRAPH ?g tidak punya IRI untuk diperiksa, jadi harus ditolak eksplisit."""
    q = "SELECT ?s WHERE { GRAPH ?g { ?s ?p ?o } } LIMIT 5"
    ok, pesan = aman(q, store)
    assert ok is False
    assert "GRAPH" in pesan or "variabel" in pesan


# --------------------------------------------------------- SERVICE


def test_service_dengan_iri_asing_ditolak(store):
    q = "SELECT ?s WHERE { SERVICE <http://jahat.example/s> { ?s ?p ?o } } LIMIT 5"
    ok, pesan = aman(q, store)
    assert ok is False
    assert "tidak dikenal" in pesan


def test_service_dengan_variabel_ditolak(store):
    """SERVICE ?v bisa terikat ke endpoint luar; harus ditolak."""
    q = "SELECT ?s WHERE { SERVICE ?v { ?s ?p ?o } } LIMIT 5"
    ok, pesan = aman(q, store)
    assert ok is False
    assert "SERVICE" in pesan or "variabel" in pesan


# ------------------------------------------------- jangan merusak yang sah


def test_query_biasa_tetap_diterima(store):
    q = (
        "SELECT ?nama WHERE { "
        "?m a <https://museumsumatera.id/ontology#Museum> ; "
        "<https://museumsumatera.id/ontology#name> ?nama } LIMIT 10"
    )
    ok, pesan = aman(q, store)
    assert ok is True, pesan


def test_query_berprefiks_tetap_diterima(store):
    q = (
        "PREFIX sdp: <https://museumsumatera.id/ontology#> "
        "SELECT ?nama WHERE { ?m a sdp:Museum ; sdp:name ?nama } LIMIT 10"
    )
    ok, pesan = aman(q, store)
    assert ok is True, pesan


def test_property_path_sah_tetap_diterima(store):
    q = (
        "PREFIX sdp: <https://museumsumatera.id/ontology#> "
        "PREFIX res: <https://museumsumatera.id/resource/> "
        "SELECT ?m WHERE { ?m sdp:locatedInProvince res:province-aceh } LIMIT 5"
    )
    ok, pesan = aman(q, store)
    assert ok is True, pesan


def test_tanpa_limit_tetap_ditolak(store):
    q = (
        "SELECT ?nama WHERE { ?m a <https://museumsumatera.id/ontology#Museum> ; "
        "<https://museumsumatera.id/ontology#name> ?nama }"
    )
    ok, _ = aman(q, store)
    assert ok is False


def test_insert_tetap_ditolak(store):
    q = "INSERT DATA { <http://x.example/a> <http://x.example/b> 1 }"
    ok, _ = aman(q, store)
    assert ok is False
