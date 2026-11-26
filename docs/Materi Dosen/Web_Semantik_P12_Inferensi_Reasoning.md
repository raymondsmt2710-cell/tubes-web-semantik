# Web_Semantik_P12_Inferensi_Reasoning

---

## Halaman 1

```text
PERTEMUAN 12 · TIF2108 · SUB-CPMK 6 (BAGIAN 2)




Inferensi dan
Reasoning
Bagaimana mesin menurunkan fakta baru dari fakta yang ada dan aturan semantik, dan bagaimana
penalaran itu membantu menemukan pemodelan yang keliru.

 Mata Kuliah Web Semantik    Program Studi Teknologi Informasi   3 SKS · 150 menit




WEB SEMANTIK · TIF2108 · PERTEMUAN 12
```

---

## Halaman 2

```text
RENCANA SESI · 150 MENIT


Alur Pertemuan Hari Ini
 15 · Pembuka   20 · Konsep          25 · RDFS     20 · OWL           10          25 · Python             20 · Protégé   15 · Kuis



 WAKTU            KEGIATAN                               FOKUS

 0–15             Pembukaan dan pemantik                 Mengapa mesin perlu menyimpulkan fakta?

 15–35            Konsep dasar                           Asserted, inferred, closure, reasoner

 35–60            Aturan RDFS                            Domain, range, subPropertyOf, subClassOf

 60–80            Konstruksi OWL                         Transitive, Symmetric, inverseOf, sameAs, disjointWith

 80–90            Istirahat atau diskusi singkat         Refleksi

 90–115           Praktik Python                         RDFLib dan OWL-RL

 115–135          Demo Protégé dan konsistensi           Menjalankan reasoner dan memeriksa hasil

 135–150          Kuis dan rangkuman                     Menguji pemahaman




WEB SEMANTIK · TIF2108 · PERTEMUAN 12
```

---

## Halaman 3

```text
SUB-CPMK 6 · BAGIAN 2


Setelah Sesi Ini, Anda Mampu…
  01                                    02                             03                                04
  Menjelaskan                           Menerapkan                     Memprediksi                       Menjalankan
  Beda asserted facts, inferred         Aturan domain, range,          Kesimpulan dari                   Reasoner OWL-RL di Python
  facts, closure, dan reasoner.         subPropertyOf, dan             TransitiveProperty,               dan HermiT di Protégé, lalu
                                        subClassOf untuk               SymmetricProperty,                membaca pesan
                                        menurunkan fakta dengan        inverseOf, sameAs, dan            inkonsistensi.
                                        tangan.                        disjointWith.

    Dicek: kuis 1–2                      Dicek: pertanyaan Oyen         Dicek: adegan OWL                  Dicek: praktik




  Cara memakai halaman ini: setiap contoh menampilkan datanya secara lengkap. Tebak dulu kesimpulannya, baru tekan tombol reasoner.
  Nama aturan bergaris titik-titik bisa diklik untuk melihat artinya.




WEB SEMANTIK · TIF2108 · PERTEMUAN 12
```

---

## Halaman 4

```text
GAMBARAN UMUM


Fakta yang Tidak Pernah Ditulis
Dalam Web Semantik, data tidak hanya berisi fakta yang ditulis.       Coba: tanyakan pada data apa adanya, lalu tanyakan lagi setelah reasoner
                                                                      bekerja.
Sistem juga dapat menurunkan fakta baru dari fakta yang ada dan
aturan semantik yang berlaku. Proses ini disebut inferensi atau         TIGA KALIMAT DI KIRI, DITULIS SEBAGAI RDF

reasoning.
                                                                        :MonaLisa    rdf:type           :Lukisan .
                                                                        :Lukisan     rdfs:subClassOf :KaryaSeni .
1     Mona Lisa adalah sebuah lukisan.
                                                                        :KaryaSeni rdfs:subClassOf :Objek .

2     Setiap lukisan merupakan karya seni.
                                                                       Tanya tanpa reasoner     Tanya setelah reasoner

3     Setiap karya seni merupakan objek.
                                                                                                Artinya: reasoner menerapkan aturan subkelas

Apakah Mona Lisa sebuah objek?
                                                                      true                      dua kali: Lukisan → KaryaSeni → Objek.
                                                                                                Kesimpulan itu kini tersimpan; graf berisi 6
                                                                                                triple, 3 ditulis dan 3 disimpulkan.




    Inti yang perlu dipahami: Web Semantik memungkinkan mesin memahami hubungan antardata dan menarik kesimpulan berdasarkan
    makna yang dinyatakan dalam ontologi.



WEB SEMANTIK · TIF2108 · PERTEMUAN 12
```

---

## Halaman 5

```text
01
Istilah Dasar dan Cara
Kerja
asserted · inferred · closure · reasoner · forward chaining · query-time
reasoning


                                                                           Foto: Alex Beauchamp · Unsplash




WEB SEMANTIK · TIF2108 · PERTEMUAN 12
```

---

## Halaman 6

```text
ISTILAH DASAR


Empat Istilah, Satu Contoh
Coba: tekan tombol, lalu baca keempat kartu dari kiri ke kanan.        Jalankan reasoner     Ulang



  ASSERTED FACTS                            INFERRED FACTS                            CLOSURE                                   REASONER

  Fakta yang ditulis eksplisit di           Fakta yang tidak ditulis, tetapi          Fakta awal ditambah seluruh fakta         Mesin yang menerapkan aturan
  dataset.                                  diturunkan reasoner dari fakta dan        yang bisa diturunkan.                     semantik pada dataset dan
                                            aturan.                                                                             ontologi untuk menghasilkan
   :KaryaSeni rdfs:subClassOf :Objek                                                  Closure = Asserted +
   .                                                                                                                            kesimpulan, dan pada kondisi
   :Lukisan rdfs:subClassOf
                                             :MonaLisa rdf:type :KaryaSeni .          Inferred                                  tertentu memeriksa konsistensi
                                             :Lukisan rdfs:subClassOf :Objek .

                                                                                      3+3=6
   :KaryaSeni .
   :MonaLisa rdf:type :Lukisan .
                                             :MonaLisa rdf:type :Objek .                                                        ontologi.
                                                                                                                                Selesai dalam 2 putaran, memakai
                                                                                                                                aturan subClassOf.




  Artinya: triple di kartu kedua tidak ditulis siapa pun, tetapi sama sahihnya dengan yang ditulis selama fakta dan aturannya benar. Bila kesimpulannya aneh,
  periksa fakta dan aturannya.




WEB SEMANTIK · TIF2108 · PERTEMUAN 12
```

