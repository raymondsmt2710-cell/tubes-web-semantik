# Bahan Ajar Web Semantik 01


---

## Slide 1

PERTEMUAN 1 · TIF2305

Pengantar Web Semantik

dan peran Knowledge Graph di era AI

Mata Kuliah Web Semantik

Program Studi Teknologi Informasi

150 menit


### Catatan Pengajar

Perkenalan dosen maksimal 3 menit — mahasiswa lebih ingat kesan pertama dari materi menarik daripada CV dosen. Lakukan presensi via LMS sambil berbicara agar hemat waktu. Ajukan pertanyaan pembuka: 'Siapa yang pernah mencari sesuatu di Google dan jawabannya langsung muncul di kotak sebelah kanan tanpa perlu klik apa pun? Dari mana Google tahu jawabannya?' — jangan dijawab dulu, akan dijawab di menit ke-105 (Google Knowledge Graph). Ini menciptakan open loop yang menjaga perhatian mahasiswa sepanjang sesi.


---

## Slide 2

RENCANA SESI

Agenda Pertemuan Hari Ini

01

Pembukaan & perkenalan

0–10

05

Semantic Web Stack & konsep dasar

85–105

02

Kontrak kuliah & pengenalan RPS

10–30

06

Studi kasus: Google KG & schema.org

105–120

03

Apa itu Web Semantik?

30–55

07

Web Semantik di era AI & GraphRAG

120–135

04

Evolusi Web: 1.0 → 2.0 → 3.0

55–75

08

Tugas proyek, diskusi, kuis, penutup

135–150

—

Istirahat

75–85

WEB SEMANTIK · TIF2305

02


### Catatan Pengajar

Sampaikan agenda secara singkat sebagai peta perjalanan sesi, jangan dibaca satu per satu secara datar. Tekankan bahwa segmen 'Apa itu Web Semantik' adalah inti pertemuan dan tidak akan terburu-buru; jika waktu mepet nanti, segmen studi kasus (bukan segmen konsep inti) yang akan dipadatkan.


---

## Slide 3

SEGMEN 02 · ATURAN MAIN

Kontrak Kuliah

KEHADIRAN

Minimal 80% sebagai syarat mengikuti UAS.

KETERLAMBATAN

Ada toleransi, dengan konsekuensi yang disepakati bersama di awal.

INTEGRITAS AKADEMIK

Plagiarisme dan penyalahgunaan AI generatif memiliki kebijakan tersendiri.

KANAL KOMUNIKASI

LMS sebagai kanal resmi, grup kelas untuk koordinasi harian.

WEB SEMANTIK · TIF2305

03


### Catatan Pengajar

Jangan membacakan aturan seperti membaca dokumen legal — sampaikan dengan nada mengajak kerja sama, bukan mengancam. Tekankan bahwa kebijakan AI generatif penting dijelaskan di awal karena mata kuliah ini sendiri banyak berhubungan dengan AI. Ingatkan sekali lagi di akhir sesi (segmen penutup) agar poin ini benar-benar melekat.


---

## Slide 4

SEGMEN 02 · RPS

Peta Jalan 16 Pertemuan

01

Pengantar Web Semantik & KG

07

Serialisasi RDF & higher-order

13

Knowledge Graph, LLM & RAG

02

Format Dokumen XML

08

Ujian Tengah Semester

14

Presentasi Tugas Proyek (1)

03

JSON-LD & Structured Data

09

SPARQL dasar: tell & ask

15

Presentasi Tugas Proyek (2)

04

Metadata & Dublin Core

10

SPARQL SELECT Query

16

Ujian Akhir Semester

05

Ontology dasar & arsitektur

11

CONSTRUCT Query & hirarki

06

RDF dasar: model triple

12

Inferensi & Reasoning

Menulis data agar mesin paham (2–5) → menyimpan pengetahuan (6–7) → bertanya kepada pengetahuan (9–12) → memakainya bersama AI (13).

WEB SEMANTIK · TIF2305

04


### Catatan Pengajar

Jangan membacakan tabel baris per baris. Ceritakan sebagai narasi: kita mulai dari cara menulis data supaya mesin paham (minggu 2-5), lalu cara menyimpan pengetahuan itu (minggu 6-7), lalu cara bertanya kepada pengetahuan itu (minggu 9-12), dan diakhiri dengan bagaimana semua ini dipakai bersama AI hari ini (minggu 13). Tugas Proyek mulai dipikirkan sejak sekarang meski dibentuk resmi di minggu ke-5.


