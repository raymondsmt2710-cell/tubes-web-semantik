# Web_Semantik_P11_CONSTRUCT_Hierarki


---

## Halaman 1

PERTEMUAN 11 · TIF2108 · SUB-CPMK 6 (BAGIAN 1)
CONSTRUCT dan
Hierarki Data

Pekan lalu Medan muncul dua kali karena jalur kelas yang belum kita pahami, dan tabel CSV kehilangan
identitas datanya. Hari ini jawaban query kita berupa graf baru, dan hierarki kelas kita telusuri dengan
property path.

 Mata Kuliah Web Semantik    Program Studi Teknologi Informasi    3 SKS · 150 menit





WEB SEMANTIK · TIF2108 · PERTEMUAN 11


---

## Halaman 2

RENCANA SESI · 150 MENIT
Alur Pertemuan Hari Ini


 10 mnt     25 mnt · CONSTRUCT     20 mnt · Kosakata    35 mnt · Hierarki                40 mnt · Live-coding                 20 mnt · Penutup


  01              10 menit      02              25 menit      03              20 menit      Siapkan sekarang
 Pembuka              Anatomi               Menyelaraskan                Laptop dengan browser modern.
  Dua sisa pekerjaan dari       CONSTRUCT            kosakata
  Pertemuan 10                                                                                     Python 3.10+ lalu jalankan                                         Dari solution menjadi triple         UNION, jalur |, VALUES,
                                                                                                    pip install rdflib sparqlwrapper                                                                     schema.org

                                                                                                    Berkas film.ttl, kota.ttl, dan kampus.ttl
  04              35 menit      05              40 menit      06              20 menit            dari LMS.
  Hierarki                Live-coding            Penutup                                                                                         Belum bawa laptop? Duduk
   Property path + * ? / ^ dan         WDQS, DBpedia, rdflib, Turtle         Etika endpoint, diskusi,                                                                                                      berpasangan.
   materialisasi                                                            ringkasan





WEB SEMANTIK · TIF2108 · PERTEMUAN 11


---

## Halaman 3

SUB-CPMK 6 · BAGIAN 1
Setelah Sesi Ini, Anda Mampu…

 01          02          03          04
  Menjelaskan           Menyusun              Menelusuri             Mengintegrasikan

   Berapa triple yang lahir dari        CONSTRUCT yang                     Hierarki kelas dengan                Graf hasil endpoint ke rdflib:
   sebuah CONSTRUCT, dan          memetakan data ke kosakata        operator jalur +, *, ?, /, ^, dan        disimpan sebagai Turtle dan
  mengapa berbeda dari jumlah         sendiri, termasuk               membedakan hasilnya.              di-query ulang secara lokal.
   baris SELECT.                    menyatukan predikat
                                     berbeda.


     Dicek: latihan                           Dicek: Demo B                           Dicek: latihan                           Dicek: live-coding



  Kontrak sesi: hari ini triple baru diturunkan dengan aturan yang kita tulis sendiri di query. Mesin yang menurunkan triple dari aturan RDFS
  dan OWL adalah porsi Pertemuan 12. INSERT dan UPDATE ke endpoint tidak dibahas.





WEB SEMANTIK · TIF2108 · PERTEMUAN 11


---

## Halaman 4

RECAP · PERTEMUAN 10
Dua Sisa Pekerjaan dari Pekan Lalu



    QUERY A · WIKIDATA                                                 DISKUSI 2 · CSV

     ?kota wdt:P31/wdt:P279* wd:Q515 ;                                 namaKota,populasi
           wdt:P17 wd:Q252 ;                                           Medan,2435252
           wdt:P1082 ?populasi .                                       Medan,2097610

  Jalur kelas yang menggandakan Medan             Tabel yang kehilangan identitas

   Kita memakai P279* sejak Pertemuan 9 tanpa pernah membahas         Kolom nama tanpa IRI tidak bisa digabung lagi dengan sumber lain
   hierarki di baliknya.                                                    secara pasti.

    Dijawab di Segmen 04: property path                                          Dijawab di Segmen 02: CONSTRUCT



  Petunjuk dari Pertemuan 10: tabel adalah daftar solution, dan satu entitas bisa mengisi beberapa baris. Graf adalah himpunan triple.





WEB SEMANTIK · TIF2108 · PERTEMUAN 11


---

## Halaman 5

PERTANYAAN PEMANTIK
Bagaimana Jika Jawabannya Berupa Graf?

Selama dua pekan jawaban query kita berupa tabel. Apa yang berubah bila jawaban itu berupa triple
yang langsung bisa disimpan, digabung, dan di-query lagi?


  Bentuk                         Kosakata                         Hierarki

   Template triple menggantikan daftar              Tiga predikat berbeda untuk arti yang            Subkelas dari subkelas, sedalam apa pun.
   kolom.                                     sama.                                                kota.ttl · ?x a/rdfs:subClassOf* ex:Kota

   film.ttl · 3 solution × 2 pola template               foaf:name · rdfs:label · schema:name
                          2    1
                                                                                             Medan di SELECT      Medan di CONSTRUCT 6   5        3   1                                                                                                                                          (baris)                      (triple)   cetakan triple    triple di graf                               predikat sumber   properti keluaran
                                                                                                         Akibat: satu kota, dua jalur ke Kota; graf   Akibat: cetakan kembar Memento a                 Akibat: satu properti milik kita sendiri.
                                                                                      menyimpannya sekali.  ex:Film tersimpan sekali.





WEB SEMANTIK · TIF2108 · PERTEMUAN 11


---

## Halaman 6

01
Anatomi CONSTRUCT

25 menit · template triple · solution menjadi triple · variabel tak terikat
· studi kasus museum





                                                                                                                                               Foto: Iana Klimenko · Unsplash



