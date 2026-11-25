import { readFileSync, writeFileSync } from "node:fs";
import type { MuseumRecord, Exhibit, MuseumImage } from "../src/lib/types.ts";

const path = "data/museums.json";
const records = JSON.parse(readFileSync(path, "utf-8")) as MuseumRecord[];

type ExhibitPatch = Partial<Exhibit> & { title: string; _new?: boolean };
type GalleryPatch = { src: string } & Partial<MuseumImage>;

const patches: Record<
  string,
  { exhibits?: ExhibitPatch[]; gallery?: GalleryPatch[]; addSources?: { label: string; url: string }[] }
> = {};

function apply() {
  let exhibitCount = 0;
  let galleryCount = 0;
  for (const [slug, patch] of Object.entries(patches)) {
    const museum = records.find((r) => r.slug === slug);
    if (!museum) {
      throw new Error(`Museum tidak ditemukan: ${slug}`);
    }

    for (const ex of patch.exhibits ?? []) {
      const { _new, ...fields } = ex;
      const existing = museum.exhibits ?? [];
      const target = existing.find((e) => e.title === ex.title);
      if (!target) {
        if (!_new) {
          throw new Error(`${slug}: pameran "${ex.title}" tidak ada.`);
        }
        museum.exhibits = [...existing, fields as Exhibit];
        exhibitCount++;
        continue;
      }
      Object.assign(target, fields);
      exhibitCount++;
    }

    for (const g of patch.gallery ?? []) {
      const { src, ...fields } = g;
      const target = museum.gallery?.find((i) => i.src.endsWith(src));
      if (!target) {
        throw new Error(`${slug}: foto "${src}" tidak ada.`);
      }
      Object.assign(target, fields);
      galleryCount++;
    }

    if (patch.addSources?.length) {
      museum.sources = [...(museum.sources ?? [])];
      for (const s of patch.addSources) {
        if (!museum.sources.some((x) => x.url === s.url)) museum.sources.push(s);
      }
    }
  }

  writeFileSync(path, JSON.stringify(records, null, 2) + "\n", "utf-8");
  console.log(`Pameran diperbarui: ${exhibitCount}`);
  console.log(`Foto diperbarui   : ${galleryCount}`);
}

export { patches, apply, records };

if (process.argv[1]?.endsWith("apply-content.ts")) {
  apply();
}
