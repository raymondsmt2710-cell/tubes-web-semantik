"""Muat graf dan hitung closure penalaran.

Materi P12 membedakan tiga hal: fakta yang ditulis (asserted), fakta turunan
(inferred), dan gabungan keduanya (closure). Reasoner tidak mengubah fakta yang
ditulis; ia menambahkan fakta baru ke graf terpisah. Kelas ini memegang ketiga
graf itu sekaligus supaya perbandingannya bisa ditampilkan apa adanya.

Sejak graf premis diperkenalkan, ada satu graf lagi: `premis` = asserted +
ontologi. OWL-RL hanya bisa menurunkan tipe superclass, domain, dan inverse bila
aksioma ontologi ikut terlihat oleh reasoner. Karena itu closure dihitung di
atas `premis`, sedangkan `asserted` tetap berarti "triple yang ditulis di berkas
data" — banyak modul lain membaca `asserted` dan artinya tidak boleh bergeser.
"""

from __future__ import annotations

from pathlib import Path

from owlrl import DeductiveClosure, OWLRL_Semantics, RDFS_Semantics
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDFS

from .namespace import BIND, SDP

# Nama berkas ontologi yang dideteksi otomatis di samping folder `data/`.
ONTO_BAKU = Path("ontology") / "museum-sumatera.ttl"


def _graf_baru() -> Graph:
    """Graf kosong yang sudah membawa prefiks aplikasi.

    Semua graf di kelas ini dibuat lewat sini supaya cetakan Turtle dan pesan
    hasil kueri memakai prefiks pendek (`sdp:`, `res:`), bukan IRI penuh.
    """
    g = Graph()
    for prefix, ns in BIND.items():
        g.bind(prefix, ns)
    return g


class MuseumStore:
    """Graf museum beserta hasil penalaran OWL-RL dan RDFS."""

    def __init__(self, asserted: Graph, ontologi: Graph | None = None) -> None:
        for prefix, ns in BIND.items():
            asserted.bind(prefix, ns)

        self.asserted: Graph = asserted
        self.ontologi: Graph = ontologi if ontologi is not None else _graf_baru()
        # Diisi `dari_turtle` hanya bila ontologi benar-benar dibaca dari berkas.
        self.ontologi_path: Path | None = None
        self.premis: Graph = self._gabung()
        self.closure: Graph = self._tutup(OWLRL_Semantics)
        self.rdfs: Graph = self._tutup(RDFS_Semantics)

    # ------------------------------------------------------------ pembuatan

    @classmethod
    def dari_turtle(
        cls,
        path: str | Path | None = None,
        data: str | None = None,
        ontologi: Graph | str | Path | None = None,
    ) -> "MuseumStore":
        """Muat store dari berkas Turtle atau dari teks Turtle.

        `ontologi` menerima `None` (deteksi otomatis di samping `data/`),
        `"none"` (tanpa ontologi), sebuah `Graph`, atau `str`/`Path` berkas.
        Bila `data=` dipakai, ontologi tidak pernah dicari di disk: pemanggil
        yang menyerahkan teks biasanya sedang menguji potongan kecil dan tidak
        ingin hasilnya bergantung pada isi folder proyek.
        """
        g = _graf_baru()
        sumber: Path | None = None
        if data is not None:
            g.parse(data=data, format="turtle")
        elif path is not None:
            sumber = Path(path)
            if not sumber.exists():
                raise FileNotFoundError(f"Berkas Turtle tidak ditemukan: {sumber}")
            g.parse(sumber, format="turtle")
        else:
            raise ValueError("Sebutkan path atau data Turtle.")

        graf_ontologi, ontologi_path = cls._muat_ontologi(sumber, ontologi)
        store = cls(g, graf_ontologi)
        store.ontologi_path = ontologi_path
        return store

    @staticmethod
    def _muat_ontologi(
        path_data: Path | None, ontologi: Graph | str | Path | None
    ) -> tuple[Graph, Path | None]:
        """Tentukan graf ontologi yang akan ikut menjadi premis.

        Berkas yang tidak ada bukan kesalahan: repositori bisa saja tidak
        menyertakan folder `ontology/`, dan penalaran tetap berjalan memakai
        aksioma yang ditulis di data itu sendiri.
        """
        if isinstance(ontologi, Graph):
            return ontologi, None
        if isinstance(ontologi, str) and ontologi == "none":
            return _graf_baru(), None

        if ontologi is None:
            if path_data is None:
                return _graf_baru(), None
            # Berkas data ada di `<akar>/data/`, ontologi di `<akar>/ontology/`.
            kandidat = Path(path_data).resolve().parent.parent / ONTO_BAKU
        else:
            kandidat = Path(ontologi)

        if not kandidat.exists():
            return _graf_baru(), None

        g = _graf_baru()
        g.parse(kandidat, format="turtle")
        return g, kandidat

    def _gabung(self) -> Graph:
        """Gabungkan asserted dan ontologi jadi graf premis yang baru.

        Graf baru, bukan `asserted` yang ditambahi: `asserted` harus tetap
        berisi persis triple yang ditulis di berkas data.
        """
        gabungan = _graf_baru()
        for triple in self.asserted:
            gabungan.add(triple)
        for triple in self.ontologi:
            gabungan.add(triple)
        return gabungan

    def _tutup(self, semantik) -> Graph:
        """Salin graf premis lalu perluas dengan aturan semantik yang diminta."""
        salinan = _graf_baru()
        for triple in self.premis:
            salinan.add(triple)
        DeductiveClosure(semantik).expand(salinan)
        return salinan

    # -------------------------------------------------------------- ringkas

    def ringkasan(self) -> dict[str, int | bool]:
        """Angka untuk halaman metode dan skrip demo."""
        asserted = len(self.asserted)
        closure = len(self.closure)
        return {
            "asserted": asserted,
            "premis": len(self.premis),
            "closure": closure,
            "closure_rdfs": len(self.rdfs),
            "inferred": closure - asserted,
            "ontologi_dimuat": len(self.ontologi) > 0,
        }

    # --------------------------------------------------------------- pencarian

    def cari_iri(self, teks: str) -> list[URIRef]:
        """Cari node yang namanya memuat `teks`, tanpa peduli huruf besar/kecil.

        Dipakai GraphRAG untuk menentukan jangkar (anchor) dari pertanyaan
        bahasa alami: pertanyaan menyebut nama, graf menyimpan IRI.
        """
        cari = teks.strip().lower()
        if not cari:
            return []

        hasil: list[URIRef] = []
        for predikat in (SDP.name, RDFS.label):
            for subjek, _, objek in self.asserted.triples((None, predikat, None)):
                if not isinstance(subjek, URIRef):
                    continue
                nilai = str(objek).strip().lower()
                if cari in nilai and subjek not in hasil:
                    hasil.append(subjek)
        return hasil

    def nama(self, subjek: URIRef) -> str:
        """Label manusiawi sebuah node, atau potongan IRI bila tidak ada label."""
        for predikat in (SDP.name, RDFS.label):
            nilai = self.asserted.value(subjek, predikat)
            if isinstance(nilai, Literal):
                return str(nilai)
        return str(subjek).rsplit("/", 1)[-1].rsplit("#", 1)[-1]