WEB SEMANTIK · TIF2108 · PERTEMUAN 11


---

## Halaman 7

SEGMEN 2 · BENTUK QUERY
WHERE yang Sama, Keluaran Berbeda
Ganti bentuk query. WHERE tidak berubah; yang berubah hanya apa yang dikeluarkan untuk setiap
solution.


  SELECT ?f ?r    CONSTRUCT { … }
                                                                       3 baris   Tabel: satu baris per solution.

  SPARQL · DATA CONTOH FILM                                                                       #     ?f                           ?r

  SELECT ?f ?r WHERE {                                               1     dbr:Following              1998-09-12
    ?f dbo:director dbr:Christopher_Nolan ;
                                                                    2     dbr:Memento                2000-09-05       dbo:releaseDate ?r .
  }                                                                    3     dbr:Memento                2001-03-16
  ORDER BY ?r

                                                                       Tiga baris, lima triple. Dari mana angka lima? Adegan
                                                                          berikutnya mencetaknya satu per satu.





WEB SEMANTIK · TIF2108 · PERTEMUAN 11


---

## Halaman 8

SEGMEN 2 · ANATOMI CONSTRUCT
Empat Blok, Satu Template
Klik setiap blok untuk menyorot bagiannya di query.

  SPARQL · CONSTRUCT                                                1 · PREFIX
                                                                     Sama seperti SELECT. ex: adalah namespace milik kita.
  PREFIX dbo: <http://dbpedia.org/ontology/>
  PREFIX dbr: <http://dbpedia.org/resource/>                                                                2 · CONSTRUCT { … }
  PREFIX ex:  <http://contoh.id/>                                                                                       Template: hanya triple berisi variabel. Tanpa FILTER, OPTIONAL,
                                                                                        atau fungsi.
  CONSTRUCT {
    ?f a ex:Film ;                                                                3 · WHERE { … }
       ex:rilis ?r .                                                        Menentukan solution, persis seperti di SELECT.
  }
  WHERE {                                                        4 · Modifier
    ?f dbo:director dbr:Christopher_Nolan ;                                LIMIT dan ORDER BY bekerja pada solution, bukan pada triple.
       dbo:releaseDate ?r .
  }
  LIMIT 100





WEB SEMANTIK · TIF2108 · PERTEMUAN 11


---

## Halaman 9

SEGMEN 2 · TELUSURI
Tiga Solution, Enam Cetakan, Lima Triple


  DATA CONTOH (REKAAN, PREFIX DIHILANGKAN)
                        3       6       5
  Following dbo:director    Nolan .                                         solution                     cetakan                           triple di graf
  Following dbo:releaseDate "1998-09-12" .
  Memento   dbo:director    Nolan .
                                                                  #   triple hasil cetakan  Memento   dbo:releaseDate "2000-09-05" .
  Memento   dbo:releaseDate "2001-03-16" .                                                               1   Following a ex:Film
  Insomnia  dbo:director    Nolan .
                                                               1   Following ex:rilis "1998-09-12"

  TEMPLATE                                                               2   Memento a ex:Film

  CONSTRUCT { ?f a ex:Film ; ex:rilis ?r . }                                                               2   Memento ex:rilis "2000-09-05"

                                                               3   Memento a ex:Film                                 sudah ada
  Cetak template per solution
                                                               3   Memento ex:rilis "2001-03-16"


                                                                Graf adalah himpunan. Cetakan yang identik hanya tersimpan sekali.
                                                              Insomnia tidak punya tanggal, jadi tanpa solution dan tanpa triple.




WEB SEMANTIK · TIF2108 · PERTEMUAN 11


---

## Halaman 10

SEGMEN 2 · VARIABEL TAK TERIKAT
Triple Bisa Hilang Tanpa Pesan Error
Pilih versi template. Perhatikan: tidak ada satu pun yang menghasilkan error.


  1 · ?r ditulis benar    2 · salah ketik ?rilis    3 · ?film tidak ada di WHERE      Uji WHERE dulu: SELECT *


  SPARQL · DATA CONTOH FILM
                                                                     6 triple

  CONSTRUCT {
                                                                         dbr:Following ex:judul "Following" @en .
    ?f ex:judul ?j ;
                                                                         dbr:Following ex:rilis 1998-09-12 .
       ex:rilis ?r .                                                                         dbr:Insomnia ex:judul "Insomnia" @en .
  }                                                                         dbr:Memento ex:judul "Memento" @en .
  WHERE {                                                                         dbr:Memento ex:rilis 2000-09-05 .
    ?f dbo:director dbr:Christopher_Nolan ;                                                                         dbr:Memento ex:rilis 2001-03-16 .
       rdfs:label ?j .
    OPTIONAL { ?f dbo:releaseDate ?r }
                                                              OPTIONAL + CONSTRUCT: Insomnia tetap mendapat ex:judul, hanya tanpa  }
                                                                                    tanggal. Triple dengan ?r kosong tidak dicetak.


  Jebakan: mesin tidak memperingatkan variabel template yang tidak ada di WHERE. Tulis WHERE dulu, uji sebagai SELECT *, baru salin
  variabelnya ke template.




WEB SEMANTIK · TIF2108 · PERTEMUAN 11


---

## Halaman 11

