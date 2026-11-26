# Web_Semantik_P13_GraphRAG_NL2SPARQL

---

## Halaman 1

```text
WEB SEMANTIK P13 · PERTEMUAN 13 · TIF2108




Knowledge Graph,
LLM, dan RAG
Dari pertanyaan bahasa manusia menuju jawaban yang bersumber dari Knowledge Graph. Deck
pembelajaran: dari GraphRAG sampai NL2SPARQL.

 Mata kuliah: Web Semantik (TIF2108)             Pertemuan 13         Fokus: GraphRAG, NL2SPARQL, live-coding, etika dan biaya


Singkatan: P13 = Pertemuan 13 · LLM = Large Language Model (model bahasa besar) · RAG = Retrieval-Augmented Generation (jawaban disusun setelah mengambil informasi) ·
GraphRAG = Graph Retrieval-Augmented Generation (RAG yang mengambil data dari graf) · NL2SPARQL = Natural Language to SPARQL (bahasa alami ke SPARQL) · SPARQL = SPARQL
Protocol and RDF Query Language · RDF = Resource Description Framework




WEB SEMANTIK · TIF2108 · PERTEMUAN 13
```

---

## Halaman 2

```text
PETA PEMBELAJARAN


Pada Pertemuan Ini Kita Akan Belajar
   1       Mengapa LLM membutuhkan                                 2        Bagaimana GraphRAG mengambil                            3       Bagaimana pertanyaan bahasa
           grounding dan sumber data.                                       subgraf dari Knowledge Graph.                                   alami diterjemahkan menjadi
                                                                                                                                            SPARQL.



   4       Bagaimana query diperiksa                               5        Bagaimana Python, RDFLib, OWL-                          6       Apa risiko etika, privasi, biaya, dan
           sebelum dijalankan.                                              RL, dan Wikidata digunakan dalam                                beban endpoint.
                                                                            demo.



   Hasil belajar: mahasiswa mampu menjelaskan alur GraphRAG dan NL2SPARQL, membaca contoh query, serta memahami mengapa validasi
   dan sumber jawaban diperlukan.


Singkatan: RDFLib = RDF Library, pustaka Python untuk mengolah RDF · OWL-RL = pustaka Python untuk reasoning profil OWL 2 RL · OWL = Web Ontology Language · RL = Rule Language (profil OWL
yang bisa dijalankan dengan aturan)




WEB SEMANTIK · TIF2108 · PERTEMUAN 13
```

---

## Halaman 3

```text
BAGIAN 1


Mengapa LLM Perlu Grounding?
LLM dapat menyusun kalimat yang lancar, tetapi kelancaran tidak otomatis berarti jawabannya benar.

TANTANGAN YANG DIBAHAS DALAM MATERI                              Coba: bandingkan dua cara menjawab pertanyaan yang sama.

  Halusinasi                                                     “Siapa pelukis Mona Lisa?”
  model dapat menghasilkan informasi yang tidak didukung data.    Jawab dari ingatan     Jawab dengan grounding

                                                                  DIAMBIL DARI GRAF MUSEUM · EX: = HTTP://CONTOH.ID/MUSEUM/
  Pengetahuan tidak selalu mutakhir
  jawaban dapat tidak sesuai keadaan data saat ini.
                                                                   SELECT ?pelukis WHERE {
                                                                       ex:MonaLisa ex:dilukisOleh ?pelukis
  Sulit melacak sumber                                             }
  jawaban belum tentu menunjukkan fakta berasal dari mana.
                                                                   Artinya: hasil query: ex:Leonardo. Jawaban diikat ke data yang baru
                                                                   diambil, dan sumbernya bisa ditunjukkan:
  Grounding mengikat jawaban model pada data yang diambil saat     http://contoh.id/museum/Leonardo.
  itu.

                                                                   Penjelasan sederhana: mahasiswa yang menjawab ujian
                                                                   berdasarkan ingatan berbeda dengan mahasiswa yang
                                                                   menjawab sambil menunjukkan halaman buku atau sumber
                                                                   datanya. Grounding membantu sistem menunjukkan dasar
                                                                   jawabannya.
WEB SEMANTIK · TIF2108 · PERTEMUAN 13
```

---

## Halaman 4

```text
BAGIAN 2


RAG: Mengambil Informasi Sebelum Menjawab
RAG (Retrieval-Augmented Generation) menggabungkan pencarian informasi dan pembuatan jawaban.
Tekan Lanjut (→) untuk menelusuri alurnya.


 1                              2                           3                          4                           5
 Chunking                       Embedding                   Retrieval / top-k          Konteks                     Jawaban
 Dokumen dipecah
 menjadi potongan.
                          →     Potongan diubah
                                menjadi deretan angka
                                                        →   Sistem mencari k
                                                            potongan yang paling
                                                                                   →   Potongan terpilih
                                                                                       diberikan kepada LLM.
                                                                                                               →   LLM menyusun jawaban
                                                                                                                   berdasarkan konteks
                                yang mewakili               relevan.                                               tersebut.
                                maknanya.




  Keterbatasan yang dibahas: pencarian berbasis potongan teks dapat kesulitan jika jawaban membutuhkan hubungan beberapa fakta,
  pertanyaan multi-hop (beberapa langkah relasi), atau pertanyaan global (jawabannya tersebar di seluruh data).



  Penjelasan sederhana: Vector RAG (RAG berbasis vektor embedding) mencari teks yang mirip dengan pertanyaan. Namun, kemiripan teks
  tidak selalu sama dengan kemampuan menelusuri hubungan antar-entitas.




WEB SEMANTIK · TIF2108 · PERTEMUAN 13
```

---

## Halaman 5

```text
BAGIAN 2 · COBA SENDIRI


Lima Potongan Teks, Satu Pertanyaan
Sebagai pengganti embedding, skor di sini = jumlah kata    POTONGAN TEKS (REKAAN) · SKOR · DUA TERATAS (TOP-2)

yang sama dengan pertanyaan, tanpa kata di, ada,
                                                            C1     Mona Lisa dilukis oleh Leonardo dan dipajang di Louvre.                              2
mana, oleh, dan, yang, adalah, pun. Sama dengan
rag_mainan.py.
                                                            C2    Louvre adalah museum di Paris.                                                        0
Coba: ganti pertanyaannya, lalu lihat potongan mana yang
terambil.                                                   C3    Paris terletak di Prancis.                                                            0

 Mona Lisa ada di negara mana?                              C4    Leonardo sezaman dengan Michelangelo.                                                 0

 Mona Lisa ada di negara mana?                              C5    Replika Mona Lisa dijual di toko suvenir negara mana pun.                             3

 Di kota mana Louvre berada?                                 Artinya: dua teratas = C5 + C1. Rantai Louvre → Paris → Prancis (C2, C3) tidak terbawa,
                                                             sehingga model harus menebak negaranya. C5 terambil karena kata “negara”, padahal isinya
 Siapa yang sezaman dengan Leonardo?                         tentang suvenir.

 KATA DARI PERTANYAAN                                      Singkatan: C1–C5 = chunk (potongan teks) nomor 1 sampai 5
 lisa · mona · negara




WEB SEMANTIK · TIF2108 · PERTEMUAN 13
```

