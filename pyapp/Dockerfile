# Aplikasi Python Semantic Search Engine Museum Sumatera.
#
# Konteks build adalah AKAR repositori (bukan pyapp/), karena aplikasi membaca
# data/ dan public/images/ dari luar folder pyapp/:
#
#   docker build -f pyapp/Dockerfile -t museum-sumatera .
#   docker run --rm -p 8000:8000 museum-sumatera
#
# atau cukup satu perintah dari akar repositori:  docker compose up --build

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8000

WORKDIR /app

# Dependensi dipasang lebih dulu agar layer ini di-cache selama
# requirements.txt tidak berubah.
COPY pyapp/requirements.txt pyapp/requirements.txt
RUN pip install -r pyapp/requirements.txt

COPY data/museums.json data/museums.json
COPY ontology/ ontology/
COPY public/images/ public/images/
COPY pyapp/ pyapp/

# Turtle selalu dibangkitkan dari sumber kebenaran (museums.json) saat build,
# jadi isi kontainer tidak bergantung pada .ttl yang kebetulan ter-commit.
RUN python pyapp/scripts/generate.py

# Jalankan sebagai pengguna biasa, bukan root.
RUN useradd --create-home --uid 10001 museum && chown -R museum /app
USER museum

WORKDIR /app/pyapp
EXPOSE 8000

# Closure OWL-RL dihitung pada permintaan pertama (beberapa detik), maka
# start-period dibuat longgar.
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD python -c "import os,urllib.request; urllib.request.urlopen(f'http://127.0.0.1:{os.environ.get(\"PORT\",\"8000\")}/api/kesehatan', timeout=8)" || exit 1

# PORT diisi otomatis oleh Railway/Fly.io/Render; default 8000 untuk lokal.
# --proxy-headers agar URL absolut di JSON-LD memakai https dari reverse proxy.
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT} --proxy-headers --forwarded-allow-ips='*'"]