SEGMEN 2 · STUDI KASUS DBPEDIA
Mengubah Data Museum Menjadi ex:Tempat


  SPARQL · DBPEDIA.ORG/SPARQL
                                                   Berapa triple paling banyak yang bisa
  PREFIX ex: <http://contoh.id/tempat/>                            dihasilkan?
  CONSTRUCT {
    ?museum a ex:Tempat ;                                                                                                  Periksa
            ex:namaTempat ?nama ;
            ex:kotaTempat ?kota .
  }
  WHERE {                                                                   LIMIT memotong solution, bukan triple. Museum dengan
    ?museum a dbo:Museum ;                                                                   dua dbo:location mengisi dua solution, dan cetakan a
            rdfs:label ?nama ;
                                                                  ex:Tempat-nya kembar.
            dbo:location ?kota .
    FILTER ( LANG(?nama) = "en" )
  }
  LIMIT 20


  Jalankan di DBpedia





WEB SEMANTIK · TIF2108 · PERTEMUAN 11


---

## Halaman 12

02
Menyelaraskan
Kosakata

20 menit · UNION di dalam CONSTRUCT · jalur alternatif | · VALUES ·
pemetaan ke schema.org




                                                                                                                                               Foto: Kelly Sikkema · Unsplash



WEB SEMANTIK · TIF2108 · PERTEMUAN 11


---

## Halaman 13

SEGMEN 3 · TIGA PREDIKAT, SATU ARTI
Empat Triple untuk Tiga Orang?
Tebak dulu berapa triple ex:nama yang lahir, lalu jalankan.


  DATA CONTOH · TIGA SUMBER (REKAAN)                                                                                    Jalankan      Perbaiki: BIND(STR(?n))

  Nolan foaf:name   "Christopher Nolan" .
  Nolan rdfs:label  "Christopher Nolan"@en .                           4 triple
  Joko  rdfs:label  "Joko Anwar"@id .
  Mira  schema:name "Mira Lesmana" .                                           dbr:Christopher_Nolan ex:nama "Christopher Nolan" . # beda literal
                                                                                        dbr:Christopher_Nolan ex:nama "Christopher Nolan" @en . # beda literal
                                                                                        dbr:Joko_Anwar ex:nama "Joko Anwar" @id .
  SPARQL                                                                              dbr:Mira_Lesmana ex:nama "Mira Lesmana" .

  CONSTRUCT { ?o ex:nama ?n . }
  WHERE {                                                                Jebakan: graf hanya menggabungkan triple yang identik.
    VALUES ?o { Nolan Joko Mira }                                                                          "Christopher Nolan" dan "Christopher Nolan"@en adalah dua
    { ?o foaf:name ?n }
                                                                                               literal berbeda. STR() menyatukannya, tetapi tag @id pada nama    UNION { ?o rdfs:label ?n }
                                                                  Joko ikut hilang.    UNION { ?o schema:name ?n }
  }





WEB SEMANTIK · TIF2108 · PERTEMUAN 11


---

## Halaman 14

SEGMEN 3 · TIGA CARA MENULIS
UNION, Jalur Alternatif, atau VALUES
Tiga WHERE berbeda, template sama: ?o ex:nama ?n. Bandingkan hasilnya.


 UNION                              Jalur alternatif |                VALUES ?p

    BAGIAN WHERE YANG BERBEDA                   BAGIAN WHERE YANG BERBEDA                   BAGIAN WHERE YANG BERBEDA

    { ?o foaf:name ?n }                         ?o foaf:name                                VALUES ?p {
    UNION                                         | rdfs:label                                foaf:name
    { ?o rdfs:label ?n }                          | schema:name ?n .                          rdfs:label
    UNION                                                                                     schema:name }
    { ?o schema:name ?n }                           Paling ringkas: satu pola, beberapa predikat.            ?o ?p ?n .

                                                     Jalankan   Bila cabang punya struktur atau FILTER berbeda.                                                                  Daftar predikat menjadi data, mudah ditambah
                                                                                                                            dari tabel pemetaan.
                                               4 triple    Jalankan
                                                                                                       Jalankan
   4 triple                                                Nolan "Christopher Nolan"
                                                           Nolan "Christopher Nolan" @en                                                                                           4 triple
                                                           Joko "Joko Anwar" @id     Nolan "Christopher Nolan"
                                                           Mira "Mira Lesmana"
     Nolan "Christopher Nolan" @en                                                                                                                 Nolan "Christopher Nolan" @en
     Joko "Joko Anwar" @id                                                                                       Nolan "Christopher Nolan"
     Mira "Mira Lesmana"                                                                                                                 Joko "Joko Anwar" @id
                                                                                                                 Mira "Mira Lesmana"


WEB SEMANTIK · TIF2108 · PERTEMUAN 11


---

## Halaman 15

SEGMEN 3 · CONTOH REALISTIS
Memetakan Data Film ke schema.org


  SPARQL · DARI DBO: KE SCHEMA:
                                                                  9 triple  3 film × 3 pola.

  CONSTRUCT {
                                                                     dbr:Following a schema:Movie .
    ?f a schema:Movie ;
                                                                     dbr:Following schema:director dbr:Christopher_Nolan .
       schema:name ?j ;                                                                     dbr:Following schema:name "Following" @en .
       schema:director ?d .                                                                     dbr:Insomnia a schema:Movie .
  }                                                                     dbr:Insomnia schema:director dbr:Christopher_Nolan .
  WHERE {                                                                     dbr:Insomnia schema:name "Insomnia" @en .
    ?f dbo:director ?d ;                                            dbr:Memento a schema:Movie .
       rdfs:label ?j .                                              dbr:Memento schema:director dbr:Christopher_Nolan .
  }                                                                  dbr:Memento schema:name "Memento" @en .


  Jalankan pemetaan                                                                        IRI tetap                Kosakata diganti         Yang tertinggal
                                                                         dbr:Memento tetap            dbo:director menjadi        Man of Steel: tanpa
                                                                             dbr:Memento.                 schema:director.               dbo:director.





WEB SEMANTIK · TIF2108 · PERTEMUAN 11


