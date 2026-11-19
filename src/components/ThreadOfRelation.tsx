import Link from "next/link";
import { themeLabels, type RelatedDTO } from "@/lib/types";

interface ThreadOfRelationProps {
  related: RelatedDTO[];
  baseName: string;
}

export default function ThreadOfRelation({ related, baseName }: ThreadOfRelationProps) {
  if (related.length === 0) return null;

  return (
    <section className="mt-14 border-t border-[--rule] pt-8">
      <h2 className="font-serif text-xl">Benang merah</h2>
      <p className="text-sm text-[--ink-soft] mt-2 measure">
        Museum-museum berikut tidak dipilih secara acak: hubungannya dihitung dari
        kedekatan tema, kota, era, dan posisi bab pada graf data — bukan dari teks
        halaman ini.
      </p>

      <ul className="mt-6 grid gap-x-8 gap-y-6 sm:grid-cols-2">
        {related.map((item) => {
          const meta = [item.city, item.province].filter(Boolean).join(" · ");

          return (
            <li key={item.slug} className="border-l-2 border-[--rule] pl-4">
              <Link href={`/museum/${encodeURIComponent(item.slug)}`} className="group">
                <span className="block font-serif text-base group-hover:underline">
                  {item.name}
                </span>
              </Link>
              <p className="text-xs text-[--ink-soft] mt-1">
                {meta} · kekuatan hubungan {item.score}
              </p>
              <p className="text-sm mt-2">
                Karena {item.reason} dengan {baseName}.
              </p>
              <p className="text-xs text-[--ink-faint] mt-1">
                {themeLabels(item.themes).join(", ")}
              </p>
            </li>
          );
        })}
      </ul>
    </section>
  );
}
