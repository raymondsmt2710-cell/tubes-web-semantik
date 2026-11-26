import { describe, it, expect, vi, afterEach } from "vitest";
import { GET } from "./route";

afterEach(() => {
  vi.unstubAllGlobals();
});

function okResponse(bindings: unknown[]) {
  return new Response(JSON.stringify({ results: { bindings } }), {
    status: 200,
    headers: { "content-type": "application/sparql-results+json" },
  });
}

describe("GET /api/tanya", () => {
  it("menolak permintaan tanpa parameter q", async () => {
    const response = await GET(new Request("http://localhost/api/tanya"));
    expect(response.status).toBe(400);
    const body = await response.json();
    expect(body.error).toMatch(/parameter q/i);
  });

  it("menolak pertanyaan yang terlalu panjang", async () => {
    const panjang = "a".repeat(400);
    const response = await GET(new Request(`http://localhost/api/tanya?q=${panjang}`));
    expect(response.status).toBe(400);
  });

  it("mengembalikan jawaban ber-sumber untuk pertanyaan yang dikenali", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(async (_url: string, init: RequestInit) => {
        const body = decodeURIComponent(String(init.body));
        if (body.includes("VALUES (?kelas ?jenis)")) {
          return okResponse([
            {
              e: { type: "uri", value: "https://museumsumatera.id/resource/province/aceh" },
              label: { type: "literal", value: "Aceh" },
              jenis: { type: "literal", value: "provinsi" },
            },
          ]);
        }
        return okResponse([
          {
            museum: {
              type: "uri",
              value: "https://museumsumatera.id/resource/museum/museum-negeri-aceh",
            },
            nama: { type: "literal", value: "Museum Negeri Aceh" },
          },
        ]);
      }),
    );

    const response = await GET(
      new Request("http://localhost/api/tanya?q=Museum%20apa%20saja%20di%20Aceh%3F"),
    );
    const body = await response.json();

    expect(response.status).toBe(200);
    expect(body.lolos).toBe(true);
    expect(body.jawaban).toContain("Museum Negeri Aceh");
    expect(body.sumber).toEqual([
      "https://museumsumatera.id/resource/museum/museum-negeri-aceh",
    ]);
    expect(body.query).toContain("LIMIT");
  });

  it("menjawab 'tidak ditemukan' saat graf tidak memuat hasil", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => okResponse([])));

    const response = await GET(
      new Request("http://localhost/api/tanya?q=Museum%20apa%20saja%3F"),
    );
    const body = await response.json();

    expect(body.jawaban).toBe("Tidak ditemukan di graf.");
    expect(body.sumber).toEqual([]);
  });

  it("mengembalikan 502 saat Fuseki tidak dapat dihubungi", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(async () => {
        throw new Error("ECONNREFUSED");
      }),
    );

    const response = await GET(
      new Request("http://localhost/api/tanya?q=Museum%20apa%20saja%3F"),
    );
    expect(response.status).toBe(502);
    const body = await response.json();
    expect(body.error).toMatch(/basis data museum/i);
  });
});
