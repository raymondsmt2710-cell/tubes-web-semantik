# Museum Sumatera — Desain (Pameran Digital Berbasis SPARQL)

Tanggal: 2026-02-16
Status: **disetujui** (arahan visual A dipilih di companion; poros cerita geografis+tema disetujui; Fuseki sudah tersedia di mesin pengguna; data museum opsi A = dirancang lalu diverifikasi pengguna)

## 1. Maksud dan alasan

Membangun situs web bertema **museum di Pulau Sumatera** dengan tujuan yang sama seperti proyek SudutPuncak (pencarian data di atas **RDF + SPARQL + Apache Jena Fuseki**), tetapi dengan **konsep/jalan cerita**: pengunjung tidak langsung disuguhi kotak pencarian, melainkan dituntun melewati sebuah **alur perjalanan** dari Aceh ke Lampung — setiap provinsi menjadi satu bab pameran.

Situs ini adalah *pameran digital yang menyamar sebagai mesin pencari*: narasi sebagai pintu masuk, katalog + pencarian sebagai mesin di ujungnya.

## 2. Siapa yang dilayani

- **Pengunjung** yang ingin mengenal museum-museum Sumatera secara runtut, bukan daftar.
- **Mahasiswa/dosen** yang menilai proyek ini sebagai tugas Web Semantik: ontologi nyata, SPARQL nyata, data ternormalisasi.
- **Pengguna yang punya tujuan spesifik** ("museum di Sumatera Barat yang temanya perjuangan") — dilayani katalog + filter.

## 3. Tujuan (goals)

1. Alur cerita berbab yang bisa ditelusuri awal→akhir, dengan navigasi bab yang selalu terlihat.
2. Setiap museum punya halaman entri bergaya katalog: judul, metadata (provinsi/kota/berdiri/tema), narasi, dan **"benang merah"** — relasi ke museum lain yang dihasilkan dari graf, bukan ditulis manual.
3. Katalog lengkap + pencarian teks dan filter (provinsi, tema, era/tahun) yang **dieksekusi di SPARQL**, bukan difilter di JavaScript.
4. Ontologi RDF/XML yang bersih dan ternormalisasi, dapat di-upload ke Fuseki sebagai satu dataset.
5. Berjalan dengan `bun dev` setelah `.env` diarahkan ke Fuseki pengguna; README memuat langkah setup lengkap.

## 4. Bukan tujuan (non-goals)

- Bukan situs resmi museum: tidak ada tiket, jam buka real-time, atau integrasi booking.
- Tidak ada autentikasi, admin panel, atau database tulis.
- Tidak ada scraping situs pihak ketiga (opsi C ditolak).
- Tidak ada dukungan multi-bahasa (hanya Bahasa Indonesia).
- Tidak ada peta interaktif berat (Leaflet/Mapbox); cukup peta tautan keluar.

## 5. Anti-goals (akan dianggap gagal walau teknis berjalan)

- Terasa seperti "SudutPuncak versi ganti objek": grid kartu tanpa alur dan tanpa narasi.
- Ranking pencarian yang dikerjakan di memori atas seluruh dataset (masalah skalabilitas proyek lama).
- Satu properti dengan dua arti berbeda (bug `statusLevel` proyek lama).
- Data museum yang tidak bisa diverifikasi pengguna dan tidak ada disclaimer.

## 6. Batasan (constraints)

- **Stack:** Next.js (App Router) + React + TypeScript + Tailwind CSS + Zustand (persist). Manajer paket **bun**.
- **Data:** RDF/XML → Apache Jena Fuseki. Endpoint dikonfigurasi lewat `.env`: `FUSEKI_ENDPOINT` (query) dan `FUSEKI_UPDATE` (opsional, untuk skrip upload).
- **Volume data:** 24–30 museum, minimal 8 provinsi di Pulau Sumatera (Aceh, Sumut, Sumbar, Riau, Kepri, Jambi, Bengkulu, Sumsel, Babel, Lampung).
- **Bahasa UI:** Bahasa Indonesia; label RDF `xml:lang="id"`.
- **Aksesibilitas:** kontras teks ≥ 4.5:1 pada kertas terang; navigasi keyboard untuk pencarian dan bab.
- **Tanpa `next/image` untuk gambar eksternal museum** (hotlink ke sumber) — gunakan `<img>` dengan fallback; gambar lokal untuk ilustrasi/tekstur.

