# Bahan Ajar Web Semantik 05


---

## Slide 1

PERTEMUAN 5 · TIF2305 · SUB-CPMK 3

Ontology Dasar & Arsitektur

Dari data terstruktur menuju pengetahuan mesin: class, property, individual, axiom, dan Semantic Web Layer Cake

Mata Kuliah Web Semantik

Program Studi Teknologi Informasi

150 menit


### Catatan Pengajar

Slide pembuka. Sapa mahasiswa dan ingatkan minggu lalu kita membahas Metadata dan Dublin Core. Sampaikan bahwa hari ini kita naik satu tingkat: dari sekadar label deskriptif ke model pengetahuan — yaitu ontology. Perkenalkan juga bahwa ini pertemuan pembentukan kelompok Tugas Proyek. Alokasi total 150 menit.


---

## Slide 2

RENCANA SESI

Alur Pertemuan Hari Ini

01

Pembuka dan jembatan dari Pertemuan 4

10 menit

02

Ontology dasar: definisi, anatomi, hirarki, property

35 menit

03

Semantic Web Layer Cake — walkthrough tiap lapis

35 menit

04

Preview Protégé dan walkthrough antarmuka

25 menit

05

Pembentukan kelompok Tugas Proyek dan template proposal

25 menit

06

Diskusi kelas, kuis LMS, dan ringkasan

20 menit

WEB SEMANTIK · TIF2305

02


### Catatan Pengajar

Bacakan enam segmen dengan cepat. Tekankan bahwa segmen 05 (pembentukan kelompok) adalah aksi konkret hari ini: mahasiswa harus keluar dari kelas sudah memiliki nama kelompok dan topik proyek. Kuis di akhir dikerjakan mandiri via LMS.


---

## Slide 3

SUB-CPMK 3 · BAGIAN 2

Capaian Pembelajaran

Empat indikator, masing-masing dengan cara pengecekan yang berbeda.

01

Mendefinisikan

Ontology beserta empat kata kunci definisi Studer.

Dicek via kuis

02

Membedakan

Class, individual, property, dan axiom dalam satu hirarki.

Mini-exercise pohon kelas

03

Menjelaskan

Delapan lapis arsitektur Web Semantik menurut W3C.

Kuis dan diskusi kelas

04

Mengenali

Antarmuka Protégé sebagai persiapan minggu 6 dan 7.

Walkthrough di kelas

Menjelaskan arsitektur berbeda dengan menerapkannya. Penerapan dimulai minggu 6 lewat praktik RDF.

WEB SEMANTIK · TIF2305

03


### Catatan Pengajar

Kaitkan indikator dengan aktivitas: indikator 1 dicek via kuis, indikator 2 lewat mini-exercise pohon kelas, indikator 4 lewat walkthrough Protégé. Ingatkan bahwa menjelaskan arsitektur berbeda dengan menerapkan; penerapan dilakukan mulai minggu 6 (RDF praktik).


---

## Slide 4

RECAP · JEMBATAN

Dari Data tentang Data ke Model tentang Makna

Metadata adalah kata sifat

dc:creator hanya tahu bahwa ada seseorang bernama Ida.

Ontology adalah gramatika

Ida adalah Lecturer, Lecturer adalah Person, dan Lecturer bisa teaches Course.

WEB SEMANTIK · TIF2305

04


### Catatan Pengajar

Poin utama: metadata itu kata sifat; ontology itu gramatika. Contohkan: dc:creator hanya tahu ada seseorang bernama Ida; ontology tahu bahwa Ida adalah Lecturer, Lecturer adalah Person, dan Lecturer bisa teaches Course. Reasoner bisa menyimpulkan Ida adalah Person tanpa kita tulis eksplisit. Pertanyaan pemantik: kalau Dublin Core sudah ada, kenapa Google dan Facebook membangun ontology sendiri?


---

## Slide 5

01

Ontology Dasar

35 menit · Slide 6–9

Tujuan: mendefinisikan ontology, membedakan class, property, individual, dan axiom, serta membaca hirarki subclass.

