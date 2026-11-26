# PWS — RDF & XML

**PWS**  
**TI034**  
**PANJI DEPARI**  
**KOM A 25**  
**P2**  
**RDF & XML**

---

## Halaman 2 — TOPICS OF DISCUSSION

01. WEB SEMANTIK  
02. RDF  
03. XML  
04. OWL  
05. PROTEGE  
06. JENA FUSEKI  
07. SPARQL  
08. SPARQL FUNCTION

---

## Halaman 3 — PREVIOUS MEETING

```html
<p> Jakarta adalah ibu kota Indonesia. <p>
```

### INTERPRETASI MANUSIA

1. Jakarta - ibu kota - Indonesia
2. Indonesia - mempunyai ibu kota - Jakarta

### INTERPRETASI KOMPUTER

??? Entah, itu cuma string

---

## Halaman 4 — SOLUTION?

**WEB SEMANTIK**

---

## Halaman 5 — QUESTION

Bagaimana menuliskan

```html
<p>Jakarta adalah ibukota Indonesia<p>
```

Agar dapat dipahami komputer?

**ITLG USU | 2026**

---

## Halaman 6 — TRIPLE

Jakarta adalah ibu kota Indonesia

Jakarta - adalah ibu kota - Indonesia

| Subjek | Predikat | Objek |
|---|---|---|

**ITLG USU | 2026**

---

## Halaman 7 — QUESTION

Bagaimana jika lebih dari 1 kalimat?

**ITLG USU | 2026**

---

## Halaman 8 — KNOWLEDGE GRAPH

**Relasi pada graph:**

- Jakarta — *adalah ibu kota* → Indonesia
- Indonesia — *adalah bagian dari* → Asia
- Malaysia — *adalah bagian dari* → Asia

**Keterangan:**

1. Jakarta adalah ibu kota Indonesia.
2. Indonesia adalah bagian dari Asia.
3. Malaysia adalah bagian dari Asia.

**ITLG USU | 2026**

---

## Halaman 9 — KEYWORD

URI, URN, URL, IRI?

**ITLG USU | 2026**

---

## Halaman 10 — KEYWORD: URI

# URI

**Uniform Resource Identifier**

String yang secara unik mengidentifikasi suatu resource  
(real maupun abstrak)

Contoh: **mailto:alice@gmail.com**  
Merujuk pada alamat email (dengan schema mailto:)

**ITLG USU | 2026**

---

## Halaman 11 — KEYWORD: URN

# URN

**Uniform Resource Name**

URI yang mengidentifikasi resource berdasarkan nama  
tanpa terikat pada lokasi atau cara mengakses datanya.

Contoh: **urn:isbn:9780140328721**  
Merujuk pada buku “Fantastic Mr. Fox”. Dikelola oleh ISBN  
International Agency.

**ITLG USU | 2026**

---

## Halaman 12 — KEYWORD: URL

# URL

**Uniform Resource Locator**

URI yang tidak hanya mengidentifikasi, tetapi juga  
memberitahu lokasi dan cara mengaksesnya.

Contoh: **https://google.com**  
Lokasi (alamat): google.com, cara mengaksesnya (protokol): https

**ITLG USU | 2026**

---

## Halaman 13 — KEYWORD: IRI

# IRI

**International Resource Identifier**

Superset dari URI yang mencakup karakter di luar ASCII.  
IRI bisa dikonversi menjadi URI.

Contoh: **http://例⼦ . 测试 /**  
Lokasi (alamat): 例⼦ . 测试 , cara mengaksesnya (protokol): http

(IRI) `http://例⼦ . 测试 /` → (URI) `http://xn--fsqu00a.xn--0zwm56d`

**ITLG USU | 2026**

---

## Halaman 14 — URI, URN, URL, IRI

- IRI
  - URI
    - URN
    - URL

**ITLG USU | 2026**

---

## Halaman 15 — URI, URN, URL, IRI?

**file:///C:/Program%20Files/Microsoft**  
URL, URI, IRI

**ftp://ftp.example.org/file.txt**  
URL, URI, IRI

**urn:uuid:4def-3523-ac3d-5ec6**  
URN, URI, IRI

**ITLG USU | 2026**

---

## Halaman 16 — URI, URN, URL, IRI?

**https://example.com/café**  
IRI

**https://example.com/caf%C3%A9**  
URL, URI, IRI

**ITLG USU | 2026**

---

## Halaman 17 — SEMANTIC WEB

# Web Semantik

Konsep yang dicetuskan oleh **W3C (World Wide Web Consortium)**.

### Tujuannya:

Ekstensi dari **Web of Documents → Web of Linked Data**

(dengan kata lain, membuat data-data yang berada di web saling terhubung  
dan seolah-olah dapat dipahami komputer)

**ITLG USU | 2026**

---

## Halaman 18 — CORNERSTONES

# PILAR PEMBENTUK WEB SEMANTIK

yang ditetapkan oleh W3C:

