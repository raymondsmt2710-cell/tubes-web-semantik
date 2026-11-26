"""Pembacaan ``.env`` tanpa dependensi tambahan.

Proyek ini sengaja tidak memakai ``python-dotenv``. Pola ``KEY=VALUE`` yang
dipakai cukup sederhana untuk dibaca sendiri, dan satu berkas kecil lebih mudah
dipertanggungjawabkan daripada satu paket tambahan.

Aturan yang dipegang:

- **Lingkungan menang atas berkas.** Variabel yang sudah diset di shell tidak
  boleh ditimpa berkas, supaya CI dan server bisa mengalahkan nilai lokal.
- **Nilai kosong dianggap tidak ada.** ``LLM_API_KEY=`` berarti "belum diisi",
  bukan "kunci berisi string kosong".
- **Berkas yang tidak ada bukan kesalahan.** Tanpa ``.env``, aplikasi tetap
  jalan dengan nilai bawaan.
"""

from __future__ import annotations

import os
from pathlib import Path

__all__ = ["AKAR", "BERKAS_ENV", "baca_env", "nilai_env"]

AKAR = Path(__file__).resolve().parents[2]
BERKAS_ENV = AKAR / ".env"


def baca_env(berkas: Path | str | None = None) -> dict[str, str]:
    """Baca pasangan ``KEY=VALUE`` dari berkas, atau kamus kosong bila tidak ada.

    Komentar (``#``) dan baris tanpa ``=`` dilewati. Tanda kutip pembungkus
    dibuang, karena ``.env`` sering ditulis dengan kutip untuk nilai berspasi.
    """
    jalur = Path(berkas) if berkas is not None else BERKAS_ENV

    if not jalur.exists():
        return {}

    nilai: dict[str, str] = {}

    for baris in jalur.read_text(encoding="utf-8", errors="replace").splitlines():
        bersih = baris.strip()
        if not bersih or bersih.startswith("#") or "=" not in bersih:
            continue

        kunci, _, isi = bersih.partition("=")
        kunci = kunci.strip()
        isi = isi.strip()

        if len(isi) >= 2 and isi[0] == isi[-1] and isi[0] in ("'", '"'):
            isi = isi[1:-1]

        if kunci:
            nilai[kunci] = isi

    return nilai


def nilai_env(
    kunci: str,
    bawaan: str = "",
    berkas: Path | str | None = None,
) -> str:
    """Nilai satu variabel: lingkungan dulu, lalu berkas, lalu bawaan.

    Nilai yang hanya berisi spasi diperlakukan sebagai tidak ada, baik di
    lingkungan maupun di berkas.
    """
    dari_lingkungan = os.environ.get(kunci, "").strip()
    if dari_lingkungan:
        return dari_lingkungan

    dari_berkas = baca_env(berkas).get(kunci, "").strip()
    if dari_berkas:
        return dari_berkas

    return bawaan
