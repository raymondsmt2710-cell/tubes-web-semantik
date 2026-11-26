# Web_Semantik_P9_SPARQL_Dasar


---

## Halaman 1

PERTEMUAN 9 · TIF2305 · SUB-CPMK 5 (BAGIAN 1)
SPARQL Dasar:
Tell & Ask dan Endpoint
Data sudah tersimpan sebagai triple. Hari ini kita belajar menanyakannya: bagaimana SPARQL
mencocokkan pola, cara membaca query, dan cara memanggil endpoint publik maupun graf lokal.

 Mata Kuliah Web Semantik    Program Studi Teknologi Informasi    3 × 50 menit





WEB SEMANTIK · TIF2305 · PERTEMUAN 9


---

## Halaman 2

RENCANA SESI · 125 MENIT
Alur Pertemuan Hari Ini


  10′            25′ · Tell & Ask                 20′ · Membaca query      25′ · Endpoint                  30′ · Live-coding                     15′


  01              10 menit      02              25 menit      03              20 menit      Siapkan sekarang
 Pembuka                  Tell & Ask            Membaca query               Laptop dengan browser modern.
  Recap graf kampus dan             Dunia terbuka dan cara                Sintaks, empat bentuk query,
  pertanyaan pemantik             SPARQL mencocokkan pola          format hasil                        Python 3.10+ lalu jalankan
                                                                                                    pip install rdflib sparqlwrapper

                                                                                                    Berkas kampus.ttl dari Pertemuan  04              25 menit      05              30 menit      06              15 menit
                                                                                                                       6.
 SPARQL endpoint        Live-coding            Penutup
  HTTP, Wikidata, DBpedia,           Lima query: publik, Python,           Etika endpoint, diskusi,             Belum bawa laptop? Duduk
   pilihan hosting                   dan lokal                           ringkasan                           berpasangan.





WEB SEMANTIK · TIF2305 · PERTEMUAN 9


---

## Halaman 3

SUB-CPMK 5 · BAGIAN 1
Setelah Sesi Ini, Anda Mampu…

 01          02          03          04
  Menjelaskan            Menelusuri             Mengenali              Menjalankan

  RDF dan SPARQL sebagai           Cara SPARQL menjawab:           Anatomi query (PREFIX,            Query di endpoint publik dan
   pasangan Tell & Ask,               pencocokan triple pattern,          SELECT, WHERE, FILTER,              graf lokal, dari browser
   termasuk arti hasil kosong           binding variabel, dan join            LIMIT) dan empat bentuk         maupun Python, secara etis.
  dalam dunia terbuka.                   implisit.                             query.


     Dicek: diskusi                           Dicek: latihan tabel                      Dicek: tanya-jawab                      Dicek: live-coding



  Kontrak sesi: OPTIONAL, DISTINCT, dan GROUP BY adalah porsi Pertemuan 10. Hari ini fokus pada cara SPARQL menjawab, membaca
  query, dan menjalankannya.





WEB SEMANTIK · TIF2305 · PERTEMUAN 9


---

## Halaman 4

RECAP · PERTEMUAN 6–7
Graf Kampus yang Sudah Anda Tulis


  TURTLE · KAMPUS.TTL

                                                                                 ex:budi           ex:mengajar           ex:tif2305  @prefix ex:   <https://data.usu.ac.id/kampus#> .
  @prefix foaf: <http://xmlns.com/foaf/0.1/> .

                                                                                     foaf:name                             ex:nama      ex:sks
  ex:budi a ex:Lecturer ;
      foaf:name "Budi Doremi"@id ;
                                                                              "Budi Doremi"                "Web Semantik"                  3      ex:mengajar ex:tif2305 .

  ex:tif2305 a ex:MataKuliah ;
      ex:nama "Web Semantik"@id ;
                                                                Pertanyaan: siapa yang mengajar Web Semantik, dan berapa SKS-      ex:sks 3 .
                                                                nya? Jawab hanya dengan membaca graf.


                                                                Jawaban: Budi Doremi, 3 SKS. Langkahnya: (1) cari node ber-ex:nama
                                                         "Web Semantik", (2) cari siapa terhubung lewat ex:mengajar, (3)
                                                                     ambil foaf:name dan ex:sks. Inilah yang akan diotomatiskan
                                                          SPARQL.




WEB SEMANTIK · TIF2305 · PERTEMUAN 9


