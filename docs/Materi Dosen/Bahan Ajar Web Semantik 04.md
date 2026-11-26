# Bahan Ajar Web Semantik 04


---

## Slide 1

PERTEMUAN 4 · TIF2305 · SUB-CPMK 3

Metadata & Dublin Core

Data tentang data: konsep, 15 elemen DCMES, dan cara menuliskannya

Mata Kuliah Web Semantik

Program Studi Teknologi Informasi

150 menit


### Catatan Pengajar

Selamat datang di Pertemuan 4. Tanyakan cepat: siapa yang pernah menambahkan meta description atau og:image pada halaman HTML sendiri? Ini jembatan yang bagus ke topik metadata — mereka sudah pernah menyentuh metadata tanpa menyebutnya demikian. Sampaikan bahwa hari ini kita masuk ke fondasi 'data tentang data' yang menjadi backbone semua sistem semantik. Durasi cover sekitar 2 menit.


---

## Slide 2

RENCANA SESI

Alur Pertemuan Hari Ini

00

Pembuka, agenda, dan capaian pembelajaran

10 menit

01

Konsep dan jenis metadata

25 menit

02

Dublin Core Element Set — 15 elemen

45 menit

03

Encoding: HTML, RDF/Turtle, JSON-LD

35 menit

04

Interoperabilitas dan OAI-PMH

15 menit

05

Praktik mandiri, kuis LMS, dan ringkasan

20 menit

WEB SEMANTIK · TIF2305

02


### Catatan Pengajar

Tunjukkan agenda dan alokasi waktu lima segmen. Tekankan segmen 03 (encoding) adalah yang paling teknis — mahasiswa perlu mengikuti contoh baris per baris dan sebaiknya membuka editor bila ingin follow-along. Kuis LMS 5 soal di menit 140 sampai 145. Alokasi ini pedoman, boleh disesuaikan dengan dinamika kelas.


---

## Slide 3

SUB-CPMK 3 · BAGIAN 1

Capaian Pembelajaran

Tiga capaian, tiga level: memahami — mengidentifikasi — menerapkan.

CPMK-A

Menjelaskan

Konsep metadata: definisi, tiga jenis utama, dan perannya di web.

CPMK-B

Mengidentifikasi

15 elemen Dublin Core (DCMES) beserta kelompok fungsionalnya.

CPMK-C

Menerapkan

Dublin Core pada HTML, RDF/Turtle, dan JSON-LD sederhana.

Pertemuan 5 (Ontology) mengasumsikan ketiga capaian ini sudah dikuasai.

WEB SEMANTIK · TIF2305

03


### Catatan Pengajar

Jelaskan bahwa CPMK-A ada di level pemahaman, CPMK-B identifikasi, dan CPMK-C penerapan — konsisten dengan Sub-CPMK 3 di RPS. Sampaikan bahwa Pertemuan 5 tentang Ontology akan mengasumsikan ketiga capaian ini sudah dikuasai. Sebutkan pemetaan asesmen: capaian A diuji lewat kuis nomor 1 dan 4, capaian B lewat kuis nomor 2, 3, 5 dan tugas, capaian C lewat tugas mandiri.


---

## Slide 4

RECAP · JEMBATAN

Dari JSON-LD ke Metadata Standar

PERTEMUAN 3

Metadata tentang halaman

Markup schema.org di halaman web, dibaca mesin pencari komersial.

→

PERTEMUAN 4

Metadata tentang karya

Dokumen, dataset, dan koleksi — dideskripsikan dengan standar internasional.

Dublin Core (ISO 15836) bukan pesaing schema.org — keduanya dua bahasa dengan target berbeda, dan bisa dipakai bersamaan dalam satu dokumen JSON-LD.

WEB SEMANTIK · TIF2305

04


### Catatan Pengajar

Tanyakan: 'kalau JSON-LD di halaman produk itu metadata bukan?' — arahkan diskusi: ya, itu metadata TENTANG produk. Hari ini kita naik satu level: metadata TENTANG dokumen, dataset, dan koleksi, dengan kosakata yang sudah menjadi standar internasional yaitu Dublin Core (ISO 15836). Tekankan perbedaan orientasi: schema.org untuk konsumen mesin pencari komersial, Dublin Core untuk pertukaran metadata antar-institusi.


