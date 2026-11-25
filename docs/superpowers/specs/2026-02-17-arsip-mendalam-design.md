# Museum Sumatera — Desain Pengembangan: Ontologi Mendalam + Frontend Arsip Digital Museum

Tanggal: 2026-02-17
Status: **siap disetujui** (memperluas desain awal `2026-02-16-museum-sumatera-design.md`; sudah
melewati builder-check independen)
Keputusan pengguna: ontologi opsi **C** (skema + data), arah visual **2C** (arsip digital museum),
identitas **tetap Arsip Kolonial**, penalaran **A1** (OWL 2 wajar), entitas **B2** (perkaya + entitas
pendukung), akurasi **C1** (isi yang dapat dipertanggungjawabkan; C2 hanya bila buntu).

Keputusan lanjutan (menutup temuan builder-check):

- **P1/P2 → taksonomi:** pemetaan 28 museum ke subkelas diturunkan dari `history` (yang menyebut
  badan pengelola di hampir semua entri). `SiteMuseum` **boleh beririsan** dengan `StateMuseum`.
  Satu museum **boleh** punya lebih dari satu `rdf:type` turunan; DTO memakai `type: string[]`.
- **P3 → `Collection`:** hanya diisi bila **sumber menyebut kategori secara eksplisit** (C1).
  Kriteria "setiap museum punya minimal satu `Collection`" **dilonggarkan** menjadi "tidak ada
  `Collection` yang dibuat tanpa dasar sumber".
- **P4 → `relatedMuseum`:** menjadi **bonus bobot +4** pada skor benang merah; tetap tunduk aturan
  lama "skor 0 disembunyikan" (museum tanpa relasi turunan maupun eksplisit tidak tampil).
- **P5 → `Facility`/`HeritageStatus`:** `Facility` hanya diisi bila sumber menyebut
  (banyak museum kosong); `HeritageStatus` **tidak diinstansiasi** (kelas didokumentasikan, dibiarkan
  kosong). `HeritageBadge` **tidak** ditampilkan bila status kosong, dan **tidak** berimpit dengan
  `VerificationBadge`.
- **P6 → kriteria #8:** dibuktikan **secara objektif dengan token**, bukan penilaian visual (§13.10).

## 1. Maksud dan alasan

Dua pekerjaan yang saling menopang, dikerjakan bersama:

1. **Ontologi lebih mendalam.** Graf saat ini dangkal: `Collection` dideklarasikan tetapi tidak
   pernah dipakai, `hasCollection` tidak pernah ditulis, tidak ada `subClassOf`, `owl:inverseOf`,
   `owl:Restriction`, maupun anotasi skema. Tujuannya: graf yang *secara terukur* lebih semantik —
   bisa didemonstrasikan penalarannya dan punya bahan jauh lebih kaya untuk "benang merah".
2. **Frontend lebih baik.** Seluruh situs memakai satu perlakuan datar. Tujuan: tiap jenis halaman
   punya karakter, dan situs terasa seperti **arsip/katalog museum modern** — label objek presisi,
   lembar katalog bergaya specimen card, plate foto berlabel — sambil mempertahankan kertas tua &
   serif Arsip Kolonial yang sudah dipilih dan disetujui.

Misi lama tidak berubah: relasi tetap dari graf, penyaringan tetap di SPARQL, benang merah tetap
dihitung dari relasi, dan situs tetap tampil utuh saat Fuseki mati.

## 2. Siapa yang dilayani

Sama seperti desain awal (pengunjung, mahasiswa/dosen penilai, pengguna bertujuan spesifik),
ditambah satu pembaca baru yang kini relevan: **penilai Web Semantik** yang akan memeriksa
kedalaman ontologi (hierarki, aksioma, inferensi) — bukan hanya bahwa situs berjalan.

## 3. Tujuan (goals)