---

## Halaman 7

```text
ALUR KONSEPTUAL


Dari Fakta sampai Jawaban
Tekan Lanjut (→) untuk menelusuri contoh Mona Lisa melewati setiap tahap.


 1                         2                      3                        4                        5                         6
 Fakta RDF                 Ontologi dan           Reasoner                 Fakta hasil              Closure                   Query
                           aturan                                          inferensi
 asserted                                         menerapkan aturan                                 asserted + inferred       memanfaatkan
                           makna kelas dan                                 inferred                                           pengetahuan

                      →                      →                         →                        →                         →
 :MonaLisa rdf:type                               aturan subClassOf,                                3 + 3 = 6 triple
 :Lukisan .                properti               2 putaran                :MonaLisa rdf:type                                 ASK { :MonaLisa
                           :KaryaSeni                                      :KaryaSeni .                                       rdf:type :Objek }
                           rdfs:subClassOf                                 :Lukisan                                           → true
                           :Objek .                                        rdfs:subClassOf
                           :Lukisan                                        :Objek .
                           rdfs:subClassOf                                 :MonaLisa rdf:type
                           :KaryaSeni .                                    :Objek .




  Ingat urutannya: reasoner tidak mengubah fakta yang ditulis. Ia menambahkan fakta turunan, lalu query bekerja pada closure.




WEB SEMANTIK · TIF2108 · PERTEMUAN 12
```

---

## Halaman 8

```text
CARA KERJA · FORWARD CHAINING


Dari Fakta ke Fakta, sampai Fixpoint
Coba: tekan tombol Putaran berulang kali sampai mesin
berhenti. Garis putus-putus kuning di graf adalah triple
turunan.                                                                                                            Lukisan                  subClassOf                Objek




  DATA ASSERTED
                                                                                                         rdf:type               subClassOf                subClassOf

  :MonaLisa          rdf:type                    :Lukisan .                                                         rdf:type

  :Lukisan           rdfs:subClassOf :KaryaSeni .
  :KaryaSeni rdfs:subClassOf :Objek .                                                         MonaLisa               rdf:type                 KaryaSeni




  Alurnya: (1) ambil fakta yang sudah ada · (2) cari aturan
  yang bisa diterapkan · (3) hasilkan fakta baru · (4) pakai               Putaran        Triple baru                                                                    Aturan (klik)
  fakta baru untuk memicu aturan lain · (5) ulangi sampai
                                                                           1              MonaLisa rdf:type KaryaSeni                                                    rdfs9
  tidak ada yang baru. Keadaan terakhir itu disebut fixpoint.
                                                                           1              Lukisan subClassOf Objek                                                       rdfs11

  Selesai            Ulang
                                                                           2              MonaLisa rdf:type Objek                                                        rdfs9



 3                           3                         6                   3              tidak ada yang baru: titik tetap, berhenti

 asserted · triple           inferred · triple         closure · triple
                                                                          Artinya: putaran 1 hanya memakai 3 fakta yang ditulis. Putaran 2 memakai fakta baru dari
                                                                          putaran 1 (langkah 4) sehingga lahir MonaLisa rdf:type Objek. Putaran 3 tidak menghasilkan
                                                                          apa pun: fixpoint, 6 triple.
WEB SEMANTIK · TIF2108 · PERTEMUAN 12
```

---

## Halaman 9

```text
CARA KERJA · DUA PENDEKATAN


Disimpan Dulu, atau Dihitung Saat Ditanya?
 PENDEKATAN                                KAPAN PENALARAN DILAKUKAN?                         GAMBARAN

 Forward chaining                          Sebelum atau selama materialisasi data             Fakta baru dihitung dan dapat disimpan

 Query-time / backward chaining            Ketika query dijalankan                            Sistem menelusuri aturan untuk menjawab pertanyaan


Coba: tambahkan lukisan baru, bandingkan kedua jawaban, lalu hitung                  1 · Tambah :StarryNight rdf:type           2 · Hitung ulang
                                                                                                                                                          Ulang
ulang.                                                                                           :Lukisan                            closure



                                                                                    Query-time (ditelusuri saat query)
  Forward chaining (disimpan)
    SPARQL                                                  1
                                                            objek ditemukan
                                                                                     SPARQL
                                                                                                                                              1
                                                                                                                                              objek ditemukan
                                                                                     SELECT ?x WHERE {
    SELECT ?x WHERE { ?x rdf:type :Objek }                  6 triple tersimpan                                                                3 triple tersimpan
                                                                                        ?x rdf:type/rdfs:subClassOf* :Objek }




  Artinya: forward chaining masih menjawab 1: closure dihitung sebelum Starry Night masuk. Query-time langsung menjawab 1 karena menelusuri subClassOf
  saat ditanya. Tekan 2.




WEB SEMANTIK · TIF2108 · PERTEMUAN 12
```

---

## Halaman 10

```text
02
Aturan Inferensi RDFS
domain · range · subPropertyOf · subClassOf · transitivitas subClassOf
· pertanyaan singkat




                                                                         Foto: Benjamin R. · Unsplash




WEB SEMANTIK · TIF2108 · PERTEMUAN 12
```

---

## Halaman 11

```text
ATURAN RDFS · RDFS:DOMAIN


Domain Memberi Tipe pada Subjek
Domain menyatakan kelas subjek yang menggunakan suatu properti.
                                                                  DISIMPULKAN REASONER RDFS                                             1 triple baru
  DATA · DITULIS (ASSERTED)
                                                                  rdfs2           :MonaLisa rdf:type :Lukisan .

  :dilukisOleh rdfs:domain :Lukisan .                             Closure = 2 ditulis + 1 disimpulkan = 3 triple. Klik nama aturan untuk melihat artinya.

  :MonaLisa     :dilukisOleh :Leonardo .
                                                                  Artinya: Mona Lisa memakai properti dilukisOleh, dan domain
Coba: tebak dulu kesimpulannya, lalu jalankan reasoner.           properti itu adalah Lukisan. Maka Mona Lisa disimpulkan sebagai
                                                                  anggota kelas Lukisan.
 Jalankan reasoner




WEB SEMANTIK · TIF2108 · PERTEMUAN 12
```

---

## Halaman 12

