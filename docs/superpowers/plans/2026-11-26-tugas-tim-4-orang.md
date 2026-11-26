# Pembagian Tugas Tim — 4 Orang

**Proyek:** Semantic Search Engine Museum Sumatera
**Dokumen induk:** [`2026-11-26-rencana-pengembangan.md`](2026-11-26-rencana-pengembangan.md)
**Tanggal:** 26 November 2026

---

## Cara membaca dokumen ini

Setiap orang mendapat **satu jalur (track)** yang tidak bertabrakan dengan yang lain.
Tugas disusun berurutan: kerjakan dari atas ke bawah. Tanda **[P]** = prioritas.

Setiap tugas punya empat bagian:

- **Apa** — yang dikerjakan
- **Di mana** — berkas yang disentuh
- **Selesai bila** — kriteria yang bisa diperiksa orang lain
- **Bergantung pada** — tugas lain yang harus selesai lebih dulu

> **Aturan main:** tidak ada yang mengerjakan tugas orang lain tanpa bicara dulu.
> Bila satu tugas ternyata menyentuh berkas milik orang lain, koordinasikan lewat
> grup sebelum mulai.

---

## Ringkasan pembagian

| Orang | Track | Fokus | Tugas |
|---|---|---|---|
| **A** | Data & Ontologi | sumber kebenaran, kualitas data, lisensi foto | A1–A4 |
| **B** | SPARQL & Inferensi | query, penalaran, materialisasi | B1–B4 |
| **C** | NL2SPARQL & LLM | pertanyaan bahasa alami, guard, integrasi model | C1–C4 |
| **D** | Antarmuka & Rilis | halaman, aksesibilitas, dokumentasi, deploy | D1–D4 |

**Berkas yang menjadi milik masing-masing** (jangan diubah orang lain tanpa izin):

| Orang | Berkas utama |
|---|---|
| A | `data/museums.json`, `ontology/*.ttl`, `pyapp/semweb/generator.py`, `public/images/` |
| B | `pyapp/semweb/search.py`, `relations.py`, `construct.py`, `reasoning.py`, `store.py` |
| C | `pyapp/semweb/nl2sparql.py`, `graphrag.py`, `pyapp/scripts/demo.py` |
| D | `pyapp/main.py`, `pyapp/templates/`, `pyapp/static/`, `README.md`, `docs/` |

`pyapp/tests/` dipakai bersama — setiap orang menambah berkas test sendiri dengan
nama yang jelas, mis. `test_data_kualitas.py` (A), `test_materialisasi.py` (B).

---

## Orang A — Data & Ontologi

Fokus: memastikan data museum benar, lengkap, dan berlisensi jelas.

### A1. [P] Perbaiki foto yang masih minim — **Perbaikan/kualitas data**

**Apa.** Enam museum hanya punya **1 foto** (terverifikasi pada data sekarang):
- `museum-negeri-lampung`
- `museum-ketransmigrasian-lampung`
- `museum-linggam-cahaya`
- `museum-kereta-api-sawahlunto`
- `museum-negeri-jambi`
- `museum-sultan-sulaiman-badrul-alamsyah`

Tambahkan **1–2 foto** untuk masing-masing, diambil dari Wikimedia Commons.

**Di mana.** `data/museums.json` (bidang `gallery`), `public/images/museums/<slug>/`,
`data/gallery-notes.json`.

**Aturan wajib.**
- Lisensi hanya **CC0, CC BY, CC BY-SA, atau domain publik**. Tidak ada pengecualian.
- Setiap foto wajib punya `credit`, `license`, `licenseUrl`, `sourceUrl` lengkap.
- `background` ≥ 220 karakter, `detail` 2–4 poin.
- **Jangan mengarang kredit.** Bila tidak yakin lisensinya, jangan dipakai.

**Selesai bila:**
- Tidak ada museum dengan kurang dari 2 foto.
- `npm run check:rdf` → 0 error, 0 peringatan kedalaman.
- `python -c "from semweb.generator import load_records, build_graph; ..."` berhasil
  (graf terbentuk tanpa error).

**Bergantung pada:** —

---