1. Ontologi punya: hierarki `subClassOf`, `owl:inverseOf`, properti `Functional`/`Transitive`,
   `owl:Restriction` cardinality, anotasi `owl:Ontology` (`owl:versionInfo`, `dcterms:created/modified`).
2. Entitas baru **dipakai nyata**, bukan kelas mati: `Person`, `Collection`, `Facility`,
   `HeritageStatus` terhubung ke museum lewat objek properti.
3. Setiap museum punya data lebih kaya (dari sumber yang tercatat), dan grafnya memberi bahan
   lebih banyak untuk benang merah dan tampilan metadata.
4. Frontend: karakter berbeda per halaman (sampul / bab / museum / katalog), bernuansa
   arsip digital museum, identitas Arsip Kolonial dipertahankan.
5. Tidak merusak: semua test lama tetap lulus; penyaringan tetap di SPARQL; situs tetap tampil
   saat Fuseki mati; kompatibel dengan OWL 2 RL (aman untuk Fuseki) dan bisa dibuka di Protégé.

## 4. Bukan tujuan (non-goals)

- Tidak menambah autentikasi/admin/tulis lewat UI.
- Tidak menambah multi-bahasa.
- Tidak mengganti stack (tetap Next 16 App Router + React 19 + Tailwind v4 + Zustand + Fuseki).
- Tidak memaksa reasoner berjalan *di* Fuseki pada runtime situs (penalaran didemonstrasikan lewat
  berkas ontologi + Protégé/reasoner CLI, bukan menjadi ketergantungan runtime).
- Tidak menulis ulang seluruh data museum dari nol; fokus memperkaya.

## 5. Anti-goals (dianggap gagal walau teknis berjalan)

- Ontologi yang "kaya" di TTL tetapi tidak ada satu instance pun memakainya (seperti `Collection`
  sekarang).
- Aksioma yang membuat reasoner tidak konsisten (mis. disjointness keliru, cardinality bertabrakan
  dengan data) — graf harus tetap *consistent* saat divalidasi.
- Redesign yang hanya mengganti warna/spasi tetapi tidak mengubah hierarki atau karakter halaman.
- Filter baru yang dijalankan di JavaScript atas seluruh dataset.
- Data karangan tanpa sumber yang disamarkan sebagai fakta (aturan C1).

## 6. Batasan (constraints)

- **Sumber kebenaran data:** tetap `data/museums.json`; artefak unggah tetap RDF/XML hasil generator.
- **Ontologi sumber:** `ontology/museum-sumatera.ttl` (dibaca/manusia) **dan** blok skema di
  generator RDF/XML harus konsisten satu sama lain (kelas/properti/aksioma yang sama).
- **OWL 2 RL-compatible** untuk aksioma yang dipakai (aman untuk Fuseki, tetap bisa dibuka Protégé).
- **Aksesibilitas:** kontras teks ≥ 4.5:1; navigasi keyboard; `prefers-reduced-motion` dihormati.
- **Tanpa `next/image` untuk gambar eksternal** (aturan lama tetap).
- **Backward-compatible DTO:** field baru di `MuseumDTO` bersifat opsional (`?:`) agar test lama
  dan pemanggil lama tidak patah.
- **Bahasa:** UI & label `@id`.

## 7. Pendekatan yang dipertimbangkan

### 7a. Ontologi

- **Opsi 1 — Skema saja (tanpa entitas baru).** Menambah aksioma pada kelas/properti yang ada.
  Cepat, tetapi tidak menambah kedalaman *data*; `Collection` tetap mati. Ditolak (tidak memenuhi C).
- **Opsi 2 — Data saja (perkaya field).** Mengisi field baru ke museum tanpa mengubah struktur.
  Menambah isi tetapi graf tetap dangkal secara semantik. Ditolak.
- **Opsi 3 — Skema + data + entitas pendukung (dipilih).** Hierarki + aksioma + kelas baru
  (`Person`, `Collection`, `Facility`, `HeritageStatus`) yang **benar-benar diinstansiasi** dan
  dihubungkan ke museum. Ini satu-satunya opsi yang memenuhi "lebih mendalam" secara graf.