```text
ATURAN RDFS · RDFS:RANGE


Range Memberi Tipe pada Objek
Range menyatakan kelas objek dari suatu properti.
                                                          DISIMPULKAN REASONER RDFS                                             1 triple baru
  DATA · DITULIS (ASSERTED)
                                                          rdfs3           :Leonardo rdf:type :Seniman .

  :dilukisOleh rdfs:range :Seniman .                      Closure = 2 ditulis + 1 disimpulkan = 3 triple. Klik nama aturan untuk melihat artinya.

  :MonaLisa     :dilukisOleh :Leonardo .
                                                          Artinya: Leonardo menjadi nilai (objek) properti dilukisOleh, dan
Coba: tebak dulu kesimpulannya, lalu jalankan reasoner.   range properti itu adalah Seniman. Maka Leonardo disimpulkan
                                                          sebagai anggota kelas Seniman.
 Jalankan reasoner




WEB SEMANTIK · TIF2108 · PERTEMUAN 12
```

---

## Halaman 13

```text
ATURAN RDFS · RDFS:SUBPROPERTYOF


Subproperti Naik ke Induknya
Bila sebuah properti adalah subproperti dari properti lain, setiap
                                                                     DISIMPULKAN REASONER RDFS                                             1 triple baru
penggunaannya juga berlaku sebagai penggunaan properti induk.
                                                                     rdfs7           :MonaLisa :memilikiPencipta :Leonardo .
  DATA · DITULIS (ASSERTED)
                                                                     Closure = 2 ditulis + 1 disimpulkan = 3 triple. Klik nama aturan untuk melihat artinya.

  :dibuatOleh rdfs:subPropertyOf :memilikiPencipta .
  :MonaLisa    :dibuatOleh :Leonardo .                               Artinya: Mona Lisa dibuat oleh Leonardo, dan dibuatOleh adalah
                                                                     bentuk khusus dari memilikiPencipta. Maka Mona Lisa juga memiliki
Coba: tebak dulu kesimpulannya, lalu jalankan reasoner.              pencipta Leonardo. Arah sebaliknya tidak berlaku: memilikiPencipta
                                                                     tidak otomatis berarti dibuatOleh.
 Jalankan reasoner




WEB SEMANTIK · TIF2108 · PERTEMUAN 12
```

---

## Halaman 14

```text
ATURAN RDFS · RDFS:SUBCLASSOF


Anggota Subkelas Mewarisi Superkelas
Bila suatu kelas adalah subclass dari kelas lain, anggota subclass juga
                                                                          DISIMPULKAN REASONER RDFS                                             1 triple baru
anggota superclass.
                                                                          rdfs9           :MonaLisa rdf:type :KaryaSeni .
  DATA · DITULIS (ASSERTED)
                                                                          Closure = 2 ditulis + 1 disimpulkan = 3 triple. Klik nama aturan untuk melihat artinya.

  :Lukisan    rdfs:subClassOf :KaryaSeni .
  :MonaLisa rdf:type :Lukisan .                                           Artinya: Mona Lisa anggota Lukisan, dan setiap Lukisan adalah
                                                                          KaryaSeni. Maka Mona Lisa juga KaryaSeni. Tipe awal Lukisan tetap
Coba: tebak dulu kesimpulannya, lalu jalankan reasoner.                   ada; reasoner hanya menambah.

 Jalankan reasoner




WEB SEMANTIK · TIF2108 · PERTEMUAN 12
```

---

## Halaman 15

```text
ATURAN RDFS · TRANSITIVITAS


Hubungan Subkelas Berantai
Hubungan subclass bisa ditelusuri berantai: subkelas dari subkelas tetap
                                                                               DISIMPULKAN REASONER RDFS                                             1 triple baru
subkelas.
                                                                               rdfs11          :Lukisan rdfs:subClassOf :Objek .
 DATA · DITULIS (ASSERTED)
                                                                               Closure = 2 ditulis + 1 disimpulkan = 3 triple. Klik nama aturan untuk melihat artinya.

  :Lukisan    rdfs:subClassOf :KaryaSeni .
  :KaryaSeni rdfs:subClassOf :Objek .                                          Artinya: Lukisan ⊑ KaryaSeni dan KaryaSeni ⊑ Objek memberi
                                                                               Lukisan ⊑ Objek. Sekarang tambahkan Mona Lisa dengan tombol
Coba: jalankan reasoner, lalu tekan tombol kedua untuk menambahkan Mona Lisa   kedua.
dan lihat apa yang ikut berubah.

 Jalankan reasoner    + :MonaLisa rdf:type :Lukisan




WEB SEMANTIK · TIF2108 · PERTEMUAN 12
```

---

## Halaman 16

```text
PERTANYAAN SINGKAT UNTUK KELAS


Apa Saja Tipe Oyen?
  DATA · DITULIS (ASSERTED)
                                                                    Tepat.
                                                                    Hijau putus-putus: tipe yang belum Anda centang. Kuning: tidak bisa
  :Kucing   rdfs:subClassOf :Mamalia .
                                                                    disimpulkan.
  :Mamalia rdfs:subClassOf :Hewan .
  :Oyen     rdf:type :Kucing .
                                                                    DISIMPULKAN REASONER

Coba: centang semua tipe yang menurut Anda dimiliki :Oyen setelah   rdfs11       :Kucing rdfs:subClassOf :Hewan .

reasoning, lalu periksa.                                            rdfs9        :Oyen rdf:type :Mamalia .

                                                                    rdfs9        :Oyen rdf:type :Hewan .
     :Oyen rdf:type :Kucing

     :Oyen rdf:type :Mamalia
                                                                    Artinya: jawaban yang diharapkan: :Mamalia dan :Hewan, selain tipe awal
                                                                    :Kucing. Tumbuhan tidak pernah disebut. Yang menjadi subkelas Hewan adalah
     :Oyen rdf:type :Hewan
                                                                    kelas :Kucing, bukan individu :Oyen.
     :Oyen rdf:type :Tumbuhan

     :Oyen rdfs:subClassOf :Hewan


  Periksa dengan reasoner       Ulang




WEB SEMANTIK · TIF2108 · PERTEMUAN 12
```

---

## Halaman 17

```text
03
OWL: Inferensi yang
Lebih Ekspresif
TransitiveProperty · SymmetricProperty · inverseOf · sameAs ·
disjointWith · konsistensi · open world · profil OWL 2


                                                                Foto: Alice Yamamura · Unsplash




WEB SEMANTIK · TIF2108 · PERTEMUAN 12
```