1. **RDF** → Bagaimana data direpresentasikan
2. **OWL** → Bagaimana makna/aturan/relasi yang lebih kompleks
3. **SPARQL** → Bagaimana data RDF ditanyakan/query

**ITLG USU | 2026**

---

## Halaman 19 — RDF

# RDF

**Resource Description Framework**

- **Resource:** Segala sesuatu yang bisa diidentifikasi dan dideskripsikan
- **Description:** Deskripsi
- **Framework:** Struktur dasar yang melandasi sebuah sistem

Standar/tata cara/aturan untuk mendeskripsikan data agar  
saling terhubung.

**ITLG USU | 2026**

---

## Halaman 20 — RULES

# Aturan Utama RDF

### 1. Model

Semua informasi harus dipecah  
dalam format **triple**.

### 2. Identifikasi

Resource yang berbeda tidak  
boleh mempunyai URI yang  
sama.

### 3. Serialisasi

Format penulisan RDF yang  
diakui oleh W3C sebagai  
standar meliputi **RDF/XML,  
Turtle, N-Triples, dan JSON-LD.**

**ITLG USU | 2026**

---

## Halaman 21 — RDF SERIALIZATION

# SERIALISASI RDF

Serialisasi RDF = Cara menuliskan RDF

**Analogi:**

RDF = Bahasa (secara umum)  
Serialisasi = Bahasa spesifik, misal Bahasa Indonesia

| Saya | cinta | kamu | I | love | you | 我 | 爱 | 你 |
|---|---|---|---|---|---|---|---|---|
| S | P | O | S | P | O | S | P | O |

**KETIGANYA MEMPUNYAI ARTI YANG SAMA**

**ITLG USU | 2026**

---

## Halaman 22 — RDF SERIALIZATION

1. **N-Triples:** bentuk paling sederhana dengan URI lengkap yang tidak disingkat. Penulisannya diakhiri dengan tanda titik.

2. **Turtle:** Sintaks dan format file untuk mengekspresikan data dalam model data RDF.

3. **XML (eXtensible Markup Language):** bahasa markup yang dirancang untuk menyimpan dan mengangkut data. XML memungkinkan pengguna untuk mendefinisikan tag mereka sendiri. XML sering digunakan dalam berbagai aplikasi untuk pertukaran data, baik di web maupun di luar web.

**ITLG USU | 2026**

---

## Halaman 23 — RDF SERIALIZATION: N-TRIPLES

# N-Triples

```ntriples
<http://example.org/JohnDoe> <http://example.org/hasJob> "Teacher" .
<http://example.org/Alice> <http://example.org/hasJob> "Student" .
<http://example.org/Bob> <http://example.org/hasGender> "Male" .
<http://example.org/Alice> <http://example.org/hasGender> "Female" .
```

**ITLG USU | 2026**

---

## Halaman 24 — RDF SERIALIZATION: TURTLE

# Turtle

**Namespace**

```turtle
@prefix ex: <http://example.org/> .

ex:JohnDoe ex:hasJob "Teacher" .
ex:Alice
    ex:hasJob "Student" ;
    ex:hasGender "Female" .
ex:Bob ex:hasGender "Male" .
```

**ITLG USU | 2026**

---

## Halaman 25 — RDF SERIALIZATION: JSON-LD

# JSON-LD

```json
{
  "@context": {
    "@vocab": "http://example.org/"
  },
  "@graph": [
    {
      "@id": "http://example.org/JohnDoe",
      "hasJob": "Teacher"
    },
    {
      "@id": "http://example.org/Alice",
      "hasJob": "Student",
      "hasGender": "Female"
    },
    {
      "@id": "http://example.org/Bob",
      "hasGender": "Male"
    }
  ]
}
```

**ITLG USU | 2026**

---

## Halaman 26 — RDF SERIALIZATION: XML

# XML

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<anggota>
    <petani>Atribut</petani>
    <petani id="2" jabatan="wakil">
    </petani>
</anggota>
```

1. Setiap file XML WAJIB memiliki 1 DAN HANYA 1 root. Dalam kasus ini, root-nya adalah `<anggota>`.
2. Root adalah parent dari semua elemen lainnya.
3. elemen dengan kedalaman setara disebut sibling.

**Bagian deklarasi**  
**Atribut**  
**Elemen**  
**Tag pembuka**  
**Tag penutup**  
**Isi elemen / content**

**ITLG USU | 2026**

---

## Halaman 27 — RDF SERIALIZATION: RDF/XML

# RDF/XML

**Namespace**

```xml
<?xml version="1.0"?>
<rdf:RDF
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:ex="http://example.org/">

    <rdf:Description rdf:about="http://example.org/JohnDoe">
        <ex:hasJob>Teacher</ex:hasJob>
    </rdf:Description>

    <rdf:Description rdf:about="http://example.org/Alice">
        <ex:hasJob>Student</ex:hasJob>
        <ex:hasGender>Female</ex:hasGender>
    </rdf:Description>

    <rdf:Description rdf:about="http://example.org/Bob">
        <ex:hasGender>Male</ex:hasGender>
    </rdf:Description>
