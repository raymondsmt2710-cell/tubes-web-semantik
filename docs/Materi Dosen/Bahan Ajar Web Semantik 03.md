# Bahan Ajar Web Semantik 03


---

## Slide 1

PERTEMUAN 3 · TIF2305 · SUB-CPMK 2

Data Terstruktur JSON-LD

@context · schema.org · penyematan ke HTML · validasi markup

Mata Kuliah Web Semantik

Program Studi Teknologi Informasi

150 menit


### Catatan Pengajar

Buka dengan pertanyaan: 'Siapa yang pernah melihat harga dan rating produk langsung muncul di hasil Google?' — itu hasil structured data. Sampaikan bahwa pertemuan ini lanjutan langsung dari XML: sama-sama format data, tetapi JSON-LD sudah membawa MAKNA. Tekankan sesi ini paling praktis sejauh ini — mahasiswa akan menulis dan memvalidasi markup sendiri. Pastikan koneksi internet siap untuk demo validator dan siapkan screenshot cadangan.


---

## Slide 2

RENCANA SESI

Agenda Hari Ini · 150 Menit

0–5

Pembuka dan recap Pertemuan 2 (XML)

Slide 1

5–15

Capaian pembelajaran dan jembatan XML → JSON-LD

Slide 3–4

15–45

Segmen 1 — Dari JSON ke JSON-LD

Slide 5–9

45–70

Segmen 2 — Kosakata schema.org

Slide 10–14

70–85

Istirahat

—

85–110

Segmen 3 — Menyematkan dan memvalidasi markup

Slide 15–18

110–130

Segmen 4 — Perbandingan dan studi kasus

Slide 19–21

130–145

Praktik markup dan kuis LMS

Slide 22–23

145–150

Ringkasan dan preview Pertemuan 4

Slide 24

WEB SEMANTIK · TIF2305

02


### Catatan Pengajar

Tunjukkan pembagian waktu; istirahat 15 menit jatuh di menit ke-70 sampai 85. Segmen 1 paling padat konsep — minta mahasiswa fokus penuh di 30 menit itu, dan sampaikan bahwa segmen ini tidak akan dipotong apa pun yang terjadi karena @context adalah fondasi seluruh sisa mata kuliah. Segmen 3 membutuhkan internet untuk demo Rich Results Test dan validator.schema.org. Praktik 15 menit di akhir: menulis satu blok JSON-LD tentang diri sendiri, lalu validasi dan unggah screenshot.


---

## Slide 3

SUB-CPMK 2 · BAGIAN 2

Capaian Pembelajaran

Setelah pertemuan ini, Anda diharapkan mampu:

01

Menjelaskan posisi JSON-LD sebagai serialisasi RDF dan bedanya dengan JSON biasa.

02

Menggunakan keyword @context, @type, @id, @value, dan @graph secara tepat.

03

Memilih tipe dan properti schema.org yang sesuai untuk sebuah entitas.

04

Menyematkan markup JSON-LD ke dalam halaman HTML dengan benar.

05

Memvalidasi markup memakai Rich Results Test dan Schema Markup Validator.

WEB SEMANTIK · TIF2305

03


### Catatan Pengajar

Bacakan lima capaian dan kaitkan tiap capaian ke segmen pada agenda sebelumnya. Tekankan capaian kelima (validasi) adalah yang dinilai lewat tugas praktik hari ini. Ingatkan bahwa Sub-CPMK 2 dinilai gabungan Pertemuan 2 (XML) dan Pertemuan 3 (JSON-LD), jadi keduanya perlu dikuasai.


---

## Slide 4

RECAP · JEMBATAN

Dari Tag Bersarang ke Data Bermakna

Struktur yang rapi belum berarti maknanya dipahami pihak lain.

Tag XML hanya dipahami oleh pihak yang menyusun skemanya. Kosakata JSON-LD disepakati bersama, sehingga satu markup dipahami semua mesin.

WEB SEMANTIK · TIF2305

04


### Catatan Pengajar

Jembatan penting: XML memberi STRUKTUR, JSON-LD memberi STRUKTUR + MAKNA. Analogi rak: XML seperti rak yang rapi tanpa label isi; JSON-LD seperti rak dengan label baku yang dipahami semua orang. Tanyakan ke kelas: 'kalau XML sudah bisa menyimpan data, kenapa masih perlu format lain?' — arahkan ke jawaban: karena tag XML hanya dipahami oleh pihak yang membuat skemanya, sementara kosakata JSON-LD disepakati bersama.