---

## Halaman 18

```text
OWL · OWL:TRANSITIVEPROPERTY


Properti Transitif: Rantai yang Menyambung
Bila A berhubungan dengan B, dan B dengan C, melalui properti transitif,
                                                                                 DISIMPULKAN REASONER OWL RL                                           3 triple baru
maka A berhubungan dengan C. Contoh konseptual: leluhurDari.
                                                                                 prp-trp         :Ali :leluhurDari :Citra .
  DATA · DITULIS (ASSERTED)
                                                                                 prp-trp         :Budi :leluhurDari :Dewi .

  :leluhurDari a owl:TransitiveProperty .                                        prp-trp         :Ali :leluhurDari :Dewi .
  :Ali   :leluhurDari :Budi .
                                                                                 Closure = 4 ditulis + 3 disimpulkan = 7 triple. Klik nama aturan untuk melihat artinya.
  :Budi :leluhurDari :Citra .
  :Citra :leluhurDari :Dewi .
                                                                                 Artinya: OWL RL menyambung rantai: Ali leluhur Citra, Budi leluhur
                                                                                 Dewi, lalu Ali leluhur Dewi. Leluhur Dewi kini Citra, Budi, dan Ali. Dari 3
Coba: jalankan reasoner RDFS dulu, lalu OWL RL. Hitung berapa hubungan leluhur
                                                                                 hubungan yang ditulis menjadi 6.
yang muncul.

 Reasoner RDFS      Reasoner OWL RL




WEB SEMANTIK · TIF2108 · PERTEMUAN 12
```

---

## Halaman 19

```text
OWL · OWL:SYMMETRICPROPERTY


Properti Simetris: Berlaku Dua Arah
Bila A berhubungan dengan B, maka B juga berhubungan dengan A. Contoh
                                                                        DISIMPULKAN REASONER OWL RL                                           1 triple baru
konseptual: bertemanDengan, bila memang dimodelkan simetris.
                                                                        prp-symp        :Sari :bertemanDengan :Andi .
  DATA · DITULIS (ASSERTED)
                                                                        Closure = 2 ditulis + 1 disimpulkan = 3 triple. Klik nama aturan untuk melihat artinya.

  :bertemanDengan a owl:SymmetricProperty .
  :Andi :bertemanDengan :Sari .                                         Artinya: OWL RL menambahkan arah sebaliknya: Sari berteman
                                                                        dengan Andi. Pemodel yang memutuskan apakah sebuah relasi
Coba: tebak dulu kesimpulannya, lalu jalankan reasoner.                 memang simetris; “mengikuti” di media sosial, misalnya, tidak
                                                                        simetris.
 Reasoner RDFS      Reasoner OWL RL




WEB SEMANTIK · TIF2108 · PERTEMUAN 12
```

---

## Halaman 20

```text
OWL · OWL:INVERSEOF


Dua Properti yang Saling Kebalikan
Dua properti dapat dinyatakan sebagai kebalikan satu sama lain. Bila A
                                                                         DISIMPULKAN REASONER OWL RL                                           1 triple baru
memilikiIbu B, maka B ibuDari A.
                                                                         prp-inv1        :Rina :ibuDari :Andi .
  DATA · DITULIS (ASSERTED)
                                                                         Closure = 2 ditulis + 1 disimpulkan = 3 triple. Klik nama aturan untuk melihat artinya.

  :memilikiIbu owl:inverseOf :ibuDari .
  :Andi :memilikiIbu :Rina .                                             Artinya: OWL RL membalik triple: Rina ibuDari Andi. Data cukup
                                                                         ditulis dari satu arah, dan query dari arah mana pun tetap terjawab.
Coba: tebak dulu kesimpulannya, lalu jalankan reasoner.

 Reasoner RDFS      Reasoner OWL RL




WEB SEMANTIK · TIF2108 · PERTEMUAN 12
```

---

## Halaman 21

```text
OWL · OWL:SAMEAS


Dua URI, Satu Individu
owl:sameAs menyatakan bahwa dua URI merujuk pada individu yang sama.
                                                                       DISIMPULKAN REASONER OWL RL                                           3 triple baru
Sifat dan hubungan keduanya lalu saling berlaku.
                                                                       eq-rep-s        :LeonardoDaVinci :lahirDi :Vinci .
  DATA · DITULIS (ASSERTED)
                                                                       eq-sym          :LeonardoDaVinci owl:sameAs :Leonardo .

  :Leonardo owl:sameAs :LeonardoDaVinci .                              eq-rep-s        :Leonardo :melukis :MonaLisa .
  :Leonardo           :lahirDi :Vinci .
                                                                       Closure = 3 ditulis + 3 disimpulkan = 6 triple. Klik nama aturan untuk melihat artinya.
  :LeonardoDaVinci :melukis :MonaLisa .

                                                                       Artinya: OWL RL menyalin fakta ke kedua nama: :Leonardo kini
Coba: tebak dulu kesimpulannya, lalu jalankan reasoner.
                                                                       melukis Mona Lisa, :LeonardoDaVinci lahir di Vinci. Karena itu sameAs
 Reasoner RDFS      Reasoner OWL RL
                                                                       harus hati-hati: satu sameAs yang salah menyalin semua fakta ke
                                                                       individu lain, tanpa pesan error.




WEB SEMANTIK · TIF2108 · PERTEMUAN 12
```

---

## Halaman 22

```text
OWL · OWL:DISJOINTWITH


Dua Kelas yang Tidak Boleh Berbagi Anggota
owl:disjointWith menyatakan bahwa dua kelas tidak boleh memiliki
                                                                              DISIMPULKAN REASONER OWL RL                                           1 triple baru
anggota yang sama. Di bawah ini ada satu salah ketik: Sari tinggal di Andi.
                                                                              rdfs3           :Andi rdf:type :Lokasi .
  DATA · DITULIS (ASSERTED)
                                                                                Tidak konsisten: :Manusia dan :Lokasi disjoint, tetapi
  :Manusia owl:disjointWith :Lokasi .                                           :Andi anggota keduanya
  :tinggalDi rdfs:range :Lokasi .
  :Andi a :Manusia .                                                          Closure = 4 ditulis + 1 disimpulkan = 5 triple. Klik nama aturan untuk melihat artinya.

  :Sari :tinggalDi :Andi .          # salah ketik
                                                                              Artinya: Andi kini Manusia sekaligus Lokasi, padahal kedua kelas
Coba: tebak dulu kesimpulannya, lalu jalankan reasoner.                       disjoint. OWL RL menandai data tidak konsisten. Pesan ini menunjuk
                                                                              letak kesalahan; memperbaikinya tetap tugas pemodel.
 Reasoner RDFS      Reasoner OWL RL




WEB SEMANTIK · TIF2108 · PERTEMUAN 12
```

