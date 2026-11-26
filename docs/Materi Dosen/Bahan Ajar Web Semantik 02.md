# Bahan Ajar Web Semantik 02


---

## Slide 1

PERTEMUAN 2 · TIF2305 · SUB-CPMK 2

Format Dokumen XML

Sintaks dasar · Well-formed & valid · DTD/XSD · Namespace & XPath

Mata Kuliah Web Semantik

Program Studi Teknologi Informasi

150 menit


### Catatan Pengajar

Buka Pertemuan 2 dengan sapaan dan pengingat singkat bahwa hari ini kita mulai menyentuh sisi teknis: cara menulis DATA yang bisa dipertukarkan antar sistem. Sampaikan XML adalah format lama tetapi masih menjadi fondasi banyak standar Web Semantik (RDF/XML, SOAP, SVG, konfigurasi Android, XSD, XSLT). Tujuan sesi: mahasiswa mampu MEMBACA dan MENULIS dokumen XML yang well-formed serta tahu kapan perlu divalidasi. Alokasi 2 menit — jangan tampilkan agenda dulu, biarkan mahasiswa menerka topiknya.


---

## Slide 2

RECAP · JEMBATAN

Dari Ide Menjadi Tulisan

PERTEMUAN 1

Data yang bermakna

Mesin perlu memahami entitas dan relasi, bukan sekadar rangkaian karakter.

→

PERTEMUAN 2

Cara menuliskannya

XML: format teks bersama agar data dapat dikirim, disimpan, dan dibaca ulang sistem lain.

XML tampak “lama”, tetapi masih menjadi fondasi RDF/XML, SOAP, SVG, XSLT — dan wajib pada sistem nasional seperti e-Faktur DJP, SPT, serta pelaporan bank ke OJK.

WEB SEMANTIK · TIF2305

02


### Catatan Pengajar

Sambungkan jembatan dari Pertemuan 1: kalau minggu lalu kita bahas IDE tentang data bermakna, hari ini kita bahas KERTAS DAN PULPEN-nya — bagaimana data itu dituliskan supaya bisa dikirim, disimpan, dan dibaca ulang oleh sistem lain. Ingatkan mahasiswa bahwa bab XML terlihat 'lama' tetapi tetap penting: XSD dipakai pada skema RDF/XML, dan banyak API pemerintah serta perbankan Indonesia masih memakai XML (e-Faktur, SPT, pelaporan OJK). Waktu 3 menit.


---

## Slide 3

RENCANA SESI

Agenda Hari Ini · 150 Menit

0–5

Pembuka dan recap Pertemuan 1

Slide 1–2

5–15

Capaian pembelajaran dan jembatan materi

Slide 3–4

15–45

Segmen 1 — Sintaks dasar XML

Slide 5–9

45–70

Segmen 2 — Well-formed vs valid

Slide 10–13

70–85

Istirahat

—

85–110

Segmen 3 — DTD dan XML Schema (XSD)

Slide 14–17

110–130

Segmen 4 — Namespace dan XPath

Slide 18–20

130–145

Praktik menulis XML dan kuis LMS

Slide 22–23

145–150

Ringkasan dan preview Pertemuan 3

Slide 24

WEB SEMANTIK · TIF2305

03


### Catatan Pengajar

Tunjukkan pembagian waktu. Tekankan istirahat 15 menit ada di menit ke-70. Segmen 1 dan 2 padat konsep — sampaikan bahwa mahasiswa perlu fokus penuh di 55 menit pertama. Segmen 3 (DTD/XSD) hanya PENGENALAN: dosen menjelaskan struktur XSD tetapi mahasiswa tidak wajib menulis XSD sendiri. Praktik akhir 15 menit: setiap mahasiswa menulis satu dokumen XML pendek dan mengunggahnya ke LMS, dilanjutkan kuis pilihan ganda 5 soal. Alokasi ini pedoman — boleh disesuaikan dengan dinamika kelas.


---

## Slide 4

SUB-CPMK 2 · BAGIAN 1

Capaian Pembelajaran

Setelah pertemuan ini, Anda diharapkan mampu:

01

