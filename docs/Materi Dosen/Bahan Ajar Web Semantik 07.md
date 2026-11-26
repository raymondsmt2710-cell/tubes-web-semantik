# Bahan Ajar Web Semantik 07


---

## Slide 1

PERTEMUAN 7 · TIF2305 · SUB-CPMK 4 (BAGIAN 2)

Serialisasi RDF dan Higher-order Relationship

Lima format serialisasi, reifikasi klasik dan RDF-star, penggabungan graf lewat named graph — semuanya dijalankan dengan rdflib.

Mata Kuliah Web Semantik

Program Studi Teknologi Informasi

150 menit


### Catatan Pengajar

Selamat datang di Pertemuan 7 Web Semantik. Hari ini kita naik satu tingkat dari model triple ke bentuk file yang dapat dipertukarkan, dan dari pernyataan biasa ke pernyataan yang membicarakan pernyataan lain. Kita gunakan rdflib sebagai perkakas.


---

## Slide 2

RENCANA SESI

Alur Pertemuan Hari Ini

01

Pembuka dan jembatan dari model triple ke bentuk file

10 menit

02

Serialisasi lanjut: Turtle, JSON-LD, RDF/XML, N-Triples, N-Quads

35 menit

03

Higher-order: reifikasi klasik dibanding RDF-star

35 menit

04

Live-coding rdflib: konversi format dan anotasi pernyataan

35 menit

05

Diskusi, Ringkasan, dan preview UTS

25 menit

WEB SEMANTIK · TIF2305

02


### Catatan Pengajar

Enam segmen selama 150 menit: pembuka, serialisasi lanjut, higher-order relationship, live-coding rdflib, mini-lab gabung graf, lalu diskusi + kuis. Akhir sesi kita akan preview UTS di Pertemuan 8. Pastikan Python 3.10+ dan rdflib 7.x sudah siap.


---

## Slide 3

SUB-CPMK 4 · BAGIAN 2

Capaian Pembelajaran

Empat indikator, masing-masing dengan cara pengecekan yang berbeda.

01

Memilih

Serialisasi yang tepat dari lima format, beserta alasannya.

Dicek via kuis

02

Menerapkan

Reifikasi klasik dengan rdf:Statement.

Live-coding segmen 04

03

Membandingkan

Pendekatan modern RDF-star dengan reifikasi klasik.

Diskusi kelas

04

Menggabungkan

Dua graf menjadi satu berkas TriG dengan named graph.

Mini-lab M7

Di akhir sesi graf Kampus USU dari Pertemuan 6 bertambah minimal 5 triple baru beserta metadata provenance.

WEB SEMANTIK · TIF2305

03


### Catatan Pengajar

Sub-CPMK 4 kita lanjutkan: setelah minggu lalu mengenal model triple dan identifier, kini fokusnya adalah representasi RDF di berbagai format serialisasi dan bagaimana RDF menangani meta-pernyataan. Ini prasyarat sebelum masuk SPARQL di paruh dua semester.


---

## Slide 4

RECAP · JEMBATAN

Graf Sudah Jadi. Bagaimana Mengirimnya?

Serialisasi

Bentuk file yang bisa dipertukarkan antar sistem.

Reifikasi

Catatan tentang siapa yang menyatakan sebuah fakta.

Penggabungan

Union graph dan named graph untuk banyak sumber data.

WEB SEMANTIK · TIF2305

04


### Catatan Pengajar

Minggu lalu kita bertanya: bagaimana komputer menyimpan graf? Jawabannya triple. Sekarang: bagaimana graf itu berpindah antar sistem? Jawabannya serialisasi. Dan bagaimana kita catat siapa yang menyatakan sesuatu? Jawabannya reifikasi atau RDF-star.


---

## Slide 5

01

Serialisasi Lanjut

35 menit · Slide 6–9

Bukan soal format mana yang terbaik, tetapi terbaik untuk apa: untuk siapa dibaca, kapan dipakai, dan seberapa luas dukungan tool-nya.

WEB SEMANTIK · TIF2305

05


### Catatan Pengajar