### 7b. Frontend

- **Opsi A — Tambal-tambal (ganti warna/spasi).** Murah, tapi tidak menyentuh masalah inti
  (semua halaman terasa sama). Ditolak.
- **Opsi B — Redesign menyeluruh dengan sistem komponen baru (dipilih).** Sistem tipografi & token
  diperluas dari Arsip Kolonial, komponen "museum plate", "specimen card", "index board" dibuat,
  tiap halaman diberi karakter. Tetap dalam identitas yang disetujui.
- **Opsi C — Ganti identitas visual total.** Ditolak pengguna (harus mempertahankan Arsip Kolonial).

## 8. Rancangan ontologi (A1 + B2)

Namespace tetap `sdp:` = `https://museumsumatera.id/ontology#`, `res:` = `.../resource/`.

### 8a. Aksioma skema (dipakai, bukan hiasan)

> **Catatan konsistensi (temuan builder-check A1).** `src/lib/ontology.ts` mendeklarasikan
> `rdfs:domain sdp:Museum` untuk `hasImage`/`hasExhibit`/`hasSource`/`hasCollection`/`hasFacility`.
> Bila properti yang sama diberi `owl:inverseOf` yang `rdfs:range`-nya `Museum`, OWL 2 RL akan
> menyimpulkan setiap `Image`/`Exhibit`/... adalah `Museum` → **graf inconsistent**. Karena itu, pada
> properti yang di-inverse, **domain/range eksplisit dilepas** dan pola domain/range dipindahkan ke
> `owl:Restriction` di sisi subjek. Ini bukan pilihan bebas: ia mengikuti aturan OWL 2 RL yang
> dipilih pengguna (A1).

- **Anotasi ontologi:** `<https://museumsumatera.id/ontology> a owl:Ontology` dengan
  `owl:versionInfo "1.1.0"`, `dcterms:created`, `dcterms:modified`, `rdfs:label`, `rdfs:comment`.
- **Hierarki `subClassOf` pada `Museum`** (P1, P2 — turunan derujuk dari `history`):
  - `sdp:StateMuseum rdfs:subClassOf sdp:Museum` — museum negeri/dikelola pemerintah (termasuk
    museum provinsi/kabupaten/kota: negeri-aceh, negeri-sumut, negeri-sumbar, dsb.).
  - `sdp:SiteMuseum rdfs:subClassOf sdp:Museum` — situs/cagar/istana/rumah bersejarah yang dibuka
    sebagai museum (huta-bolon, taman-purbakala-sriwijaya, purbakala-pugung-raharjo, malikussaleh,
    istana-siak, rumah-pengasingan-bung-karno, rumah-kelahiran-buya-hamka, dsb.).
  - `sdp:PrivateMuseum rdfs:subClassOf sdp:Museum` — museum swasta/yayasan (tb-silalahi-center).
  - Setiap instance museum mendapat **minimal satu** `rdf:type` turunan selain `sdp:Museum`;
    `SiteMuseum` **boleh** beririsan dengan `StateMuseum` (P1). DTO `type` = `string[]` (P2).
- **`subClassOf` pada entitas:** `sdp:Founder rdfs:subClassOf sdp:Person`,
  `sdp:Curator rdfs:subClassOf sdp:Person` (memungkinkan peran tokoh).
- **`owl:inverseOf` (berpasangan):**
  - `hasImage` ↔ `imageOfMuseum`
  - `hasExhibit` ↔ `exhibitOfMuseum`
  - `hasSource` ↔ `sourceOfMuseum`
  - `hasCollection` ↔ `collectionOfMuseum`
  - `hasFacility` ↔ `facilityOfMuseum`
  - `locatedInProvince` ↔ `provinceOfMuseum`
  - Pada tiap pasangan: **domain/range dilepas** (lihat catatan A1) dan dinyatakan lewat
    `owl:Restriction` di kelas pemilik. Generator cukup menulis satu arah; reasoner membentuk inverse.