Menjelaskan tujuan dan sejarah singkat XML.

02

Menyusun dokumen XML sederhana dengan sintaks elemen dan atribut yang benar.

03

Membedakan dokumen well-formed dari dokumen valid.

04

Menjelaskan peran DTD dan XSD dalam validasi struktur.

05

Memahami fungsi XML Namespace dan sintaks dasar XPath.

WEB SEMANTIK · TIF2305

04


### Catatan Pengajar

Baca lima capaian satu per satu, jangan buru-buru. Jelaskan bahwa kelima capaian ini akan diuji lewat kuis 5 soal pilihan ganda di akhir sesi dan menjadi bagian dari UTS. Kaitkan setiap capaian dengan segmen yang akan dibawakan hari ini supaya mahasiswa punya peta harapan yang jelas. Waktu 3 menit.


---

## Slide 5

01

Sintaks Dasar XML

30 menit · Slide 5–9

Tujuan: Anda dapat menyebut anatomi dokumen XML dan menuliskan dokumen sederhana yang benar.

Dua sistem berbeda saling memahami melalui satu format teks bersama.

WEB SEMANTIK · TIF2305

05


### Catatan Pengajar

Buka segmen dengan pertanyaan pemantik: 'Bagaimana dua sistem yang berbeda bertukar data tanpa saling tahu bahasa pemrogramannya?' Biarkan mahasiswa menjawab, lalu sambungkan: keduanya butuh format bersama — Extensible Markup Language. Tekankan XML adalah markup untuk DATA, bukan untuk TAMPILAN seperti HTML. Sifat extensible berarti tag ditentukan sendiri; konsekuensinya kita butuh skema (DTD/XSD) untuk menyepakati tag yang boleh dipakai. Sebut contoh nyata Indonesia: e-Faktur DJP, SPT, laporan bank ke OJK. Beri kesempatan mahasiswa menyebut contoh lain (layout Android, SVG). Segmen ini 30 menit.


---

## Slide 6

SEGMEN 1 · PERBANDINGAN

Beda Tujuan: Tampilan vs Makna

Keduanya turunan SGML — yang berbeda adalah apa yang ingin dijelaskan oleh tag.

HTML — tag baku dan tidak bisa diubah; menjelaskan cara dokumen ditampilkan.

XML — extensible : tag dibuat sendiri sesuai konteks data yang dimodelkan.

WEB SEMANTIK · TIF2305

06


### Catatan Pengajar

Jelaskan perbedaan tujuan, bukan perbedaan sintaks. HTML fokus pada TAMPILAN dokumen dengan tag yang sudah baku (h1, p, div). XML fokus pada MAKNA DATA dengan tag yang dibuat sendiri sesuai konteks. Sebutkan keduanya turunan SGML — ini menjawab pertanyaan klasik 'bedanya XML dan HTML apa?'. Kalau ada pertanyaan tentang prolog: dokumen tanpa prolog masih well-formed, tetapi prolog sangat disarankan agar encoding UTF-8 eksplisit sehingga karakter non-ASCII tidak salah baca.


---

## Slide 7

SEGMEN 1 · ANATOMI

Anatomi Dokumen XML

XML

<?xml version="1.0" encoding="UTF-8"?>
<!-- daftar mahasiswa TIF2305 -->
<mahasiswaList>
  <mahasiswa nim="221401001">
    <nama>Rina Anggraini</nama>
    <angkatan>2022</angkatan>
  </mahasiswa>
</mahasiswaList>

Prolog

Versi XML dan encoding karakter — tulis UTF-8 secara eksplisit.

Komentar

Diabaikan parser sepenuhnya, hanya untuk pembaca manusia.

Root element

Wajib ada dan tepat satu , membungkus seluruh elemen lain.

Elemen & teks

Tag pembungkus data beserta nilai teks di dalamnya.

Atribut

Metadata penyerta elemen; nilainya wajib diapit tanda kutip.

WEB SEMANTIK · TIF2305

07


### Catatan Pengajar