---

## Slide 5

01

Konsep & Jenis Metadata

25 menit · Slide 5–9

Tujuan: memahami apa itu metadata, tiga fungsi utamanya, dan tiga jenisnya — sebelum masuk ke standar yang konkret.

WEB SEMANTIK · TIF2305

05


### Catatan Pengajar

Divider — beri jeda lima detik untuk menandai pergantian segmen. Alokasi 25 menit sampai divider berikutnya: definisi 5 menit, tiga fungsi 7 menit, tiga jenis 8 menit, metadata di web 5 menit.


---

## Slide 6

SEGMEN 1 · DEFINISI

Kartu Katalog untuk Era Digital

DEFINISI · ISO 15836

Informasi terstruktur yang mendeskripsikan, menjelaskan, mencari lokasi, atau memudahkan pencarian, penggunaan, dan pengelolaan sebuah sumber daya informasi.

Satu kartu kecil cukup untuk menemukan satu buku di antara ratusan ribu. Metadata melakukan hal yang sama untuk dokumen, dataset, dan halaman web.

Google Scholar meranking karya bukan hanya dari isi PDF, tetapi dari judul, penulis, tahun, dan abstraknya.

WEB SEMANTIK · TIF2305

06


### Catatan Pengajar

Mulai dengan pertanyaan pemantik: 'kalau kalian mencari makalah di Google Scholar, apa yang Google cari — isi PDF atau metadatanya?' Jawabannya keduanya, tetapi metadata (judul, penulis, tahun, abstrak) yang men-drive ranking. Pakai analogi kartu katalog perpustakaan — ini konsep yang paling mudah membekas: satu kartu kecil mendeskripsikan satu buku besar. Bacakan definisi resmi ISO 15836.


---

## Slide 7

SEGMEN 1 · FUNGSI

Tiga Fungsi Utama Metadata

FIND

Membantu mesin pencari seperti Google Scholar mengindeks dan meranking karya.

MANAGE

Mengatur arsip internal seperti repositori DSpace kampus.

INTEROP

Memungkinkan sistem antar-institusi saling berbicara lewat OAI-PMH.

WEB SEMANTIK · TIF2305

07


### Catatan Pengajar

Beri contoh konkret untuk tiap fungsi. FIND — perlihatkan hasil Google Scholar dengan snippet penulis dan tahun. MANAGE — sebut DSpace atau repositori kampus untuk pengelolaan arsip internal. INTEROP — jelaskan OAI-PMH sebagai protokol yang bergantung seratus persen pada metadata Dublin Core. Tekankan ketiga fungsi ini adalah alasan mengapa institusi mau berinvestasi menulis metadata dengan rapi.


---

## Slide 8

SEGMEN 1 · KLASIFIKASI

Tiga Wajah Metadata

Deskriptif WHAT

Siapa penulisnya, apa judulnya, apa kata kuncinya — wilayah Dublin Core.

Struktural HOW ORGANIZED

Bagaimana bab disusun, urutan halaman, hubungan antar berkas.

Administratif HOW MANAGED

Kapan diarsipkan, siapa pemegang hak cipta, apa tipe berkasnya.

WEB SEMANTIK · TIF2305

08


### Catatan Pengajar

Tekankan kolom pertanyaan yang dijawab tiap jenis — ini cara paling mudah mahasiswa mengingat perbedaannya. Deskriptif menjawab what dan who, struktural menjawab how organized, administratif menjawab how managed. Ingatkan bahwa Dublin Core hari ini berfokus pada metadata deskriptif; sisi administratif hanya diwakili sebagian oleh Date, Rights, dan Format.


---

## Slide 9

SEGMEN 1 · LANSKAP

Metadata di Web Modern

Enam ekosistem yang hidup berdampingan — Dublin Core adalah lapisan paling universal.

schema.org

Kosakata mesin pencari komersial untuk halaman web.

Open Graph

Pratinjau tautan di media sosial dan aplikasi pesan.

Dublin Core

Standar minimal dan universal untuk pertukaran antar-institusi.

EXIF & IPTC

Metadata teknis dan editorial yang menempel pada berkas gambar.

DataCite

Skema metadata untuk DOI dataset penelitian — banyak mengambil dari DC.