---

## Halaman 23

```text
KONSISTENSI ONTOLOGI · MUSEUM.TTL


Reasoner Menemukan Pemodelan yang Keliru
Reasoning juga membantu menemukan pemodelan yang bermasalah. Contoh
                                                                          REASONER OWL RL                                     1 pesan galat
dari museum.ttl dengan satu baris salah ketik:
                                                                          ex:MuseumReinaSofia rdf:type
 BARIS MUSEUM.TTL + GUERNICA_SALAH.TTL YANG BERPERAN
                                                                          ex:Museum · ex:Orang · ex:Pelukis · ex:Seniman ·

  ex:dilukisOleh rdfs:range ex:Pelukis .
                                                                          ex:Tempat
  ex:Pelukis rdfs:subClassOf ex:Seniman .
                                                                           Tidak konsisten: ex:Orang dan ex:Tempat disjoint,
  ex:Seniman rdfs:subClassOf ex:Orang .
                                                                           tetapi ex:MuseumReinaSofia anggota keduanya
  ex:Museum    rdfs:subClassOf ex:Tempat .
  ex:Orang     owl:disjointWith ex:Tempat .
                                                                          Artinya: museum itu kini Orang sekaligus Tempat, padahal Orang dan
  # salah ketik: maksudnya ex:lokasiDi                                    Tempat disjoint. OWL RL menandai data tidak konsisten, sehingga
  ex:Guernica ex:dilukisOleh ex:MuseumReinaSofia .                        salah ketiknya akhirnya terlihat.
  ex:MuseumReinaSofia a ex:Museum .

                                                                          Hal penting: kesalahan sering berasal dari pemilihan
 1 · Reasoner RDFS      2 · Reasoner OWL RL      3 · Perbaiki: lokasiDi
                                                                          domain, range, kelas, atau properti yang tidak tepat. Periksa
                                                                          makna relasi sebelum menambahkan aturan.
 Lihat museum.ttl + guernica_salah.ttl lengkap




WEB SEMANTIK · TIF2108 · PERTEMUAN 12
```

---

## Halaman 24

```text
OPEN WORLD ASSUMPTION


Tidak Tercatat Bukan Berarti Salah

                                                                         false
Dalam Web Semantik, ketiadaan suatu fakta tidak otomatis berarti fakta
itu salah. Bisa jadi informasinya belum tersedia.

  DATA · DITULIS (ASSERTED)


  :Andi :tinggalDi :Medan .                                              Artinya: false di sini berarti “tidak tercatat”, bukan “Budi tidak tinggal
  :Budi rdf:type      :Mahasiswa .                                       di Medan”. Kita tidak boleh menyimpulkan Budi tinggal di tempat lain.
                                                                         Reasoner pun tidak menurunkan fakta negatif dari ketiadaan data.

Coba: tanyakan untuk Andi, lalu untuk Budi.

 ASK { :Andi :tinggalDi :Medan }   ASK { :Budi :tinggalDi :Medan }




WEB SEMANTIK · TIF2108 · PERTEMUAN 12
```

---

## Halaman 25

```text
OWL 2 PROFILES


Pilih Sesuai Kebutuhan, Bukan yang Terkuat
 PROFIL      GAMBARAN UMUM


 OWL 2       Mendukung penalaran berbasis aturan dan cocok untuk pendekatan rule-based. Inilah yang dijalankan owlrl dan reasoner di halaman
 RL          ini.

 OWL 2
             Dirancang untuk ontologi besar dengan kebutuhan klasifikasi yang efisien.
 EL

 OWL 2
             Ditujukan untuk query terhadap data dalam jumlah besar, terutama dengan pemetaan ke basis data relasional.
 QL

 OWL 2       Ekspresivitas lebih luas dengan batasan formal agar penalaran tetap terdefinisi. Secara teknis DL adalah bahasa lengkapnya; RL, EL, dan
 DL          QL adalah profil, yaitu potongan DL. Dipakai HermiT dan Pellet.



  Pilih profil sesuai kebutuhan aplikasi, ukuran data, ekspresivitas ontologi, dan kemampuan reasoner. Makin ekspresif, makin mahal
  penalarannya.




WEB SEMANTIK · TIF2108 · PERTEMUAN 12
```

---

## Halaman 26

```text
04
Praktik: Python,
Protégé, dan
Konsistensi
RDFLib dan OWL-RL · Rina terhitung · RDFS lawan OWL RL · HermiT ·
pesan galat

                                                                    Foto: Safar Safarov · Unsplash




WEB SEMANTIK · TIF2108 · PERTEMUAN 12
```

---

## Halaman 27

```text
PRAKTIK · RDFLIB DAN OWL-RL


Menjalankan Inferensi RDFS di Python
 8.1 · INSTALASI                                             Coba: klik langkah untuk menyorot barisnya di kode.
                                                              1   Graph() membuat graph RDF.
  pip install rdflib owlrl
                                                              2   Namespace memudahkan penulisan URI.

 8.2 · CONTOH_RDFS.PY                                         3   g.add() menambahkan fakta dan aturan.

                                                                  DeductiveClosure(RDFS_Semantics).expand(g)
  from rdflib import Graph, Namespace, RDF, RDFS              4
                                                                  menjalankan inferensi RDFS dan menambahkan hasilnya ke graph.
  from owlrl import DeductiveClosure, RDFS_Semantics
                                                                  Perulangan g.triples menampilkan tipe Mona Lisa setelah
  g = Graph()                                                 5
                                                                  inferensi.
  EX = Namespace("http://example.org/")

                                                             KELUARAN SAAT DIJALANKAN (RDFLIB + OWLRL 7.6.2)
  g.bind("ex", EX)

                                                              Jumlah triple awal: 3
  g.add((EX.Lukisan, RDFS.subClassOf, EX.KaryaSeni))
                                                              Jumlah triple setelah inferensi: 16
  g.add((EX.KaryaSeni, RDFS.subClassOf, EX.Objek))
                                                              ex:MonaLisa rdf:type ex:Lukisan
  g.add((EX.MonaLisa, RDF.type, EX.Lukisan))
                                                              ex:MonaLisa rdf:type rdfs:Resource
                                                              ex:MonaLisa rdf:type ex:KaryaSeni
  print("Jumlah triple awal:", len(g))
                                                              ex:MonaLisa rdf:type ex:Objek

  DeductiveClosure(RDFS_Semantics).expand(g)

  print("Jumlah triple setelah inferensi:", len(g))            Artinya: 3 triple menjadi 16, tetapi yang bermakna hanya
                                                               3: MonaLisa sebagai KaryaSeni dan Objek, serta Lukisan ⊑
  for s, p, o in g.triples((EX.MonaLisa, RDF.type, None)):
      print(s, p, o)                                           Objek. Sisanya trivial, seperti rdfs:Resource. Urutan
                                                               baris bisa berbeda.
 Salin kode          Unduh contoh_rdfs.py



WEB SEMANTIK · TIF2108 · PERTEMUAN 12
```