Bongkar anatomi dokumen sambil menunjuk kode di layar: prolog, komentar, root, elemen, atribut, dan teks. Tekankan ROOT harus TEPAT SATU — analogi satu batang pohon dengan banyak ranting. Tanyakan ke kelas: 'kalau prolog dihapus, apakah masih XML yang sah?' Jawaban: masih well-formed, encoding default UTF-8, tetapi sangat disarankan tetap ditulis. Ingatkan aturan nama tag: boleh mengandung angka dan tanda hubung, tetapi TIDAK boleh diawali angka — produk-01 valid, 01produk tidak.


---

## Slide 8

SEGMEN 1 · PILIHAN DESAIN

Kapan Elemen, Kapan Atribut?

Tidak ada aturan baku — yang ada adalah prinsip praktis dan konsistensi.

ATRIBUT

Untuk kunci identitas atau metadata tentang elemen.

<mahasiswa nim="221401001">

ELEMEN

Untuk data utama yang akan ditampilkan atau diolah lebih lanjut.

<nim>221401001</nim>

KUIS LISAN

Pada <harga mata_uang="IDR">15000</harga> — mengapa mata uang menjadi atribut, sementara nilainya menjadi teks elemen?

WEB SEMANTIK · TIF2305

08


### Catatan Pengajar

Bahas perdebatan klasik elemen vs atribut. Prinsip praktis: DATA yang akan ditampilkan atau diolah lanjut menjadi elemen; METADATA tentang elemen menjadi atribut. Contoh: harga dengan atribut mata_uang. Ajukan kuis lisan: pada mahasiswa nim=... apakah nim seharusnya elemen atau atribut? Jawaban 'benar' tergantung konteks — sebagai kunci identitas cocok jadi atribut, sebagai data yang ditampilkan cocok jadi elemen. Tegaskan tidak ada aturan baku, yang penting konsisten dalam satu skema.


---

## Slide 9

SEGMEN 1 · KASUS KHUSUS

Karakter Khusus dan CDATA

LIMA ENTITY BAWAAN

&lt;

< lebih kecil

&gt;

> lebih besar

&amp;

& ampersand

&quot;

" kutip ganda

&apos;

' kutip tunggal

Gunakan CDATA saat menyisipkan potongan kode atau rumus yang penuh karakter khusus.

WEB SEMANTIK · TIF2305

09


### Catatan Pengajar

Demo cepat: tulis dokumen berisi harga 10 < 20 lalu buka di browser — parser menganggap tanda kurang dari sebagai awal tag baru sehingga muncul error. Perbaiki dengan entity &lt;. Jelaskan lima entity bawaan XML. Untuk CDATA: dipakai kalau kita menyisipkan potongan kode atau rumus. Bedakan dengan komentar — isi komentar diabaikan parser SEPENUHNYA, sedangkan isi CDATA tetap menjadi bagian data teks, hanya karakter khususnya yang tidak diproses.


---

## Slide 10

02

Well-formed vs Valid

25 menit · Slide 10–13

Tujuan: Anda dapat membedakan dua tingkat pengecekan XML dan mengenali kesalahan sintaks yang paling umum. XML tidak memaafkan kesalahan seperti HTML.

WEB SEMANTIK · TIF2305

10


### Catatan Pengajar

Segmen ini berisi kaidah yang paling sering diuji di kuis dan UTS. Tegaskan perbedaan sikap dengan HTML: browser sering 'memaafkan' tag HTML yang tidak ditutup, XML tidak pernah memaafkan. Tujuan segmen: mahasiswa dapat membedakan dua tingkat pengecekan XML dan mengenali kesalahan sintaks umum. Alokasi 25 menit.


---

## Slide 11

SEGMEN 2 · KAIDAH

Enam Aturan Well-formed

Hafalkan keenam aturan ini — akan muncul pada kuis hari ini dan pada UTS.

01

Wajib memiliki tepat satu root element.

02

Setiap tag pembuka wajib memiliki tag penutup.

03

Bersifat case-sensitive: <Nama> ≠ <nama>.

04

Bersarang dengan benar — tidak boleh tumpang tindih.

05

Nilai atribut wajib diapit tanda kutip.

06