---

## Halaman 16

03
Hierarki dan Property
Path

35 menit · rdfs:subClassOf · operator + * ? / ^ · Medan tunggal di graf ·
materialisasi · latihan




                                                                                                                                               Foto: Jorge Campos · Unsplash



WEB SEMANTIK · TIF2108 · PERTEMUAN 11


---

## Halaman 17

SEGMEN 4 · DATA CONTOH HIERARKI
Apakah Medan Sebuah Tempat?
Tidak ada triple “Medan a Tempat”. Tanyakan dua kali: tanpa jalur, lalu dengan jalur.


                                                                                   ?x a ex:Tempat
                                        Tempat
                                                                                   ?x a/rdfs:subClassOf* ex:Tempat
                                        subClassOf

                                                                                     4 baris  Medan dua kali: dua jalan.                                      Permukiman

                                                                                     #        ?x
                               subClassOf            subClassOf
                                                                                 1        ex:Medan
                       Kota                                    Desa
                                                                                 2        ex:Medan
                subClassOf   subClassOf                             a
                                                                                 3        ex:Surabaya

      KotaMetropolitan          KotaDiIndonesia                 Tomok                                                                                 4        ex:Tomok

                 a                          a                             a
                                                                                                  Di Wikidata: wdt:P279 berperan seperti
                Medan                   Surabaya                                                 rdfs:subClassOf, wdt:P31 seperti rdf:type (a).





WEB SEMANTIK · TIF2108 · PERTEMUAN 11


---

## Halaman 18

SEGMEN 4 · OPERATOR JALUR
Turun atau Naik, Satu Langkah atau Lebih
Pilih kelas, operator, dan arah. Kelas yang cocok menyala di graf.


                                                                                                   KotaMetropolitan    Kota    Permukiman    Tempat
                                        Tempat
                                                                                   +    *    ?       turun     naik
                                        subClassOf
                                                                                     SPARQL · KOTA.TTL
                                      Permukiman
                                                                                    SELECT ?c WHERE {
                               subClassOf            subClassOf                               ?c rdfs:subClassOf+ ex:Kota .
                                                                                    }
                       Kota                                    Desa

                                                                                     2 baris  KotaDiIndonesia · KotaMetropolitan                subClassOf   subClassOf                             a

                                                                                  + : satu langkah atau lebih. Kelas awal tidak ikut. Variabel di      KotaMetropolitan          KotaDiIndonesia                 Tomok
                                                                                                          subjek: mencari subkelas.

                 a                          a                             a

                Medan                   Surabaya





WEB SEMANTIK · TIF2108 · PERTEMUAN 11


---

## Halaman 19

SEGMEN 4 · KEJANGGALAN PERTEMUAN 10
Medan Ganda di Tabel, Tunggal di Graf


                                                                            SELECT ?X                         CONSTRUCT { ?X A EX:KOTA }
                                                                      3 baris                          2 triple                            KotaMetropolitan
                     a                                                                      #     ?x                                ex:Medan a ex:Kota .        Medan                                              subClassOf                                                                                                                                      ex:Medan a ex:Kota . # kembar
                                                         Kota           1    ex:Medan                       ex:Surabaya a ex:Kota .
                       a
                                              subClassOf                   2    ex:Medan

                             KotaDiIndonesia                            3    ex:Surabaya

                        a

       Surabaya                                                   Jebakan: graf menggabungkan cetakan kembar, bukan nilai yang
                                                                      berbeda. Bila template memuat ex:penduduk ?p, Medan tetap
                                                                punya dua angka populasi.

   Telusuri jalur a/rdfs:subClassOf* ex:Kota





WEB SEMANTIK · TIF2108 · PERTEMUAN 11


---

## Halaman 20

SEGMEN 4 · JALUR / DAN ^
Kota Kelahiran Sutradara dalam Satu Pola


                                                                             SPARQL · FILM.TTL

       Following
                                                                            SELECT ?f ?kota WHERE {
                                                                              ?f dbo:director/dbo:birthPlace ?kota .
                                                                            }                        director
        Memento                                                              ORDER BY ?f
                    director
                                Christopher_Nolan   birthPlace   London
                    director                                                   3 baris
       Insomnia
                         producer                                                                            #     ?f                        ?kota

                                                                         1     dbr:Following            dbr:London
       Man of Steel
                                                                         2     dbr:Insomnia             dbr:London

                                                                         3     dbr:Memento              dbr:London
  / : dari film    ^ : dari London    dua pola eksplisit

                                                                                                  Jalur / tidak memberi nama node perantara. Butuh nama sutradara? Tulis
                                                                               dua pola eksplisit.





WEB SEMANTIK · TIF2108 · PERTEMUAN 11


---

## Halaman 21

SEGMEN 4 · CONTOH REALISTIS
Hierarki Nyata: Kelas Kota di Wikidata
Ubah arah dan operator, lalu jalankan di Wikidata Query Service.

  turun: subkelas kota     naik: kota termasuk apa      +    *                          Arah
                                                                                                   Variabel di subjek mencari ke bawah; di objek mencari ke atas.
  SPARQL · QUERY.WIKIDATA.ORG
                                                                     + atau *
  SELECT ?kelas ?kelasLabel WHERE {
                                                                               Dengan *, wd:Q515 (kota) sendiri ikut.
    ?kelas wdt:P279+ wd:Q515 .
    SERVICE wikibase:label {
                                                                          LIMIT
      bd:serviceParam wikibase:language "id,en" .
                                                                                                      Hierarki Wikidata besar. Batasi saat menjelajah.
    }
  }
                                                                                         Hati-hati
  LIMIT 30
                                                                                                      Hierarki disunting komunitas. Periksa kelas yang mengejutkan
                                                                                  sebelum memakai P279*.
  Jalankan di Wikidata     Salin query





