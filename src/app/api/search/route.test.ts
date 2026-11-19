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

describe("GET /api/search", () => {
  it("mengembalikan 502 dengan pesan Bahasa Indonesia saat Fuseki tidak dapat dihubungi", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(async () => {
        throw new Error("ECONNREFUSED");
      }),
    );

    const response = await GET(new Request("http://localhost/api/search?q=aceh"));
    const body = await response.json();

    expect(response.status).toBe(502);
    expect(body.error).toMatch(/basis data museum/i);
  });

  it("meneruskan filter provinsi ke query SPARQL, bukan menyaring di JS", async () => {
    let sent = "";
    vi.stubGlobal(
      "fetch",
      vi.fn(async (_url: string, init: RequestInit) => {
        sent = decodeURIComponent(String(init.body));
        return okResponse([]);
      }),
    );

    await GET(new Request("http://localhost/api/search?province=Aceh"));

    expect(sent).toContain('FILTER(STR(?province) = "Aceh")');
  });

  it("mengurutkan hasil teks dan menandai kelompok utama/sekunder", async () => {
    const bindings = [
      {
        museum: { type: "uri", value: "https://museumsumatera.id/resource/museum/a" },
        slug: { type: "literal", value: "a" },
        name: { type: "literal", value: "Museum Negeri Aceh" },
        themes: { type: "literal", value: "etnografi" },
      },
      {
        museum: { type: "uri", value: "https://museumsumatera.id/resource/museum/b" },
        slug: { type: "literal", value: "b" },
        name: { type: "literal", value: "Museum Timah Indonesia" },
        themes: { type: "literal", value: "sains-teknologi" },
      },
    ];
    vi.stubGlobal("fetch", vi.fn(async () => okResponse(bindings)));

    const response = await GET(
      new Request("http://localhost/api/search?q=museum%20negeri%20aceh"),
    );
    const body = await response.json();

    expect(body.total).toBe(2);
    expect(body.museums[0].slug).toBe("a");
    expect(body.ranking[0]).toMatchObject({ slug: "a", group: "primary" });
    expect(body.ranking[1].group).toBe("secondary");
  });

  it("mengembalikan seluruh katalog tanpa peringkat saat q kosong", async () => {
    const bindings = [
      {
        museum: { type: "uri", value: "https://museumsumatera.id/resource/museum/a" },
        slug: { type: "literal", value: "a" },
        name: { type: "literal", value: "Museum A" },
        themes: { type: "literal", value: "arkeologi" },
      },
    ];
    vi.stubGlobal("fetch", vi.fn(async () => okResponse(bindings)));

    const response = await GET(new Request("http://localhost/api/search?province=Aceh"));
    const body = await response.json();

    expect(body.total).toBe(1);
    expect(body.ranking).toBeUndefined();
    expect(body.museums[0].themes).toEqual(["arkeologi"]);
  });
});