MARC & METS

Standar perpustakaan dan pengemasan objek digital yang lebih rinci.

WEB SEMANTIK · TIF2305

09


### Catatan Pengajar

Tunjukkan bahwa Dublin Core hanya SATU dari sekian ekosistem metadata — bukan pengganti yang lain. Yang membuatnya penting: paling minimal, paling universal, dan paling banyak diadopsi. OAI-PMH bahkan MEWAJIBKAN Dublin Core sebagai format baseline. Kalau ditanya apakah DC masih relevan di era schema.org: ya, karena DataCite dan repositori akademik mengambil banyak dari DC.


---

## Slide 10

02

Dublin Core Element Set

45 menit · Slide 10–15

Lima belas elemen, tiga kelompok fungsional — semuanya opsional dan dapat diulang.

WEB SEMANTIK · TIF2305

10


### Catatan Pengajar

Divider segmen inti. Sampaikan bahwa 45 menit berikutnya adalah materi paling padat hari ini — mahasiswa perlu mengaktifkan catatan. Segmen ini dibagi lima blok: sejarah DCMI, peta 15 elemen, kelompok konten, kelompok hak dan instansiasi, lalu DCTERMS.


---

## Slide 11

SEGMEN 2 · SEJARAH

Satu Standar untuk Banyak Katalog

Lokakarya Dublin, Ohio (1995) — bukan Dublin di Irlandia.

1995

Lokakarya OCLC/NCSA menyepakati kebutuhan deskripsi minimal lintas domain.

DCMES 1.1

15 elemen inti — kemudian dibakukan sebagai ISO 15836.

DCTERMS

75+ istilah kualifikasi yang dipelihara DCMI hingga sekarang.

WEB SEMANTIK · TIF2305

11


### Catatan Pengajar

Fun fact: 'Dublin' merujuk ke Dublin, Ohio — kantor OCLC — bukan Dublin di Irlandia. Ini sering keliru. Ceritakan masalah awal web: setiap institusi memiliki skema metadatanya sendiri sehingga sistem A tidak bisa membaca katalog sistem B. Solusinya lokakarya 1995 yang melahirkan DCMI. Sebutkan DCMI tetap aktif dan memelihara dua kosakata: DCMES 15 elemen dan DCTERMS 75 istilah lebih.


---

## Slide 12

SEGMEN 2 · PETA ELEMEN

15 Elemen, Tiga Kelompok

Semua elemen bersifat opsional dan dapat diulang.

KONTEN

7 elemen

Title

Type

Subject

Source

Description

Relation

Coverage

KEKAYAAN INTELEKTUAL

4

Creator

Publisher

Contributor

Rights

INSTANSIASI

4

Date

Format

Identifier

Language

Namespace resmi DCMES 1.1: http://purl.org/dc/elements/1.1/

WEB SEMANTIK · TIF2305

12


### Catatan Pengajar

Slide ini penting — minta mahasiswa memotret atau screenshot. Sebutkan ketiga cluster satu per satu: KONTEN (apa isinya) tujuh elemen, KEKAYAAN INTELEKTUAL (siapa yang punya) empat elemen, INSTANSIASI (bentuk fisik atau digitalnya) empat elemen. Total lima belas. Tekankan semua elemen bersifat OPSIONAL dan DAPAT DIULANG — tidak ada yang wajib menurut spesifikasi, meski Application Profile lokal boleh mewajibkan subset.


---

## Slide 13

SEGMEN 2 · KELOMPOK KONTEN

Tujuh Elemen tentang Isi

Title

Nama yang diberikan pada sumber daya.

Subject

Topik — kata kunci dari thesaurus.

Description

Abstrak atau ringkasan naratif.

Type

Genre — wajib dari DCMI Type Vocabulary.

Source

Sumber asal tempat karya ini diturunkan.

Relation

Kaitan dengan sumber daya lain.

Coverage

Cakupan ruang atau waktu.

SERING TERTUKAR

Subject = kata atau frase kunci, sebaiknya dari thesaurus (LCSH, MeSH, DDC). Description = kalimat atau abstrak naratif.

DCMI Type Vocabulary · 12 tipe

Text · Dataset · Image · StillImage · MovingImage · 
Sound · Software · Collection · Event · Service · 
PhysicalObject · InteractiveResource