WEB SEMANTIK · TIF2108 · PERTEMUAN 11


---

## Halaman 22

SEGMEN 4 · BATAS PROPERTY PATH
Yang Tidak Bisa Dilakukan Satu Jalur
Klik setiap kartu untuk melihat jalan keluarnya.

  BATAS Menyebut            Jalur tidak memberi nama node di tengah       BATAS Menghitung       Kedalaman kelas tidak tersedia di SPARQL
   1                                                                                     2
       perantara              rantai.                                langkah            1.1 standar.

  Jalur tidak memberi nama node di tengah rantai.                    Kedalaman kelas tidak tersedia di SPARQL 1.1 standar.
  Jalan keluar: Tulis pola eksplisit, seperti dua pola sutradara.                   Jalan keluar: Pola per tingkat, atau hitung di Python.

  BATAS Murah di           Jalur * tanpa jangkar di endpoint besar bisa        BATAS 4 Mengingat hasil  Setiap query harus menulis ulang jalurnya.
   3
       endpoint           timeout.
                                                                        Setiap query harus menulis ulang jalurnya.
  Jalur * tanpa jangkar di endpoint besar bisa timeout.                      Jalan keluar: Simpan kesimpulan sebagai triple: materialisasi.
  Jalan keluar: Jangkar satu ujung dengan IRI, pakai LIMIT.


  Batas nomor 4 yang akan kita atasi sekarang: simpan hasil penelusuran sebagai triple baru.





WEB SEMANTIK · TIF2108 · PERTEMUAN 11


---

## Halaman 23

SEGMEN 4 · MATERIALISASI
Menyimpan Kesimpulan sebagai Triple Baru


  SPARQL · ATURAN BUATAN SENDIRI                                                                   12 triple

  CONSTRUCT { ?x a ?super . }
                                                                       ex:Medan a ex:Kota . # baru
  WHERE {                                                                       ex:Medan a ex:KotaDiIndonesia .
    ?x a/rdfs:subClassOf* ?super .                                                                       ex:Medan a ex:KotaMetropolitan .
  }                                                                       ex:Medan a ex:Permukiman . # baru
                                                                       ex:Medan a ex:Tempat . # baru
Bila ?x bertipe kelas K, dan K subkelas dari ?super sedalam apa pun, maka ?x        ex:Surabaya a ex:Kota . # baru
juga bertipe ?super.                                                       ex:Surabaya a ex:KotaDiIndonesia .
                                                                       ex:Surabaya a ex:Permukiman . # baru
  1 · Tanya ?x a ex:Tempat    2 · Jalankan aturan dan gabungkan                 ex:Surabaya a ex:Tempat . # baru
                                                                       ex:Tomok a ex:Desa .
  3 · Tanya lagi     Reset                                                  ex:Tomok a ex:Permukiman . # baru
                                                                       ex:Tomok a ex:Tempat . # baru
 12       4        8
  triple hasil CONSTRUCT      sudah ada di data               triple baru
                                                      Anda baru saja menulis satu aturan inferensi dengan tangan
                                                                          (setara rdfs9 dan rdfs11). Pertemuan 12: mesin yang
                                                                menjalankannya sendiri.





WEB SEMANTIK · TIF2108 · PERTEMUAN 11


---

## Halaman 24

LATIHAN BERPASANGAN · 7 MENIT
Tebak Hasilnya Sebelum Mesin Menjawab


  KOTA.TTL (PREFIX DIHILANGKAN)
                                                                         SOAL A
  Permukiman       rdfs:subClassOf Tempat .                                       SELECT ?c WHERE {
  Kota             rdfs:subClassOf Permukiman .                                   ?c rdfs:subClassOf+ Tempat                                                                                                   }
  Desa             rdfs:subClassOf Permukiman .
                                                                          Berapa baris hasilnya?  KotaMetropolitan rdfs:subClassOf Kota .
  KotaDiIndonesia  rdfs:subClassOf Kota .                               SOAL B
  Medan    a KotaMetropolitan , KotaDiIndonesia ;                               CONSTRUCT {
           populasi 2435252 , 2097610 ; label "Medan"@id .                    ?x nama ?l ;
                                                                                                        penduduk ?p }
  Surabaya a KotaDiIndonesia ;                                                         WHERE {
                                                                                                     ?x a Desa ;           populasi 2874314 ; label "Surabaya"@id .                                                                                                        label ?l .
  Tomok    a Desa ; label "Tomok"@id .                                                OPTIONAL { ?x populasi ?p }
                                                                                                   }

                                                                          Berapa triple yang dihasilkan?

                                                                         SOAL C

                                                                                                   CONSTRUCT {
                                                                                                     ?k a Kota ;
                                                                                                        penduduk ?p }
                                                                                                   WHERE {
                                                                                                     ?k a/rdfs:subClassOf* Kota ;
                                                                                                        populasi ?p .
                                                                                                   }

                                                                          Berapa triple yang dihasilkan?


WEB SEMANTIK · TIF2108 · PERTEMUAN 11


---

## Halaman 25

04
Live-Coding: Dari
Endpoint ke Graf Lokal

40 menit · A kota di WDQS · B Nolan ke schema.org · C simpan Turtle ·
D materialisasi lokal




                                                                                                                                               Foto: Safar Safarov · Unsplash



WEB SEMANTIK · TIF2108 · PERTEMUAN 11


---

## Halaman 26

