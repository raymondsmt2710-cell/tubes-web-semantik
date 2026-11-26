"""Store bersama untuk test yang butuh graf penuh.

Membangun `MuseumStore` dari data asli butuh ~8-10 detik: memuat 4.400+ triple
lalu menghitung closure OWL-RL dan RDFS. Tanpa berbagi, suite menghabiskan
menitannya hanya untuk memuat graf yang sama berulang kali — dan itu membuat
setiap iterasi pengembangan terasa lambat.

Store tidak dimutasi oleh test mana pun (`fakta_turunan`, `aturan_fakta`, dan
`cari_museum` hanya membaca), jadi berbagi satu instance per kombinasi aman.
"""

from __future__ import annotations

from pathlib import Path

from semweb.store import MuseumStore

AKAR = Path(__file__).resolve().parent.parent.parent
DATA_TTL = AKAR / "data" / "museum-sumatera.ttl"
ONTO_TTL = AKAR / "ontology" / "museum-sumatera.ttl"

_CACHE: dict[str, MuseumStore] = {}


def store_data(ontologi: str | Path | None = None) -> MuseumStore:
    """Store dari data asli, dibangun sekali per kombinasi ontologi.

    `ontologi` diteruskan apa adanya ke `MuseumStore.dari_turtle`, jadi
    `"none"` memberi store tanpa aksioma ontologi — berguna untuk menguji bahwa
    fakta turunan memang bergantung pada ontologi.
    """
    kunci = str(ontologi)
    if kunci not in _CACHE:
        _CACHE[kunci] = MuseumStore.dari_turtle(path=DATA_TTL, ontologi=ontologi)
    return _CACHE[kunci]