---

## Halaman 6

```text
BAGIAN 3


Mengapa Knowledge Graph?
Knowledge Graph menyimpan fakta sebagai entitas dan hubungan.

  CONTOH TRIPLE RDF (TURTLE)


   ex:MonaLisa               ex:dilukisOleh                ex:Leonardo .

                                                                                                      ex:MonaLisa         ex:dilukisOleh         ex:Leonardo
Coba: klik tiap bagian triple, atau tombol di bawah.

  Subject        Predicate        Object


Singkatan: ex: = prefiks (awalan) untuk alamat http://contoh.id/museum/ · Turtle = Terse RDF
Triple Language, format penulisan RDF yang dipakai berkas .ttl
                                                                                               Node mewakili entitas.

                                                                                               Edge mewakili relasi.

                                                                                               Sekumpulan fakta yang saling terhubung membentuk subgraf.


                                                                                                 Penjelasan sederhana: “Mona Lisa — dilukis oleh — Leonardo”.
                                                                                                 Relasi dinyatakan secara eksplisit, bukan hanya tersirat dalam
                                                                                                 kalimat.


WEB SEMANTIK · TIF2108 · PERTEMUAN 13
```

---

## Halaman 7

```text
BAGIAN 4


Apa Itu GraphRAG?
GraphRAG adalah pendekatan RAG yang unit retrieval-nya berupa
node, relasi, atau subgraf dari Knowledge Graph. Hasil retrieval
diberikan kepada LLM sebagai konteks. Tekan Lanjut (→).

  Node / anchor      ex:MonaLisa                                             ex:MonaLisa                                     ex:Paris

                     Entitas jangkar yang disebut atau ditemukan dari
                     pertanyaan.                                                           lokasiDi               lokasiDi
                                                                                                                                    lokasiDi

  Relation / path    ex:lokasiDi                                             dilukisOleh
                                                                                                      ex:Louvre
                     Relasi yang ditelusuri dari anchor.

                                                                                                                                          ex:Prancis
  Subgraph           MonaLisa → Louvre → Paris → Prancis
                     Kumpulan fakta terhubung yang relevan dengan            ex:Leonardo
                     pertanyaan.


  Inti: model menerima fakta dan hubungan yang diambil dari graf,
  sehingga tidak perlu menebak hubungan antar-entitas.

                                                                        Penjelasan sederhana: Vector RAG mengambil potongan paragraf;
                                                                        GraphRAG mengambil fakta dan hubungan dalam graf.



WEB SEMANTIK · TIF2108 · PERTEMUAN 13
```

---

## Halaman 8

```text
BAGIAN 5


Lima Tahap GraphRAG
Tekan Lanjut (→) untuk membuka contoh setiap tahap dalam materi.

  TAHAP                        KEGIATAN                                                                                                     CONTOH DALAM MATERI

  1. Ingest                    Mengumpulkan dokumen, database, API, atau dump                                                               SPARQL endpoint dan CONSTRUCT

  2. Extraction                NER/LLM mengusulkan triple kandidat                                                                          Mengidentifikasi entitas dan relasi

  3. Construction              Memetakan ke ontologi, menormalkan IRI, menggabungkan duplikasi                                              RDF, ontology, sameAs

  4. Index                     Menyimpan di triple store; ringkasan node dapat di-embedding                                                 RDFLib Graph, file .ttl

  5. Retrieval                 Anchor → n-hop → subgraph → context                                                                          Mengambil konteks untuk LLM



Singkatan: API = Application Programming Interface · NER = Named Entity Recognition (pengenalan nama entitas dalam teks) · IRI = Internationalized Resource Identifier (alamat unik sebuah entitas) ·
.ttl = berkas Turtle



   Peringatan dari materi: kesalahan pada tahap Construction, seperti IRI duplikat atau sameAs yang keliru, dapat terbawa ke banyak
   jawaban.



   Penjelasan sederhana: kualitas jawaban tidak hanya ditentukan oleh LLM. Kualitas graf dan proses pembentukannya juga sangat penting.
WEB SEMANTIK · TIF2108 · PERTEMUAN 13
```

---

## Halaman 9

```text
BAGIAN 6


Memahami Hop
Hop adalah satu langkah menelusuri relasi dari sebuah node.

  RANTAI LOKASI PADA MUSEUM.TTL                                                         PERTANYAAN KELAS

                                                                                        Jika pertanyaan hanya menanyakan
  ex:MonaLisa ex:lokasiDi ex:Louvre .
  ex:Louvre       ex:lokasiDi ex:Paris .
                                                                                        museum tempat Mona Lisa berada, apakah
  ex:Paris        ex:lokasiDi ex:Prancis .                                              kita perlu menelusuri sampai tiga hop?


DARI MONA LISA    1 hop      2 hop    3 hop                                             Cukup 1 hop

                                                                                        Perlu 2 hop

                                                                                        Perlu 3 hop

    ex:MonaLisa   lokasiDi    ex:Louvre   lokasiDi   ex:Paris   lokasiDi   ex:Prancis

                                                                                        Penjelasan sederhana: lebih banyak hop tidak
                                                                                        selalu lebih baik. Hop yang terlalu jauh dapat
                                                                                        menambah konteks yang tidak diperlukan.
  1 HOP · DIJALANKAN PADA MUSEUM.TTL


  SELECT ?t WHERE { ex:MonaLisa ex:lokasiDi ?t }

1 hop: Louvre

WEB SEMANTIK · TIF2108 · PERTEMUAN 13
```

---

## Halaman 10