### A2. [P] Uji kepatuhan ontologi otomatis — **Pengembangan**

**Apa.** Buat skrip yang memeriksa ontologi secara otomatis, menggantikan
pemeriksaan manual di Protégé.

**Di mana.** Buat baru: `pyapp/scripts/cek_ontologi.py` dan
`pyapp/tests/test_ontologi.py`.

**Yang diperiksa.**
1. Setiap properti objek punya `rdfs:domain` dan `rdfs:range`.
2. Tidak ada properti yang punya dua arti (mis. satu properti dipakai untuk
   dua jenis relasi berbeda).
3. Setiap kelas yang dipakai di data dideklarasikan di ontologi.
4. `owl:disjointWith` tidak dilanggar data.
5. Setiap subkelas museum benar-benar punya individu.

**Selesai bila:**
- Skrip keluar kode `0` pada ontologi sekarang, kode `1` bila diberi ontologi rusak
  (uji dengan fixture yang sengaja dirusak).
- Ada test untuk setiap pemeriksaan di atas.

**Bergantung pada:** —

---

### A3. [P] Verifikasi `tahun_min` untuk tahun < 1000 — ✅ **SUDAH DIPERBAIKI**

Bug ini ditemukan saat menyusun rencana dan **sudah diperbaiki** karena dampaknya
kecil dan perbaikannya singkat. Test regresi ada di
`pyapp/tests/test_rencana_regresi.py`.

**Yang dikerjakan (sudah selesai):**
- `search.py` membandingkan (panjang, isi) tahun, bukan string mentah.
- Test: data tahun `950` dan `1980`; `tahun_min=1000` tidak mengembalikan 950.

**Sisa pekerjaan untuk Orang A:** **jangan dikerjakan ulang.** Cukup jalankan
`pytest tests/test_rencana_regresi.py` untuk memastikan tetap hijau saat mengubah
data. Bila kelak data memuat `establishedYear` berbentuk tanggal
(`"1915-01-01"`), perbaiki `search.py` agar hanya mengambil empat digit pertama.

**Bergantung pada:** —

### A3b. [P] Tangani `establishedYear` berbentuk tanggal — **Perbaikan bug (pencegahan)**

**Apa.** Bila data memuat tahun berbentuk `"1915-01-01"` (bisa terjadi bila
seseorang mengisi tanggal lengkap), filter tahun dan halaman museum harus tetap
bekerja.

**Di mana.** `pyapp/semweb/search.py`, `pyapp/main.py` (`_tahun_dari` sudah aman).
**Minta izin Orang B** untuk `search.py`.

**Yang dikerjakan.** Pastikan pengambilan tahun mengambil empat digit pertama
sebelum dibandingkan. Tambahkan test dengan data berbentuk tanggal.

**Selesai bila:** test baru hijau; filter tahun minimum tetap benar untuk data
berbentuk tanggal.

**Bergantung pada:** izin Orang B.

---

### A4. [P] Verifikasi ulang data museum — **Kualitas data**

**Apa.** Seluruh 28 museum berstatus `perlu-verifikasi`. Periksa minimal **nama,
kota, provinsi, dan tahun berdiri** terhadap sumber resmi (situs museum, Wikipedia,
situs pemerintah daerah).

**Kondisi sekarang:** **24 dari 28 museum hanya punya 1 sumber.** Target minimal
2 sumber per museum.

**Di mana.** `data/museums.json` (bidang `name`, `city`, `province`,
`establishedYear`, `verificationStatus`, `sources`).

**Selesai bila:**
- Setiap museum punya minimal **2 sumber** di bidang `sources`.
- Museum yang sudah diperiksa diubah statusnya menjadi `terverifikasi`.
- Perbedaan yang ditemukan dicatat di kolom komentar commit atau laporan terpisah.
- Museum yang **tidak** bisa diverifikasi tetap `perlu-verifikasi` — jangan dipaksa.

**Bergantung pada:** —

---

## Orang B — SPARQL & Inferensi

Fokus: kebenaran query, penalaran, dan performa triple store.

### B1. [P] Materialisasi closure ke Fuseki — **Pengembangan**