---

## Slide 5

01

Dari JSON ke JSON-LD

30 menit · Slide 5–9

Tujuan: Anda dapat menyebut komponen dokumen JSON-LD dan menjelaskan bagaimana @context mengubah JSON biasa menjadi RDF.

WEB SEMANTIK · TIF2305

05


### Catatan Pengajar

Segmen 1 — 30 menit. Konsep inti pertemuan ini ada di sini, jadi jangan dipotong walaupun waktu mepet. Tujuan: mahasiswa dapat menyebut komponen dokumen JSON-LD dan menjelaskan bagaimana @context mengubah JSON biasa menjadi RDF.


---

## Slide 6

SEGMEN 1 · POSISI

JSON-LD = JSON + Linked Data

Semua JSON-LD adalah JSON yang sah — tetapi tidak semua JSON adalah JSON-LD.

JSON biasa

{
  "nama": "Ida Dadi",
  "pekerjaan": "Dosen"
}

JSON-LD

{
  
"@context" : "https://schema.org",
   
"@type" : "Person",
   
"@id" : "https://usu.ac.id/dosen/idadi",
  "name": "Ida Dadi",
  "jobTitle": "Dosen"
}

Familiar — sintaksnya JSON, cukup JSON.parse() tanpa pustaka khusus.

Native RDF — setiap baris bisa diuraikan menjadi triple yang terhubung ke web.

Direkomendasikan — format structured data pilihan Google untuk halaman web.

WEB SEMANTIK · TIF2305

06


### Catatan Pengajar

Pertanyaan pemantik: 'Apa bedanya file JSON biasa dengan JSON-LD?' — jawaban kunci: kehadiran @context. Tekankan bahwa semua berkas JSON-LD adalah JSON yang sah, tetapi tidak semua JSON adalah JSON-LD. Sebutkan bahwa JSON-LD dirancang agar bisa dipakai tanpa pustaka khusus — JSON.parse() saja sudah cukup — inilah alasan ia menang populer dibanding RDF/XML yang verbose. Sebutkan Google secara resmi merekomendasikan JSON-LD untuk structured data.


---

## Slide 7

SEGMEN 1 · ANATOMI

Anatomi Dokumen JSON-LD

profil.jsonld

{
  "@context": "https://schema.org",
  "@type": "Person",
  "@id": "https://usu.ac.id/dosen/idadi",
  "name": "Ida Dadi",
  "jobTitle": "Dosen",
  "worksFor": {
    "@type": "Organization",
    "name": "FASILKOM-TI USU"
  }
}

@context

Kamus yang memetakan setiap kunci ke IRI kosakata global.

@type

Jenis entitas — diambil dari kosakata schema.org.

@id

IRI identitas node agar dapat dirujuk dari tempat lain.

properti

Nama properti mengikuti schema.org; nilainya boleh bahasa apa pun.

Tanpa tiga baris @ di awal, dokumen ini hanya JSON biasa — tanpa makna bagi mesin.

WEB SEMANTIK · TIF2305

07


### Catatan Pengajar

Bedah kode baris per baris dari atas ke bawah, sejajarkan dengan penjelasan di kanan. Tunjukkan bahwa tanpa tiga baris @ pertama, ini hanyalah JSON biasa tanpa makna. Ingatkan aturan JSON: kunci dan string WAJIB memakai kutip ganda dan tidak boleh ada koma menggantung di properti terakhir. Jelaskan bahwa @id tidak wajib, tetapi tanpa @id node menjadi blank node — sah namun tidak bisa dirujuk dari tempat lain.


---

## Slide 8

SEGMEN 1 · KOSAKATA INTI

Enam Keyword yang Wajib Dikenali

Tiga yang pertama dipakai di hampir setiap markup — hafalkan.

@context

Kamus universal: memetakan kunci lokal ke IRI kosakata global — seperti xmlns pada XML.

@type

Jenis entitas. Bersifat case-sensitive : Person bukan person.

@id

IRI identitas node. Tanpa @id , node menjadi blank node yang tak bisa dirujuk.

@value

Nilai literal mentah ketika perlu dipisahkan dari penandanya.

@language

Penanda bahasa nilai — dipakai untuk data multibahasa.

@graph

Wadah untuk beberapa node sekaligus dalam satu blok markup.

WEB SEMANTIK · TIF2305

08


### Catatan Pengajar