</rdf:RDF>
```

**ITLG USU | 2026**

---

## Halaman 28 — RDF SERIALIZATION: EXAMPLE 1

# Contoh Lain 1 (Turtle)

```turtle
@prefix dbr: <http://dbpedia.org/resource/> .
@prefix dbp: <http://dbpedia.org/property/> .

dbr:Harry_Potter dbp:books dbr:Harry_Potter_and_the_Deathly_Hallows,
    dbr:Harry_Potter_and_the_Prisoner_of_Azkaban,
    dbr:Harry_Potter_and_the_Chamber_of_Secrets,
    dbr:Harry_Potter_and_the_Order_of_the_Phoenix,
    dbr:Harry_Potter_and_the_Goblet_of_Fire,
    dbr:Harry_Potter_and_the_Half-Blood_Prince .
```

**ITLG USU | 2026**

---

## Halaman 29 — RDF SERIALIZATION: EXAMPLE 1

# Graph Contoh Lain 1

**Subjek:** `dbr:Harry_Potter`  
**Predikat:** `dbp:books`  
**Objek:**

- `dbr:Harry_Potter_and_the_Deathly_Hallows`
- `dbr:Harry_Potter_and_the_Prisoner_of_Azkaban`
- `dbr:Harry_Potter_and_the_Chamber_of_Secrets`
- `dbr:Harry_Potter_and_the_Order_of_the_Phoenix`
- `dbr:Harry_Potter_and_the_Goblet_of_Fire`
- `dbr:Harry_Potter_and_the_Half_Blood_Prince`

**ITLG USU | 2026**

---

## Halaman 30 — RDF SERIALIZATION: EXAMPLE 2

# Contoh Lain 2 (RDF/XML)

```xml
<rdf:Description rdf:about="http://dbpedia.org/resource/Harry_Potter">
    <dbp:genre rdf:resource="http://dbpedia.org/resource/Young-adult_fiction" />
    <dbp:genre rdf:resource="http://dbpedia.org/resource/Mystery_fiction" />
    <dbp:genre rdf:resource="http://dbpedia.org/resource/Drama" />
    <dbp:genre rdf:resource="http://dbpedia.org/resource/Fantasy_literature" />
    <dbp:genre rdf:resource="http://dbpedia.org/resource/Thriller_(genre)" />
    <dbp:genre rdf:resource="http://dbpedia.org/resource/Bildungsroman" />
    <dbp:country rdf:datatype="http://www.w3.org/1999/02/22-rdf-syntax-ns#langString">
        United Kingdom
    </dbp:country>
    <dbp:language rdf:datatype="http://www.w3.org/1999/02/22-rdf-syntax-ns#langString">
        English
    </dbp:language>
    <dbp:author rdf:resource="http://dbpedia.org/resource/J._K._Rowling" />
</rdf:Description>
```

**ITLG USU | 2026**

---

## Halaman 31 — RDF SERIALIZATION: EXAMPLE 2

# Graph Contoh Lain 2

**Subjek:** `dbr:Harry_Potter`

**Predikat dan objek:**

- `dbp:author` → `dbr:J._K._Rowling`
- `dbp:country` → United Kingdom
- `dbp:language` → English
- `dbp:genre` → `dbr:Bildungsroman`
- `dbp:genre` → `dbr:Mystery_(fiction)`
- `dbp:genre` → `dbr:Thriller_(genre)`
- `dbp:genre` → `dbr:Young-adult_fiction`
- `dbp:genre` → `dbr:Drama`
- `dbp:genre` → `dbr:Fantasy_literature`

**ITLG USU | 2026**

---

## Halaman 32 — ASSIGNMENT

# Tugas??

**ITLG USU | 2026**

---

## Halaman 33 — ASSIGNMENT

# Tidak ada tugas

**ITLG USU | 2026**

---

## Halaman 34 — ASSIGNMENT

# Reaksi kalian

←

**ITLG USU | 2026**

---

## Halaman 35 — ASSIGNMENT

# Tapi boong,

awokwok

**ITLG USU | 2026**

---

## Halaman 36 — ASSIGNMENT

# Tugas 1

1. Carilah sebuah RDF dalam format XML (Topiknya bebas).
2. Minimal 12 Objek.
3. Representasikan RDF tersebut ke dalam Graph (Format png / jpeg).
3. File yang dikumpulkan adalah file XML dan file png/jpeg

**Instruksi:**

**Deadline:** 7 Oktober 2026 pukul 23.59

**Pengumpulan:** https://forms.gle/p8MZ8xX4Mt729ysv8

**ITLG USU | 2026**

---

## Halaman 37 — THANK YOU

# THANK YOU

# FOR YOUR

# ATTENTION

~ Bis Mortis, Semel Sepultus