```text
BAGIAN 7


Asserted Graph dan OWL RL Closure
Asserted graph: triple yang dinyatakan secara eksplisit dalam data. Closure: graf yang                           # closure, 1 hop dari ex:MonaLisa: 10 triple
                                                                                                                 1 ex:MonaLisa ex:lokasiDi ex:Prancis .
diperluas dengan fakta hasil reasoning berdasarkan aturan inferensi.
                                                                                                                 1    ex:MonaLisa rdf:type ex:Objek .
Coba: klik baris tabel untuk melihat triple subgrafnya dari ex:MonaLisa.                                         1    ex:MonaLisa ex:dibuatOleh dbr:Leonardo_da_Vinci .
                                                                                                                 1    ex:MonaLisa rdf:type ex:Karya .
                                                                                                                 1    ex:MonaLisa ex:dilukisOleh dbr:Leonardo_da_Vinci .
                               JUMLAH                   HALAMAN               PRANCIS
  POLA PADA SLIDE                                                                                                1    ex:MonaLisa ex:lokasiDi ex:Paris .
                               TRIPLE                   INI                   DITEMUKAN?                         1    ex:MonaLisa ex:dibuatOleh ex:Leonardo .
                                                                                                                 1    ex:MonaLisa rdf:type ex:Lukisan .
                                                                                                                 1    ex:MonaLisa ex:lokasiDi ex:Louvre .
  Asserted, 1 hop              2                        2                     Tidak
                                                                                                                 1    ex:MonaLisa ex:dilukisOleh ex:Leonardo .

  Asserted, 2 hop              6                        6                     Tidak

  Asserted, 3 hop              10                       10                    Ya

  OWL RL closure, 1
                               12                       10                    Ya
  hop

  OWL RL closure, 2
                               58                       34                    Ya                                     Penjelasan sederhana: reasoning dapat membuat fakta
  hop
                                                                                                                     yang dibutuhkan tersedia lebih dekat. Namun, closure
  OWL RL closure, 3
                               97                       49                    Ya
                                                                                                                     juga dapat memperbesar jumlah triple dan konteks.
  hop

Catatan penting: angka “Jumlah triple” adalah hasil eksperimen pada museum.ttl di slide (Python, owlrl          Singkatan: rdf:, rdfs:, owl: = prefiks kosakata standar RDF, RDFS (RDF
7.6.2), bukan aturan universal untuk semua graf. Kolom “Halaman ini” dihitung ulang di browser; untuk closure   Schema), dan OWL · dbr: = DBpedia resource, prefiks entitas DBpedia
angkanya lebih kecil karena reasoner halaman tidak menyimpan triple trivial seperti a owl:Thing.

WEB SEMANTIK · TIF2108 · PERTEMUAN 13
```

---

## Halaman 11

```text
BAGIAN 8


Tiga Pola Retrieval GraphRAG
  A · Neighbors      B · Path      C · Structured Query / NL2SPARQL


 SPARQL · POLA A                                                            10 triple    closure

  CONSTRUCT {                                                               ex:MonaLisa rdf:type ex:Karya .
      ex:MonaLisa ?p ?o                                                     ex:MonaLisa rdf:type ex:Lukisan .
  }                                                                         ex:MonaLisa rdf:type ex:Objek .
  WHERE {                                                                   ex:MonaLisa ex:dibuatOleh ex:Leonardo .
      ex:MonaLisa ?p ?o                                                     ex:MonaLisa ex:dibuatOleh dbr:Leonardo_da_Vinci .
                                                                            ex:MonaLisa ex:dilukisOleh ex:Leonardo .
  }
                                                                            ex:MonaLisa ex:dilukisOleh dbr:Leonardo_da_Vinci .
                                                                            ex:MonaLisa ex:lokasiDi ex:Louvre .
Neighbors: mengambil semua triple keluar dari anchor.                       ex:MonaLisa ex:lokasiDi ex:Paris .
                                                                            ex:MonaLisa ex:lokasiDi ex:Prancis .
 Jalankan pada asserted    Jalankan pada closure

                                                                             Artinya: 10 triple, termasuk MonaLisa lokasiDi Prancis. Di Python,
                                                                             owlrl menghitung 12 karena ikut menyimpan triple trivial.

  Penting: ketiga pola retrieval dilakukan sebelum LLM menyusun jawaban. Model menerima hasil retrieval, bukan harus membaca seluruh
  graf.



WEB SEMANTIK · TIF2108 · PERTEMUAN 13
```

---

## Halaman 12

```text
BAGIAN 9


Hybrid Retrieval
Hybrid retrieval menggabungkan pencarian semantik dan penelusuran graf. Tekan Lanjut (→) untuk
mengikuti alurnya.


 1                                   2                             3                              4                            5
 Pertanyaan
 “lukisan senyum misterius di
                                → Vector / label
                                  Menemukan IRI terdekat:
                                                             → Graf
                                                               Subgraf satu hop: 10 triple
                                                                                             → LLM
                                                                                               Menerima subgraf sebagai
                                                                                                                          → Kode
                                                                                                                            Menempelkan IRI sumber
 Paris”                              ex:MonaLisa                                                  konteks                      pada jawaban



 # subgraf satu hop dari ex:MonaLisa (closure, tanpa triple trivial)
 ex:MonaLisa ex:dibuatOleh dbr:Leonardo_da_Vinci .                                     Peran masing-masing: embedding/vector membantu
 ex:MonaLisa ex:dibuatOleh ex:Leonardo .                                               menemukan entitas dari bahasa bebas; graph traversal
 ex:MonaLisa ex:dilukisOleh dbr:Leonardo_da_Vinci .
 ex:MonaLisa ex:dilukisOleh ex:Leonardo .
                                                                                       menelusuri hubungan setelah entitas ditemukan.
 ex:MonaLisa ex:lokasiDi ex:Louvre .
 ex:MonaLisa ex:lokasiDi ex:Paris .
 ex:MonaLisa ex:lokasiDi ex:Prancis .                                                  Penjelasan sederhana: mesin pencari membantu
 ex:MonaLisa rdf:type ex:Karya .
 ex:MonaLisa rdf:type ex:Lukisan .
                                                                                       menemukan “orang yang dimaksud”; Knowledge Graph
 ex:MonaLisa rdf:type ex:Objek .                                                       membantu memeriksa hubungan orang tersebut dengan fakta
                                                                                       lain.




WEB SEMANTIK · TIF2108 · PERTEMUAN 13
```

---

## Halaman 13

```text
BAGIAN 10


Vector RAG vs GraphRAG
  ASPEK                          VECTOR RAG                                            GRAPHRAG

  Unit retrieval                 Potongan teks                                         Node, relasi, subgraf

  Multi-hop                      Lemah jika fakta tidak berada dalam satu chunk        Kuat melalui penelusuran graf

  Pertanyaan global              Sulit dengan top-k chunk                              Dapat memakai SPARQL aggregation atau community summary

  Traceability                   File dan posisi chunk                                 IRI per fakta

  Biaya awal                     Embedding relatif rendah                              Ontologi dan resolusi entitas lebih mahal

  Pemeliharaan                   Re-embedding saat dokumen berubah                     Memperbarui triple dan menjaga konsistensi skema

  Cocok untuk                    FAQ, dokumen, pencarian ringan                        Domain dengan relasi padat dan kebutuhan traceability



   Kesimpulan materi: GraphRAG cocok ketika relasi antar-fakta padat dan keterlacakan sumber diperlukan. Untuk kebutuhan sederhana,
   Vector RAG sering kali sudah cukup.


Singkatan: FAQ = Frequently Asked Questions (daftar pertanyaan yang sering diajukan)



WEB SEMANTIK · TIF2108 · PERTEMUAN 13
```