Tiga keyword pertama dipakai di hampir semua markup — pastikan mahasiswa hafal. @value dan @language baru terasa perlu saat data multibahasa; beri contoh judul buku dalam dua bahasa. @graph sangat berguna saat satu halaman mendeskripsikan beberapa entitas sekaligus — alternatifnya memakai beberapa blok script, keduanya sah.


---

## Slide 9

SEGMEN 1 · KONSEP KUNCI

@context — Jembatan Menuju Makna

Kunci lokal dipetakan ke IRI global, lalu dokumen terurai menjadi triple.

N-Quads hasil expand

<https://usu.ac.id/dosen/idadi>
  <https://schema.org/name>
  "Ida Dadi" .

Satu baris JSON menjadi satu triple . Inilah konsep Pertemuan 1 yang kini benar-benar terbentuk — dan @context memainkan peran xmlns dari Pertemuan 2.

WEB SEMANTIK · TIF2305

09


### Catatan Pengajar

Ini slide terpenting di segmen 1 — jangan buru-buru. Demo di JSON-LD Playground: tempel kode ini, buka tab N-Quads, tunjukkan triple yang muncul. Kaitkan ke Pertemuan 1: triple subjek-predikat-objek yang dulu dibahas kini benar-benar terbentuk dari markup. Kaitkan ke Pertemuan 2: @context berperan seperti xmlns pada XML namespace. Jika ditanya apakah URL di @context harus benar-benar ada: untuk schema.org ya, karena diambil prosesor JSON-LD; secara konsep IRI hanyalah identifier.


---

## Slide 10

02

Kosakata schema.org

25 menit · Slide 10–14

Tujuan: memilih tipe dan properti yang tepat untuk sebuah entitas — bukan menghafal seluruh daftar tipe.

WEB SEMANTIK · TIF2305

10


### Catatan Pengajar

Segmen 2 — 25 menit. Fokusnya memilih tipe yang benar, bukan menghafal semua tipe. Tujuan: mahasiswa dapat memilih tipe dan properti schema.org yang tepat untuk sebuah entitas serta menyusun relasi antar entitas.


---

## Slide 11

SEGMEN 2 · KAMUS BERSAMA

Satu Kosakata, Semua Mesin Pencari

Google, Bing, Yahoo, dan Yandex mendirikan schema.org pada 2011 — tulis markup sekali, dipahami semuanya.

Setiap halaman tipe memuat daftar properti lengkap beserta Expected Type — bacalah sebelum menulis markup.

Pilih tipe paling spesifik yang masih tepat ; jangan berhenti di Thing.

Properti yang tidak terdaftar akan diabaikan diam-diam oleh mesin pencari — tanpa pesan error. Ini kekeliruan yang sulit disadari.

WEB SEMANTIK · TIF2305

11


### Catatan Pengajar

Perkenalkan schema.org sebagai kamus bersama. Sebutkan empat mesin pencari pendirinya — inilah yang membuat markup cukup ditulis sekali dan dipahami semuanya. Telusuri live di schema.org: buka Thing lalu CreativeWork lalu Book, tunjukkan daftar properti lengkap dengan Expected Type di setiap halaman tipe. Ingatkan: pakai tipe paling spesifik yang masih tepat, jangan asal memakai Thing. Kalau tipe yang dibutuhkan tidak ada, pilih tipe induk terdekat lalu tambahkan additionalType.


---

## Slide 12

SEGMEN 2 · HIERARKI & TIPE

Memilih Tipe yang Tepat

TIPE YANG PALING SERING DIPAKAI

Person

name · jobTitle · affiliation · knowsAbout

Organization

name · url · logo · address

Course

courseCode · provider · educationalLevel

Event

startDate · location · organizer

ScholarlyArticle

headline · author · datePublished

Product

offers · aggregateRating · brand

Setiap properti punya expected type: author mengharapkan Person atau Organization — bukan teks bebas.

WEB SEMANTIK · TIF2305

12


### Catatan Pengajar

Course dan Event paling relevan untuk konteks kampus — pakai keduanya sebagai contoh utama. Tekankan bahwa properti punya expected type: author mengharapkan Person atau Organization, bukan string bebas. Latihan cepat dua menit: minta mahasiswa menebak tipe yang cocok untuk kanal YouTube prodi (Organization atau CreativeWork), skripsi mahasiswa (ScholarlyArticle atau Thesis), laboratorium komputer (Place), dan mata kuliah ini (Course). Satu entitas boleh punya lebih dari satu tipe, ditulis sebagai array.


---

## Slide 13

SEGMEN 2 · CONTOH

