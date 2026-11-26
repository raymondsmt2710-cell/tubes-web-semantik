# Rencana Pengerjaan & Pengembangan — Semantic Search Engine Museum Sumatera

**Tanggal:** 26 November 2026
**Status proyek saat ini:** berjalan, 188 test Python + 200 test TypeScript hijau
**Mata kuliah:** Web Semantik (TIF2305) — Tugas Proyek

---

## 1. Ringkasan proyek

Semantic Search Engine untuk **28 museum di Pulau Sumatera**. Data disimpan sebagai
RDF, dinalarkan dengan OWL-RL, dan ditanyai lewat SPARQL. Pengguna dapat mencari
museum dengan penyaringan semantik, melihat relasi antar museum, dan bertanya dengan
bahasa Indonesia.

Yang membedakan proyek ini dari katalog biasa: **pencariannya bekerja dengan
mencocokkan pola pada graf**, bukan mencocokkan teks halaman. Setiap jawaban
menyertakan query yang dipakai sehingga bisa diperiksa ulang.

### 1.1 Kondisi saat ini

| Bagian | Status |
|---|---|
| Data museum | 28 museum, 10 provinsi, 7 bab, 114 isi pameran, 66 foto berlisensi |
| Graf | 3.625 triple asserted → 6.757 setelah penalaran |
| Aplikasi Python (`pyapp/`) | Berjalan — beranda, cari, museum, tanya, metode, API JSON |
| Aplikasi TypeScript (`src/`) | Berjalan — katalog, jelajah bab, tanya |
| Test | 188 (Python) + 200 (TypeScript), semua hijau |
| Triple store | Apache Jena Fuseki, dataset `museum` |

### 1.2 Peta ke materi kuliah

| Pertemuan | Materi | Wujud di proyek |
|---|---|---|
| P1 | Pengantar Web Semantik & Knowledge Graph | Dokumen ini, halaman `/metode` |
| P2 | XML | RDF/XML tersedia lewat `to_rdfxml()` |
| P3 | JSON-LD & structured data | Belum ada — kandidat pengembangan (lihat §5) |
| P4 | Metadata & Dublin Core | `dcterms:created`, `dcterms:modified` pada ontologi |
| P5 | Ontologi RDFS/OWL | `ontology/museum-sumatera.ttl` |
| P6–P7 | RDF, triple, serialisasi | `semweb/generator.py`, `data/museum-sumatera.ttl` |
| P9–P10 | SPARQL SELECT | `semweb/search.py` |
| P11 | SPARQL CONSTRUCT & property path | `semweb/relations.py`, `semweb/construct.py` |
| P12 | Inferensi & reasoning | `semweb/reasoning.py`, `semweb/store.py` |
| P13 | GraphRAG & NL2SPARQL | `semweb/graphrag.py`, `semweb/nl2sparql.py` |

---

## 2. Arsitektur

### 2.1 Alur data

```
data/museums.json  (sumber kebenaran)
        │
        │  generator.py  (rdflib)
        ▼
data/museum-sumatera.ttl  (335 KB, Turtle)
        │
        ├──► store.py ──► asserted (3.625 triple)
        │                 closure OWL-RL (6.757 triple)
        │
        ├──► upload_fuseki.py ──► Apache Jena Fuseki
        │
        ▼
    Modul domain (semweb/*.py)
        ├── search.py      SELECT      → pencarian & filter
        ├── relations.py   CONSTRUCT   → benang merah
        ├── construct.py   CONSTRUCT   → hierarki kelas
        ├── reasoning.py               → asserted vs inferred
        ├── graphrag.py                → jangkar → n-hop → konteks
        └── nl2sparql.py               → pertanyaan → SPARQL → guard → jawaban
        │
        ▼
    main.py (FastAPI) ──► templates/ (Jinja2)
```

### 2.2 Prinsip yang dipegang

