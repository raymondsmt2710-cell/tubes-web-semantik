# Web_Semantik_P10_SPARQL_SELECT


---

## Halaman 1

PERTEMUAN 10 · TIF2108 · SUB-CPMK 5 (BAGIAN 2)
SPARQL SELECT Query:
Membentuk Jawaban
Pekan lalu ada film Nolan yang hilang dan kota yang muncul dua kali. Hari ini kita membedah
penyebabnya, lalu menulis SELECT yang mengendalikan baris hasilnya, dari editor sampai DataFrame.

 Mata Kuliah Web Semantik    Program Studi Teknologi Informasi    3 SKS · 150 menit





WEB SEMANTIK · TIF2108 · PERTEMUAN 10


---

## Halaman 2

RENCANA SESI · 150 MENIT
Alur Pertemuan Hari Ini


  10′          20′ · Anatomi         30′ · OPTIONAL                30′ · Membentuk hasil          40′ · Live-coding                         20′ · Penutup


  01              10 menit      02              20 menit      03              30 menit      Siapkan sekarang
 Pembuka              Anatomi SELECT        Data tidak lengkap           Laptop dengan browser modern.
  Dua kejanggalan dari              Empat blok dan urutan kerja        OPTIONAL, letak FILTER, NOT
  Pertemuan 9                     mesin query                       EXISTS, UNION                     Python 3.10+ lalu jalankan
                                                                                                    pip install sparqlwrapper pandas

                                                                                                Query Wikidata Anda dari tugas  04              30 menit      05              40 menit      06              20 menit
                                                                                               Pertemuan 9.
 Membentuk hasil        Live-coding            Penutup
  DISTINCT, urutan, paginasi,        WDQS, DBpedia, Python ke           Etika endpoint, diskusi,             Belum bawa laptop? Duduk
   agregasi                         pandas                             ringkasan                           berpasangan.





WEB SEMANTIK · TIF2108 · PERTEMUAN 10


---

## Halaman 3

SUB-CPMK 5 · BAGIAN 2
Setelah Sesi Ini, Anda Mampu…

 01          02          03          04
  Menjelaskan           Menyusun            Membentuk             Mengintegrasikan

  Mengapa sebuah baris hilang       SELECT dengan pola wajib            Hasil dengan DISTINCT,              Hasil query ke pandas: sel
   atau muncul ganda, dengan         dan pola boleh kosong:           ORDER BY, LIMIT/OFFSET,          kosong tertangani, duplikat
   menelusuri solution mapping.       OPTIONAL, FILTER, UNION,          serta GROUP BY dan agregat.         diperiksa, data disimpan ke
                            NOT EXISTS.                                                         CSV.


     Dicek: latihan                           Dicek: tanya-jawab                      Dicek: latihan                           Dicek: live-coding



  Kontrak sesi: hari ini semua jawaban berupa tabel. Membangun graf baru dengan CONSTRUCT adalah porsi Pertemuan 11; qualifier
  Wikidata (p:, ps:, pq:) hanya disinggung.





WEB SEMANTIK · TIF2108 · PERTEMUAN 10


---

## Halaman 4

RECAP · PERTEMUAN 9
Dua Kejanggalan yang Belum Terjawab



    QUERY B · DBPEDIA                                                  QUERY A · WIKIDATA

     ?film a dbo:Film ;                                                ?kota wdt:P31/wdt:P279* wd:Q515 ;
           dbo:director dbr:Christopher_Nolan ;                              wdt:P17 wd:Q252 ;
           rdfs:label ?judul ;                                               wdt:P1082 ?populasi ;
           dbo:releaseDate ?rilis .                                          rdfs:label ?namaKota .

  Film Nolan yang hilang                           Kota yang muncul dua kali

   Dibanding filmografi di Wikipedia, ada film yang tidak muncul di            Satu kota mengisi lebih dari satu baris di tabel sepuluh besar.
   hasil.
                                                                              Dijawab di Segmen 04: DISTINCT dan agregasi
    Dijawab di Segmen 03: OPTIONAL



  Petunjuk dari Pertemuan 9: satu solution adalah satu baris. Hilang dan ganda adalah dua sisi aturan yang sama.





WEB SEMANTIK · TIF2108 · PERTEMUAN 10


---

## Halaman 5

PERTANYAAN PEMANTIK
Siapa yang Menentukan Jumlah Baris?

Hasil SELECT selalu berupa tabel, tetapi Anda tidak pernah menuliskan berapa barisnya. Lalu
dari mana angka itu datang?


  Data tidak lengkap               Data berlapis                  Query Anda

   Satu pola wajib tidak menemukan triple.          Satu entitas cocok dengan pola lewat           OPTIONAL, DISTINCT, dan GROUP BY
 3    2                     beberapa jalan.                           mengubah aturan main.
    film disutradarai Nolan   baris hasil query              2 3          3   2
                                                            kota    baris hasil query                                       film (OPTIONAL)   kota (DISTINCT)   Akibat: seluruh baris entitas itu hilang.
                                                      Akibat: satu entitas mengisi beberapa baris.         Akibat: Anda yang memutuskan bentuk
                                                                                                         tabelnya.





WEB SEMANTIK · TIF2108 · PERTEMUAN 10


---

## Halaman 6

01
Anatomi SELECT dan
Urutan Kerjanya

20 menit · empat blok · proyeksi dan ekspresi · urutan evaluasi





                                                                                                                                               Foto: Amsterdam City Archives · Unsplash



WEB SEMANTIK · TIF2108 · PERTEMUAN 10


---

## Halaman 7

