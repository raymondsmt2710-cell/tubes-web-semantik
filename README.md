_Repositori: `tubes-web-semantik` — Tugas Proyek Web Semantik._

# Museum Sumatera — Pameran Digital

Situs pameran digital tentang museum di Pulau Sumatera. Alih-alih katalog datar,
28 museum disusun sebagai tujuh bab perjalanan dari Aceh ke Lampung, lalu
dihubungkan kembali lewat tema, kota, era, dan kedekatan bab. Seluruh data
disimpan sebagai RDF di Apache Jena Fuseki dan dibaca lewat SPARQL.

## Dua aplikasi, satu data

Repositori ini berisi **dua** aplikasi yang membaca data yang sama
(`data/museums.json`):

| | Aplikasi Python (`pyapp/`) — **utama** | Aplikasi TypeScript (`src/`) |
|---|---|---|
| Teknologi | FastAPI, rdflib, owlrl, Jinja2 | Next.js, Fuseki |
| Triple store | Turtle dibaca langsung, closure OWL-RL di memori | Apache Jena Fuseki (wajib) |
| Halaman | beranda, cari, museum, **peta**, tanya, metode, API JSON / JSON-LD | katalog, jelajah bab, tanya |
| Test | `cd pyapp && pytest` | `npx vitest run` |

Jalankan aplikasi Python dengan satu perintah (butuh Docker):

```bash
docker compose up --build      # lalu buka http://localhost:8000
```

Tanpa Docker: lihat [`pyapp/README.md`](pyapp/README.md). Panduan deploy ke
Railway / VPS: [`docs/deploy.md`](docs/deploy.md).

### Keputusan desain

- **Mengapa Python.** Materi kuliah (P6–P13) mengajarkan `rdflib` untuk RDF dan
  SPARQL serta `owlrl` untuk penalaran OWL-RL. Aplikasi pertama ditulis dalam
  TypeScript; aplikasi Python dibuat agar setiap konsep kuliah punya wujud
  langsung di kode yang sama dengan materi, dan agar penalaran bisa dijalankan
  di proses aplikasi tanpa server tambahan.
- **Mengapa datanya sama.** `data/museums.json` tetap satu-satunya sumber
  kebenaran. Kedua aplikasi membangkitkan RDF dari berkas itu, sehingga
  perbedaan hasil antara keduanya pasti berasal dari kode, bukan data. Data yang
  sudah dikurasi (lisensi foto, sumber) juga tidak perlu dikerjakan dua kali.
- **Mengapa Fuseki opsional di Python.** Untuk 28 museum (±6.700 triple
  setelah penalaran) graf muat di memori. Query tetap ditulis sebagai SPARQL
  standar dengan `PREFIX` lengkap, jadi bisa dipindah ke Fuseki tanpa berubah.
- **JSON-LD schema.org (P3).** Setiap halaman museum menyisipkan
  `<script type="application/ld+json">` berkosakata `schema.org`
  (`Museum`, `PostalAddress`, `GeoCoordinates`), dan tersedia di
  `/api/museum/{slug}.jsonld` serta `/api/museum.jsonld` (seluruh museum).
  Bidang yang tidak ada di graf dihilangkan, bukan diisi `null`.

### Batasan yang diketahui

Ditulis supaya penilaian jujur. Status per 27 November 2026.

- **4 dari 28 museum belum terverifikasi**: Museum Sisingamangaraja XII,
  Museum Siginjai, Rumah Pengasingan Bung Karno, dan Taman Purbakala Pugung
  Raharjo. Museum Sisingamangaraja XII juga baru punya satu sumber acuan.
  Rincian pemeriksaan ada di
  [`docs/superpowers/reports/2026-11-26-verifikasi-data-museum.md`](docs/superpowers/reports/2026-11-26-verifikasi-data-museum.md).