1. **Satu sumber kebenaran.** Semua data berasal dari `data/museums.json`. Tidak ada
   data yang hanya hidup di kode.
2. **Penyaringan di dalam SPARQL.** Bukan menyaring list di Python setelah query —
   supaya query bisa dipindah ke Fuseki tanpa berubah arti.
3. **`PREFIX` selalu ditulis lengkap.** Walau editor menyuntikkannya otomatis.
4. **Guard sebelum eksekusi.** Query diperiksa dulu; yang ditolak tidak pernah jalan.
5. **Jawaban hanya dari graf.** Tidak menambah fakta di luar data.
6. **Kode domain bisa diuji tanpa server.** Semua logika ada di `semweb/`, bukan di route.

### 2.3 Struktur berkas

```
pyapp/
  main.py                    FastAPI: halaman + API JSON
  semweb/
    namespace.py             sdp:, res:, prefiks baku
    generator.py             museums.json → Turtle
    store.py                 muat graf + closure OWL-RL & RDFS
    sparql.py                PREFIXES, escaping, helper IRI
    search.py                SELECT: pencarian & filter
    relations.py             CONSTRUCT: benang merah
    construct.py             CONSTRUCT: hierarki & materialisasi
    reasoning.py             asserted vs inferred, konsistensi
    nl2sparql.py             skema, prompt, guard, verbalisasi
    graphrag.py              jangkar, n-hop, subgraf, konteks
  templates/                 Jinja2
  static/style.css
  scripts/                   generate, demo, upload_fuseki
  tests/                     pytest (188 test)
ontology/museum-sumatera.ttl  ontologi
data/
  museums.json               sumber kebenaran
  museum-sumatera.ttl        hasil generator
  museum-sumatera.rdf        dipakai aplikasi TypeScript
public/images/museums/       66 foto berlisensi
```

---

## 3. Cara menjalankan

### 3.1 Prasyarat

- Python 3.10+ (diuji pada 3.12)
- Node.js 20+ (untuk aplikasi TypeScript)
- Java 17+ dan Apache Jena Fuseki (opsional, untuk triple store terpisah)

### 3.2 Aplikasi Python

```bash
cd pyapp
pip install -r requirements.txt
python scripts/generate.py          # museums.json → Turtle
python -m uvicorn main:app --port 8000
```

Buka <http://localhost:8000>.

### 3.3 Aplikasi TypeScript

```bash
npm install
npm run generate:rdf
npm run check:rdf
npm run upload:fuseki               # butuh Fuseki
npm run dev
```

Buka <http://localhost:3000>.

### 3.4 Test

```bash
cd pyapp && pytest                  # 188 test
npx vitest run                      # 200 test
```

---

## 4. Riwayat pengerjaan (yang sudah selesai)

### 4.1 Fase 1 — Aplikasi TypeScript (fondasi)

| Tahap | Isi | Hasil |
|---|---|---|
| 1 | 28 museum sebagai data, 7 bab perjalanan | `data/museums.json` |
| 2 | Generator RDF + ontologi | `museum-sumatera.rdf`, `.ttl` |
| 3 | Katalog, pencarian, halaman museum | `src/app/` |
| 4 | Benang merah antar museum | bobot tema/kota/era/bab |
| 5 | Pemasangan Fuseki + dataset `museum` | 28 museum terverifikasi |
| 6 | Memperdalam isi pameran & galeri | deskripsi 86 → 563 karakter |
| 7 | NL2SPARQL di sisi TypeScript | `src/lib/nl2sparql.ts` |

### 4.2 Fase 2 — Revisi ke Python

Alasan revisi: materi kuliah mengajarkan Python (`rdflib`, `owlrl`), sedangkan
aplikasi pertama memakai TypeScript. Data dan tema dipertahankan.