---

## Halaman 5

PERTANYAAN PEMANTIK
Dari Enam Triple ke Miliaran Triple

                                            Wikidata menyimpan lebih dari 100 juta item
                                      dan miliaran triple. Bagaimana Anda100 juta+                                   menemukan jawaban di sana?item di Wikidata. Tidak mungkin dibaca dengan mata.


  Data engineer                      Peneliti                         Developer
   Butuh antarmuka stabil untuk pipeline.          Butuh eksplorasi cepat tanpa membangun       Butuh integrasi ke aplikasi.
                                                           aplikasi.  SPARQL: Endpoint HTTP dengan format                                                SPARQL: Library seperti SPARQLWrapper
   hasil standar (JSON, CSV).                   SPARQL: Editor query di browser, hasil          dan rdflib.
                                                langsung tampil.





WEB SEMANTIK · TIF2305 · PERTEMUAN 9


---

## Halaman 6

01
RDF dan SPARQL
sebagai Tell & Ask

25 menit · Tell & Ask · dunia terbuka · posisi di stack · pencocokan
pola




                                                                                                                                               Foto: Erol Ahmed · Unsplash



WEB SEMANTIK · TIF2305 · PERTEMUAN 9


---

## Halaman 7

SEGMEN 2 · KONSEP INTI
Dua Tombol: Catat dan Tanya

                                                                                 Levesque (1984) memandang basis pengetahuan dari dua
    Basis pengetahuan · 6 triple                                                 Reset                                                                                               operasi: TELL menambahkan pernyataan, ASK
                                                                                menanyakannya. Penanya tidak perlu tahu cara datanya
                                                                      "Web Semantik"            disimpan.

                                                                ex:nama                                                                                    TELL · SPARQL UPDATE
             ex:budi          ex:mengajar         ex:tif2305
                                                                                                         Sari mengajar Data Mining
                                                                    ex:sks
             foaf:name                                                                            "3"                                                                                           Budi juga mengajar Data Mining

          "Budi Doremi"
                                                                                                         Sari mengajar Web Semantik

                                                                        ASK · SPARQL QUERY

                                                                                  Apakah Budi mengajar Data Mining?

                                                                                            Siapa saja yang mengajar Web Semantik?





WEB SEMANTIK · TIF2305 · PERTEMUAN 9


---

## Halaman 8

SEGMEN 2 · MEMBACA JAWABAN
Jawaban “Tidak” Belum Tentu Berarti Salah


  SPARQL · GRAF KAMPUS.TTL
                                                   Jalankan
  ASK { ex:budi ex:mengajar ex:tif2410 }




   ASUMSI DUNIA TERTUTUP                                             ASUMSI DUNIA TERBUKA
  Basis data relasional                      Web Semantik
   Yang tidak ada di tabel dianggap salah. Tabel jadwal adalah daftar          Yang tidak tercatat berarti tidak diketahui. Tafsir yang tepat: “graf
   lengkap, jadi “Budi tidak mengajar TIF2410”.                                        ini tidak mencatat bahwa Budi mengajar TIF2410”.



  Konsekuensi praktis: SPARQL mengevaluasi query terhadap graf yang ada, tetapi data Web tidak pernah lengkap. Hitungan dari Wikidata
  adalah jumlah yang tercatat, bukan jumlah di dunia nyata.





WEB SEMANTIK · TIF2305 · PERTEMUAN 9


---

## Halaman 9

SEGMEN 2 · POSISI DI STACK
SPARQL Duduk Tepat di Atas RDF

                Aplikasi dan antarmuka                                                         SPARQL 1.0 menjadi W3C Recommendation (Januari 2008).                    2008
          OWL · aturan · inferensi
                                                         SPARQL 1.1: sebelas dokumen, antara lain Query, Update,                    2013          SPARQL — bahasa Ask                                     Protocol, format hasil, dan federated query. Versi yang
                                                                     dipakai kelas ini.
          RDFS — kosakata dan skema
                                                         SPARQL 1.2 masih Working Draft, mengikuti RDF 1.2 yang                    2026          RDF — model data, sisi Tell                             memperkenalkan triple term (penerus RDF-star dari
                                                               Pertemuan 7).
              IRI · Unicode · serialisasi

                                                               Tiga dokumen yang perlu Anda kenal: Query Language (sintaks), Protocol
                                                            (pengiriman lewat HTTP), Query Results JSON Format (bentuk jawaban).





