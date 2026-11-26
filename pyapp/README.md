# Semantic Search Engine Museum Sumatera (Python)

Pencarian semantik untuk 28 museum di Pulau Sumatera. Seluruh data disimpan
sebagai RDF, dinalarkan dengan OWL-RL, dan ditanyai lewat SPARQL. Antarmuka web
dibangun dengan FastAPI, sedangkan logika domain ada di paket Python murni yang
bisa diuji tanpa server.

Proyek ini adalah revisi dari aplikasi Next.js/TypeScript di akar repo. Data dan
temanya sama; yang berubah adalah teknologinya: **Python, rdflib, dan owlrl**,
mengikuti materi kuliah Web Semantik.

## Peta ke materi kuliah

| Materi | Pertemuan | Wujud di proyek ini |
|---|---|---|
| Model triple, URI, Turtle | P6–P7 | `semweb/generator.py`, `semweb/namespace.py` |
| Ontologi RDFS & OWL | P5 | `ontology/museum-sumatera.ttl`, kelas di `generator.py` |
| SPARQL SELECT | P9–P10 | `semweb/search.py` (filter di dalam query) |
| SPARQL CONSTRUCT & property path | P11 | `semweb/relations.py`, `semweb/construct.py` |
| Inferensi & reasoning | P12 | `semweb/reasoning.py`, `semweb/store.py` (`DeductiveClosure`) |
| GraphRAG & NL2SPARQL | P13 | `semweb/graphrag.py`, `semweb/nl2sparql.py` |
| Antarmuka | — | `main.py`, `templates/` |

## Prasyarat

- Python 3.10 atau lebih baru
- (opsional) Apache Jena Fuseki, untuk menjalankan graf di triple store terpisah.
  Panduan ada di [`docs/fuseki-setup.md`](../docs/fuseki-setup.md).

## Menjalankan

```bash
cd pyapp

# 1. Pasang dependensi
pip install -r requirements.txt

# 2. Hasilkan Turtle dari data museum
python scripts/generate.py

# 3. Jalankan aplikasi web
python -m uvicorn main:app --port 8000
```

Buka <http://localhost:8000>.

Bila `data/museum-sumatera.ttl` belum ada, aplikasi akan menghasilkannya sendiri
saat pertama dijalankan — langkah 2 hanya untuk memastikan lebih dulu.

### Unggah ke Fuseki (opsional)

```bash
python scripts/upload_fuseki.py
```

Skrip ini mengganti seluruh isi graph default lewat Graph Store Protocol, jadi
tidak ada sisa entri lama. Endpoint dibaca dari `FUSEKI_UPDATE` di `.env`.

### Demo ujung-ke-ujung

```bash
python scripts/demo.py
python scripts/demo.py "Berapa jumlah pameran di Museum Negeri Aceh?"
```

Demo menelusuri lima lapisan berurutan: ringkasan graf dan penalaran, hierarki
kelas dengan `CONSTRUCT`, pencarian `SELECT`, benang merah, lalu GraphRAG dan
NL2SPARQL.

### Test

```bash
pytest
```

## Halaman

| Halaman | Isi |
|---|---|
| `/` | Ringkasan graf dan hirarki kelas museum |
| `/cari` | Pencarian dengan filter provinsi, tema, era, tahun minimum |
| `/museum/{slug}` | Satu museum: isi pameran, galeri, benang merah, rantai penalaran |
| `/tanya` | Pertanyaan bahasa Indonesia → SPARQL → guard → jawaban |
| `/metode` | Asserted vs closure, fakta turunan, konsistensi, skema dari graf |
| `/api/docs` | Dokumentasi OpenAPI |

API JSON tersedia di `/api/cari`, `/api/museum/{slug}`, `/api/tanya`,
`/api/metode`, dan `/api/kesehatan`.

## Cara kerja

### 1. Data menjadi triple

`data/museums.json` adalah sumber kebenaran. `semweb/generator.py` mengubahnya
menjadi `data/museum-sumatera.ttl` dengan aturan yang sama seperti aplikasi lama:

- `sdp:` = `https://museumsumatera.id/ontology#`
- `res:` = `https://museumsumatera.id/resource/`
- Teks memakai `@id`; `establishedYear` memakai `xsd:gYear`; urutan memakai
  `xsd:integer`; `exhibitHighlight` memakai `xsd:boolean`.

