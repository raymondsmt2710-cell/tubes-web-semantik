# Museum Sumatera Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Membangun situs "Museum Sumatera" — pameran digital berbab tentang museum di Pulau Sumatera dengan pencarian data di atas RDF + SPARQL (Apache Jena Fuseki).

**Architecture:** Next.js 16 App Router (TypeScript, Tailwind v4, Zustand) sebagai satu aplikasi. Data museum dikelola tangan di `data/museums.json`, digenerate menjadi RDF/XML oleh skrip Node, di-upload ke Fuseki, lalu dibaca kembali oleh route handler `app/api/*` melalui klien SPARQL (`lib/sparql.ts`). Penyaringan dieksekusi di SPARQL; JS hanya memeringkat kandidat terbatas dan menghitung "benang merah" dari relasi graf.

**Tech Stack:** Next.js 16, React 19, TypeScript 5, Tailwind CSS 4, Zustand 5, Vitest, Apache Jena Fuseki (endpoint eksternal), bun sebagai manajer paket.

**Spec:** `docs/superpowers/specs/2026-02-16-museum-sumatera-design.md`

## Global Constraints

- Manajer paket: **bun**. Semua perintah memakai `bun`, bukan `npm`.
- Versi: `next@16`, `react@19`, `react-dom@19`, `typescript@5`, `tailwindcss@4`, `zustand@5`, `vitest` (dev).
- Bahasa UI: **Bahasa Indonesia**. Label RDF `xml:lang="id"`.
- Prefix RDF: `sdp:` = `https://museumsumatera.id/ontology#`, `res:` = `https://museumsumatera.id/resource/`.
- Env: `FUSEKI_ENDPOINT` (wajib, contoh `http://localhost:3030/museum/query`), `FUSEKI_UPDATE` (opsional, contoh `http://localhost:3030/museum/data`).
- **Satu properti = satu arti.** Dilarang memodelkan tingkat kesulitan/kondisi dengan properti bernama status ganda.
- **Tidak ada filter yang dijalankan di JavaScript.** Provinsi/tema/era/minYear/urutan dieksekusi di SPARQL.
- Pencocokan string (`q`) di JS hanya atas hasil ber-`LIMIT 300`.
- Jumlah museum: **28**, seluruhnya `verificationStatus: "perlu-verifikasi"` pada rilis pertama.
- Semua teks yang tampil ke pengguna ditulis dalam Bahasa Indonesia baku.

## Review Focus

Hal-hal yang tidak diuji langsung oleh test sebuah task, tetapi paling mungkin menggigit pengguna:

1. **Fuseki mati / salah nama dataset.** Pengguna menavigasi bab lalu semua halaman jadi error putih. Diharapkan: setiap halaman yang bergantung pada Fuseki menampilkan pesan ramah ("Tidak dapat terhubung ke basis data museum") + tautan ke `/katalog` dengan data cadangan dari `museums.json` bila memungkinkan, bukan layar kosong atau stack trace.
2. **Museum tanpa `establishedYear` (null).** Filter `minYear` dan pengurutan tahun harus tetap berfungsi, museum tanpa tahun tidak boleh hilang dari katalog saat filter tahun aktif — ia harus tersaring secara wajar (tidak masuk hasil `minYear>0`) tanpa error.
3. **Nama museum dengan karakter non-ASCII dan spasi** (mis. "Museum Negeri Provinsi Riau"). Slug dipakai di URL; museum harus tetap bisa dibuka dari tautan mana pun, termasuk URL yang ter-encode.
4. **Bab yang tidak ditemukan** (`/jelajah/99` atau `/jelajah/abc`). Diharapkan halaman "Bab tidak ditemukan" dengan tautan ke sampul, bukan crash.
5. **RDF hasil generate gagal parse / duplikat `rdf:about`.** Dua museum ber-slug sama akan merusak dataset sehingga seluruh situs kosong. Generator harus gagal keras (`exit 1`) dengan pesan yang menyebut slug bentrok, bukan diam-diam menulis RDF rusak.

---

### Task 1: Fondasi proyek, tooling, dan skrip paket

**Files:**
- Create: `package.json`, `next.config.ts`, `tsconfig.json`, `postcss.config.mjs`, `.gitignore`, `.env.example`, `next-env.d.ts` (auto)
- Create: `vitest.config.ts`, `test/setup.ts`
- Create: `src/app/layout.tsx`, `src/app/globals.css`, `src/app/page.tsx` (placeholder sementara, diganti Task 7)
- Modify: `README.md`

**Interfaces:**
- Consumes: —
- Produces: skrip bun `dev`, `build`, `start`, `test`, `generate:rdf`, `check:rdf`; alias TS `@/*` → `./src/*`; variabel ter-type `FUSEKI_ENDPOINT`, `FUSEKI_UPDATE`.

- [ ] **Step 1: Buat `package.json` dengan skrip lengkap**