WEB SEMANTIK · TIF2305

13


### Catatan Pengajar

Fokus utama diskusi: Subject vs Description — mahasiswa sering rancu. Subject adalah KATA atau FRASE KUNCI, sebaiknya diambil dari thesaurus seperti LCSH, MeSH, atau DDC. Description adalah KALIMAT atau abstrak naratif. Type harus diambil dari DCMI Type Vocabulary yang berisi dua belas tipe: Collection, Dataset, Event, Image, InteractiveResource, MovingImage, PhysicalObject, Service, Software, Sound, StillImage, Text. Untuk coverage: DCMES menyatukan cakupan geografis dan temporal; kalau perlu presisi gunakan dcterms:spatial dan dcterms:temporal.


---

## Slide 14

SEGMEN 2 · HAK & INSTANSIASI

Delapan Elemen Sisanya

Creator

Penulis atau pencipta utama.

Publisher

Pihak yang menerbitkan.

Contributor

Editor, penerjemah, ilustrator.

Rights

Hak dan lisensi — sertakan URL-nya.

Date

Tanggal peristiwa daur hidup karya.

Format

Tipe media, mis. application/pdf.

Identifier

Pengenal unik — utamakan URI atau DOI.

Language

Kode bahasa BCP 47.

JEBAKAN FORMAT YANG SERING SALAH

SALAH

BENAR

05/03/2012

2012-03-05

"Bahasa Indonesia"

id · en-US · jv

No. 1204/TI/2026

https://doi.org/10.…

Di konteks Linked Data, nilai dc:creator sebaiknya berupa URI (misalnya ORCID) agar identitas penulis tidak ambigu.

WEB SEMANTIK · TIF2305

14


### Catatan Pengajar

Tekankan aturan format yang paling sering salah. Date memakai ISO 8601 format tahun-bulan-tanggal, bukan 05/03/2012. Identifier utamakan URI atau DOI, bukan nomor lokal. Language memakai kode BCP 47 seperti id, en-US, atau jv — bukan string bebas 'Bahasa Indonesia'. Rights sebaiknya menyertakan URL lisensi bila memakai Creative Commons atau lisensi open source. Jelaskan juga beda Creator dan Contributor: Creator adalah entitas utama yang bertanggung jawab atas isi, Contributor adalah pihak pendukung seperti editor, penerjemah, atau ilustrator.


---

## Slide 15

SEGMEN 2 · KUALIFIKASI

DCTERMS: Dari Sederhana ke Spesifik

Perluasan resmi berbasis sub-property — memperkaya tanpa merusak sistem lama.

DCMES · 15 ELEMEN

Sangat luas dan universal.

Cocok untuk penandaan HTML yang cepat.

Contoh: dc:date

DCTERMS · 75+ ISTILAH

Mendukung Linked Data modern.

Cocok untuk repositori dan dataset serius.

Contoh: dcterms:created

contoh kualifikasi

dc:date       → dcterms:created, dcterms:modified
dc:coverage   → dcterms:spatial, dcterms:temporal
dc:format     → dcterms:extent, dcterms:medium

Setiap istilah DCTERMS adalah sub-property dari elemen DCMES-nya — parser lama yang hanya paham dc:date tetap dapat melakukan fallback.

WEB SEMANTIK · TIF2305

15


### Catatan Pengajar

Poin penting: DCTERMS BACKWARD-COMPATIBLE dengan DCMES. dcterms:created adalah sub-property dari dc:date, sehingga parser sederhana yang hanya paham dc:date tetap bisa melakukan fallback. Dorong mahasiswa MEMAKAI DCTERMS saat serius — repositori dan dataset — dan memakai DCMES saat cepat seperti HTML meta. Contoh nyata perlunya kualifikasi: coverage yang ambigu dipecah menjadi dcterms:spatial dan dcterms:temporal.


---

## Slide 16

03

Encoding Metadata

35 menit · Slide 16–19

Empat cara menuliskan Dublin Core: HTML <meta> , RDF/XML, Turtle, dan JSON-LD.

WEB SEMANTIK · TIF2305

16


### Catatan Pengajar