Poin pengamatan foto disimpan sebagai **node tersendiri** (`sdp:ImageDetail`
dengan `sdp:detailIndex` dan `sdp:detailText`), bukan sebagai dua properti pada
foto. Alasannya: bila indeks dan teks dua properti terpisah pada node yang sama,
kueri SPARQL menghasilkan perkalian silang dan urutan poin menjadi acak.

### 2. Penalaran

`semweb/store.py` memuat graf dua kali: satu apa adanya (`asserted`), satu
diperluas dengan `DeductiveClosure(OWLRL_Semantics)`. Pencarian memakai closure
agar fakta turunan ikut ditemukan; halaman `/metode` membandingkan keduanya.

Contoh pada data ini: 3.623 triple asserted menjadi 6.712 setelah penalaran.

### 3. Pencarian

Semua penyaringan dijalankan **di dalam SPARQL**, bukan dengan menyaring list di
Python setelah query. Setiap kata pada kata kunci harus muncul di salah satu
bidang yang dicari (nama, kota, provinsi, tema, era, deskripsi).

### 4. Guard NL2SPARQL

Pertanyaan diterjemahkan dengan aturan (deterministik), lalu diperiksa sebelum
dieksekusi:

1. sintaks sah (`prepareQuery`)
2. hanya `SELECT` — `ASK`, `CONSTRUCT`, `INSERT`, `DELETE` ditolak
3. `LIMIT` ada dan tidak melebihi 50
4. semua IRI dikenal graf

Query yang ditolak **tidak pernah dijalankan**. Pertanyaan yang tidak menyebut
apa pun dari graf dijawab terus terang, bukan dengan angka asal-asalan.

### 4b. Adapter LLM (opsional)

Penerjemah aturan tetap menjadi jalur bawaan. Model bahasa bisa dipakai sebagai
jalur kedua untuk dibandingkan, lewat `semweb/llm.py`.

Isi `.env`:

```
LLM_PROVIDER=openai        # openai, groq, atau gemini
LLM_API_KEY=...            # jangan di-commit
LLM_MODEL=                 # kosongkan untuk model bawaan
```

Yang dijaga:

- **Tanpa `LLM_API_KEY`, adapter tidak dibuat.** Aplikasi tetap jalan dengan
  penerjemah aturan; tidak ada crash dan tidak ada peringatan.
- **Query dari model tetap melewati guard yang sama.** Tidak ada jalan pintas:
  `jawab()` memanggil `aman()` sebelum eksekusi, siapa pun yang menulis query.
- **Kegagalan jaringan menghasilkan query kosong**, yang lalu ditolak guard
  dengan pesan yang bisa dibaca pengguna — bukan halaman error.
- **Kunci tidak pernah ditulis di kode** dan tidak ikut tercatat di badan
  permintaan.

Membandingkan kedua jalur pada 10 pertanyaan:

```bash
python scripts/bandingkan_llm.py
```

Tanpa kunci, skrip hanya menjalankan jalur aturan dan memberi tahu bahwa
pembandingan belum bisa dilakukan; kode keluarnya tetap 0.

## Struktur

```
pyapp/
  main.py                  FastAPI: halaman + API JSON
  semweb/
    namespace.py           sdp:, res:, prefiks baku
    generator.py           museums.json -> Turtle
    store.py               muat graf + closure OWL-RL & RDFS
    sparql.py              PREFIXES, escaping, helper IRI
    search.py              SELECT: pencarian & filter
    relations.py           CONSTRUCT: benang merah
    construct.py           CONSTRUCT: hierarki & materialisasi
    reasoning.py           asserted vs inferred, konsistensi
    nl2sparql.py           skema, prompt, guard, verbalisasi
    llm.py                 adapter model bahasa (opsional)
    graphrag.py            jangkar, n-hop, subgraf, konteks
  templates/               Jinja2
  static/style.css
  scripts/                 generate, demo, upload_fuseki
  tests/                   pytest
```

## Catatan verifikasi

Seluruh entri berstatus **perlu-verifikasi**. Nama, alamat, tahun berdiri, dan
catatan kunjungan disusun untuk keperluan pembelajaran dan belum diperiksa ulang
terhadap sumber resmi museum. Jangan memakai data di sini sebagai rujukan
perjalanan tanpa memeriksanya kembali.

Foto berasal dari Wikimedia Commons dengan lisensi CC0, CC BY, CC BY-SA, atau
domain publik; kredit dan tautan lisensinya ditampilkan di bawah setiap gambar.