---

## Slide 5

SEGMEN 02 · PENILAIAN

Komponen Penilaian

5%

Tugas

5%

Quiz

50%

Tugas Proyek kelompok

20%

Ujian Tengah Semester

20%

Ujian Akhir Semester

Tugas Proyek adalah komponen terbesar. Kelompok dibentuk resmi di minggu ke-5, tetapi mulailah memikirkan topik sejak hari ini.

WEB SEMANTIK · TIF2305

05


### Catatan Pengajar

Tekankan dengan jelas bahwa Tugas Proyek (40%) adalah komponen terbesar, lebih besar dari UTS dan UAS masing-masing. Ini penting supaya mahasiswa tidak menyepelekannya dan mulai memikirkan topik sejak pertemuan pertama, walau kelompok baru dibentuk resmi minggu ke-5.


---

## Slide 6

SUB-CPMK1

Capaian Pembelajaran

Mahasiswa akan dapat menjelaskan dan memahami Web Semantik.

1

Menjelaskan konsep dasar Web Semantik dengan kalimatnya sendiri.

2

Menjelaskan perkembangan teknologi Web 1.0 → 2.0 → 3.0.

3

Menyebutkan lapisan Semantic Web Stack beserta fungsinya.

4

Menjelaskan relevansi Web Semantik terhadap perkembangan AI terkini.

WEB SEMANTIK · TIF2305

06


### Catatan Pengajar

Sub-CPMK1 adalah fondasi bagi seluruh topik pertemuan berikutnya — sampaikan ini secara eksplisit supaya mahasiswa paham mengapa pertemuan pertama ini penting meski belum ada coding. Empat indikator ini persis yang akan diujikan di kuis LMS pada akhir sesi (segmen 8).


---

## Slide 7

SEGMEN 03 · TITIK BERANGKAT

Mesin Tidak Memahami Makna

“Java memiliki populasi lebih dari 150 juta jiwa.”

Yang tidak diketahui komputer:

“Java”

Sebuah pulau — bukan bahasa pemrograman, bukan merek kopi.

“populasi”

Properti yang berlaku pada wilayah geografis.

“150 juta jiwa”

Nilai numerik dengan satuan penduduk.

Web tradisional menyimpan dokumen, bukan makna.

WEB SEMANTIK · TIF2305

07


### Catatan Pengajar

Mulai dari masalah, bukan dari definisi — tuliskan kalimat 'Java memiliki populasi lebih dari 150 juta jiwa' di papan tulis. Tanyakan ke kelas: 'Apa yang dipahami komputer dari kalimat ini?' Biarkan mahasiswa menjawab dulu sebelum menjelaskan tiga poin ambiguitas (Java sebagai pulau/bahasa pemrograman/kopi, populasi sebagai properti geografis, 150 juta sebagai nilai numerik berunit).


---

## Slide 8

SEGMEN 03 · DEFINISI

Apa itu Web Semantik?

DEFINISI

Perluasan dari World Wide Web yang memungkinkan data di web memiliki makna terdefinisi secara formal, sehingga dapat diproses, dihubungkan, dan disimpulkan secara otomatis oleh mesin.

Perluasan

Tidak menggantikan web yang ada, tetapi menambahkan lapisan makna di atasnya.

Makna terdefinisi formal

Makna dinyatakan eksplisit lewat standar: URI, RDF, ontology — bukan ditebak dari konteks.

Diproses otomatis

Mesin dapat menarik kesimpulan baru yang tidak pernah ditulis secara eksplisit.

WEB SEMANTIK · TIF2305

08


### Catatan Pengajar

Bacakan definisi pelan-pelan, lalu bedah tiga kata kuncinya satu per satu: 'perluasan' (bukan pengganti web lama), 'makna terdefinisi formal' (bukan ditebak dari konteks seperti manusia, tapi dinyatakan eksplisit), dan 'diproses otomatis' (mesin bisa menyimpulkan hal baru). Kaitkan kembali ke masalah 'Java' pada slide sebelumnya sebagai contoh konkret dari setiap kata kunci.


---

