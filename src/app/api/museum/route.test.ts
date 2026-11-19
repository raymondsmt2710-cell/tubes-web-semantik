import { describe, it, expect, vi, afterEach } from "vitest";
import { GET } from "./route";

afterEach(() => {
  vi.unstubAllGlobals();
});

function ok(bindings: unknown[]) {
  return new Response(JSON.stringify({ results: { bindings } }), {
    status: 200,
    headers: { "content-type": "application/sparql-results+json" },
  });
}

const baseRow = {
  museum: { type: "uri", value: "https://museumsumatera.id/resource/museum/museum-a" },
  slug: { type: "literal", value: "museum-a" },
  name: { type: "literal", value: "Museum A" },
  province: { type: "literal", value: "Aceh" },
  city: { type: "literal", value: "Banda Aceh" },
  themes: { type: "literal", value: "etnografi" },
  era: { type: "literal", value: "kolonial" },
  chapterIndex: { type: "literal", value: "1" },
  verification: { type: "literal", value: "perlu-verifikasi" },
};

const relatedRow = {
  museum: { type: "uri", value: "https://museumsumatera.id/resource/museum/museum-b" },
  slug: { type: "literal", value: "museum-b" },
  name: { type: "literal", value: "Museum B" },
  province: { type: "literal", value: "Aceh" },
  city: { type: "literal", value: "Lhokseumawe" },
  themes: { type: "literal", value: "etnografi" },
  era: { type: "literal", value: "kolonial" },
  chapterIndex: { type: "literal", value: "1" },
};

describe("GET /api/museum", () => {
  it("mengembalikan 400 bila parameter slug tidak ada", async () => {
    const response = await GET(new Request("http://localhost/api/museum"));
    expect(response.status).toBe(400);
  });

  it("mengembalikan 404 dengan pesan Bahasa Indonesia bila museum tidak ada", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => ok([])));
    const response = await GET(new Request("http://localhost/api/museum?slug=tidak-ada"));
    const body = await response.json();

    expect(response.status).toBe(404);
    expect(body.error).toMatch(/tidak ditemukan/i);
  });

  it("mengembalikan museum beserta benang merah dari relasi graf", async () => {
    let call = 0;
    vi.stubGlobal(
      "fetch",
      vi.fn(async () => {
        call += 1;
        return ok(call === 1 ? [baseRow] : [relatedRow]);
      }),
    );

    const response = await GET(new Request("http://localhost/api/museum?slug=museum-a"));
    const body = await response.json();

    expect(response.status).toBe(200);
    expect(body.museum.slug).toBe("museum-a");
    expect(body.related).toHaveLength(1);
    expect(body.related[0].slug).toBe("museum-b");
    expect(body.related[0].reason).toMatch(/tema/i);
  });

  it("mengembalikan 502 saat Fuseki tidak dapat dihubungi", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(async () => {
        throw new Error("ECONNREFUSED");
      }),
    );

    const response = await GET(new Request("http://localhost/api/museum?slug=museum-a"));
    expect(response.status).toBe(502);
  });
});