---

## Halaman 28

```text
PRAKTIK · PENAMBAHAN INDIVIDU BARU · KAMPUS.TTL


Rina Baru Terhitung Setelah Inferensi Diulang
                                                                                 KELUARAN SAAT DIJALANKAN (OWLRL 7.6.2)
 PYTHON · DEMO_A.PY

                                                                                   9 32 23
  # Demo A Pertemuan 12 — reasoner RDFS menjawab kejanggalan Rina (kampus.ttl)
                                                                                   Orang: 3
  from rdflib import Graph
                                                                                   Ada Rina: 4
  from owlrl import DeductiveClosure, RDFS_Semantics
  Q_ORANG = """PREFIX foaf: <http://xmlns.com/foaf/0.1/>
  SELECT ?x WHERE { ?x a foaf:Person }"""                                        Baris pertama: 9 triple ditulis, closure 32, jadi 23 triple disimpulkan.
  RINA = "@prefix ex: <http://contoh.id/kampus/> . ex:rina a ex:DosenTetap ."
                                                                                 Coba: ulangi kejadiannya di sini. Tambahkan Rina sebagai
  def tutup(asserted):
     closure = Graph() + asserted            # salinan, asserted utuh            DosenTetap, lalu jalankan ulang inferensi.
     DeductiveClosure(RDFS_Semantics).expand(closure)
      return closure, closure - asserted       # inferred = selisihnya             1 · Tambah Rina         2 · Jalankan ulang inferensi         Ulang
  asserted = Graph().parse("kampus.ttl")


                                                                                   3
  closure, inferred = tutup(asserted)
  print(len(asserted), len(closure), len(inferred))                                      individu foaf:Person terdeteksi
  print("Orang:", len(closure.query(Q_ORANG)))
  asserted.parse(data=RINA, format="turtle")
  print("Ada Rina:", len(tutup(asserted)[0].query(Q_ORANG)))                       Artinya: Rina sudah masuk sebagai DosenTetap, tetapi
                                                                                   tetap 3. Closure lama tidak memperbarui dirinya sendiri.
 Salin kode     Unduh demo_a.py         Lihat kampus.ttl lengkap




WEB SEMANTIK · TIF2108 · PERTEMUAN 12
```

---

## Halaman 29

```text
PRAKTIK · MUSEUM.TTL


Membandingkan Hasil RDFS dan OWL RL
 Ukuran                          Asserted                 RDFS        OWL RL   Coba: klik nama query di tabel untuk melihat baris jawabannya di tiap
                                                                               tahap.
 Jumlah triple                   40                       109         271
                                                                                 SPARQL · QUERY LOKASI

 Query                       Asserted                 RDFS            OWL RL
                                                                                 SELECT ?t WHERE { ex:MonaLisa ex:lokasiDi ?t }

   lokasi                    1                        1               3
                                                                                ASSERTED · 1              RDFS · 1                  OWL RL · 3
                                                                                ex:Louvre                 ex:Louvre                 ex:Prancis
   melukis                   0                        0               2
                                                                                                                                    ex:Paris
                                                                                                                                    ex:Louvre
   orang                     0                        2               3
                                                                                 Artinya: RDFS tidak mengenal TransitiveProperty, jadi Mona Lisa hanya di
Angka dari demo_b.py dengan owlrl 7.6.2.   Lihat museum.ttl lengkap              Louvre. OWL RL menyambung rantai Louvre → Paris → Prancis.




   Pesan pembelajaran: makin banyak aturan semantik yang diterapkan, makin banyak kesimpulan yang mungkin. Jumlah triple yang lebih
   besar tidak otomatis berarti model lebih baik; kualitas hasil bergantung pada ketepatan data, ontologi, dan aturan.



WEB SEMANTIK · TIF2108 · PERTEMUAN 12
```

---

## Halaman 30

```text
PRAKTIK · PROTÉGÉ 5.6 + HERMIT


Melihat Hasil Inferensi di Protégé
Dilakukan dosen di Protégé; bagian ini tidak bisa dijalankan di halaman web.


1      Buka Protégé, lalu File › Open › museum.ttl.                                               PERTANYAAN UNTUK ANDA

                                                                                                  Fakta mana yang berasal
2      Periksa kelas, individu, dan properti di tab Entities: baru yang ditulis.                  dari data awal, dan fakta
                                                                                                  mana yang baru diketahui
3      Reasoner › HermiT › Start reasoner.                                                        setelah reasoner dijalankan?

4      Individuals › MonaLisa: tipe berlatar kuning adalah hasil inferensi. Klik tanda tanya di
       sampingnya untuk melihat aksioma yang menurunkannya.


5      Bandingkan yang ditulis dengan yang disimpulkan. Untuk menyimpan: File › Export
       inferred axioms as ontology… (berkas asli tidak berubah).




WEB SEMANTIK · TIF2108 · PERTEMUAN 12
```

---

## Halaman 31