Kita masuk topik teknis pertama: bentuk file RDF. Perhatikan tiga hal untuk tiap format — untuk siapa (mesin/manusia), kapan dipakai (embed/dump/stream), dan apa dukungan tool-nya. Bukan soal format mana yang terbaik tapi terbaik untuk apa.


---

## Slide 6

SEGMEN 1 · TURTLE

Turtle Ditulis untuk Dibaca Manusia

Lima singkatan ini yang membuat berkas Turtle jauh lebih pendek daripada N-Triples.

@prefix ex: <http://usu.ac.id/kampus#> . @prefix foaf: <http://xmlns.com/foaf/0.1/> . 
ex:ida a 
foaf:Person ; 
foaf:name "Ida Adi"@id ; 
ex:mengajar ex:tif2305, ex:tif2401 ; 
ex:kontak [ ex:email "ida@usu.ac.id" ] .

a

Singkatan untuk rdf:type.

;

Subjek yang sama, predikat berikutnya.

,

Predikat yang sama, objek berikutnya.

[ ]

Blank node inline, tanpa perlu URI.

( )

RDF Collection, daftar yang berurutan.

WEB SEMANTIK · TIF2305

06


### Catatan Pengajar

Turtle dibuat agar mudah dibaca manusia. Singkatan penting: a untuk rdf:type, titik-koma untuk berbagi subjek, koma untuk berbagi predikat, kurung siku untuk blank node inline, dan kurung biasa untuk RDF Collection. Prefiks dideklarasi @prefix di awal.


---

## Slide 7

@prefix ex <http://usu.ac.id/kampus#> .
@prefix foaf: <http://xmlns.com/foaf/0.1/>

ex:ida a foaf:Person ;
    foaf:name Ida Adi@id ;
    ex:mengajar "ex:tif2305", ex:tif2401
    ex:usia "dua puluh satu"^^xsd:integer ;
    ex:kontak [
        ex:email "ida@usu.ac.id" .
    ]

Deklarasi prefiks ex kehilangan tanda titik dua
Deklarasi prefiks foaf tidak diakhiri titik.
Prefiks xsd belum didefinisikan.
Ida Adi harus ditulis sebagai literal:
"ex:tif2305" merupakan string, bukan resource. Tanda kutip harus dihilangkan.
Setelah ex:tif2401 diperlukan titik koma karena predikat berikutnya masih memakai subjek ex:ida.
Nilai usia tidak cocok dengan xsd:integer. Gunakan 21 atau "21"^^xsd:integer.
Titik di dalam blank node ditempatkan secara keliru.
Pernyataan utama belum ditutup dengan titik.


---

## Slide 8

SEGMEN 1 · JSON-LD

JSON Biasa, Ditambah Tiga Kunci Khusus

{
  "@context": {
    "ex": "http://usu.ac.id/kampus#",
    "foaf": "http://xmlns.com/foaf/0.1/"
  },
  "@id": "ex:ida",
  "@type": "foaf:Person",
  "foaf:name": {
    "@value": "Ida Adi",
    "@language": "id"
  },
  "ex:mengajar": [
    { "@id": "ex:tif2305" },
    { "@id": "ex:tif2401" }
  ]
}

WEB SEMANTIK · TIF2305

07

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Course",
  "name": "Web Semantik"
}
</script>


### Catatan Pengajar

JSON-LD memakai struktur JSON biasa dengan kunci khusus: @context (peta prefiks), @id (URI subjek), @type (kelas). Sangat pas untuk halaman web dan API JSON. Ingat pelajaran minggu 3: mesin pencari sudah mengonsumsi JSON-LD sebagai structured data. Miskonsepsi: JSON-LD lebih baru belum berarti lebih baik untuk semua kasus.


---

## Slide 9

{
  "@context": {
    "ex": "http://usu.ac.id/kampus",
    "nama": "foaf:name"
  },
  "@id": "Ida Adi",
  "@type": "foaf:Person",
  "nama": {
    "@id": "Ida Adi",
    "@language": "Indonesia"
  },
  "ex:mengajar": "ex:tif2305",
  "ex:usia": {
    "@value": "dua puluh satu",
    "@type": "xsd:integer"
  }
}