WEB SEMANTIK · TIF2305

05


### Catatan Pengajar

Divider singkat 30 detik. Ajukan pertanyaan pemantik: kalau kita sudah punya Dublin Core, kenapa masih butuh model yang lebih kompleks? Biarkan satu atau dua mahasiswa merespon sebelum lanjut.


---

## Slide 6

SEGMEN 1 · DEFINISI

Empat Pilar Fondasi Makna

Definisi · Studer et al. 1998 — Ontology adalah spesifikasi explicit dan formal dari sebuah conceptualization yang shared.

WEB SEMANTIK · TIF2305

06


### Catatan Pengajar

Tekankan bahwa definisi Gruber jadi rujukan hampir semua textbook Web Semantik. Berikan analogi: explicit dan formal seperti UML class diagram; shared seperti standar bersama, bukan dokumen internal; conceptualization seperti mental model domain tertentu, misalnya domain perpustakaan atau kedokteran.


---

## Slide 7

SEGMEN 1 · ANATOMI

Empat Komponen Pembentuk Ontology

Analogi database membantu, tetapi tidak akurat: OWL bersifat open-world dan mendukung inferensi otomatis.

Class

Konsep abstrak, misalnya Person. ≈ tabel

Individual

Instance konkret, misalnya Budi. ≈ baris

Property

Relasi atau atribut antar konsep. ≈ kolom

Axiom

Aturan logis yang mengikat model. ≈ constraint

WEB SEMANTIK · TIF2305

07


### Catatan Pengajar

Runut satu per satu. Analogi Class sama dengan tabel, Individual sama dengan baris, Property sama dengan kolom, Axiom sama dengan trigger dan constraint. Tetapi tekankan: analogi database tidak selalu tepat, karena OWL open-world dan mendukung inferensi.


---

## Slide 8

SEGMEN 1 · HIRARKI

Satu Baris Subclass, Satu Kesimpulan Gratis

:Student rdfs:subClassOf :Person . :andi_s001 rdf:type :Student .

Reasoner menyimpulkan sendiri bahwa :andi_s001 juga bertipe :Person — fakta itu tidak pernah kita tulis.

WEB SEMANTIK · TIF2305

08


### Catatan Pengajar

Jelaskan pohon: Person adalah superclass; Student dan Lecturer adalah subclass. andi:s001 adalah instance Student, budi:l010 adalah instance Lecturer. Berkat rdfs:subClassOf, reasoner otomatis menyimpulkan andi:s001 juga bertipe Person. Ini contoh inferensi murah yang membedakan ontology dari sekadar tabel.


---

## Slide 9

SEGMEN 1 · MISKONSEPSI

rdfs:domain Bukan Validasi

Yang dikira mahasiswa

Domain menolak data yang tipenya salah, seperti constraint di database.

Yang sebenarnya terjadi

Jika X mengajar Y , reasoner menyimpulkan X pasti seorang Dosen. Tidak ada yang ditolak.

WEB SEMANTIK · TIF2305

09


### Catatan Pengajar

Ini konsep yang paling sering keliru: banyak mahasiswa mengira domain dan range membatasi input. Sebenarnya di OWL open-world, keduanya memberi tahu reasoner tipe — bukan menolak. Peringatkan hal ini agar tidak salah paham saat praktik nanti.


---

## Slide 10

02

Semantic Web Layer Cake

35 menit · Slide 11–14

Delapan lapis arsitektur menurut W3C. Setiap lapis dibangun di atas lapis sebelumnya dan tidak berdiri sendiri.

WEB SEMANTIK · TIF2305

10


### Catatan Pengajar

Segmen ini menjelaskan gambar besar arsitektur Web Semantik. Ingatkan bahwa setiap lapis dibangun di atas lapis sebelumnya dan tidak berdiri sendiri.


---

## Slide 11

SEGMEN 2 · ARSITEKTUR

Arsitektur Web Semantik (W3C)

Ontology (OWL) duduk tepat di atas RDF: ia menambahkan logika di atas data relasional sederhana, dan menjadi fondasi bagi Query, Rules, Proof, hingga Trust.