Nama tag tidak boleh diawali angka: produk-01 boleh, 01produk tidak.

WEB SEMANTIK · TIF2305

11


### Catatan Pengajar

Perkenalkan enam aturan well-formed dan minta mahasiswa MENGHAFAL — ini bahan kuis dan UTS. Bacakan satu per satu dengan contoh salah di papan tulis untuk setiap aturan. Aturan keempat (bersarang benar, tidak boleh tumpang tindih) adalah yang paling sering keliru: tag a dibuka, tag b dibuka, lalu a ditutup sebelum b. Aturan keenam soal nama tag: boleh mengandung angka, tidak boleh diawali angka.


---

## Slide 12

SEGMEN 2 · LATIHAN

Temukan Empat Kesalahan

Tunjuk kesalahannya sebelum jawabannya dibuka.

XML · tidak well-formed

<profil>
  <Nama>Budi Santoso</nama>
  <mahasiswa nim=221401002>
  <angkatan>2022
  <hobi>Membaca <kota>Medan</hobi></kota>
</profil>

1. Huruf besar-kecil tidak cocok — <Nama> ditutup </nama>.

2. Nilai atribut nim tidak diapit tanda kutip.

3. Tag <angkatan> tidak pernah ditutup.

4. <hobi> dan <kota> bersarang silang.

WEB SEMANTIK · TIF2305

12


### Catatan Pengajar

Latihan aktif: tampilkan kode ini dan minta mahasiswa MENUNJUK empat kesalahan sebelum Anda menyebutkannya. Beri waktu satu sampai dua menit, panggil dua atau tiga mahasiswa. Kunci: (1) tag Nama dibuka dengan huruf besar dan ditutup huruf kecil — case mismatch; (2) atribut nim tanpa tanda kutip; (3) tag angkatan tidak ditutup; (4) tag hobi dan kota bersarang silang. Kalau ada jaringan, buka w3schools.com/xml/xml_validator.asp, tempel kode salah ini, dan tampilkan pesan error aslinya.


---

## Slide 13

SEGMEN 2 · DUA LEVEL

Dua Level Kebenaran XML

Browser hanya memeriksa well-formed. Untuk valid , perlu validator eksternal terhadap skema — dan pertukaran data antar organisasi mensyaratkannya.

WEB SEMANTIK · TIF2305

13


### Catatan Pengajar

Gunakan analogi kalimat: 'Kucing makan pesawat' secara tata bahasa benar (well-formed) tetapi tidak masuk akal menurut kamus fakta (tidak valid). Well-formed = sintaks benar, browser bisa menampilkan pohonnya tanpa error. Valid = struktur dan tipe data sesuai skema eksternal DTD/XSD. Jawab pertanyaan yang sering muncul: browser hanya mengecek well-formed; untuk valid perlu validator eksternal seperti xmllint, oXygen, atau library lxml. Dokumen valid pun belum menjamin kebenaran fakta di dalamnya — itu urusan aplikasi dan manusia. Sistem internal boleh cukup well-formed, tetapi pertukaran data antar organisasi seperti e-Faktur ke DJP WAJIB divalidasi karena ada kontrak formal.


---

## Slide 14

03

DTD & XML Schema

25 menit · Slide 14–17

Tujuan: Anda dapat membaca skema DTD dan XSD sederhana, serta menjelaskan mengapa XSD lebih kuat. Menulis XSD panjang belum diminta semester ini.

WEB SEMANTIK · TIF2305

14


### Catatan Pengajar

Tujuan segmen: mahasiswa dapat MEMBACA skema DTD dan XSD sederhana serta menjelaskan mengapa XSD lebih kuat daripada DTD. Sampaikan sejak awal bahwa mahasiswa TIDAK diminta menulis XSD panjang semester ini — cukup membaca. Kalau kelas kurang responsif, penjelasan DTD bisa dipotong: cukup sebut sebagai skema klasik yang sudah digantikan XSD, lalu lompat ke XSD dan pakai waktu sisanya untuk demo validasi live. Alokasi 25 menit.


---

## Slide 15

SEGMEN 3 · SKEMA KLASIK

DTD: Kontrak Generasi Pertama