| Tahap | Isi | Test |
|---|---|---|
| 1 | Generator Turtle + namespace | 9 |
| 2 | Store graf + closure OWL-RL | 8 |
| 3 | Pencarian SPARQL SELECT | 17 |
| 4 | Benang merah CONSTRUCT + property path | 10 |
| 5 | Penalaran asserted vs inferred | 10 |
| 6 | Skema graf + guard NL2SPARQL | 56 |
| 7 | GraphRAG retrieval | (bawaan modul) |
| 8 | Aplikasi web FastAPI + Jinja2 | 26 |
| 9 | Skrip CLI + README | — |

### 4.3 Fase 3 — Perbaikan bug (review independen)

Dua putaran review menemukan bug nyata. Semua diperbaiki lewat test yang gagal dulu.

**Putaran 1 — 6 temuan serius:**

| Tingkat | Bug | Perbaikan |
|---|---|---|
| Critical | Guard bisa dilewati lewat property path (`sdp:x+`) | `_iri_di` menangani `rdflib.paths.Path` |
| Critical | "berapa harga tiket pesawat **ke Aceh**?" → "Ada 28 museum" | daftar `_DI_LUAR_DOMAIN` |
| Critical | `fakta_turunan` selalu 0; `/metode` kontradiksi | generator menulis tipe spesifik saja |
| Important | `LIMIT` tidak ditegakkan di subquery/OFFSET | `_slice_di()` menelusuri seluruh pohon |
| Important | "berapa provinsi?" → "Ada 10 museum" | peta satuan lengkap |
| Important | jangkar diabaikan di cabang hitung (114 vs 5 pameran) | jangkar mempersempit query |

**Putaran 2 — 9 temuan minor + 5 temuan tambahan hasil fuzz:**

`maks` tidak bisa dinaikkan · `xsd:integer()` pada `gYear` diganti `STR()` ·
"koleksi" dipisah dari "pameran" · fallback nama bukan slug · `int(gYear)` aman ·
`bool("false")` dibaca False · titik koma query dirapikan · `LIMIT` di benang merah ·
konsistensi memeriksa closure · satuan "galeri" → "foto" · daftar terpotong diberi
keterangan · "alamat museum?" tidak menjawab satu museum acak · slug URL divalidasi ·
graf kosong memberi pesan jelas.

---

## 5. Rencana pengembangan

Diurutkan berdasarkan **dampak terhadap nilai proyek** lalu **biaya**. Setiap item
punya kriteria selesai yang bisa diperiksa.

### 5.1 Prioritas tinggi — menutup celah materi

#### P1. JSON-LD & structured data (P3)

**Mengapa:** P3 diajarkan tetapi belum ada wujudnya. Ini juga cara paling nyata
memperlihatkan Web Semantik ke mesin pencari.

**Yang dikerjakan:**
- Ekspor `data/museum-sumatera.jsonld` dari graf yang sama.
- Halaman museum menyisipkan `<script type="application/ld+json">` dengan
  kosakata `schema.org` (`@type: Museum`, `name`, `address`, `geo`, `openingHours`).
- Endpoint `/api/museum/{slug}.jsonld`.

**Kriteria selesai:**
- JSON-LD lolos validasi `search.google.com/test/rich-results`.
- Test: JSON-LD yang dihasilkan, bila di-parse balik ke RDF, menghasilkan triple
  yang sama dengan graf asal untuk properti yang dipetakan.

#### P2. Perbandingan RDFS vs OWL-RL yang bisa dijelaskan

**Mengapa:** `/metode` sudah menampilkan angka, tetapi belum menjelaskan **aturan
mana** yang menurunkan fakta mana. Ini inti P12.

**Yang dikerjakan:**
- Tabel: untuk setiap fakta turunan, sebutkan aturan yang menghasilkannya
  (`rdfs9`, `rdfs11`, `prp-symp`, dll).
- Panel "jalankan penalaran bertahap": tampilkan putaran 1, 2, 3 sampai fixpoint
  seperti contoh Mona Lisa pada materi.

