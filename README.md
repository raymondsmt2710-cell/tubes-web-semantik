# Museum Sumatera — Pameran Digital

Situs pameran digital tentang museum di Pulau Sumatera. Alih-alih katalog datar,
28 museum disusun sebagai tujuh bab perjalanan dari Aceh ke Lampung, lalu
dihubungkan kembali lewat tema, kota, era, dan kedekatan bab. Seluruh data
disimpan sebagai RDF di Apache Jena Fuseki dan dibaca lewat SPARQL.

## Prasyarat

- Node.js 20 atau lebih baru dan npm (proyek ini memakai **npm**, bukan bun).
- Apache Jena Fuseki yang berjalan lokal. Langkah lengkapnya ada di
  [`docs/fuseki-setup.md`](docs/fuseki-setup.md).

## Menjalankan dari nol

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

**Gambar.** Foto diambil hanya dari Wikimedia Commons yang lisensinya jelas
(CC0, CC BY, CC BY-SA, atau domain publik). Setiap foto disimpan lengkap dengan
pencipta, nama lisensi, tautan lisensi, dan tautan halaman asalnya. Foto
diunduh ke `public/images/museums/<slug>/` supaya situs tidak bergantung pada
hotlink, dan kreditnya ditampilkan di bawah setiap gambar. Foto interior dari
situs resmi museum tidak dipakai karena hak ciptanya tidak jelas.

**Pemeriksaan data.** `npm run check:rdf` menolak foto tanpa `src`,
`license`, atau `sourceUrl`, serta menolak sumber yang bukan URL `http(s)`.
Generator RDF juga berhenti dengan pesan yang menyebut museum dan nomor foto
bila aturan itu dilanggar.

**Status data.** Semua museum tetap berstatus `perlu-verifikasi`. Catatan
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

Seluruh entri saat ini berstatus **perlu-verifikasi**. Nama, alamat, tahun
berdiri, dan catatan kunjungan disusun untuk keperluan pembelajaran dan belum
diperiksa ulang terhadap sumber resmi. Lencana pada setiap halaman museum
menunjukkan status ini secara terbuka. Jangan memakai data di situs ini sebagai
rujukan perjalanan tanpa memeriksanya kembali.

## Test

```bash
npm test
```

Test mencakup generator RDF, validasi data, pembentukan kueri SPARQL, escaping,
pemeringkatan teks, relasi benang merah, route handler, dan serialisasi filter
katalog. Halaman UI diverifikasi lewat `npm run build` dan penelusuran manual.