SEGMEN 2 · ANATOMI SELECT
Empat Blok, Satu Query Induk
Query A Pertemuan 9 dipakai sepanjang sesi. Klik setiap blok untuk menyorotnya.

  SPARQL · QUERY A PERTEMUAN 9                                           1 · PREFIX
                                                                                                          Alias namespace. Disuntikkan otomatis di WDQS, wajib
  PREFIX wd:   <http://www.wikidata.org/entity/>                                                                                                                      ditulis di endpoint lain.
  PREFIX wdt:  <http://www.wikidata.org/prop/direct/>
  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>                                                                    2 · SELECT
                                                                                                      Proyeksi: kolom yang ditampilkan.
  SELECT ?kota ?namaKota ?populasi
  WHERE {                                                                    3 · WHERE
    ?kota wdt:P31/wdt:P279* wd:Q515 ;                                                Pola yang dicocokkan ke graf. Bagian ini yang
          wdt:P17 wd:Q252 ;                                                  menentukan baris.
          wdt:P1082 ?populasi ;
          rdfs:label ?namaKota .                                       4 · Modifier
                                                                      GROUP BY, ORDER BY, LIMIT, OFFSET: membentuk tabel    FILTER ( LANG(?namaKota) = "id" )
                                                                                                                  akhir.  }
  ORDER BY DESC(?populasi)
                                                                                  Buka di Wikidata Query Service
  LIMIT 10





WEB SEMANTIK · TIF2108 · PERTEMUAN 10


---

## Halaman 8

SEGMEN 2 · PROYEKSI
SELECT Memilih Kolom, Bukan Baris
Pilih kolom yang ditampilkan. Perhatikan jumlah barisnya.


  *    ?kota    ?nama    ?populasi
                                                                       5 baris   Kolom berubah, baris tetap.

  (?populasi / 1000000 AS ?juta)                                                                       #      ?nama                         ?populasi

  SPARQL · DATA CONTOH KOTA                                          1     "Medan" @id                  2097610

                                                                    2     "Medan" @id                  2097610  SELECT ?nama ?populasi WHERE {
    ?kota ex:instanceOf/ex:subclassOf* ex:Kota ;
                                                                    3     "Medan" @id                  2435252
          ex:populasi ?populasi ;
          rdfs:label ?nama .                                                                    4     "Medan" @id                  2435252
  }
                                                                    5     "Surabaya" @id               2874314  ORDER BY ?nama ?populasi


                                                                    SELECT * cocok untuk debug di graf lokal, bukan untuk endpoint publik. Alias
  Jebakan: membuang ?populasi dari SELECT tidak membuang baris                                                                                                hasil AS tidak boleh sudah dipakai di WHERE.
  ganda yang ia sebabkan. Proyeksi memotong kolom; jumlah baris
  tetap sama.





WEB SEMANTIK · TIF2108 · PERTEMUAN 10


---

## Halaman 9

SEGMEN 2 · URUTAN EVALUASI
Urutan Tulis Berbeda dengan Urutan Kerja

 1                                             5            2          3          4                      6 WHERE                                                                          Proyeksi                     GROUP BY            Ekspresi            ORDER BY                                Potong  pola, OPTIONAL, UNION,                                                                                    kolom SELECT, lalu                                  agregat, lalu HAVING         kolom SELECT … AS          mengurutkan solution                                   OFFSET, lalu LIMIT
  FILTER, BIND                                                                                            DISTINCT


  SPARQL · DATA CONTOH KOTA                               LIMIT 1 bekerja paling akhir: satu baris unik, bukan satu baris lalu disaring.

  SELECT DISTINCT ?nama WHERE {                              1 baris
    ?k ex:instanceOf ?kelas ;
                                                             #           ?nama       rdfs:label ?nama .
  }                                                          1           "Surabaya" @id
  ORDER BY DESC(?nama)
  LIMIT 1


  Tahap sebelumnya    Tahap berikutnya





WEB SEMANTIK · TIF2108 · PERTEMUAN 10


---

## Halaman 10

02
Data Tidak Lengkap:
OPTIONAL

30 menit · film Nolan yang hilang · OPTIONAL · blok dan letak FILTER ·
mencari yang tidak tercatat · UNION




                                                                                                                                               Foto: Jason Leung · Unsplash



WEB SEMANTIK · TIF2108 · PERTEMUAN 10


---

## Halaman 11

SEGMEN 3 · MENELUSURI KEJANGGALAN 1
Mengapa Film Nolan Bisa Hilang


  DATA CONTOH (REKAAN, PREFIX DIHILANGKAN)                       QUERY

  Following dbo:director    Nolan .                              SELECT ?film ?rilis WHERE {
  Following dbo:releaseDate "1998-09-12" .                         ?film dbo:director Nolan .        # pola 1
  Memento   dbo:director    Nolan .                                ?film dbo:releaseDate ?rilis .   # pola 2
  Memento   dbo:releaseDate "2000-09-05" .                       }
  Insomnia  dbo:director    Nolan .


  Pola 1 · 3 cocok                           Pola 2 · 2 cocok                            Hasil · digabung lewat ?film

                                                                                           2 baris   ?film                                       ?film               ?rilis

                                                                                           #   ?film              ?rilis    Following                                 Following         1998-09-12

                                                                                       1   dbr:Memento       2000-09-05    Memento                                   Memento           2000-09-05

                                                                                       2   dbr:Following     1998-09-12   Insomnia



  Insomnia tidak punya pasangan di pola 2, jadi seluruh solution-nya terbuang. Di SQL kolom kosong tetap memberi baris dengan NULL. Di
  RDF, triple yang tidak tercatat memang tidak ada.


WEB SEMANTIK · TIF2108 · PERTEMUAN 10