- **Jam buka dan harga tiket belum ada di data.** Karena itu JSON-LD tidak
  memuat `openingHours`; bidang itu akan muncul otomatis bila
  `sdp:openingHours` diisi.
- **NL2SPARQL bawaan masih berbasis aturan.** Adapter LLM (`pyapp/semweb/llm.py`)
  sudah ada dan bisa dibandingkan lewat `scripts/bandingkan_llm.py`, tetapi
  butuh `LLM_API_KEY`; tanpa kunci, aplikasi memakai penerjemah aturan.
  Pertanyaan di luar pola yang dikenali ditolak, bukan ditebak.
- **Image Docker tidak membawa `.env`.** Bila ingin memakai LLM di kontainer,
  isi `LLM_PROVIDER` dan `LLM_API_KEY` sebagai variabel lingkungan platform.
- **Peta bergantung pada CDN** (unpkg untuk Leaflet, OpenStreetMap untuk
  ubin peta). Bila jaringan memblokirnya, halaman `/peta` tetap menampilkan
  daftar museum lengkap dengan koordinat, tanpa peta.
- **Aksesibilitas** diperiksa dengan axe-core (0 pelanggaran pada 6 halaman
  utama) dan test otomatis (`pyapp/tests/test_aksesibilitas.py`), tetapi belum
  diuji langsung dengan pembaca layar (NVDA/VoiceOver).
- **Closure dihitung saat permintaan pertama** setelah server menyala, sehingga
  permintaan pertama butuh beberapa detik.

## Aplikasi TypeScript

### Prasyarat

- Node.js 20 atau lebih baru dan npm (proyek ini memakai **npm**, bukan bun).
- Apache Jena Fuseki yang berjalan lokal. Langkah lengkapnya ada di
  [`docs/fuseki-setup.md`](docs/fuseki-setup.md).

### Menjalankan dari nol

```bash
# 1. Pasang dependensi
npm install

# 2. Siapkan konfigurasi
cp .env.example .env
#    Isi FUSEKI_ENDPOINT (default: http://localhost:3030/museum/query)
#    Isi FUSEKI_UPDATE hanya bila ingin memakai skrip unggah otomatis.

# 3. Buat berkas RDF dari data sumber
npm run generate:rdf

# 4. Periksa kualitas data (error = gagal, warning = boleh lanjut)
npm run check:rdf

# 5. Unggah ke Fuseki
npm run upload:fuseki
#    Atau unggah manual data/museum-sumatera.rdf lewat UI Fuseki
#    (Add data → Upload file).

# 6. Jalankan situs
npm run dev
```

Buka `http://localhost:3000`. Bila Fuseki belum siap, halaman tetap terbuka
dengan catatan bahwa basis data sedang tidak dapat dihubungi — situs tidak
memblokir narasi bab.

## Skrip

| Perintah | Kegunaan |
|---|---|
| `npm run dev` | Server pengembangan Next.js |
| `npm run build` | Build produksi (sekaligus pemeriksaan TypeScript) |
| `npm run start` | Menjalankan hasil build |
| `npm test` | Menjalankan seluruh test Vitest |
| `npm run generate:rdf` | `data/museums.json` → `data/museum-sumatera.rdf` |
| `npm run check:rdf` | Validasi data; keluar dengan kode 1 bila ada error |
| `npm run upload:fuseki` | Bersihkan graph default lalu unggah RDF ke Fuseki |

## Struktur folder

```
data/
  museums.json            sumber kebenaran data museum (termasuk sejarah,
                          isi pameran, galeri, dan sumber acuan)
  museum-sumatera.rdf     hasil generate, berkas yang diunggah ke Fuseki
ontology/
  museum-sumatera.ttl     ontologi (nama kelas dan properti)
public/
  images/museums/<slug>/  foto museum yang sudah diunduh lokal
scripts/
  generate-rdf.ts         generator RDF/XML
  check-rdf.ts            pemeriksa data
  upload-fuseki.ts        pengunggah ke Fuseki
src/
  app/                    halaman dan route handler Next.js
    api/search/           katalog + pencarian teks
    api/museum/           satu museum + benang merah
    api/chapters/         jumlah museum per bab
    jelajah/[chapter]/    halaman bab
    museum/[slug]/        halaman entri museum
    katalog/              katalog dengan penyaringan
    tentang/              metode dan status data
  components/             komponen UI
  lib/                    tipe, kueri SPARQL, pemeringkatan, relasi
  store/                  preferensi katalog (Zustand persist)
```

