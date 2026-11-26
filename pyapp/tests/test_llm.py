"""Test adapter LLM: penyedia, prompt, dan pagar keamanan.

Yang dikunci di sini bukan kualitas jawaban model — model sungguhan tidak
dipanggil saat test. Yang dikunci adalah kontrak adapter:

1. Tanpa API key, adapter tidak melempar error; ia mengembalikan ``None``
   sehingga pemanggil jatuh ke penerjemah aturan.
2. API key tidak pernah tertulis di kode; hanya dibaca dari lingkungan.
3. Query yang dihasilkan model **tetap** melewati guard — jalur itu diuji
   dengan respons tiruan yang berbahaya.
4. Kegagalan jaringan tidak menjatuhkan aplikasi.
"""

from __future__ import annotations

import json

import pytest

from semweb import llm as modul_llm
from semweb.llm import (
    NAMA_ENV_KUNCI,
    NAMA_ENV_MODEL,
    NAMA_ENV_PENYEDIA,
    adapter_dari_env,
    bersihkan_query,
    daftar_penyedia,
    susun_pesan,
)
from semweb.nl2sparql import jawab
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


@pytest.fixture
def tanpa_env(monkeypatch):
    for nama in (NAMA_ENV_KUNCI, NAMA_ENV_MODEL, NAMA_ENV_PENYEDIA):
        monkeypatch.delenv(nama, raising=False)


# ------------------------------------------------------- daftar penyedia


def test_daftar_penyedia_memuat_tiga_pilihan():
    penyedia = daftar_penyedia()
    assert set(penyedia) == {"openai", "gemini", "groq"}


def test_setiap_penyedia_punya_url_dan_model_bawaan():
    for nama, info in daftar_penyedia().items():
        assert info["url"].startswith("https://"), nama
        assert info["model"], nama
        assert info["gaya"] in ("openai", "gemini"), nama


# ------------------------------------------------------- tanpa API key


def test_tanpa_api_key_adapter_mengembalikan_none(tanpa_env):
    assert adapter_dari_env() is None


def test_penyedia_tak_dikenal_tidak_melempar(tanpa_env, monkeypatch):
    monkeypatch.setenv(NAMA_ENV_KUNCI, "kunci-palsu")
    monkeypatch.setenv(NAMA_ENV_PENYEDIA, "penyedia-yang-tidak-ada")
    assert adapter_dari_env() is None


def test_api_key_tidak_pernah_hardcode():
    sumber = open(modul_llm.__file__, encoding="utf-8").read()
    assert "sk-" not in sumber
    assert "AIza" not in sumber
    assert "gsk_" not in sumber


def test_nama_env_dokumen_sama_dengan_yang_dibaca():
    assert NAMA_ENV_KUNCI == "LLM_API_KEY"
    assert NAMA_ENV_MODEL == "LLM_MODEL"
    assert NAMA_ENV_PENYEDIA == "LLM_PROVIDER"


# ------------------------------------------------------- pembersihan query


def test_bersihkan_query_membuang_pagar_markdown():
    mentah = "```sparql\nSELECT ?s WHERE { ?s ?p ?o } LIMIT 5\n```"
    assert bersihkan_query(mentah) == "SELECT ?s WHERE { ?s ?p ?o } LIMIT 5"


def test_bersihkan_query_membuang_prefiks_penjelasan():
    mentah = "Berikut query-nya:\nSELECT ?s WHERE { ?s ?p ?o } LIMIT 5"
    assert bersihkan_query(mentah).startswith("SELECT")


def test_bersihkan_query_mengembalikan_string_kosong_bila_tidak_ada_select():
    assert bersihkan_query("Maaf, saya tidak bisa membantu.") == ""


def test_bersihkan_query_mempertahankan_prefix_di_dalam_query():
    mentah = (
        "```\nPREFIX sdp: <https://museumsumatera.id/ontology#>\n"
        "SELECT ?s WHERE { ?s a sdp:Museum } LIMIT 5\n```"
    )
    hasil = bersihkan_query(mentah)
    assert hasil.startswith("PREFIX sdp:")
    assert hasil.endswith("LIMIT 5")


# ------------------------------------------------------- susun pesan


def test_susun_pesan_memuat_skema_dan_pertanyaan(store):
    pesan = susun_pesan("museum apa saja di Aceh?", store)
    gabung = "\n".join(p["content"] for p in pesan)
    assert "museum apa saja di Aceh?" in gabung
    assert "sdp:Museum" in gabung
    assert "LIMIT" in gabung


