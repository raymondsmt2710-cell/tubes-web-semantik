# Bahan Ajar Web Semantik 06


---

## Slide 1

PERTEMUAN 6 · TIF2305 · SUB-CPMK 4 (BAGIAN 1)

RDF Dasar: Model Triple dan Identifier

Dari model konseptual ke model data: subject, predicate, object, URI/IRI, literal, blank node, dan operasi dasar rdflib di Python.

Mata Kuliah Web Semantik

Program Studi Teknologi Informasi

150 menit


### Catatan Pengajar

Slide pembuka. Sapa mahasiswa dan ingatkan minggu lalu kita menutup dengan pembentukan kelompok Tugas Proyek dan preview Protege. Hari ini kita membongkar apa yang sesungguhnya ada di dalam ontology, yaitu triple RDF. Sebut Sub-CPMK 4 bagian 1: menyusun pernyataan RDF. Perkirakan sesi 150 menit.


---

## Slide 2

RENCANA SESI

Alur Pertemuan Hari Ini

01

Pembuka dan jembatan dari Pertemuan 5 ke Pertemuan 6

10 menit

02

Anatomi triple: subject, predicate, object, dan jenis node

30 menit

03

URI, IRI, namespace, dan prefiks — konvensi penamaan

25 menit

04

Live-coding rdflib: Graph, tambah triple, serialisasi Turtle dan JSON-LD

40 menit

05

Mini-lab berpasangan: graf Kampus USU minimal 10 triple

25 menit

06

Diskusi, ringkasan, dan preview Pertemuan 7

20 menit

WEB SEMANTIK · TIF2305

02


### Catatan Pengajar

Bacakan enam segmen dengan cepat. Tegaskan bahwa segmen 04 (live-coding rdflib) dan 05 (mini-lab) adalah puncak sesi: mahasiswa harus keluar dari kelas sudah mampu menulis triple sendiri dalam Python. Ingatkan mereka membuka laptop di segmen 04.


---

## Slide 3

SUB-CPMK 4 · BAGIAN 1

Capaian Pembelajaran

Empat indikator, masing-masing dengan cara pengecekan yang berbeda.

01

Menjelaskan

Model triple RDF: subject, predicate, dan object.

Dicek via kuis

02

Mengidentifikasi

Peran URI/IRI, literal, dan blank node di dalam graf.

Latihan lisan di papan

03

Menggunakan

Namespace dan prefiks agar triple mudah dibaca.

Live-coding segmen 04

04

Menyusun

Graf minimal 10 triple dengan rdflib, lalu diekspor.

Mini-lab dan tugas M6→M7

Di akhir sesi Anda sudah memiliki graf mini Kampus USU yang tersimpan sebagai berkas Turtle dan JSON-LD.

WEB SEMANTIK · TIF2305

03


### Catatan Pengajar

Indikator Sub-CPMK 4 bagian 1 yang dinilai hari ini: (1) menjelaskan model triple, (2) mengidentifikasi jenis node, (3) menggunakan namespace dan prefiks, (4) menyusun minimal 10 triple via rdflib. Nilai formatif diambil dari mini-lab, kuis, dan tugas mandiri M6 ke M7.


---

## Slide 4

RECAP · JEMBATAN

Dari Pohon Hirarki ke Jaringan Triple

Ontology adalah idenya

Hirarki Person → Student → Ida yang minggu lalu kita gambar di kertas.

RDF adalah aksaranya

Ide yang sama, diketik menjadi kumpulan triple yang bisa disimpan komputer.

WEB SEMANTIK · TIF2305

04


### Catatan Pengajar

Poin utama: ontology adalah ide atau gramatika; RDF adalah aksara atau notasi yang menyimpan ide itu. Analogi: kalau ontology sama dengan kelas UML, RDF adalah baris data yang mengisinya. Tekankan bahwa hirarki Person ke Student ke Ida yang minggu lalu digambar di kertas, hari ini akan diketik menjadi triple. Recall Layer Cake: tunjuk lapis RDF, di bawah Ontology dan di atas XML.