## Ontologi singkat

Namespace aplikasi: `sdp:` = `https://museumsumatera.id/ontology#`,
`res:` = `https://museumsumatera.id/resource/`.

- Kelas dasar: `sdp:Museum`, `sdp:Province`, `sdp:City`, `sdp:Theme`, `sdp:Era`,
  `sdp:Chapter`, `sdp:Collection`, `sdp:Exhibit`, `sdp:Image`, `sdp:Source`.
- **Subkelas museum:** `sdp:StateMuseum`, `sdp:SiteMuseum`, `sdp:PrivateMuseum`
  (semua `rdfs:subClassOf sdp:Museum`). Sebuah museum boleh punya lebih dari satu
  tipe; `StateMuseum` dan `PrivateMuseum` dibuat `owl:disjointWith`.
- **Entitas pendukung:** `sdp:Person` (dengan subkelas `Founder`, `Curator`),
  `sdp:Facility`, `sdp:HeritageStatus`.
- Object property: `locatedInProvince`, `locatedInCity`, `partOfProvince`,
  `hasTheme`, `hasEra`, `chapter`, `hasCollection`, `hasExhibit`, `hasImage`,
  `hasSource`, `hasFacility`, `hasFounder`, `hasCurator`, `namedAfter`,
  `relatedMuseum` (simetris), `heritageStatusOf`.
- **Aksioma OWL:** pasangan `owl:inverseOf` (mis. `hasImage ↔ imageOfMuseum`),
  properti fungsional (`chapter`, `locatedInCity`, `heritageStatusOf`), dan
  `owl:Restriction` cardinality pada `Museum` (tepat 1 provinsi & bab, minimal 1
  tema, maksimal 1 kota). Properti yang memiliki inverse **tidak** menyimpan
  `rdfs:domain`/`rdfs:range` eksplisit agar graf konsisten di bawah OWL 2 RL.
- Datatype property: `establishedYear` (`xsd:gYear`), `description`, `imageUrl`,
  `officialUrl`, `address`, `latitude`, `longitude`, `admissionNote`,
  `verificationStatus`, `chapterIndex`, `chapterTitle`, `collectionSize`
  (`xsd:integer`), `governingBody`, `openingHours`, `collectionCategory`,
  `facilityName`, `personName`.
- **Isi pameran dan foto:** `exhibitIndex` (`xsd:integer`), `exhibitTitle`,
  `exhibitDescription`, `exhibitPeriod`, `exhibitOrigin`, `exhibitMaterial`,
  `exhibitHighlight` (`xsd:boolean`), `imageIndex` (`xsd:integer`), `imageTitle`,
  `imageBackground`, `imagePeriod`, `imageDetail` (→ `sdp:ImageDetail`), `detailIndex`
  (`xsd:integer`), `detailText`, `imageAlt`, `imageCaption`,
  `imageCredit`, `imageLicense`, `imageLicenseUrl` (`xsd:anyURI`), `imageSource`
  (`xsd:anyURI`), `sourceIndex`, `sourceLabel`, `sourceUrl`.

Setiap museum menunjuk langsung ke babnya (`sdp:chapter`). Keanggotaan bab
sengaja tidak diturunkan dari provinsi supaya alur cerita bisa tetap utuh bila
pembagian provinsi berubah.

