# Memperdalam Isi Pameran dan Memperkaya Galeri — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Memperdalam setiap entri isi pameran (dari 1 baris menjadi 3–5 kalimat + periode/asal/bahan) dan memperkaya setiap foto galeri, lalu menampilkan kedalaman itu di halaman museum.

**Architecture:** Skema RDF diperluas dengan empat datatype property baru pada `sdp:Exhibit` (`exhibitPeriod`, `exhibitOrigin`, `exhibitMaterial`, `exhibitHighlight`) dan dua pada `sdp:Image` (`imagePeriod`, `imageDetail`). Data di `data/museums.json` ditulis ulang; validator menegakkan ambang kedalaman supaya regresi teks tertangkap otomatis. Halaman museum mendapat `ExhibitList` dua kolom yang menampilkan metadata baru, dan `MuseumGallery` menampilkan `detail` sebagai daftar poin.

**Tech Stack:** Next.js 16 (App Router), TypeScript, React 19, Tailwind v4, Apache Jena Fuseki (SPARQL), Vitest, RDF/XML generator di `src/lib/ontology.ts`.

**Spec:** `docs/superpowers/specs/2026-02-14-isi-pameran-galeri-design.md` (short design — lihat bagian "Approaches" di bawah; spec ini ditulis lebih dulu sebelum Task 1)

## Global Constraints

- Proyek memakai **npm**, bukan bun. Node.js 20+.
- Semua teks antarmuka dan isi memakai **Bahasa Indonesia**.
- Isi pameran ditulis minimal **3 kalimat** dan minimal **180 karakter**; latar belakang foto minimal **220 karakter** (ambang ini ditegakkan validator, bukan sekadar anjuran).
- Setiap klaim sejarah harus dapat ditelusuri ke entri `sources` museum itu. **Dilarang mengarang** nama benda, tahun, atau angka yang tidak didukung sumber.
- Foto **wajib** dari Wikimedia Commons dengan lisensi CC0, CC BY, CC BY-SA, atau domain publik; wajib menyimpan `credit`, `license`, `licenseUrl`, `sourceUrl`. Foto dari situs resmi museum **tidak boleh** dipakai (hak cipta tidak jelas).
- Seluruh museum tetap berstatus `perlu-verifikasi`; jangan mengubah status.
- Semua kueri ke Fuseki lewat route handler Next.js sisi server; tidak ada permintaan browser langsung ke Fuseki.
- Properti RDF baru mengikuti pola yang ada: camelCase, `rdfs:domain`/`rdfs:range` lewat helper `datatypeProperty()`, dan ditulis dengan `xml:lang="id"` bila berupa teks.
- `npm test` dan `npm run build` harus lulus di akhir setiap task.

## Approaches

Tiga arah dipertimbangkan saat desain:

| Arah | Isi | Trade-off | Keputusan |
|---|---|---|---|
| **A. Perdalam teks saja** | Naikkan deskripsi pameran & latar galeri, tanpa bidang baru | Cepat, nol risiko foto, tapi halaman tidak terasa berubah strukturnya | Ditolak sendirian — pengguna minta "lebih penuh", kedalaman teks saja tidak menambah apa yang *terlihat* |
| **C. Perdalam teks + bidang naratif baru** | A + `period`/`origin`/`material`/`highlight` pada pameran, `period`/`detail` pada foto | Sedikit mengubah skema + validator + 2 komponen | **DIPILIH** — kedalaman terasa tanpa bergantung ketersediaan foto berlisensi |
| **B. Tambah foto + teks** | C + unduh 2–3 foto baru per museum | Paling penuh, tapi 4 museum hanya punya 1 foto layak di Commons; verifikasi lisensi manual per foto | Dikerjakan **sebagian**: hanya museum yang sudah terbukti punya foto Commons layak (lihat Task 6) |

Keputusan pengguna: "langsung aja" — melanjutkan arah **C**, lalu **B** secara terbatas.

## File Structure

