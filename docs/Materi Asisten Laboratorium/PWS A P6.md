# PWS A P6

## Halaman 1
PWS

KOM A 25

APACHE JENA FUSEKI
DAN
SPARQL

P6

PANJI DEPARI TI034

---

## Halaman 2
TOPICS OF
DISCUSSION

01. WEB SEMANTIK
02. RDF
03. XML
04. OWL
05. PROTEGE
06. JENA FUSEKI
07. SPARQL
08. SPARQL FUNCTION

---

## Halaman 3
WHAT WE KNOW

Sampai saat ini..
Kita sudah menuliskan pengetahuan/knowledge
base/dataset sesuai ketentuan Web Semantik

ITLG USU | 2026

---

## Halaman 4
PROBLEM

Bagaimana cara mengolah
pengetahuan tersebut?

ITLG USU | 2026

---

## Halaman 5
SOLUTION

Apache Jena Fuseki

ITLG USU | 2026

---

## Halaman 6
ANALOGY

Protégé
GUI untuk manajemen database
relasional (MySQL)

Struktur data: table
Bahasa kueri: SQL

Apache Jena Fuseki
GUI untuk manajemen dataset triple,
sekaligus sebagai data server

Struktur data: graf
Bahasa kueri: SPARQL

ITLG USU | 2026

---

## Halaman 7
JENA FUSEKI & SPARQL

Saatnya Hands-on
Buka Notion

ITLG USU | 2026

---

## Halaman 8
PROBLEM

SPARQL tidak memiliki reasoner bawaan,
sehingga akan bingung jika tidak diberikan
RDF yang lengkap

ITLG USU | 2026

---

## Halaman 9
PROBLEM: EXAMPLE

Result: True

Result: False

ITLG USU | 2026

---

## Halaman 10
SOLUTION

Konfigurasikan reasoner untuk
SPARQL

ITLG USU | 2026

---

## Halaman 11
PROBLEM

ITLG USU | 2026

Bagaimana cara mengolah
pengetahuan tersebut?

---

## Halaman 12
PROBLEM

Menulis sintax triple sangat ribet
dan mudah silap

ITLG USU | 2026

---

## Halaman 13
SPARQL

SPARQL

SPARQL Protocol and RDF Query Language

ITLG USU | 2026

---

## Halaman 14
SPARQL

Aku   suka   Nasi
S      P      O

`:Aku :suka :Nasi`

ITLG USU | 2026

---

## Halaman 15
SPARQL: EX#1

`:Aku :suka :Nasi`
S      P     O

Pertanyaan:
`?variable :suka :Nasi`

`?variable = :Aku`

ITLG USU | 2026

---

## Halaman 16
SPARQL: EX#2

`:Aku :suka :Nasi`
S     P      O

Pertanyaan:
`:Aku :suka ?variable`

`?variable = :Nasi`

ITLG USU | 2026

---

## Halaman 17
SPARQL: EX#3

`:Aku :suka :Nasi`
S      P     O

Pertanyaan:
`?variable1 :suka ?variable2`

`?variable1 = :Aku`
`?variable2 = :Nasi`

ITLG USU | 2026

---

## Halaman 18
SPARQL: EX#3

`:Aku :suka :Nasi`
`:Kamu :suka :Nasi`

Pertanyaan:
`?variable1 :suka ?variable2`

`?variable1 = :Aku :Kamu`

ITLG USU | 2026

---

## Halaman 19
SPARQL: HOW TO

4 cara untuk bertanya di SPARQL

SELECT
Mencari triple yang
sesuai pola

ASK
Bertanya untuk
mendapatkan jawaban
True/False

DESCRIBE
Mendeskripsikan sebuah resource
(triple yang melibatkannya)

CONSTRUTCT
Membuat graph baru
yang berisi triple sesuai
ketentuan

ITLG USU | 2026

---

## Halaman 20
SPARQL: SELECT#0

SELECT

mengoutput Object
dari triple yang
menggunakan :nama
sebagai property

ITLG USU | 2026

---

## Halaman 21
SPARQL: SELECT#1

Menggunakan Prefix

SELECT

mengoutput Object
dari triple yang
menggunakan :nama
sebagai property

ITLG USU | 2026

---

## Halaman 22
SPARQL: SELECT#2

SELECT

mengoutput nama
individu dari class
Mahasiswa

ITLG USU | 2026

---

## Halaman 23
SPARQL: SELECT#3

SELECT

mengoutput nama
individu beserta
umurnya dan
diurutkan berdasarkan
umur.

ITLG USU | 2026

---

## Halaman 24
SPARQL: SELECT#4

SELECT

mengoutput nama
individu beserta
umurnya dan
diurutkan berdasarkan
umur. Ambil hanya 2
teratas, skip row 1.

ITLG USU | 2026

---

## Halaman 25
SPARQL: ASK

ASK

Bertanya apakah ada
individu dari class
Mahasiswa bernama
“FAREL HIA”

*FALSE karena case sensitive

ITLG USU | 2026

---

## Halaman 26
SPARQL: DESCRIBE

DESCRIBE

Mendeskripsikan :chyntia
(triple yang subject
nya merupakan :chyntia)

ITLG USU | 2026

---

## Halaman 27
SPARQL: CONSTRUCT

CONSTRUCT

Membuat graph baru
sesuai ketentuan.

ITLG USU | 2026

---

## Halaman 28
THANK YOU
FOR YOUR
ATTENTION

~ Ecce Agnus Dei