---

## Slide 5

01

Anatomi Triple

30 menit · Slide 6–9

Tujuan: memecah kalimat alami menjadi triple dan mengidentifikasi peran setiap node — URI, literal, atau blank node.

WEB SEMANTIK · TIF2305

05


### Catatan Pengajar

Divider singkat 30 detik. Ajukan pertanyaan pemantik: kalau saya bilang Ida mengajar Web Semantik, ada berapa fakta atomik di kalimat itu? Jawaban yang diharapkan: satu, yaitu satu triple.


---

## Slide 6

SEGMEN 1 · DEFINISI

Satu Triple Sama dengan Satu Fakta

Definisi — Triple adalah atom pengetahuan: satu pernyataan yang tersusun dari tepat tiga bagian, yaitu subject, predicate, dan object.

SUBJECT · SUBJEK

Ida

Entitas yang dibicarakan. Wajib URI atau blank node.

PREDICATE · PREDIKAT

mengajar

Relasi atau properti yang menghubungkan. Selalu URI.

OBJECT · OBJEK

TIF2305

Nilai atau entitas tujuan. Bisa URI, literal, atau blank node.

ex:ida ex:mengajar ex:tif2305 .

WEB SEMANTIK · TIF2305

06


### Catatan Pengajar

Definisikan triple sebagai atom pengetahuan dengan tiga komponen: subject, predicate, object. Contoh sederhana Ida, mengajar, TIF2305. Kaitkan dengan pola SPO di bahasa Indonesia; hampir semua kalimat aktif bisa dipecah menjadi satu triple atau lebih.


---

## Slide 7

SEGMEN 1 · GRAF

Satu Kalimat, Satu Panah, Satu Fakta

Banyak triple berarti banyak panah, dan kumpulan panah itulah yang kita sebut Knowledge Graph . Node yang sama dapat muncul di banyak triple sekaligus.

WEB SEMANTIK · TIF2305

07


### Catatan Pengajar

Ajak mahasiswa membayangkan RDF sebagai graf: node bulat untuk subject dan object, panah berlabel untuk predicate. Gambar mini di papan: Ida, panah mengajar, TIF2305. Sampaikan bahwa banyak triple sama dengan banyak panah sama dengan graf. Inilah kenapa disebut Knowledge Graph.


---

## Slide 8

SEGMEN 1 · JENIS NODE

Tidak Semua Node Boleh Berdiri di Mana Saja

Subject

URI atau blank node. Literal tidak pernah boleh.

Predicate

Selalu URI. Ini aturan paling ketat di RDF 1.1.

Object

Paling fleksibel: URI, literal, atau blank node.

WEB SEMANTIK · TIF2305

08


### Catatan Pengajar

Runut tiga jenis node: URI/IRI sebagai nama global, literal sebagai nilai, blank node sebagai nama lokal anonim. Ingatkan aturan keras RDF 1.1: subject wajib URI atau blank node, predicate wajib URI, object bebas. Miskonsepsi umum: mahasiswa menuliskan objek sebagai string biasa padahal seharusnya URI. Aturan cepat: kalau objek pernah muncul sebagai subject di triple lain, jadikan URI.


---

## Slide 9

SEGMEN 1 · LITERAL & BLANK NODE

Ujung Rantai Data dan Node Tanpa Nama

ex:tif2305 ex:sks "3"^^xsd:integer . ex:ida foaf:name "Ida Adi"@id .

Miskonsepsi umum: literal tanpa tipe. Angka 2025 yang tersimpan sebagai string tidak bisa dibandingkan secara matematis.

WEB SEMANTIK · TIF2305

09


### Catatan Pengajar

Tunjukkan literal bertipe (xsd:integer, xsd:date, xsd:decimal) dibanding literal berbahasa (Ida@id, Ida@en). Peringatkan miskonsepsi umum: mahasiswa sering lupa memberi tipe, sehingga angka 2025 tersimpan sebagai string dan tidak bisa dibandingkan secara matematis. Blank node ditulis dengan tanda kurung siku di Turtle; hindari pemakaian berlebihan.