**Apa.** Simpan hasil CONSTRUCT sebagai named graph di Fuseki, lalu bandingkan
waktu query sebelum dan sesudah.

**Di mana.** Buat baru: `pyapp/scripts/materialisasi.py`,
`pyapp/tests/test_materialisasi.py`. Manfaatkan `semweb/construct.py`
(fungsi `materialisasi()` sudah ada).

**Yang dikerjakan.**
1. Jalankan CONSTRUCT materialisasi → graf baru.
2. Unggah hasilnya ke Fuseki sebagai named graph `res:graph/closure`.
3. Ukur: waktu query dengan closure dihitung saat query vs sudah dimaterialisasi.
4. Tulis hasilnya di komentar berkas atau `docs/materialisasi.md`.

**Selesai bila:**
- Ada angka waktu sebelum/sesudah pada data 28 museum.
- Query hasil materialisasi memberi jawaban yang **sama** dengan query closure.
- Ada test yang membandingkan kedua hasil.

**Bergantung pada:** Fuseki berjalan (`docs/fuseki-setup.md`).

---

### B2. [P] Penelusuran aturan penalaran — **Pengembangan**

**Apa.** `/metode` menampilkan fakta turunan, tetapi belum menjelaskan **aturan
mana** yang menghasilkannya. Ini inti materi P12.

**Di mana.** `pyapp/semweb/reasoning.py`, `pyapp/templates/metode.html`
**koordinasi dengan Orang D** untuk template.

**Yang dikerjakan.**
- Untuk setiap fakta turunan, tentukan aturan yang menghasilkannya:
  - `rdfs9` — tipe dari subkelas
  - `rdfs11` — subkelas transitif
  - `rdfs2` / `rdfs3` — domain / range memberi tipe
  - `prp-symp` — properti simetris
  - `prp-inv` — properti invers
- Tampilkan bertahap: putaran 1, 2, 3 sampai tidak ada fakta baru (fixpoint),
  seperti contoh Mona Lisa pada materi.

**Selesai bila:**
- Ada test yang memverifikasi aturan untuk minimal 3 jenis fakta turunan berbeda.
- Halaman `/metode` menampilkan nama aturan di samping setiap fakta turunan.

**Bergantung pada:** —

---

### B3. [P] Perbaiki risiko subquery bersarang di guard — **Perbaikan bug**

**Apa.** Guard menolak subquery tanpa `LIMIT`, tetapi belum diuji untuk
**tiga level** subquery bersarang.

**Di mana.** `pyapp/semweb/nl2sparql.py` (`_slice_di()`).
**Koordinasikan dengan Orang C** — ini berkasnya.

**Yang dikerjakan.**
- Uji query dengan subquery 3 level, pastikan guard menolak yang tanpa `LIMIT`.
- Bila lolos, perbaiki.
- Tambahkan test regresi.

**Selesai bila:**
- Test baru ada dan hijau.
- Guard tetap menerima query sah yang biasa.

**Bergantung pada:** bicara dengan Orang C dulu.

---

### B4. [P] Percepat halaman `/metode` — **Performa**

**Apa.** `/metode` menghitung `fakta_turunan(batas=10_000)` pada setiap kunjungan.
Biayanya tumbuh seiring ukuran closure.

**Di mana.** `pyapp/semweb/reasoning.py`.
**Koordinasikan dengan Orang D** (main.py memanggilnya).

**Yang dikerjakan.**
- Saring subjek `res:` lebih awal di dalam generator (bukan setelah semua
  triple dikumpulkan), atau
- Simpan hasilnya di cache proses, hitung sekali.

**Selesai bila:**
- Waktu render `/metode` turun terukur (catat sebelum/sesudah di komentar commit).
- Test `fakta_turunan` tetap hijau.

**Bergantung pada:** —

---

## Orang C — NL2SPARQL & LLM

Fokus: pertanyaan bahasa Indonesia, keamanan guard, dan integrasi model.

### C1. [P] Adapter LLM sungguhan — **Pengembangan**

**Apa.** Penerjemah sekarang berbasis aturan (deterministik). Materi P13 memakai
LLM. Sambungkan satu penyedia agar keduanya bisa dibandingkan.