| File | Tanggung jawab |
|---|---|
| `src/lib/types.ts` | Tambah bidang opsional pada `Exhibit` dan `MuseumImage` |
| `src/lib/ontology.ts` | Tulis properti RDF baru saat membangun graf |
| `src/lib/queries.ts` | Tarik properti baru di kueri rincian; petakan ke DTO |
| `src/lib/validate.ts` | Tegakkan ambang kedalaman teks + kelengkapan metadata pameran |
| `src/components/ExhibitList.tsx` | Tampilkan metadata pameran dalam tata letak dua kolom |
| `src/components/MuseumGallery.tsx` | Tampilkan `detail` sebagai daftar poin |
| `data/museums.json` | Sumber kebenaran isi — ditulis ulang per museum |
| `src/lib/ontology.test.ts` (baru) | Test generator untuk properti baru |

---

### Task 1: Perluas tipe data

**Files:**
- Modify: `src/lib/types.ts:85-88` (`Exhibit`), `src/lib/types.ts:69-83` (`MuseumImage`)
- Test: `src/lib/types.test.ts` (buat baru)

**Interfaces:**
- Consumes: tidak ada
- Produces: `Exhibit` mendapat `period?`, `origin?`, `material?`, `highlight?` (semua `string | null`); `MuseumImage` mendapat `period?`, `detail?` (semua `string | null`)

- [ ] **Step 1: Write the failing test**

Buat `src/lib/types.test.ts`:

```ts
import { describe, it, expect } from "vitest";
import type { Exhibit, MuseumImage } from "./types";

describe("tipe isi pameran dan foto", () => {
  it("menerima bidang kedalaman pada Exhibit", () => {
    const exhibit: Exhibit = {
      title: "Lonceng Cakra Donya",
      description: "Deskripsi panjang yang memenuhi ambang validator.",
      period: "abad ke-15",
      origin: "Kesultanan Pasai",
      material: "perunggu",
      highlight: true,
    };
    expect(exhibit.period).toBe("abad ke-15");
    expect(exhibit.highlight).toBe(true);
  });

  it("menerima bidang kedalaman pada MuseumImage", () => {
    const image: MuseumImage = {
      src: "/images/museums/x/1.jpg",
      alt: "Foto",
      caption: "Keterangan",
      credit: "Seseorang",
      license: "CC BY-SA 4.0",
      licenseUrl: null,
      sourceUrl: "https://commons.wikimedia.org/wiki/File:X.jpg",
      period: "1915",
      detail: ["Poin pertama", "Poin kedua"],
    };
    expect(image.detail).toHaveLength(2);
  });
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `npx vitest run src/lib/types.test.ts`
Expected: FAIL — `Type '{ ... }' is not assignable to type 'Exhibit'` (bidang `period` tidak dikenal)

- [ ] **Step 3: Implement type fields**

Pada `src/lib/types.ts`, ganti `Exhibit` dengan:

```ts
/** Satu bagian/isi pameran yang bisa dilihat pengunjung. */
export interface Exhibit {
  title: string;
  description: string;
  /** Masa atau tarikh benda, mis. "abad ke-15", "1915". */
  period?: string | null;
  /** Asal perolehan atau daerah benda berasal. */
  origin?: string | null;
  /** Bahan utama, mis. "perunggu", "kayu kemuning". */
  material?: string | null;
  /** Tandai bila benda termasuk andalan museum. */
  highlight?: boolean | null;
}
```

Pada `MuseumImage`, tambahkan sebelum `credit`:

```ts
  /** Masa atau tarikh yang tampak pada foto, mis. "1915", "era 1970-an". */
  period?: string | null;
  /** 2–4 poin ringkas tentang apa yang layak diamati pada foto. */
  detail?: string[] | null;
```

- [ ] **Step 4: Run test to verify it passes**

Run: `npx vitest run src/lib/types.test.ts`
Expected: PASS (2 test)

- [ ] **Step 5: Commit**

```bash
git add src/lib/types.ts src/lib/types.test.ts
git commit -m "feat: tambah bidang kedalaman pada tipe Exhibit dan MuseumImage"
```

---

### Task 2: Tulis properti RDF baru

**Files:**
- Modify: `src/lib/ontology.ts:371-382` (properti Exhibit), `src/lib/ontology.ts:384-398` (properti Image), `src/lib/ontology.ts:668-682` (penulisan blok Exhibit), `src/lib/ontology.ts:640-663` (penulisan blok Image)
- Test: `src/lib/ontology.test.ts` (buat baru)

**Interfaces:**
- Consumes: `Exhibit` dan `MuseumImage` dari Task 1
- Produces: properti RDF `sdp:exhibitPeriod`, `sdp:exhibitOrigin`, `sdp:exhibitMaterial`, `sdp:exhibitHighlight` (xsd:boolean), `sdp:imagePeriod`, `sdp:imageDetail` (string, satu triple per poin); `buildRdf()` menulisnya

- [ ] **Step 1: Write the failing test**

Buat `src/lib/ontology.test.ts`:

```ts
import { describe, it, expect } from "vitest";
import { buildRdf } from "./ontology";
import type { MuseumRecord } from "./types";