```text
PRAKTIK · MUSEUM.TTL + GUERNICA_SALAH.TTL


Membaca Pesan Inkonsistensi
 PYTHON · DEMO_D.PY                                                                      Pengujian              Jumlah triple                  Error

  # Demo D Pertemuan 12 — satu baris salah ketik: RDFS diam, OWL RL bersuara             RDFS                   121                            0
  from rdflib import Graph, Namespace, RDF
  from owlrl import DeductiveClosure, RDFS_Semantics, OWLRL_Semantics                    OWL RL                 288                            1
  ERR = Namespace("http://www.daml.org/2002/03/agents/agent-ont#")
  asserted = Graph().parse("museum.ttl").parse("guernica_salah.ttl")                    KELUARAN SAAT DIJALANKAN (OWLRL 7.6.2)
  for nama, sem in [("RDFS", RDFS_Semantics), ("OWL RL", OWLRL_Semantics)]:
                                                                                         RDFS 121 triple | 0 pesan galat
      g = Graph() + asserted                                                             OWL RL 288 triple | 1 pesan galat
      DeductiveClosure(sem).expand(g)                                                       Disjoint classes http://contoh.id/museum/Orang and
      pesan = [str(e) for m in g.subjects(RDF.type, ERR.ErrorMessage)                    http://contoh.id/museum/Tempat have a common individual
                                                                                         http://contoh.id/museum/MuseumReinaSofia
               for e in g.objects(m, ERR.error)]
      print(nama, len(g), "triple |", len(pesan), "pesan galat")
      for p in pesan:                                                                     Artinya: pada owlrl, pesan kesalahan dimasukkan ke
          print("   ", p)
                                                                                          graph sebagai ErrorMessage, bukan dilempar
                                                                                          sebagai exception Python. Jangan hanya
 Salin kode     Unduh demo_d.py         Lihat museum.ttl + guernica_salah.ttl lengkap     mengandalkan try/except; periksa isi graph, seperti
                                                                                          yang dilakukan kode di kiri.




WEB SEMANTIK · TIF2108 · PERTEMUAN 12
```

---

## Halaman 32

```text
PRAKTIK BAIK MENGEMBANGKAN ONTOLOGI


Enam Kebiasaan Sebelum Menyimpan Hasil
Reasoning
Coba: centang yang sudah Anda lakukan pada proyek ontologi Anda sendiri.


    Pisahkan fakta yang ditulis (asserted) dari fakta hasil inferensi (inferred) bila aplikasi perlu melacak asal-usul informasi.

    Catat reasoner, versi pustaka, profil OWL, dan konfigurasi yang digunakan.

    Pastikan domain dan range sesuai dengan makna properti.

    Gunakan owl:sameAs dengan hati-hati: ia menyatakan identitas, bukan kemiripan.

    Uji konsistensi ontologi setelah mengubah kelas, properti, atau batasan.

    Evaluasi apakah inferensi perlu dimaterialisasi, atau cukup dilakukan saat query.




WEB SEMANTIK · TIF2108 · PERTEMUAN 12
```

---

## Halaman 33

```text
PERTANYAAN DISKUSI


Diskusikan Dulu, Baru Balik Kartunya
 DISKUSI 1                                       DISKUSI 2                                  DISKUSI 3                                 DISKUSI 4
 Mengapa sebuah aplikasi Web                     Apa perbedaan asserted facts dan           Mengapa domain dan range dapat            Apa perbedaan forward chaining dan
 Semantik membutuhkan inferensi?                 inferred facts?                            menghasilkan tipe baru?                   query-time reasoning?

 ARAH JAWABAN                                    ARAH JAWABAN                               ARAH JAWABAN                              ARAH JAWABAN
 Agar fakta yang tersirat tidak perlu ditulis    Asserted ditulis langsung; inferred        Karena keduanya adalah aturan             Forward chaining menghitung dan
 satu per satu, dan data dari sumber             diturunkan reasoner. Keduanya sama sahih   penyimpulan, bukan pemeriksaan.           menyimpan dulu; query-time menelusuri
 berbeda tetap bisa ditanyai lewat makna         bila fakta dan aturannya benar.            Pemakai properti otomatis mendapat        aturan saat ditanya. Lihat adegan Rina dan
 kelas dan propertinya.                                                                     kelasnya.                                 Starry Night.


 DISKUSI 5                                       DISKUSI 6                                  DISKUSI 7
 Mengapa penggunaan owl:sameAs                   Apa dampak kesalahan dalam                 Mengapa ketiadaan fakta tidak selalu
 harus hati-hati?                                menentukan domain dan range?               berarti fakta itu salah?

 ARAH JAWABAN                                    ARAH JAWABAN                               ARAH JAWABAN
 Satu sameAs menyalin semua fakta ke             Tipe yang salah menyebar diam-diam,        Open World Assumption: data mungkin
 individu lain, tanpa error. Satu tautan salah   seperti museum yang menjadi pelukis.       belum lengkap. “Tidak tercatat” berbeda
 mencemari banyak data.                          Hanya aksioma pembatas seperti             dengan “tidak benar”.
                                                 disjointWith yang membuatnya terlihat.




WEB SEMANTIK · TIF2108 · PERTEMUAN 12
```

---

## Halaman 34

```text
KUIS · UJI PEMAHAMAN


Jawab dalam Hati, Lalu Balik Kartunya
 SOAL 1                                    SOAL 2                                        SOAL 3                                 SOAL 4
 Apa yang dimaksud dengan asserted         Apa yang dimaksud dengan inferred             Jika :Kucing rdfs:subClassOf           Apa fungsi rdfs:domain?
 facts?                                    facts?                                        :Mamalia dan :Oyen rdf:type :Kucing,
                                                                                         apa kesimpulannya?                     JAWABAN
 JAWABAN                                   JAWABAN                                                                              Menentukan kelas yang dapat disimpulkan
 Fakta yang dinyatakan secara eksplisit    Fakta yang diturunkan dari fakta dan aturan   JAWABAN                                untuk subjek yang menggunakan properti
 dalam dataset.                            semantik.                                     :Oyen rdf:type :Mamalia.               tersebut.



 SOAL 5                                    SOAL 6                                        SOAL 7
 Apa fungsi rdfs:range?                    Apa makna owl:SymmetricProperty?              Apakah fakta yang tidak ada di
                                                                                         dataset otomatis salah?
 JAWABAN                                   JAWABAN
 Menentukan kelas yang dapat disimpulkan   Jika A berhubungan dengan B, maka B juga      JAWABAN
 untuk objek dari suatu properti.          berhubungan dengan A melalui properti         Tidak. Web Semantik umumnya memakai
                                           tersebut.                                     Open World Assumption.




WEB SEMANTIK · TIF2108 · PERTEMUAN 12
```

---

## Halaman 35