---

## Halaman 14

```text
BAGIAN 11


Semantic Layer
Semantic Layer menjadi lapisan yang menjelaskan arti istilah sebelum agen atau LLM mengakses
database atau graf.

                                 Agen atau LLM                   Tiga manfaat menurut materi

                                                                 1
                “Berapa mahasiswa aktif semester ini?”
                                                                        Agen tidak menebak nama kolom atau properti.

                                         ↓
                                                                 2      Definisi istilah seragam untuk semua tim.
                               Semantic Layer
                       Arti: mahasiswa aktif · IPK · prasyarat   3      Satu titik untuk kontrol akses dan audit.


                                         ↓                           DISKUSI KELAS

                                                                     Entitas apa di kampus yang layak masuk Semantic Layer? Relasi apa yang
                              Database atau graf                     paling sering ditanyakan mahasiswa?

Singkatan: IPK = Indeks Prestasi Kumulatif




WEB SEMANTIK · TIF2108 · PERTEMUAN 13
```

---

## Halaman 15

```text
BAGIAN 12


NL2SPARQL: Dari Bahasa Manusia ke Query
NL2SPARQL menerjemahkan pertanyaan dalam bahasa alami (Natural Language) menjadi query
SPARQL.

                                                        ALURNYA (LANJUT → )
“Siapa pembuat Pieta?”
 QUERY
                                                          1   Pengguna menulis pertanyaan.


  SELECT ?s WHERE {                                       2   LLM membuat query SPARQL.
      ex:Pieta ex:dibuatOleh ?s
  }
                                                          3   Sistem memeriksa query.
  LIMIT 10
                                                          4   Query yang lolos dijalankan pada graf.

 Jalankan pada museum.ttl                                 5   Hasil query digunakan untuk menyusun jawaban.

  #           ?s
                                                          LLM membantu menulis query; Knowledge Graph
  1           ex:Michelangelo                             menyediakan fakta.




WEB SEMANTIK · TIF2108 · PERTEMUAN 13
```

---

## Halaman 16

```text
BAGIAN 13


Empat Langkah NL2SPARQL
Tekan Lanjut (→) untuk membuka penawar setiap risiko.

 LANGKAH         ISI                                    RISIKO                          PENAWAR

                 Kirim kelas dan properti yang boleh
 1. Skema                                               Model mengarang IRI             Skema di prompt; guard memeriksa IRI
                 dipakai

 2. Contoh       2–3 pasangan pertanyaan dan query      Contoh terlalu seragam          Variasikan pola dasar, path, agregasi

                                                        Sintaks salah, tanpa LIMIT,
 3. Validasi     Parse lokal sebelum query dijalankan                                   prepareQuery, wajib LIMIT, hanya SELECT
                                                        UPDATE

 4.                                                     Model menambah fakta dari       Jawab dari data; hasil kosong berarti tidak
                 Model merangkai hasil query
 Verbalisasi                                            ingatan                         ditemukan



  Penjelasan sederhana: empat langkah ini adalah inti NL2SPARQL dalam materi. Jangan melompat langsung dari prompt ke eksekusi query.




WEB SEMANTIK · TIF2108 · PERTEMUAN 13
```

---

## Halaman 17

```text
BAGIAN 14


Skema Diambil dari Graf
Skema harus berasal dari graf, bukan diciptakan oleh model.

  QUERY PADA SLIDE                                                             5 baris

  SELECT ?p ?d ?r WHERE {                                                      #    ?p                      ?d               ?r
      ?p a owl:ObjectProperty .
      OPTIONAL { ?p rdfs:domain ?d }                                           1    ex:dibuatOleh           ex:Karya         ex:Seniman
      OPTIONAL { ?p rdfs:range ?r }
                                                                               2    ex:dilukisOleh          ex:Lukisan       ex:Pelukis
  }
  ORDER BY ?p                                                                  3    ex:lokasiDi              –               –


?p properti · ?d domain · ?r range · OPTIONAL: domain atau range dapat tidak   4    ex:melukis               –               –

tersedia.
                                                                               5    ex:sezamanDengan         –               –

 Jalankan pada graf asserted

                                                                               Jebakan: ex:melukis tidak memiliki domain dan range pada
                                                                               graf asserted. Prompt tetap perlu menjelaskan arah relasi:
                                                                               Pelukis → Lukisan.




WEB SEMANTIK · TIF2108 · PERTEMUAN 13
```

---

## Halaman 18

```text
BAGIAN 15


Prompt NL2SPARQL
 CONTOH ISI PROMPT                                             Coba: klik bagian untuk menyorotnya di prompt.
                                                                1. Skema
  Terjemahkan pertanyaan ke SPARQL untuk graf museum.
                                                                Daftar IRI yang boleh dipakai, termasuk arah relasi.
  # SKEMA: hanya IRI berikut yang boleh dipakai
  PREFIX ex: <http://contoh.id/museum/>                         2. Contoh
                                                                Dua pola berbeda, misalnya query dasar dan path.
  Kelas:
  ex:Lukisan ex:Patung ex:Karya ex:Pelukis ex:Museum ex:Kota    3. Aturan
                                                                Query saja, hanya SELECT, selalu LIMIT ≤ 50.
  ex:dilukisOleh (Lukisan → Pelukis)
  ex:dibuatOleh (Karya → Seniman)
  ex:melukis (Pelukis → Lukisan)
                                                                4. Pertanyaan
  ex:lokasiDi (transitif)                                       Teks pertanyaan pengguna.

  # CONTOH                                                      Lukisan apa saja yang dilukis Leonardo?
  T: Siapa pembuat Pieta?
  Q: SELECT ?s WHERE { ex:Pieta ex:dibuatOleh ?s } LIMIT 10
                                                                 replace()      format()       Salin
  T: Di mana saja Louvre berada?
  Q: SELECT ?t WHERE { ex:Louvre ex:lokasiDi+ ?t } LIMIT 10
                                                                 PROMPT.format(pertanyaan=t)
  # ATURAN                                                       KeyError: ' ex'
  Query saja, tanpa penjelasan.
  Hanya SELECT.
  Selalu LIMIT ≤ 50.                                             Artinya: Jebakan Python: .format() menganggap kurung
                                                                 kurawal milik SPARQL sebagai placeholder. Slide
  T: {pertanyaan}
  Q:
                                                                 menyarankan replace().

                                                               Singkatan: T: = tanya (pertanyaan) · Q: = query jawabannya


WEB SEMANTIK · TIF2108 · PERTEMUAN 13
```

---

## Halaman 19