---

## Slide 10

02

Identitas: URI, IRI, Namespace

25 menit · Slide 11–14

Tujuan: membedakan URI, URL, URN, dan IRI, lalu memakai namespace dan prefiks agar triple tetap ringkas dan terbaca.

WEB SEMANTIK · TIF2305

10


### Catatan Pengajar

Segmen ini fokus ke identitas. Ajukan pertanyaan pemantik: bagaimana komputer tahu bahwa Ida di data kita adalah Ida yang sama di sistem lain? Jawabannya: URI global.


---

## Slide 11

SEGMEN 2 · IDENTIFIER

Memberi Alamat Global pada Setiap Entitas

URI

Payung untuk semua identifier.

URL

URI yang menunjuk lokasi: http://…

URN

Identitas tanpa lokasi: urn:isbn:…

IRI

URI yang aman untuk karakter Unicode.

WEB SEMANTIK · TIF2305

11


### Catatan Pengajar

Perbandingan singkat: URI adalah payung; URL adalah URI yang meng-alamati lokasi; URN adalah URI tanpa lokasi seperti urn:isbn; IRI adalah URI yang mendukung Unicode. Kelas ini memakai HTTP-URI karena paling umum di web modern dan Linked Data. Untuk nama Indonesia dengan karakter khusus, gunakan IRI.


---

## Slide 12

SEGMEN 2 · KONVENSI

Lima Aturan Membuat URI yang Baik

URI yang stabil adalah investasi. Mengubahnya berarti memutus setiap tautan yang pernah dibuat orang lain.

01

HTTP-based. Pakai skema http atau https agar bisa di-dereference sebagai Linked Data.

02

Stabil. Sekali dipublikasikan, jangan diubah.

03

Satu URI, satu entitas. Jangan memakai satu identifier untuk dua hal berbeda.

04

Konsisten. Pilih pola slash / atau hash #, lalu pakai terus.

05

Bebas ekstensi teknis. Hindari .php atau .aspx di dalam URI.

“Cool URIs don't change” — Tim Berners-Lee, 1998.

WEB SEMANTIK · TIF2305

12


### Catatan Pengajar

Lima aturan singkat: HTTP-based, stabil jangan diubah, satu URI satu entitas, pakai slash atau hash secara konsisten, hindari ekstensi teknis seperti .php atau .aspx. Referensi: Cool URIs don't change (Berners-Lee, 1998). Untuk latihan kelas, pola http://usu.ac.id/kampus# sudah cukup walau belum di-host.


---

## Slide 13

SEGMEN 2 · NAMESPACE

Meringkas Alamat Panjang dengan Prefiks

@prefix ex: <http://usu.ac.id/kampus#> . @prefix foaf: <http://xmlns.com/foaf/0.1/> . ex:ida foaf:name "Ida Adi"@id .

Namespace standar yang wajib dikenali

rdf · rdfs · xsd · foaf · dc / dcterms

Prefiks dideklarasikan dengan @prefix di Turtle, xmlns di RDF/XML, dan @context di JSON-LD.

WEB SEMANTIK · TIF2305

13


### Catatan Pengajar

Namespace adalah kumpulan URI dengan awalan yang sama; prefiks adalah singkatannya. Contoh: @prefix ex: menunjuk ke http://usu.ac.id/kampus# sehingga kita bisa menulis ex:ida alih-alih URI lengkap. Analogi: URI adalah alamat rumah unik di seluruh dunia, namespace adalah kode pos dan nama jalan, prefiks adalah singkatan. Sebutkan namespace standar yang wajib dihafal: rdf, rdfs, xsd, foaf, dc atau dcterms.


---

## Slide 14

03

Live-coding rdflib

40 menit · Slide 16–19

Empat langkah ini adalah seluruh isi segmen. Buka laptop sekarang; error saat pertama kali menjalankan kode adalah hal yang normal.

WEB SEMANTIK · TIF2305

15


### Catatan Pengajar