WEB SEMANTIK · TIF2305 · PERTEMUAN 9


---

## Halaman 10

SEGMEN 2 · CARA SPARQL MENJAWAB
Triple Pattern: Triple yang Berlubang

                                                                                         Pola 1     Pola 2     Pola 3

                                                      ?dosen  ex:mengajar  ?mk  .

         ex:budi       ex:mengajar       ex:tif2305
                                                                                      Pindai graf
                                                    ex:nama


                                                     "Web Semantik"

                    ex:mengajar



         ex:sari       ex:mengajar       ex:tif2410

                                                    ex:nama

                                                     "Data Mining"

                                                                                       Solution mapping = satu cara mengisi lubang. Satu solution = satu
                                                                                                baris hasil.



WEB SEMANTIK · TIF2305 · PERTEMUAN 9


---

## Halaman 11

SEGMEN 2 · CONTOH DITELUSURI
Variabel Bersama Menjadi Join Implisit


  SPARQL · DATA LATIHAN

  SELECT ?dosen ?namaMK WHERE {
    ?dosen ex:mengajar ?mk .      # pola 1
    ?mk    ex:nama     ?namaMK .  # pola 2
  }


  Pola 1 · 3 baris                           Pola 2 · 2 baris                            Hasil · 3 baris

   ?dosen         ?mk                          ?mk               ?namaMK                   ?dosen        ?namaMK

   ex:budi        ex:tif2305                  ex:tif2305      "Web Semantik"           ex:budi      "Web Semantik"

                                                                                       ex:sari      "Data Mining"   ex:sari        ex:tif2410                  ex:tif2410      "Data Mining"

                                                                                       ex:sari      "Web Semantik"   ex:sari        ex:tif2305



  Gabungkan baris yang nilai ?mk-nya sama. Warna yang sama         Nol baris bukan error. Query sah, tetapi tidak ada pengisian yang
   berarti node yang sama. Tidak ada kata JOIN: menulis ?mk di dua      memenuhi semua pola. Urutan pola juga bebas: hasilnya sama.
  pola sudah berarti “harus node yang sama”.

WEB SEMANTIK · TIF2305 · PERTEMUAN 9


---

## Halaman 12

LATIHAN BERPASANGAN · 5 MENIT
Tebak Hasilnya, Lalu Biarkan Mesin Menjawab
Pakai data latihan lima triple: budi→tif2305, sari→tif2410, sari→tif2305, tif2305 “Web Semantik”,
tif2410 “Data Mining”.

 A            B             C

    SPARQL                                       SPARQL                                       SPARQL

     SELECT ?mk WHERE {                          SELECT ?dosen WHERE {                       SELECT ?a ?b WHERE {
       ex:budi ex:mengajar ?mk .                   ?dosen ex:mengajar ?mk .                    ?a ex:mengajar ?mk .
       ex:sari ex:mengajar ?mk .                   ?mk ex:nama "Data Mining" .                 ?b ex:mengajar ?mk .
     }                                           }                                           }

  Berapa baris hasilnya?                      Berapa baris hasilnya?                      Berapa baris hasilnya?

                  Periksa                                          Periksa                                          Periksa





WEB SEMANTIK · TIF2305 · PERTEMUAN 9


---

## Halaman 13

02
Membaca Query
SPARQL

20 menit · anatomi · sintaks · empat bentuk query · format hasil ·
SPARQL dan SQL




                                                                                                                                               Foto: Jon Tyson · Unsplash



WEB SEMANTIK · TIF2305 · PERTEMUAN 9


---

## Halaman 14

SEGMEN 3 · ANATOMI QUERY
Lima Bagian yang Selalu Anda Temui
Klik setiap bagian untuk menyorotnya di query.

  SPARQL · WIKIDATA                                                        PREFIX
                                                                                                                 Alias namespace, sama seperti @prefix di Turtle, tetapi
  PREFIX wd:   <http://www.wikidata.org/entity/>                                   tanpa @ dan tanpa titik di akhir.
  PREFIX wdt:  <http://www.wikidata.org/prop/direct/>
  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>                     SELECT
                                                                                                            Variabel yang menjadi kolom hasil.
  SELECT ?kota ?namaKota
                                                                        WHERE  WHERE {
                                                                                                      Basic graph pattern yang dicocokkan ke graf. Titik koma
    ?kota wdt:P31 wd:Q515 ;    # instance of: city                                                                                    memakai ulang subjek ?kota.
          wdt:P17 wd:Q252 ;    # country: Indonesia
          rdfs:label ?namaKota .                                                                        FILTER
    FILTER ( LANG(?namaKota) = "id" )                                         Membuang solution yang tidak memenuhi syarat. Bekerja
  }                                                                                                     setelah pencocokan pola.
  LIMIT 25
                                                                        LIMIT
                                                                                                 Batas jumlah baris. Wajib saat eksplorasi endpoint publik.

                                                                                   Buka di Wikidata Query Service