```json
{
  "name": "museum-sumatera",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "test": "vitest run",
    "generate:rdf": "bun run scripts/generate-rdf.ts",
    "check:rdf": "bun run scripts/check-rdf.ts",
    "upload:fuseki": "bun run scripts/upload-fuseki.ts"
  },
  "dependencies": {
    "next": "16.0.6",
    "react": "19.2.0",
    "react-dom": "19.2.0",
    "zustand": "^5.0.9"
  },
  "devDependencies": {
    "@tailwindcss/postcss": "^4",
    "@types/node": "^20",
    "@types/react": "^19",
    "@types/react-dom": "^19",
    "tailwindcss": "^4",
    "typescript": "^5",
    "vitest": "^2.1.0"
  }
}
```

- [ ] **Step 2: Pasang dependensi**

Run: `bun install`
Expected: `bun.lock` terbentuk, tanpa error.

- [ ] **Step 3: Tulis `tsconfig.json` dengan alias yang benar**

Alias `@/*` → `./src/*` **dan** `@data/*` → `./data/*`, dengan `include` menyertakan `scripts/**/*.ts` sehingga skrip generator ikut ter-typecheck.

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": { "@/*": ["./src/*"], "@data/*": ["./data/*"] }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

- [ ] **Step 4: Tulis konfigurasi pendukung**

`next.config.ts`:
```ts
import type { NextConfig } from "next";
const nextConfig: NextConfig = {};
export default nextConfig;
```

`postcss.config.mjs`:
```js
export default { plugins: { "@tailwindcss/postcss": {} } };
```

`vitest.config.ts`:
```ts
import { defineConfig } from "vitest/config";
export default defineConfig({
  test: { environment: "node", include: ["src/**/*.test.ts", "scripts/**/*.test.ts"] },
  resolve: { alias: { "@": new URL("./src/", import.meta.url).pathname, "@data": new URL("./data/", import.meta.url).pathname } },
});
```

`.env.example`:
```
# Endpoint SPARQL query (wajib). Sesuaikan nama dataset dengan milik Anda.
FUSEKI_ENDPOINT=http://localhost:3030/museum/query
# Endpoint Graph Store / update (opsional, hanya untuk skrip upload)
FUSEKI_UPDATE=http://localhost:3030/museum/data
```

`.gitignore`: tambahkan `.env`, `.next/`, `node_modules/`, `.superpowers/`.

- [ ] **Step 5: Tulis `globals.css` dengan token visual "Arsip Kolonial"**

Token wajib (dipakai semua task UI berikutnya): `--paper #f3ece0`, `--paper-2 #eae0cf`, `--ink #2f2a24`, `--ink-soft #6b5f4d`, `--rule #d8cdb8`, `--accent #0f766e` (teal tipis). Font: `--font-serif: Georgia, 'Times New Roman', serif`, `--font-sans: ui-sans-serif, system-ui, sans-serif`. Sertakan kelas utilitas `.rule` (garis 1px `--rule`), `.label` (uppercase, letter-spacing .1em, 11px, `--ink-soft`), dan `.paper-texture` (gradien radial halus, tanpa gambar eksternal).

- [ ] **Step 6: Tulis `src/app/layout.tsx`**

Metadata: `title: "Museum Sumatera — Pameran Digital"`, `description: "Jelajahi museum di Pulau Sumatera, dari Aceh hingga Lampung."`, `lang="id"`, memuat `globals.css`, memasang `<footer>` berisi disclaimer: *"Data museum disusun untuk keperluan pembelajaran dan belum seluruhnya terverifikasi."*

- [ ] **Step 7: Buat halaman placeholder agar build lolos**

`src/app/page.tsx` mengembalikan `<h1>Museum Sumatera</h1>`. Ini akan diganti penuh di Task 7.

- [ ] **Step 8: Verifikasi build & test runner**

Run: `bun run build` → Expected: build sukses, halaman `/` ter-render.
Run: `bun run test` → Expected: "No test files found" dengan exit 0 (belum ada test; Vitest dikonfigurasi `passWithNoTests` bila perlu).

- [ ] **Step 9: Commit**

```bash
git add -A
git commit -m "chore: scaffold Next.js project with tooling and design tokens"
```

---

### Task 2: Pembungkus SPARQL dan tipe domain

**Files:**
- Create: `src/lib/types.ts`, `src/lib/sparql.ts`, `src/lib/sparql.test.ts`

**Interfaces:**
- Consumes: `FUSEKI_ENDPOINT` dari env.
- Produces:
  - `type SparqlBinding = Record<string, { type: string; value: string } | undefined>`
  - `interface SparqlResults { results: { bindings: SparqlBinding[] } }`
  - `async function runSelect(query: string): Promise<SparqlBinding[]>` — POST form `query=…`, header `Accept: application/sparql-results+json`; melempar `FusekiError` bila non-2xx atau body bukan JSON.
  - `class FusekiError extends Error { status?: number; detail?: string }`
  - Tipe DTO: `MuseumDTO`, `ChapterDTO`, `RelatedDTO`, `SearchResponse`, `CatalogResponse` (definisi persis di Step 1).

- [ ] **Step 1: Tulis test yang gagal untuk `runSelect`**

