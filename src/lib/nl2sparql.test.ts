import { describe, it, expect } from "vitest";
import {
  MAX_LIMIT,
  askGraph,
  bacaIntent,
  periksa,
  rakitQuery,
  cariEntitas,
} from "./nl2sparql";
import type { SparqlBinding } from "./sparql";
import { RES, SDP } from "./ontology";

/** Runner palsu: mencatat query dan mengembalikan baris yang sudah ditentukan. */
function runner(rows: SparqlBinding[] = []) {
  const queries: string[] = [];
  const run = async (q: string) => {
    queries.push(q);
    return rows;
  };
  return { run, queries };
}

describe("bacaIntent", () => {
  it("membaca permintaan hitung tanpa jebakan substring", () => {
    // "era" ada di dalam "berapa"; batas kata harus mencegahnya cocok.
    const intent = bacaIntent("Berapa jumlah museum?");
    expect(intent.jenis).toBe("hitung");
    expect(intent.topik).toBe("museum");
  });

  it("memperlakukan 'berapa tahun ... berdiri' sebagai atribut, bukan COUNT", () => {
    const intent = bacaIntent("Berapa tahun Museum Negeri Aceh berdiri?");
    expect(intent.jenis).toBe("atribut");
    expect(intent.atribut).toBe("establishedYear");
  });

  it("mengenali topik pameran dan galeri", () => {
    expect(bacaIntent("Apa saja pameran di Museum Aceh?").topik).toBe("pameran");
    expect(bacaIntent("Apa saja foto di Museum Aceh?").topik).toBe("galeri");
  });
});

describe("cariEntitas", () => {
  it("memilih label terpanjang bila dua entitas cocok", async () => {
    const rows: SparqlBinding[] = [
      {
        e: { type: "uri", value: `${RES}province/aceh` },
        label: { type: "literal", value: "Aceh" },
        jenis: { type: "literal", value: "provinsi" },
      },
      {
        e: { type: "uri", value: `${RES}museum/museum-negeri-aceh` },
        label: { type: "literal", value: "Museum Negeri Aceh" },
        jenis: { type: "literal", value: "museum" },
      },
    ];
    const { run } = runner(rows);
    const hasil = await cariEntitas("Apa isi Museum Negeri Aceh?", run);
    expect(hasil[0].label).toBe("Museum Negeri Aceh");
  });

  it("menerima kedua jalur nama (sdp:name dan rdfs:label)", async () => {
    const { run, queries } = runner([]);
    await cariEntitas("museum", run);
    expect(queries[0]).toContain("(sdp:name|rdfs:label)");
  });

  it("tidak mengembalikan entitas yang tidak disebut", async () => {
    const rows: SparqlBinding[] = [
      {
        e: { type: "uri", value: `${RES}museum/x` },
        label: { type: "literal", value: "Museum X" },
        jenis: { type: "literal", value: "museum" },
      },
    ];
    const { run } = runner(rows);
    expect(await cariEntitas("berapa harga tiket pesawat", run)).toEqual([]);
  });

  it("membatasi hasil ke dua entitas teratas", async () => {
    const rows: SparqlBinding[] = ["A", "B", "C"].map((n) => ({
      e: { type: "uri", value: `${RES}museum/${n}` },
      label: { type: "literal", value: `Museum ${n}` },
      jenis: { type: "literal", value: "museum" },
    }));
    const { run } = runner(rows);
    const hasil = await cariEntitas("Museum A, Museum B, Museum C", run);
    expect(hasil).toHaveLength(2);
  });
});

describe("rakitQuery", () => {
  it("memakai path multi-hop untuk provinsi", () => {
    const q = rakitQuery({ jenis: "daftar", topik: "museum", atribut: null, kata: [] }, [
      { iri: `${RES}province/aceh`, label: "Aceh", jenis: "provinsi" },
    ]);
    expect(q).toContain("locatedInCity/sdp:partOfProvince");
  });

  it("memakai locatedInCity langsung untuk kota", () => {
    const q = rakitQuery({ jenis: "daftar", topik: "museum", atribut: null, kata: [] }, [
      { iri: `${RES}city/banda-aceh`, label: "Banda Aceh", jenis: "kota" },
    ]);
    expect(q).toContain("?museum sdp:locatedInCity");
    expect(q).not.toContain("partOfProvince");
  });

  it("selalu menyertakan LIMIT yang aman", () => {
    const q = rakitQuery({ jenis: "daftar", topik: "museum", atribut: null, kata: [] }, []);
    expect(q).toContain(`LIMIT ${MAX_LIMIT}`);
  });

  it("memakai DISTINCT supaya museum tidak muncul ganda", () => {
    const q = rakitQuery({ jenis: "daftar", topik: "museum", atribut: null, kata: [] }, [
      { iri: `${RES}province/aceh`, label: "Aceh", jenis: "provinsi" },
    ]);
    expect(q).toContain("SELECT DISTINCT");
  });
});