Dua Entitas, Dua Markup

Nama properti berbahasa Inggris mengikuti schema.org; nilainya boleh bahasa Indonesia.

Person

{
  "@context": "https://schema.org",
  "@type": "Person",
  "@id": "https://usu.ac.id/mhs/221401001",
  "name": "Rina Anggraini",
  "affiliation": "FASILKOM-TI USU",
   
"knowsAbout": ["Web Semantik", "Python"] }

Event

{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "Seminar Web Semantik",
   
"startDate": "2026-09-12T09:00+07:00" ,
  "location": "Aula FASILKOM-TI USU",
  "organizer": { "@type": "Organization",
                 "name": "Prodi TI" }
}

Gunakan kurung siku bila satu properti memiliki lebih dari satu nilai.

Tanggal wajib ISO 8601 lengkap dengan zona waktu — +07:00 untuk WIB.

WEB SEMANTIK · TIF2305

13


### Catatan Pengajar

Sorot properti knowsAbout sebagai contoh nilai berbentuk ARRAY. Sorot startDate: formatnya WAJIB ISO 8601 lengkap dengan zona waktu, +07:00 untuk WIB. Tanyakan ke kelas: 'kalau seminarnya daring, properti mana yang berubah?' — jawaban: eventAttendanceMode dan location menjadi VirtualLocation. Ingatkan nama properti mengikuti schema.org dalam bahasa Inggris, tetapi nilainya boleh bahasa Indonesia.


---

## Slide 14

SEGMEN 2 · RELASI

Nesting, Array, dan Rujukan @id

Analogi basis data: @id adalah primary key, rujukan @id adalah foreign key.

Merujuk, bukan menduplikasi: bila data entitas berubah, cukup diperbarui di satu tempat.

WEB SEMANTIK · TIF2305

14


### Catatan Pengajar

Tunjukkan bahwa objek author hanya berisi @id — inilah RUJUKAN, bukan duplikasi data. Analogi basis data: @id berperan seperti primary key, rujukan @id seperti foreign key. Tekankan manfaatnya: kalau nama dosen berubah, cukup diperbarui di satu tempat dan seluruh rujukan mengikuti. Ini juga penjelasan mengapa @id sebaiknya selalu diberikan pada data yang akan ditautkan.


---

## Slide 15

03

Menyematkan & Memvalidasi

25 menit · Slide 15–18

Tujuan: menyematkan markup ke halaman HTML, memvalidasinya dengan alat resmi, dan mengenali kesalahan yang paling sering terjadi.

WEB SEMANTIK · TIF2305

15


### Catatan Pengajar

Segmen 3 — 25 menit. Bagian paling praktis; siapkan browser dan koneksi internet, serta screenshot cadangan bila internet bermasalah. Tujuan: mahasiswa dapat menyematkan markup ke halaman HTML, memvalidasinya, dan mengenali kesalahan yang paling sering terjadi.


---

## Slide 16

SEGMEN 3 · PENYEMATAN

Menyematkan JSON-LD ke Halaman HTML

HTML

<script type="application/ld+json">
  { "@context": "https://schema.org", ... }
</script>

Markup terpisah dari HTML tampilan sehingga mudah dirawat — berbeda dengan Microdata dan RDFa yang menyatu dengan tag.

Kesalahan tersering: menulis application/json — markup langsung diabaikan mesin pencari.

ATURAN GOOGLE

Markup tidak boleh mendeskripsikan konten yang tidak ada di halaman — pelanggaran pedoman spam terstruktur.

WEB SEMANTIK · TIF2305

16


### Catatan Pengajar

Tunjukkan pola embedding: script dengan type application/ld+json di dalam head. Tekankan markup TERPISAH dari HTML tampilan sehingga mudah dirawat — inilah bedanya dengan Microdata dan RDFa yang menyatu dengan tag. Bukti lapangan: buka satu situs berita atau e-commerce, tekan Ctrl+U, cari kata ld+json. Kesalahan paling sering: menulis type='application/json' sehingga markup diabaikan mesin pencari. Sebut aturan Google: markup tidak boleh mendeskripsikan konten yang tidak ada di halaman — pelanggaran pedoman spam terstruktur bisa membuat situs kehilangan rich result.


---

## Slide 17

SEGMEN 3 · VALIDASI

Alat yang Tepat untuk Tujuan yang Tepat

Pertanyaan pertama selalu: apa yang ingin Anda periksa?

search.google.com/test/rich-results — kelayakan tampil sebagai kartu hasil kaya.