SEGMEN 5 · PETA DEMO
Empat Langkah, dari Browser ke Berkas


  DEMO A                       DEMO B                       DEMO C                       DEMO D
   query.wikidata.org                  dbpedia.org/sparql                  Python · SPARQLWrapper              Python · rdflib lokal
  Satu Medan, satu          Nolan ke schema.org       Graf menjadi .ttl            Materialisasi kelas
  triple                                    Pemetaan kosakata pada data            Hasil Demo B disimpan, lalu di-          Aturan materialisasi pada data
                                        DBpedia.                             query tanpa internet.                 kampus.   Query A Pertemuan 9 diubah
   menjadi CONSTRUCT.



  Siapkan: pip install rdflib sparqlwrapper · berkas kampus.ttl dari LMS · User-Agent berisi nama aplikasi dan email Anda.





WEB SEMANTIK · TIF2108 · PERTEMUAN 11


---

## Halaman 27

SEGMEN 5 · DEMO A · WDQS
Query A Pertemuan 9 sebagai CONSTRUCT

  1 · Query A (SELECT)    2 · Versi CONSTRUCT


                                                                                 SIMULASI PADA KOTA.TTL (REKAAN; WDT:P31/WDT:P279* DITULIS
  SPARQL · QUERY.WIKIDATA.ORG                                                                                 A/RDFS:SUBCLASSOF*)

  SELECT ?kota ?namaKota ?populasi WHERE {                                                                             5 baris
    ?kota wdt:P31/wdt:P279* wd:Q515 ;
          wdt:P17 wd:Q252 ;                                                  #   ?kota           ?namaKota          ?populasi
          wdt:P1082 ?populasi ;
                                                                         1   ex:Surabaya     "Surabaya" @id     2874314          rdfs:label ?namaKota .
    FILTER ( LANG(?namaKota) = "id" )                                                                         2   ex:Medan        "Medan" @id        2435252
  }
  ORDER BY DESC(?populasi)                                                 3   ex:Medan        "Medan" @id        2435252
  LIMIT 10
                                                                         4   ex:Medan        "Medan" @id        2097610

  Jalankan di Wikidata                                                        5   ex:Medan        "Medan" @id        2097610


                                                                         Medan muncul empat kali: 2 jalur kelas × 2 angka populasi.





WEB SEMANTIK · TIF2108 · PERTEMUAN 11


---

## Halaman 28

SEGMEN 5 · DEMO B · DBPEDIA
Film Nolan ke Kosakata schema.org

                                                                                        SIMULASI PADA DATA CONTOH FILM (REKAAN)
  SPARQL · DBPEDIA.ORG/SPARQL

                                                                                   12 triple
  PREFIX schema: <https://schema.org/>
  CONSTRUCT {
                                                                                                       dbr:Following a schema:Movie .
    ?film a schema:Movie ;                                                                       dbr:Following schema:datePublished 1998-09-12 .
          schema:name ?judul ;                                                                  dbr:Following schema:director dbr:Christopher_Nolan .
          schema:director dbr:Christopher_Nolan ;                                           dbr:Following schema:name "Following" @en .
                                                                                                       dbr:Insomnia a schema:Movie .
          schema:datePublished ?rilis .                                                                                                       dbr:Insomnia schema:director dbr:Christopher_Nolan .
  }                                                                                                       dbr:Insomnia schema:name "Insomnia" @en .
  WHERE {                                                                                            dbr:Memento a schema:Movie .
    ?film a dbo:Film ;                                                                            dbr:Memento schema:datePublished 2000-09-05 .
                                                                                                       dbr:Memento schema:datePublished 2001-03-16 .
          dbo:director dbr:Christopher_Nolan ;                                                                                                       dbr:Memento schema:director dbr:Christopher_Nolan .
          rdfs:label ?judul .                                                                                                       dbr:Memento schema:name "Memento" @en .
    FILTER ( LANG(?judul) = "en" )
    OPTIONAL { ?film dbo:releaseDate ?rilis }
                                                                                    OPTIONAL: Insomnia tetap menjadi schema:Movie tanpa tanggal.
  }
                                                                               Memento membawa dua tanggal.

  Jalankan di DBpedia     Simulasikan pada film.ttl





WEB SEMANTIK · TIF2108 · PERTEMUAN 11


---

## Halaman 29

SEGMEN 5 · DEMO C · PYTHON
Graf dari Endpoint, Disimpan sebagai Turtle

                                                                                    KELUARAN · ENDPOINT DIGANTI HASIL DEMO B PADA FILM.TTL
  PYTHON · PIP INSTALL RDFLIB SPARQLWRAPPER

                                                                                                 12 triple
  from SPARQLWrapper import SPARQLWrapper, TURTLE                                                                                                 Film tanpa tanggal: 1
  from rdflib import Graph

  Q_NOLAN_GRAF = open("q_demo_b.rq", encoding="utf-8").read()   # query Demo B
                                                                                           FILM_NOLAN.TTL
  Q_TANPA_TANGGAL = """PREFIX schema: <https://schema.org/>
  SELECT (COUNT(?f) AS ?n) WHERE { ?f a schema:Movie .                                                                                                                     dbr:Following a schema:Movie .
    FILTER NOT EXISTS { ?f schema:datePublished ?d } }"""                                                dbr:Following schema:datePublished 1998-09-12 .
                                                                                                                     dbr:Following schema:director dbr:Christopher_Nolan .
                                                                                                                     dbr:Following schema:name "Following" @en .  UA = "KelasWebSemantik/1.0 (email@kampus.ac.id)"   # ganti dengan email Anda
                                                                                                                     dbr:Insomnia a schema:Movie .
  sp = SPARQLWrapper("https://dbpedia.org/sparql", agent=UA)
                                                                                                                     dbr:Insomnia schema:director dbr:Christopher_Nolan .
  sp.setQuery(Q_NOLAN_GRAF)                                                                                                                     dbr:Insomnia schema:name "Insomnia" @en .
  sp.setReturnFormat(TURTLE)                                                                                                                     dbr:Memento a schema:Movie .
  g = Graph().parse(data=sp.queryAndConvert(), format="turtle")                                         dbr:Memento schema:datePublished 2000-09-05 .
  print(len(g), "triple")                                                                                       dbr:Memento schema:datePublished 2001-03-16 .
                                                                                                                     dbr:Memento schema:director dbr:Christopher_Nolan .  g.serialize("film_nolan.ttl", format="turtle")
                                                                                                                     dbr:Memento schema:name "Memento" @en .

  lokal = Graph().parse("film_nolan.ttl")   # tanpa internet
  for b in lokal.query(Q_TANPA_TANGGAL):
      print("Film tanpa tanggal:", b.n)

  Jalankan pada data contoh     Salin kode    Unduh demo_c.py