---

## Halaman 12

SEGMEN 3 · OPTIONAL
Pertahankan Baris, Biarkan Selnya Kosong

Pola tanggal rilis:   wajib    OPTIONAL                                                                     3 baris   Insomnia kembali.

  SPARQL · DATA CONTOH FILM                                                                     #      ?film                        ?rilis

  SELECT ?film ?rilis WHERE {                                       1     dbr:Insomnia                    –
    ?film dbo:director dbr:Christopher_Nolan .
                                                                  2     dbr:Following               1998-09-12    OPTIONAL { ?film dbo:releaseDate ?rilis }
  }                                                                  3     dbr:Memento                 2000-09-05
  ORDER BY ?rilis

                                                                     JSON W3C · BARIS INSOMNIA, DIHASILKAN MESIN DI HALAMAN INI
 Padanan SQL           Kosong bukan NULL     Urutan naik
                                                                               {  LEFT JOIN                   Di JSON hasil, kuncinya      Sel kosong ditaruh
                                                                                 "film": {
                                tidak ada.                    paling atas.
                                                                                   "type": "uri",
                                                                                   "value": "dbr:Insomnia"
                                                                                 }
                                                                               }
                                                                               # tidak ada kunci "rilis"





WEB SEMANTIK · TIF2108 · PERTEMUAN 10


---

## Halaman 13

SEGMEN 3 · JEBAKAN OPTIONAL (1)
Satu Blok atau Dua Blok OPTIONAL?
Tebak isi tabel dulu, lalu jalankan.

  Satu blok: semua atau tidak                   Dua blok: masing-masing

    BAGIAN YANG BERBEDA                                                BAGIAN YANG BERBEDA

    OPTIONAL { ?film dbo:releaseDate ?rilis .                         OPTIONAL { ?film dbo:releaseDate ?rilis }
               ?film dbo:budget ?anggaran }                           OPTIONAL { ?film dbo:budget ?anggaran }


    Jalankan                                                                  Jalankan

   3 baris                                                             3 baris

   #    ?film                 ?rilis           ?anggaran             #    ?film                 ?rilis           ?anggaran

   1    dbr:Following          –                   –                    1    dbr:Following        1998-09-12         –

   2    dbr:Insomnia           –                   –                    2    dbr:Insomnia           –               46000000

  Aturan3    dbr:Mementopraktis: satu OPTIONAL2000-09-05untuk satu informasi9000000pelengkap. Tulis pola wajib3    dbr:Mementolebih dulu, karena OPTIONAL2000-09-05menempel pada9000000solution di
  sebelah kirinya. Tanda – berarti tidak terikat.




WEB SEMANTIK · TIF2108 · PERTEMUAN 10


---

## Halaman 14

SEGMEN 3 · JEBAKAN OPTIONAL (2)
FILTER di Dalam atau di Luar OPTIONAL?
Tebak berapa baris yang tersisa, lalu jalankan.

  Di dalam: menyaring tanggal                      Di luar: menyaring film

    BAGIAN YANG BERBEDA                                                BAGIAN YANG BERBEDA

    OPTIONAL { ?film dbo:releaseDate ?rilis                           OPTIONAL { ?film dbo:releaseDate ?rilis }
      FILTER ( YEAR(?rilis) >= 2000 ) }                               FILTER ( YEAR(?rilis) >= 2000 )


    Jalankan                                                                  Jalankan

   3 baris                                                             1 baris

   #     ?film                        ?rilis                        #      ?film                      ?rilis

   1     dbr:Following                   –                           1      dbr:Memento               2000-09-05

   2     dbr:Insomnia                    –                               Insomnia ikut terbuang: YEAR dari variabel kosong adalah error, dan error
                                                                                  dibaca false.
   3     dbr:Memento                 2000-09-05
  Tanyakan sebelum menulis FILTER: syarat ini menyaring nilai pelengkap, atau menyaring entitasnya?  Semua film tampil; tanggal sebelum 2000 dikosongkan.



WEB SEMANTIK · TIF2108 · PERTEMUAN 10


---

## Halaman 15

SEGMEN 3 · NEGASI
Mencari yang Belum Tercatat
Film Nolan mana yang belum punya tanggal rilis di graf ini? Tiga cara, satu jawaban.


 A · FILTER NOT EXISTS    B · OPTIONAL + !BOUND    C · MINUS
                                                                          1 baris

  SPARQL · DATA CONTOH FILM                                                                          #          ?film

  SELECT ?film WHERE {                                                  1         dbr:Insomnia
    ?film dbo:director dbr:Christopher_Nolan .
    FILTER NOT EXISTS { ?film dbo:releaseDate ?r }
  }                                                                     Dipakai untuk audit kualitas data dan daftar kurasi: entitas
                                                           mana yang propertinya belum diisi.
SPARQL 1.1. Paling mudah dibaca: simpan film yang tidak memiliki triple releaseDate.

                                                               Baca hasilnya sebagai belum tercatat, bukan “tidak pernah
                                                                                                         rilis” (dunia terbuka, Pertemuan 9).





WEB SEMANTIK · TIF2108 · PERTEMUAN 10


---

## Halaman 16