validator.schema.org — kebenaran tipe dan properti terhadap kosakata.

json-ld.org/playground — triple yang benar-benar terbentuk dari markup.

Valid adalah syarat perlu, bukan syarat cukup — Google tetap menentukan sendiri kapan rich result ditampilkan.

WEB SEMANTIK · TIF2305

17


### Catatan Pengajar

Demo live: tempel markup Event dari slide 13 ke Rich Results Test, tunjukkan hasil valid. Lalu rusak sengaja satu baris — hapus satu tanda kutip — dan tunjukkan pesan errornya; mahasiswa perlu terbiasa membaca pesan error. Jelaskan beda peran: Rich Results Test menguji KELAYAKAN tampil di Google, validator.schema.org menguji KEBENARAN kosakata, Playground menunjukkan triple yang terbentuk. Ingatkan Structured Data Testing Tool yang lama sudah dipensiunkan. Jika internet bermasalah, tampilkan screenshot cadangan. Tekankan valid adalah syarat perlu, bukan syarat cukup — Google tetap menentukan sendiri kapan menampilkan rich result.


---

## Slide 18

SEGMEN 3 · LATIHAN

Temukan Lima Kesalahan

Tunjuk kesalahannya sebelum daftar jawaban dibacakan.

markup bermasalah

{
  "@context": "https://schema.org",
  "@type": "person",
  "@id": "https://usu.ac.id/dosen/idadi",
  'name': "Rina Anggraini",
  "birthDate": "12 September 2004",
  "nomorInduk": "221401001",
}

1. Tipe ditulis person — seharusnya Person.

2. Kunci memakai kutip tunggal, bukan kutip ganda.

3. Tanggal bukan ISO 8601 — seharusnya 2004-09-12.

4. nomorInduk tidak ada di schema.org — diabaikan diam-diam.

5. Koma menggantung di properti terakhir — JSON ditolak total.

WEB SEMANTIK · TIF2305

18


### Catatan Pengajar

Minta mahasiswa menemukan kesalahannya sendiri sebelum daftar di kanan dibacakan. Kesalahan pada kode: koma menggantung di properti terakhir, kutip tunggal alih-alih kutip ganda, tipe ditulis huruf kecil (person), tanggal dalam format lokal bukan ISO 8601, dan @id yang lupa diubah setelah menyalin contoh. Tekankan JSON-LD bersifat case-sensitive dan properti yang tidak dikenal schema.org diabaikan diam-diam tanpa pesan error mencolok.


---

## Slide 19

04

Perbandingan & Praktik

20 menit · Slide 19–21

Tujuan: memilih serialisasi yang tepat sesuai konteks, dan melihat JSON-LD dipakai di dunia nyata.

WEB SEMANTIK · TIF2305

19


### Catatan Pengajar

Segmen 4 — 20 menit, dilanjutkan praktik 15 menit. Tujuan: mahasiswa dapat memilih serialisasi yang tepat sesuai konteks dan menyebut contoh pemakaian JSON-LD di dunia nyata. Kalau internet bermasalah atau kelas ramai, segmen ini boleh dipotong menjadi 10 menit — cukup bacakan tabel perbandingan — karena inti penilaian ada pada segmen 1 sampai 3.


---

## Slide 20

SEGMEN 4 · PERBANDINGAN

XML vs JSON-LD vs Turtle

ASPEK

XML

JSON-LD

TURTLE

Kekuatan

Ekosistem matang: XSD, XPath, XSLT

Ringkas, familiar bagi developer, native RDF

Paling ringkas dan nyaman ditulis manusia

Kelemahan

Verbose untuk data web modern

Perlu terbiasa membaca struktur graf

Tidak berjalan langsung di browser

Konteks

Dokumen resmi, perbankan, e-Faktur, SOAP

Structured data halaman web dan API modern

Penulisan ontologi dan dataset RDF · Pertemuan 7

Tidak ada yang “paling benar” — pilihan bergantung konteks pemakaian.

WEB SEMANTIK · TIF2305

20


### Catatan Pengajar

Tekankan tidak ada yang 'paling benar' — pilihan bergantung konteks pemakaian. Untuk markup halaman web: JSON-LD. Untuk menulis ontologi: Turtle, yang akan dibahas mendalam di Pertemuan 7. Untuk pertukaran dokumen resmi dan sistem lama: XML. Jawab pertanyaan klasik: XML tidak akan mati, ia tetap dominan di dokumen resmi, perbankan, perpajakan, dan SOAP. Slide ini menutup Sub-CPMK 2 sekaligus menyiapkan mahasiswa untuk materi RDF di Pertemuan 6 dan 7.