## Slide 9

SEGMEN 03 · LATAR SEJARAH

Visi Tim Berners-Lee

1989–1991

Menemukan World Wide Web di CERN.

1998

Menulis Semantic Web Road Map dan What the Semantic Web can represent .

2001

Artikel di Scientific American memperkenalkan visi ini ke publik luas.

Web seharusnya menjadi ruang data global — bukan sekadar kumpulan dokumen untuk dibaca manusia.

WEB SEMANTIK · TIF2305

09


### Catatan Pengajar

Berikan konteks historis singkat: orang yang sama yang menemukan web (1989-1991) juga yang menggagas Semantic Web hanya beberapa tahun kemudian. Ini menunjukkan bahwa visi ini bukan tren baru, melainkan bagian dari rencana besar sejak awal internet modern. Artikel Scientific American 2001 bisa disebutkan sebagai bacaan tambahan opsional bagi mahasiswa yang tertarik.


---

## Slide 10

SEGMEN 03 · PERBANDINGAN

Web Dokumen vs Web Data

ASPEK

WEB TRADISIONAL

WEB SEMANTIK

Unit dasar

Dokumen (halaman HTML)

Data (pernyataan / triple)

Tautan

Link antar halaman

Link antar entitas dengan makna

Pembaca utama

Manusia

Mesin — dan manusia

Contoh pertanyaan

“Halaman apa yang memuat kata X?”

“Entitas apa yang punya properti X bernilai Y?”

Hasil pencarian

Daftar tautan

Jawaban langsung dan terstruktur

WEB SEMANTIK · TIF2305

10


### Catatan Pengajar

Gunakan tabel ini untuk merangkum perbedaan setelah contoh 'Java' dan definisi tadi. Baris 'Hasil pencarian' bisa dikaitkan lagi ke pertanyaan pembuka soal Google — nanti dijawab tuntas di segmen studi kasus.


---

## Slide 11

SEGMEN 03 · ILUSTRASI

Inferensi Otomatis

Medan

terletakDi →

Sumatera Utara

Sumatera Utara

terletakDi →

Indonesia

terletakDi bersifat transitif

Medan

terletakDi →

Indonesia

FAKTA BARU — TIDAK PERNAH DITULIS

“Apakah komputer bisa menyimpulkan bahwa Medan terletak di Indonesia?”

Bisa — karena kita telah memberi tahu mesin bahwa relasi terletakDi bersifat transitif. Inilah yang disebut inferensi.

WEB SEMANTIK · TIF2305

11


### Catatan Pengajar

Tuliskan tiga pernyataan ini di papan tulis dengan panah, lalu ajukan pertanyaannya ke kelas dan beri waktu mereka berpikir sebelum dijawab. Tekankan bahwa kemampuan menyimpulkan fakta baru yang tidak pernah ditulis eksplisit adalah salah satu kekuatan terbesar Web Semantik dibanding basis data biasa.


---

## Slide 12

SEGMEN 04 · GARIS WAKTU

Evolusi Web: Dari Dokumen ke Data

Web 1.0

± 1991–2004 · read-only

HTML statis, hampir tanpa basis data dinamis.

Pengguna sebagai konsumen pasif.

Contoh: situs perusahaan sebagai brosur digital.

Seperti perpustakaan.

Web 2.0

± 2004–kini · read-write

AJAX, API, aplikasi web interaktif.

Pengguna sebagai prosumer.

Masalah: data melimpah tetapi terkurung dalam silo platform.

Seperti kafe.

Web 3.0

visi 2001 · read-write-execute

URI, RDF, OWL, SPARQL, Knowledge Graph.

Pengguna berkolaborasi dengan agen cerdas.

Contoh: Google Knowledge Graph, Wikidata.

Seperti asisten pribadi.

WEB SEMANTIK · TIF2305

12


### Catatan Pengajar

Jelaskan tiga era secara berurutan dengan analoginya masing-masing: Web 1.0 seperti perpustakaan (boleh baca, tidak boleh tulis), Web 2.0 seperti kafe (semua boleh bicara), Web 3.0 seperti asisten pribadi yang benar-benar paham maksud pertanyaan. Tekankan masalah di Web 2.0 (silo data) sebagai jembatan ke pentingnya Web Semantik. Tutup dengan pertanyaan pemantik: 'Menurut kalian, apakah kita sekarang sudah di Web 3.0, atau masih Web 2.0 yang ditempeli AI?' — beri 2-3 menit diskusi terbuka.