**Di mana.** Buat baru: `pyapp/semweb/llm.py`, `pyapp/tests/test_llm.py`.
Manfaatkan parameter `penerjemah` / `llm` yang **sudah ada** di `nl2sparql.py`.

**Aturan wajib.**
- **API key dibaca dari `.env`**, tidak pernah ditulis di kode atau di-commit.
- Query dari model **tetap wajib lolos guard** — tidak ada jalan pintas.
- Bila API key tidak ada, aplikasi harus tetap jalan dengan penerjemah aturan
  (jangan crash).

**Yang dikerjakan.**
1. `llm.py`: fungsi yang memanggil penyedia, mengembalikan teks query.
2. Pilihan di `/tanya`: "aturan" atau "model".
3. Skrip pembanding: 10 pertanyaan uji → untuk tiap pertanyaan, catat
   (a) lolos guard atau tidak, (b) jawabannya benar atau tidak, (c) waktu respons.

**Selesai bila:**
- Ada tabel perbandingan aturan vs model untuk 10 pertanyaan.
- Test: guard tetap menolak query berbahaya yang dihasilkan model (pakai respons
  tiruan/fixture, tidak perlu memanggil API saat test).
- Tanpa API key, `pytest` tetap hijau.

**Bergantung pada:** —

---

### C2. [P] Perbaiki jangkar untuk nama museum pendek — **PERBAIKAN BUG**

**Apa.** `graphrag.jangkar()` menuntut **label lengkap** muncul di pertanyaan.

**Terbukti:** pertanyaan `"Museum Aceh"` menghasilkan jangkar **provinsi Aceh**,
bukan museum "Museum Negeri Aceh" — karena label "Museum Negeri Aceh" tidak muncul
utuh di teks.

**Di mana.** `pyapp/semweb/graphrag.py` (fungsi `jangkar` dan `_memuat`).

**Yang dikerjakan.**
- Uji kasus: `"Museum Aceh"`, `"Museum Negeri Aceh"`, `"Museum Tsunami Aceh"`,
  pertanyaan yang menyebut **dua** museum.
- Pertimbangkan: cocokkan per kata bermakna (bukan label utuh), atau beri skor
  sebagian (partial match) dan pilih yang tertinggi.
- **Jangan merusak** yang sudah benar: `"berapa pameran di Museum Tsunami Aceh?"`
  harus tetap menjawab **4**, bukan 114.

**Selesai bila:**
- Test untuk minimal 4 kasus nama mirip, semuanya hijau.
- `"Museum Aceh"` mengarah ke museum, bukan provinsi (atau jelas menyebut
  bahwa nama itu ambigu).
- Seluruh suite Python tetap hijau.

**Bergantung pada:** —

---

### C3. [P] Guard: larang `GRAPH` dan `FROM` — **Perbaikan bug**

**Apa.** Guard memeriksa IRI, tetapi belum ada test eksplisit bahwa klausa
`GRAPH <...>` dan `FROM <...>` dengan IRI tak dikenal ditolak.

**Di mana.** `pyapp/semweb/nl2sparql.py`, `pyapp/tests/test_nl2sparql.py`.

**Yang dikerjakan.**
- Test: `SELECT ... FROM <http://jahat.example/>`, `GRAPH <http://jahat.example/>`,
  `SERVICE <http://jahat.example/>`.
- Perbaiki bila ada yang lolos.

**Selesai bila:**
- Ketiga bentuk ditolak dengan pesan "IRI tidak dikenal".
- Test lama tetap hijau.

**Bergantung pada:** —

---

### C4. [P] Perluas cakupan pertanyaan — **Pengembangan**

**Apa.** Penerjemah aturan sekarang mengenali: museum, pameran, galeri, provinsi,
kota, tema, era, koleksi. Tambahkan pertanyaan yang wajar ditanyakan pengunjung.

**Di mana.** `pyapp/semweb/nl2sparql.py`, `pyapp/tests/test_nl2sparql.py`.

**Kandidat pertanyaan.**
- "museum apa saja yang punya foto?" (museum dengan `hasImage`)
- "museum yang berdiri sebelum 1950?"
- "apa hubungan Museum A dengan Museum B?"
- "museum tertua di Aceh?"
- "tema apa saja yang ada?" (daftar, bukan hitung)