```text
DISKUSI KELOMPOK


Dua Kasus untuk Dikerjakan Bersama
Tulis jawaban kelompok Anda, lalu uji di Lab pada adegan berikutnya.


  Kasus A · Museum dan lukisan                                   Kasus B · Hubungan keluarga
  Sebuah dataset memuat museum, lukisan, dan seniman. Tentukan   Sebuah ontologi memodelkan memilikiIbu dan ibuDari.
  domain dan range yang tepat untuk dipamerkanDi, dilukisOleh,
                                                                    Tentukan apakah kedua properti merupakan inverse.
  dan memilikiKoleksi.
                                                                    Buat fakta awal.
      Tentukan domain dan range setiap properti.
                                                                    Turunkan fakta yang dapat disimpulkan.
      Buat beberapa triple RDF.
                                                                    Jelaskan perbedaan fakta awal dan hasil inferensi.
      Tuliskan fakta yang dapat diinferensikan.

      Identifikasi kemungkinan kesalahan pemodelan.




WEB SEMANTIK · TIF2108 · PERTEMUAN 12
```

---

## Halaman 36

```text
LAB BEBAS


Tulis Data, Pilih Reasoner, Lihat Kesimpulannya
 Mona Lisa       Oyen         leluhurDari          Kasus B          Kasus A (awal)   museum.ttl                                    tanpa reasoner   RDFS   OWL RL



  @prefix :       <http://contoh.id/kuliah/> .                                                     3 ditulis   3 disimpulkan   2 putaran
  @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
  @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
  @prefix owl:    <http://www.w3.org/2002/07/owl#> .                                               3 baris
  :MonaLisa   rdf:type               :Lukisan .
  :Lukisan    rdfs:subClassOf :KaryaSeni .                                                         #              ?c
  :KaryaSeni rdfs:subClassOf :Objek .
                                                                                                   1              :Objek

                                                                                                   2              :KaryaSeni

                                                                                                   3              :Lukisan


                                                                                                  TRIPLE YANG DISIMPULKAN

                                                                                                  rdfs11       :Lukisan rdfs:subClassOf :Objek .
  SELECT ?c WHERE { :MonaLisa rdf:type ?c }
                                                                                                  rdfs9        :MonaLisa rdf:type :KaryaSeni .

                                                                                                  rdfs9        :MonaLisa rdf:type :Objek .

  Jalankan       Ctrl/⌘ + Enter · prefix : rdf: rdfs: owl: ex: tersedia di query




WEB SEMANTIK · TIF2108 · PERTEMUAN 12
```

---

## Halaman 37

```text
RINGKASAN PENUTUP


Yang Anda Bawa dari Hari Ini
01       Inferensi adalah proses menghasilkan fakta baru berdasarkan fakta dan aturan semantik.

02       Asserted facts dinyatakan langsung; inferred facts adalah hasil penalaran. Closure mencakup keduanya.

03       RDFS mendukung inferensi melalui domain, range, subproperty, dan subclass.

04       OWL menambah properti transitif, simetris, inverse, sameAs, dan disjointWith.

05       Reasoner menghasilkan pengetahuan baru dan membantu memeriksa konsistensi.

06       Pemodelan yang tepat sangat penting agar hasil inferensi bermakna.


  Pesan utama: Web Semantik bukan hanya tentang menyimpan data yang saling terhubung, tetapi juga tentang menyatakan makna
  hubungan itu agar mesin dapat menarik kesimpulan yang dapat dipertanggungjawabkan.




WEB SEMANTIK · TIF2108 · PERTEMUAN 12
```

---

## Halaman 38

```text
TINDAK LANJUT


Sebelum Pertemuan 13
  PERTEMUAN 13
                                                                    Pekerjaan rumah
  Knowledge Graph, LLM, dan RAG                                       Jalankan contoh §8.2 dan demo_a.py, demo_b.py, demo_d.py di
  Closure museum.ttl berisi 271 triple, padahal “Mona Lisa ada di     laptop Anda; kode dan data ada di LMS.
  negara mana?” hanya butuh satu. Pertemuan 13: memilih subgraf       Selesaikan Kasus A atau B, lalu uji hasilnya dengan reasoner.
  yang relevan untuk diberikan kepada model bahasa.
                                                                      Kerjakan Latihan Pertemuan 12 di repo pertemuan-12.

                                                                      Baca RDF 1.1 Semantics §9.2.1 dan OWL 2 Profiles §4.3.




WEB SEMANTIK · TIF2108 · PERTEMUAN 12
```

---

## Halaman 39

```text
REFERENSI


Bacaan Wajib dan Pendukung
BUKU DAN TUTORIAL                                                              SPESIFIKASI DAN DOKUMENTASI

Antoniou, G., Groth, P., van Harmelen, F., & Hoekstra, R. (2012). A Semantic   W3C (2014). RDF 1.1 Semantics, §9.2.1. w3.org/TR/rdf11-mt
Web Primer (3rd ed.). MIT Press.
                                                                               W3C (2014). RDF Schema 1.1. w3.org/TR/rdf-schema
Allemang, D., Hendler, J., & Gandon, F. (2020). Semantic Web for the Working
                                                                               W3C (2012). OWL 2 Web Ontology Language Primer (2nd ed.).
Ontologist (3rd ed.). ACM Books.
                                                                               w3.org/TR/owl2-primer
Hitzler, P., Krötzsch, M., & Rudolph, S. Foundations of Semantic Web
                                                                               W3C (2012). OWL 2 Profiles (2nd ed.), §4.3. w3.org/TR/owl2-profiles
Technologies. Chapman & Hall/CRC.
                                                                               RDFLib. OWL-RL. github.com/RDFLib/OWL-RL
Horridge, M. (2011). A Practical Guide to Building OWL Ontologies Using
Protégé 4 and CO-ODE Tools, Edition 1.3. University of Manchester.




WEB SEMANTIK · TIF2108 · PERTEMUAN 12
```

---

## Halaman 40

```text
PENUTUP · TANYA-JAWAB




Mesin tahu Mona Lisa ada di
Prancis. Bisakah ia menjawab orang
yang bertanya dalam bahasa sehari-
hari?
Pertanyaan ini menjadi pembuka Pertemuan 13: knowledge graph, LLM, dan RAG.

 Asserted dan inferred   Aturan menentukan kesimpulan   Sampai jumpa di Pertemuan 13




WEB SEMANTIK · TIF2108 · PERTEMUAN 12
```