Namespace ex kehilangan pemisah #. Akibatnya ex:ida dapat berkembang menjadi IRI yang tidak diinginkan, seperti http://usu.ac.id/kampusida.

Prefiks foaf belum didefinisikan.

Prefiks xsd belum didefinisikan.

Nilai @id berupa nama dengan spasi, bukan identitas resource yang tepat.

Nama dimodelkan dengan @id. Nama seharusnya menjadi literal.

@language tidak boleh dipasangkan dengan @id seperti pada contoh tersebut.

Tag bahasa seharusnya menggunakan kode bahasa, misalnya id, bukan "Indonesia".

Nilai "ex:tif2305" menjadi string. Hubungan menuju resource harus menggunakan @id.

Teks "dua puluh satu" tidak dapat diberi tipe xsd:integer.


---

## Slide 10

SEGMEN 1 · TIGA FORMAT LAINNYA

Yang Tua, Yang Datar, dan Yang Berkonteks

Ketiganya jarang ditulis tangan, tetapi sering Anda temukan sebagai keluaran mesin.

.rdf

RDF/XML

Serialisasi paling tua dan paling verbose. Masih relevan untuk dataset historis, misalnya dump DBpedia lama.

.nt

N-Triples

Satu baris satu triple, tanpa prefiks. Paling tahan terhadap git-diff dan ideal untuk streaming.

.nq

N-Quads

N-Triples dengan kolom keempat: nama graf atau konteks tempat triple itu berada.

<http://usu.ac.id/kampus#ida> <http://xmlns.com/foaf/0.1/name> "Ida Adi" . <http://usu.ac.id/kampus#ida> <http://xmlns.com/foaf/0.1/name> "Ida Adi" <http://usu.ac.id/g/kampus> .

WEB SEMANTIK · TIF2305

08


### Catatan Pengajar

RDF/XML: serialisasi paling tua, verbose, tetap dipakai untuk kompatibilitas dataset lama. N-Triples: satu baris satu triple — pilihan terbaik untuk streaming dan git-diff. N-Quads: N-Triples ditambah kolom keempat berisi nama graf atau konteks.


---

## Slide 11

SEGMEN 1 · RDF/XML

RDF/XML

RDF/XML merupakan salah satu sintaks RDF yang paling awal distandardisasi. Ia menuliskan graf RDF menggunakan elemen dan atribut XML.

<rdf:RDF
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:foaf="http://xmlns.com/foaf/0.1/"
    xmlns:ex="http://usu.ac.id/kampus#">

  <foaf:Person rdf:about="http://usu.ac.id/kampus#ida">
    <foaf:name xml:lang="id">Ida Adi</foaf:name>
    <ex:mengajar rdf:resource="http://usu.ac.id/kampus#tif2305"/>
  </foaf:Person>
</rdf:RDF>

WEB SEMANTIK · TIF2305

09


### Catatan Pengajar

Turtle dibuat agar mudah dibaca manusia. Singkatan penting: a untuk rdf:type, titik-koma untuk berbagi subjek, koma untuk berbagi predikat, kurung siku untuk blank node inline, dan kurung biasa untuk RDF Collection. Prefiks dideklarasi @prefix di awal.


---

## Slide 12

SEGMEN 1 · N-Triples

N-Triples

N-Triples menggunakan satu baris untuk satu triple. Tidak ada prefiks atau singkatan.

<http://usu.ac.id/kampus#ida> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://xmlns.com/foaf/0.1/Person> .
<http://usu.ac.id/kampus#ida> <http://xmlns.com/foaf/0.1/name> "Ida Adi"@id .
<http://usu.ac.id/kampus#ida> <http://usu.ac.id/kampus#mengajar> <http://usu.ac.id/kampus#tif2305> .

WEB SEMANTIK · TIF2305

10


### Catatan Pengajar

Turtle dibuat agar mudah dibaca manusia. Singkatan penting: a untuk rdf:type, titik-koma untuk berbagi subjek, koma untuk berbagi predikat, kurung siku untuk blank node inline, dan kurung biasa untuk RDF Collection. Prefiks dideklarasi @prefix di awal.


---

## Slide 13

SEGMEN 1 · N-Quads

N-Quads

