# PWS A P8

## Halaman 1

PWS

TI034

PANJI DEPARI

KOM A 25

P8

BEYOND THE BASICS

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

SEMANTIC WEB

Membuat komputer bisa memahami data layaknya  
manusia berpikir

ITLG USU | 2026

---

## Halaman 4

SEMANTIC WEB

Kelemahan RDF

Setiap pengetahuan harus ditulis dalam format Triple.

Faktanya, Tidak semua pengetahuan bisa ditulis secara efisien  
dengan triple.

ITLG USU | 2026

---

## Halaman 5

SEMANTIC WEB: MODERN APPROACH

Property Graph

Vector

ITLG USU | 2026

---

## Halaman 6

SEMANTIC WEB: PROPERTY GRAPH

1. Subject dan Object dianggap sebagai node.
2. Property dianggap sebagai edge.
3. Node dan edge dapat mempunyai atributnya sendiri.

ITLG USU | 2026

---

## Halaman 7

SEMANTIC WEB: PROPERTY GRAPH

1. Daniel is a person. Sunita is also a person.
2. Daniel is the brother of Sunita, and Sunita is the sister of Daniel.
3. They are both associated with the same car. The car is a Volvo.
4. Sunita owns this Volvo. She purchased it on January 10th, 2011.
5. Sunita also drives the same car, beginning on the same date, January 10th, 2011.
6. Daniel also drives this Volvo, but he started driving it later, on March 15th, 2013.

ITLG USU | 2026

---

## Halaman 8

SEMANTIC WEB: PROPERTY GRAPH

ITLG USU | 2026

**Teks pada diagram:**

- Brotherhood-1
- Daniel
- Sunita
- Person 1
- Person 2
- Sisterhood-1
- Driveship-1
- Driveship-2
- Car-Purchase 1
- Car 1
- Person
- Car
- Volvo
- 15/Mar/13
- 10/Jan/11
- 10/Jan/11

**Label hubungan pada diagram:**

- name-is
- is_brother_via
- brother_of_via
- sister_of_via
- is_sister_via
- Drives via
- by-person
- of car
- rdf:type
- start-date
- purchase-date
- Brand-is

---

## Halaman 9

SEMANTIC WEB: PROPERTY GRAPH

ITLG USU | 2026

**Teks pada diagram:**

- Person
  - Name: Daniel
- Person
  - Name: Sunita
- Car
  - Brand: Volvo

**Hubungan dan keterangan pada diagram:**

- BROTHER_OF
- SISTER_OF
- OWNS
  - Since: 10/Jan/11
- DRIVES
  - Since: 15/Mar/13
- DRIVES
  - Since: 10/Jan/11

---

## Halaman 10

SEMANTIC WEB: PROPERTY GRAPH

Use Case

Sistem Rekomendasi

Supply chain analysis

Fraud detection

ITLG USU | 2026

---

## Halaman 11

SEMANTIC WEB: PROPERTY GRAPH

ITLG USU | 2026

**Teks pada diagram:**

- Action
- FAVORITE
- User1
- WATCHED
- movie1
- movie2
- movie3
- movie4
- movie5
- movie6
- movie7
- movie8
- movie9
- movie10
- movie11
- movie12
- similar

---

## Halaman 12

SEMANTIC WEB: PROPERTY GRAPH

Contoh Database Graph

Neo4j

Amazon Neptune

ArangoDB

ITLG USU | 2026

---

## Halaman 13

SEMANTIC WEB: VECTOR

1. Data disimpan dalam bentuk vektor dimensi tinggi.
2. Data yang “mirip” mempunyai jarak vektor yang berdekatan.
3. Jarak vektor dihitung dengan euclidean distance atau cosine similarity.

ITLG USU | 2026

---

## Halaman 14

SEMANTIC WEB: VECTOR

Euclidean Distance

2D

3D

**Rumus 2D:**

d = √(|y₂ − y₁|² + |x₂ − x₁|²)

**Teks pada ilustrasi 3D:**

Distance Between Two Points in 3D

d = √((x₂ − x₁)² + (y₂ − y₁)² + (z₂ − z₁)²)

here,

d = distance between A and B

A = (x₁,y₁,z₁)

B = (x₂,y₂,z₂)

ITLG USU | 2026

---

## Halaman 15

SEMANTIC WEB: VECTOR

Cosine Similiarity

**Teks pada ilustrasi:**

Vector Similarity Measures: Cosine | Zilliz

cos(θ) = (A · B) / (||A|| ||B||)

Queen = [0.3, 0.9]

King = [0.5, 0.7]

Cos(Queen, King) = ((0.3*0.5) + (0.9*0.7)) / (√(0.3² + 0.9²) * √(0.5² + 0.7²))

= (0.15 + 0.63) / (√0.9² * √0.74)

= 0.78 / √0.666

= 0.956

Cosine Similarity sering digunakan untuk AI dalam memahami kemiripan kata.

ITLG USU | 2026

---

## Halaman 16

SEMANTIC WEB: VECTOR

Use Case

Similarity search

Anomaly detection

Large Language  
Model (LLM)

ITLG USU | 2026

---

## Halaman 17

SEMANTIC WEB: VECTOR

ITLG USU | 2026

**Teks pada ilustrasi:**

- [0.34, 2.35, 8.34, ...]
- 300 dimensions
- Chicken
- Wolf
- Dog
- Cat
- Banana
- Apple
- G

---

## Halaman 18

SEMANTIC WEB: VECTOR

Contoh Database Vector

Pinecone

Milvus

Weaviate

ITLG USU | 2026

---

## Halaman 19

ASSIGNMENT

Tugas??

ITLG USU | 2026

---

## Halaman 20

ASSIGNMENT

Tidak ada tugas

ITLG USU | 2026

---

## Halaman 21

ASSIGNMENT

Reaksi kalian

←

ITLG USU | 2026

---

## Halaman 22

ASSIGNMENT

Tapi...

ITLG USU | 2026

---

## Halaman 23

EXAM

Minggu depan  
kita UAS

ITLG USU | 2026

---

## Halaman 24

THANK YOU  
FOR YOUR  
ATTENTION

~ Kyrie eleison