**Kriteria selesai:** pengguna dapat menelusuri satu kesimpulan dari fakta awal
sampai kesimpulan akhir, dengan nama aturan di setiap langkah.

#### P3. Materialisasi ke Fuseki (P11)

**Mengapa:** `construct.py` sudah punya `materialisasi()`, tetapi hasilnya belum
pernah disimpan. Materi P11 menekankan CONSTRUCT menghasilkan graf baru.

**Yang dikerjakan:**
- Skrip `scripts/materialisasi.py`: jalankan CONSTRUCT, simpan hasil sebagai
  named graph `res:graph/closure` di Fuseki.
- Bandingkan waktu query: closure dihitung saat query vs sudah dimaterialisasi.

**Kriteria selesai:** ada angka waktu query sebelum/sesudah materialisasi pada
dataset 28 museum.

### 5.2 Prioritas sedang — memperkuat kualitas

#### P4. LLM sungguhan untuk NL2SPARQL

**Mengapa:** materi P13 memakai LLM. Saat ini penerjemah berbasis aturan (deterministik).
Adapter sudah disiapkan lewat parameter `penerjemah`/`llm`.

**Yang dikerjakan:**
- Adapter ke satu penyedia (OpenAI/Gemini/Groq) yang membaca API key dari `.env`.
- **Guard tetap wajib** — query dari model tidak boleh langsung dieksekusi.
- Halaman `/tanya` menampilkan pilihan: "aturan" atau "model".

**Kriteria selesai:** dengan 10 pertanyaan uji, bandingkan hasil aturan vs model:
jumlah yang lolos guard, jumlah yang jawabannya benar, dan waktu respons.

#### P5. Uji kepatuhan ontologi (OWL 2 RL)

**Mengapa:** README menyebut HermiT, tetapi belum pernah dijalankan otomatis.

**Yang dikerjakan:**
- Skrip yang memeriksa: setiap properti punya `domain`/`range`, tidak ada properti
  bermakna ganda, `owl:disjointWith` konsisten dengan data.
- Opsional: jalankan `robot reason` bila tersedia.

**Kriteria selesai:** skrip keluar dengan kode 1 bila ontologi melanggar aturan,
dan lulus pada ontologi sekarang.

#### P6. Foto tambahan dari Wikimedia Commons

**Mengapa:** 4 museum hanya punya 1 foto (Museum Lampung, Ketransmigrasian,
Linggam Cahaya, Kereta Api Sawahlunto).

**Yang dikerjakan:** tambah 1–2 foto per museum untuk yang masih minim, dengan
`credit`, `license`, `licenseUrl`, `sourceUrl` lengkap.

**Kriteria selesai:** tidak ada museum dengan kurang dari 2 foto; `check:rdf` nol
peringatan kedalaman.

> **Peringatan:** lisensi wajib diperiksa satu per satu. Salah lisensi =
> pelanggaran hak cipta. Jangan mengarang kredit.

### 5.3 Prioritas rendah — pemantapan

| Item | Isi | Kriteria selesai |
|---|---|---|
| P7 | Halaman peta museum (Leaflet + koordinat yang sudah ada) | 28 museum tampil di peta |
| P8 | Ekspor hasil pencarian ke CSV/JSON | tombol unduh di `/cari` |
| P9 | Aksesibilitas: kontras, `alt`, navigasi keyboard | lolos pemeriksaan axe tanpa error |
| P10 | Mode gelap | mengikuti `prefers-color-scheme` |
| P11 | Deploy (Railway/Fly.io/VPS) + dokumentasi | URL publik aktif, Fuseki terjangkau |

---

## 6. Perbaikan bug yang masih terbuka

Tidak ada bug yang diketahui saat ini — 188 test Python dan 200 test TypeScript
hijau. Namun ada **risiko** yang belum tertutup dan sebaiknya diperiksa:

| # | Risiko | Cara memunculkannya | Perbaikan bila muncul |
|---|---|---|---|
### R1 `tahun_min` salah untuk tahun di bawah 1000 — ✅ **SUDAH DIPERBAIKI**

