# Deploy aplikasi Python

Panduan ini cukup diikuti tanpa bertanya. Semua perintah dijalankan dari
**akar repositori** (folder yang berisi `pyapp/`, `data/`, `public/`).

> Yang di-deploy adalah **aplikasi Python** (`pyapp/`, FastAPI). Aplikasi ini
> membaca Turtle langsung dan **tidak membutuhkan Fuseki**, jadi cukup satu
> kontainer. Aplikasi TypeScript (`src/`) tidak termasuk panduan ini.

## 1. Jalankan lokal dengan Docker (satu perintah)

Prasyarat: Docker Desktop / Docker Engine dengan plugin `compose`.

```bash
docker compose up --build
```

Buka <http://localhost:8000>. Hentikan dengan `Ctrl+C`.

Yang terjadi saat build (`pyapp/Dockerfile`):

1. Memasang dependensi dari `pyapp/requirements.txt`.
2. Menyalin `data/museums.json`, `ontology/`, `public/images/`, dan `pyapp/`.
3. Menjalankan `python pyapp/scripts/generate.py` — Turtle selalu dibangkitkan
   ulang dari sumber kebenaran, bukan dari `.ttl` yang kebetulan ter-commit.
4. Menjalankan uvicorn sebagai pengguna non-root di port `$PORT` (default 8000).

Permintaan pertama butuh beberapa detik karena closure OWL-RL dihitung saat itu
(beberapa ribu triple). Permintaan berikutnya cepat.

Tanpa compose, perintah setaranya:

```bash
docker build -f pyapp/Dockerfile -t museum-sumatera .
docker run --rm -p 8000:8000 museum-sumatera
```

> Konteks build **harus** akar repositori (titik `.` di akhir), bukan `pyapp/`,
> karena aplikasi membaca `data/` dan `public/images/` dari luar `pyapp/`.

### Memastikan berjalan

```bash
curl http://localhost:8000/api/kesehatan
# {"status":"ok","triple_asserted":...,"triple_closure":...,"museum":28}
# Angka triple berubah setiap data diperbarui; yang penting "museum": 28.
```

## 2. Variabel lingkungan

| Variabel | Wajib | Kegunaan |
|---|---|---|
| `PORT` | tidak | Port uvicorn. Railway/Fly.io/Render mengisinya otomatis. Default `8000`. |
| `SITUS_URL` | disarankan di produksi | URL publik situs, mis. `https://museum-sumatera.up.railway.app/`. Dipakai untuk `url` dan `image` absolut di JSON-LD. Bila kosong, diambil dari header permintaan. |

| `LLM_PROVIDER`, `LLM_API_KEY`, `LLM_MODEL` | tidak | Adapter LLM opsional (lihat `pyapp/README.md`). Tanpa `LLM_API_KEY` aplikasi memakai penerjemah aturan. |

`.env` sengaja **tidak** ikut masuk image (lihat `.dockerignore`). Isi kunci
API lewat menu Variables di platform, jangan di-commit.

## 3. Deploy ke Railway

1. Masuk ke <https://railway.com>, **New Project → Deploy from GitHub repo**,
   pilih repositori ini.
2. Di **Settings** service: biarkan **Root Directory kosong** (Railway harus
   meng-clone seluruh repositori, karena Dockerfile membutuhkan `data/` dan
   `public/`).
3. Di **Variables**, tambahkan:
   - `RAILWAY_DOCKERFILE_PATH` = `pyapp/Dockerfile`
   - `SITUS_URL` = URL publik yang diberikan Railway (isi setelah langkah 4,
     lalu redeploy).
4. **Settings → Networking → Generate Domain**.
5. (Opsional) **Settings → Deploy → Healthcheck Path** = `/api/kesehatan`.

Tanda berhasil: log build memuat `Turtle ditulis ke /app/data/museum-sumatera.ttl`
dan `/api/kesehatan` di domain publik mengembalikan `"museum": 28`.

## 4. Deploy ke VPS kampus / server Linux

Prasyarat: Docker terpasang, port 80/443 dibuka.

```bash
git clone https://github.com/raymondsmt2710-cell/tubes-web-semantik.git
cd tubes-web-semantik
SITUS_URL=https://museum.contoh.ac.id/ docker compose up -d --build
```

Letakkan reverse proxy (nginx/Caddy) di depan port 8000 untuk HTTPS. Contoh
Caddy (`/etc/caddy/Caddyfile`), sertifikat HTTPS diurus otomatis:

```
museum.contoh.ac.id {
    reverse_proxy 127.0.0.1:8000
}
```

uvicorn dijalankan dengan `--proxy-headers`, sehingga URL di JSON-LD memakai
`https://` dari reverse proxy.

Memperbarui setelah ada commit baru:

```bash
git pull && docker compose up -d --build
```

## 5. Setelah deploy: periksa JSON-LD

1. Buka `https://<domain>/api/museum/museum-negeri-aceh.jsonld`.
2. Tempel URL halaman `https://<domain>/museum/museum-negeri-aceh` ke
   **Schema Markup Validator** (<https://validator.schema.org/>) — harus
   terbaca satu item `Museum` tanpa error.
3. **Rich Results Test** (<https://search.google.com/test/rich-results>)
   hanya menampilkan jenis yang didukung Google untuk hasil kaya. `Museum`
   bukan salah satunya, jadi wajar bila hasilnya "tidak ada hasil kaya yang
   terdeteksi"; yang penting **tidak ada error parsing**. Lampirkan tangkapan
   layar keduanya untuk penilaian.

## 6. Masalah yang sering muncul

| Gejala | Penyebab | Perbaikan |
|---|---|---|
| `COPY data/museums.json: not found` | build dijalankan dari `pyapp/` | jalankan dari akar repositori dengan `-f pyapp/Dockerfile .` |
| Railway membangun Dockerfile yang salah / Railpack | `RAILWAY_DOCKERFILE_PATH` belum diisi atau Root Directory terisi | kosongkan Root Directory, isi variabel, redeploy |
| Foto tidak tampil | `public/images/` tidak ikut ter-copy | pastikan `.dockerignore` tidak mengecualikan `public/` |
| JSON-LD berisi `http://` atau alamat internal | di belakang proxy tanpa header | isi `SITUS_URL` |
| Peta kosong, hanya daftar | CDN unpkg diblokir jaringan | perilaku yang disengaja (progressive enhancement); daftar tetap lengkap |
