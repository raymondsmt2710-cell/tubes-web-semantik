# PWS A P3

## Halaman 1
PWS

KOM A 25

OWL

P3

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
CASE STUDY 1

Jakarta adalah ibu kota Indonesia

Jakarta (s) - adalah ibu kota (p) - Indonesia (o)
Indonesia (s) - mempunyai ibu kota (p) - Jakarta (o)

ITLG USU | 2026

---

## Halaman 4
PROBLEM

Mesin tidak tahu bahwa kedua
statement itu setara

ITLG USU | 2026

---

## Halaman 5
SOLUTION

OWL

Web Ontology Language

ITLG USU | 2026

---

## Halaman 6
CASE STUDY 1: TURTLE

Tidak perlu lagi menulis:

ITLG USU | 2026

---

## Halaman 7
CASE STUDY 1: RDF/XML

ITLG USU | 2026

---

## Halaman 8
CASE STUDY 2

Wowo teman Tedi

Wowo (s) - teman (p) - Tedi (o)
Tedi (s) - teman (p) - Wowo (o)

ITLG USU | 2026

---

## Halaman 9
CASE STUDY 2: TURTLE

Tidak perlu lagi menulis:

ITLG USU | 2026

---

## Halaman 10
CASE STUDY 2: RDF/XML

ITLG USU | 2026

---

## Halaman 11
CASE STUDY 3

Semua makanan khas Medan adalah
makanan Indonesia.

ITLG USU | 2026

---

## Halaman 12
CASE STUDY 3: TURTLE

ITLG USU | 2026

---

## Halaman 13
CASE STUDY 3: RDF/XML

ITLG USU | 2026

---

## Halaman 14
KEYWORD

Ontologi

KBBI: Cabang ilmu filsafat yang berhubungan dengan hakikat hidup.

ITLG USU | 2026

---

## Halaman 15
OWL

WEB ONTOLOGY LANGUAGE (OWL)

Standar W3C yang dibangun di atas RDF. Fungsi utamanya untuk
mendeskripsikan arti dari istilah-istilah beserta aturan-aturannya.

Intinya: Membuat RDF semakin cerdas.

ITLG USU | 2026

---

## Halaman 16
SEMANTIC WEB: STRUCTURE

Sumber: https://www.researchgate.net/figure/OWL-in-the-Semantic-Web-architecture_fig1_221233499

ITLG USU | 2026

---

## Halaman 17
RDFS: EXAMPLE

Contoh RDFS

ITLG USU | 2026

Deklarasi Class
`ex:Person a rdfs:Class .`

Subclass
`ex:Student rdfs:subClassOf ex:Person .`

Definisi Property
```turtle
ex:teaches rdf:type rdf:Property ;
    rdfs:domain ex:Teacher ;
    rdfs:range ex:Subject .
```

Subproperty
`ex:instructs rdfs:subPropertyOf ex:teaches .`

---

## Halaman 18
OWL: EXAMPLE

Contoh OWL

ITLG USU | 2026

Class Equivalence
```turtle
ex:Feline owl:equivalentClass ex:Cat .
```

Disjoint Class
```turtle
ex:Cat owl:disjointWith ex:Dog .
```

Inverse Property
```turtle
ex:hasParent owl:inverseOf ex:hasChild .
```

Same Individual
```turtle
ex:Donald_Trump owl:sameAs ex:Donald_John_Trump .
```

---

## Halaman 19
OWL: COMPONENT

Komponen Utama OWL

1. Classes
2. Individuals
3. Properties

ITLG USU | 2026

---

## Halaman 20
OWL COMPONENT: CLASSES

Classes

Sekelompok benda/konsep dengan ciri-ciri yang sama.

Contoh:
1. Orang
2. Hewan
3. Makanan
4. Minuman

ITLG USU | 2026

---

## Halaman 21
OWL COMPONENT: INDIVIDUALS

INDIVIDUALS

Instance / anggota dari Class

Contoh:
1. Orang (Class) → Wowo, Tedi (Individuals)
2. Hewan (Class) → Beruang (Individuals)
3. Makanan (Class) → BPK, Rendang (Individuals)
4. Minuman (Class) → Air Mineral (Individuals)

ITLG USU | 2026

---

## Halaman 22
OWL COMPONENT: PROPERTIES

Properties

Terdapat 2 jenis property

Object Property
Merelasikan individu ke individu

Contoh:
Andi adalah teman Budi

`:adalahTeman`
Andi — Budi

Data Property
Merelasikan individu ke properti individunya

Contoh:
PWS memiliki kode TIF2109

`:memilikiKode`
PWS — TIF2109

ITLG USU | 2026

---

## Halaman 23
SEMANTIC WEB: TOOLS

Protégé

Apache Jena Fuseki

Tutorial Download & Install ada di Notion

ITLG USU | 2026

---

## Halaman 24
ASSIGNMENT

ITLG USU | 2026

Tugas??

---

## Halaman 25
ASSIGNMENT

ITLG USU | 2026

Tidak ada tugas

---

## Halaman 26
ASSIGNMENT

ITLG USU | 2026

Reaksi kalian
←

---

## Halaman 27
THANK YOU
FOR YOUR
ATTENTION

~ Ad Maiorem Dei Gloriam