describe("periksa (guard)", () => {
  it("menerima SELECT dengan LIMIT kecil", () => {
    const q = `PREFIX sdp: <${SDP}>\nSELECT ?s WHERE { ?s a sdp:Museum } LIMIT 10`;
    expect(periksa(q).lolos).toBe(true);
  });

  it("menolak query tanpa LIMIT", () => {
    const hasil = periksa(`PREFIX sdp: <${SDP}>\nSELECT ?s WHERE { ?s a sdp:Museum }`);
    expect(hasil.lolos).toBe(false);
    expect(hasil.pesan).toContain("LIMIT");
  });

  it("menolak LIMIT yang terlalu besar", () => {
    const hasil = periksa(`SELECT ?s WHERE { ?s a <${SDP}Museum> } LIMIT 500`);
    expect(hasil.lolos).toBe(false);
  });

  it("menolak DELETE", () => {
    expect(periksa("DELETE WHERE { ?s ?p ?o }").lolos).toBe(false);
  });

  it("menolak CONSTRUCT", () => {
    expect(periksa("CONSTRUCT { ?s ?p ?o } WHERE { ?s ?p ?o } LIMIT 5").lolos).toBe(false);
  });

  it("menolak properti karangan", () => {
    const hasil = periksa(`SELECT ?n WHERE { ?s sdp:namaLengkap ?n } LIMIT 5`);
    expect(hasil.lolos).toBe(false);
    expect(hasil.pesan).toContain("tidak dikenal");
  });

  it("tidak salah menuduh deklarasi PREFIX sebagai IRI asing", () => {
    // Regresi: sebelumnya <https://…ontology#> di baris PREFIX ikut diperiksa.
    expect(periksa(`PREFIX sdp: <${SDP}>\nSELECT ?s WHERE { ?s a sdp:Museum } LIMIT 5`).lolos).toBe(
      true,
    );
  });

  it("menolak kurung kurawal tidak seimbang", () => {
    expect(periksa(`SELECT ?s WHERE { ?s a <${SDP}Museum> LIMIT 5`).lolos).toBe(false);
  });

  it("menolak query kosong", () => {
    expect(periksa("   ").lolos).toBe(false);
  });
});

describe("askGraph", () => {
  it("menjawab dari data dan menempelkan sumber berupa IRI entitas", async () => {
    const rows: SparqlBinding[] = [
      {
        museum: { type: "uri", value: `${RES}museum/museum-negeri-aceh` },
        nama: { type: "literal", value: "Museum Negeri Aceh" },
      },
    ];
    const { run } = runner(rows);
    const hasil = await askGraph("Museum apa saja di Aceh?", run);
    expect(hasil.lolos).toBe(true);
    expect(hasil.jawaban).toContain("Museum Negeri Aceh");
    expect(hasil.sumber).toEqual([`${RES}museum/museum-negeri-aceh`]);
  });

  it("menjawab 'tidak ditemukan' saat hasil kosong", async () => {
    const { run } = runner([]);
    const hasil = await askGraph("Museum apa saja di Kota TidakAda?", run);
    expect(hasil.lolos).toBe(true);
    expect(hasil.jawaban).toBe("Tidak ditemukan di graf.");
    expect(hasil.sumber).toEqual([]);
  });

  it("tidak pernah menjalankan query yang ditolak guard", async () => {
    const { run, queries } = runner([]);
    const hasil = await askGraph("   ", run);
    expect(hasil.lolos).toBe(false);
    expect(queries).toHaveLength(0);
  });

  it("menghitung dengan COUNT untuk permintaan jumlah", async () => {
    const rows: SparqlBinding[] = [{ jumlah: { type: "literal", value: "28" } }];
    const { run, queries } = runner(rows);
    const hasil = await askGraph("Berapa jumlah museum?", run);
    expect(queries.some((q) => q.includes("COUNT"))).toBe(true);
    expect(hasil.jawaban).toContain("28");
  });

  it("menjawab tahun berdiri sebagai atribut", async () => {
    const rows: SparqlBinding[] = [{ nilai: { type: "literal", value: "1915" } }];
    const { run } = runner(rows);
    const hasil = await askGraph("Berapa tahun Museum Negeri Aceh berdiri?", run);
    expect(hasil.jawaban).toContain("1915");
  });

  it("menyertakan baris hasil agar dapat diperiksa", async () => {
    const rows: SparqlBinding[] = [
      {
        museum: { type: "uri", value: `${RES}museum/x` },
        nama: { type: "literal", value: "Museum X" },
      },
    ];
    const { run } = runner(rows);
    const hasil = await askGraph("Museum apa saja?", run);
    expect(hasil.baris[0]).toContain("Museum X");
  });
});