---

## Slide 13

SEGMEN 04 · CATATAN PENTING

Web 3.0 Bukan Web3

Dua istilah yang mirip namanya, tetapi memecahkan masalah yang sama sekali berbeda.

DIPELAJARI DI MATA KULIAH INI

Web 3.0 = Semantic Web

Makna asli menurut Berners-Lee: data di web diberi makna formal agar dapat diproses mesin.

TOPIK YANG BERBEDA

Web3 = Blockchain

Web terdesentralisasi berbasis blockchain: fokus pada kepemilikan, bukan pada makna data.

WEB SEMANTIK · TIF2305

13


### Catatan Pengajar

Ini poin yang sering bikin mahasiswa bingung, jadi luruskan secara eksplisit dan jangan terburu-buru. Web 3.0 (istilah Berners-Lee, tentang makna data) dan Web3 (istilah komunitas blockchain, tentang kepemilikan terdesentralisasi) kebetulan mirip namanya tapi memecahkan masalah yang sangat berbeda. Ini juga salah satu pertanyaan yang paling sering muncul di sesi tanya jawab, jadi baik untuk diantisipasi di sini.


---

## Slide 14

SEGMEN 05 · ARSITEKTUR

Semantic Web Stack

Fondasi (identitas) → struktur (fakta) → kecerdasan (kesimpulan dan kepercayaan).

7

Trust

Keandalan dan asal-usul data

—

6

Proof / Logic

Pembuktian dan aturan

Minggu 12

5

Ontology — RDFS, OWL

Kosakata dan hubungan antar konsep

Minggu 5, 12

4

Query — SPARQL

Bertanya kepada data

Minggu 9–11

3

RDF

Model data berbentuk triple

Minggu 6–7

2

XML / JSON-LD / Turtle

Format serialisasi

Minggu 2–3

1

URI / IRI dan Unicode

Identitas dan karakter

Minggu 1, 6

WEB SEMANTIK · TIF2305

14


### Catatan Pengajar

Gambarkan susunan ini di papan tulis dari bawah ke atas sambil menyampaikan tabel. Ini adalah 'peta mental' yang akan terus dirujuk sepanjang semester — sebutkan secara eksplisit minggu keberapa tiap lapisan akan dibahas mendalam. Jangan masuk ke sintaks apa pun di sini, cukup kenalkan istilah dan fungsinya; kalau ada yang bertanya detail teknis, arahkan ke minggu yang relevan.


---

## Slide 15

SEGMEN 05 · FONDASI

URI dan Triple

URI — nama unik global

Identitas untuk apa pun: orang, tempat, konsep, bahkan relasi. Dua sistem di dua negara berbeda bisa yakin sedang membicarakan hal yang sama.

http://www.wikidata.org/entity/Q3757

Pulau Jawa — tidak ambigu lagi.

Triple — satuan pengetahuan terkecil

Medan

SUBJEK

terletakDi

PREDIKAT

Sumatera Utara

OBJEK

Kumpulan triple yang saling terhubung membentuk graf pengetahuan .

WEB SEMANTIK · TIF2305

15


### Catatan Pengajar

URI menyelesaikan masalah ambiguitas 'Java' dari slide sebelumnya — dengan URI, dua sistem di dua negara berbeda bisa yakin sedang membicarakan hal yang sama. Untuk triple, gambarkan sebagai simpul dan panah di papan tulis (bukan hanya teks) — representasi visual ini biasanya langsung membuat konsepnya 'klik' bagi mahasiswa. Tutup dengan menjelaskan bahwa kumpulan triple yang saling terhubung itulah yang disebut knowledge graph.


---

## Slide 16

SEGMEN 06 · STUDI KASUS · DEMO LANGSUNG

Google Knowledge Graph

01

Cari Tim Berners-Lee.

02

Tunjukkan Knowledge Panel: foto, tanggal lahir, penghargaan, karya.

03

Informasi ini dirakit dari basis pengetahuan terstruktur — bukan disalin dari satu halaman.

04

Klik entitas terkait untuk menunjukkan keterhubungannya.

“Things, not strings.”