WEB SEMANTIK · TIF2305

11


### Catatan Pengajar

Bahas dari bawah ke atas. Kaitkan setiap lapis dengan minggu-minggu sebelumnya: URI minggu 1, XML minggu 2, JSON-LD minggu 3, RDF akan dibahas minggu 6. Beri tahu bahwa ontology adalah kue lapis yang jadi fokus hari ini dan minggu depan. Gambar Layer Cake ada banyak versi; untuk kelas ini pakai versi delapan lapis yang umum dipakai di textbook Antoniou.


---

## Slide 12

SEGMEN 2 · PETA JALAN

Delapan Lapis dan Minggu Kuliahnya

LAPIS

PERAN

DIBAHAS

Trust

Kepercayaan terhadap sumber dan hasil penalaran

Minggu 13

Proof

Jejak yang menjelaskan bagaimana kesimpulan diperoleh

Minggu 12

Rules

Aturan inferensi tambahan di luar OWL

Minggu 12

Query

Pengambilan data dari graf dengan SPARQL

Minggu 9–11

Ontology

Makna dan relasi antar konsep lewat RDFS dan OWL

Hari ini

RDF

Model data triple: subjek, predikat, objek

Minggu 6–7

XML

Sintaks pertukaran dokumen antar sistem

Minggu 2

URI / IRI

Identitas unik untuk setiap sumber daya di web

Minggu 1

WEB SEMANTIK · TIF2305

12


### Catatan Pengajar

Tabel ini sekaligus jadi peta jalan kuliah: minggu 6 dan 7 untuk RDF, 9 sampai 11 untuk SPARQL, 12 untuk reasoning, 13 untuk aplikasi Trust via GraphRAG. Ingatkan mahasiswa untuk memfoto tabel ini karena akan sering dirujuk.


---

## Slide 13

SEGMEN 2 · NILAI TAMBAH

Kenapa RDFS Saja Tidak Cukup

RDFS menyediakan fungsi dasar

subClassOf · subPropertyOf · domain · range

OWL menambah operator penalaran

equivalentClass · disjointWith · cardinality · someValuesFrom

Google memakai schema.org (ontology) di atas JSON-LD (serialisasi) di atas URL. Semua lapis bekerja bersama.

WEB SEMANTIK · TIF2305

13


### Catatan Pengajar

Poin utama: ontology tidak berdiri sendiri, ia butuh URI dan RDF di bawahnya serta SPARQL dan Rules di atasnya. Beri contoh nyata: mesin pencari Google menggunakan schema.org (ontology) di atas JSON-LD (serialisasi) di atas URL. Semua lapis bekerja bersama.


---

## Slide 14

SEGMEN 2 · STUDI KASUS

Reuse Before Reinvent

Tiga vocabulary yang sudah matang dan dipakai luas di dunia nyata.

FOAF

Jejaring sosial

Mendeskripsikan orang, akun, dan relasi antar-manusia. Kosakata paling awal yang diadopsi luas.

schema.org

Data terstruktur web

Dipakai mesin pencari untuk memahami produk, artikel, acara, dan resep di halaman web.

SNOMED CT

Terminologi medis

Ratusan ribu konsep klinis yang dipakai sistem rekam medis di banyak negara.

Cari dulu di LOV (Linked Open Vocabularies) atau BioPortal. Bangun sendiri hanya bagian yang benar-benar spesifik domain Anda. Tugas Proyek wajib menyebut minimal satu vocabulary eksternal.

WEB SEMANTIK · TIF2305

14


### Catatan Pengajar

Sampaikan bahwa mahasiswa tidak perlu membangun ontology dari nol — hampir selalu ada vocabulary siap pakai yang bisa di-reuse. Prinsip: reuse before reinvent. Tugas Proyek nanti wajib menyebutkan minimal satu vocabulary eksternal yang dipakai.


---

## Slide 15

03

Preview Protégé

25 menit · Slide 16–17