Segmen aksi. Minta mahasiswa membuka laptop dan menyiapkan Python atau notebook. Sampaikan: dalam 40 menit ke depan kita akan menulis, membaca, dan menyimpan triple pertama mereka. Sabar dengan error, itu normal.


---

## Slide 15

SEGMEN 2 · VOCABULARY

Empat Vocabulary yang Siap Dipakai

Anda hampir tidak perlu membuat property sendiri. Cari dulu di lov.linkeddata.es sebelum menciptakan yang baru.

foaf:

FOAF

Friend-of-a-Friend: orang, akun, dan relasi antar orang.

dcterms:

Dublin Core

Metadata dokumen — sudah kita bahas di Pertemuan 4.

schema:

Schema.org

Structured data untuk mesin pencari — Pertemuan 3.

skos:

SKOS

Kosakata terkontrol, tesaurus, dan sistem klasifikasi.

Reuse before reinvent.

WEB SEMANTIK · TIF2305

14


### Catatan Pengajar

Sekilas empat vocabulary siap pakai: FOAF untuk orang dan akun, Dublin Core untuk metadata dokumen, Schema.org untuk structured data web, SKOS untuk kosakata terkontrol dan tesaurus. Ingatkan prinsip reuse before reinvent: cari dulu di LOV.linkeddata.es sebelum membuat property sendiri.


---

## Slide 16

SEGMEN 3 · FASE 1 DAN 2

Pasang rdflib, Siapkan Kanvas Kosong

$ pip install rdflib $ python -c "import rdflib; print(rdflib.__version__)"

Butuh Python 3.10+ dan rdflib 7.x. Jika instalasi gagal karena jaringan kelas, pakai notebook Google Colab cadangan di LMS — jalankan !pip install rdflib di sel pertama.

WEB SEMANTIK · TIF2305

16


### Catatan Pengajar

Perintah: pip install rdflib, atau pip install rdflib==7.1.1 bila ingin versi tetap. Uji dengan python -c import rdflib print rdflib.__version__. Untuk yang gagal install karena WiFi atau proxy, arahkan ke notebook Google Colab cadangan yang sudah disiapkan di LMS.


---

## Slide 17

SEGMEN 3 · FASE 3

Merakit Triple ke dalam Graf

from rdflib import Graph, Namespace, Literal from rdflib.namespace import RDF, FOAF, XSD g = Graph() EX = Namespace("http://usu.ac.id/kampus#") g.bind("ex", EX); g.bind("foaf", FOAF)

Perhatikan bahwa EX.ida menjadi pusat: satu URI yang sama dipakai sebagai subject di banyak triple, sehingga panah keluar bertambah tanpa menduplikasi node.

WEB SEMANTIK · TIF2305

17


### Catatan Pengajar

Tunjukkan alur: Graph() lalu Namespace() lalu bind() lalu add((s,p,o)). Tulis di layar lima triple pertama secara live, sengaja lambat, minta mahasiswa mengetik ulang. Setelah lima triple, panggil serialize(format='turtle') dan tampilkan output. Ringkas tiga pola yang baru dipakai: add, serialize, iterate.


---

## Slide 18

SEGMEN 3 · FASE 4

Satu Graf, Dua Format Ekspor

Turtle (.ttl)

Ringkas dan paling mudah dibaca manusia. Perhatikan titik koma yang menyingkat subject yang sama.

JSON-LD (.jsonld)

JSON dengan @context . Direkomendasikan W3C untuk integrasi API dan web modern.

WEB SEMANTIK · TIF2305

18


### Catatan Pengajar

Serialisasi adalah cara menyimpan graf ke file. Turtle ringkas, human-friendly, dan menjadi standar. JSON-LD adalah JSON dengan @context, cocok untuk web dan API. Tunjukkan output kedua format di layar, lalu minta mahasiswa memilih mana yang paling mudah dibaca menurut mereka.


---

## Slide 19

SEGMEN 3 · MEMBACA GRAF

Bertanya kepada Graf dengan Python Biasa

g.parse("kampus.ttl", format="turtle")