Slogan Google saat peluncuran, 2012

Berisi miliaran fakta tentang entitas dan relasi antar entitas. Inilah jawaban dari pertanyaan pembuka sesi ini.

WEB SEMANTIK · TIF2305

16


### Catatan Pengajar

Lakukan demo langsung: buka Google, cari 'Tim Berners-Lee', tunjukkan Knowledge Panel di sisi kanan. Tekankan bahwa informasi ini dirakit dari basis pengetahuan terstruktur, bukan diambil dari satu halaman. Ini adalah jawaban dari pertanyaan pembuka di slide 1 — kaitkan kembali secara eksplisit ('open loop' yang dibuka di awal sesi ditutup di sini). Jika internet bermasalah, gunakan tangkapan layar cadangan.


---

## Slide 17

SEGMEN 06 · STUDI KASUS · DEMO LANGSUNG

schema.org & Structured Data

JSON-LD

{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Tim Berners-Lee",
  "birthDate": "1955-06-08",
  "award": "Turing Award"
}

Kosakata bersama yang disepakati Google, Microsoft, Yahoo, dan Yandex sejak 2011.

JSON-LD adalah format serialisasi yang paling direkomendasikan Google — dibahas mendalam di minggu ke-3.

Manfaat praktis: rich snippet di hasil pencarian — rating, harga, waktu memasak.

Contoh Web Semantik yang paling langsung bisa dipraktikkan pada Tugas Proyek Anda.

Hasil rich snippet dari data terstruktur.

schema.org

search.google.com/test/rich-results

query.wikidata.org

WEB SEMANTIK · TIF2305

17


### Catatan Pengajar

Demo langsung: buka schema.org, tunjukkan daftar tipe entitas. Lalu buka situs resep/e-commerce populer, lihat page source, cari blok script application/ld+json. Tempelkan URL ke search.google.com/test/rich-results untuk menunjukkan hasil parsing-nya. Tekankan ini contoh Web Semantik yang paling mudah langsung dipraktikkan mahasiswa di Tugas Proyek mereka nanti.


---

## Slide 18

SEGMEN 07 · ERA AI

Keterbatasan Large Language Model

Sangat mahir berbahasa, tetapi memiliki kelemahan mendasar.

Halusinasi

Menghasilkan pernyataan yang terdengar meyakinkan namun keliru.

Sumber tidak jelas

Sulit melacak dari mana sebuah klaim berasal.

Pengetahuan membeku

Terbatas pada data pelatihan sampai tanggal tertentu.

Sulit diaudit

Menjadi masalah serius pada domain kritis: kesehatan, hukum, keuangan.

WEB SEMANTIK · TIF2305

18


### Catatan Pengajar

LLM seperti ChatGPT, Claude, dan Gemini sangat mahir berbahasa tetapi punya kelemahan mendasar ini. Kalau memungkinkan, tunjukkan satu contoh nyata jawaban AI yang keliru (halusinasi) untuk membuat masalahnya terasa konkret bagi mahasiswa, bukan sekadar teori.


---

## Slide 19

SEGMEN 07 · PERBANDINGAN

Knowledge Graph sebagai Penyeimbang

Keduanya tidak bersaing — kekuatan yang satu menutup kelemahan yang lain.

ASPEK

LARGE LANGUAGE MODEL

KNOWLEDGE GRAPH

Kekuatan

Bahasa alami, generalisasi

Fakta presisi, relasi eksplisit

Sumber

Sulit dilacak

Setiap triple punya asal-usul

Pembaruan

Perlu pelatihan ulang

Cukup tambah atau ubah triple

Audit

Sulit

Mudah ditelusuri

WEB SEMANTIK · TIF2305

19


### Catatan Pengajar

Gunakan tabel ini untuk menunjukkan bahwa LLM dan Knowledge Graph punya kekuatan yang saling melengkapi, bukan bersaing. Ini jembatan langsung menuju konsep GraphRAG di slide berikutnya.


---

## Slide 20

SEGMEN 07 · SINTESIS

GraphRAG: Knowledge Graph Bertemu LLM

Pertanyaan pengguna

→

Ambil sub-graf dari Knowledge Graph

→

LLM menyusun jawaban

→

Akurat, dapat dijelaskan, dapat diverifikasi

Dari RAG ke GraphRAG