WEB SEMANTIK · TIF2108 · PERTEMUAN 11


---

## Halaman 30

SEGMEN 5 · DEMO D · RDFLIB LOKAL
Materialisasi Kelas, dan Satu Kejanggalan Baru

                                                                                  KELUARAN · KAMPUS.TTL DIJALANKAN DI HALAMAN INI
  PYTHON · KAMPUS.TTL

                                                                                           Sebelum: 0 # tidak ada triple a foaf:Person
  from rdflib import Graph
                                                                                           Sesudah: 3 # 7 triple turunan, 4 baru
                                                                                           Ada Rina: 3 # Rina tertinggal
  g = Graph().parse("kampus.ttl")
  Q_ORANG = "SELECT ?x WHERE { ?x a foaf:Person }"
  print("Sebelum:", len(g.query(Q_ORANG)))

  turunan = g.query("""CONSTRUCT { ?x a ?super }
      WHERE { ?x a/rdfs:subClassOf* ?super }""")                                       Rina bertipe ex:DosenTetap, tetapi tidak
  for t in turunan:
                                                                                           terhitung sebagai foaf:Person. Dan di      g.add(t)
  print("Sesudah:", len(g.query(Q_ORANG)))                                                 kampus_v4.ttl, triple turunan tidak bisa dibedakan
  g.serialize("kampus_v4.ttl", format="turtle")                                                 dari triple asli. Dijawab di Pertemuan 12.

  RINA = "@prefix ex: <http://contoh.id/kampus/> . ex:rina a ex:DosenTetap ."
  g.parse(data=RINA, format="turtle")   # dosen baru
  print("Ada Rina:", len(g.query(Q_ORANG)))


  Jalankan langkah demi langkah     Salin kode     Reset





WEB SEMANTIK · TIF2108 · PERTEMUAN 11


---

## Halaman 31

SEGMEN 5 · DIAGNOSIS
CONSTRUCT Tidak Sesuai Harapan? Cek Ini
Klik setiap gejala untuk melihat penyebab dan langkahnya.


  GEJALA Graf kosong, tanpa error               GEJALA Satu properti hilang                    GEJALA Triple lebih sedikit dari baris

  WHERE tidak cocok, atau semua pola             Salah ketik variabel di template, atau            Cetakan kembar digabung. Ini wajar.
  template memakai variabel tak terikat.         OPTIONAL kosong.                                                                                                     Langkah: Hitung per pola template.
  Langkah: Jalankan WHERE sebagai SELECT *          Langkah: Samakan nama variabel template dan
   dulu.                                     WHERE.

  GEJALA Dua nilai yang tampak sama          GEJALA Superkelas tidak ditemukan          GEJALA Timeout di endpoint

  Beda tag bahasa atau tipe data.                  Pola tanpa jalur subClassOf*.                      Jalur * tanpa jangkar IRI.
  Langkah: STR(), atau pilih satu bahasa.               Langkah: Tambah jalur, atau materialisasi.            Langkah: Jangkar satu ujung, persempit, LIMIT.





WEB SEMANTIK · TIF2108 · PERTEMUAN 11


---

## Halaman 32

SEGMEN 5 · TANTANGAN
Tantangan: Kembalikan Triple ex:rilis
CONSTRUCT ini seharusnya memberi judul dan tanggal rilis film Nolan, tetapi semua triple ex:rilis hilang
tanpa error. Perbaiki sampai graf berisi 6 triple.


  CONSTRUCT {                                                     3 triple, 0 di antaranya ex:rilis. Tidak ada error, jadi
    ?f ex:judul ?j ;                                                    masalahnya di nama variabel, bukan sintaks.
       ex:rilis ?rilis .
  }
                                                                             3 triple  WHERE {
    ?f dbo:director dbr:Christopher_Nolan ;
                                                                                          dbr:Following ex:judul "Following" @en .
       rdfs:label ?j .                                                                                          dbr:Insomnia ex:judul "Insomnia" @en .
    OPTIONAL { ?f dbo:releaseDate ?r }                                            dbr:Memento ex:judul "Memento" @en .
  }





  Jalankan      Petunjuk     Ulang    PREFIX dbo: dbr: rdfs: ex: sudah tersedia



WEB SEMANTIK · TIF2108 · PERTEMUAN 11


---

## Halaman 33