**Selesai bila:**
- Minimal 4 pertanyaan baru dikenali dengan benar.
- Pertanyaan di luar domain **tetap ditolak** (jangan sampai pelonggaran ini
  membuat "harga tiket pesawat" lolos lagi).
- Ada test untuk setiap pertanyaan baru, termasuk yang harus tetap ditolak.

**Bergantung pada:** C1 (opsional, bila ingin membandingkan dengan model).

---

## Orang D — Antarmuka & Rilis

Fokus: halaman, aksesibilitas, dokumentasi, dan deploy.

### D1. [P] JSON-LD & schema.org — **Pengembangan**

**Apa.** Materi P3 diajarkan, belum ada wujudnya. Tambahkan structured data.

**Di mana.** `pyapp/main.py`, `pyapp/templates/museum.html`,
buat baru `pyapp/semweb/jsonld.py` dan `pyapp/tests/test_jsonld.py`.

**Yang dikerjakan.**
1. `jsonld.py`: ubah satu museum dari graf menjadi JSON-LD dengan kosakata
   `schema.org` (`@type: Museum`, `name`, `address`, `geo`, `openingHours`,
   `url`, `image`).
2. Halaman museum menyisipkan `<script type="application/ld+json">`.
3. Endpoint `/api/museum/{slug}.jsonld`.

**Selesai bila:**
- JSON-LD lolos `search.google.com/test/rich-results` (lampirkan tangkapan layar).
- Test: JSON-LD yang di-parse balik ke RDF menghasilkan triple yang sama dengan
  graf asal untuk properti yang dipetakan.
- Tidak ada `None` yang bocor ke JSON-LD.

**Bergantung pada:** —

---

### D2. [P] Aksesibilitas — **Pengembangan**

**Apa.** Pastikan halaman bisa dipakai pembaca layar dan keyboard.

**Di mana.** `pyapp/templates/`, `pyapp/static/style.css`.

**Yang dikerjakan.**
- Kontras warna memenuhi WCAG AA (4.5:1 untuk teks biasa).
- Setiap `<img>` punya `alt` bermakna.
- Navigasi bisa dilakukan hanya dengan keyboard (Tab, Enter).
- Ada `skip-link` ke konten utama.
- Ukuran teks bisa diperbesar tanpa merusak tata letak.

**Selesai bila:**
- Pemeriksaan axe DevTools pada 5 halaman utama: **0 error**.
- Tab melalui beranda sampai footer tidak tersangkut.

**Bergantung pada:** —

---

### D3. [P] Halaman peta museum — **Pengembangan**

**Apa.** Data `latitude`/`longitude` sudah ada untuk semua museum, tetapi belum
ditampilkan di peta.

**Di mana.** Buat baru `pyapp/templates/peta.html`, tambah route di `pyapp/main.py`.

**Yang dikerjakan.**
- Peta dengan Leaflet (dari CDN, bukan npm — proyek Python tidak perlu bundler).
- 28 penanda museum, klik → tautan ke halaman museum.
- Bisa disaring per provinsi.

**Selesai bila:**
- Semua 28 museum tampil di posisi yang benar.
- Tanpa JavaScript, halaman tetap menampilkan daftar museum (progressive enhancement).

**Bergantung pada:** —

---

### D4. [P] Deploy & dokumentasi rilis — **Pengembangan**

**Apa.** Proyek berjalan lokal. Perlu bisa diakses juri/dosen lewat URL.

**Di mana.** Buat baru: `pyapp/Dockerfile`, `docs/deploy.md`, perbarui `README.md`.

**Yang dikerjakan.**
1. `Dockerfile` untuk aplikasi Python (uvicorn).
2. Panduan deploy ke satu platform (Railway / Fly.io / VPS kampus).
3. Dokumentasi keputusan: mengapa Python, mengapa data sama dengan versi TypeScript.
4. Bagian "Batasan yang diketahui" di README — supaya penilaian jujur.