## 7. Pendekatan yang dipertimbangkan

**A. Cerita sebagai pintu masuk, pencarian sebagai mesin.** Halaman judul naratif → bab per provinsi → entri museum → katalog + pencarian di ujung alur. Relasi RDF (provinsi/tema/era) menenun bab dan "benang merah". **Dipilih.**

**B. Pencarian di depan, cerita sebagai penuntun di hasil.** Fungsional, tetapi "cerita"-nya tipis dan menghasilkan situs yang secara struktur sama dengan proyek lama. Ditolak.

**C. Situs statis (bab ditulis manual di markdown) + pencarian terpisah.** Ceritanya kuat tetapi SPARQL jadi tempelan, dan relasi graf tidak dipakai untuk menarasikan apa pun. Ditolak karena melemahkan inti tugas Web Semantik.

**Arah visual:** **Arsip Kolonial** — kertas tua, tipografi serif, label katalog, aksen teal dipakai tipis untuk elemen interaktif. Dipilih pengguna di companion (opsi A).

## 8. Struktur cerita

Poros utama **geografis** (perjalanan barat → timur), lapisan kedua **tema**:

| Bab | Provinsi | Judul kerja |
|---|---|---|
| I | Aceh | Dari Pelabuhan ke Pedalaman |
| II | Sumatera Utara | Tanah Karo dan Danau Toba |
| III | Riau & Kepulauan Riau | Jejak Kerajaan Melayu |
| IV | Sumatera Barat | Rumah Gadang dan Perang Padri |
| V | Jambi & Bengkulu | Antara Batanghari dan Bukit Barisan |
| VI | Sumatera Selatan & Bangka Belitung | Sungai Musi dan Timah |
| VII | Lampung | Gerbang Selat Sunda |

Tema museum (dipakai sebagai filter dan untuk "benang merah"): `perjuangan`, `arkeologi`, `etnografi`, `seni-budaya`, `sains-teknologi`, `sejarah-alam`.

## 9. Model data (ontologi)

Namespace: `sdp:` = `https://museumsumatera.id/ontology#` (nama prefix dipertahankan `sdp` agar familiar; URI memakai domain proyek baru), `res:` = `https://museumsumatera.id/resource/`.

**Kelas:** `Museum`, `Province` (Provinsi), `City` (Kota/Kabupaten), `Theme` (Tema), `Era` (Era/Periode), `Chapter` (Bab), `Collection` (Koleksi unggulan, opsional per museum).

**Instance `Chapter`:** bab **selalu di-assert** ke setiap museum lewat `museum:chapter` (tidak dihitung dari provinsi), karena bab III/V/VI menggabungkan dua provinsi dan urutan alur tidak bisa diturunkan dari data provinsi. Setiap instance `Chapter` membawa `chapterIndex` (xsd:integer, 1–7), `rdfs:label`, dan `chapterTitle`. Sumber kebenaran pemetaan museum→bab adalah `data/museums.json`; `api/chapters` menghitung jumlah museum per bab dengan `COUNT` di SPARQL.

**Object property:**
- `museum:locatedInProvince` → `Province`
- `museum:locatedInCity` → `City`
- `city:partOfProvince` → `Province`
- `museum:hasTheme` → `Theme` (multi-nilai, minimal 1)
- `museum:hasEra` → `Era`
- `museum:hasCollection` → `Collection`
- `museum:chapter` → `Chapter` (instance bab, dipakai untuk urutan alur)

**Datatype property:** `museum:name` (via `rdfs:label`), `museum:establishedYear` (xsd:gYear), `museum:description` (xsd:string, `xml:lang="id"`), `museum:imageUrl` (xsd:anyURI), `museum:officialUrl` (xsd:anyURI), `museum:address` (xsd:string), `museum:latitude`/`museum:longitude` (xsd:decimal), `museum:admissionNote` (xsd:string), `museum:verificationStatus` (`terverifikasi`/`perlu-verifikasi`), `chapter:chapterIndex` (xsd:integer).

