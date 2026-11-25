"""Muat graf dan hitung closure penalaran.

Materi P12 membedakan tiga hal: fakta yang ditulis (asserted), fakta turunan
(inferred), dan gabungan keduanya (closure). Reasoner tidak mengubah fakta yang
ditulis; ia menambahkan fakta baru ke graf terpisah. Kelas ini memegang ketiga
graf itu sekaligus supaya perbandingannya bisa ditampilkan apa adanya.
"""

from __future__ import annotations

from pathlib import Path

from owlrl import DeductiveClosure, OWLRL_Semantics, RDFS_Semantics
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDFS

from .namespace import BIND, SDP


class MuseumStore:
    """Graf museum beserta hasil penalaran OWL-RL dan RDFS."""

    def __init__(self, asserted: Graph) -> None:
        for prefix, ns in BIND.items():
            asserted.bind(prefix, ns)

        self.asserted: Graph = asserted
        self.closure: Graph = self._tutup(OWLRL_Semantics)
        self.rdfs: Graph = self._tutup(RDFS_Semantics)

    # ------------------------------------------------------------ pembuatan

    @classmethod
    def dari_turtle(
        cls, path: str | Path | None = None, data: str | None = None
    ) -> "MuseumStore":
        """Muat store dari berkas Turtle atau dari teks Turtle."""
        g = Graph()
        if data is not None:
            g.parse(data=data, format="turtle")
        elif path is not None:
            sumber = Path(path)
            if not sumber.exists():
                raise FileNotFoundError(f"Berkas Turtle tidak ditemukan: {sumber}")
            g.parse(sumber, format="turtle")
        else:
            raise ValueError("Sebutkan path atau data Turtle.")
        return cls(g)

    def _tutup(self, semantik) -> Graph:
        """Salin graf lalu perluas dengan aturan semantik yang diminta."""
        salinan = Graph()
        for prefix, ns in BIND.items():
            salinan.bind(prefix, ns)
        for triple in self.asserted:
            salinan.add(triple)
        DeductiveClosure(semantik).expand(salinan)
        return salinan

    # -------------------------------------------------------------- ringkas

    def ringkasan(self) -> dict[str, int]:
        """Angka untuk halaman metode dan skrip demo."""
        asserted = len(self.asserted)
        closure = len(self.closure)
        return {
            "asserted": asserted,
            "closure": closure,
            "closure_rdfs": len(self.rdfs),
            "inferred": closure - asserted,
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
