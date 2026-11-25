# Ontologi Mendalam + Frontend Arsip Digital Museum — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Memperdalam ontologi RDF (subkelas, inverse, cardinality, entitas pendukung) dan merombak frontend menjadi "arsip digital museum" yang berkarakter, tanpa menyerpih identitas Arsip Kolonial.

**Architecture:** Data bergerak satu arah: `data/museums.json` → `buildRdf()` (RDF/XML) → Fuseki → SPARQL → DTO → React. Kita memperkaya `MuseumRecord` dengan field baru, menambah kelas/properti/aksioma di generator dan TTL, menambah query rincian, lalu memakai field baru di UI melalui komponen `SpecimenCard`/`IndexBoard`/`MuseumPlate` yang baru.

**Tech Stack:** Next.js 16 (App Router), React 19, TypeScript, Tailwind v4, Zustand, Vitest, Oxigraph (uji integrasi), Apache Jena Fuseki.

**Spec:** `docs/superpowers/specs/2026-02-17-arsip-mendalam-design.md`

## Global Constraints

- Namespace tetap: `SDP` = `https://museumsumatera.id/ontology#`, `RES` = `https://museumsumatera.id/resource/`.
- **Jangan** menambah literal `xsd:gYear` untuk field baru — pakai `xsd:integer` (temuan builder-check #2; `generate-rdf.test.ts` menguji `#gYear">`).
- Semua field baru di `MuseumDTO` **wajib opsional** (`?:`) — fixture `related.test.ts`/`route.test.ts` memakai objek literal lengkap (temuan #4).
- `type` di SPARQL harus dikumpulkan via subquery `GROUP_CONCAT`, bukan `OPTIONAL` langsung (temuan #3, cegah baris berganda).
- Properti yang punya `owl:inverseOf` **tidak boleh** menyimpan `rdfs:domain`/`rdfs:range` eksplisit (konsistensi A1).
- `Collection` hanya diisi bila sumber menyebut kategori eksplisit (P3). `Facility` hanya bila sumber menyebut (P5). `HeritageStatus` **tidak** diinstansiasi (P5).
- `relatedMuseum` = bonus bobot **+4** pada skor benang merah; aturan "skor 0 disembunyikan" tetap (P4).
- Penyaringan katalog tetap **100% di SPARQL**. Bahasa UI & label `@id`.
- Identitas Arsip Kolonial: `--paper: #f3ece0` dan `--font-serif` tetap ada di `globals.css` (kriteria #10).
- Pakai `npm` (bukan bun), meski desain lama menyebut bun.

## Pemetaan Subkelas (dikunci dari `history`/`description`)

`type` per museum (field baru `types: string[]` di JSON; memakai nama lokal kelas):

| slug | types |
|---|---|
| museum-negeri-aceh | StateMuseum |
| museum-tsunami-aceh | StateMuseum |
| museum-cut-nyak-dhien | StateMuseum |
| museum-malikussaleh | SiteMuseum |
| museum-negeri-sumatera-utara | StateMuseum |
| museum-huta-bolon-simanindo | SiteMuseum |
| museum-tb-silalahi-center | PrivateMuseum |
| museum-sisingamangaraja-xii | SiteMuseum, StateMuseum |
| museum-daerah-deli-serdang | StateMuseum |
| museum-sang-nila-utama | StateMuseum |
| museum-sultan-sulaiman-badrul-alamsyah | SiteMuseum, StateMuseum |
| museum-linggam-cahaya | SiteMuseum |
| museum-istana-siak | SiteMuseum |
| museum-adityawarman | StateMuseum |
| museum-rumah-kelahiran-buya-hamka | SiteMuseum |
| museum-tuanku-imam-bonjol | SiteMuseum |
| museum-kereta-api-sawahlunto | SiteMuseum, StateMuseum |
| museum-negeri-jambi | StateMuseum |
| museum-siginjai | StateMuseum |
| museum-negeri-bengkulu | StateMuseum |
| rumah-pengasingan-bung-karno | SiteMuseum |
| museum-negeri-sumatera-selatan | StateMuseum |
| museum-sultan-mahmud-badaruddin-ii | SiteMuseum, StateMuseum |
| museum-taman-purbakala-sriwijaya | SiteMuseum |
| museum-timah-indonesia | StateMuseum |
| museum-negeri-lampung | StateMuseum |
| museum-ketransmigrasian-lampung | StateMuseum |
| museum-purbakala-pugung-raharjo | SiteMuseum |

Aturan: setiap entri **minimal** satu tipe; `SiteMuseum` boleh beririsan dengan `StateMuseum`; tidak pernah `StateMuseum` + `PrivateMuseum` sekaligus (disjoint).

## Review Focus

Input/keadaan yang spek implikasikan tetapi tak dieksplisitkan tes — satu baris tiap, dan tesnya ada di task pemilik:

1. **Museum tanpa kategori/fasilitas/`relatedMuseum` (mayoritas).** Harapan: halaman museum tetap rapi tanpa bagian kosong yang menganga — tidak ada `<h2>Klasifikasi koleksi</h2>` yang diikuti ruang kosong. (Task 9.)
2. **Museum dengan >1 `rdf:type`** (mis. `SiteMuseum`+`StateMuseum`). Harapan: katalog tidak menghasilkan baris ganda dan badge tipe menampilkan keduanya. (Task 7.)
3. **Fuseki mati saat membuka halaman museum/bab/katalog.** Harapan: kondisi offline lama tetap jalan; field baru tidak membuat halaman crash. (Task 9, 10.)
4. **`q`/filter tetap memakai field baru?** Harapan: perluasan pencarian tidak memecahkan query lama; filter tetap di SPARQL. (Task 8.)
5. **`relatedMuseum` menunjuk museum yang tidak ada / dirinya sendiri.** Harapan: generator menolak (validasi), bukan menghasilkan graf setengah jadi. (Task 4.)

---

### Task 1: Tipe data baru untuk `MuseumRecord`

**Files:**
- Modify: `src/lib/types.ts:86-111` (MuseumRecord), tambah konstanta kelas
- Test: `src/lib/types.test.ts` (buat baru bila perlu) — atau perluas test validasi di Task 3

**Interfaces:**
- Consumes: —
- Produces: `MUSEUM_TYPES = ["StateMuseum","SiteMuseum","PrivateMuseum"] as const`; `type MuseumType`; field baru opsional di `MuseumRecord`: `types?: MuseumType[]`, `collections?: string[]`, `facilities?: string[]`, `founder?: string | null`, `governingBody?: string | null`, `openingHours?: string | null`, `collectionSize?: number | null`, `heritage?: string | null`, `relatedSlugs?: string[]`.

- [ ] **Step 1: Tambah konstanta & tipe di `src/lib/types.ts`**

Tambahkan setelah `VERIFICATION_STATUSES`:

```ts
export const MUSEUM_TYPES = ["StateMuseum", "SiteMuseum", "PrivateMuseum"] as const;
export type MuseumType = (typeof MUSEUM_TYPES)[number];

export const MUSEUM_TYPE_LABELS: Record<MuseumType, string> = {
  StateMuseum: "Museum Negeri",
  SiteMuseum: "Museum Situs",
  PrivateMuseum: "Museum Swasta",
};
```

- [ ] **Step 2: Tambah field opsional pada `MuseumRecord`**

Di akhir interface `MuseumRecord` (sebelum `}` penutup):

```ts
  /** Subklasifikasi ontologi; minimal satu. */
  types?: MuseumType[];
  /** Kategori koleksi — hanya bila sumber menyebut eksplisit. */
  collections?: string[];
  /** Fasilitas — hanya bila sumber menyebut eksplisit. */
  facilities?: string[];
  /** Nama pendiri/tokoh (string), atau null. */
  founder?: string | null;
  governingBody?: string | null;
  openingHours?: string | null;
  collectionSize?: number | null;
  /** Status cagar budaya bila sumber menyebut; sering null. */
  heritage?: string | null;
  /** Slug museum terkait (relasi eksplisit); generator menulis dua arah. */
  relatedSlugs?: string[];
```

- [ ] **Step 3: Tambah field DTO opsional pada `MuseumDTO`**

Di akhir interface `MuseumDTO`:

```ts
  types?: string[];
  collections?: string[];
  facilities?: string[];
  founder?: string | null;
  governingBody?: string | null;
  openingHours?: string | null;
  collectionSize?: number | null;
  heritage?: string | null;
  relatedSlugs?: string[];
```

- [ ] **Step 4: Verifikasi kompilasi**

Run: `npx tsc --noEmit`
Expected: PASS (tidak ada error baru; field baru opsional).

- [ ] **Step 5: Commit**

```bash
git add src/lib/types.ts
git commit -m "feat(types): tambah tipe & field opsional untuk entitas ontologi baru"
```

---

### Task 2: Validasi data untuk entitas baru

**Files:**
- Modify: `src/lib/validate.ts` (tambah aturan)
- Test: `src/lib/validate.test.ts` (perluas)

**Interfaces:**
- Consumes: `MUSEUM_TYPES`, `MuseumType`, `MuseumRecord` (Task 1).
- Produces: `validateMuseums` mengeluarkan error/warning baru untuk `types`, `collections`, `facilities`, `collectionSize`, `relatedSlugs` (slug tak ada).

- [ ] **Step 1: Tulis test gagal**

Tambahkan ke `src/lib/validate.test.ts` (memakai fixture `ok` yang sudah ada di file itu, jangan buat fixture duplikat):

```ts
describe("validasi entitas baru", () => {
  it("menolak tipe yang tidak dikenal", () => {
    const issues = validateMuseums([{ ...ok, types: ["Bogus" as never] }]);
    expect(issues.some((i) => i.field === "types" && i.level === "error")).toBe(true);
  });

  it("menerima tipe sah", () => {
    const issues = validateMuseums([{ ...ok, types: ["StateMuseum", "SiteMuseum"] }]);
    expect(issues.some((i) => i.field === "types" && i.level === "error")).toBe(false);
  });

  it("menolak StateMuseum + PrivateMuseum sekaligus", () => {
    const issues = validateMuseums([{ ...ok, types: ["StateMuseum", "PrivateMuseum"] }]);
    expect(issues.some((i) => i.field === "types" && i.level === "error")).toBe(true);
  });

  it("menolak collectionSize negatif / bukan integer", () => {
    const neg = validateMuseums([{ ...ok, collectionSize: -1 }]);
    expect(neg.some((i) => i.field === "collectionSize" && i.level === "error")).toBe(true);
    const frac = validateMuseums([{ ...ok, collectionSize: 1.5 }]);
    expect(frac.some((i) => i.field === "collectionSize" && i.level === "error")).toBe(true);
  });

  it("menolak relatedSlugs yang menunjuk dirinya sendiri atau slug tak ada", () => {
    const self = validateMuseums([{ ...ok, relatedSlugs: ["museum-ok"] }]);
    expect(self.some((i) => i.field === "relatedSlugs" && i.level === "error")).toBe(true);
    const missing = validateMuseums([{ ...ok, relatedSlugs: ["tidak-ada"] }]);
    expect(missing.some((i) => i.field === "relatedSlugs" && i.level === "error")).toBe(true);
  });
});
```

- [ ] **Step 2: Jalankan test untuk memastikan gagal**

Run: `npx vitest run src/lib/validate.test.ts`
Expected: FAIL — aturan belum ada.

- [ ] **Step 3: Implementasi aturan di `src/lib/validate.ts`**

Tambahkan impor `MUSEUM_TYPES` dari `./types`. Di dalam loop `validateMuseums`, setelah blok `verificationStatus`:

```ts
    if (record.types !== undefined) {
      if (record.types.length === 0) {
        add("types", "error", "Museum harus punya minimal satu tipe.");
      } else {
        for (const t of record.types) {
          if (!(MUSEUM_TYPES as readonly string[]).includes(t)) {
            add("types", "error", `Tipe tidak dikenal: "${t}".`);
          }
        }
        if (record.types.includes("StateMuseum") && record.types.includes("PrivateMuseum")) {
          add("types", "error", "StateMuseum dan PrivateMuseum tidak boleh bersamaan.");
        }
      }
    }

    if (
      record.collectionSize !== null &&
      record.collectionSize !== undefined &&
      (!Number.isInteger(record.collectionSize) || record.collectionSize < 0)
    ) {
      add("collectionSize", "error", `Ukuran koleksi tidak sah: ${record.collectionSize}.`);
    }
```

Untuk `relatedSlugs`, validasi setelah loop karena butuh daftar slug lengkap — tambahkan di akhir fungsi sebelum `return issues`:

```ts
  const allSlugs = new Set(records.map((r) => r.slug));
  for (const record of records) {
    for (const target of record.relatedSlugs ?? []) {
      if (target === record.slug) {
        issues.push({ slug: record.slug, field: "relatedSlugs", level: "error",
          message: "Museum tidak boleh menautkan dirinya sendiri." });
      } else if (!allSlugs.has(target)) {
        issues.push({ slug: record.slug, field: "relatedSlugs", level: "error",
          message: `Museum terkait tidak ditemukan: "${target}".` });
      }
    }
  }
```

- [ ] **Step 4: Jalankan test untuk memastikan lulus**

Run: `npx vitest run src/lib/validate.test.ts`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/lib/validate.ts src/lib/validate.test.ts
git commit -m "feat(validate): validasi types, collectionSize, relatedSlugs"
```

---

### Task 3: Data museum diperkaya (C1)

**Files:**
- Modify: `data/museums.json` (28 record)

**Interfaces:**
- Consumes: field baru `MuseumRecord` (Task 1).
- Produces: `museums.json` dengan `types` (semua), dan `collections`/`facilities`/`founder`/`governingBody`/`collectionSize`/`relatedSlugs` **hanya bila sumber mendukung**.

- [ ] **Step 1: Tambahkan `types` ke seluruh 28 record sesuai tabel Pemetaan Subkelas** (di atas). Pastikan `tb-silalahi` hanya `["PrivateMuseum"]`.

- [ ] **Step 2: Tambahkan field dari sumber yang eksplisit.** Contoh yang didukung sumber:
  - `museum-negeri-aceh`: `collections: ["etnografika","filologika"]` (exhibit menyebut "Koleksi etnografika dan filologika"); `collectionSize: 6038` (history/exhibit menyebut "sekitar 6.038 benda").
  - `museum-timah-indonesia`: `collections: ["etnografi"]` bila exhibit menyebut "Koleksi etnografi Bangka".
  - `museum-negeri-aceh`, `museum-tb-silalahi-center`, dll: `governingBody` **hanya** bila `history`/`description` menyebut badan pengelola eksplisit; bila tidak, biarkan tidak ada.
  - Museum tanpa penyebutan: **jangan** isi `collections`/`facilities`/`heritage`.
- [ ] **Step 3: Tambahkan `relatedSlugs` eksplisit** untuk pasangan yang `history`-nya mendukung (minimal: `museum-negeri-jambi` ↔ `museum-siginjai`; `museum-negeri-aceh` ↔ `museum-tsunami-aceh`). Generator akan menulis dua arah.
- [ ] **Step 4: Verifikasi data**

Run: `npm run check:rdf`
Expected: keluar dengan kode 0; tidak ada error `types`/`collectionSize`/`relatedSlugs`. Warning `perlu-verifikasi` boleh ada.

- [ ] **Step 5: Commit**

```bash
git add data/museums.json
git commit -m "feat(data): perkaya 28 museum dengan types & field bersumber (C1)"
```

---

### Task 4: Generator RDF menulis kelas/aksioma/entitas baru

**Files:**
- Modify: `src/lib/ontology.ts` (`buildRdf`: tambah kelas, property, aksioma, instance)
- Test: `src/lib/ontology.ts` dites lewat `scripts/generate-rdf.test.ts` — perluas

**Interfaces:**
- Consumes: `MuseumRecord` baru (Task 1), `MUSEUM_TYPES` (Task 1), data (Task 3).
- Produces: RDF/XML berisi `rdf:type` turunan, kelas baru, `owl:inverseOf`, restriction, instance `Collection`/`Facility`/`Person`/`relatedMuseum` dua arah.

- [ ] **Step 1: Tulis test gagal** di `scripts/generate-rdf.test.ts`

```ts
it("menulis tipe turunan Museum dan kelas baru", () => {
  const xml = buildRdf(records); // fixture records yang ada
  expect(xml).toContain("sdp:StateMuseum");
  expect(xml).toContain("rdfs:subClassOf");
  expect(xml).toContain("owl:inverseOf");
  expect(xml).toContain("owl:Restriction");
});

it("menulis relatedMuseum dua arah", () => {
  const a = { ...baseRecord("a"), relatedSlugs: ["b"] };
  const b = baseRecord("b");
  const xml = buildRdf([a, b]);
  // a→b dan b→a sama-sama ada
  expect((xml.match(/relatedMuseum/g) ?? []).length).toBeGreaterThanOrEqual(4); // 2 deklarasi + 2 instance
});
```

- [ ] **Step 2: Jalankan test untuk memastikan gagal**

Run: `npx vitest run scripts/generate-rdf.test.ts`
Expected: FAIL.

- [ ] **Step 3: Implementasi di `src/lib/ontology.ts`**

(a) Tambah `classBlock` baru: `StateMuseum`, `SiteMuseum`, `PrivateMuseum`, `Person`, `Founder`, `Curator`, `Facility`, `HeritageStatus`. Tulis `rdfs:subClassOf` untuk tiap subkelas Museum dan Person.

(b) Ubah `objectProperty`/`datatypeProperty` agar menerima argumen `inverse?: string` dan **bila inverse**, **jangan** tulis `rdfs:domain`/`range` (konsistensi A1); tulis `<owl:inverseOf rdf:resource="${SDP}${inverse}"/>`. Contoh:

```ts
function objectProperty(name, domain, range, label, inverse?: string): string[] {
  const head = [
    `${INDENT}<owl:ObjectProperty rdf:about="${SDP}${name}">`,
    `${INDENT}    <rdfs:label xml:lang="id">${label}</rdfs:label>`,
  ];
  if (inverse) {
    head.push(`${INDENT}    <owl:inverseOf rdf:resource="${SDP}${inverse}"/>`);
  } else {
    head.push(`${INDENT}    <rdfs:domain rdf:resource="${SDP}${domain}"/>`);
    head.push(`${INDENT}    <rdfs:range rdf:resource="${SDP}${range}"/>`);
  }
  head.push(`${INDENT}</owl:ObjectProperty>`, "");
  return head;
}
```

(c) Tambah `owl:Restriction` di kelas `Museum` (cardinality: locatedInProvince 1, chapter 1, hasTheme min 1, locatedInCity max 1) — blok `rdfs:subClassOf [ a owl:Restriction ; ... ]`.

(d) Untuk setiap record: tulis `rdf:type` **hanya** untuk tipe turunan (mis. `<sdp:StateMuseum rdf:about="...">` atau tambahkan `<rdf:type rdf:resource="..."/>`), **bukan** selalu `sdp:Museum` bila reasoner bisa menyimpulkan. *(Aman: tetap tulis `sdp:Museum` juga agar kueri lama `?museum a sdp:Museum` terus jalan, ditambah tipe turunan.)*

(e) Tulis instance `Collection` (bila `collections` ada) dengan `collectionCategory`, hubungkan `hasCollection`; instance `Facility` (bila `facilities`); instance `Person`+`Founder` (bila `founder`), hubungkan `hasFounder`. **Jangan** tulis `HeritageStatus`.

(f) Tulis `relatedMuseum` **dua arah**: untuk setiap slug A dengan target B, emit `A relatedMuseum B` dan `B relatedMuseum A` (dekopin, cek agar tidak dobel).

(g) Tambah datatype property: `collectionSize`, `governingBody`, `openingHours`, `collectionCategory`, `facilityName`, `personName`.

- [ ] **Step 4: Jalankan test untuk memastikan lulus**

Run: `npx vitest run scripts/generate-rdf.test.ts`
Expected: PASS.

- [ ] **Step 5: Generate & verifikasi count**

Run: `npm run generate:rdf && npm run check:rdf`
Expected: RDF ditulis; check lolos.

- [ ] **Step 6: Commit**

```bash
git add src/lib/ontology.ts scripts/generate-rdf.test.ts data/museum-sumatera.rdf
git commit -m "feat(ontology): subkelas, inverse, restriction, entitas Collection/Facility/Person, relatedMuseum"
```

---

### Task 5: Selaraskan berkas TTL ontologi

**Files:**
- Modify: `ontology/museum-sumatera.ttl`

**Interfaces:**
- Consumes: skema baru (Task 4) — selaraskan nama kelas/properti/aksioma.
- Produces: `ontology/museum-sumatera.ttl` yang sama semantiknya dengan blok skema di generator.

- [ ] **Step 1: Tambah kelas** `StateMuseum`/`SiteMuseum`/`PrivateMuseum` (+`rdfs:subClassOf sdp:Museum`), `Person`/`Founder`/`Curator` (+subClassOf), `Facility`, `HeritageStatus` dengan label & comment `@id`.
- [ ] **Step 2: Tambah objek property baru** (`hasFounder`/`founderOfMuseum`, `hasFacility`/`facilityOfMuseum`, `heritageStatusOf`/`isHeritageStatusOf`, `namedAfter`/`isNamesakeOfMuseum`, `relatedMuseum`) dengan `owl:inverseOf` dan `owl:SymmetricProperty` pada `relatedMuseum`.
- [ ] **Step 3: Tambah datatype property baru** dan `owl:Restriction` cardinality pada `sdp:Museum`; tambah anotasi `owl:Ontology` (`owl:versionInfo "1.1.0"`, `dcterms:created`, `dcterms:modified`).
- [ ] **Step 4: Verifikasi TTL bisa diparse** (Oxigraph sudah ada di devDependencies):

Run: `npx tsx -e "import {Store} from 'oxigraph'; import {readFileSync} from 'node:fs'; const s=new Store(); s.load(readFileSync('ontology/museum-sumatera.ttl','utf8'),{format:'text/turtle'}); console.log('OK', s.size)"`
Expected: cetak `OK <n>` tanpa error.

- [ ] **Step 5: Verifikasi konsistensi ontologi dengan reasoner (kriteria #2)**

Bila `robot` tersedia di mesin (`robot --help`), jalankan:

Run: `robot reason --input ontology/museum-sumatera.ttl --reasoner hermit --output /tmp/check.owl`
Expected: selesai tanpa "inconsistent ontology".

Bila `robot` **tidak** tersedia, catat di komentar commit bahwa validasi reasoner dilakukan manual lewat Protégé (buka TTL, jalankan HermiT; tidak ada warna merah). Jangan menggagalkan task hanya karena tool tidak terpasang — tapi **jangan** klaim lolos tanpa salah satu bukti.

- [ ] **Step 6: Commit**

```bash
git add ontology/museum-sumatera.ttl
git commit -m "feat(ontology): selaraskan TTL dengan skema generator"
```

---

### Task 6: Query rincian & DTO baru

**Files:**
- Modify: `src/lib/queries.ts` (perluas `MUSEUM_PROJECTION`, `MUSEUM_PATTERNS`, `mapMuseumRow`, `attachMuseumDetail`; tambah query entitas)
- Test: `src/lib/queries.test.ts` (perluas), `src/lib/ontology.test.ts` bila ada

**Interfaces:**
- Consumes: field DTO (Task 1), data RDF (Task 4).
- Produces: `museumCollectionsQuery(slug)`, `museumFacilitiesQuery(slug)`; `MuseumDTO.types` terisi via `GROUP_CONCAT`; `attachMuseumDetail` mengisi `collections`, `facilities`.

- [ ] **Step 1: Tulis test gagal** di `src/lib/queries.test.ts`

```ts
it("mengumpulkan types via GROUP_CONCAT tanpa menggandakan baris", () => {
  const q = searchCatalogQuery({});
  expect(q).toContain("GROUP_CONCAT");
  expect(q).toContain("?types");
  // tidak ada 'a ?type' bebas di blok utama
});
```

- [ ] **Step 2: Jalankan test → FAIL.**

Run: `npx vitest run src/lib/queries.test.ts`

- [ ] **Step 3: Implementasi**

(a) Tambah ke `MUSEUM_PROJECTION`: `?types ?collectionSize ?governingBody ?openingHours ?founder ?heritage`.

(b) Tambah subquery `GROUP_CONCAT` untuk tipe turunan (filtrasi `?type != sdp:Museum`) agar tidak menggandakan baris.

(c) `OPTIONAL` untuk `collectionSize`, `governingBody`, `openingHours`, `founder`, `heritage`.

(d) `mapMuseumRow`: isi field baru (`types: split |`, `collectionSize: num`, dst.). Field kosong → `undefined`.

(e) Tambah `museumCollectionsQuery` dan `museumFacilitiesQuery`; panggil di `attachMuseumDetail` via `Promise.all`.

- [ ] **Step 4: Jalankan test → PASS.**

Run: `npx vitest run src/lib/queries.test.ts`

- [ ] **Step 5: Commit**

```bash
git add src/lib/queries.ts src/lib/queries.test.ts
git commit -m "feat(queries): types via GROUP_CONCAT, query collections/facilities"
```

---

### Task 7: Benang merah + relasi eksplisit (+4)

**Files:**
- Modify: `src/lib/related.ts`
- Test: `src/lib/related.test.ts` (perluas)

**Interfaces:**
- Consumes: `MuseumDTO.relatedSlugs` (Task 1/6).
- Produces: `scoreRelated` menambah `+4` bila `candidate.slug` ada di `base.relatedSlugs`, dengan alasan "relasi arsip eksplisit".

- [ ] **Step 1: Tulis test gagal**

Tambahkan ke `src/lib/related.test.ts`. **Netralkan dulu fixture** agar skor dasar 0 (tema/kota/era/bab tidak sama), sehingga +4 terisolasi:

```ts
it("memberi +4 untuk relasi eksplisit", () => {
  const base = museum({
    slug: "a",
    relatedSlugs: ["b"],
    themes: ["etnografi"],
    city: "Banda Aceh",
    era: "kolonial",
    chapterIndex: 1,
  });
  const cand = museum({
    slug: "b",
    themes: ["arkeologi"],
    city: "Medan",
    era: "modern",
    chapterIndex: 5,
  });
  expect(scoreRelated(base, cand).score).toBe(4);
  expect(scoreRelated(base, cand).reason).toMatch(/arsip/i);
});
```

- [ ] **Step 2: Jalankan → FAIL.**

- [ ] **Step 3: Implementasi** di `related.ts`:

```ts
const EXPLICIT_WEIGHT = 4;
// di scoreRelated, sebelum return (setelah blok bab):
if ((base.relatedSlugs ?? []).includes(candidate.slug)) {
  score += EXPLICIT_WEIGHT;
  reasons.push("relasi arsip eksplisit");
}
```

Aturan filter `entry.score > 0` tetap.

- [ ] **Step 4: Jalankan → PASS.**

Run: `npx vitest run src/lib/related.test.ts`

- [ ] **Step 5: Commit**

```bash
git add src/lib/related.ts src/lib/related.test.ts
git commit -m "feat(related): bobot +4 untuk relasi arsip eksplisit"
```

---

### Task 8: Perluas pencarian ke field baru (tetap di SPARQL)

**Files:**
- Modify: `src/lib/queries.ts` (filters `q` mencari `collections`/`facilities` juga)
- Test: `src/lib/queries.test.ts`

**Interfaces:**
- Consumes: query dari Task 6.
- Produces: `q` mencocokkan juga `?collections`/`?facilities` (via `GROUP_CONCAT`), tanpa membobol SPARQL.

- [ ] **Step 1: Test gagal** — query dengan `q` menghasilkan `FILTER` yang menyebut `?collections`.

- [ ] **Step 2: Jalankan → FAIL.**

- [ ] **Step 3: Implementasi** — tambahkan `CONTAINS(LCASE(COALESCE(STR(?collections),"")),"..." )` ke klausa pencarian per-token; kumpulkan `?collections` via subquery `GROUP_CONCAT` terpisah agar tidak menggandakan baris.

- [ ] **Step 4: Jalankan → PASS.** `npx vitest run src/lib/queries.test.ts`

- [ ] **Step 5: Commit** — `git commit -m "feat(search): q mencakup koleksi dan fasilitas"`

---

### Task 9: Halaman museum — SpecimenCard + panel baru

**Files:**
- Create: `src/components/SpecimenCard.tsx`, `src/components/KoleksiPanel.tsx`, `src/components/FacilityList.tsx`
- Modify: `src/app/museum/[slug]/page.tsx`
- Test: tidak ada unit test UI (sesuai aturan lama); verifikasi lewat `npm run build` + penelusuran manual.

**Interfaces:**
- Consumes: `MuseumDTO` (Task 6), `scoreRelated` (Task 7).
- Produces: halaman museum menampilkan badge tipe, koleksi, fasilitas (hanya bila ada).

- [ ] **Step 1: Buat `SpecimenCard`** — membungkus judul, plate foto berlabel, dan tabel metadata presisi. Props: `{ museum: MuseumDTO }`. **Jangan** render bagian `Klasifikasi koleksi` bila `museum.collections` kosong (Review Focus #1).
- [ ] **Step 2: Buat `KoleksiPanel`** — chips kategori; render `null` bila kosong. `FacilityList` — daftar fasilitas; `null` bila kosong.
- [ ] **Step 3: Integrasikan di `page.tsx`** — ganti blok hero/sidebar dengan `SpecimenCard`; tambahkan `KoleksiPanel`/`FacilityList`; tampilkan badge tipe (`MUSEUM_TYPE_LABELS`). Tetap pertahankan `HeritageBadge` **tidak** dipakai (heritage null).
- [ ] **Step 4: Verifikasi**

Run: `npm run build`
Expected: build lolos TypeScript. Lalu buka satu museum tanpa koleksi — tidak ada bagian kosong.

- [ ] **Step 5: Commit** — `git commit -m "feat(ui): SpecimenCard, panel koleksi & fasilitas di halaman museum"`

---

### Task 10: Sampul & bab — IndexBoard

**Files:**
- Create: `src/components/IndexBoard.tsx`
- Modify: `src/app/page.tsx`, `src/app/jelajah/[chapter]/page.tsx`, `src/components/ChapterList.tsx`, `src/components/MuseumEntry.tsx`
- Test: verifikasi `npm run build`.

**Interfaces:**
- Consumes: `CHAPTERS`, `MuseumDTO` (Task 6), `MUSEUM_TYPE_LABELS` (Task 1).
- Produces: papan indeks bernomor arsip di sampul & bab.

- [ ] **Step 1: Buat `IndexBoard`** — props `{ items: { index:number; label:string; title:string; count:number|null; href?:string }[]; variant?: "cover" | "chapter" }`. Nomor romawi besar serif.
- [ ] **Step 2: Pakai di `page.tsx`** (variant cover) dan `jelajah` (variant chapter).
- [ ] **Step 3: Perbarui `MuseumEntry`** — nomor arsip + plate foto kecil + badge tipe.
- [ ] **Step 4: Verifikasi** `npm run build`.
- [ ] **Step 5: Commit** — `git commit -m "feat(ui): IndexBoard di sampul dan halaman bab"`

---

### Task 11: Katalog — indeks arsip

**Files:**
- Modify: `src/app/katalog/page.tsx`, `src/components/CatalogView.tsx`, `src/components/globals.css` (token baru `.index-board`, `.specimen-card`, `.plate`, `.meta-table`)
- Test: verifikasi `npm run build` + filter tetap di SPARQL (sudah dites Task 8).

**Interfaces:**
- Consumes: `CatalogResponse` (field baru opsional), `MUSEUM_TYPE_LABELS`.
- Produces: katalog tampil seperti indeks kabinet; tidak mengubah logika filter.

- [ ] **Step 1: Tambah utility CSS & token** di `globals.css` (jangan hapus `--paper: #f3ece0`, `--font-serif` — kriteria #10).
- [ ] **Step 2: Ubah `CatalogView`** — grid/daftar indeks; tampilkan jumlah hasil; badge tipe.
- [ ] **Step 3: Verifikasi** `npm run build`; uji filter manual di katalog.
- [ ] **Step 4: Commit** — `git commit -m "feat(ui): katalog sebagai indeks arsip"`

---

### Task 12: Tentang — lembar metode ontologi

**Files:**
- Modify: `src/app/tentang/page.tsx`
- Test: verifikasi `npm run build`.

**Interfaces:**
- Consumes: —
- Produces: halaman Tentang menjelaskan kelas baru & aksioma + cara validasi reasoner.

- [ ] **Step 1: Tambah bagian** "Struktur ontologi" (daftar kelas, subkelas, inverse, restriction) dan "Cara memvalidasi" (perintah `robot`/Protégé).
- [ ] **Step 2: Verifikasi** `npm run build`.
- [ ] **Step 3: Commit** — `git commit -m "docs(ui): lembar metode ontologi di Tentang"`

---

### Task 13: README, verifikasi token, dan uji menyeluruh

**Files:**
- Modify: `README.md`
- (verifikasi) `src/app/globals.css`

**Interfaces:**
- Consumes: seluruh perubahan.
- Produces: dokumentasi mutakhir; bukti kriteria #10.

- [ ] **Step 1: Perbarui README** — bagian ontologi (kelas/aksioma baru), cara memvalidasi dengan reasoner, catatan entitas (Collection/Facility dari sumber).
- [ ] **Step 2: Buktikan kriteria #10 dengan token**:

Run: `grep -E "\-\-paper #f3ece0|\-\-font-serif" src/app/globals.css`
Expected: menemukan kedua token (bukan penilaian visual).

- [ ] **Step 3: Uji menyeluruh**

Run: `npm test && npm run build && npm run generate:rdf && npm run check:rdf`
Expected: semua PASS; `check:rdf` keluar kode 0.

- [ ] **Step 4: Upload & asap manual**

Run: `npm run upload:fuseki` lalu buka `http://localhost:3000`, `http://localhost:3000/katalog`, satu museum, satu bab.
Expected: semua tampil; tidak ada bagian kosong yang menganga.

- [ ] **Step 5: Commit** — `git commit -m "docs: README ontologi baru & bukti token Arsip Kolonial"`
