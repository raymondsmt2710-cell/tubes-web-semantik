"""Namespace bersama seluruh aplikasi.

Nilainya sengaja identik dengan data museum yang sudah ada supaya RDF lama dan
baru bisa dibaca oleh kueri yang sama.
"""

from rdflib import Namespace
from rdflib.namespace import OWL, RDF, RDFS, XSD

SDP = Namespace("https://museumsumatera.id/ontology#")
RES = Namespace("https://museumsumatera.id/resource/")

BIND = {
    "sdp": SDP,
    "res": RES,
    "rdf": RDF,
    "rdfs": RDFS,
    "owl": OWL,
    "xsd": XSD,
}