def test_susun_pesan_memakai_peran_system_dan_user(store):
    pesan = susun_pesan("museum apa saja di Aceh?", store)
    assert pesan[0]["role"] == "system"
    assert pesan[1]["role"] == "user"
    assert "museum apa saja di Aceh?" in pesan[1]["content"]


# ------------------------------------------------------- guard tetap berlaku


def test_query_berbahaya_dari_model_tetap_ditolak_guard(store):
    def model_palsu(_prompt: str) -> str:
        return "SELECT ?s WHERE { ?s ?p ?o }"

    hasil = jawab("museum apa saja?", store, penerjemah=model_palsu)
    assert hasil.lolos is False
    assert "LIMIT" in hasil.pesan or "limit" in hasil.pesan.lower()


def test_query_dengan_iri_asing_dari_model_ditolak_guard(store):
    def model_palsu(_prompt: str) -> str:
        return (
            "SELECT ?s WHERE { ?s <http://jahat.example/x> ?o } LIMIT 5"
        )

    hasil = jawab("museum apa saja?", store, penerjemah=model_palsu)
    assert hasil.lolos is False


def test_query_sah_dari_model_diterima_guard(store):
    def model_palsu(_prompt: str) -> str:
        return (
            "SELECT ?nama WHERE { ?m a "
            "<https://museumsumatera.id/ontology#Museum> ; "
            "<https://museumsumatera.id/ontology#name> ?nama } LIMIT 10"
        )

    hasil = jawab("museum apa saja?", store, penerjemah=model_palsu)
    assert hasil.lolos is True
    assert hasil.query


# ------------------------------------------------------- kegagalan jaringan


def test_kegagalan_jaringan_tidak_melempar(tanpa_env, monkeypatch):
    def meledak(*_a, **_k):
        raise OSError("jaringan mati")

    monkeypatch.setattr(modul_llm, "_kirim_http", meledak)
    adapter = modul_llm.buat_adapter(
        penyedia="openai", kunci="kunci-palsu", model="m", pengirim=meledak
    )
    assert adapter("prompt") == ""


def test_balasan_bukan_json_tidak_melempar():
    adapter = modul_llm.buat_adapter(
        penyedia="openai",
        kunci="kunci-palsu",
        model="m",
        pengirim=lambda *a, **k: "bukan json",
    )
    assert adapter("prompt") == ""


def test_balasan_kosong_tidak_melempar():
    adapter = modul_llm.buat_adapter(
        penyedia="openai",
        kunci="kunci-palsu",
        model="m",
        pengirim=lambda *a, **k: json.dumps({}),
    )
    assert adapter("prompt") == ""


# ------------------------------------------------------- bentuk balasan


def test_adapter_openai_membaca_choices_message_content():
    balasan = json.dumps(
        {"choices": [{"message": {"content": "SELECT ?s WHERE { ?s ?p ?o } LIMIT 5"}}]}
    )
    adapter = modul_llm.buat_adapter(
        penyedia="openai",
        kunci="kunci-palsu",
        model="m",
        pengirim=lambda *a, **k: balasan,
    )
    assert adapter("prompt").startswith("SELECT")


def test_adapter_gemini_membaca_candidates_content_parts():
    balasan = json.dumps(
        {"candidates": [{"content": {"parts": [{"text": "SELECT ?s WHERE { ?s ?p ?o } LIMIT 5"}]}}]}
    )
    adapter = modul_llm.buat_adapter(
        penyedia="gemini",
        kunci="kunci-palsu",
        model="m",
        pengirim=lambda *a, **k: balasan,
    )
    assert adapter("prompt").startswith("SELECT")


def test_adapter_membungkus_pagar_markdown_dari_model():
    balasan = json.dumps(
        {"choices": [{"message": {"content": "```sql\nSELECT ?s WHERE { ?s ?p ?o } LIMIT 5\n```"}}]}
    )
    adapter = modul_llm.buat_adapter(
        penyedia="openai",
        kunci="kunci-palsu",
        model="m",
        pengirim=lambda *a, **k: balasan,
    )
    assert adapter("prompt").startswith("SELECT")
    assert "```" not in adapter("prompt")


def test_kunci_tidak_ikut_dicatat_dalam_pesan():
    tercatat: list[dict] = []

    def pengirim(url, tajuk, badan, waktu):
        tercatat.append({"url": url, "tajuk": dict(tajuk), "badan": badan})
        return json.dumps({"choices": [{"message": {"content": "SELECT ?s WHERE { ?s ?p ?o } LIMIT 5"}}]})

    adapter = modul_llm.buat_adapter(
        penyedia="openai", kunci="kunci-rahasia", model="m", pengirim=pengirim
    )
    adapter("prompt")
    assert tercatat
    assert "kunci-rahasia" not in tercatat[0]["badan"]