`src/lib/sparql.test.ts`:
```ts
import { describe, it, expect, vi, afterEach } from "vitest";
import { runSelect, FusekiError } from "./sparql";

afterEach(() => vi.unstubAllGlobals());

describe("runSelect", () => {
  it("mengembalikan bindings dari respons JSON Fuseki", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => new Response(
      JSON.stringify({ results: { bindings: [{ museum: { type: "uri", value: "http://x/1" } }] } }),
      { status: 200, headers: { "content-type": "application/sparql-results+json" } },
    )));
    const rows = await runSelect("SELECT * WHERE { ?s ?p ?o }");
    expect(rows).toHaveLength(1);
    expect(rows[0].museum?.value).toBe("http://x/1");
  });

  it("melempar FusekiError saat endpoint membalas 500", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => new Response("boom", { status: 500 })));
    await expect(runSelect("SELECT * WHERE { }")).rejects.toBeInstanceOf(FusekiError);
  });

  it("mengirim query sebagai form-urlencoded dan meminta hasil JSON", async () => {
    const spy = vi.fn(async () => new Response(JSON.stringify({ results: { bindings: [] } }), { status: 200 }));
    vi.stubGlobal("fetch", spy);
    await runSelect("SELECT ?s WHERE { ?s a ?o }");
    const [url, init] = spy.mock.calls[0] as any;
    expect(String(url)).toContain("FUSEKI_ENDPOINT_VALUE_OR_LOCALHOST");
    expect(init.method).toBe("POST");
    expect(init.headers.Accept).toBe("application/sparql-results+json");
    expect(String(init.body)).toBe("query=SELECT%20%3Fs%20WHERE%20%7B%20%3Fs%20a%20%3Fo%20%7D");
  });
});
```

- [ ] **Step 2: Jalankan test, pastikan gagal**

Run: `bun run test src/lib/sparql.test.ts`
Expected: FAIL — `sparql.ts` belum ada.

- [ ] **Step 3: Implementasi `src/lib/types.ts` dan `src/lib/sparql.ts`**

`src/lib/types.ts` mendefinisikan:
```ts
export interface MuseumDTO {
  uri: string; slug: string; name: string;
  province: string | null; city: string | null;
  themes: string[]; era: string | null;
  establishedYear: number | null; description: string | null;
  imageUrl: string | null; officialUrl: string | null;
  address: string | null; latitude: number | null; longitude: number | null;
  admissionNote: string | null; verificationStatus: "terverifikasi" | "perlu-verifikasi";
  chapterIndex: number | null; chapterTitle: string | null;
}
export interface ChapterDTO { index: number; slug: string; label: string; title: string; museumCount: number }
export interface RelatedDTO { uri: string; slug: string; name: string; city: string | null; province: string | null; themes: string[]; score: number; reason: string }
export const FALLBACK_IMAGE = "/images/placeholder-museum.svg";
export function toSlug(name: string): string;   // lower, non-alfanumerik → "-", trim "-"
export function yearLabel(y: number | null): string; // null → "Tahun tidak tercatat"
```

`src/lib/sparql.ts` memakai `process.env.FUSEKI_ENDPOINT ?? "http://localhost:3030/museum/query"`.

- [ ] **Step 4: Jalankan test, pastikan lulus**

Run: `bun run test src/lib/sparql.test.ts`
Expected: PASS (3 test).

- [ ] **Step 5: Commit**

```bash
git add src/lib
git commit -m "feat: add SPARQL client and domain types"
```

---

### Task 3: Data museum dan generator RDF

**Files:**
- Create: `data/museums.json`, `data/_.json` tidak diperlukan
- Create: `src/lib/ontology.ts`, `src/lib/ontology.test.ts`
- Create: `scripts/generate-rdf.ts`, `scripts/generate-rdf.test.ts`
- Create: `ontology/museum-sumatera.ttl`

**Interfaces:**
- Consumes: `toSlug` (Task 2).
- Produces:
  - `interface MuseumRecord` (bentuk `museums.json`) — lihat Step 1.
  - `function escapeXml(s: string): string` di `src/lib/ontology.ts`
  - `function buildRdf(museums: MuseumRecord[]): string` di `src/lib/ontology.ts` — mengembalikan dokumen RDF/XML lengkap.
  - `scripts/generate-rdf.ts` menulis `data/museum-sumatera.rdf`.

- [ ] **Step 1: Tulis `data/museums.json` berisi 28 museum**

Setiap entri berbentuk:
```json
{
  "slug": "museum-negeri-aceh",
  "name": "Museum Negeri Aceh",
  "city": "Banda Aceh",
  "province": "Aceh",
  "themes": ["etnografi", "perjuangan"],
  "era": "kolonial",
  "establishedYear": 1915,
  "address": "Jl. Sultan Mahmudsyah, Banda Aceh",
  "latitude": 5.5483, "longitude": 95.3238,
  "description": "…2–3 kalimat bahasa Indonesia…",
  "imageUrl": null,
  "officialUrl": null,
  "admissionNote": null,
  "chapter": 1,
  "verificationStatus": "perlu-verifikasi"
}
```