RAG mengambil potongan teks; GraphRAG mengambil sub-graf. Relasi berjenjang — “siapa saja rekan kerja dari mahasiswa bimbingan Profesor X?” — sulit dijawab dengan pencarian teks biasa.

Konteks industri 2025

ISWC 2025 mengangkat integrasi Knowledge Graph dan LLM sebagai tema utama, termasuk GraphRAG dan NL2SPARQL. Gartner merekomendasikan adopsi ontology dan knowledge graph untuk mendukung penggunaan AI.

WEB SEMANTIK · TIF2305

20


### Catatan Pengajar

Ini segmen paling ampuh menjawab pertanyaan 'apakah materi 2001 ini masih relevan?' — sampaikan dengan antusias. Jelaskan bahwa International Semantic Web Conference (ISWC) 2025 menjadikan integrasi Knowledge Graph dan LLM sebagai tema utama, dengan istilah GraphRAG dan NL2SPARQL. Sebutkan juga bahwa Gartner 2025 merekomendasikan adopsi ontology dan knowledge graph untuk kebutuhan AI di industri.


---

## Slide 21

SEGMEN 07 · RELEVANSI

Peluang Karier

Peran nyata di industri yang membutuhkan kompetensi ini.

01

Knowledge Engineer

Merancang ontology dan model pengetahuan domain.

02

Data Architect (graph)

Menata arsitektur data berbasis graf di perusahaan.

03

AI Engineer

Membangun sistem RAG dan GraphRAG.

04

Semantic Data Analyst

Sektor kesehatan, keuangan, dan pemerintahan.

WEB SEMANTIK · TIF2305

21


### Catatan Pengajar

Sebutkan peran-peran nyata ini untuk memotivasi mahasiswa bahwa kompetensi mata kuliah ini punya jalur karier konkret, bukan sekadar materi akademis. Bisa dikaitkan dengan Tugas Proyek semester sebagai kesempatan awal membangun portofolio di bidang ini.


---

## Slide 22

SEGMEN 08 · TUGAS PROYEK

Tugas Proyek Semester

50%

nilai akhir

3–4

orang per kelompok

Luaran: aplikasi sederhana berbasis Web Semantik beserta laporan.

Minggu 5

Pembentukan kelompok dan pemilihan topik

Minggu 13

Konsultasi progres

Minggu 14–15

Presentasi dan pengumpulan laporan

CONTOH TOPIK

Knowledge graph untuk domain tertentu: perpustakaan kampus, pariwisata daerah, kuliner lokal.

Aplikasi pencarian berbasis SPARQL dengan endpoint publik seperti Wikidata.

Penerapan markup schema.org pada sebuah situs dan pengukuran dampaknya.

Prototipe GraphRAG sederhana untuk menjawab pertanyaan dari sebuah knowledge graph.

WEB SEMANTIK · TIF2305

22


### Catatan Pengajar

Minta mahasiswa mulai memikirkan kelompok dan topik sejak sekarang walaupun pembentukan resminya baru minggu ke-5. Berikan contoh topik konkret agar tidak terasa abstrak — bisa dikaitkan ke studi kasus Google Knowledge Graph dan schema.org yang baru saja dibahas.


---

## Slide 23

SEGMEN 08 · PENUTUP

Web Semantik membuat web dapat dipahami mesin — dan menjadi fondasi bagi AI yang akurat serta dapat dipercaya.

DISKUSI

Sebutkan satu aplikasi yang Anda pakai hari ini — apakah ia memakai prinsip Web Semantik? Mengapa?

KUIS LMS

5 soal pilihan berganda. Benar bernilai 2, salah 0. Nilai tertinggi 10, batas terendah 6.

PERTEMUAN BERIKUTNYA

Format Dokumen XML. Tugas baca: A Semantic Web Primer Bab 1.

WEB SEMANTIK · TIF2305

23


### Catatan Pengajar

Beri kesempatan 2-3 mahasiswa menjawab pertanyaan diskusi, apresiasi setiap jawaban termasuk yang keliru — pertemuan pertama menentukan apakah kelas akan aktif sepanjang semester. Buka kuis LMS (5 soal, benar=2, salah=0, nilai tertinggi 10, batas lulus 6). Tutup dengan mengingatkan tugas baca dan preview singkat minggu depan.