- **Properti `Functional`:** `establishedYear` (satu tahun — **hanya bila ada**, tidak boleh dikasih
  `minCardinality` karena 15 museum bernilai null), `chapter` (satu bab), `locatedInCity` (satu kota
  **per museum** — lihat A5), `heritageStatusOf` (satu status per museum bila ada).
- **`owl:Functional` pada `locatedInCity` bermakna "satu museum satu kota"**, bukan "satu kota satu
  museum". Data sekarang: 5 kota berisi >1 museum (Palembang 3; Banda Aceh, Toba, Jambi, Bengkulu
  2) sehingga `locatedInCity` **tidak boleh** `InverseFunctional`/fungsional dari sisi kota (A5).
- **`owl:TransitiveProperty`:** hierarki wilayah (`sdp:ancestorRegion`: Province→Region→Region)
  opsional. Bila tidak dibutuhkan untuk tampilan, **dilepas** (M3); bukti penalaran cukup diambil
  dari rantai `rdfs:subClassOf`. Bila dipakai, harus konsisten.
- **`owl:Restriction` (cardinality yang valid terhadap data, terbukti A3):**
  - `Museum rdfs:subClassOf [ a owl:Restriction ; owl:onProperty sdp:locatedInProvince ;
    owl:cardinality 1 ]`
  - `Museum rdfs:subClassOf [ ... sdp:chapter ; owl:cardinality 1 ]`
  - `Museum rdfs:subClassOf [ ... sdp:hasTheme ; owl:minCardinality 1 ]`
  - `Museum rdfs:subClassOf [ ... sdp:locatedInCity ; owl:maxCardinality 1 ]`
  - `Museum rdfs:subClassOf [ ... sdp:hasImage ; owl:minCardinality 0 ]` dan seterusnya untuk pola
    domain (menggantikan `rdfs:domain` pada properti yang di-inverse).
- **Disjointness minimal yang aman:** `owl:disjointWith` **hanya** antara `StateMuseum` dan
  `PrivateMuseum` (paling sedikit: museum negeri dan museum yayasan tidak bisa sama). `SiteMuseum`
  **tidak** dibuat disjoint dari keduanya (P1). Data diuji agar tidak melanggar.
- **Validasi:** berkas ontologi harus lolos reasoner (HermiT/Protégé atau `robot`) tanpa
  inconsistency. Ini jadi bukti penalaran yang bisa ditunjukkan saat penilaian.

### 8b. Kelas & properti baru (entitas B2)

**Kelas baru:** `Person`, `Founder` (⊑ Person), `Curator` (⊑ Person), `Facility`,
`HeritageStatus`, `Region` (untuk hierarchy wilayah), dan kelas turunan `Museum` (8a).

**Object property baru:**
- `hasFounder` → `Person` (inverse `founderOfMuseum`), juga `hasCurator` → `Person`.
  `hasCurator` **tidak** `Functional` (A2) — museum bisa punya lebih dari satu kurator.
- `hasFacility` → `Facility` (inverse `facilityOfMuseum`).
- `heritageStatusOf` → `HeritageStatus` (Functional; inverse `isHeritageStatusOf`).
- `namedAfter` → `Person` (museum dinamai tokoh; inverse `isNamesakeOfMuseum`).
- `relatedMuseum` → `Museum` (`owl:SymmetricProperty`). **Generator menulis pasangan dua arah**
  agar Fuseki (tanpa reasoner) dan Protégé (dengan reasoner) memberi hasil sama (A7).

**Datatype property baru (museum):** `collectionSize` (xsd:integer), `governingBody` (string),
`openingHours` (string), `foundedBy` (string, **hanya bila** tidak ada entitas Person —
lihat M10: jangan isi `foundedBy` dan `hasFounder` bersamaan), `wikidataId` (anyURI, opsional).

