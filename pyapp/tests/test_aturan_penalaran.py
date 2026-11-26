"""Fakta turunan: bersih, terurut, dan berlabel aturan."""

from pathlib import Path

from rdflib import BNode
from rdflib.namespace import OWL, RDFS

from semweb.reasoning import fakta_turunan
from semweb.store import MuseumStore

AKAR = Path(__file__).resolve().parent.parent.parent
DATA_TTL = AKAR / "data" / "museum-sumatera.ttl"
ONTO_TTL = AKAR / "ontology" / "museum-sumatera.ttl"

PREDIKAT_AKSIOMA = {
    str(RDFS.domain),
    str(RDFS.range),
    str(RDFS.subClassOf),
    str(RDFS.subPropertyOf),
    str(OWL.equivalentClass),
    str(OWL.equivalentProperty),
}


def store_penuh():
    return MuseumStore.dari_turtle(path=DATA_TTL)


def test_tidak_ada_sameas_di_fakta_turunan():
    for f in fakta_turunan(store_penuh(), batas=10_000):
        assert not f["predikat"].endswith("sameAs")


def test_tidak_ada_bnode_di_fakta_turunan():
    store = store_penuh()
    bnode = {str(b) for b in store.closure.all_nodes() if isinstance(b, BNode)}
    for f in fakta_turunan(store, batas=10_000):
        assert f["subjek"] not in bnode
        assert f["objek"] not in bnode


def test_tidak_ada_aksioma_vocabulary():
    for f in fakta_turunan(store_penuh(), batas=10_000):
        assert f["predikat"] not in PREDIKAT_AKSIOMA


def test_tidak_ada_objek_trivial():
    for f in fakta_turunan(store_penuh(), batas=10_000):
        assert not f["objek"].endswith("owl#Thing")
        assert not f["objek"].endswith("owl#Nothing")
        assert not f["objek"].endswith("rdf-schema#Resource")


def test_312_fakta_dan_218_prp_inv():
    if not ONTO_TTL.exists():
        return
    fakta = fakta_turunan(store_penuh(), batas=10_000)
    assert len(fakta) == 312
    inv = [f for f in fakta if f["predikat"].endswith("OfMuseum")]
    assert len(inv) == 218


def test_urutan_deterministik():
    store = store_penuh()
    a = [(f["subjek"], f["predikat"], f["objek"]) for f in fakta_turunan(store, batas=10_000)]
    b = [(f["subjek"], f["predikat"], f["objek"]) for f in fakta_turunan(store, batas=10_000)]
    assert a == b
    assert a == sorted(a)


def test_setiap_fakta_punya_kunci_aturan():
    for f in fakta_turunan(store_penuh(), batas=10_000):
        assert isinstance(f["aturan"], list)
        assert f["aturan"]