DTD

<!ELEMENT katalog (buku+)>
<!ELEMENT buku (judul, tahun, harga?)>
<!ELEMENT judul (#PCDATA)>
<!ELEMENT tahun (#PCDATA)>
<!ELEMENT harga (#PCDATA)>
<!ATTLIST buku isbn CDATA #REQUIRED>

+

Satu atau lebih

*

Nol atau lebih

?

Opsional

DUA KEKURANGAN

Tidak mengenal tipe data — angka dan teks diperlakukan sama. Tidak mendukung namespace. Dua alasan inilah yang melahirkan XSD.

WEB SEMANTIK · TIF2305

15


### Catatan Pengajar

Jelaskan sintaks DTD singkat: !ELEMENT mendefinisikan elemen dan anak-anaknya, !ATTLIST mendaftar atribut. Simbol pengulangan: tanda plus berarti satu atau lebih, tanda bintang nol atau lebih, tanda tanya opsional. Lalu bahas kekurangannya: tidak ada tipe data sehingga angka dan string sama saja, dan tidak mendukung namespace. Karena dua kekurangan inilah W3C membuat XSD pada 2001. Kalau waktu sempit, slide ini boleh dipadatkan menjadi satu kalimat: DTD adalah skema klasik yang sudah digantikan XSD.


---

## Slide 16

SEGMEN 3 · PERBANDINGAN

Kontrak Data: DTD vs XSD

ASPEK

DTD

XSD · STANDAR MODERN

Format

Sintaks khusus yang ringkas

Ditulis sepenuhnya dalam XML

Tipe data

Tidak ada tipe spesifik

string · integer · date · gYear · decimal · boolean

Fitur lanjut

Simbol pengulangan sederhana (+, *, ?)

Namespace, kardinalitas minOccurs/maxOccurs, derivasi tipe

Status

Skema generasi pertama

Rekomendasi W3C sejak 2001

Analogi: XSD adalah skema tabel SQL untuk dokumen — kolom, tipe, dan aturan wajib.

WEB SEMANTIK · TIF2305

16


### Catatan Pengajar

Gunakan tabel ini untuk merangkum mengapa XSD menjadi standar modern. Analogi database: XSD mirip skema tabel SQL — ada kolom, tipe, dan aturan wajib. Antisipasi pertanyaan: mengapa XSD ditulis dalam XML? Supaya bisa diproses tool XML yang sama — parser, XPath — jadi konsisten satu ekosistem. Bahasa skema lain: Relax NG dan Schematron, tetapi XSD tetap dominan di industri; padanan modern untuk data non-XML adalah JSON Schema. Kalau ditanya 'tidak repot?' — repot di awal, aman di produksi, terutama pada domain terregulasi seperti perbankan, pajak, dan kesehatan.


---

## Slide 17

SEGMEN 3 · ANATOMI

Anatomi XML Schema (XSD)

buku.xsd

<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="buku">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="judul" type="xs:string"/>
        <xs:element name="tahun" type="xs:gYear"/>
        <xs:element name="harga" type="xs:decimal"/>
      </xs:sequence>
      <xs:attribute name="isbn" type="xs:string"
                    use="required"/>
    </xs:complexType>
  </xs:element>
</xs:schema>

xs:sequence

Anak elemen harus muncul persis pada urutan tersebut.

type="xs:gYear"

Mencegah data korup — nilai yang bukan tahun ditolak.

use="required"

Atribut isbn mutlak harus ada.

Tantangan: apa yang terjadi bila elemen <tahun> dihapus dari dokumen?

WEB SEMANTIK · TIF2305

17


### Catatan Pengajar

Bacakan skema ini bagian per bagian. Tunjukkan bahwa xs:sequence berarti anak elemen HARUS muncul persis pada urutan itu. Tipe xs:gYear mencegah data korup — input yang bukan format tahun ditolak. Atribut isbn dengan use=required berarti mutlak harus ada. Beri tantangan ke kelas: apa yang terjadi kalau elemen tahun dihapus dari dokumen? Jawaban: gagal validasi, karena minOccurs default bernilai 1. Kalau tersedia waktu dan jaringan, tampilkan XSD asli e-Faktur DJP untuk memberi kesan skema industri.


---

## Slide 18

04

Namespace & XPath

20 menit · Slide 18–20

Identitas kosakata dan cara menavigasinya — bekal langsung untuk JSON-LD pekan depan dan SPARQL di minggu 9–11.

WEB SEMANTIK · TIF2305

18


### Catatan Pengajar

Tujuan segmen: mahasiswa memahami fungsi namespace dan dapat membaca lima sampai enam pola ekspresi XPath dasar. Sampaikan bahwa kedua topik ini adalah bekal langsung untuk pertemuan berikutnya (JSON-LD dengan @context) dan untuk SPARQL di minggu 9 sampai 11. Alokasi 20 menit: sekitar 8 menit namespace, 12 menit XPath.


---

## Slide 19

SEGMEN 4A · IDENTITAS

Namespace: Solusi Bentrok Nama

Bagaimana jika dua kosakata memiliki nama tag yang persis sama?

XML

<katalog xmlns:bk="https://usu.ac.id/ns/buku">
  <bk:title>A Semantic Web Primer</bk:title>
</katalog>

URI pada xmlns hanyalah identifier — tidak perlu bisa dibuka di browser. Wajib pada RDF/XML, SOAP, SVG, dan XSD; muncul lagi sebagai @context di JSON-LD pekan depan.

WEB SEMANTIK · TIF2305

19


### Catatan Pengajar

Masalahnya: dua kosakata berbeda bisa memakai nama tag yang persis sama, misalnya title pada skema buku dan title pada HTML. Solusinya: setiap kosakata diberi URI unik lewat atribut xmlns, lalu dipanggil dengan prefix. Analogi: prefix seperti nama panggilan, URI seperti nama lengkap resmi — beberapa panggilan boleh sama asal nama lengkapnya berbeda. Tegaskan URI di sini murni IDENTIFIER: tidak perlu bisa dibuka di browser dan tidak perlu didaftarkan seperti domain; konvensi memakai bentuk URL hanya karena mudah dijamin unik. Namespace wajib pada RDF/XML, SOAP, SVG, dan XSD — serta akan muncul lagi sebagai @context di JSON-LD pekan depan. Alokasi sekitar 8 menit.


---

## Slide 20

SEGMEN 4B · NAVIGASI

XPath: SQL-nya XML

Sintaksnya menyerupai path berkas pada sistem operasi — indeks dimulai dari 1.

/katalog/buku

Semua <buku> di root katalog.

//judul

Semua <judul> di kedalaman berapa pun.

/katalog/buku[1]

Buku pertama — indeks mulai dari 1.

//buku[@isbn]

Semua buku yang memiliki atribut isbn.

//buku[harga>100000]

Buku dengan harga di atas 100.000.

//buku/pengarang/text()

Nilai teks dari elemen pengarang.

XPath juga menjadi dasar XSLT, XQuery, dan library pengujian otomatis — serta pemanasan menuju SPARQL.

WEB SEMANTIK · TIF2305

20


### Catatan Pengajar

Perkenalkan XPath sebagai 'SQL-nya XML'. Gunakan analogi path file: /katalog/buku sama seperti /home/user/file. Garis miring ganda berarti di kedalaman berapa pun. Tanda kurung siku adalah predikat atau filter. Tanda at adalah awalan untuk atribut. Ingat indeks XPath dimulai dari 1, bukan 0 — ini sering keliru. Jangan mendalami operator lanjutan, cukup enam pola pada tabel. Kalau memungkinkan, demo cepat di Python: from lxml import etree lalu tree.xpath('//judul'). Sebutkan XPath juga dasar dari XSLT, XQuery, dan banyak library pengujian otomatis seperti Selenium. Alokasi sekitar 12 menit.


---

## Slide 21

SINTESIS · STUDI KASUS

Peta Ekosistem XML

RSS feed — berita yang Anda baca setiap hari dikirim sebagai XML.

Layout Android — antarmuka aplikasi ditulis dalam berkas XML.

e-Faktur DJP — negara mewajibkan pelaporan pajak berformat XML.

WEB SEMANTIK · TIF2305

21


### Catatan Pengajar

Gunakan slide ini untuk merangkum keempat segmen menjadi satu bangunan: sintaks sebagai bahan bangunan, well-formed sebagai integritas struktur, DTD/XSD sebagai cetak biru validasi, dan namespace/XPath sebagai sistem navigasi serta identitas. Tunjukkan bahwa XML bukan topik kuliah kuno: buka satu RSS feed berita di browser agar mahasiswa melihat tag XML sungguhan, sebut layout Android bagi yang pernah memakai Android Studio, dan e-Faktur sebagai contoh sistem pemerintahan yang mewajibkan XML.


---

## Slide 22

PRAKTIK MANDIRI · 15 MENIT

Misi: Buat profil_saya.xml

Tulis biodata singkat Anda, buka di browser, lalu unggah ke folder Pertemuan 2 di LMS.

kerangka · profil_saya.xml

<?xml version="1.0" encoding="UTF-8"?>
<!-- profil mahasiswa TIF2305 -->
<profil nim="2214010__">
  <nama>...</nama>
  <angkatan>2022</angkatan>
  <hobi>...</hobi>
  <hobi>...</hobi>
</profil>

KRITERIA PENILAIAN · 100 POIN

40

Well-formed — terbuka di browser tanpa pesan error.

30

Kelengkapan elemen wajib: nama, angkatan, dan minimal dua hobi.

15

Penggunaan atribut nim yang benar.

15

Komentar dan prolog dengan encoding UTF-8.

Uji cepat: tarik berkas ke jendela Chrome — tampil sebagai pohon berarti well-formed.

WEB SEMANTIK · TIF2305

22


### Catatan Pengajar

Beri instruksi teknis singkat: buka Notepad, VS Code, atau editor XML online. Simpan berkas sebagai profil_saya.xml, lalu tarik berkasnya ke jendela Chrome — kalau tampil sebagai pohon berarti well-formed, kalau muncul pesan error merah berarti perlu diperbaiki. Berkeliling membantu satu per satu selama praktik. Setelah sekitar 12 menit, minta satu atau dua mahasiswa menampilkan hasilnya di layar. Ingatkan mengunggah ke folder Pertemuan 2 di LMS. Alokasi 15 menit.


---

## Slide 23

RINGKASAN & PREVIEW

Lima Poin untuk Dibawa Pulang

01

XML adalah markup untuk data, bukan untuk tampilan.

02

Satu dokumen, tepat satu root element.

03

Well-formed adalah soal sintaks; valid adalah soal kesesuaian skema.

04

XSD memberi ketepatan tipe data dan dukungan namespace yang tidak dimiliki DTD.

05

Namespace menjaga identitas kosakata; XPath menavigasinya.

PERTEMUAN 3

JSON-LD sebagai serialisasi RDF modern — @context, @id, @type — dan structured data schema.org.

TUGAS UNTUK PEKAN DEPAN

Baca W3Schools XML Tutorial bagian 1–4, lalu bawa satu berkas XML nyata (RSS, layout Android, atau SVG) untuk dibongkar bersama.

WEB SEMANTIK · TIF2305

24


### Catatan Pengajar

Rangkum lima poin utama secara cepat. Ajak diskusi satu sampai dua menit: 'menurut Anda, mana yang lebih sering dipakai hari ini — XML atau JSON?' Jawabannya JSON, tetapi tekankan XML masih dominan di beberapa domain: pemerintahan, keuangan, dan dokumen publikasi. Sampaikan preview Pertemuan 3: JSON-LD sebagai serialisasi RDF modern (@context, @id, @type), structured data schema.org, dan perbandingan XML vs JSON-LD vs Turtle. PR: baca W3Schools XML Tutorial bagian 1–4; cari satu berkas XML di internet (RSS feed, konfigurasi Android, atau SVG) dan bawa ke kelas untuk dibongkar; siapkan satu pertanyaan tentang JSON-LD. Tutup dengan apresiasi dan ingatkan tenggat unggahan praktik.