**Memvalidasi ontologi.** Buka `ontology/museum-sumatera.ttl` di Protégé dan
jalankan HermiT (tidak boleh ada kelas merah = inconsistent). Bila `robot`
tersedia: `robot reason --input ontology/museum-sumatera.ttl --reasoner hermit`.

**Klasifikasi koleksi & fasilitas.** `Collection` dan `Facility` hanya ditulis
bila sumber museum menyebutnya secara eksplisit — bukan dikarang dari tema. Karena
itu sebagian museum memang tidak punya kategori koleksi atau daftar fasilitas, dan
halaman menyesuaikan diri tanpa menyisakan bagian kosong.

## Cara kerja pencarian

- Penyaringan provinsi, tema, era, dan tahun minimum dijalankan **di dalam
  SPARQL**, bukan dengan menyaring array di browser.
- Kandidat dibatasi `LIMIT 300` sebelum masuk ke pemeringkatan teks di
  JavaScript. Pemeringkatan hanya menyusun ulang nama yang sudah lolos
  penyaringan; ia tidak menambah atau menghapus museum.
- Kata kunci `q` juga disaring **di dalam SPARQL** dan mencocokkan nama museum,
  kota, provinsi, tema, era, serta deskripsi. Setiap kata pada `q` harus muncul
  di salah satu bidang tersebut, jadi "museum aceh" dan "medan" sama-sama bisa
  ditemukan tanpa mengetik nama lengkap.
- Hasil dibagi menjadi "hasil utama" dan "hasil lainnya" berdasarkan skor
  kemiripan nama; kecocokan di kota/tema/deskripsi (skor 0.75) ikut diangkat
  sebagai hasil utama tetapi tidak mengalahkan nama yang benar-benar mirip.
  Bila kata kunci kosong, seluruh katalog ditampilkan tanpa peringkat.

## Catatan museum: sejarah, pameran, dan galeri

Selain data dasar, setiap museum punya isi naratif yang disimpan di
`data/museums.json` dan ikut masuk ke graf:

| Bagian | Properti RDF | Tampil di |
|---|---|---|
| Sejarah (paragraf) | `sdp:history` | bagian **Sejarah** |
| Isi pameran | `sdp:hasExhibit` → `sdp:Exhibit` | bagian **Isi pameran** |
| Galeri foto | `sdp:hasImage` → `sdp:Image` | bagian **Galeri** |
| Sumber acuan | `sdp:hasSource` → `sdp:Source` | bagian **Sumber catatan** |

**Kedalaman isi pameran.** Setiap entri `sdp:Exhibit` membawa metadata di luar
prosa, sehingga informasinya ikut masuk graf dan bukan hanya tampil sebagai teks:

| Properti | Arti |
|---|---|
| `sdp:exhibitPeriod` | masa atau tarikh benda, mis. "abad ke-15" |
| `sdp:exhibitOrigin` | asal perolehan atau daerah benda |
| `sdp:exhibitMaterial` | bahan utama, mis. "perunggu" |
| `sdp:exhibitHighlight` (`xsd:boolean`) | penanda benda andalan |

**Kedalaman galeri.** Setiap `sdp:Image` punya `sdp:imagePeriod` (masa yang tampak
pada foto) dan menautkan poin pengamatan lewat `sdp:imageDetail` ke node
`sdp:ImageDetail`. Setiap node poin menyimpan `sdp:detailIndex` (urutan) dan
`sdp:detailText` (teks). Bentuk ini dipilih supaya urutan poin terjamin — bila
indeks disimpan sebagai properti terpisah pada foto, kueri SPARQL akan
menghasilkan perkalian silang dan urutan poin menjadi acak.

**Arti `period`.** `exhibitPeriod` dan `imagePeriod` hanya boleh berisi tarikh atau
masa ("1915", "abad ke-15", "era 1970-an", "masa kolonial"). Topik atau subjek foto
tempatnya di `title`/`caption`, bukan di `period` — `npm run check:rdf` memberi
peringatan bila `period` tidak memuat penanda tarikh.