Ini masih query manual. Di Pertemuan 9 kita menggantinya dengan SPARQL yang jauh lebih ekspresif.

WEB SEMANTIK · TIF2305

19


### Catatan Pengajar

Cara memuat balik: g.parse('kampus.ttl', format='turtle'). Cara iterasi: for s,p,o in g.triples((None, RDF.type, EX.Lecturer)) lalu print(s). Sampaikan bahwa ini adalah query manual; minggu 9 kita akan memakai SPARQL yang jauh lebih ekspresif.


---

## Slide 20

04

Mini-lab Kampus USU

25 menit · Slide 21 · berpasangan

Sepuluh triple terasa sedikit. Ia adalah batu bata pertama dari ekosistem yang sekarang berukuran miliaran.

WEB SEMANTIK · TIF2305

20


### Catatan Pengajar

Segmen mini-lab. Bagi mahasiswa berpasangan dua orang, bukan berkelompok proyek, supaya tidak terjebak dinamika kelompok. Bagikan template notebook di LMS: kampus_mini.ipynb. Motivasi: sepuluh triple yang mereka tulis hari ini adalah batu bata pertama dari ekosistem data sebesar DBpedia.


---

## Slide 21

SEGMEN 4 · INSTRUKSI

Bahan Baku dan Kriteria Keberhasilan

15 menit

Menulis triple berpasangan di notebook.

10 menit

Review pasangan; tiga pasangan presentasi singkat.

Triple bibit

ex:tif2305 ex:sks "3"^^xsd:integer .

WEB SEMANTIK · TIF2305

21


### Catatan Pengajar

Tugas: susun graf minimal 10 triple berisi 3 dosen, 3 mata kuliah, 2 mahasiswa. Wajib memakai minimal dua namespace: ex ditambah salah satu dari foaf atau dc. Serialisasi ke Turtle. Waktu 15 menit menulis dan 10 menit review berpasangan. Beri contoh triple bibit di layar. Tiga pasangan mempresentasikan graf singkat; kelas menandai satu triple paling menarik.


---

## Slide 22

SEGMEN 5 · DISKUSI KELAS

Tiga Pertanyaan, Tiga Baris Kursi

Tiga menit diskusi, dua menit sharing. Setiap baris membahas satu pertanyaan.

1

Kenapa objek yang berupa entitas harus URI, bukan literal?

2

Kapan blank node benar-benar tepat dipakai?

3

Apa risiko URI yang tidak stabil dan sering diubah?

WEB SEMANTIK · TIF2305

22


### Catatan Pengajar

Tiga pertanyaan pemantik. Bagi kelas menjadi tiga baris; masing-masing baris membahas satu pertanyaan. Tiga menit diskusi ditambah dua menit sharing. Moderasi ringkas per baris kursi.


---

## Slide 23

PENUTUP

Tiga Hal untuk Dibawa Pulang

01

RDF adalah graf yang tersusun dari triple. Satu triple sama dengan satu fakta.

02

URI, namespace, dan prefiks adalah infrastruktur identitas — bukan sekadar kosmetik.

03

Dengan rdflib, operasi baca-tulis-serialisasi selesai dalam kurang dari sepuluh baris kode.

PERTEMUAN 7

Serialisasi lanjutan, higher-order relationship, reifikasi, dan penggabungan graf dari banyak sumber.

BACAAN WAJIB

W3C RDF 1.1 Turtle · Programming the Semantic Web, Bab 3.

WEB SEMANTIK · TIF2305

24


### Catatan Pengajar

Tutup dengan tiga poin utama: (1) RDF adalah graf dari triple, (2) URI ditambah namespace ditambah prefiks adalah infrastruktur identitas, (3) rdflib memungkinkan operasi baca-tulis dalam kurang dari sepuluh baris kode. Preview Pertemuan 7: serialisasi lanjutan, Turtle detail, RDF/XML sekilas, higher-order relationship, reifikasi, dan penggabungan graf dari banyak sumber. Bacaan: RDF 1.1 Turtle spec dan Programming the Semantic Web Bab 3.
