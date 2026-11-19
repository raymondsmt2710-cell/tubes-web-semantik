import { describe, it, expect, vi, afterEach } from "vitest";
import { runSelect, FusekiError } from "./sparql";

afterEach(() => {
  vi.unstubAllGlobals();
  delete process.env.FUSEKI_ENDPOINT;
});

describe("runSelect", () => {
  it("mengembalikan bindings dari respons JSON Fuseki", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(
        async () =>
          new Response(
            JSON.stringify({
              results: { bindings: [{ museum: { type: "uri", value: "http://x/1" } }] },
            }),
            { status: 200, headers: { "content-type": "application/sparql-results+json" } },
          ),
      ),
    );

    const rows = await runSelect("SELECT * WHERE { ?s ?p ?o }");

    expect(rows).toHaveLength(1);
    expect(rows[0].museum?.value).toBe("http://x/1");
  });

  it("melempar FusekiError saat endpoint membalas 500", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => new Response("boom", { status: 500 })));

    await expect(runSelect("SELECT * WHERE { }")).rejects.toBeInstanceOf(FusekiError);
  });

  it("mengirim query sebagai form-urlencoded dan meminta hasil JSON", async () => {
    process.env.FUSEKI_ENDPOINT = "http://localhost:3030/museum/query";
    const spy = vi.fn(
      async () => new Response(JSON.stringify({ results: { bindings: [] } }), { status: 200 }),
    );
    vi.stubGlobal("fetch", spy);

    await runSelect("SELECT ?s WHERE { ?s a ?o }");

    const [url, init] = spy.mock.calls[0] as unknown as [string, RequestInit];
    expect(String(url)).toBe("http://localhost:3030/museum/query");
    expect(init.method).toBe("POST");
    expect((init.headers as Record<string, string>).Accept).toBe(
      "application/sparql-results+json",
    );
    expect(String(init.body)).toBe(
      "query=SELECT%20%3Fs%20WHERE%20%7B%20%3Fs%20a%20%3Fo%20%7D",
    );
  });

  it("memakai endpoint lokal default saat env tidak diisi", async () => {
    const spy = vi.fn(
      async () => new Response(JSON.stringify({ results: { bindings: [] } }), { status: 200 }),
    );
    vi.stubGlobal("fetch", spy);

    await runSelect("SELECT * WHERE { ?s ?p ?o }");

    expect(String((spy.mock.calls[0] as unknown as [string])[0])).toBe(
      "http://localhost:3030/museum/query",
    );
  });

  it("melempar FusekiError saat body bukan JSON", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(async () => new Response("<html>error</html>", { status: 200 })),
    );

    await expect(runSelect("SELECT * WHERE { }")).rejects.toBeInstanceOf(FusekiError);
  });
});

describe("toSlug / yearLabel", () => {
  it("mengubah nama museum menjadi slug yang aman untuk URL", async () => {
    const { toSlug } = await import("./types");
    expect(toSlug("Museum Negeri Provinsi Riau")).toBe("museum-negeri-provinsi-riau");
    expect(toSlug("Museum  Budaya  Aceh!")).toBe("museum-budaya-aceh");
    expect(toSlug("Museum Sriwijaya — Palembang")).toBe("museum-sriwijaya-palembang");
  });

  it("menampilkan tahun tak tercatat dalam bahasa Indonesia", async () => {
    const { yearLabel } = await import("./types");
    expect(yearLabel(1932)).toBe("1932");
    expect(yearLabel(null)).toBe("Tahun tidak tercatat");
  });
});
