import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { buildRdf } from "../src/lib/ontology";
import { CHAPTERS } from "../src/lib/chapters";
import type { MuseumRecord } from "../src/lib/types";

const inputPath = fileURLToPath(new URL("../data/museums.json", import.meta.url));
const outputPath = fileURLToPath(new URL("../data/museum-sumatera.rdf", import.meta.url));

function main() {
  const records = JSON.parse(readFileSync(inputPath, "utf-8")) as MuseumRecord[];
  const xml = buildRdf(records);
  writeFileSync(outputPath, xml, "utf-8");

  const provinces = new Set(records.map((r) => r.province));
  const themes = new Set(records.flatMap((r) => r.themes));
  const chapters = new Set(records.map((r) => r.chapter));

  console.log(`RDF ditulis ke ${outputPath}`);
  console.log(`  museum   : ${records.length}`);
  console.log(`  provinsi : ${provinces.size}`);
  console.log(`  tema     : ${themes.size}`);
  console.log(`  bab      : ${chapters.size} dari ${CHAPTERS.length}`);
}

try {
  main();
} catch (error) {
  console.error("Gagal membuat RDF:");
  console.error(error instanceof Error ? error.message : error);
  process.exit(1);
}