SEGMEN 3 · UNION
UNION: Cocok dengan Salah Satu Pola

  Tampilkan cabang (BIND)    DISTINCT
                                                                       5 baris

  SPARQL · SUTRADARA ATAU PRODUSER                                                                       #        ?judul

  SELECT ?judul WHERE {                                              1       "Following" @en
    ?film rdfs:label ?judul .
                                                                    2       "Following" @en    { ?film dbo:director dbr:Christopher_Nolan }
    UNION                                                                    3       "Insomnia" @en
    { ?film dbo:producer dbr:Christopher_Nolan }
  }                                                                 4       "Man of Steel" @en
  ORDER BY ?judul
                                                                    5       "Memento" @en


   PAKAI       KETIKA
                                                                      Following muncul dua kali karena cocok lewat kedua cabang.
   OPTIONAL   ada informasi tambahan yang boleh kosong                                                                                       Ini kejanggalan kedua dalam bentuk lain: pintu masuk ke
                                                          Segmen 04.
  UNION       ada dua jalan berbeda menuju jawaban yang sama





WEB SEMANTIK · TIF2108 · PERTEMUAN 10


---

## Halaman 17

03
Membentuk Hasil:
DISTINCT, Urutan,
Agregasi

30 menit · kota yang muncul dua kali · DISTINCT dan batasnya ·
ORDER BY · paginasi · GROUP BY · latihan


                                                                                                                                               Foto: Lucas George Wendt · Unsplash



WEB SEMANTIK · TIF2108 · PERTEMUAN 10


---

## Halaman 18

SEGMEN 4 · MENELUSURI KEJANGGALAN 2
Mengapa Medan Muncul Dua Kali

                                                                                                  Telusuri jalur

                                   ex:KotaMetropolitan
                      instanceOf                                                                                               SELECT ?kota: Medan, Medan, Surabaya.                                                                                   3 baris        ex:medan                                                          subclassOf
                                                                                   #   ?kota           ?kelas  (tak terlihat)
                                                                      ex:Kota
                        instanceOf
                                                                                1   ex:medan       ex:KotaDiIndonesia
                                                          subclassOf
                                                                                2   ex:medan       ex:KotaMetropolitan
                                    ex:KotaDiIndonesia
                                                                                3   ex:surabaya    ex:KotaDiIndonesia
                         instanceOf

        ex:surabaya
                                                                   Dua jalan menuju Kota berarti dua solution.
                                                                                           Variabel perantara tidak Anda tulis, tetapi tetap
  POLA JALUR DAN ARTINYA                                                 membentuk baris.

  ?kota ex:instanceOf/ex:subclassOf* ex:Kota .
  # dievaluasi seperti:
  ?kota  ex:instanceOf  ?kelas .
  ?kelas ex:subclassOf* ex:Kota .



WEB SEMANTIK · TIF2108 · PERTEMUAN 10


---

## Halaman 19

SEGMEN 4 · DISTINCT
DISTINCT Membuang Baris yang Identik

  DISTINCT     ikutkan ?kelas
                                                                       3 baris

  SPARQL · DATA CONTOH KOTA                                                                       #          ?nama

  SELECT ?nama WHERE {                                               1         "Medan" @id
    ?kota ex:instanceOf/ex:subclassOf* ex:Kota ;
                                                                    2         "Medan" @id          rdfs:label ?nama .
  }                                                                    3         "Surabaya" @id
  ORDER BY ?nama

Coba nyalakan DISTINCT, lalu ikutkan ?kelas. Mengapa baris Medan tidak lagi       Yang dibandingkan     Semua kolom yang di-SELECT, bukan satu kolom
dibuang?                                                                                                                saja.

                                                                Kapan bekerja          Setelah proyeksi, sebelum LIMIT.

                                                                Kapan tidak dipakai     Saat frekuensi itu sendiri informasinya.





WEB SEMANTIK · TIF2108 · PERTEMUAN 10


---

## Halaman 20

SEGMEN 4 · BATAS DISTINCT
Saat DISTINCT Tidak Menolong
Data contoh: Medan punya dua angka populasi. Pilih cara membentuk tabel, lalu lihat rata-ratanya.


  Baris mentah     SELECT DISTINCT ?nama ?populasi    MAX per kota (GROUP BY)


  SPARQL · DATA CONTOH KOTA
                                                                          5 baris

  SELECT ?nama ?populasi WHERE {                                                                          #     ?nama                       ?populasi
    ?kota ex:instanceOf/ex:subclassOf* ex:Kota ;
          ex:populasi ?populasi ;                                       1     "Medan" @id                 2097610
          rdfs:label ?nama .
                                                                       2     "Medan" @id                 2097610  }
  ORDER BY ?nama ?populasi                                                                       3     "Medan" @id                 2435252

                                                                       4     "Medan" @id                 2435252
 MAX adalah aturan bisnis: terbesar belum tentu terbaru. Tuliskan
                                                                       5     "Surabaya" @id              2874314  aturan Anda sebelum menghitung.


                                                                                                      Rata-rata 5 baris            Rata-rata 3 baris            Rata-rata 2 kota, MAX
                                                                                    mentah                 DISTINCT           2.654.783
                                                             2.388.007,6      2.469.058,7



WEB SEMANTIK · TIF2108 · PERTEMUAN 10


---

## Halaman 21

SEGMEN 4 · ORDER BY
Urutan yang Bisa Diandalkan

 ORDER BY ?rilis    ORDER BY DESC(?rilis)    ORDER BY ?judul    tanpa ORDER BY


  SPARQL · DATA CONTOH FILM
                                                                       3 baris

  SELECT ?judul ?rilis WHERE {                                                                       #     ?judul                       ?rilis
    ?film dbo:director dbr:Christopher_Nolan ;
          rdfs:label ?judul .                                        1     "Insomnia" @en                   –
    OPTIONAL { ?film dbo:releaseDate ?rilis }
                                                                    2     "Following" @en              1998-09-12  }
  ORDER BY ?rilis                                                                    3     "Memento" @en                2000-09-05

  Pola sepuluh besar: ORDER BY DESC(…) lalu LIMIT 10. Urutkan           Naik: sel kosong (Insomnia) diurutkan paling awal, sesuai spesifikasi SPARQL
  dulu, baru potong. Tambah pemecah seri bila nilai bisa sama: ORDER      1.1 bagian 15.1.
  BY DESC(?populasi) ?kota.