Aturan semantik yang mengikat (memperbaiki bug proyek lama):
- **Satu properti = satu arti.** Tidak ada `statusLevel` ganda. Tingkat kesulitan/kondisi tidak dimodelkan sama sekali.
- **Provinsi dan Kota adalah resource**, bukan string berulang.
- **`establishedYear`** bertipe `xsd:gYear` dan boleh kosong (`OPTIONAL` di query, `null` di DTO).
- Setiap museum **wajib** punya `locatedInProvince`, `hasTheme`, dan `chapter`; sisanya opsional.

## 10. Arsitektur aplikasi

```
src/
  app/
    page.tsx                    → sampul (cover) + daftar bab + pencarian ringkas
    jelajah/[chapter]/page.tsx  → satu bab: narasi + entri museum bab itu
    museum/[slug]/page.tsx      → entri museum + "benang merah" + tautan
    katalog/page.tsx            → katalog lengkap + filter (provinsi/tema/era/tahun) + urut
    api/search/route.ts         → pencarian (q, province, theme, era, minYear, sort)
    api/museum/route.ts         → satu museum by slug + related (sql-free, SPARQL)
    api/chapters/route.ts       → daftar bab + jumlah museum per bab
  components/                   → MuseumEntry, ChapterNav, CatalogFilters, ThreadOfRelation, SearchBox, Footer
  lib/                          → sparql.ts (client), types.ts, ranking.ts, format.ts
  store/                        → recentVisited.ts, catalogPrefs.ts (Zustand persist)
data/
  museums.json                  → sumber kebenaran data (dikelola tangan, 24–30 entri)
ontology/
  museum-sumatera.ttl | .rdf    → ontologi (kelas + properti + label)
scripts/
  generate-rdf.ts               → museums.json → data/museum-sumatera.rdf
  upload-fuseki.ts              → (opsional) PUT ke FUSEKI_UPDATE
docs/superpowers/…              → spec & plan
```

**Alur permintaan:** Klien → route handler Next (`app/api/*`) → `lib/sparql.ts` POST ke Fuseki (`application/sparql-results+json`) → DTO → React Server Component / klien.

**Batas tegas "di SPARQL" vs "di JS"** (mengikat, agar tidak disalahartikan saat penilaian):

- **Semua penyaringan dan pengurutan dieksekusi sebagai `FILTER`/`ORDER BY` di SPARQL**: provinsi, tema, era, `minYear`, urutan nama/tahun. Tidak ada satu pun filter yang diterapkan di JavaScript.
- **Teknik pencocokan string (fuzzy/akronim) dieksekusi di JS**, tetapi **hanya atas himpunan yang sudah dibatasi SPARQL** (`LIMIT 300`). Ini bukan pelanggaran: SPARQL menyaring, JS hanya memeringkat kandidat terbatas, dan plafon 300 baris memastikan biaya tidak tumbuh dengan ukuran dataset.
- Bila `q` kosong, route langsung mengembalikan hasil `ORDER BY` dari SPARQL tanpa menyentuh ranking.

**Aturan "benang merah"** (`lib/related.ts`, dibatasi `LIMIT 6` di SPARQL, lalu diberi skor):
- Bobot: **tema sama = +3 per tema**, **kota sama = +2**, **era sama = +1**, **bab bersebelahan (±1) = +1**. Boneka museum tidak boleh merekomendasikan dirinya sendiri (`FILTER(?museum != <self>)`).
- Urutkan skor menurun; bila seri, urutkan `rdfs:label` agar hasil deterministik (bisa diuji).
- Museum dengan skor 0 tidak ditampilkan. Nol museum dengan skor > 0 berarti halaman entri menyembunyikan bagian "benang merah" (bukan menampilkan bagian kosong).

**Ranking pencarian** (di `lib/ranking.ts`, murni fungsi yang bisa diuji): normalisasi → exact 1.0 → prefix 0.95 → akronim 0.85 → subsequence `0.7×rasio` → substring 0.6 → fallback rasio karakter. Ambang "hasil utama" ≥ 0.7. (Diwarisi dari proyek lama karena terbukti, tetapi kini hanya dijalankan atas himpunan terfilter.)