WEB SEMANTIK · TIF2305 · PERTEMUAN 9


---

## Halaman 15

SEGMEN 3 · SINTAKS
Dari Pernyataan ke Pertanyaan
Sebagian besar sintaks SPARQL diwarisi dari Turtle. Yang baru hanya variabel dan kata kunci query.

  ex:budi ex:mengajar ex:tif2305 .


     1 · Lubangi subjeknya     2 · Tambah pola nama     3 · Jalankan di kampus.ttl     Coba tanpa @id      Ulang

     Ini sebuah pernyataan (Tell). Klik tombol 1 untuk mengubahnya menjadi pertanyaan.





  ?var atau $var    <IRI penuh>    prefix:nama    "teks"@id    "3"^^xsd:integer    a = rdf:type       ; dan , seperti Turtle   # komentar





WEB SEMANTIK · TIF2305 · PERTEMUAN 9


---

## Halaman 16

SEGMEN 3 · BENTUK QUERY
Empat Cara Bertanya, Empat Bentuk Jawaban

  SELECT     ASK     CONSTRUCT     DESCRIBE


  SPARQL · DATA LATIHAN
                                                                          HASIL · DIJALANKAN LANGSUNG

  SELECT ?dosen ?namaMK WHERE {                                                                        #      ?dosen            ?namaMK
    ?dosen ex:mengajar ?mk .
                                                                    1     ex:sari          "Web Semantik"    ?mk ex:nama ?namaMK .
  }                                                                    2     ex:sari          "Data Mining"

                                                                    3     ex:budi          "Web Semantik"→ tabel binding. Paling sering dipakai. Dibahas lebih dalam di
Pertemuan 10.


Bagian WHERE-nya sama: semuanya memakai pencocokan pola. Sisi Tell di
SPARQL adalah SPARQL Update (INSERT DATA, DELETE DATA).





WEB SEMANTIK · TIF2305 · PERTEMUAN 9


---

## Halaman 17

SEGMEN 3 · PERBANDINGAN
Mirip SQL di Permukaan, Berbeda di Dalam


  SQL · JOIN EKSPLISIT
                                                              ASPEK          SQL               SPARQL

  SELECT d.nama, m.nama                                                                  Model              tabel, baris, kolom     graf triple
  FROM mengajar g
  JOIN dosen d ON g.dosen_id = d.id                                                           Skema            wajib di depan        opsional
  JOIN matkul m ON g.mk_id = m.id;
                                                                               Identitas         primary key lokal      IRI global

  SPARQL · JOIN LEWAT VARIABEL BERSAMA
                                                                            Join            JOIN … ON            variabel bersama
  SELECT ?nama ?namaMK WHERE {
                                                                                        Nilai tak ada     NULL                   triple tidak ada    ?d  ex:mengajar ?mk ; foaf:name ?nama .
    ?mk ex:nama ?namaMK .
                                                                       Ketiadaan        dunia tertutup        dunia terbuka  }

                                                                               Lintas sumber    ETL dulu           SERVICE (federasi)

                                                                               Hasil              tabel                  tabel, boolean, graf





WEB SEMANTIK · TIF2305 · PERTEMUAN 9


---

## Halaman 18

03
SPARQL Endpoint

25 menit · layanan HTTP yang menerima query SPARQL dan
mengembalikan hasil dalam format standar





                                                                                                                                               Foto: Valentin Lacoste · Unsplash



WEB SEMANTIK · TIF2305 · PERTEMUAN 9


---

## Halaman 19

SEGMEN 4 · SPARQL 1.1 PROTOCOL
Dikirim lewat HTTP, Dijawab sesuai Permintaan


        Klien                    Permintaan                   Endpoint                     Triple store
    browser · curl · Python                 GET ?query=… · Accept                        satu URL …/sparql                      mencocokkan pola




