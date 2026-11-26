"""Adapter LLM untuk NL2SPARQL: satu penyedia, dipakai bergantian dengan aturan.

Materi P13 langkah 2 menyebut "LLM membuat query SPARQL". Modul ini menyediakan
jalur itu tanpa mengorbankan pagar keamanan:

- **Kunci dibaca dari lingkungan**, tidak pernah ditulis di kode.
- **Tanpa kunci, adapter tidak ada.** Pemanggil jatuh ke penerjemah aturan, jadi
  aplikasi tetap jalan tanpa jaringan dan tanpa akun.
- **Query dari model tetap melewati guard** di :func:`semweb.nl2sparql.jawab`.
  Adapter ini hanya menulis teks; ia tidak pernah mengeksekusi apa pun.
- **Kegagalan apa pun menghasilkan string kosong**, bukan exception. Guard akan
  menolak string kosong, sehingga pengguna melihat penolakan yang jelas alih-alih
  halaman error.

Bentuk balasan tiap penyedia berbeda, dan itu satu-satunya hal yang
penyedia-spesifik di sini. Pemanggilan HTTP-nya sendiri seragam supaya bisa
diganti tiruan saat test.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Callable

from .env import nilai_env
from .nl2sparql import prompt
from .store import MuseumStore

__all__ = [
    "NAMA_ENV_KUNCI",
    "NAMA_ENV_MODEL",
    "NAMA_ENV_PENYEDIA",
    "adapter_dari_env",
    "bersihkan_query",
    "buat_adapter",
    "daftar_penyedia",
    "susun_pesan",
]

NAMA_ENV_KUNCI = "LLM_API_KEY"
NAMA_ENV_MODEL = "LLM_MODEL"
NAMA_ENV_PENYEDIA = "LLM_PROVIDER"

WAKTU_TUNGGU = 30

# Bentuk permintaan dan pembacaan balasan per penyedia. ``url`` memakai ``{}``
# untuk model, karena hanya Gemini yang menaruh nama model di path.
_PENYEDIA: dict[str, dict[str, Any]] = {
    "openai": {
        "url": "https://api.openai.com/v1/chat/completions",
        "model": "gpt-4o-mini",
        "gaya": "openai",
    },
    "groq": {
        "url": "https://api.groq.com/openai/v1/chat/completions",
        "model": "llama-3.3-70b-versatile",
        "gaya": "openai",
    },
    "gemini": {
        "url": "https://generativelanguage.googleapis.com/v1beta/models/{}:generateContent",
        "model": "gemini-2.0-flash",
        "gaya": "gemini",
    },
}


def daftar_penyedia() -> dict[str, dict[str, Any]]:
    """Penyedia yang didukung beserta model bawaannya."""
    return {nama: dict(info) for nama, info in _PENYEDIA.items()}


# --------------------------------------------------------------- pembersihan


def bersihkan_query(teks: str) -> str:
    """Ambil query SPARQL dari balasan model yang mungkin berisi pembungkus.

    Model sering membalas dengan pagar markdown, kalimat pengantar, atau
    keduanya. Guard menolak semua itu, dan penolakan atas query buatan sistem
    sendiri membingungkan pengguna. Karena itu pembungkus dibuang di sini,
    bukan di guard: guard tetap ketat, adapter yang sopan.
    """
    if not teks:
        return ""

    isi = teks.strip()

    if "```" in isi:
        bagian = isi.split("```")
        for calon in bagian[1:]:
            bersih = calon.strip()
            if bersih.lower().startswith(("sparql", "sql")):
                bersih = bersih.split("\n", 1)[-1].strip()
            if bersih.upper().startswith(("SELECT", "PREFIX")):
                isi = bersih
                break

    baris = isi.splitlines()
    for i, baris_isi in enumerate(baris):
        if baris_isi.strip().upper().startswith(("SELECT", "PREFIX")):
            isi = "\n".join(baris[i:]).strip()
            break
    else:
        return ""

    if isi.endswith("```"):
        isi = isi[:-3].strip()

    return isi


# ------------------------------------------------------------------- pesan


def susun_pesan(pertanyaan: str, store: MuseumStore) -> list[dict[str, str]]:
    """Pesan bergaya chat: aturan di ``system``, prompt P13 di ``user``.

    Prompt-nya memakai :func:`semweb.nl2sparql.prompt` yang sama dengan jalur
    aturan, supaya skema yang dikirim ke model tidak pernah berbeda dari skema
    yang dipakai guard.
    """
    return [
        {
            "role": "system",
            "content": (
                "Kamu penerjemah pertanyaan Bahasa Indonesia menjadi SPARQL. "
                "Balas hanya query, tanpa penjelasan. Hanya SELECT. "
                "Selalu sertakan LIMIT tidak lebih dari 50. "
                "Jangan memakai IRI di luar skema yang diberikan."
            ),
        },
        {"role": "user", "content": prompt(pertanyaan, store)},
    ]


# ---------------------------------------------------------------- transport


def _kirim_http(
    url: str, tajuk: dict[str, str], badan: dict[str, Any], waktu: int
) -> str:
    """POST JSON dan kembalikan teks balasan.

    Dipisah sebagai fungsi sendiri supaya test bisa menggantinya tanpa jaringan.
    """
    data = json.dumps(badan).encode("utf-8")
    permintaan = urllib.request.Request(url, data=data, method="POST")
    for nama, nilai in tajuk.items():
        permintaan.add_header(nama, nilai)
    permintaan.add_header("Content-Type", "application/json")

    with urllib.request.urlopen(permintaan, timeout=waktu) as jawaban:
        return jawaban.read().decode("utf-8", errors="replace")


def _baca_balasan(gaya: str, teks: str) -> str:
    """Ambil teks query dari balasan penyedia, atau kosong bila bentuknya asing."""
    try:
        data = json.loads(teks)
    except (ValueError, TypeError):
        return ""

    if not isinstance(data, dict):
        return ""

    if gaya == "openai":
        pilihan = data.get("choices")
        if not isinstance(pilihan, list) or not pilihan:
            return ""
        pesan = pilihan[0].get("message") if isinstance(pilihan[0], dict) else None
        if not isinstance(pesan, dict):
            return ""
        isi = pesan.get("content")
        return isi if isinstance(isi, str) else ""

    kandidat = data.get("candidates")
    if not isinstance(kandidat, list) or not kandidat:
        return ""
    isi_kandidat = kandidat[0].get("content") if isinstance(kandidat[0], dict) else None
    if not isinstance(isi_kandidat, dict):
        return ""
    bagian = isi_kandidat.get("parts")
    if not isinstance(bagian, list) or not bagian:
        return ""
    potongan = bagian[0].get("text") if isinstance(bagian[0], dict) else None
    return potongan if isinstance(potongan, str) else ""


def buat_adapter(
    penyedia: str,
    kunci: str,
    model: str,
    pengirim: Callable[[str, dict[str, str], dict[str, Any], int], str] | None = None,
) -> Callable[[str], str]:
    """Bangun fungsi ``prompt -> query`` untuk satu penyedia.

    Fungsi yang dikembalikan **tidak pernah melempar**. Kegagalan jaringan,
    balasan bukan JSON, atau bentuk balasan yang asing semuanya menghasilkan
    string kosong; guard yang akan menolaknya dengan pesan yang bisa dibaca
    pengguna.
    """
    info = _PENYEDIA.get(penyedia)
    if info is None:
        return lambda _prompt: ""

    gaya = info["gaya"]
    url = info["url"].format(model) if "{}" in info["url"] else info["url"]
    kirim = pengirim or _kirim_http

    def adapter(isi_prompt: str) -> str:
        if gaya == "openai":
            tajuk = {"Authorization": f"Bearer {kunci}"}
            badan: dict[str, Any] = {
                "model": model,
                "messages": [
                    {"role": "user", "content": isi_prompt},
                ],
                "temperature": 0,
            }
        else:
            tajuk = {"x-goog-api-key": kunci}
            badan = {
                "contents": [{"parts": [{"text": isi_prompt}]}],
                "generationConfig": {"temperature": 0},
            }

        try:
            mentah = kirim(url, tajuk, badan, WAKTU_TUNGGU)
        except (OSError, urllib.error.URLError, TimeoutError, ValueError):
            return ""

        return bersihkan_query(_baca_balasan(gaya, mentah))

    return adapter


def adapter_dari_env(
    berkas: Path | str | None = None,
) -> Callable[[str], str] | None:
    """Adapter dari ``.env`` dan variabel lingkungan, atau ``None`` bila kosong.

    Lingkungan menang atas berkas, sehingga server dan CI bisa mengalahkan nilai
    lokal. ``None`` adalah jawaban yang sah, bukan kegagalan: aplikasi memang
    harus tetap jalan dengan penerjemah aturan saat tidak ada kunci.
    """
    kunci = nilai_env(NAMA_ENV_KUNCI, berkas=berkas)
    if not kunci:
        return None

    penyedia = nilai_env(NAMA_ENV_PENYEDIA, "openai", berkas=berkas).lower()
    info = _PENYEDIA.get(penyedia)
    if info is None:
        return None

    model = nilai_env(NAMA_ENV_MODEL, "", berkas=berkas) or info["model"]
    return buat_adapter(penyedia=penyedia, kunci=kunci, model=model)