## 11. Yang diputuskan pengguna

- Arah visual **Arsip Kolonial**.
- Poros cerita **geografis + tema**.
- Fuseki **sudah tersedia** (dikonfigurasi lewat `.env`).
- Data museum: **opsi A** — dirancang oleh saya, lalu **diverifikasi/dikoreksi pengguna**. Semua entri diberi `verificationStatus` dan UI menampilkan disclaimer di footer + lencana pada entri yang belum terverifikasi.
- **Model data museum:** 28 museum, seluruhnya ditandai `perlu-verifikasi` pada pengiriman pertama. Pengguna mengoreksi `data/museums.json` dan menaikkan status per entri ke `terverifikasi`. Situs tetap harus tampil utuh walau semua entri belum terverifikasi.
- **Fuseki:** instance sudah berjalan di mesin pengguna. Nama dataset **belum dipastikan**; karena itu `.env.example` memuat dua variabel dengan contoh yang harus disesuaikan, dan README menulis **jalur upload sebagai alur utama** (bukan opsional), supaya proyek bisa dijalankan dari nol di mesin lain maupun di mesin pengguna.
- **Versi Next: 16 (App Router)**, sama dengan proyek pembanding; `react` 19 dan fungsi App Router versi terkini dipakai. Pengguna memakai **bun**.
- **Artefak RDF:** sumber ontologi `ontology/museum-sumatera.ttl` (dibaca & dipelihara), sedangkan **artefak upload ke Fuseki adalah RDF/XML** `data/museum-sumatera.rdf` hasil generator. Keduanya di-commit.

## 12. Yang diserahkan ke pembangun (builder's discretion)

- Nama file komponen persis, pembagian sub-komponen, dan pemakaian Server vs Client Component selama aturan Next App Router dipatuhi.
- Pilihan pustaka kecil (mis. `zod` untuk validasi JSON) bila tidak menambah berat berarti.
- Detail tipografi web (pasangan serif), lebar kolom baca, dan tekstur kertas CSS.
- Strategi cache: `revalidate` pada fetch Fuseki (disarankan 60 detik) atau `unstable_cache`.
- Struktur test: Vitest untuk unit (`sparql`, `ranking`, `related`, `validate`, `generate-rdf`) + smoke test route handler dengan Fuseki di-mock (tanpa React Testing Library; UI diverifikasi manual di browser).
- Daftar provinsi resmi yang dipakai validasi & filter (mengunci "minimal 8 provinsi"): `Aceh`, `Sumatera Utara`, `Sumatera Barat`, `Riau`, `Kepulauan Riau`, `Jambi`, `Bengkulu`, `Sumatera Selatan`, `Bangka Belitung`, `Lampung`. Kotak koordinat Sumatera: lat `-6.5..6.5`, lon `94..107.5`.
- Himpunan era tertutup: `pra-kolonial`, `kolonial`, `kemerdekaan`, `modern`. Himpunan tema tertutup: `perjuangan`, `arkeologi`, `etnografi`, `seni-budaya`, `sains-teknologi`, `sejarah-alam`.

## 13. Kriteria selesai yang bisa diperiksa

1. `bun dev` menampilkan sampul; tujuh bab dapat dinavigasi berurutan dan tiap bab menampilkan museum yang benar.
2. Halaman museum menampilkan metadata, narasi, dan minimal satu "benang merah" yang benar-benar berasal dari relasi graf.
3. Pencarian + filter mengembalikan hasil yang sama dengan isi `museums.json` (dibuktikan lewat test pada fungsi ranking dan satu test integrasi dengan Fuseki di-mock).
4. `bun run generate:rdf` menghasilkan RDF valid yang lolos parser, dan `bun run check:rdf` memverifikasi setiap museum punya provinsi, tema, dan bab.
5. `.env.example` + README memungkinkan orang lain menyiapkan Fuseki dari nol dan menjalankan situs.
6. Tidak ada properti bermakna ganda, tidak ada filter yang dijalankan di JS atas seluruh dataset.