SEGMEN 5 · LAB
Lab Bebas: Film, Kota, dan Kampus di Browser
Ketiga data contoh dimuat ke satu graf. Pilih contoh, jalankan, lalu ubah query sesuka Anda.


 CONSTRUCT    UNION     Jalur |     Jalur +     Materialisasi    Kampus                 PREFIX dbo: dbr: rdfs: foaf: schema: xsd: ex: kampus: tersedia


  CONSTRUCT {                                                            5 triple
    ?f a ex:Film ;
       ex:rilis ?r .                                                        dbr:Following a ex:Film .
  }                                                                           dbr:Following ex:rilis 1998-09-12 .
                                                                              dbr:Memento a ex:Film .  WHERE {
                                                                              dbr:Memento ex:rilis 2000-09-05 .    ?f dbo:director dbr:Christopher_Nolan ;
                                                                              dbr:Memento ex:rilis 2001-03-16 .
       dbo:releaseDate ?r .
  }





  Jalankan    Ctrl/⌘ + Enter



WEB SEMANTIK · TIF2108 · PERTEMUAN 11


---

## Halaman 34

SEGMEN 6 · ETIKA ENDPOINT
Empat Aturan Main di Endpoint Publik
CONSTRUCT dengan jalur * adalah query termahal yang Anda tulis hari ini. Endpoint publik menanggung
biayanya.

 1          2          3          4
  User-Agent bermakna     LIMIT saat eksplorasi      Simpan, jangan           Jangkar jalur
                                                        ulangi  Nama aplikasi dan kontak.            LIMIT membatasi solution.                                                     Jalur * dan + selalu berangkat
   Klien anonim bisa diblokir.            Satu solution bisa mencetak         Simpan graf ke .ttl sekali, lalu           dari IRI tertentu, bukan dari
                                    beberapa triple.                      olah di laptop seperti Demo C.        dua variabel.



  Untuk skrip yang memanggil endpoint berulang kali: beri jeda antar-permintaan, dan catat tanggal pengambilan serta teks query di
  samping berkas .ttl.





WEB SEMANTIK · TIF2108 · PERTEMUAN 11


---

## Halaman 35

SEGMEN 6 · DISKUSI · 7 MENIT
Dua Pertanyaan untuk Dibawa Pulang
Diskusi kelompok kecil, lalu berbagi. Klik “Lihat arah” setelah berdiskusi.

 01                    02
  Tim Anda menyimpan hasil materialisasi Demo D ke       Untuk dashboard populasi kota, Anda memakai
  graf produksi. Setahun kemudian taksonominya         SELECT atau CONSTRUCT? Untuk menggabungkan
  berubah. Triple mana yang kini salah, dan                data kota dari tiga sumber?
  bagaimana Anda menemukannya?


     Arah: triple turunan tidak bisa dibedakan dari triple asli;
    simpan terpisah, catat asal, atau hitung ulang. Pertemuan              Arah: tabel untuk analisis dan agregasi, graf untuk integrasi
     12: reasoner.                                                 dan identitas. CONSTRUCT tidak memilih nilai.





WEB SEMANTIK · TIF2108 · PERTEMUAN 11


---

## Halaman 36

RINGKASAN
Lima Hal yang Anda Bawa dari Hari Ini


      CONSTRUCT mencetak template sekali per solution; graf hasilnya himpunan, jadi cetakan kembar01
        tersimpan sekali.


         Triple dengan variabel tak terikat tidak dicetak, tanpa error. OPTIONAL memakai sifat ini dengan sengaja.02

       UNION, jalur |, dan VALUES menyatukan predikat berbeda menjadi satu properti milik kita.03

       + satu langkah atau lebih, * nol atau lebih, / berurutan, ^ terbalik. Jalur tidak menyebut perantara.04

         Materialisasi menyimpan kesimpulan sebagai triple, tetapi harus dihitung ulang dan asalnya hilang.05





WEB SEMANTIK · TIF2108 · PERTEMUAN 11


---

## Halaman 37

TINDAK LANJUT
Sebelum Pertemuan 12

  PERTEMUAN 12                                       Pekerjaan rumah
  Inferensi dan Reasoning                                Ulangi Demo C dan D di laptop Anda; kode dan data contoh ada di
                                                                         LMS.   Rina yang tertinggal dan triple turunan tanpa asal-usul dari Demo D.
   Reasoner menurunkan triple dari aturan RDFS dan OWL, dan                                                                   Ubah pertanyaan Wikidata Anda menjadi CONSTRUCT ke kosakata
  membedakan yang di-asert dari yang disimpulkan.                                                                                        ex: Anda. Simpan sebagai .ttl, catat jumlah baris SELECT dan
                                                                             jumlah triple-nya.

                                                                                Kerjakan Latihan Pertemuan 11 di repo pertemuan-11.

                                                                       Baca SPARQL 1.1 Query Language, bagian 9 (Property Paths) dan
                                                                            16.2 (CONSTRUCT).




  REFERENSI
   Antoniou, Groth, van Harmelen & Hoekstra (2012), A Semantic Web Primer, 3rd ed., MIT Press · DuCharme (2013), Learning SPARQL, 2nd ed., O’Reilly · Allemang, Hendler &
  Gandon (2020), Semantic Web for the Working Ontologist, 3rd ed., ACM Books · Hitzler, Krötzsch & Rudolph, Foundations of Semantic Web Technologies, Chapman & Hall/CRC ·
  W3C (2013), SPARQL 1.1 Query Language · W3C (2014), RDF Schema 1.1 · W3C (2009), SKOS Reference · Wikidata SPARQL query service · rdflib documentation.





WEB SEMANTIK · TIF2108 · PERTEMUAN 11


---

## Halaman 38

PENUTUP · TANYA-JAWAB
Triple yang Anda bangun hari ini
benar menurut aturan Anda. Siapa
yang menjaga aturan itu tetap benar
besok?

Pertanyaan ini menjadi pembuka Pertemuan 12: inferensi dan reasoning.


  Graf adalah himpunan     Jalur menelusuri hierarki    Sampai jumpa di Pertemuan 12





WEB SEMANTIK · TIF2108 · PERTEMUAN 11
