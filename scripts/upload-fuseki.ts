import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

// Next.js memuat .env otomatis, tetapi skrip yang dijalankan lewat tsx tidak.
// Muat di sini supaya `npm run upload:fuseki` menghormati isi .env; nilai yang
// sudah ada di shell tidak ditimpa.
const loadEnvFile = (
  process as unknown as { loadEnvFile?: (path?: string) => void }
).loadEnvFile;

if (typeof loadEnvFile === "function") {
  try {
    loadEnvFile();
  } catch {
    // .env opsional: endpoint boleh diisi langsung lewat environment shell.
  }
}

const rdfPath = fileURLToPath(new URL("../data/museum-sumatera.rdf", import.meta.url));

const updateEndpoint = process.env.FUSEKI_UPDATE?.trim();
const queryEndpoint = process.env.FUSEKI_ENDPOINT?.trim();

async function main() {
  if (!updateEndpoint) {
    console.error(
      [
        "FUSEKI_UPDATE belum diisi, jadi unggahan otomatis dilewati.",
        "",
        "Pilihan Anda:",
        "  1. Salin .env.example menjadi .env dan isi FUSEKI_UPDATE,",
        "     mis. http://localhost:3030/museum/data",
        "  2. Unggah manual: buka Fuseki → dataset → Add data → Upload file,",
        `     pilih ${rdfPath}`,
        "",
        "Jangan lupa periksa juga FUSEKI_ENDPOINT",
        queryEndpoint ? `   (sekarang: ${queryEndpoint})` : "   (belum diisi; memakai default localhost)",
      ].join("\n"),
    );
    process.exit(2);
  }

  const body = readFileSync(rdfPath, "utf-8");

  console.log("Membersihkan graph default...");
  // FUSEKI_UPDATE menunjuk Graph Store Protocol (/data). "CLEAR DEFAULT"
  // adalah operasi SPARQL Update yang ditolak endpoint ini, jadi kosongkan
  // graph lewat DELETE ?default sesuai GSP.
  const separator = updateEndpoint.includes("?") ? "&" : "?";
  const clearResponse = await fetch(`${updateEndpoint}${separator}default`, {
    method: "DELETE",
  });
  if (!clearResponse.ok && clearResponse.status !== 404) {
    console.error(`Gagal membersihkan graph (${clearResponse.status}).`);
    console.error((await clearResponse.text()).slice(0, 500));
    process.exit(1);
  }

  console.log("Mengunggah RDF...");
  const uploadResponse = await fetch(updateEndpoint, {
    method: "POST",
    headers: { "Content-Type": "application/rdf+xml" },
    body,
  });

  if (!uploadResponse.ok) {
    console.error(`Gagal mengunggah RDF (${uploadResponse.status}).`);
    console.error((await uploadResponse.text()).slice(0, 500));
    process.exit(1);
  }

  console.log("Selesai. Data museum terunggah ke Fuseki.");
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : error);
  process.exit(1);
});
