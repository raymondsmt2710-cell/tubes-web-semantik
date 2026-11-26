"""Test pemeriksa kepatuhan ontologi (tugas A2).

Dua lapis pengujian:

1. **Ontologi dan data proyek yang sebenarnya** harus lulus tanpa temuan.
   Ini yang menjaga agar cacat ontologi tidak kembali diam-diam.
2. **Setiap aturan diuji dengan fixture yang sengaja dirusak.** Tanpa lapis
   ini, pemeriksa yang selalu menjawab "tidak ada temuan" akan lulus semua
   test dan tidak menjaga apa pun.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from rdflib import Graph, URIRef
from rdflib.namespace import OWL, RDFS

from semweb.ontologi import Temuan, periksa_ontologi

AKAR = Path(__file__).resolve().parents[2]
BERKAS_ONTO = AKAR / "ontology" / "museum-sumatera.ttl"
BERKAS_DATA = AKAR / "data" / "museum-sumatera.ttl"
SKRIP = AKAR / "pyapp" / "scripts" / "cek_ontologi.py"

PREFIX = """
@prefix sdp:  <https://museumsumatera.id/ontology#> .
@prefix res:  <https://museumsumatera.id/resource/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl:  <http://www.w3.org/2002/07/owl#> .
@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
"""

# Ontologi minimum yang sehat: satu properti objek lengkap dengan domain dan
# range, satu properti data, satu subkelas yang punya individu.
ONTO_SEHAT = PREFIX + """
sdp:Museum a owl:Class .
sdp:City a owl:Class .
sdp:StateMuseum a owl:Class ; rdfs:subClassOf sdp:Museum .

sdp:locatedInCity a owl:ObjectProperty ;
    rdfs:domain sdp:Museum ;
    rdfs:range sdp:City .

sdp:name a owl:DatatypeProperty ;
    rdfs:domain sdp:Museum ;
    rdfs:range xsd:string .
"""

DATA_SEHAT = PREFIX + """
res:m1 a sdp:StateMuseum ;
    sdp:name "Museum Satu" ;
    sdp:locatedInCity res:c1 .
