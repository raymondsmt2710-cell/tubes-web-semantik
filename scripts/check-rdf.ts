import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { hasErrors, validateMuseums } from "../src/lib/validate";
import type { MuseumRecord } from "../src/lib/types";

const inputPath = fileURLToPath(new URL("../data/museums.json", import.meta.url));

function main() {
  const records = JSON.parse(readFileSync(inputPath, "utf-8")) as MuseumRecord[];
  const issues = validateMuseums(records);

  const errors = issues.filter((i) => i.level === "error");
  const warnings = issues.filter((i) => i.level === "warning");

  console.log(`Diperiksa ${records.length} museum.`);
  console.log(`  error   : ${errors.length}`);
  console.log(`  warning : ${warnings.length}`);

  for (const issue of errors) {
    console.log(`  [ERROR] ${issue.slug} · ${issue.field}: ${issue.message}`);
  }

  if (warnings.length > 0) {
    console.log("\nPeringatan (tidak menghalangi):");
    const byField = new Map<string, number>();
    for (const warning of warnings) {
      const key = `${warning.field}: ${warning.message}`;
      byField.set(key, (byField.get(key) ?? 0) + 1);
    }
    for (const [key, count] of byField) {
      console.log(`  [WARN] ${count}× ${key}`);
    }
  }

  if (hasErrors(issues)) {
    console.error("\nData museum belum siap; perbaiki error di atas.");
    process.exit(1);
  }

  console.log("\nSiap digenerate menjadi RDF.");
}

try {
  main();
} catch (error) {
  console.error(error instanceof Error ? error.message : error);
  process.exit(1);
}