**Gambar.** Foto diambil hanya dari Wikimedia Commons yang lisensinya jelas
(CC0, CC BY, CC BY-SA, atau domain publik). Setiap foto disimpan lengkap dengan
pencipta, nama lisensi, tautan lisensi, dan tautan halaman asalnya. Foto
diunduh ke `public/images/museums/<slug>/` supaya situs tidak bergantung pada
hotlink, dan kreditnya ditampilkan di bawah setiap gambar. Foto interior dari
situs resmi museum tidak dipakai karena hak ciptanya tidak jelas.

**Pemeriksaan data.** `npm run check:rdf` menolak foto tanpa `src`,
`license`, atau `sourceUrl`, serta menolak sumber yang bukan URL `http(s)`.
Pemeriksa juga menjaga kedalaman isi: deskripsi isi pameran minimal **180
karakter**, latar belakang foto minimal **220 karakter**, setiap foto wajib punya
`detail`, dan setiap pameran wajib punya judul. Pelanggaran aturan ini muncul
sebagai peringatan (bukan error) supaya data lama tidak memblokir build, tetapi
kondisi sehat adalah nol peringatan kedalaman. Generator RDF juga berhenti dengan
pesan yang menyebut museum dan nomor foto bila aturan lisensi dilanggar.

**Status data.** 24 museum berstatus `terverifikasi` dan 4 masih
`perlu-verifikasi` (lihat *Batasan yang diketahui*). Catatan
sejarah disusun ulang dari sumber yang tercantum di setiap halaman, bukan
salinan langsung, dan pengguna diarahkan memeriksa kanal resmi museum untuk jam
buka serta harga tiket.

## Benang merah

Pada halaman museum, museum lain dipilih dari graf dengan bobot:

| Relasi | Bobot |
|---|---|
| Tema yang sama | +3 per tema |
| Relasi arsip eksplisit (`relatedMuseum`) | +4 |
| Kota yang sama | +2 |
| Era yang sama | +1 |
| Bab bersebelahan | +1 |

Kandidat berskor nol disembunyikan, urutan seri dipecah berdasarkan nama, dan
maksimum enam rekomendasi ditampilkan. Alasan setiap rekomendasi ditulis apa
adanya dari relasi yang cocok.

## Endpoint API

| Endpoint | Keterangan |
|---|---|
| `GET /api/search` | Katalog. Parameter: `q`, `province`, `theme`, `era`, `minYear`, `sort` (`name`/`year`), `order` (`asc`/`desc`). |
| `GET /api/museum?slug=…` | Satu museum dan daftar benang merah. 400 tanpa slug, 404 bila tidak ada. |
| `GET /api/chapters` | Tujuh bab beserta jumlah museumnya. |

Kegagalan menghubungi Fuseki dibalas `502` dengan pesan Bahasa Indonesia.

## Memperbarui data

1. Ubah `data/museums.json`.
2. `npm run check:rdf` — perbaiki semua error sebelum lanjut.
3. `npm run generate:rdf`.
4. `npm run upload:fuseki` (atau unggah ulang berkas RDF secara manual).
5. Muat ulang situs.

## Catatan verifikasi

24 dari 28 entri berstatus **terverifikasi**: nama, kota, provinsi, dan tahun
berdiri sudah dicocokkan ke sumber resmi. Empat entri lain masih
**perlu-verifikasi**. Lencana pada setiap halaman museum menunjukkan status ini
secara terbuka, dan jam buka serta harga tiket belum diperiksa. Jangan memakai data di situs ini sebagai
rujukan perjalanan tanpa memeriksanya kembali.

## Test

```bash
npm test
```

Test mencakup generator RDF, validasi data, pembentukan kueri SPARQL, escaping,
pemeringkatan teks, relasi benang merah, route handler, dan serialisasi filter
katalog. Halaman UI diverifikasi lewat `npm run build` dan penelusuran manual.