res:c1 a sdp:City .
"""


def periksa(onto_ttl: str, data_ttl: str) -> list[Temuan]:
    """Jalankan pemeriksa pada dua graf Turtle yang diberikan."""
    onto = Graph().parse(data=onto_ttl, format="turtle")
    data = Graph().parse(data=data_ttl, format="turtle")
    return periksa_ontologi(onto, data)


def aturan(temuan: list[Temuan]) -> set[str]:
    """Kumpulan nama aturan yang terlanggar, untuk assertion yang ringkas."""
    return {t.aturan for t in temuan}


# --------------------------------------------------- ontologi proyek sendiri


def test_ontologi_dan_data_proyek_lulus_tanpa_temuan():
    """Ontologi yang dipakai aplikasi harus bersih dari semua temuan."""
    onto = Graph().parse(BERKAS_ONTO, format="turtle")
    data = Graph().parse(BERKAS_DATA, format="turtle")
    temuan = periksa_ontologi(onto, data)
    pesan = "\n".join(f"  [{t.aturan}] {t.pesan}" for t in temuan)
    assert temuan == [], f"ontologi masih melanggar:\n{pesan}"


def test_tidak_ada_properti_ber_inverse_yang_memberi_domain_atau_range():
    """README: properti ber-owl:inverseOf tidak menyimpan domain/range eksplisit.

    Alasan yang tertulis di README: supaya graf tetap konsisten di bawah
    OWL 2 RL. Pemeriksa aturan 1 sengaja mengecualikan properti semacam ini,
    jadi tanpa test tersendiri pelanggarannya bisa lolos tanpa ketahuan.
    """
    onto = Graph().parse(BERKAS_ONTO, format="turtle")
    pelanggar = []
    for prop in onto.subjects(OWL.inverseOf, None):
        if not isinstance(prop, URIRef):
            continue
        for nama, predikat in (("domain", RDFS.domain), ("range", RDFS.range)):
            if (prop, predikat, None) in onto:
                pelanggar.append(f"{prop.rsplit('#', 1)[-1]} punya {nama}")
    assert pelanggar == [], "properti ber-inverse tidak boleh punya domain/range: " + ", ".join(pelanggar)


def test_fixture_sehat_tidak_menghasilkan_temuan():
    """Kontrol negatif: pemeriksa tidak boleh melaporkan yang sehat."""
    assert periksa(ONTO_SEHAT, DATA_SEHAT) == []


# ------------------------------------------ aturan 1: domain dan range objek


def test_properti_objek_tanpa_domain_dilaporkan():
    onto = ONTO_SEHAT.replace(
        "sdp:locatedInCity a owl:ObjectProperty ;\n    rdfs:domain sdp:Museum ;\n"
        "    rdfs:range sdp:City .",
        "sdp:locatedInCity a owl:ObjectProperty ;\n    rdfs:range sdp:City .",
    )
    temuan = periksa(onto, DATA_SEHAT)
    assert "domain-range" in aturan(temuan)
    assert any("locatedInCity" in t.pesan and "domain" in t.pesan for t in temuan)


def test_properti_objek_tanpa_range_dilaporkan():
    onto = ONTO_SEHAT.replace(
        "    rdfs:domain sdp:Museum ;\n    rdfs:range sdp:City .",
        "    rdfs:domain sdp:Museum .",
    )
    temuan = periksa(onto, DATA_SEHAT)
    assert "domain-range" in aturan(temuan)
    assert any("locatedInCity" in t.pesan and "range" in t.pesan for t in temuan)


def test_properti_ber_inverse_dikecualikan_dari_syarat_domain_range():
    """README: properti ber-inverse sengaja tidak menyimpan domain/range.

    Pasangannya yang menyimpan, dan OWL 2 RL menurunkan sisanya. Pemeriksa
    tidak boleh menyalahkan keputusan desain yang sudah dipegang proyek.
    """
    onto = ONTO_SEHAT + """
sdp:hasImage a owl:ObjectProperty ; owl:inverseOf sdp:imageOfMuseum .
sdp:imageOfMuseum a owl:ObjectProperty ;
    owl:inverseOf sdp:hasImage ;
    rdfs:domain sdp:Image ;
    rdfs:range sdp:Museum .
sdp:Image a owl:Class .
"""
    temuan = periksa(onto, DATA_SEHAT)
    assert "domain-range" not in aturan(temuan), (
        "properti ber-inverse tidak boleh dituntut punya domain/range"
    )


# -------------------------------------------------- aturan 2: makna ganda


def test_properti_bermakna_ganda_dilaporkan():
    """Satu properti tidak boleh sekaligus objek dan data."""
    onto = ONTO_SEHAT + """
sdp:ambigu a owl:ObjectProperty , owl:DatatypeProperty ;
    rdfs:domain sdp:Museum ;
    rdfs:range sdp:City .
"""
    temuan = periksa(onto, DATA_SEHAT)
    assert "makna-ganda" in aturan(temuan)
    assert any("ambigu" in t.pesan for t in temuan)


def test_properti_objek_dipakai_untuk_literal_dilaporkan():
    """Properti objek yang dipakai dengan literal berarti dua arti."""
    data = DATA_SEHAT + """
res:m1 sdp:locatedInCity "Medan" .
"""
    temuan = periksa(ONTO_SEHAT, data)
    assert "makna-ganda" in aturan(temuan)
    assert any("locatedInCity" in t.pesan for t in temuan)


# --------------------------------------- aturan 3: kelas harus dideklarasikan


def test_kelas_dipakai_data_tapi_tidak_dideklarasikan_dilaporkan():
    data = DATA_SEHAT + """