Walkthrough antarmuka dan alur kerja. Belum praktik — praktik mandiri dimulai setelah kelas.

WEB SEMANTIK · TIF2305

15


### Catatan Pengajar

Segmen ini walkthrough saja — belum praktik. Tayangkan aplikasi Protégé atau screenshot. Fokus perkenalkan bagian antarmuka.


---

## Slide 16

SEGMEN 3 · ANTARMUKA

Enam Tab yang Perlu Dikenali

Active Ontology

IRI, versi, dan import ontology yang sedang dibuka.

Entities

Semua entitas dalam satu pohon gabungan.

Classes

Hirarki class dan tempat mendefinisikan subclass.

Object Properties

Relasi antar individual, lengkap dengan domain dan range.

Data Properties

Atribut bernilai literal seperti angka dan teks.

Individuals

Instance konkret beserta pernyataan tipenya.

Unduh Protégé Desktop 5.6.x di protege.stanford.edu. Alternatif berbasis browser: webprotege.stanford.edu.

WEB SEMANTIK · TIF2305

16


### Catatan Pengajar

Kalau memungkinkan, buka aplikasi Protégé di layar dan tunjuk setiap tab. Jika tidak, tayangkan screenshot dari Protégé Wiki. Beritahu link download: protege.stanford.edu — versi Desktop 5.6.x. Alternatif jika Desktop tidak jalan: WebProtégé di webprotege.stanford.edu, perlu akun Google atau email.


---

## Slide 17

SEGMEN 3 · ALUR KERJA

Enam Langkah Membangun Ontology

Enam langkah ini adalah versi ringkas. Versi lengkapnya ada di Ontology Development 101 (Noy & McGuinness, Stanford) — bacaan wajib minggu 7.

WEB SEMANTIK · TIF2305

17


### Catatan Pengajar

Alur ini sengaja dibuat enam langkah sederhana — tidak semua best practice ada di sini. Beritahu bahwa versi lengkap ada di Ontology Development 101 (Noy dan McGuinness, Stanford) yang jadi bacaan wajib minggu 7.


---

## Slide 18

SEGMEN 5 · TUGAS

Praktik Mandiri M5 → M6

Lima aspek penilaian formatif, dikumpulkan sebelum Pertemuan 6.

20%

Instal Protégé Desktop dan buka berkas contoh pizza.owl

20%

Ekspor ke dua format: Turtle dan RDF/XML, lalu bandingkan keduanya

40%

Bangun ontology mini bertema Kampus dengan hirarki yang logis

10%

Lampirkan screenshot tab Classes dan tab Individuals dengan resolusi cukup

10%

Ketepatan waktu pengumpulan sebelum tenggat

Protégé Desktop membutuhkan Java 11 ke atas. Jika instalasi bermasalah, gunakan WebProtégé di webprotege.stanford.edu — fungsinya mirip dan berjalan di browser.

WEB SEMANTIK · TIF2305

21


### Catatan Pengajar

Jelaskan bahwa praktik ini melatih kesiapan sebelum masuk RDF. Sarankan pakai laptop dengan Java 11 ke atas; jika kesulitan instal, ada versi web WebProtégé sebagai alternatif. Praktik dikumpulkan sebelum pertemuan 6.


---

## Slide 19

PENUTUP

Rekapitulasi & Misi Minggu Depan

01

Ontology adalah definisi ditambah relasi — lebih dari sekadar taksonomi is-a.

02

Ia berdiri di atas RDF di dalam Layer Cake, bukan menggantikannya.

03

Kelompok proyek terbentuk hari ini. Minggu depan: RDF dengan Python dan rdflib.

WEB SEMANTIK · TIF2305

24


### Catatan Pengajar

Tutup kelas dengan ringkasan cepat tiga poin utama: ontology adalah definisi ditambah relasi, ontology berdiri di atas RDF di dalam Layer Cake, dan kelompok proyek terbentuk hari ini. Beri semangat: minggu depan kita mulai coding dengan Python. Bacaan wajib: Antoniou Bab 3.1 sampai 3.3.