**Datatype property baru (entitas):** `personName` (string), `personRole` (string),
`facilityName` (string), `heritageLabel` (string), `collectionCategory` (string) untuk `Collection`.

**`Collection` kini dipakai nyata (P3).** Kategori diambil **hanya dari sumber** yang menyebut
eksplisit (mis. Museum Aceh: "Koleksi etnografika dan filologika" → `etnografika`, `filologika`;
Museum Timah Indonesia: "Koleksi etnografi Bangka"). **Museum tanpa penyebutan kategori tidak
mendapat `Collection`.** Tidak ada pembuatan kategori generik (C2 tidak dipakai di sini).

### 8c. Perkaya data (C1)

- **C1 dulu:** isi field baru (`collectionSize`, `governingBody`, `openingHours`, `foundedBy`,
  `categories`, `collections[]`, `founder`, `facilities[]`, `heritage`, `relatedSlugs[]`) dari
  sumber yang sudah tercatat di `sources` masing-masing museum. Bila tak ada sumber → biarkan
  kosong (field `null`/tidak ada) dan tetap tandai `perlu-verifikasi`.
- **C2 hanya bila buntu mutlak:** bila sebuah field memang tak punya sumber sama sekali untuk
  museum tertentu tetapi nilainya krusial untuk tampilan, isi nilai generik yang masuk akal dan
  beri disclaimer global di footer/tentang. Jangan diam-diam; beri komentar data bahwa ini generik.
- **Konsekuensi yang disengaja (P3, P5):** banyak museum **tidak** akan punya `collections[]`,
  `facilities[]`, atau `heritage` karena sumbernya tidak menyebut. Ini **benar**: graf lebih baik
  jujur dan kosong daripada berisi kategori karangan. Tampilan menangani field kosong dengan baik.
- **`museums.json` disentuh:** field baru ditambahkan ke `MuseumRecord` (`src/lib/types.ts`) dan ke
  28 record. Ini konsisten dengan misi, tetapi plan harus menyebutnya eksplisit (berarti menyentuh
  seluruh 28 record, walau sebagian hanya mendapat field opsional kosong).