Sebaran wajib: 28 entri, minimal **8 provinsi** berbeda, ketujuh bab (`chapter` 1–7) masing-masing minimal 3 museum, setiap `themes` berisi 1–3 nilai dari himpunan `themes` resmi, `era` salah satu dari `kolonial`, `kemerdekaan`, `modern`, `pra-kolonial`. Gunakan museum yang benar-benar ada bila Anda yakin; bila ragu, pakai museum yang dikenal publik dan tetap tandai `perlu-verifikasi`.

- [ ] **Step 2: Tulis `ontology/museum-sumatera.ttl`**

Deklarasikan prefix `sdp:`, `rdfs:`, `owl:`, `xsd:`, `geo:` dan kelas `sdp:Museum`, `sdp:Province`, `sdp:City`, `sdp:Theme`, `sdp:Era`, `sdp:Chapter`, `sdp:Collection`; object property `locatedInProvince`, `locatedInCity`, `partOfProvince`, `hasTheme`, `hasEra`, `hasCollection`, `chapter` (dengan `rdfs:range` yang tepat); datatype property `establishedYear`, `description`, `imageUrl`, `officialUrl`, `address`, `latitude`, `longitude`, `admissionNote`, `verificationStatus`, `chapterIndex`. Setiap properti wajib punya `rdfs:domain` dan `rdfs:range`.

- [ ] **Step 3: Tulis test generator yang gagal**

`scripts/generate-rdf.test.ts` memuat `data/museums.json` dan menguji `buildRdf`:
```ts
it("menghasilkan RDF/XML dengan root rdf:RDF dan satu sdp:Museum per entri", () => { … countOccurrences("<sdp:Museum ") === 28 });
it("meng-escape karakter XML berbahaya", () => { const out = buildRdf([{...base, name: 'Museum "A" & <B>'} as any); expect(out).toContain("&quot;A&quot; &amp; &lt;B&gt;"); expect(out).not.toContain('<B>'); });
it("melempar error yang menyebut slug bila ada slug duplikat", () => { expect(() => buildRdf([a, {...a}])).toThrow(/duplikat.*museum-negeri-aceh/i); });
it("menolak museum tanpa provinsi, tema, atau bab", () => { expect(() => buildRdf([{...a, province: ""}])).toThrow(/provinsi/i); });
it("menulis establishedYear sebagai xsd:gYear hanya bila terisi", () => { … });
```

- [ ] **Step 4: Jalankan test, pastikan gagal**

Run: `bun run test scripts/generate-rdf.test.ts`
Expected: FAIL — `buildRdf` belum ada.

- [ ] **Step 5: Implementasi `src/lib/ontology.ts`**

`buildRdf` memvalidasi dulu (gagal keras sebelum menulis satu byte), lalu membangun RDF/XML: deklarasi kelas & properti, instance `Province`/`City`/`Theme`/`Era`/`Chapter` yang unik (dihitung dengan `Set`), lalu instance `Museum`. URI museum: `res:museum/{slug}`.

- [ ] **Step 6: Implementasi `scripts/generate-rdf.ts`**

Membaca `data/museums.json` via `Bun.file`/`readFileSync`, memanggil `buildRdf`, menulis `data/museum-sumatera.rdf`, mencetak ringkasan: jumlah museum, provinsi, tema, dan bab. Exit 1 dengan pesan jelas bila validasi gagal.

- [ ] **Step 7: Jalankan test dan generator**

Run: `bun run test scripts/generate-rdf.test.ts` → Expected: PASS (5 test).
Run: `bun run generate:rdf` → Expected: file `data/museum-sumatera.rdf` ada, ringkasan "28 museum, ≥8 provinsi, 7 bab".

- [ ] **Step 8: Commit**

```bash
git add data ontology scripts src/lib
git commit -m "feat: add 28 museum records, ontology, and RDF generator"
```

---

### Task 4: Pemeriksa data & pengunggah Fuseki

**Files:**
- Create: `scripts/check-rdf.ts`, `scripts/check-rdf.test.ts`, `scripts/upload-fuseki.ts`
- Create: `src/lib/validate.ts`, `src/lib/validate.test.ts`

**Interfaces:**
- Consumes: `MuseumRecord` dari Task 3.
- Produces:
  - `interface ValidationIssue { slug: string; field: string; message: string }`
  - `function validateMuseums(rows: MuseumRecord[]): ValidationIssue[]` di `src/lib/validate.ts`
  - `scripts/check-rdf.ts` mencetak tabel isu dan exit 1 bila ada isu tingkat `error`.

- [ ] **Step 1: Tulis test `validateMuseums` yang gagal**

```ts
it("menandai museum tanpa provinsi sebagai error", () => { expect(validateMuseums([{...ok, province: ""}])).toContainEqual(expect.objectContaining({ field: "province" })); });
it("menandai provinsi di luar daftar resmi sebagai error", () => { expect(validateMuseums([{...ok, province: "Jawa Barat"}]).some(i => i.field === "province")).toBe(true); });
it("menerima establishedYear null tanpa isu", () => { expect(validateMuseums([{...ok, establishedYear: null}])).toHaveLength(0); });
it("menandai bab di luar rentang 1..7 sebagai error", () => { expect(validateMuseums([{...ok, chapter: 9}]).some(i => i.field === "chapter")).toBe(true); });
it("menandai koordinat di luar Sumatera sebagai error", () => { /* lat 5.5 lon 95.3 lolos; lat -7.0 lon 110.0 error */ });
it("memperingatkan museum yang belum terverifikasi", () => { expect(validateMuseums([{...ok, verificationStatus: "perlu-verifikasi"}])[0].message).toMatch(/verifikasi/i); });
```