```text
BAGIAN 16


Guard: Periksa Dulu, Baru Jalankan
Guard memeriksa query sebelum dieksekusi.

 FUNGSI YANG DITAMPILKAN DALAM MATERI                                    Coba: klik pemeriksaan untuk menyorot barisnya di kode.

                                                                           1 Sintaks query sah.
  def aman(q, maks=50):
      try:
         a = prepareQuery(q, initNs=NS).algebra
                                                                           2 Jenis query adalah SELECT.
      except Exception:
             return False, "query tidak sah"                               3 LIMIT tersedia dan tidak lebih dari 50.

      if a.name != "SelectQuery":                                          4 Semua IRI dikenal.
             return False, "hanya SELECT"
                                                                         KOSAKATA berisi semua IRI dari graf asserted. iri_di() menelusuri pohon
      lim = a.p.length if a.p.name == "Slice" else None
                                                                         query.

                                                                         Singkatan: NS = namespace: pasangan prefiks dan alamat, misalnya ex: →
      if lim is None or lim > maks:                                      http://contoh.id/museum/ · initNs = initial namespaces, prefiks yang dikenal saat
             return False, f"wajib LIMIT ≤ {maks}"                       query di-parse · NM = namespace manager · n3() = menulis IRI dalam notasi N3
                                                                         (Notation3), misalnya ex:Leonardo
      asing = sorted(i.n3(NM) for i in iri_di(a) if i not in KOSAKATA)


      if asing:
             return False, "IRI tidak dikenal: " + ", ".join(asing)


      return True, "ok"




WEB SEMANTIK · TIF2108 · PERTEMUAN 13
```

---

## Halaman 20

```text
BAGIAN 17


Contoh Query yang Diterima dan Ditolak
Coba: tebak hasil guard, lalu klik baris.   Periksa semua   SELECT ?k WHERE { ?k ex:dilukisOleh ex:Leonardo } LIMIT 10

 1   Pola benar, LIMIT 10                              ?


 2   Tanpa LIMIT                                       ?    Periksa, lalu jalankan

 3   LIMIT 500                                         ?
                                                            Penting: lolos guard bukan berarti query pasti benar secara semantik
 4   ex:namaLengkap                                    ?    atau pasti menghasilkan data.

 5   ex:MonaLiza (salah ketik)                         ?

                                                            Penjelasan sederhana: guard yang dicontohkan memeriksa
 6   DELETE WHERE { … }                                ?
                                                            struktur query dan kosakata. Ia tidak otomatis memahami
 7   Kurung kurawal hilang                             ?    apakah arah relasi sesuai maksud pertanyaan.

 8   CONSTRUCT … LIMIT 10                              ?




WEB SEMANTIK · TIF2108 · PERTEMUAN 13
```

---

## Halaman 21

```text
BAGIAN 18


Verbalisasi: Graf Menjawab, Model Merangkai
  Ada hasil       Hasil kosong       Query ditolak    Tiga kemungkinan setelah query dibuat



 1   LLM menerjemahkan pertanyaan            “Lukisan apa saja yang dilukis Leonardo?”
                                             SELECT ?k WHERE { ?k ex:dilukisOleh ex:Leonardo } LIMIT 10
                                             lolos ok
 2   Guard memeriksa query
                                              ATURAN PROMPT VERBALISASI + DATA
 3   Query dijalankan pada closure
                                              Jawab HANYA dari data di bawah. Jika data tidak cukup, katakan tidak cukup. Jangan
 4   LLM merangkai kalimat                    menambah fakta dari ingatan Anda.
                                              Pertanyaan: Lukisan apa saja yang dilukis Leonardo?
 5   Kode menempel IRI sumber                 Data:
                                              ex:MonaLisa


                                             return → [jawaban model, dirangkai dari data]
                                             Sumber: http://contoh.id/museum/MonaLisa




  Jebakan: “jangan menambah fakta” adalah permintaan, bukan jaminan. Karena itu sumber ditempel oleh kode, dan hasil kosong tidak
  dikirim ke model.



WEB SEMANTIK · TIF2108 · PERTEMUAN 13
```

---

## Halaman 22

```text
BAGIAN 19 · LATIHAN


Tebak Hasil Sebelum Mesin Menjawab
Gunakan museum.ttl apa adanya: graf asserted, tanpa reasoner. Instruksi: tulis triple yang cocok
terlebih dahulu, baru hitung hasilnya.


  A
        Relasi masuk dan keluar dari Michelangelo.
        Berapa baris?                                B     Path lokasi Louvre. Berapa baris?
                                                                                               C     Lukisan Leonardo. Berapa baris?


    SPARQL · MUSEUM.TTL ASSERTED                       SPARQL · MUSEUM.TTL ASSERTED              SPARQL · MUSEUM.TTL ASSERTED


    SELECT * WHERE {                                   SELECT ?t WHERE {                         SELECT ?k WHERE {
        { ex:Michelangelo ?p ?o }                          ex:Louvre ex:lokasiDi+ ?t                 ex:Leonardo ex:melukis ?k
        UNION                                          }                                         }
        { ?s ?p ex:Michelangelo }                                                                LIMIT 10
    }                                                Tebakan:                     Cek
                                                                                               Tebakan:                    Cek
  Tebakan:                    Cek




WEB SEMANTIK · TIF2108 · PERTEMUAN 13
```

---

## Halaman 23

```text
BAGIAN 20


Live-coding: Empat Demo
PERSIAPAN DARI SLIDE
                                                                           DEMO   ISI
  TERMINAL


  pip install rdflib owlrl sparqlwrapper
                                                                           A      Python: RDFLib dan OWL-RL; subgraf sebagai konteks


BAHAN
                                                                           B      Python: NL2SPARQL lokal; guard memutuskan sebelum query jalan

museum.ttl
                                                                           C      Python: mengambil konteks dari endpoint publik Wikidata
prompt_museum.txt

nl2sparql.py                                                               D      Python: alur utuh dan jawaban ber-sumber

Satu chatbot di browser

Singkatan: pip = Package Installer for Python, pemasang pustaka Python ·
.txt = berkas teks biasa · .py = berkas program Python




WEB SEMANTIK · TIF2108 · PERTEMUAN 13
```

---

## Halaman 24