N-Quads memperluas N-Triples dengan menambahkan posisi keempat, yaitu graph label.

<http://usu.ac.id/kampus#ida>
<http://xmlns.com/foaf/0.1/name>
"Ida Adi"
<http://usu.ac.id/g/kampus> .

WEB SEMANTIK · TIF2305

11

subject + predicate + object + graph


### Catatan Pengajar

Turtle dibuat agar mudah dibaca manusia. Singkatan penting: a untuk rdf:type, titik-koma untuk berbagi subjek, koma untuk berbagi predikat, kurung siku untuk blank node inline, dan kurung biasa untuk RDF Collection. Prefiks dideklarasi @prefix di awal.


---

## Slide 14

SEGMEN 1 · MATRIKS PERBANDINGAN

Memilih Format Sesuai Konsumennya

Tampil di halaman

JSON-LD, di-embed sebagai structured data.

Tersimpan di data lake

N-Quads, karena konteks graf ikut tersimpan.

Diproses git-diff

N-Triples, satu baris satu fakta.

WEB SEMANTIK · TIF2305

12


### Catatan Pengajar

Tayangkan tabel: Turtle unggul di keringkasan; JSON-LD unggul di web; RDF/XML unggul di kompatibilitas lama; N-Triples unggul di streaming atau diff; N-Quads unggul saat butuh named graph. Diskusikan skenario per baris supaya mahasiswa punya kompas memilih.


---

## Slide 15

SEGMEN 2 · REIFIKASI KLASIK

Satu Pernyataan Menjadi Node Tersendiri

@prefix ex:   <http://usu.ac.id/kampus#> .
@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix dct:  <http://purl.org/dc/terms/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .

ex:stmt01
    a rdf:Statement ;
    rdf:subject ex:Budi ;
    rdf:predicate ex:mengambil ;
    rdf:object ex:TIF2305 ;
    prov:wasAttributedTo ex:Ida ;
    dct:date "2026-08-05"^^xsd:date ;
    prov:wasDerivedFrom ex:SIA .

Reifikasi berarti memperlakukan sesuatu yang abstrak sebagai objek atau resource yang dapat dibicarakan.

Satu fakta sederhana butuh minimal empat triple pembungkus sebelum anotasi ditambahkan. Boros, tetapi kompatibel 100 persen dengan sistem RDF 1.1.

WEB SEMANTIK · TIF2305

13


### Catatan Pengajar

Reifikasi klasik: buat resource baru bertipe rdf:Statement, lalu tempelkan rdf:subject, rdf:predicate, rdf:object. Setelah itu tambahkan atribut lain seperti dct:creator dan dct:date. Verbose karena butuh 4 triple pembungkus, tetapi kompatibel di semua tool RDF 1.1.


---

## Slide 16

02

Higher-order Relationship

25 menit · Slide 11–14

Pertanyaannya bukan lagi apa faktanya, melainkan kata siapa, kapan dicatat, dan dari mana sumbernya.

WEB SEMANTIK · TIF2305

14


### Catatan Pengajar

Kita beralih ke pertanyaan yang lebih dalam: bagaimana RDF menyatakan pernyataan tentang pernyataan lain? Contoh: Ida menyatakan bahwa Budi mengambil TIF2305 pada 2026-08-05. Ada dua jalur — reifikasi klasik dan RDF-star yang lebih baru.


Namun, dalam sistem nyata muncul pertanyaan tambahan:
- Siapa yang melaporkan fakta tersebut?
- Kapan data dicatat?
- Dari sistem mana data berasal?
- Seberapa yakin kita terhadap informasi itu?
- Apakah informasi tersebut sudah diverifikasi?
- Apakah kita sedang menyatakan fakta atau hanya mencatat klaim seseorang?


---

## Slide 17

SEGMEN 2 · RDF-STAR

Triple sebagai Subjek Triple Lain

1 triple

Cukup satu triple pembungkus, bukan empat.

RDF 1.2 draft

Sudah stabil di banyak tool, spesifikasi masih draft.

Dukungan

rdflib ≥ 6.2 · Jena 4.x · GraphDB 10.x

WEB SEMANTIK · TIF2305

15