Daftar provinsi resmi (dipakai validasi dan filter UI): `Aceh`, `Sumatera Utara`, `Sumatera Barat`, `Riau`, `Kepulauan Riau`, `Jambi`, `Bengkulu`, `Sumatera Selatan`, `Bangka Belitung`, `Lampung`. Rentang kotak Sumatera: lat `-6.5..6.5`, lon `94..107.5`.

- [ ] **Step 2: Jalankan test, pastikan gagal**

Run: `bun run test src/lib/validate.test.ts` → Expected: FAIL.

- [ ] **Step 3: Implementasi `src/lib/validate.ts`, `scripts/check-rdf.ts`, `scripts/upload-fuseki.ts`**

`upload-fuseki.ts` melakukan `PUT` ke `FUSEKI_UPDATE` dengan `Content-Type: application/rdf+xml` dan isi file RDF, setelah membersihkan graph (`DELETE … WHERE { ?s ?p ?o }` via `POST` ke `FUSEKI_UPDATE?graph=default`). Bila `FUSEKI_UPDATE` tidak diisi, cetak instruksi manual (upload lewat UI Fuseki) lalu exit 2.

- [ ] **Step 4: Jalankan test dan pemeriksa**

Run: `bun run test src/lib/validate.test.ts` → Expected: PASS (6 test).
Run: `bun run check:rdf` → Expected: daftar peringatan verifikasi untuk 28 museum, exit 0.

- [ ] **Step 5: Commit**

```bash
git add scripts src/lib
git commit -m "feat: add data validation and Fuseki upload scripts"
```

---

### Task 5: Query SPARQL untuk bab dan katalog

**Files:**
- Create: `src/lib/queries.ts`, `src/lib/queries.test.ts`
- Create: `src/app/api/chapters/route.ts`, `src/app/api/search/route.ts`, `src/app/api/search/route.test.ts`

**Interfaces:**
- Consumes: `runSelect`, `MuseumDTO`, `ChapterDTO`.
- Produces:
  - `function chaptersQuery(): string`
  - `function museumsByChapterQuery(chapterIndex: number): string`
  - `function searchCatalogQuery(params: CatalogParams): string` dengan `interface CatalogParams { q?: string; province?: string; theme?: string; era?: string; minYear?: number; sort?: "name"|"year"; order?: "asc"|"desc" }`
  - `function mapMuseumRow(b: SparqlBinding): MuseumDTO` — memakai `GROUP_CONCAT` untuk tema (`SEPARATOR "|"`)
  - Route `GET /api/chapters` → `{ chapters: ChapterDTO[] }`
  - Route `GET /api/search` → `CatalogResponse = { museums: MuseumDTO[]; total: number; ranking?: { slug: string; score: number }[] }`

- [ ] **Step 1: Tulis test query builder yang gagal**

```ts
it("menyisipkan FILTER provinsi ke dalam query, bukan setelahnya", () => {
  const q = searchCatalogQuery({ province: "Aceh" });
  expect(q).toContain('?provinceLabel = "Aceh"');
  expect(q).toContain("LIMIT 300");
});
it("meng-escape tanda kutip pada input provinsi", () => {
  expect(searchCatalogQuery({ province: 'Aceh" OR 1=1' })).toContain('\\"');
});
it("memakai ORDER BY tahun saat sort=year", () => {
  expect(searchCatalogQuery({ sort: "year", order: "desc" })).toMatch(/ORDER BY DESC\(\?year\)/);
});
it("tidak menambahkan filter tema bila kosong", () => {
  expect(searchCatalogQuery({})).not.toContain("hasTheme");
});
```

- [ ] **Step 2: Jalankan test, pastikan gagal**

Run: `bun run test src/lib/queries.test.ts` → Expected: FAIL.

- [ ] **Step 3: Implementasi `src/lib/queries.ts`**

Semua query memakai `PREFIX sdp:`/`res:` dan `OPTIONAL` terpisah untuk setiap properti opsional (provinsi, kota, era, tahun, gambar, url, alamat, koordinat, admissionNote, verifikasi, bab). Tema diambil dengan subquery `GROUP_CONCAT` agar museum multi-tema tidak terduplikasi. `LIMIT 300` selalu ada pada query katalog.

- [ ] **Step 4: Implementasi route `api/chapters` dan `api/search`**

`api/search`: bila `q` kosong → kembalikan hasil SPARQL apa adanya (`total = museums.length`). Bila `q` ada → jalankan query yang sama (tetap berfilter SPARQL), lalu ranking memakai `rankMuseums` dari Task 6 terhadap hasil tersebut. Bila `FusekiError` → balas `502` dengan `{ error: "Tidak dapat terhubung ke basis data museum.", detail }`.