```text
BAGIAN 21 · DEMO A


271 Triple Menjadi 10
  KODE INTI DARI SLIDE                                                                                           Graf                   Triple graf                     Triple konteks

  from rdflib import Graph, URIRef, OWL, RDFS                                                                    Asserted               40                              2
  from owlrl import DeductiveClosure, OWLRL_Semantics
                                                                                                                 Closure                271                             10
  asserted = Graph().parse("museum.ttl")
                                                                                                               Hasil pada slide (Python, owlrl 7.6.2). Coba: ganti jangkar dan graf; konteks dihitung ulang di
  closure = Graph() + asserted                                                                                 halaman ini.
  DeductiveClosure(OWLRL_Semantics).expand(closure)
                                                                                                                 MonaLisa           Louvre         Leonardo          Pieta           asserted
  nm = asserted.namespace_manager
  TRIVIAL = {OWL.Thing, RDFS.Resource}
                                                                                                                 closure
  def konteks(g, jangkar):
      return sorted(                                                                                             # konteks(closure, ex:MonaLisa) · 10 triple
          " ".join(x.n3(nm) for x in (s, p, o)) + " ."                                                           ex:MonaLisa ex:dibuatOleh dbr:Leonardo_da_Vinci .
          for s, p, o in g.triples((jangkar, None, None))                                                        ex:MonaLisa ex:dibuatOleh ex:Leonardo .
          if o not in TRIVIAL and o != jangkar                                                                   ex:MonaLisa ex:dilukisOleh dbr:Leonardo_da_Vinci .
      )                                                                                                          ex:MonaLisa ex:dilukisOleh ex:Leonardo .
                                                                                                                 ex:MonaLisa ex:lokasiDi ex:Louvre .
                                                                                                                 ex:MonaLisa ex:lokasiDi ex:Paris .
  Salin kode        Unduh demo_a.py            Unduh museum.ttl                                                  ex:MonaLisa ex:lokasiDi ex:Prancis .
                                                                                                                 ex:MonaLisa rdf:type ex:Karya .

Singkatan: URIRef = URI Reference, tipe rdflib untuk IRI; URI = Uniform Resource Identifier · nm = namespace
manager                                                                                                           Inti: seluruh graf tidak dikirim ke model. Program memilih fakta yang
                                                                                                                  relevan dari entitas jangkar.




WEB SEMANTIK · TIF2108 · PERTEMUAN 13
```

---

## Halaman 25

```text
BAGIAN 22 · DEMO B


NL2SPARQL Lokal
 KODE INTI DARI SLIDE
                                                                    “Lukisan apa saja yang dilukis Leonardo?”                           Jalankan
                                                                    SELECT ?k WHERE { ?k ex:dilukisOleh ex:Leonardo } LIMIT 10
  from nl2sparql import ke_sparql, aman, llm_tempel, closure, NS
                                                                    lolos ok · 1 baris: ex:MonaLisa
  for t in [
      "Lukisan apa saja yang dilukis Leonardo?",
                                                                    “Di negara mana Mona Lisa berada?”                                  Jalankan
      "Di negara mana Mona Lisa berada?",
      "Siapa nama lengkap Leonardo?"                                SELECT ?t WHERE { ex:MonaLisa ex:lokasiDi ?t } LIMIT 10
  ]:                                                                lolos ok · 3 baris: ex:Prancis, ex:Paris, ex:Louvre
      q = ke_sparql(t, llm_tempel)

     ok, pesan = aman(q)
                                                                    “Siapa nama lengkap Leonardo?”                                      Jalankan
     print(pesan, "|", q)                                           SELECT ?n WHERE { ex:Leonardo ex:namaLengkap ?n } LIMIT 5
                                                                    ditolak IRI tidak dikenal: ex:namaLengkap
      if ok:
          for baris in closure.query(q, initNs=NS):
                                                                     Tempel query dari chatbot di sini
              print("   ", *baris)


                                                                     Periksa dan jalankan
 Salin kode     Unduh demo_b.py       Unduh nl2sparql.py
                                                                   Keluaran model dapat berbeda. Query yang lolos guard belum tentu benar secara
                                                                   semantik.




WEB SEMANTIK · TIF2108 · PERTEMUAN 13
```

---

## Halaman 26

```text
BAGIAN 23 · DEMO C


Wikidata
Materi menggunakan endpoint publik Wikidata untuk mengambil karya Leonardo.

                                                                        CATATAN
 SPARQL
                                                                        PREFIX ditulis lengkap.
  PREFIX wd: <http://www.wikidata.org/entity/>
  PREFIX wdt: <http://www.wikidata.org/prop/direct/>                    Label diambil lewat rdfs:label.
  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
  SELECT ?karya ?judul ?tahun WHERE {                                   Slide tidak menggunakan SERVICE wikibase:label.
    ?karya wdt:P170 wd:Q762 ; wdt:P31 wd:Q3305213 ; wdt:P571 ?tahun .
    OPTIONAL { ?karya rdfs:label ?id FILTER(LANG(?id) = "id") }         Hasil bergantung pada isi Wikidata saat query dilakukan.
    OPTIONAL { ?karya rdfs:label ?en FILTER(LANG(?en) = "en") }
    BIND(COALESCE(?id, ?en) AS ?judul)                                  Catat tanggal pengambilan dan jumlah baris.
  } ORDER BY ?tahun LIMIT 10                                            Halaman ini tidak memanggil Wikidata; tombol membuka query di Wikidata Query
                                                                        Service (WDQS).

 Buka di Wikidata Query Service      Salin query   Unduh demo_c.py      Singkatan: wd: = Wikidata entity (entitas) · wdt: = Wikidata direct property
                                                                        (properti langsung) · Q762 = Leonardo da Vinci · P31 = instance of (jenis) ·
 INTI PYTHON DARI SLIDE                                                 Q3305213 = lukisan · P170 = pencipta · P571 = waktu dibuat · "id" / "en" =
                                                                        kode bahasa Indonesia / Inggris · URL = Uniform Resource Locator · UA = User-
  s = SPARQLWrapper(URL, agent=UA)                                      Agent, identitas program yang mengirim permintaan · JSON = JavaScript Object
  s.setQuery(Q)                                                         Notation · WDQS = Wikidata Query Service
  s.setReturnFormat(JSON)

  r = s.queryAndConvert()
  rows = r["results"]["bindings"]



WEB SEMANTIK · TIF2108 · PERTEMUAN 13
```

---

## Halaman 27