WEB SEMANTIK · TIF2108 · PERTEMUAN 10


---

## Halaman 22

SEGMEN 4 · LIMIT DAN OFFSET
Memotong Hasil Menjadi Halaman
Empat film diurutkan menurut judul, dua baris per halaman. Geser halamannya.

Halaman:  1    2    3    OFFSET = (1 − 1) × 2 = 0


  SPARQL · DATA CONTOH FILM
                                                                  1 · Following   2 · Insomnia     3 · Man of     4 · Memento
                                                                                                      Steel  SELECT ?judul WHERE {
    ?film a dbo:Film ;
          rdfs:label ?judul .
  }                                                               2 baris
  ORDER BY ?judul
                                                                  #          ?judul  LIMIT 2 OFFSET 0

                                                               1         "Following" @en

                                                               2         "Insomnia" @en



  Butuh urutan total. Tanpa ORDER BY dan          OFFSET besar tetap mahal. Server tetap            Endpoint punya batas sendiri. Batas waktu dan
  pemecah seri, halaman 2 bisa mengulang baris       menghitung baris yang dilewati.                      batas baris server tidak tergantikan oleh LIMIT
  halaman 1.                                                                                      Anda.



WEB SEMANTIK · TIF2108 · PERTEMUAN 10


---

## Halaman 23

SEGMEN 4 · GROUP BY DAN AGREGAT
Dari Baris ke Ringkasan
Satu kelompok per kota. Pilih fungsi agregatnya.


  COUNT    SUM    AVG    MIN    MAX    SAMPLE    GROUP_CONCAT


  SPARQL · DATA CONTOH KOTA
                                                                       2 baris

  SELECT ?nama (COUNT(?p) AS ?hasil) WHERE {                                                                       #      ?nama                            ?hasil
    ?k ex:populasi ?p ;
       rdfs:label ?nama .                                            1      "Medan" @id                      2
  }
                                                                    2      "Surabaya" @id                   1  GROUP BY ?nama
  ORDER BY ?nama
                                                                      Jumlah nilai populasi per kota.

  Dua aturan: variabel non-agregat di SELECT wajib ada di GROUP BY,       Jumlah film per sutradara di DBpedia (VALUES + GROUP BY)
  sama seperti SQL. Hitung entitas dengan COUNT(DISTINCT …):
  UNION film Nolan memberi COUNT 5, COUNT(DISTINCT) 4.





WEB SEMANTIK · TIF2108 · PERTEMUAN 10


---

## Halaman 24

SEGMEN 4 · HAVING DAN VALUES
Menyaring Kelompok, Membatasi Masukan


  HAVING · KOTA DENGAN LEBIH DARI SATU ANGKA POPULASI                   VALUES · HANYA ENTITAS YANG ANDA SEBUT

   HAVING    coba pakai FILTER                                          SPARQL · DATA CONTOH FILM

    SPARQL · DATA CONTOH KOTA                                         SELECT ?judul ?anggaran WHERE {
                                                                        VALUES ?film { dbr:Memento dbr:Insomnia }
    SELECT ?nama (COUNT(?p) AS ?n) WHERE {                              ?film rdfs:label ?judul ;
      ?k ex:populasi ?p ;                                                     dbo:budget ?anggaran .
         rdfs:label ?nama .                                           }
    }                                                                 ORDER BY ?judul
    GROUP BY ?nama
    HAVING ( COUNT(?p) > 1 )                                                                     2 baris

                                                                     #      ?judul                         ?anggaran   1 baris

                                                                  1      "Insomnia" @en                46000000   #         ?nama                               ?n

                                                                  2      "Memento" @en                 9000000   1         "Medan" @id                         2

  FILTER menyaring baris sebelum dikelompokkan; HAVING menyaring                 Satu query dengan daftar menggantikan banyak query kecil dalam loop: aturan
  kelompok sesudahnya.                                                                  etika ketiga dari Pertemuan 9.





WEB SEMANTIK · TIF2108 · PERTEMUAN 10


---

## Halaman 25

LATIHAN BERPASANGAN · 7 MENIT
Tebak Hasilnya Sebelum Mesin Menjawab


  DATA CONTOH FILM DAN KOTA           Nolan = dbr:Christopher_Nolan · – = triple tidak ada
                                                                            SOAL A
   ?film           director   producer   releaseDate   budget                                                                                                 SELECT ?f ?a WHERE {
                                                                                                   ?f dbo:director Nolan .
   Following      Nolan      Nolan      1998-09-12     –                        OPTIONAL { ?f dbo:budget ?a }
                                                                                                   FILTER ( ?a > 10000000 )
   Memento        Nolan       –          2000-09-05    9000000              }

                                                                              Berapa baris hasilnya?   Insomnia       Nolan       –            –             46000000
                                                                            SOAL B
   Man of Steel    –          Nolan       –                –
                                                                                                 SELECT (COUNT(?f) AS ?n)
                                                                                                 WHERE {
   ?k            label         instanceOf              populasi                 { ?f dbo:director Nolan }
                                                                                                   UNION
                             KotaMetropolitan       2435252                  { ?f dbo:producer Nolan }   medan        Medan
                             KotaDiIndonesia        2097610                }

                                                                              Berapa nilai ?n?   surabaya     Surabaya     KotaDiIndonesia        2874314
                                                                            SOAL C

                                                                                                 SELECT ?nama (COUNT(*) AS ?n)
                                                                                                 WHERE {
                                                                                                   ?k instanceOf ?kelas ;
                                                                                                      populasi ?p ;
                                                                                                      label ?nama .
                                                                                                 }
                                                                                                 GROUP BY ?nama