<< ex:Budi ex:mengambil ex:TIF2305 ~ ex:stmt01 >>
    prov:wasAttributedTo ex:Ida ;
    dct:date "2026-08-05"^^xsd:date ;
    prov:wasDerivedFrom ex:SIA .


ex:Budi ex:mengambil ex:TIF2305
    {|
        prov:wasAttributedTo ex:Ida ;
        dct:date "2026-08-05"^^xsd:date ;
        prov:wasDerivedFrom ex:SIA
    |} .


### Catatan Pengajar

RDF-star (draft RDF 1.2) memperkenalkan sintaks kurung sudut ganda: triple bertindak sebagai subjek atau objek triple lain. Ringkas, hanya butuh 1 triple pembungkus. rdflib 6.2 ke atas, Jena 4.x, dan GraphDB 10.x sudah mendukung parse dan serialize format bintang.


---

## Slide 18

SEGMEN 2 · KEPUTUSAN

Kapan Memakai yang Mana

Interoperabilitas menang

Reifikasi klasik, saat data akan dibaca graph database lama atau parser RDF standar.

Keringkasan menang

RDF-star, saat stack sudah modern dan Anda butuh kueri SPARQL-star.

Mencampur keduanya boleh, selama konsisten di dalam satu berkas.

WEB SEMANTIK · TIF2305

15


### Catatan Pengajar

Pilih klasik jika audiens masih pada tool RDF 1.1 atau butuh interop maksimal. Pilih RDF-star jika target sistem sudah mendukung, dan Anda ingin graf ringkas serta query SPARQL-star yang lugas. Boleh campur, tapi konsisten dalam satu berkas.


---

## Slide 19

SEGMEN 2 · TRIG & NAMED GRAPH

Banyak Graf dalam Satu Berkas

@prefix ex:   <http://usu.ac.id/kampus#> .
@prefix dct:  <http://purl.org/dc/terms/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .

ex:gSIA {
    ex:Budi ex:mengambil ex:TIF2305 .
    ex:Budi ex:terdaftarPada ex:TI .
}

ex:gSurvei {
    ex:Budi ex:menyukai ex:WebSemantik .
}

//metatada gSIA
ex:gSIA
    dct:source ex:SIA ;
    prov:generatedAtTime "2026-08-05"^^xsd:date .

Setiap blok punya identitas sendiri, sehingga data dari banyak sumber bisa disimpan berdampingan tanpa tercampur. Ekstensi berkasnya .trig.

WEB SEMANTIK · TIF2305

17


### Catatan Pengajar

Named graph menjawab kebutuhan: siapa pemilik atau asal dari sekumpulan triple. TriG membungkus Turtle dengan blok bernama, misalnya blok untuk graf kampus. Ini format alami untuk menyimpan multi-sumber data dalam satu berkas.


---

## Slide 20

03

Live-coding rdflib

35 menit · Slide 16–18

Tiga blok ini adalah seluruh isi segmen: muat dan konversi, reifikasi, lalu aktifkan format bintang. Buka laptop sekarang.

WEB SEMANTIK · TIF2305

15


### Catatan Pengajar

Saatnya turun ke kode. Kita akan memuat kampus_mini.ttl hasil minggu 6, mengkonversi ke JSON-LD dan N-Triples, lalu menambahkan reifikasi klasik. Bila waktu cukup, tambahkan pula demo RDF-star. Perhatikan perubahan jumlah triple.


---

## Slide 21

SEGMEN 3 · KONVERSI FORMAT

Satu Graf, Tiga Berkas Keluaran

Muat berkas Turtle hasil Pertemuan 6, lalu tulis ulang dalam format lain tanpa mengubah isinya.

from rdflib import Graph, Namespace 
from rdflib.namespace import DCTERMS 

EX = Namespace("http://usu.ac.id/kampus#") 
g = Graph() 
g.bind("ex", EX) 
g.bind("dct", DCTERMS) 
g.parse("kampus_mini.ttl", format="turtle") 
g.serialize("kampus_mini.jsonld", format="json-ld" , indent=2) 
g.serialize("kampus_mini.nt", format="nt")

Bind dulu, serialisasi kemudian