```text
BAGIAN 24 · DEMO D


Alur Utuh
 STRUKTUR FUNGSI JAWAB() DARI SLIDE                              1      Lukisan apa saja yang dilukis Leonardo?

  def jawab(pertanyaan, llm):                                    2      Di negara mana Mona Lisa berada?
      q = ke_sparql(pertanyaan, llm)

                                                                 3      Siapa nama lengkap Leonardo?
      ok, pesan = aman(q)
      if not ok:
          return f"Query ditolak ({pesan})."                     4      Lukisan apa saja yang dilukis Michelangelo?

      rows = list(closure.query(q, initNs=NS))                   1      Terjemahkan pertanyaan.
      if not rows:
          return "Tidak ditemukan di graf."                      2      Validasi query.

      data = "\n".join(                                          3      Jalankan query pada closure.
          " | ".join(x.n3(NM) for x in r)
          for r in rows                                          4      Jika kosong, hentikan dan beri pesan.
      )
                                                                 5      Kirim data hasil query ke LLM.
      teks = llm(
          f"{ATURAN}\nPertanyaan: {pertanyaan}\nData:\n{data}"   6      Tempelkan IRI sumber menggunakan kode.
      )

                                                                 # model menulis: SELECT ?t WHERE { ex:MonaLisa ex:lokasiDi ?t } LIMIT 10
      iri = sorted({
                                                                 # data ke model: ex:Prancis · ex:Paris · ex:Louvre
          str(x) for r in rows for x in r
                                                                 return [jawaban model, dirangkai dari data]
          if isinstance(x, URIRef)
      })                                                         Sumber: http://contoh.id/museum/Louvre, http://contoh.id/museum/Paris,
                                                                 http://contoh.id/museum/Prancis
      return teks + "\nSumber: " + ", ".join(iri)

                                                                     Prinsip: fakta berasal dari graf, bahasa berasal dari model, atribusi sumber
 Salin demo_d.py        Unduh demo_d.py                              dikerjakan oleh kode.


WEB SEMANTIK · TIF2108 · PERTEMUAN 13
```

---

## Halaman 28

```text
BAGIAN 25


Kejanggalan: Dari Mana Model Tahu?
“Di negara mana Mona Lisa berada?”
                                                                            Jika model menjawab “Prancis”, dari mana ia
  DATA YANG DIBERIKAN KEPADA MODEL                                          tahu?
  ex:Louvre
                                                                            Kemungkinan model menggunakan pengetahuan dari ingatannya,
  ex:Paris                                                                  bukan hanya data yang diberikan.
  ex:Prancis

                                                                            Pelajaran: jawaban yang benar menurut pengetahuan umum
Sumber IRI juga disertakan. Namun, tidak ada satu triple pun dalam contoh
                                                                            belum tentu terbukti oleh sumber data yang dipakai sistem.
tersebut yang menyatakan bahwa Prancis adalah negara.

Coba: periksa sendiri di graf.
                                                                            Jika jawaban harus dibuktikan oleh graf, graf harus memuat
 Apa tipe ex:Prancis?    SELECT ?c WHERE { ex:Prancis a ?c } → 0 baris
                                                                            fakta atau relasi yang relevan dan query harus mengambilnya.




WEB SEMANTIK · TIF2108 · PERTEMUAN 13
```

---

## Halaman 29

```text
BAGIAN 26


Diagnosis Masalah
Depan kartu: gejala. Tebak penyebabnya, lalu balik kartunya.

  GEJALA 1                                         GEJALA 2                                          GEJALA 3                                   GEJALA 4
  KeyError(' ex')                                  Query ditolak “tidak sah”                         Hasil kosong padahal fakta ada             Properti karangan

  PENYEBAB DAN PENANGANAN                          PENYEBAB DAN PENANGANAN                           PENYEBAB DAN PENANGANAN                    PENYEBAB DAN PENANGANAN
  Penyebab: .format() pada teks berisi {}.         Penyebab: prefix tidak dikenal.                   Penyebab: query di graf asserted.          Penyebab: skema tidak dikirim atau tidak
  Penanganan: gunakan replace().                   Penanganan: lengkapi PREFIX atau initNs.          Penanganan: jalankan pada closure.         jelas. Penanganan: skema dari graf; cek
                                                                                                                                                IRI.


  GEJALA 5                                         GEJALA 6                                          GEJALA 7
  Fakta di luar data                               HTTP 429 atau timeout WDQS                        Query Wikidata gagal setelah
                                                                                                     backend berubah
  PENYEBAB DAN PENANGANAN                          PENYEBAB DAN PENANGANAN
  Penyebab: model menambah dari ingatan.           Penyebab: query berat atau terlalu sering.        PENYEBAB DAN PENANGANAN
  Penanganan: aturan verbalisasi; sumber           Penanganan: LIMIT, User-Agent, simpan             Penyebab: SERVICE wikibase:label, prefix
  dari kode.                                       hasil.                                            bawaan. Penanganan: PREFIX lengkap,
                                                                                                     rdfs:label.



Singkatan: HTTP = Hypertext Transfer Protocol; kode 429 = Too Many Requests (permintaan terlalu sering)




WEB SEMANTIK · TIF2108 · PERTEMUAN 13
```

---

## Halaman 30

```text
BAGIAN 27


Etika dan Biaya
Materi menekankan empat aturan main.


  1                                     2                              3                             4
  Beban endpoint                        Kebocoran data                 Biaya token                   Atribusi
  Gunakan LIMIT, User-Agent             Prompt ke API pihak ketiga     Skema panjang di setiap       Jawaban menyertakan IRI
  bermakna, dan simpan hasil.           dapat meninggalkan             prompt membutuhkan biaya.     sumber. Tanpa itu, sistem
  Jangan biarkan banyak laptop          lingkungan kampus. Untuk       Kirim bagian skema yang       hanya menjadi chatbot lain
  menjalankan loop ke WDQS              data mahasiswa, gunakan        relevan dan simpan pasangan   tanpa jejak sumber yang jelas.
  secara bersamaan.                     model lokal atau anonimisasi   tanya-query.
                                        terlebih dahulu.




WEB SEMANTIK · TIF2108 · PERTEMUAN 13
```

---

## Halaman 31

```text
BAGIAN 28


Guard Bukan Otorisasi
SKENARIO DISKUSI DALAM SLIDE                                           BEDAKAN TIGA LAPISAN (LANJUT → )


Query “IPK semua mahasiswa angkatan 2023” sah,                           Prompt: mengarahkan model.
memiliki LIMIT, dan semua IRI dikenal. Guard
meloloskannya.
                                                                         Guard: memeriksa bentuk dan kosakata query.
Apa yang salah?

                                                                         Otorisasi: menentukan data apa yang boleh diakses
  Guard memeriksa bentuk query, bukan hak akses pengguna.
                                                                         pengguna.

  Arah solusi dalam materi: otorisasi harus dilakukan di server atau
  Semantic Layer, bukan hanya di prompt.




WEB SEMANTIK · TIF2108 · PERTEMUAN 13
```

---

## Halaman 32

```text
BAGIAN 29


Diskusi Kelas
  PERTANYAAN 1                                                                          PERTANYAAN 2
  Kampus ingin chatbot yang menjawab “Siapa dosen pengampu mata kuliah                  Query “IPK semua mahasiswa angkatan 2023” sah, ber-LIMIT, dan semua IRI
  prasyarat X?” Sumbernya PDF pedoman akademik. Pilih Vector RAG atas PDF atau          dikenal. Guard meloloskannya. Apa yang salah dan di lapisan mana harus
  graf kampus?                                                                          dicegah?

  ARAH JAWABAN                                                                          ARAH JAWABAN
  Pertimbangkan: berapa hop yang diperlukan? Seberapa sering data berubah? Siapa yang   Guard memeriksa bentuk, bukan hak akses. Otorisasi berada di server atau Semantic Layer.
  merawat graf? Apa biaya masing-masing pilihan?



Singkatan: PDF = Portable Document Format




WEB SEMANTIK · TIF2108 · PERTEMUAN 13
```