Dulu `search.py` membandingkan tahun sebagai string (`STR(?tahun) >= "1000"`),
sehingga `"950" > "1000"` secara leksikografis. Sudah diperbaiki menjadi
perbandingan (panjang, isi) yang benar untuk tahun berapa pun digitnya, dengan
test regresi di `pyapp/tests/test_rencana_regresi.py`.

**Jangan dikerjakan ulang.** Bila ingin memeriksa: `pytest tests/test_rencana_regresi.py`.

### R2 Subquery tiga level di guard

Guard menolak subquery tanpa `LIMIT` pada dua level. Belum diuji tiga level.
Pemilik: **Ryan F** (berkas `nl2sparql.py` milik Ryan D — minta izin dulu).

### R3 Jangkar meleset untuk nama museum yang pendek — **BUG, perlu diperbaiki**

**Terbukti:** pertanyaan `"Museum Aceh"` menghasilkan jangkar **provinsi Aceh**,
bukan museum. Museum bernama "Museum Negeri Aceh" tidak ikut terpilih karena
pencarian menuntut label lengkap muncul di teks.

Pemilik: **Ryan D** (berkas `graphrag.py`).

### R4 Data tahun berbentuk tanggal

`_tahun_dari()` di `main.py` sudah aman, tetapi `search.py` belum menangani
`establishedYear` berbentuk `"1915-01-01"`. Belum ada di data, tetapi bisa muncul
bila data diperluas. Pemilik: **Alvin**.

### R5 Fuseki mati saat halaman dibuka

Aplikasi Python **tidak** bergantung Fuseki (membaca Turtle langsung), jadi tetap
jalan. Aplikasi TypeScript bergantung Fuseki; perlu pesan jelas. Pemilik: **Cherles**.

### Yang sudah diperbaiki (jangan dikerjakan ulang)

Slug URL divalidasi · `bool("false")` dibaca False · "koleksi" dipisah dari
"pameran" · graf kosong memberi pesan jelas · daftar terpotong diberi keterangan ·
"alamat museum?" tidak menjawab museum acak · satuan "galeri" → "foto".

---

## 7. Konvensi kerja

### 7.1 Alur kerja

1. **Satu tugas, satu cabang git.** `git checkout -b feat/nama-tugas`.
2. **Tulis test dulu**, jalankan, pastikan **gagal**, baru tulis kode.
3. Jalankan **seluruh** suite sebelum commit.
4. Commit kecil dengan pesan jelas: `feat(py): ...`, `fix(py): ...`, `docs: ...`.
5. Ajukan pull request; minimal satu orang lain meninjau.

### 7.2 Aturan penulisan kode

- **Penyaringan di dalam SPARQL**, bukan di Python.
- **`PREFIX` ditulis lengkap** di dalam string query.
- **Kata kunci pengguna tidak pernah disambung mentah** ke query.
- **Jawaban hanya dari graf**; hasil kosong berarti "tidak ditemukan", bukan alasan mengarang.
- **Komentar menjelaskan "mengapa"**, bukan "apa" — kode sudah menjelaskan apa.
- **Pesan ke pengguna dalam Bahasa Indonesia**, menyebut langkah berikutnya.

### 7.3 Daftar periksa sebelum merge

- [ ] `pytest` hijau
- [ ] `npx vitest run` hijau (bila menyentuh TypeScript)
- [ ] `python scripts/generate.py` menghasilkan Turtle yang sama
- [ ] Tidak ada `print` debug yang tertinggal
- [ ] Pesan error diuji: apa yang dilihat pengguna bila input salah?
- [ ] Dokumentasi diperbarui bila perilaku berubah

---

## 8. Pembagian tugas

Lihat dokumen terpisah: [`2026-11-26-tugas-tim-4-orang.md`](2026-11-26-tugas-tim-4-orang.md).