WEB SEMANTIK · TIF2108 · PERTEMUAN 10                                           Berapa ?n untuk Medan?


---

## Halaman 26

04
Live-Coding: Dari
Editor ke DataFrame

40 menit · A memperbaiki Query A di WDQS · B Nolan lengkap di
DBpedia · C JSON ke pandas · D olah lokal




                                                                                                                                               Foto: Markus Spiske · Unsplash



WEB SEMANTIK · TIF2108 · PERTEMUAN 10


---

## Halaman 27

SEGMEN 5 · QUERY BROWSER
Tiga Editor, Satu Bahasa

 WDQS                        DBpedia                     YASGUI

   query.wikidata.org                          dbpedia.org/sparql                          editor generik
  + Prefix otomatis; tampilan peta, timeline,       + Virtuoso; banyak prefix bawaan.             + Satu editor untuk endpoint mana pun,
   bubble.                                                                             dengan auto-complete.                                                                            ! Bisa lambat; data hasil ekstraksi
    ! SERVICE wikibase:label khas Wikidata.          Wikipedia per rilis.                                              ! Endpoint tujuan harus mengizinkan akses
                                                                                                             dari browser.
    Buka editor                                   Buka editor



  Kebiasaan baik: tulis PREFIX lengkap walau editor menyuntikkannya, supaya query bisa dipindah ke endpoint lain atau ke rdflib tanpa
  diubah.





WEB SEMANTIK · TIF2108 · PERTEMUAN 10


---

## Halaman 28

SEGMEN 5 · DEMO A · WDQS
Memperbaiki Query A: Satu Baris per Kota

  1 · Query A apa adanya    2 · Tambah DISTINCT    3 · GROUP BY + MAX


                                                                                 SIMULASI PADA DATA CONTOH KOTA (REKAAN)
  SPARQL · QUERY.WIKIDATA.ORG

                                                                             5 baris  SELECT ?kota ?namaKota ?populasi WHERE {
    ?kota wdt:P31/wdt:P279* wd:Q515 ;                                                                             #   ?kota           ?namaKota          ?populasi
          wdt:P17 wd:Q252 ;
          wdt:P1082 ?populasi ;                                            1   ex:surabaya     "Surabaya" @id     2874314
          rdfs:label ?namaKota .
                                                                         2   ex:medan        "Medan" @id        2435252    FILTER ( LANG(?namaKota) = "id" )
  }                                                                         3   ex:medan        "Medan" @id        2435252
  ORDER BY DESC(?populasi)
  LIMIT 10                                                                4   ex:medan        "Medan" @id        2097610

                                                                         5   ex:medan        "Medan" @id        2097610
  Jalankan di Wikidata

                                                                                      Kota mana yang muncul lebih dari sekali?





WEB SEMANTIK · TIF2108 · PERTEMUAN 10


---

## Halaman 29

SEGMEN 5 · DEMO B · DBPEDIA
Film Nolan, Kali Ini Lengkap

  Query B Pertemuan 9    OPTIONAL + MIN + GROUP BY


                                                                                 SIMULASI PADA DATA CONTOH FILM (REKAAN)
  SPARQL · DBPEDIA.ORG/SPARQL

                                                                             2 baris  PREFIX dbo: <http://dbpedia.org/ontology/>
  PREFIX dbr: <http://dbpedia.org/resource/>                                                                             #   ?film              ?judul              ?tahun
  SELECT ?film ?judul ?tahun WHERE {
    ?film a dbo:Film ;                                                    1   dbr:Following     "Following" @en     1998
          dbo:director dbr:Christopher_Nolan ;
                                                                         2   dbr:Memento       "Memento" @en       2000          rdfs:label ?judul ;
          dbo:releaseDate ?rilis .
    BIND ( YEAR(?rilis) AS ?tahun )                                            Bandingkan jumlah baris kedua versi di DBpedia. Selisihnya adalah film
                                                                                    yang hari itu tidak punya dbo:releaseDate. Jangan menyebut judulnya    FILTER ( LANG(?judul) = "en" )
                                                                                sebelum melihat hasil.  }
  ORDER BY ?tahun


  Jalankan di DBpedia





WEB SEMANTIK · TIF2108 · PERTEMUAN 10


---

## Halaman 30