---

## Halaman 33

```text
BAGIAN 30


Lima Hal yang Harus Diingat
1       Model bahasa fasih, tetapi tidak otomatis membawa jejak sumber. Grounding mengikat jawaban ke data yang diambil saat
        itu.

2       RAG vektor mengambil potongan teks yang mirip dengan pertanyaan; ia tidak menelusuri relasi antar-fakta.

3       GraphRAG mengambil subgraf dari entitas jangkar. Reasoning dapat membuat fakta tersedia dengan penelusuran yang
        lebih pendek.

4       NL2SPARQL membutuhkan skema dari graf, contoh bervariasi, dan guard sebelum query dijalankan.

5       Hasil kosong dijawab “tidak ditemukan”. Sumber ditempel oleh kode, bukan oleh model.




WEB SEMANTIK · TIF2108 · PERTEMUAN 13
```

---

## Halaman 34

```text
BAGIAN 31


Latihan dan Tindak Lanjut
   Sebelum Pertemuan 14                                          UNTUK PRESENTASI PROYEK


        Ulangi Demo A–D.
                                                                 1 Tunjukkan skema.
        Gunakan kode dan museum.ttl dari LMS.                    2 Tunjukkan minimal tiga query yang berjalan.
        Pasang alur Demo B pada graf kampus.
                                                                 3 Tunjukkan satu jawaban ber-sumber.
        Ambil skema dari query pada slide skema (bagian 14).

        Buat dua contoh pertanyaan dan query.                    4 Buktikan bahwa jawaban hanya berasal dari graf.
        Siapkan lima pertanyaan uji.

        Catat hasil setiap query: lolos, ditolak, atau kosong.



Singkatan: LMS = Learning Management System (kelas.usu.ac.id)




WEB SEMANTIK · TIF2108 · PERTEMUAN 13
```

---

## Halaman 35

```text
BAGIAN 32


Kuis Pemahaman
Jawab dalam hati, lalu balik kartunya. Nomor bagian di balik kartu menunjukkan tempat jawabannya
dibahas.

 SOAL 1                             SOAL 2                             SOAL 3                           SOAL 4                             SOAL 5
 Apa perbedaan unit retrieval       Apa yang dimaksud node,            Mengapa tahap Construction       Apa perbedaan asserted             Apa arti tanda + pada
 Vector RAG dan GraphRAG?           edge, subgraf, dan hop?            penting dalam GraphRAG?          graph dan OWL RL closure?          property path SPARQL?

 JAWABAN                            JAWABAN                            JAWABAN                          JAWABAN                            JAWABAN
 Vector RAG: potongan teks.         Node = entitas; edge = relasi;     IRI duplikat atau sameAs yang    Asserted: triple eksplisit dalam   Relasi diikuti satu kali atau lebih.
 GraphRAG: node, relasi, subgraf.   subgraf = fakta yang saling        keliru dapat terbawa ke banyak   data. Closure: graf yang           (bagian 8)
 (bagian 10)                        terhubung; hop = satu langkah      jawaban. (bagian 5)              diperluas fakta hasil reasoning.
                                    menelusuri relasi. (bagian 3, 6)                                    (bagian 7)


 SOAL 6                             SOAL 7                             SOAL 8                           SOAL 9                             SOAL 10
 Mengapa skema harus                Apa empat langkah                  Apa saja yang diperiksa oleh     Mengapa hasil kosong tidak         Mengapa guard tidak sama
 diberikan kepada LLM?              NL2SPARQL?                         guard dalam contoh materi?       dikirim kepada model?              dengan otorisasi?

 JAWABAN                            JAWABAN                            JAWABAN                          JAWABAN                            JAWABAN
 Agar model tidak mengarang IRI;    Skema, contoh, validasi,           Sintaks sah, hanya SELECT,       Sistem menjawab “Tidak             Guard memeriksa bentuk dan
 skema memuat kelas, properti,      verbalisasi. (bagian 13)           LIMIT ada dan ≤ 50, semua IRI    ditemukan di graf.” tanpa          kosakata query, bukan hak
 dan arah relasi. (bagian 13–15)                                       dikenal. (bagian 16)             memberi model kesempatan           akses. (bagian 28)
                                                                                                        menambah fakta. (bagian 18)




WEB SEMANTIK · TIF2108 · PERTEMUAN 13
```

---

## Halaman 36

```text
BAGIAN 33


Referensi dalam Materi
BUKU DAN ARTIKEL                                                                                     SPESIFIKASI DAN DOKUMENTASI

Antoniou, G., Groth, P., van Harmelen, F., & Hoekstra, R. (2012). A Semantic Web                     W3C (2013). SPARQL 1.1 Query Language.
Primer (3rd ed.). MIT Press.
                                                                                                     Wikidata Query Service: User Manual dan halaman WDQS backend update.
Lewis, P., dkk. (2020). Retrieval-Augmented Generation for Knowledge-Intensive
                                                                                                     RDFLib, OWL-RL, SPARQLWrapper.
NLP Tasks. arXiv:2005.11401.
                                                                                                     Ollama API.
Peng, B., dkk. (2024). Graph Retrieval-Augmented Generation: A Survey.
arXiv:2408.08921.

Edge, D., dkk. (2024). From Local to Global: A Graph RAG Approach to Query-
Focused Summarization. arXiv:2404.16130.

Scherp, A., dkk. (2024). Semantic Web: Past, Present, and Future.
arXiv:2412.17159.


Singkatan: 3rd ed. = third edition (edisi ketiga) · MIT = Massachusetts Institute of Technology · dkk. = dan kawan-kawan · NLP = Natural Language Processing · arXiv = nama repositori artikel
pracetak, bukan singkatan · W3C = World Wide Web Consortium




WEB SEMANTIK · TIF2108 · PERTEMUAN 13
```

---

## Halaman 37

```text
PENUTUP




Graf tahu faktanya, model tahu
bahasanya.
Bagian mana dari sistem Anda yang memutuskan apa yang benar?

 Data dan relasi berasal dari Knowledge   Model membantu menerjemahkan dan
                                                                               Guard memeriksa query.
 Graph.                                   menyusun bahasa.

                                          Kode menempelkan sumber yang dapat
 Otorisasi mengendalikan akses.
                                          ditelusuri.


Akhir Pertemuan 13 — Web Semantik




WEB SEMANTIK · TIF2108 · PERTEMUAN 13
```