- [ ] **Step 5: Tulis test route handler dengan Fuseki di-mock**

```ts
it("mengembalikan 502 dengan pesan bahasa Indonesia saat Fuseki mati", async () => {
  vi.stubGlobal("fetch", vi.fn(async () => new Response("down", { status: 503 })));
  const res = await GET(new Request("http://localhost/api/search?q=aceh"));
  expect(res.status).toBe(502);
  expect((await res.json()).error).toMatch(/Tidak dapat terhubung/);
});
it("meneruskan filter provinsi ke query SPARQL", async () => { /* spy: body mengandung Aceh */ });
```

- [ ] **Step 6: Jalankan semua test**

Run: `bun run test` → Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add src/lib src/app/api
git commit -m "feat: add SPARQL query builders and catalog/chapter API routes"
```

---

### Task 6: Peringkat pencarian dan benang merah

**Files:**
- Create: `src/lib/ranking.ts`, `src/lib/ranking.test.ts`
- Create: `src/lib/related.ts`, `src/lib/related.test.ts`
- Create: `src/app/api/museum/route.ts`, `src/app/api/museum/route.test.ts`

**Interfaces:**
- Consumes: `MuseumDTO`, `RelatedDTO`, `rankMuseums` dipakai Task 5 Step 4.
- Produces:
  - `function similarity(query: string, name: string): number`
  - `function rankMuseums<T extends { name: string }>(rows: T[], q: string): { primary: T[]; secondary: T[]; scores: Map<string, number> }` dengan ambang `0.7`.
  - `function scoreRelated(base: MuseumDTO, candidate: MuseumDTO): { score: number; reason: string }` (tema sama +3/tema, kota sama +2, era sama +1, bab ±1 +1)
  - `function pickRelated(base: MuseumDTO, candidates: MuseumDTO[], limit?: number): RelatedDTO[]` — deterministik, tanpa skor 0, default limit 6.
  - Route `GET /api/museum?slug=…` → `{ museum: MuseumDTO; related: RelatedDTO[] }`, `404` + `{ error: "Museum tidak ditemukan." }`.

- [ ] **Step 1: Tulis test ranking yang gagal**

```ts
it("memberi skor 1.0 untuk kecocokan persis tanpa peduli kapitalisasi", () => { expect(similarity("semeru","Semeru")).toBe(1); });
it("mengenali akronim", () => { expect(similarity("mnb","Museum Negeri Bengkulu")).toBeGreaterThanOrEqual(0.85); });
it("memisahkan hasil utama pada ambang 0.7", () => { const r = rankMuseums([{name:"Museum Aceh"},{name:"Gedung Arsip"}], "aceh"); expect(r.primary.map(m=>m.name)).toContain("Museum Aceh"); });
it("tidak membuang hasil saat query kosong", () => { expect(rankMuseums([{name:"A"},{name:"B"}], "").secondary).toHaveLength(2); });
```

- [ ] **Step 2: Jalankan test, pastikan gagal**

Run: `bun run test src/lib/ranking.test.ts` → Expected: FAIL.

- [ ] **Step 3: Implementasi `src/lib/ranking.ts`**

Rumus sesuai spec: exact 1.0 → prefix 0.95 → akronim 0.85 → subsequence `0.7×(len(q)/len(n))` → substring 0.6 → fallback rasio karakter (maks 0.4). Ekspor `similarity` dan `rankMuseums`.

- [ ] **Step 4: Tulis test benang merah yang gagal**

```ts
it("museum dengan tema sama mendapat skor lebih tinggi daripada yang hanya sebaya bab", () => { … });
it("mengembalikan reason yang menyebut alasan dalam bahasa Indonesia", () => { expect(pickRelated(base, [sameTheme])[0].reason).toMatch(/tema/i); });
it("tidak pernah merekomendasikan museum itu sendiri", () => { expect(pickRelated(base, [base]).some(r => r.slug === base.slug)).toBe(false); });
it("deterministik: dua museum berskor sama diurutkan berdasarkan nama", () => { … });
it("menyembunyikan kandidat berskor 0", () => { expect(pickRelated(base, [unrelated])).toHaveLength(0); });
```

- [ ] **Step 5: Implementasi `src/lib/related.ts` dan jalankan test**

Run: `bun run test src/lib/related.test.ts` → Expected: PASS.

- [ ] **Step 6: Implementasi `api/museum` + test route**

Test: `404` untuk slug tak dikenal; `200` dengan `related` terisi untuk slug yang cocok dengan dua museum bertema sama (Fuseki di-mock).

Run: `bun run test` → Expected: PASS semua.

- [ ] **Step 7: Commit**

```bash
git add src/lib src/app/api
git commit -m "feat: add text ranking and graph-derived related museums"
```

---

### Task 7: Sampul dan daftar bab (halaman `/`)

**Files:**
- Create: `src/app/page.tsx` (mengganti placeholder), `src/components/ChapterList.tsx`, `src/components/SearchBox.tsx`
- Create: `src/app/page.test.tsx` (bila memakai React Testing Library; bila tidak, cukup verifikasi manual di Step 4)
- Modify: `src/app/globals.css` bila perlu penyesuaian

**Interfaces:**
- Consumes: `ChapterDTO`, route `/api/chapters`.
- Produces: `SearchBox` dengan prop `{ onSubmit?: (q: string) => void; defaultValue?: string }` yang menavigasi ke `/katalog?q=…`; `ChapterList` dengan prop `{ chapters: ChapterDTO[] }` yang menautkan ke `/jelajah/{index}`.

- [ ] **Step 1: Bangun sampul**

Server Component. Sampul berisi: judul serif besar "Museum Sumatera", subjudul "Perjalanan dari Aceh ke Lampung", paragraf pembuka 2 kalimat, `SearchBox` ringkas, dan `ChapterList`. Gaya mengikuti token Task 1: latar `--paper`, garis `--rule`, label uppercase untuk "BAB I" dsb.

**Sketsa tata letak yang harus terlihat:**
```
─────────────────────────────────────────────
 MUSEUM SUMATERA                [ Cari … ] →
 Perjalanan dari Aceh ke Lampung