Divider — segmen paling teknis. Ingatkan mahasiswa membuka laptop atau editor kalau mau follow along. Idealnya buka editor dan browser berdampingan di layar. Empat cara akan dibahas: HTML meta 8 menit, RDF/XML dan Turtle 12 menit, JSON-LD dengan dcterms 12 menit, ditutup aktivitas JSON-LD Playground 3 menit.


---

## Slide 17

SEGMEN 3 · CARA 1

Dublin Core di <head> HTML

Rekomendasi resmi DCMI-HTML (2003) — masih dihasilkan DSpace dan EPrints hari ini.

HTML

<head>
  <link rel="schema.DC"
        href="http://purl.org/dc/elements/1.1/">
  <meta name="DC.title"
        content="Pengantar Web Semantik">
  <meta name="DC.creator" content="Budi Santoso">
  <meta name="DC.creator" content="Siti Aminah">
  <meta name="DC.date" content="2026-03-05">
  <meta name="DC.language" content="id">
</head>

Pemetaan prefix lewat link rel="schema.DC" wajib dilakukan sekali di awal.

Nama elemen bersifat case-sensitive: DC.title, bukan dc.title.

Elemen boleh diulang — dua DC.creator berarti dua penulis.

Manfaat lain: Zotero dan Mendeley membaca blok meta DC untuk menyusun sitasi otomatis.

WEB SEMANTIK · TIF2305

17


### Catatan Pengajar

Jelaskan bahwa cara ini adalah rekomendasi resmi DCMI-HTML tahun 2003. Meski Google modern lebih memilih schema.org, banyak sistem repositori seperti DSpace dan EPrints MASIH menghasilkan blok meta DC ini agar bisa dipanen OAI-PMH. Titik penting: link rel schema.DC memetakan prefix DC, nama elemen bersifat case-sensitive (DC.title bukan dc.title), dan elemen boleh diulang — dua Creator berarti dua penulis. Sebut juga manfaat lain: Zotero dan Mendeley membaca meta DC untuk sitasi.


---

## Slide 18

SEGMEN 3 · CARA 2 & 3

RDF/XML dan Turtle

Dua bentuk tulisan, satu himpunan triple yang identik.

RDF/XML

<rdf:RDF
  xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
  xmlns:dc="http://purl.org/dc/elements/1.1/">
  <rdf:Description
      rdf:about="http://repo.usu.ac.id/paper/123">
    <dc:title>Pengantar Web Semantik</dc:title>
    <dc:creator>Budi Santoso</dc:creator>
    <dc:date>2026-03-05</dc:date>
  </rdf:Description>
</rdf:RDF>

Turtle

@prefix dc:  <http://purl.org/dc/elements/1.1/> .
@prefix dct: <http://purl.org/dc/terms/> .

<http://repo.usu.ac.id/paper/123>
    dc:title   "Pengantar Web Semantik" ;
    dc:creator "Budi Santoso" ;
    dct:created "2026-03-05" ;
    dc:language "id" .

RDF/XML dapat diproses seluruh alat XML dari Pertemuan 2 — tetapi verbose.

Turtle jauh lebih ringkas dan nyaman ditulis manusia — dibahas mendalam di Pertemuan 7.

WEB SEMANTIK · TIF2305

18


### Catatan Pengajar

Tunjukkan kedua format berdampingan — keduanya menghasilkan TRIPLES yang IDENTIK, hanya bentuk serialisasinya berbeda. RDF/XML verbose, Turtle jauh lebih ringkas dan enak dibaca manusia. Sebutkan bahwa ini fondasi minggu 6 dan 7 tentang RDF dasar dan serialisasinya. Ingatkan prefix wajib: dc mengarah ke purl.org/dc/elements/1.1/ dan dct ke purl.org/dc/terms/.


---

## Slide 19

SEGMEN 3 · CARA 4

JSON-LD dengan dcterms

Wadah modern + kosakata universal — dan boleh dicampur dengan schema.org.

metadata.jsonld

{
  "@context": {
    "dc":  "http://purl.org/dc/elements/1.1/",
    "dct": "http://purl.org/dc/terms/",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },
  "@id": "http://repo.usu.ac.id/paper/123",
  "dc:title": "Pengantar Web Semantik",
  "dct:created": { "@value": "2026-03-05",
                   "@type": "xsd:date" },
  "dct:license": {
    "@id": "https://creativecommons.org/licenses/by/4.0/"
  }
}