Tanpa g.bind , keluaran penuh URI panjang dan sulit dibaca.

Isi sama, bentuk berbeda

Bandingkan ukuran ketiga berkas di layar; jumlah triple tetap identik.

WEB SEMANTIK · TIF2305

16


### Catatan Pengajar

g.serialize dengan destination kampus_mini.jsonld, format json-ld, indent 2 menghasilkan file JSON-LD; ganti format menjadi nt untuk N-Triples. Selalu bind namespace dulu supaya output Turtle atau JSON-LD tetap ringkas dan mudah dibaca.


---

## Slide 22

SEGMEN 3 · REIFIKASI DI RDFLIB

Empat Triple Pembungkus, Dua Anotasi

Pernyataan Ida mengajar TIF2305 kini punya penulis dan tanggal pencatatan.

from rdflib import URIRef, Literal from rdflib.namespace import RDF, DCTERMS, XSD s = URIRef(EX + "stmt-01") g.add((s, RDF.type, RDF.Statement)) g.add((s, RDF.subject, EX.Ida)) g.add((s, RDF.predicate, EX.mengajar)) g.add((s, RDF.object, EX.tif2305)) g.add((s, DCTERMS.creator, EX.Ida)) g.add((s, DCTERMS.date, Literal("2026-08-05", datatype=XSD.date)))

Perhatikan jumlah baris

Satu fakta yang semula satu baris kini menjadi enam triple di berkas Turtle.

Pernyataan asli tetap ada

Reifikasi tidak menggantikan triple aslinya; ia hanya menambah lapisan catatan.

WEB SEMANTIK · TIF2305

17


### Catatan Pengajar

Buat URIRef untuk pernyataan, misalnya EX.stmt_01, lalu tambahkan 4 triple pembungkus: rdf:type Statement, subject, predicate, object. Bubuhkan dct:creator dan dct:date pada resource yang sama. Serialisasi ulang ke Turtle, jelaskan pertambahan baris.


---

## Slide 23

SEGMEN 3 · RDF-STAR DI RDFLIB

Mengaktifkan Format Bintang

Format ttls untuk parse, trig-star untuk menulis named graph sekaligus.

turtle_star = ''' @prefix ex: <http://usu.ac.id/kampus#> . << ex:Ida ex:mengajar ex:tif2305 >> dct:creator ex:Budi . ''' g.parse(data=turtle_star, format="ttls" ) g.serialize("kampus_mini.trigs", format="trig-star" ) print(len(g)) # bandingkan dengan hasil reifikasi klasik

Reifikasi klasik

Empat triple pembungkus ikut terhitung sebagai triple biasa.

RDF-star

Triple pembungkus dihitung sebagai satu triple asserted saja.

WEB SEMANTIK · TIF2305

18


### Catatan Pengajar

Aktifkan parser bintang dengan g.parse data turtle_star_string format ttls. Serialisasi kembali dengan format trig-star agar named graph juga tertulis. Bandingkan jumlah triple di g dan di file — RDF-star menghitung triple pembungkus sebagai 1 triple asserted.


---

## Slide 24

PENUTUP

Tiga Hal untuk Dibawa Pulang

01

Lima format serialisasi, satu prinsip: pilih sesuai konsumen berkas.

02

Dua pola higher-order: reifikasi klasik untuk interop, RDF-star untuk keringkasan.

03

Named graph dan TriG menyatukan banyak sumber tanpa kehilangan jejak asalnya.

PERTEMUAN 8 · UTS

Sintesis Pertemuan 1 sampai 7: teori singkat ditambah praktikum rdflib. Latihan pra-UTS diunggah di LMS malam ini.

BACAAN WAJIB

W3C RDF 1.1 Turtle · JSON-LD 1.1 · TriG · RDF-star Draft

WEB SEMANTIK · TIF2305

23


### Catatan Pengajar

Ringkasan: 5 format serialisasi, 2 pola higher-order, dan penggabungan lewat named graph. Pertemuan 8 adalah UTS: sintesis Pertemuan 1 sampai 7 dengan format teori singkat ditambah praktikum rdflib. Latihan pra-UTS akan diunggah di LMS malam ini.