SEGMEN 5 · DEMO C · SPARQLWRAPPER
JSON ke DataFrame, Kolom Tetap Utuh

                                                                                        UJI DI SINI: JSON W3C DARI DATA CONTOH → DATAFRAME
  PYTHON · PIP INSTALL SPARQLWRAPPER PANDAS
                                                                                              Hasil Demo B    Semua tanggal kosong
  from SPARQLWrapper import SPARQLWrapper, JSON
  import pandas as pd                                                                                   Cara lama: kunci per baris     head.vars

  UA = "KelasWebSemantik/1.0 (email@kampus.ac.id)"
                                                                               film                judul          rilisAwal

  def ke_dataframe(endpoint, query):                                                                        0   dbr:Insomnia       Insomnia       NaN
      sp = SPARQLWrapper(endpoint, agent=UA)
                                                                        1   dbr:Following      Following     1998-09-12      sp.setQuery(query); sp.setReturnFormat(JSON)
      hasil = sp.queryAndConvert()
                                                                        2   dbr:Memento        Memento       2000-09-05
      kolom = hasil["head"]["vars"]
      baris = [{k: b.get(k, {}).get("value") for k in kolom}
                                                                                        df.isna().sum()               for b in hasil["results"]["bindings"]]
                                                                                        film       0
      return pd.DataFrame(baris, columns=kolom)                                                                                        judul      0
                                                                                        rilisAwal  1
  Q_NOLAN = """
  PREFIX dbo: <http://dbpedia.org/ontology/>
  PREFIX dbr: <http://dbpedia.org/resource/>
  SELECT ?film ?judul (MIN(?rilis) AS ?rilisAwal) WHERE {

  Salin kode    Unduh demo_c.py


WEB SEMANTIK · TIF2108 · PERTEMUAN 10


---

## Halaman 31

SEGMEN 5 · DEMO D · PANDAS
Ambil Sekali, Periksa, Baru Hitung

                                                                                KELUARAN · DATA CONTOH KOTA SEBAGAI PENGGANTI WIKIDATA
  PYTHON · LANJUTAN DEMO C

                                                                                              5 2
  # lanjutan Demo C: ke_dataframe dan pandas sudah tersedia                                                                                              # 5 baris, tetapi hanya 2 kota
  WDQS = "https://query.wikidata.org/sparql"                                                                kota namaKota  populasi
  Q_KOTA_P9 = """                                                                          1  http://contoh.org/medan    Medan   2435252
  SELECT ?kota ?namaKota ?populasi WHERE {                                             2  http://contoh.org/medan    Medan   2435252
                                                                                              3  http://contoh.org/medan    Medan   2097610
    ?kota wdt:P31/wdt:P279* wd:Q515 ;
                                                                                              4  http://contoh.org/medan    Medan   2097610
          wdt:P17 wd:Q252 ;                                                                                              # empat baris Medan: 2 kelas × 2 populasi
          wdt:P1082 ?populasi ;                                                          2654783.0
          rdfs:label ?namaKota .                                                        # rata-rata setelah MAX per kota
    FILTER ( LANG(?namaKota) = "id" )
  }                                                                                          Periksa dulu          Bila jumlah baris lebih dari jumlah kota, ada
  ORDER BY DESC(?populasi)                                                                                                duplikat.
  LIMIT 50
                                                                                        Aturan yang sama   MAX per kota, sama dengan Demo A.  """
                                                                                                                        Hasilnya harus cocok.

  df = ke_dataframe(WDQS, Q_KOTA_P9)      # Query A apa adanya                                                                               Simpan IRI         Kolom kota (IRI) ikut ke CSV, bukan hanya
  df["populasi"] = pd.to_numeric(df["populasi"])                                                                                                       nama.

  print(len(df), df["kota"].nunique())   # baris vs kota
  print(df[df.duplicated("kota", keep=False)])

  Jalankan pada data contoh     Salin kode
WEB SEMANTIK · TIF2108 · PERTEMUAN 10


---

## Halaman 32

SEGMEN 5 · DIAGNOSIS
Baris Hilang atau Ganda? Cek Ini
Klik setiap gejala untuk melihat penyebab dan langkahnya.


  GEJALA Entitas yang Anda tahu ada           GEJALA Kolom label kosong                    GEJALA Baris identik berulang
         tidak muncul
                                              Tak ada label di bahasa itu, atau SERVICE        Beberapa jalan: jalur kelas, UNION.
  Satu pola wajib tidak cocok.                        label lupa dipasang.                                                      → DISTINCT.
 → Uji per pola; OPTIONAL bila pelengkap.       → Tambah bahasa cadangan, misalnya "id,en".


  GEJALA Entitas sama, nilai berbeda           GEJALA COUNT terlalu besar                   GEJALA Halaman berikut mengulang
                                                                                                baris
  Properti bernilai ganda.                          Duplikat ikut terhitung.
                                                                                            Urutan belum total. → Agregasi dengan aturan tertulis.          → COUNT(DISTINCT …).
                                                      → Pemecah seri di ORDER BY.





WEB SEMANTIK · TIF2108 · PERTEMUAN 10


---

## Halaman 33

SEGMEN 5 · TANTANGAN
Tantangan: Kembalikan Insomnia
Query ini dimaksudkan menampilkan semua film yang disutradarai Nolan beserta tanggal rilis sejak
1990 bila ada. Hasilnya kurang satu film. Perbaiki tanpa menghapus syarat tahunnya.


  SELECT ?judul ?rilis WHERE {                                      2 baris, Insomnia belum muncul. Tidak ada error, jadi
    ?film dbo:director dbr:Christopher_Nolan ;                          masalahnya di letak syarat, bukan sintaks.
          rdfs:label ?judul .
    OPTIONAL { ?film dbo:releaseDate ?rilis }
                                                                             2 baris    FILTER ( YEAR(?rilis) >= 1990 )
  }
                                                                             #     ?judul                     ?rilis
  ORDER BY ?judul
                                                                         1    "Following" @en           1998-09-12

                                                                         2    "Memento" @en             2000-09-05





  Jalankan      Petunjuk     Ulang    PREFIX dbo: dbr: rdfs: sudah tersedia



WEB SEMANTIK · TIF2108 · PERTEMUAN 10


---

## Halaman 34

SEGMEN 5 · LAB CADANGAN
Bila Jaringan Bermasalah: Data Contoh di Browser
Film dan kota dimuat ke satu graf. Pilih contoh, jalankan, lalu ubah query sesuka Anda.


 OPTIONAL    NOT EXISTS    UNION    DISTINCT   GROUP BY    HAVING                          PREFIX dbo: dbr: rdfs: xsd: ex: sudah tersedia


  SELECT ?film ?rilis WHERE {                                            3 baris
    ?film dbo:director dbr:Christopher_Nolan .
                                                                          #     ?film                      ?rilis    OPTIONAL { ?film dbo:releaseDate ?rilis }
  }                                                                      1     dbr:Insomnia                  –
  ORDER BY ?rilis
                                                                      2     dbr:Following             1998-09-12

                                                                      3     dbr:Memento               2000-09-05





  Jalankan    Ctrl/⌘ + Enter



WEB SEMANTIK · TIF2108 · PERTEMUAN 10


---

## Halaman 35

SEGMEN 6 · ETIKA ENDPOINT
Empat Aturan Main di Endpoint Publik
ORDER BY, DISTINCT, dan GROUP BY adalah query termahal yang Anda tulis hari ini. Endpoint publik
menanggung biayanya.

 1          2          3          4
  User-Agent bermakna     LIMIT saat eksplorasi      Cache, jangan looping      Persempit sebelum
                                                                                   agregasi  Nama aplikasi dan kontak.           Termasuk saat mencoba            Simpan hasil ke CSV; ganti
   Klien anonim bisa diblokir.         GROUP BY dan ORDER BY.             seribu query kecil dengan satu       GROUP BY atas seluruh
                                                                     VALUES.                             Wikidata hampir pasti timeout.
                                                                                                                      Batasi dengan pola selektif
                                                                                                               atau VALUES.



  Kaitkan dengan live-coding: siapa yang tadi lupa LIMIT saat mencoba GROUP BY? Timeout adalah cara endpoint publik melindungi
  pengguna lain.





WEB SEMANTIK · TIF2108 · PERTEMUAN 10


---

## Halaman 36

SEGMEN 6 · DISKUSI · 7 MENIT
Dua Pertanyaan untuk Dibawa Pulang
Dua menit refleksi sendiri, lima menit berbagi. Klik “Lihat arah” setelah berdiskusi.

 01                    02
  Dashboard Anda menampilkan rata-rata populasi          Hasil SELECT berupa tabel, bukan graf. Bila Anda
  sepuluh kota terbesar dari Wikidata, dan angkanya       hanya menyimpan kolom nama ke CSV, apa yang
  berbeda dari BPS. Penyebab mana yang ada di             hilang saat data itu ingin digabung lagi dengan
  query, mana yang ada di data, dan bagaimana Anda      sumber lain?
  membuktikannya?


     Arah: Duplikat, aturan MAX, kota yang hilang, tahun data,               Arah: IRI sebagai identitas global, label ambigu dan
      definisi kota.                                                       berbahasa, CONSTRUCT di Pertemuan 11.





WEB SEMANTIK · TIF2108 · PERTEMUAN 10


---

## Halaman 37

RINGKASAN
Lima Hal yang Anda Bawa dari Hari Ini


      WHERE menentukan baris: satu cara mengisi variabel = satu baris. Proyeksi tidak mengubahnya.01

        Pola wajib yang gagal membuang entitas; OPTIONAL mempertahankannya. Letak FILTER menentukan apa02
        yang dibuang.


       Ganda identik dibereskan DISTINCT; ganda berbeda nilai butuh agregasi dengan aturan tertulis.03

        Urutan kerja: WHERE, GROUP BY, ORDER BY, proyeksi dan DISTINCT, lalu OFFSET dan LIMIT.04

        Ambil sekali ke DataFrame dari head.vars, periksa duplikat, baru hitung. Simpan IRI-nya.05





WEB SEMANTIK · TIF2108 · PERTEMUAN 10


---

## Halaman 38

TINDAK LANJUT
Sebelum Pertemuan 11

  PERTEMUAN 11                                       Pekerjaan rumah
 CONSTRUCT dan Hierarki Data                   Ulangi Demo A–D di laptop Anda; kode dan data contoh ada di LMS.
   Dari tabel kembali ke graf: membangun triple baru dari hasil query,                                                                                      Perbaiki pertanyaan Anda untuk Wikidata: minimal satu OPTIONAL
  dan menelusuri hierarki kelas seperti jalur subclass yang hari ini                                                                      dan satu agregasi. Catat jumlah baris sebelum dan sesudah.
  menggandakan Medan.
                                                                                Kerjakan Latihan Pertemuan 10 di repo pertemuan-10.

                                                                       Baca SPARQL 1.1 Query Language, bagian 6 (OPTIONAL) dan 11
                                                                                     (Aggregates).




  REFERENSI
   Antoniou, Groth, van Harmelen & Hoekstra (2012), A Semantic Web Primer, 3rd ed., MIT Press · Segaran, Evans & Taylor (2009), Programming the Semantic Web, O’Reilly ·
   Wood, Zaidman, Ruth & Hausenblas (2014), Linked Data, Manning · Rietveld & Hoekstra (2017), The YASGUI family of SPARQL clients, Semantic Web 8(3) · W3C (2013),
  SPARQL 1.1 Query Language dan Query Results JSON Format · Wikidata SPARQL tutorial · SPARQLWrapper documentation · DBpedia, Querying DBpedia.





WEB SEMANTIK · TIF2108 · PERTEMUAN 10


---

## Halaman 39

PENUTUP · TANYA-JAWAB
Query Anda menghasilkan
berapa baris, dan bisakah Anda
menjelaskan setiap barisnya?

Sebelum menghitung apa pun dari hasil query, pastikan Anda tahu dari mana setiap baris berasal.


  Pola menentukan baris    Anda menentukan bentuk tabel    Sampai jumpa di Pertemuan 11





WEB SEMANTIK · TIF2108 · PERTEMUAN 10