res:x a sdp:Hantu .
"""
    temuan = periksa(ONTO_SEHAT, data)
    assert "kelas-tak-deklarasi" in aturan(temuan)
    assert any("Hantu" in t.pesan for t in temuan)


def test_properti_dipakai_data_tapi_tidak_dideklarasi_dilaporkan():
    """Lawan dari aturan 3 untuk predikat: properti pun harus dideklarasikan.

    Pemeriksaan ini tambahan di luar daftar tertulis tugas A2, karena tanpa
    ini properti yang dipakai data bisa hilang dari ontologi tanpa ketahuan.
    """
    data = DATA_SEHAT + """
res:m1 sdp:propertiHantu "nilai" .
"""
    temuan = periksa(ONTO_SEHAT, data)
    assert "properti-tak-deklarasi" in aturan(temuan)
    assert any("propertiHantu" in t.pesan for t in temuan)


# ------------------------------------------------ aturan 4: owl:disjointWith


def test_pelanggaran_disjoint_dilaporkan():
    onto = ONTO_SEHAT + """
sdp:PrivateMuseum a owl:Class ;
    rdfs:subClassOf sdp:Museum ;
    owl:disjointWith sdp:StateMuseum .
"""
    data = DATA_SEHAT + """
res:m1 a sdp:PrivateMuseum .
"""
    temuan = periksa(onto, data)
    assert "disjoint" in aturan(temuan)
    assert any("m1" in t.pesan for t in temuan)


def test_disjoint_yang_dihormati_tidak_dilaporkan():
    """Data hanya memakai StateMuseum, jadi aturan disjoint tidak boleh berbunyi.

    Hanya aturan `disjoint` yang diperiksa di sini; `PrivateMuseum` sengaja
    tidak punya individu sehingga aturan `subkelas-kosong` memang berbunyi.
    """
    onto = ONTO_SEHAT + """
sdp:PrivateMuseum a owl:Class ;
    rdfs:subClassOf sdp:Museum ;
    owl:disjointWith sdp:StateMuseum .
"""
    assert "disjoint" not in aturan(periksa(onto, DATA_SEHAT))


# ------------------------------------- aturan 5: subkelas museum punya individu


def test_subkelas_museum_tanpa_individu_dilaporkan():
    onto = ONTO_SEHAT + """
sdp:SiteMuseum a owl:Class ; rdfs:subClassOf sdp:Museum .
"""
    temuan = periksa(onto, DATA_SEHAT)
    assert "subkelas-kosong" in aturan(temuan)
    assert any("SiteMuseum" in t.pesan for t in temuan)


def test_subkelas_museum_berindividu_tidak_dilaporkan():
    onto = ONTO_SEHAT + """
sdp:SiteMuseum a owl:Class ; rdfs:subClassOf sdp:Museum .
"""
    data = DATA_SEHAT + """
res:m2 a sdp:SiteMuseum ; sdp:name "Museum Dua" .
"""
    assert periksa(onto, data) == []


# --------------------------------------------------------------- skrip CLI


def _jalankan(ontologi: Path, data: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(SKRIP),
            "--ontologi",
            str(ontologi),
            "--data",
            str(data),
        ],
        capture_output=True,
        text=True,
        cwd=str(SKRIP.parents[1]),
    )


def test_skrip_keluar_nol_pada_ontologi_sekarang():
    hasil = _jalankan(BERKAS_ONTO, BERKAS_DATA)
    assert hasil.returncode == 0, hasil.stdout + hasil.stderr
    assert "lulus" in hasil.stdout.lower()


def test_skrip_keluar_satu_pada_ontologi_rusak(tmp_path: Path):
    rusak = tmp_path / "rusak.ttl"
    rusak.write_text(
        ONTO_SEHAT.replace(
            "    rdfs:domain sdp:Museum ;\n    rdfs:range sdp:City .",
            "    rdfs:range sdp:City .",
        ),
        encoding="utf-8",
    )
    hasil = _jalankan(rusak, BERKAS_DATA)
    assert hasil.returncode == 1, hasil.stdout + hasil.stderr
    assert "locatedInCity" in hasil.stdout