Header Accept:   application/sparql-results+json     application/sparql-results+xml     text/csv     text/tab-separated-values     Kirim


PERMINTAAN                                                  RESPONS · DARI DATA LATIHAN

  GET /sparql?query=PREFIX%20ex%3A%20%20%20%3Chttps%3A%2F%2Fdat        {
  a.usu.ac.id%2Fkampus%23%3E%0ASELECT%20%3Fdosen%20%3FnamaMK%20W         "head": {
  HERE%20%7B%20%3Fdosen%20ex%3Amengajar%20%3Fmk%20.%20%3Fmk%20e            "vars": [
  x%3Anama%20%3FnamaMK%20%7D HTTP/1.1                                        "dosen",
  Accept: application/sparql-results+json                                    "namaMK"
  User-Agent: KelasWebSemantik/1.0 (email@kampus.ac.id)                    ]
                                                                         },
                                                                         "results": {
                                                                           "bindings": [
                                                                             {
                                                                               "dosen": {



WEB SEMANTIK · TIF2305 · PERTEMUAN 9


---

## Halaman 20

SEGMEN 4 · COBA DI TERMINAL ANDA
Rakit Permintaan, Salin, Jalankan

  Wikidata                   application/sparql-results+json       BASH · MACOS / LINUX / GIT BASH

                                                   curl -G "https://query.wikidata.org/sparql" \
  ASK { wd:Q3630 wdt:P17 wd:Q252 }
                                                     -H "Accept: application/sparql-results+json" \
                                                     -H "User-Agent: KelasWebSemantik/1.0 (email@kampus.ac.id)" \
                                                     --data-urlencode "query=ASK { wd:Q3630 wdt:P17 wd:Q252 }"


                                                                 Salin perintah     Buka di browser
  Jakarta di Indonesia?     Jakarta di Jepang?

                                                 -G mengirim sebagai GET, --data-urlencode meng-encode query. Tambahkan -i  Label Jakarta
                                                      untuk melihat kode status. Hapus satu kurung kurawal untuk melihat status 400.
Q3630 = Jakarta, Q252 = Indonesia, Q17 = Jepang, P17 = country.
Windows PowerShell: ketik curl.exe dan tulis dalam satu baris.





WEB SEMANTIK · TIF2305 · PERTEMUAN 9


---

## Halaman 21

SEGMEN 4 · MEMBACA RESPONS
Kode Status Memberi Tahu Apa yang Salah
Klik setiap kartu untuk membaliknya.


        0 baris                                        di DBpedia                          Bad Request 200                  200                  400

  Query sah, pola tidak cocok.                Bisa hasil parsial bila timeout.              Sintaks query salah.
  Debug pola, bukan sintaks.                     Cek header X-SQL-State; perkecil query.           Baca pesan error; cek kurung, titik, PREFIX.


         Forbidden                              Too Many Requests                                Server error 403                  429                  500/503

  Permintaan ditolak.                      Rate limit terlampaui.                       Error server atau batas waktu.
   Isi User-Agent sesuai kebijakan endpoint.           Hentikan loop, tunggu (Retry-After), cache          Sederhanakan, tambah LIMIT, coba lagi.
                                                               hasil.


  Paling berbahaya adalah 200 yang menyesatkan: tanpa error, tetapi datanya kosong atau terpotong. Selalu periksa jumlah baris sebelum
  memakai hasil.




WEB SEMANTIK · TIF2305 · PERTEMUAN 9


---

## Halaman 22

SEGMEN 4 · ENDPOINT UTAMA
Cara Wikidata Menyimpan Fakta

                                                              ID yang sering dipakai
       wd:Q3630 · Jakarta           wdt:P17 (negara)          wd:Q252 · Indonesia
                                                                                         Q252 Indonesia    Q3630 Jakarta

                                                                                         Q515 city    Q3918 university

                                                                                         Q4022 river    Q5 human
wd:                 Entitas: item (Q…) dan properti (P…)
                                                                                         P31 instance of    P279 subclass of
wdt:                 Nilai langsung “truthy”, peringkat terbaik                                                                                         P17 country    P131 located in

p: ps: pq:      Pernyataan lengkap beserta kualifier (Pertemuan 10–11)                 P1082 population    P2043 length
                                                                                                                 Cari ID di wikidata.org, atau di editor query ketik
rdfs:label    Nama manusiawi, satu per bahasa                                   wd: lalu tekan Ctrl+Space.





WEB SEMANTIK · TIF2305 · PERTEMUAN 9


---

## Halaman 23

SEGMEN 4 · QUERY.WIKIDATA.ORG
Endpoint Publik Juga Berubah


                                                                      query.wikidata.org 60 detik
   batas waktu per query


Editor dengan autocomplete, tombol Run, panel
Examples, dan tampilan tabel, peta, timeline, serta
graf. Prefix wd: wdt: wikibase: bd: sudah
tersedia.

  Januari 2026: graph split      Ganti mesin

  Ulang





WEB SEMANTIK · TIF2305 · PERTEMUAN 9


---

## Halaman 24

SEGMEN 4 · DBPEDIA.ORG/SPARQL
DBpedia: Wikipedia sebagai Graf

 10.000       120 detik     50
   baris maksimum per hasil                       batas waktu eksekusi                           koneksi paralel per IP


dbo:    Ontologi DBpedia: properti terpetakan dan                                         Satu IRI, dua representasi
          bersih.
                                                                    Accept: text/html     Accept: text/turtle
dbp:    Properti mentah dari infobox.
                                                                                        dbpedia.org/page/Medan
dbr:   Satu IRI untuk satu artikel Wikipedia.            About: Medan
                                                          Halaman HTML untuk manusia: tabel properti dan nilai.





                                                                                      Ilustrasi diringkas. Ini prinsip Linked Data dari Pertemuan 5: server mengarahkan klien ke
                                                                           representasi sesuai header Accept.




WEB SEMANTIK · TIF2305 · PERTEMUAN 9


---

## Halaman 25

SEGMEN 4 · KEPUTUSAN ARSITEKTUR
Di Mana Graf Anda Akan Ditanya?
Pilih skenario, lalu lihat pilihan yang paling masuk akal.


  Tugas kelas, graf kecil      Aplikasi web kampus dengan data internal      Riset film memakai data publik


  Endpoint publik                   Triple store sendiri               Lokal di program
   Wikidata, DBpedia                                Apache Jena Fuseki, GraphDB, Virtuoso, QLever            rdflib di Python

  + Gratis, data besar siap pakai.               + Data internal, kontrol penuh atas batas        + Tanpa server dan jaringan, cocok untuk
  − Batas waktu, rate limit, tidak untuk data        dan akses.                                             belajar.
   privat.                                  − Operasional, backup, keamanan, biaya        − Graf di memori; tidak untuk data besar
                                                         server.                                        atau banyak pengguna.





WEB SEMANTIK · TIF2305 · PERTEMUAN 9


---

## Halaman 26

04
Live-Coding Lima
Query

30 menit · A Wikidata · B DBpedia · C Python ke endpoint · D graf lokal
· E Tell & Ask lokal




                                                                                                                                               Foto: Mohammad Rahmani · Unsplash



WEB SEMANTIK · TIF2305 · PERTEMUAN 9


---

## Halaman 27

SEGMEN 5 · QUERY A DAN B
Bertanya ke Wikidata dan DBpedia

A · Sepuluh kota terpadat di Indonesia           B · Film sutradara Christopher Nolan

  SPARQL · WIKIDATA                                                  SPARQL · DBPEDIA

  SELECT ?kota ?namaKota ?populasi WHERE {                          PREFIX dbo: <http://dbpedia.org/ontology/>
    ?kota wdt:P31/wdt:P279* wd:Q515 ;                               PREFIX dbr: <http://dbpedia.org/resource/>
          wdt:P17 wd:Q252 ;                                         SELECT ?film ?judul ?tahun WHERE {
          wdt:P1082 ?populasi ;                                       ?film a dbo:Film ;
          rdfs:label ?namaKota .                                            dbo:director dbr:Christopher_Nolan ;
    FILTER ( LANG(?namaKota) = "id" )                                       rdfs:label ?judul ;
  }                                                                         dbo:releaseDate ?rilis .
  ORDER BY DESC(?populasi)                                            BIND ( YEAR(?rilis) AS ?tahun )
  LIMIT 10                                                            FILTER ( LANG(?judul) = "en" )
                                                                    }
wdt:P31/wdt:P279* = instance of, lalu subclass of nol kali atau lebih. Amati:      ORDER BY ?tahun
ada kota yang muncul dua kali? Ada yang hilang?
                                                               a = rdf:type, BIND membuat variabel turunan. Bandingkan dengan filmografi di
  Jalankan di Wikidata                                                        Wikipedia: adakah yang tidak muncul?

                                                                      Jalankan di DBpedia





WEB SEMANTIK · TIF2305 · PERTEMUAN 9


---

## Halaman 28

SEGMEN 5 · QUERY C
Endpoint yang Sama, Dipanggil dari Kode


  PYTHON · PIP INSTALL SPARQLWRAPPER                                                                           agent=UA
                                                                                                    User-Agent bermakna: nama aplikasi dan  from SPARQLWrapper import SPARQLWrapper, JSON
                                                                                                           kontak.

  UA = "KelasWebSemantik/1.0 (email@kampus.ac.id)"
  sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent=UA)                 JSON
  sparql.setReturnFormat(JSON)                                                                Format hasil standar W3C.
  sparql.setQuery("""
  SELECT ?kotaLabel ?populasi WHERE {                                             bindings
    ?kota wdt:P31/wdt:P279* wd:Q515 ; wdt:P17 wd:Q252 ;                                        Satu dict per baris; nilai di ["value"].
          wdt:P1082 ?populasi .
    SERVICE wikibase:label { bd:serviceParam wikibase:language "id". }                                                                           wikibase:label
  } ORDER BY DESC(?populasi) LIMIT 5""")
                                                                                                           Ekstensi khusus Wikidata, bukan SPARQL
                                                                                                                standar.
  hasil = sparql.queryAndConvert()
  for b in hasil["results"]["bindings"]:
                                                                                                                         Salin kode    Unduh query_c.py      print(b["kotaLabel"]["value"], b["populasi"]["value"])





WEB SEMANTIK · TIF2305 · PERTEMUAN 9


---

## Halaman 29

SEGMEN 5 · QUERY D DAN E
Lab Graf Lokal: kampus.ttl di Browser
Mesin SPARQL berjalan di halaman ini, tanpa server. Pilih langkah, jalankan, lalu ubah query sesuka
Anda.


 D · SELECT    E1 · ASK    E2 · INSERT DATA    E3 · ASK lagi                                                           6 triple    Reset graf


  PREFIX ex:   <https://data.usu.ac.id/kampus#>                                                                1 baris
  PREFIX foaf: <http://xmlns.com/foaf/0.1/>
  SELECT ?nama ?namaMK ?sks WHERE {                                      #   ?nama           ?namaMK          ?sks
    ?dosen ex:mengajar ?mk ;
                                                                           "Budi          "Web
                                                                                                                                      ^^xsd:integer           foaf:name   ?nama .                                         1                                  "3"                                                                           Doremi" @id     Semantik" @id
    ?mk    ex:nama     ?namaMK ;
           ex:sks      ?sks .
  }





  Jalankan    Ctrl/⌘ + Enter



WEB SEMANTIK · TIF2305 · PERTEMUAN 9


---

## Halaman 30

SEGMEN 5 · DEBUGGING
Tantangan: Kenapa Hasilnya Kosong?
Query ini sah tetapi menghasilkan nol baris pada kampus.ttl. Perbaiki sampai keluar hasil.


                                                                         PERIKSA BERURUTAN
  PREFIX ex:   <http://usu.ac.id/kampus#>
                                                                                                         Uji tiap triple pattern sendiri dengan LIMIT 5.  PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                                                                         Cek IRI dan PREFIX huruf demi huruf: http atau https, # atau /.
  SELECT ?nama ?namaMK WHERE {
                                                                         Cek literal: tag bahasa dan tipe data harus sama persis.    ?dosen ex:mengajar ?mk ;
           foaf:name ?nama .                                                                              Lepas FILTER, lalu pasang kembali satu per satu.
    ?mk    ex:nama ?namaMK .
    FILTER ( ?namaMK = "Web Semantik" )                                           Lihat datanya langsung: ex:budi ?p ?o.
  }





  Jalankan      Petunjuk     Ulang




WEB SEMANTIK · TIF2305 · PERTEMUAN 9


---

## Halaman 31

SEGMEN 6 · ETIKA ENDPOINT
Lima Aturan Main di Endpoint Publik
Endpoint publik dipakai bersama ribuan pengguna dan dibiayai pihak lain.

 1        2        3        4        5
  LIMIT               User-Agent         Cache               Kebijakan            Lisensi

   Selalu pakai LIMIT saat            Isi nama aplikasi dan          Simpan hasil ke berkas.        Baca batas tiap                 Wikidata CC0; DBpedia
   eksplorasi.                     kontak, agar pengelola          Seribu query kecil              endpoint sebelum query       CC BY-SA, wajib atribusi
                                    bisa menghubungi,             sebaiknya menjadi satu         massal; hormati Retry-            bila dipublikasikan
                              bukan memblokir.               query.                              After.                           ulang.



  Untuk riset: catat tanggal pengambilan data dan query yang dipakai. Wikidata berubah setiap menit, jadi hasil yang sama tidak bisa diulang
  tanpa catatan ini.





WEB SEMANTIK · TIF2305 · PERTEMUAN 9


---

## Halaman 32

SEGMEN 6 · DISKUSI · 5 MENIT
Dua Pertanyaan untuk Dibawa Pulang
Dua menit refleksi sendiri, tiga menit berbagi dengan pasangan. Klik “Lihat arah” setelah berdiskusi.

 01                    02
  SPARQL sering disebut “SQL untuk graf”. Di titik      Wikidata sedang mengganti mesin query-nya.
  mana analogi itu pecah, dan apa akibatnya bagi       Jika kampus ingin datanya bisa di-query seperti
  cara Anda membaca hasil?                          Wikidata, keputusan arsitektur apa yang diambil
                                                  pertama, dan apa risikonya?


     Lihat arah                                                                           Lihat arah





WEB SEMANTIK · TIF2305 · PERTEMUAN 9


---

## Halaman 33

RINGKASAN
Lima Hal yang Anda Bawa dari Hari Ini


      RDF adalah sisi Tell, SPARQL sisi Ask. Jawaban kosong atau false dibaca sebagai “tidak tercatat”.01

       SPARQL menjawab dengan mencocokkan triple pattern. Variabel bersama adalah join; satu solution adalah02
        satu baris.


       Anatomi tetap: PREFIX, bentuk query (SELECT, ASK, CONSTRUCT, DESCRIBE), WHERE, lalu modifier.03

        Endpoint adalah HTTP biasa: query lewat GET atau POST, format lewat Accept, dan kode status harus04
         dibaca.


       Query standar yang sama berjalan di endpoint publik, triple store sendiri, dan rdflib lokal.05





WEB SEMANTIK · TIF2305 · PERTEMUAN 9


---

## Halaman 34

TINDAK LANJUT
Sebelum Pertemuan 10

  PERTEMUAN 10                                       Pekerjaan rumah
 SPARQL SELECT Query                                  Ulangi Query A–E di laptop Anda.
  OPTIONAL untuk film Nolan yang hilang, DISTINCT untuk kota yang                                                                       Baca A Semantic Web Primer, bab tentang querying (SPARQL).
  muncul dua kali, ORDER BY, LIMIT/OFFSET, GROUP BY dan COUNT,
                                                                         Pasang pandas: pip install pandas.   plus ekspor hasil ke pandas.

                                                                                  Catat satu pertanyaan yang ingin Anda ajukan ke Wikidata.




  REFERENSI
   Antoniou, Groth, van Harmelen & Hoekstra (2012), A Semantic Web Primer, 3rd ed., MIT Press · Levesque (1984), Foundations of a functional approach to knowledge
   representation, Artificial Intelligence 23(2) · W3C (2013), SPARQL 1.1 Query Language, Protocol, Query Results JSON Format · Wikidata, WDQS graph split & backend update
   (2025–2026) · DBpedia, Querying DBpedia · RDFLib documentation.





WEB SEMANTIK · TIF2305 · PERTEMUAN 9


---

## Halaman 35

PENUTUP · TANYA-JAWAB
Pertanyaan apa yang ingin Anda
ajukan ke Wikidata malam ini?

Tulis pertanyaannya dalam bahasa manusia, lalu coba ubah menjadi pola triple: apa subjeknya,
propertinya, dan apa yang menjadi variabel?


 RDF mencatat    SPARQL bertanya    Sampai jumpa di Pertemuan 10





WEB SEMANTIK · TIF2305 · PERTEMUAN 9