─────────────────────────────────────────────
 BAB I    Dari Pelabuhan ke Pedalaman      3 museum →
 BAB II   Tanah Karo dan Danau Toba        4 museum →
 …
─────────────────────────────────────────────
```

- [ ] **Step 2: Tangani keadaan Fuseki mati**

Bila `/api/chapters` gagal, halaman tetap menampilkan sampul + daftar bab **statis** dari konstanta `src/lib/chapters.ts` (tujuh bab, definisi tetap) dengan `museumCount: null`, plus catatan kecil: *"Basis data museum sedang tidak dapat dihubungi."*

- [ ] **Step 3: Tulis `src/lib/chapters.ts`**

Ekspor `export const CHAPTERS: { index: number; label: string; title: string }[]` berisi tujuh bab persis seperti spec §8 dengan label "Bab I".."Bab VII".

- [ ] **Step 4: Verifikasi di browser**

Run: `bun dev`, buka `http://localhost:3000`.
Expected: sampul tampil dengan 7 bab; mengosongkan `FUSEKI_ENDPOINT` sementara menampilkan catatan "Basis data museum sedang tidak dapat dihubungi" tanpa crash.

- [ ] **Step 5: Commit**

```bash
git add src
git commit -m "feat: add cover page with chapter list and search entry"
```

---

### Task 8: Halaman bab (`/jelajah/[chapter]`)

**Files:**
- Create: `src/app/jelajah/[chapter]/page.tsx`, `src/components/MuseumEntry.tsx`, `src/components/ChapterNav.tsx`

**Interfaces:**
- Consumes: `museumsByChapterQuery`, `CHAPTERS`, `MuseumDTO`.
- Produces: `MuseumEntry` dengan prop `{ museum: MuseumDTO }`; `ChapterNav` dengan prop `{ current: number }` menampilkan tautan bab sebelum/berikutnya.

- [ ] **Step 1: Implementasi rute dinamis**

`params.chapter` divalidasi: harus bilangan bulat 1–7. Selain itu → `notFound()` dengan halaman `src/app/jelajah/[chapter]/not-found.tsx` berjudul "Bab tidak ditemukan" dan tautan ke `/`.

- [ ] **Step 2: Bangun tampilan bab**

Header: "BAB {INISIAL ROMAWI} — {title}", diikuti narasi pembuka (2–3 kalimat, disimpan di `src/lib/chapters.ts` sebagai field `intro`). Lalu daftar `MuseumEntry` sebagai **baris katalog** (bukan kartu): nomor, nama serif, "Kota · Provinsi · Tahun", tema sebagai label. Setiap baris menautkan ke `/museum/{slug}`.

- [ ] **Step 3: Tambahkan `ChapterNav` di kaki halaman**

Tautan "← Bab sebelumnya" dan "Bab berikutnya →", disembunyikan di ujung alur. Sertakan juga tautan "Lihat katalog lengkap".

- [ ] **Step 4: Verifikasi terhadap Fuseki**

Run: `bun dev`, buka `/jelajah/1`..`/jelajah/7`.
Expected: tiap bab menampilkan museum yang benar (jumlah cocok dengan `museumCount` di sampul); `/jelajah/99` dan `/jelajah/abc` menampilkan "Bab tidak ditemukan".

- [ ] **Step 5: Commit**

```bash
git add src
git commit -m "feat: add chapter pages with catalog-style museum entries"
```

---

### Task 9: Halaman entri museum (`/museum/[slug]`)

**Files:**
- Create: `src/app/museum/[slug]/page.tsx`, `src/components/ThreadOfRelation.tsx`, `src/components/VerificationBadge.tsx`

**Interfaces:**
- Consumes: route `/api/museum?slug=`, `MuseumDTO`, `RelatedDTO`, `FALLBACK_IMAGE`.
- Produces: `ThreadOfRelation` dengan prop `{ related: RelatedDTO[] }` yang merender "benang merah" atau `null` bila kosong; `VerificationBadge` dengan prop `{ status: MuseumDTO["verificationStatus"] }`.

- [ ] **Step 1: Implementasi halaman entri**