**Selesai bila:**
- Aplikasi bisa dijalankan dengan satu perintah Docker.
- `docs/deploy.md` cukup diikuti orang lain tanpa bertanya.
- README menyebut: apa yang belum dikerjakan (mis. foto masih minim di 4 museum),
  dan mengapa.

**Bergantung pada:** D1 (JSON-LD sebaiknya sudah ada sebelum deploy).

---

## Urutan pengerjaan yang disarankan

```
Minggu 1     A1  A4        B1  B2        C2  C3        D1  D2
Minggu 2     A2  A3        B3  B4        C1  C4        D3  D4
Minggu 3     integrasi: gabungkan semua cabang, uji bersama, siapkan presentasi
```

**Titik integrasi:** setiap akhir minggu, semua orang merge ke `main` dan
menjalankan **kedua** suite test bersama. Bila ada yang merah, **hentikan**
penambahan fitur sampai hijau.

---

## Pembagian perbaikan bug secara ringkas

Status **terverifikasi** pada 26 November 2026.

| Bug / risiko | Status | Pemilik | Butuh izin dari |
|---|---|---|---|
| `tahun_min` salah untuk tahun < 1000 | ✅ sudah diperbaiki | — | — |
| Jangkar meleset: "Museum Aceh" → provinsi, bukan museum (**terbukti**) | **AKTIF** | C | — |
| Foto hanya 1 buah di **6** museum | Kualitas data | A | — |
| **24 dari 28** museum hanya punya 1 sumber | Kualitas data | A | — |
| Subquery 3 level di guard | Belum diuji | B | C (`nl2sparql.py`) |
| `/metode` lambat (hitung 10.000 fakta tiap kunjungan) | Performa | B | D (`main.py`) |
| `GRAPH`/`FROM`/`SERVICE` di guard | **Sudah ditolak** — perlu test formal | C | — |
| Data tahun berbentuk tanggal (`1915-01-01`) | Pencegahan | A | B (`search.py`) |
| Slug URL tidak sah | ✅ sudah diperbaiki | — | — |
| `bool("false")` dibaca True | ✅ sudah diperbaiki | — | — |
| "koleksi" dianggap "pameran" | ✅ sudah diperbaiki | — | — |
| Graf kosong: pesan menyesatkan | ✅ sudah diperbaiki | — | — |
| Daftar terpotong menyamar sebagai total | ✅ sudah diperbaiki | — | — |
| "alamat museum?" menjawab museum acak | ✅ sudah diperbaiki | — | — |
| Satuan "galeri" seharusnya "foto" | ✅ sudah diperbaiki | — | — |

---

## Aturan kolaborasi

1. **Satu tugas, satu cabang.** `git checkout -b feat/A1-foto-lampung`.
2. **Test dulu, baru kode.** Jalankan test, lihat gagal, baru perbaiki.
3. **Seluruh suite hijau** sebelum commit — bukan hanya test yang baru dibuat.
4. **Commit kecil dan sering.** Pesan: `feat(py): tambah foto Museum Lampung`.
5. **Jangan mengubah berkas milik orang lain** tanpa bicara dulu di grup.
6. **Bila macet lebih dari 30 menit, tanya.** Jangan diam-diam mengerjakan
   hal lain yang bukan tugasmu.
7. **Setiap perbaikan bug wajib punya test** yang gagal sebelum diperbaiki —
   kalau tidak, bug yang sama akan kembali.

---

## Daftar periksa sebelum presentasi

- [ ] `cd pyapp && pytest` → semua hijau
- [ ] `npx vitest run` → semua hijau
- [ ] `npm run check:rdf` → 0 error
- [ ] Aplikasi Python jalan tanpa error di browser (cek konsol)
- [ ] Aplikasi TypeScript jalan tanpa error di browser
- [ ] Semua halaman bisa dibuka: beranda, cari, museum, tanya, metode, peta
- [ ] 10 pertanyaan uji dijawab benar di `/tanya`
- [ ] Demo `python scripts/demo.py` jalan tanpa traceback
- [ ] README menyebut batasan yang diketahui
- [ ] Tangkapan layar JSON-LD dari Rich Results Test terlampir
- [ ] Setiap orang bisa menjelaskan bagian orang lain secara singkat