---

## Slide 21

SEGMEN 4 · STUDI KASUS

JSON-LD di Dunia Nyata

Google Rich Results — rating, harga, dan waktu memasak tampil langsung di hasil pencarian.

Situs e-commerce — buka View Source, cari blok Product + Offer + AggregateRating.

Wikidata & DBpedia — entitas yang sama disajikan dalam JSON-LD lewat content negotiation.

Google Dataset Search — metadata Dataset membuat dataset penelitian terindeks.

Structured data bukan faktor peringkat langsung — tetapi rich result menaikkan click-through rate secara nyata.

WEB SEMANTIK · TIF2305

21


### Catatan Pengajar

Buka satu situs e-commerce Indonesia, lihat source, tunjukkan blok Product, Offer, dan AggregateRating yang nyata. Kaitkan ke Pertemuan 1: Google Knowledge Graph diberi makan sebagian oleh structured data seperti ini. Sebutkan manfaat bisnisnya konkret: structured data bukan faktor peringkat langsung, tetapi rich result meningkatkan click-through rate. Sebut juga Wikidata dan DBpedia yang menyajikan entitas yang sama dalam JSON-LD, serta Google Dataset Search yang mengindeks metadata Dataset schema.org.


---

## Slide 22

PRAKTIK MANDIRI · 15 MENIT

Misi: Buat profil_saya.jsonld

Tulis markup tentang diri Anda, validasi di validator.schema.org, unggah berkas beserta screenshot hasilnya.

kerangka · profil_saya.jsonld

{
  "@context": "https://schema.org",
  "@type": "Person",
  "@id": "https://usu.ac.id/mhs/2214010__",
  "name": "...",
  "alumniOf": {
    "@type": "CollegeOrUniversity",
    "name": "Universitas Sumatera Utara"
  },
  "knowsAbout": ["...", "..."]
}

KRITERIA PENILAIAN · 100 POIN

25

JSON sah tanpa error sintaks.

25

@context, @type, dan @id terisi benar.

20

Properti sesuai kosakata schema.org.

15

Objek bersarang alumniOf benar.

15

Lolos validator dan screenshot dilampirkan.

Tulis langsung di JSON-LD Playground agar kesalahan sintaks terlihat seketika.

WEB SEMANTIK · TIF2305

22


### Catatan Pengajar

Berkeliling saat mahasiswa mengerjakan; kesalahan paling sering adalah koma menggantung dan kutip yang salah. Anjurkan menulis langsung di JSON-LD Playground agar kesalahan sintaks langsung terlihat. Sisakan tiga menit di akhir untuk membahas satu jawaban mahasiswa di depan kelas. Ingatkan mengunggah berkas beserta screenshot hasil validasi ke folder Pertemuan 3 di LMS.


---

## Slide 23

RINGKASAN & PREVIEW

Lima Poin untuk Dibawa Pulang

01

JSON-LD adalah JSON yang membawa makna — bedanya hanya kehadiran keyword @.

02

@context memetakan kunci ke IRI; di sinilah triple terbentuk.

03

schema.org adalah kamus bersama empat mesin pencari — pilih tipe paling spesifik.

04

Markup disematkan lewat application/ld+json dan wajib mencerminkan isi halaman.

05

Valid adalah syarat perlu — selalu uji dengan validator sebelum dipublikasikan.

PERTEMUAN 4

Metadata dan Dublin Core: lima belas elemen inti DCMI, penerapannya di repositori institusi, dan pemetaan Dublin Core ↔ schema.org.

TUGAS UNTUK PEKAN DEPAN

Baca schema.org Getting Started, cari satu situs yang memakai JSON-LD lewat View Source, dan selesaikan profil_saya.jsonld beserta screenshot validasi.

WEB SEMANTIK · TIF2305

24


### Catatan Pengajar

Rekap lima poin di kiri dengan cepat — minta mahasiswa menyebutkan satu poin yang paling berkesan. Sambungkan ke Pertemuan 4: schema.org adalah kosakata untuk web, Dublin Core adalah kosakata untuk dokumen dan koleksi digital; akan dibahas juga pemetaan Dublin Core ke schema.org. Ingatkan tenggat tugas praktik dan kuis LMS sebelum kelas berikutnya, serta PR membaca schema.org Getting Started dan mencari satu situs yang memakai JSON-LD.