Menampilkan: judul serif, metadata sebagai tabel label–nilai (Kota, Provinsi, Berdiri, Tema, Era, Alamat, Catatan kunjungan), narasi deskripsi, `VerificationBadge`, dan gambar dengan `onError` → `FALLBACK_IMAGE`. `establishedYear` null ditampilkan "Tahun tidak tercatat".

- [ ] **Step 2: Implementasi `ThreadOfRelation`**

Untuk setiap `RelatedDTO`, tulis kalimat naratif yang memakai `reason`, mis.: *"Satu tema dengan Museum Negeri Aceh — keduanya menyimpan koleksi etnografi."* Tautkan ke `/museum/{slug}`.

- [ ] **Step 3: Verifikasi**

Run: `bun dev`, buka satu museum dari bab, ikuti satu tautan benang merah.
Expected: halaman terbuka, minimal satu benang merah tampil, tidak ada museum merekomendasikan dirinya sendiri. Untuk museum dengan slug tak dikenal → halaman "Museum tidak ditemukan".

- [ ] **Step 4: Commit**

```bash
git add src
git commit -m "feat: add museum entry page with graph-derived threads"
```

---

### Task 10: Katalog dan pencarian (`/katalog`)

**Files:**
- Create: `src/app/katalog/page.tsx`, `src/components/CatalogFilters.tsx`, `src/components/SearchBox.tsx` (modifikasi), `src/store/catalogPrefs.ts`
- Create: `src/components/EmptyState.tsx`

**Interfaces:**
- Consumes: route `/api/search`, `CatalogParams`, `CHAPTERS`.
- Produces: `CatalogFilters` dengan prop `{ value: CatalogParams; onChange: (next: CatalogParams) => void; disabled?: boolean }`; `useCatalogPrefs` (Zustand persist) menyimpan `sort`/`order` terakhir dengan key `"museum-catalog-prefs"`.

- [ ] **Step 1: Implementasi halaman katalog**

Client Component. Search box + filter provinsi (dari daftar resmi Task 4), tema, era, minYear, urutkan (nama/tahun), urutan. Semua nilai filter **dikirim ke `/api/search` sebagai query param** — tidak ada `.filter()` atau `.sort()` di komponen ini. State disinkronkan ke URL (`?q=&province=&theme=&era=&minYear=&sort=&order=`).

- [ ] **Step 2: Tangani keadaan kosong dan error**

`EmptyState` memakai dua varian: *"Tidak ada museum yang cocok dengan penyaringan Anda."* (ada filter) dan *"Belum ada data museum."* (tanpa filter, kemungkinan Fuseki kosong). Error Fuseki menampilkan pesan bahasa Indonesia dari Task 5.

- [ ] **Step 3: Tampilkan jumlah hasil dan hasil utama/sekunder**

Bila `ranking` ada, tampilkan dua kelompok: "Hasil utama" dan "Hasil lainnya", memakai `MuseumEntry`. Bila tidak, tampilkan satu daftar datar.

- [ ] **Step 4: Verifikasi**

Run: `bun dev`, buka `/katalog?province=Aceh&theme=etnografi&minYear=1900`.
Expected: hasil menyusut sesuai filter; mengubah URL langsung mengubah hasil; tidak ada error konsol.

- [ ] **Step 5: Commit**

```bash
git add src
git commit -m "feat: add catalog page with SPARQL-backed search and filters"
```

---

### Task 11: README setup dan verifikasi menyeluruh

**Files:**
- Modify: `README.md`
- Create: `docs/fuseki-setup.md`

**Interfaces:**
- Consumes: semua skrip Task 1–4.
- Produces: dokumentasi yang memungkinkan orang lain menjalankan proyek dari nol.

- [ ] **Step 1: Tulis `docs/fuseki-setup.md`**

Langkah bernomor: unduh Apache Jena Fuseki, jalankan `fuseki-server`, buat dataset bernama `museum` (TDB2), upload `data/museum-sumatera.rdf` (lewat UI *Add data* atau `bun run upload:fuseki`), verifikasi dengan query contoh `SELECT (COUNT(*) AS ?n) WHERE { ?s a sdp:Museum }` yang harus mengembalikan `28`, lalu sesuaikan `.env`.

- [ ] **Step 2: Tulis ulang `README.md`**

Bagian: apa ini, prasyarat (bun, Fuseki), langkah menjalankan (5 langkah), struktur folder, penjelasan ontologi singkat, cara memperbarui data (`museums.json` → `generate:rdf` → `upload:fuseki`), catatan verifikasi data, dan daftar endpoint API.

- [ ] **Step 3: Jalankan verifikasi menyeluruh**

```bash
bun run test          # semua test lulus
bun run check:rdf     # exit 0
bun run build         # build sukses
bun dev               # cek manual: sampul → bab 1 → museum → benang merah → katalog → filter
```

Expected: semuanya lulus; tidak ada error konsol di browser; jumlah museum di katalog = 28.

- [ ] **Step 4: Commit**

```bash
git add README.md docs
git commit -m "docs: add end-to-end setup and data pipeline instructions"
```