@context

Memetakan prefix — cukup satu kali di atas.

@id

URI subjek, analog rdf:about.

@value + @type

Literal bertipe: tanggal atau bilangan.

{ "@id": … }

Nilai berupa IRI, misalnya URL lisensi.

Aktivitas: tempel di json-ld.org/playground, buka tab N-Quads, lihat triple yang terbentuk.

WEB SEMANTIK · TIF2305

19


### Catatan Pengajar

Ini kombinasi paling powerful hari ini: JSON-LD sebagai wadah, Dublin Core sebagai kosakata universal, dan schema.org untuk kekayaan semantik. Poin ajar: @context memetakan prefix cukup sekali di atas; @id adalah URI subjek, analog dengan rdf:about di RDF/XML; literal bertipe seperti date memakai pola @value plus @type — sama seperti Pertemuan 3; nilai IRI seperti URL lisensi dibungkus @id. Tutup dengan aktivitas: buka json-ld.org/playground, tempel contoh ini, dan lihat tab N-Quads untuk melihat triple yang terbentuk.


---

## Slide 20

04

Interoperabilitas

15 menit · Slide 20–21

Satu deposit lokal, visibilitas global — inilah alasan praktis menulis metadata dengan standar.

WEB SEMANTIK · TIF2305

20


### Catatan Pengajar

Divider — segmen aplikasi. Siapkan tautan ke portal repositori kampus bila ada, dan buka base-search.net untuk demo. Fokus segmen ini: mengapa metadata standar penting secara praktis, bukan hanya teoretis.


---

## Slide 21

SEGMEN 4 · STUDI KASUS

OAI-PMH: Dari Lokal ke Global

Protokol berbasis HTTP untuk memanen metadata antar-repositori. Format wajibnya oai_dc — Simple Dublin Core, 15 elemen.

ENAM VERBA

Identify

ListIdentifiers

ListMetadataFormats

ListRecords

ListSets

GetRecord

http://repo.usu.ac.id/oai/request?verb=ListRecords&metadataPrefix=oai_dc

Dipanen oleh BASE (350+ juta dokumen), OpenAIRE, CORE, dan Google Scholar.

WEB SEMANTIK · TIF2305

21


### Catatan Pengajar

Ini contoh riil kekuatan metadata standar: satu deposit lokal menghasilkan visibilitas global. Jelaskan OAI-PMH sebagai protokol berbasis HTTP untuk memanen metadata antar-repositori, dengan enam verba: Identify, ListMetadataFormats, ListSets, ListIdentifiers, ListRecords, GetRecord. Format WAJIB adalah oai_dc yaitu Simple Dublin Core 15 elemen. Ekosistemnya: BASE dengan lebih dari 350 juta dokumen, OpenAIRE, CORE, dan Google Scholar. Kalau ada waktu, buka base-search.net dan cari nama kampus atau dosen untuk membuktikan deposit lokal muncul di indeks global.


---

## Slide 22

RINGKASAN & PREVIEW

Empat Poin untuk Dibawa Pulang

01

Metadata adalah kartu katalog terstruktur yang bisa dibaca mesin.

02

Dublin Core — 15 elemen DCMES — adalah standar bahasa universalnya.

03

JSON-LD adalah cara penulisan paling modern; HTML meta dan Turtle tetap relevan.

04

OAI-PMH memakai Dublin Core untuk mendistribusikan karya lokal ke dunia.

PERTEMUAN 5 · ONTOLOGY

Dari deskripsi minimal menuju deskripsi kaya dengan aturan. Persiapan: baca A Semantic Web Primer Bab 3.1–3.3.

WEB SEMANTIK · TIF2305

24


### Catatan Pengajar

Rekap cepat — bacakan empat poin. Ingatkan tenggat tugas mandiri dan kuis LMS. Sambungkan ke Pertemuan 5: setelah 'deskripsi minimal' berupa metadata, kita naik ke 'deskripsi kaya dengan aturan' yaitu ontologi. Persiapan: baca A Semantic Web Primer Bab 3.1 sampai 3.3 sebelum kelas berikutnya. Tutup dengan terima kasih dan waktu untuk pertanyaan singkat.