- **Jangan tambah literal `xsd:gYear` untuk field baru.** `generate-rdf.test.ts` menguji bahwa
  literal `gYear` hanya muncul sesuai harapan; field baru (mis. tahun penetapan cagar budaya)
  memakai `xsd:integer`, bukan `gYear` (temuan builder-check #2).

## 9. Rancangan frontend (arsip digital museum, identitas Arsip Kolonial)

### 9a. Fondasi (diperluas, bukan diganti)

Token warna & tipografi dari `globals.css` dipertahankan; **ditambah**:
- Skala tipografi arsip: `--type-index` (nomor arsip besar serif), `--type-label` (label museum),
  `--type-meta` (mono kecil untuk kode/kredit).
- Warna pendukung: `--accent-soft`, `--gold` (garis/aksen katalog), tetap netral kertas.
- Komponen utilitas baru: `.plate` (bingkai foto museum), `.specimen-card` (lembar katalog),
  `.index-board` (papan indeks), `.meta-table` (tabel metadata presisi).

### 9b. Karakter per halaman

- **Sampul (`/`):** hero narasi + **papan indeks** tujuh bab (nomor romawi besar, provinsi, jumlah
  museum). Kesan: pintu masuk lemari arsip.
- **Bab (`/jelajah/[n]`):** narasi + daftar museum sebagai **papan indeks bab** dengan nomor
  arsip; tiap entri kartu ringkas dengan plate foto kecil + label.
- **Museum (`/museum/[slug]`):** **lembar katalog bergaya specimen card** — nomor arsip, judul,
  plate foto berlabel (kredit + lisensi rapi di bawah), tabel metadata presisi (mono untuk kode),
  bagian Sejarah, Isi pameran, klasifikasi koleksi, benang merah.
- **Katalog (`/katalog`):** **indeks arsip** — grid/daftar seperti indeks kabinet, dengan panel
  penyaring yang menonjol, penanda hasil (jumlah), tetap memakai filter di SPARQL.
- **Tentang (`/tentang`):** tambahkan penjelasan ontologi yang lebih kaya (kelas baru, aksioma)
  sebagai "lembar metode" — berguna untuk penilaian.

### 9c. Komponen baru / diubah

- Baru: `MuseumPlate`, `SpecimenCard`, `IndexBoard`, `MetaTable`, `KoleksiPanel` (collection chips),
  `FacilityList`, `HeritageBadge` (hanya dirender bila status cagar budaya **ada**; **tidak**
  berimpit dengan `VerificationBadge` — P5).
- Diubah: `MuseumEntry`, `ChapterList`, `ChapterNav`, `MuseumGallery`, `CatalogView`,
  `VerificationBadge` (tetap murni status verifikasi; tidak digabung dengan heritage).
- Tetap: `SearchBox`, `SourceList`, `ThreadOfRelation`, `EmptyState`, `MuseumImage` (inti).

## 10. Arsitektur & aliran data

```
data/museums.json  ──generate──▶  data/museum-sumatera.rdf ──upload──▶ Fuseki
        │                                   ▲
        └─ dikonsumsi UI via lib/types.ts    │  ontology/museum-sumatera.ttl
                                              (skema diselaraskan generator)
UI: page.tsx · jelajah · museum · katalog · tentang
    lib/queries.ts (SPARQL, tambah query entitas baru)
    lib/types.ts   (field/DTO baru, opsional)
```

- **Query baru** di `lib/queries.ts`: `museumCollectionsQuery`, `museumFacilitiesQuery`,
  (dan `museumHeritageQuery` disiapkan bila `heritage` kelak terisi) dipakai `attachMuseumDetail`.
  `MUSEUM_PROJECTION` diperluas untuk `collectionSize`, `governingBody`, `openingHours`,
  `categories`, dan `type` (subkelas).
- **Peringatan duplikasi baris (temuan builder-check #3):** menambahkan `?museum a ?type` di luar
  subquery akan **menggandakan baris katalog**. `type` harus dikumpulkan seperti `themes` — lewat
  subquery `GROUP_CONCAT` (atau `FILTER(?type != sdp:Museum)` di dalam klausa terpisah) — bukan
  sebagai pola `OPTIONAL` langsung di blok utama.
- **`MuseumDTO` field baru wajib bersifat opsional (`?:`)** agar `src/lib/related.test.ts` (fixture
  objek literal lengkap) dan `route.test.ts` tetap lulus kompilasi (temuan builder-check #4).
  `mapMuseumRow` boleh mengisi `undefined` (bukan `[]`) untuk field kosong. `attachMuseumDetail`
  juga harus memperbarui `type` bila ia diisi lewat query rincian (temuan #5).
- **`POST` tetap** ke Fuseki `application/sparql-results+json`; kegagalan → 502/offline seperti lama.
- **`check:rdf` (A6):** `scripts/check-rdf.ts` memanggil `validateMuseums(records)` atas JSON, jadi
  aturan baru (mis. `collectionSize` integer ≥ 0, `type` valid, tidak ada `Collection` duplikat per
  museum) ditambahkan ke `src/lib/validate.ts` — bukan ke parser RDF.

## 11. Yang diputuskan pengguna

- Ontologi opsi **C** (skema + data) dan level **A1** (OWL 2 wajar).
- Entitas **B2** (perkaya + `Person`, `Collection`, `Facility`, `HeritageStatus`).
- Akurasi **C1**; **C2** hanya bila benar-benar buntu.
- Visual opsi **2C** (arsip digital museum), identitas **Arsip Kolonial dipertahankan**.
- **P1/P2:** taksonomi 3 subkelas diturunkan dari `history`; `SiteMuseum` boleh beririsan dengan
  `StateMuseum`; museum boleh punya lebih dari satu tipe turunan; DTO `type: string[]`.
- **P3:** `Collection` hanya bila sumber menyebut kategori eksplisit; kriteria "setiap museum punya"
  dilonggarkan.
- **P4:** `relatedMuseum` = bonus bobot **+4**; aturan "skor 0 disembunyikan" tetap berlaku.
- **P5:** `Facility` hanya dari sumber; `HeritageStatus` tidak diinstansiasi; `HeritageBadge` tidak
  berimpit dengan `VerificationBadge`.
- **P6:** kriteria identitas Arsip Kolonial dibuktikan **dengan token** (objektif, §13.10).

## 12. Yang diserahkan ke pembangun (builder's discretion)

- Nama komponen final & pembagian sub-komponen; urutan pengerjaan
  (disarankan: TTL → generator skema → generator data/entitas → query/DTO → UI).
- Apakah `ancestorRegion`/`Region` dipakai (lihat catatan 8a) selama konsistensi terjaga; bila tidak
  perlu, **dilepas** dan bukti Transitive diambil dari rantai `subClassOf`.
- Skala tipografi persis, spesimen grid vs list pada katalog, tekstur kertas halus.
- Reasoner yang dipakai untuk validasi (`robot`/Protégé/HermiT) dan skrip pengecek opsional.
- Detail alat uji baru (unit test query entitas, test generator entitas, test konsistensi ontologi).
- Kata kunci alasan (`reason`) untuk `relatedMuseum` ("satu koleksi", "ditautkan arsip", dst.).
- Cara mengumpulkan `type` di SPARQL (subquery `GROUP_CONCAT`) — asalkan tidak menggandakan baris.

## 13. Kriteria selesai yang bisa diperiksa

1. `npm run generate:rdf` menghasilkan RDF/XML dengan kelas/properti/aksioma baru; setiap museum
   punya **minimal satu** `rdf:type` turunan `Museum` (State/Site/Private); museum yang sumbernya
   menyebut kategori eksplisit punya `sdp:Collection` (tidak ada `Collection` tanpa dasar sumber).
2. Ontologi TTL lolos reasoner tanpa inconsistency (bukti inferensi: instance turunan ⇒ subkelas
   `Museum`; inverse terbentuk).
3. `npm run check:rdf` diperluas lewat `src/lib/validate.ts`: menolak museum tanpa tema/bab/provinsi;
   bila `collectionSize` ada harus integer ≥ 0; `type` harus subset yang sah; tidak ada
   `Collection` duplikat dalam satu museum.
4. `npm test` lulus semua (termasuk test baru query entitas & generator), dan `npm run build` lolos
   TypeScript (memastikan field DTO `?` tidak mematahkan fixture test lama).
5. Halaman sampul/bab/museum/katalog menampilkan komponen baru dan tetap tampil walau Fuseki mati.
6. Filter katalog masih 100% di SPARQL; benang merah masih dari relasi (turunan + `relatedMuseum`
   bonus +4).
7. README & halaman Tentang menjelaskan ontologi baru dan cara memvalidasi dengan reasoner.
8. `HeritageStatus` tidak diinstansiasi di data; `Facility` hanya ada bila sumber menyebut.
9. Tidak ada properti yang menyimpan domain/range eksplisit **dan** `owl:inverseOf` sekaligus
   (konsistensi A1). Dibuktikan lewat pemeriksaan teks/skema otomatis.
10. **Identitas Arsip Kolonial dibuktikan dengan token (objektif):** `globals.css` tetap mendefinisikan
    `--paper: #f3ece0` (atau nilai ekivalen gelap-kertas) dan `--font-serif`, serta tidak
    memperkenalkan variabel palet baru yang menggantikan `--paper`/`--ink`/`--rule`. Diperiksa
    dengan `grep` atas berkas CSS; bukan penilaian visual.