const record: MuseumRecord = {
  slug: "museum-uji",
  name: "Museum Uji",
  city: "Banda Aceh",
  province: "Aceh",
  themes: ["etnografi"],
  era: "kolonial",
  establishedYear: 1915,
  address: "Jl. Uji",
  latitude: 5.5,
  longitude: 95.3,
  description: "Deskripsi.",
  imageUrl: null,
  officialUrl: null,
  admissionNote: null,
  chapter: 1,
  verificationStatus: "perlu-verifikasi",
  exhibits: [
    {
      title: "Lonceng",
      description: "Deskripsi panjang.",
      period: "abad ke-15",
      origin: "Kesultanan Pasai",
      material: "perunggu",
      highlight: true,
    },
  ],
  gallery: [
    {
      src: "/images/museums/museum-uji/1.jpg",
      alt: "Foto",
      caption: "Keterangan",
      credit: "Seseorang",
      license: "CC BY-SA 4.0",
      licenseUrl: "https://creativecommons.org/licenses/by-sa/4.0",
      sourceUrl: "https://commons.wikimedia.org/wiki/File:X.jpg",
      period: "1915",
      detail: ["Poin pertama", "Poin kedua"],
    },
  ],
};

describe("buildRdf — kedalaman isi pameran dan foto", () => {
  it("menulis properti kedalaman pada Exhibit", () => {
    const xml = buildRdf([record]);
    expect(xml).toContain('<sdp:exhibitPeriod xml:lang="id">abad ke-15</sdp:exhibitPeriod>');
    expect(xml).toContain(
      '<sdp:exhibitOrigin xml:lang="id">Kesultanan Pasai</sdp:exhibitOrigin>',
    );
    expect(xml).toContain('<sdp:exhibitMaterial xml:lang="id">perunggu</sdp:exhibitMaterial>');
    expect(xml).toContain('<sdp:exhibitHighlight rdf:datatype="http://www.w3.org/2001/XMLSchema#boolean">true</sdp:exhibitHighlight>');
  });

  it("menulis properti kedalaman pada Image", () => {
    const xml = buildRdf([record]);
    expect(xml).toContain('<sdp:imagePeriod xml:lang="id">1915</sdp:imagePeriod>');
  });

  it("menulis satu triple imageDetail per poin", () => {
    const xml = buildRdf([record]);
    const matches = xml.match(/<sdp:imageDetail xml:lang="id">/g) ?? [];
    expect(matches).toHaveLength(2);
  });

  it("tidak menulis properti kedalaman bila bidang kosong", () => {
    const minimal: MuseumRecord = {
      ...record,
      exhibits: [{ title: "Lonceng", description: "Deskripsi." }],
      gallery: [],
    };
    const xml = buildRdf([minimal]);
    expect(xml).not.toContain("sdp:exhibitPeriod");
    expect(xml).not.toContain("sdp:exhibitHighlight");
  });
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `npx vitest run src/lib/ontology.test.ts`
Expected: FAIL — `expect(received).toContain(...)` gagal untuk `sdp:exhibitPeriod`

- [ ] **Step 3: Declare the new datatype properties**

Pada `src/lib/ontology.ts`, setelah blok `datatypeProperty("exhibitDescription", ...)` (sekitar baris 379), tambahkan:

```ts
  lines.push(...datatypeProperty("exhibitPeriod", "Exhibit", `${XSD}string`, "masa atau tarikh benda"));
  lines.push(...datatypeProperty("exhibitOrigin", "Exhibit", `${XSD}string`, "asal benda"));
  lines.push(...datatypeProperty("exhibitMaterial", "Exhibit", `${XSD}string`, "bahan benda"));
  lines.push(
    ...datatypeProperty("exhibitHighlight", "Exhibit", `${XSD}boolean`, "benda andalan"),
  );
```

Setelah `datatypeProperty("imageBackground", ...)` (sekitar baris 387), tambahkan:

```ts
  lines.push(...datatypeProperty("imagePeriod", "Image", `${XSD}string`, "masa atau tarikh foto"));
  lines.push(...datatypeProperty("imageDetail", "Image", `${XSD}string`, "poin pengamatan foto"));
```

- [ ] **Step 4: Emit the new properties in the Exhibit block**

Pada blok penulisan `sdp:Exhibit` (sekitar baris 675), setelah penulisan `exhibitDescription`, tambahkan:

```ts
      if (exhibit.period) {
        lines.push(
          `${INDENT}    <sdp:exhibitPeriod xml:lang="id">${escapeXml(exhibit.period)}</sdp:exhibitPeriod>`,
        );
      }
      if (exhibit.origin) {
        lines.push(
          `${INDENT}    <sdp:exhibitOrigin xml:lang="id">${escapeXml(exhibit.origin)}</sdp:exhibitOrigin>`,
        );
      }
      if (exhibit.material) {
        lines.push(
          `${INDENT}    <sdp:exhibitMaterial xml:lang="id">${escapeXml(exhibit.material)}</sdp:exhibitMaterial>`,
        );
      }
      if (exhibit.highlight) {
        lines.push(
          `${INDENT}    <sdp:exhibitHighlight rdf:datatype="${XSD}boolean">true</sdp:exhibitHighlight>`,
        );
      }
```

- [ ] **Step 5: Emit the new properties in the Image block**

Pada blok penulisan `sdp:Image` (sekitar baris 648, setelah `imageBackground`), tambahkan:

```ts
      if (image.period) {
        lines.push(
          `${INDENT}    <sdp:imagePeriod xml:lang="id">${escapeXml(image.period)}</sdp:imagePeriod>`,
        );
      }
      for (const point of image.detail ?? []) {
        lines.push(
          `${INDENT}    <sdp:imageDetail xml:lang="id">${escapeXml(point)}</sdp:imageDetail>`,
        );
      }
```

- [ ] **Step 6: Run test to verify it passes**

Run: `npx vitest run src/lib/ontology.test.ts`
Expected: PASS (4 test)

- [ ] **Step 7: Commit**

```bash
git add src/lib/ontology.ts src/lib/ontology.test.ts
git commit -m "feat: tulis properti RDF kedalaman pameran dan galeri"
```

---

### Task 3: Tegakkan ambang kedalaman di validator

**Files:**
- Modify: `src/lib/validate.ts:99-122` (blok isi/galeri)
- Test: `src/lib/validate.test.ts` (tambah kasus)

**Interfaces:**
- Consumes: `MuseumRecord` dari Task 1
- Produces: `ValidationIssue` untuk `exhibits` dan `gallery` bila teks lebih pendek dari ambang; konstanta `MIN_EXHIBIT_DESCRIPTION_CHARS = 180` dan `MIN_IMAGE_BACKGROUND_CHARS = 220` diekspor dari `validate.ts`

- [ ] **Step 1: Write the failing test**

Tambahkan ke `src/lib/validate.test.ts` di dalam `describe("validateMuseums", ...)`:

```ts
  it("menandai deskripsi pameran yang terlalu pendek", () => {
    const issues = validateMuseums([
      {
        ...ok,
        exhibits: [{ title: "Lonceng", description: "Terlalu singkat." }],
      },
    ]);
    expect(issues).toContainEqual(
      expect.objectContaining({ field: "exhibits", level: "warning" }),
    );
  });

  it("meloloskan deskripsi pameran yang memenuhi ambang", () => {
    const panjang = "Koleksi ini tercatat sejak awal abad kedua puluh. ".repeat(5);
    const issues = validateMuseums([
      { ...ok, exhibits: [{ title: "Lonceng", description: panjang }] },
    ]);
    expect(issues.filter((i) => i.field === "exhibits")).toHaveLength(0);
  });

  it("menandai foto tanpa bidang detail", () => {
    const issues = validateMuseums([
      {
        ...ok,
        gallery: [
          {
            src: "/images/museums/museum-ok/1.jpg",
            alt: "Foto",
            caption: "Keterangan",
            background: "Latar belakang yang cukup panjang. ".repeat(8),
            credit: "Seseorang",
            license: "CC BY-SA 4.0",
            licenseUrl: null,
            sourceUrl: "https://commons.wikimedia.org/wiki/File:X.jpg",
          },
        ],
      },
    ]);
    expect(issues).toContainEqual(
      expect.objectContaining({ field: "gallery", level: "warning" }),
    );
  });
```

- [ ] **Step 2: Run test to verify it fails**

Run: `npx vitest run src/lib/validate.test.ts`
Expected: FAIL — tiga test baru gagal karena belum ada pemeriksaan panjang teks maupun `detail`

- [ ] **Step 3: Implement the length checks**

Pada `src/lib/validate.ts`, setelah `SUMATRA_BOUNDS`, tambahkan:

```ts
/** Ambang kedalaman teks; di bawah ini isi dianggap masih terlalu tipis. */
export const MIN_EXHIBIT_DESCRIPTION_CHARS = 180;
export const MIN_IMAGE_BACKGROUND_CHARS = 220;
```

Di dalam blok `if (record.history || record.exhibits?.length || record.gallery?.length)`, setelah pemeriksaan `source.url`, tambahkan:

```ts
      for (const [index, exhibit] of (record.exhibits ?? []).entries()) {
        if (!exhibit.title?.trim()) {
          add("exhibits", "error", `Pameran ke-${index + 1} tidak punya judul.`);
        }
        const panjang = exhibit.description?.trim().length ?? 0;
        if (panjang < MIN_EXHIBIT_DESCRIPTION_CHARS) {
          add(
            "exhibits",
            "warning",
            `Pameran ke-${index + 1} ("${exhibit.title}") baru ${panjang} karakter; minimal ${MIN_EXHIBIT_DESCRIPTION_CHARS}.`,
          );
        }
      }
```

Lalu di dalam `for (const [index, image] of (record.gallery ?? []).entries())`, tambahkan di akhir badan loop:

```ts
        const panjangLatar = image.background?.trim().length ?? 0;
        if (panjangLatar < MIN_IMAGE_BACKGROUND_CHARS) {
          add(
            "gallery",
            "warning",
            `Foto ke-${index + 1} latar belakangnya ${panjangLatar} karakter; minimal ${MIN_IMAGE_BACKGROUND_CHARS}.`,
          );
        }
        if (!image.detail?.length) {
          add("gallery", "warning", `Foto ke-${index + 1} belum punya poin pengamatan (detail).`);
        }
```

- [ ] **Step 4: Run test to verify it passes**

Run: `npx vitest run src/lib/validate.test.ts`
Expected: PASS (semua test, termasuk 3 baru)

- [ ] **Step 5: Commit**

```bash
git add src/lib/validate.ts src/lib/validate.test.ts
git commit -m "feat: tegakkan ambang kedalaman isi pameran dan galeri"
```

---

### Task 4: Tarik dan petakan properti baru di kueri

**Files:**
- Modify: `src/lib/queries.ts:281-296` (`museumExhibitsQuery`), `src/lib/queries.ts:298-312` (`museumImagesQuery`), dan fungsi pemetaan rincian di file yang sama
- Test: `src/lib/queries.test.ts` (tambah kasus)

**Interfaces:**
- Consumes: properti RDF dari Task 2
- Produces: `museumExhibitsQuery` mengembalikan kolom `?period ?origin ?material ?highlight`; `museumImagesQuery` mengembalikan `?period ?detail`; `attachMuseumDetail()` mengisi `Exhibit.period/origin/material/highlight` dan `MuseumImage.period/detail`

- [ ] **Step 1: Write the failing test**

Tambahkan ke `src/lib/queries.test.ts`:

```ts
  it("menarik properti kedalaman pada kueri pameran", () => {
    const q = museumExhibitsQuery("museum-uji");
    expect(q).toContain("sdp:exhibitPeriod");
    expect(q).toContain("sdp:exhibitOrigin");
    expect(q).toContain("sdp:exhibitMaterial");
    expect(q).toContain("sdp:exhibitHighlight");
  });

  it("menarik properti kedalaman pada kueri galeri", () => {
    const q = museumImagesQuery("museum-uji");
    expect(q).toContain("sdp:imagePeriod");
    expect(q).toContain("sdp:imageDetail");
  });
```

- [ ] **Step 2: Run test to verify it fails**

Run: `npx vitest run src/lib/queries.test.ts`
Expected: FAIL — kueri belum memuat `sdp:exhibitPeriod`

- [ ] **Step 3: Extend both queries**

Ganti `museumExhibitsQuery` dengan:

```ts
export function museumExhibitsQuery(slug: string): string {
  return `${PREFIXES}
SELECT ?index ?title ?description ?period ?origin ?material ?highlight
WHERE {
  ${museumIri(slug)} sdp:hasExhibit ?node .
  ?node sdp:exhibitIndex ?index ;
        sdp:exhibitTitle ?title .
  OPTIONAL { ?node sdp:exhibitDescription ?description . }
  OPTIONAL { ?node sdp:exhibitPeriod ?period . }
  OPTIONAL { ?node sdp:exhibitOrigin ?origin . }
  OPTIONAL { ?node sdp:exhibitMaterial ?material . }
  OPTIONAL { ?node sdp:exhibitHighlight ?highlight . }
}
ORDER BY ?index
`;
}
```

Ganti baris `SELECT` pada `museumImagesQuery` dan tambahkan OPTIONAL baru:

```ts
SELECT ?index ?src ?title ?background ?detail ?period ?alt ?caption ?credit ?license ?licenseUrl ?sourceUrl
```

```ts
  OPTIONAL { ?node sdp:imageDetail ?detail . }
  OPTIONAL { ?node sdp:imagePeriod ?period . }
```

- [ ] **Step 4: Update the mapping functions**

Pada fungsi pemetaan pameran di `queries.ts`, saat membangun objek `Exhibit`, tambahkan:

```ts
      period: row.period,
      origin: row.origin,
      material: row.material,
      highlight: row.highlight === "true" || row.highlight === true,
```

Pada fungsi pemetaan foto, tambahkan:

```ts
      period: row.period,
      detail: detailPoin,
```

di mana `detailPoin` dikumpulkan sebelum pemetaan dengan cara mengelompokkan baris ber-`index` sama:

```ts
    const detailByIndex = new Map<string, string[]>();
    for (const row of rowsFoto) {
      if (typeof row.detail !== "string") continue;
      const key = String(row.index);
      const daftar = detailByIndex.get(key) ?? [];
      if (!daftar.includes(row.detail)) daftar.push(row.detail);
      detailByIndex.set(key, daftar);
    }
```

- [ ] **Step 5: Run test to verify it passes**

Run: `npx vitest run src/lib/queries.test.ts`
Expected: PASS (termasuk 2 test baru)

- [ ] **Step 6: Commit**

```bash
git add src/lib/queries.ts src/lib/queries.test.ts
git commit -m "feat: tarik properti kedalaman pameran dan galeri dari graf"
```

---

### Task 5: Tampilkan kedalaman di antarmuka

**Files:**
- Modify: `src/components/ExhibitList.tsx` (seluruh badan), `src/components/MuseumGallery.tsx:37-72` (figcaption)
- Test: verifikasi visual lewat `npm run build`

**Interfaces:**
- Consumes: `Exhibit` dan `MuseumImage` hasil Task 4
- Produces: tidak ada (komponen daun)

- [ ] **Step 1: Rewrite ExhibitList with metadata row**

Ganti badan `ExhibitList` sehingga setiap item menampilkan judul, deretan metadata (`period` · `origin` · `material`), deskripsi, dan penanda "Andalan" bila `highlight` benar:

```tsx
const meta = [exhibit.period, exhibit.origin, exhibit.material]
  .filter(Boolean)
  .join(" · ");
```

Penanda andalan memakai `<span className="chip">Andalan</span>` yang sudah ada di sistem desain.

- [ ] **Step 2: Rewrite the gallery figcaption detail list**

Pada `MuseumGallery`, setelah paragraf `background`, tambahkan:

```tsx
{image.detail && image.detail.length > 0 && (
  <ul className="m-0 p-0 list-none mt-1 space-y-1 text-sm text-[--ink-soft]">
    {image.detail.map((point) => (
      <li key={point} className="flex gap-2">
        <span aria-hidden className="text-[--ink-faint]">—</span>
        <span>{point}</span>
      </li>
    ))}
  </ul>
)}
```

Dan tampilkan `image.period` di samping label "Foto NN".

- [ ] **Step 3: Verify the build**

Run: `npm run build`
Expected: build sukses, tidak ada error TypeScript

- [ ] **Step 4: Commit**

```bash
git add src/components/ExhibitList.tsx src/components/MuseumGallery.tsx
git commit -m "feat: tampilkan kedalaman isi pameran dan poin pengamatan galeri"
```

---

### Task 6: Tulis ulang isi data per museum

**Files:**
- Modify: `data/museums.json` (bidang `exhibits`, `gallery`, `sources` per museum)

**Interfaces:**
- Consumes: tipe dari Task 1, ambang dari Task 3
- Produces: `data/museums.json` yang lolos `npm run check:rdf` tanpa warning kedalaman

Dikerjakan **per provinsi**, satu commit per provinsi, urutan bab 1→7:

- [ ] **Step 1: Bab I — Aceh (4 museum)**

Untuk 4 museum: set `history` minimal 3 paragraf; `exhibits` minimal 4 item dengan `description` ≥180 karakter dan `period`/`origin`/`material` terisi bila sumber mendukung; `gallery` tiap foto ber-`background` ≥220 karakter dan `detail` 2–4 poin; `sources` ditambah ke minimal 2.

Run: `npm run check:rdf`
Expected: tidak ada error; warning `exhibits`/`gallery` nol untuk 4 museum ini

```bash
git add data/museums.json
git commit -m "data: perdalam isi pameran dan galeri Bab I (Aceh)"
```

- [ ] **Step 2: Bab II — Sumatera Utara (5 museum)**

Sama seperti Step 1 untuk museum ber-`chapter: 2`.

Run: `npm run check:rdf`
Expected: warning kedalaman nol untuk 5 museum ini

```bash
git add data/museums.json
git commit -m "data: perdalam isi pameran dan galeri Bab II (Sumatera Utara)"
```

- [ ] **Step 3: Bab III — Riau/Kepulauan Riau (4 museum)**

Sama seperti Step 1 untuk museum ber-`chapter: 3`.

```bash
git add data/museums.json
git commit -m "data: perdalam isi pameran dan galeri Bab III (Melayu)"
```

- [ ] **Step 4: Bab IV — Sumatera Barat (4 museum)**

Sama seperti Step 1 untuk museum ber-`chapter: 4`.

```bash
git add data/museums.json
git commit -m "data: perdalam isi pameran dan galeri Bab IV (Sumatera Barat)"
```

- [ ] **Step 5: Bab V — Jambi/Bengkulu (4 museum)**

Sama seperti Step 1 untuk museum ber-`chapter: 5`.

```bash
git add data/museums.json
git commit -m "data: perdalam isi pameran dan galeri Bab V (Jambi-Bengkulu)"
```

- [ ] **Step 6: Bab VI — Sumatera Selatan/Bangka Belitung (4 museum)**

Sama seperti Step 1 untuk museum ber-`chapter: 6`.

```bash
git add data/museums.json
git commit -m "data: perdalam isi pameran dan galeri Bab VI (Sumatera Selatan)"
```

- [ ] **Step 7: Bab VII — Lampung (3 museum)**

Sama seperti Step 1 untuk museum ber-`chapter: 7`. Museum Negeri Lampung dan Ketransmigrasian hanya punya 1 foto — tambahkan `detail` 3–4 poin pada foto tunggal itu supaya tetap terasa penuh.

```bash
git add data/museums.json
git commit -m "data: perdalam isi pameran dan galeri Bab VII (Lampung)"
```

- [ ] **Step 8: Verifikasi menyeluruh**

Run: `npm run check:rdf`
Expected: `error : 0`, dan tidak ada baris `[WARN]` untuk `exhibits:` maupun `gallery:` terkait ambang kedalaman

Run: `npm test`
Expected: semua test lulus

---

### Task 7: Tambah foto galeri dari Wikimedia Commons

**Files:**
- Modify: `data/museums.json` (bidang `gallery`), `public/images/museums/<slug>/` (berkas gambar baru), `data/gallery-notes.json` (catatan untuk foto baru)

**Interfaces:**
- Consumes: `MuseumImage` dari Task 1
- Produces: tiap museum minimal 3 foto, kecuali yang Commons-nya terbukti tidak punya foto layak (didokumentasikan di commit)

- [ ] **Step 1: Cari kandidat foto per museum**

Untuk setiap museum, cari di Wikimedia Commons. Simpan hanya foto dengan lisensi CC0/CC BY/CC BY-SA/domain publik dan resolusi sisi terpanjang ≥1000 px.

- [ ] **Step 2: Unduh dan catat**

Unduh ke `public/images/museums/<slug>/<n>.jpg`, lalu isi `gallery` dengan `src`, `alt`, `caption`, `title`, `background` (≥220 karakter), `detail` (2–4 poin), `period`, `credit`, `license`, `licenseUrl`, `sourceUrl`. Catatan panjang untuk foto baru masuk `data/gallery-notes.json`.

- [ ] **Step 3: Verifikasi**

Run: `npm run check:rdf`
Expected: tidak ada error `gallery`; setiap foto baru punya `license`, `licenseUrl`, dan `sourceUrl` berisi URL http(s)

Run: `npm run generate:rdf && npm run upload:fuseki`
Expected: unggah sukses

- [ ] **Step 4: Commit**

```bash
git add data/museums.json data/gallery-notes.json public/images/museums
git commit -m "data: tambah foto Commons berlisensi jelas untuk galeri"
```

---

### Task 8: Perbarui dokumentasi

**Files:**
- Modify: `README.md` (bagian "Catatan museum: sejarah, pameran, dan galeri", bagian "Ontologi singkat")

**Interfaces:**
- Consumes: semua task sebelumnya
- Produces: tidak ada

- [ ] **Step 1: Catat properti baru di README**

Pada tabel "Catatan museum", tambahkan baris untuk `exhibitPeriod`/`exhibitOrigin`/`exhibitMaterial`/`exhibitHighlight` dan `imagePeriod`/`imageDetail`. Pada bagian Ontologi singkat, tambahkan keenam properti itu ke daftar datatype property.

- [ ] **Step 2: Catat ambang validator**

Pada bagian "Pemeriksaan data", sebutkan bahwa `npm run check:rdf` memberi peringatan bila deskripsi pameran <180 karakter atau latar foto <220 karakter.

- [ ] **Step 3: Verifikasi**

Run: `npm run check:rdf && npm test && npm run build`
Expected: ketiganya sukses

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "docs: catat properti kedalaman dan ambang validator"
```

---

## Review Focus

Hal-hal yang tidak diuji test tetapi paling mungkin menggigit pengguna:

1. **Museum dengan satu foto** — Museum Lampung, Ketransmigrasian, Linggam Cahaya, Kereta Api Sawahlunto punya 1 foto; galeri tidak boleh tampak kosong atau memakai `detail` kosong sehingga seksi galeri hanya satu kartu sendirian tanpa konteks.
2. **Museum tanpa `material`/`period` karena sumber tidak menyebut** — metadata tidak boleh dirender sebagai baris kosong atau pemisah `·` menggantung; diuji lewat `meta` yang difilter.
3. **Fuseki mati saat halaman museum dibuka** — halaman harus tetap menampilkan pesan "Basis data tidak terjangkau", bukan crash karena `period`/`detail` undefined.
4. **`highlight` sebagai boolean vs string** — SPARQL mengembalikan `"true"` sebagai string; pemetaan harus menerima keduanya agar penanda Andalan tidak hilang.
5. **Teks dengan karakter `&`, `<`, `>` pada judul pameran** — generator RDF harus meng-escape; diuji di Task 2 lewat `escapeXml`.

## Self-Review

**1. Spec coverage:** Kedalaman isi pameran → Task 1–5. Kedalaman galeri → Task 1–5. Penambahan foto → Task 7. Dokumentasi → Task 8. Ambang anti-regresi → Task 3. ✅
**2. Step scan:** Setiap step punya perintah atau kode konkret. Task 6 sengaja berupa instruksi per-bab dengan ambang eksak dari Task 3, bukan transkrip 28 museum. ✅
**3. Type consistency:** `period`/`origin`/`material`/`highlight` pada `Exhibit`, `period`/`detail` pada `MuseumImage` — nama sama dipakai di Task 1, 2, 4, 5. Konstanta `MIN_EXHIBIT_DESCRIPTION_CHARS`/`MIN_IMAGE_BACKGROUND_CHARS` konsisten di Task 3. ✅
**4. Review Focus:** 5 baris, masing-masing punya test atau pemeriksaan di task pemiliknya (2 & 4 di Task 5/4, 1 di Task 6 Step 7, 3 di Task 5 Step 3 lewat build, 5 di Task 2). ✅
**5. Proportion:** Plan lebih pendek dari hasil akhirnya (28 museum × ~5 pameran × 3 kalimat) — isi data tidak ditranskrip, hanya ambang dan bentuknya. ✅
