"""Test pembacaan ``.env``: berkas dibaca, lingkungan menang, bentuk aneh aman.

Adapter LLM membaca kunci lewat modul ini. Tanpa modul ini, mengisi ``.env``
tidak berpengaruh apa pun karena ``os.environ`` tidak pernah melihatnya — dan
pengguna akan mengira fitur model rusak padahal kuncinya sudah benar.
"""

from __future__ import annotations

import pytest

from semweb.env import baca_env, nilai_env


def _tulis(tmp_path, isi: str):
    berkas = tmp_path / ".env"
    berkas.write_text(isi, encoding="utf-8")
    return berkas


def test_membaca_pasangan_kunci_nilai(tmp_path):
    berkas = _tulis(tmp_path, "A=1\nB=dua\n")
    assert baca_env(berkas) == {"A": "1", "B": "dua"}


def test_mengabaikan_komentar_dan_baris_kosong(tmp_path):
    berkas = _tulis(
        tmp_path,
        "# komentar\n\n  \nA=1\n   # komentar menjorok\nB=2\n",
    )
    assert baca_env(berkas) == {"A": "1", "B": "2"}


def test_membuang_spasi_di_sekitar_kunci_dan_nilai(tmp_path):
    berkas = _tulis(tmp_path, "  A  =  1  \n")
    assert baca_env(berkas) == {"A": "1"}


def test_membuang_kutip_pembungkus(tmp_path):
    berkas = _tulis(tmp_path, 'A="satu dua"\nB=\'tiga\'\n')
    assert baca_env(berkas) == {"A": "satu dua", "B": "tiga"}


def test_nilai_mengandung_tanda_sama_dipertahankan(tmp_path):
    berkas = _tulis(tmp_path, "URL=http://x/?a=1&b=2\n")
    assert baca_env(berkas)["URL"] == "http://x/?a=1&b=2"


def test_berkas_tidak_ada_menghasilkan_kamus_kosong(tmp_path):
    assert baca_env(tmp_path / "tidak-ada.env") == {}


def test_baris_tanpa_sama_dengan_dilewati(tmp_path):
    berkas = _tulis(tmp_path, "BUKAN_PASANGAN\nA=1\n")
    assert baca_env(berkas) == {"A": "1"}


def test_nilai_env_mengutamakan_lingkungan(tmp_path, monkeypatch):
    berkas = _tulis(tmp_path, "K=dari-berkas\n")
    monkeypatch.setenv("K", "dari-lingkungan")
    assert nilai_env("K", berkas=berkas) == "dari-lingkungan"


def test_nilai_env_jatuh_ke_berkas_bila_lingkungan_kosong(tmp_path, monkeypatch):
    berkas = _tulis(tmp_path, "K=dari-berkas\n")
    monkeypatch.delenv("K", raising=False)
    assert nilai_env("K", berkas=berkas) == "dari-berkas"


def test_nilai_env_memakai_bawaan_bila_tidak_ada_di_mana_pun(tmp_path, monkeypatch):
    berkas = _tulis(tmp_path, "A=1\n")
    monkeypatch.delenv("K", raising=False)
    assert nilai_env("K", bawaan="cadangan", berkas=berkas) == "cadangan"


def test_lingkungan_kosong_dianggap_tidak_ada(tmp_path, monkeypatch):
    berkas = _tulis(tmp_path, "K=dari-berkas\n")
    monkeypatch.setenv("K", "   ")
    assert nilai_env("K", berkas=berkas) == "dari-berkas"


# ------------------------------------------------------- sambungan ke adapter


def test_adapter_membaca_kunci_dari_berkas_env(tmp_path, monkeypatch):
    from semweb.llm import adapter_dari_env

    berkas = _tulis(
        tmp_path,
        "LLM_PROVIDER=openai\nLLM_API_KEY=kunci-dari-berkas\nLLM_MODEL=m\n",
    )
    monkeypatch.delenv("LLM_PROVIDER", raising=False)
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    monkeypatch.delenv("LLM_MODEL", raising=False)

    adapter = adapter_dari_env(berkas=berkas)
    assert adapter is not None


def test_adapter_tetap_none_bila_berkas_tidak_punya_kunci(tmp_path, monkeypatch):
    from semweb.llm import adapter_dari_env

    berkas = _tulis(tmp_path, "LLM_PROVIDER=openai\nLLM_API_KEY=\n")
    monkeypatch.delenv("LLM_API_KEY", raising=False)

    assert adapter_dari_env(berkas=berkas) is None


def test_adapter_tetap_none_bila_berkas_tidak_ada(tmp_path, monkeypatch):
    from semweb.llm import adapter_dari_env

    monkeypatch.delenv("LLM_API_KEY", raising=False)
    assert adapter_dari_env(berkas=tmp_path / "tidak-ada.env") is None
