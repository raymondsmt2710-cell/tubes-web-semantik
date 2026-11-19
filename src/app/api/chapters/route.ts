import { NextResponse } from "next/server";
import { runSelect, FusekiError } from "@/lib/sparql";
import { chaptersQuery } from "@/lib/queries";
import { CHAPTERS } from "@/lib/chapters";
import type { ChaptersResponse } from "@/lib/types";

export const dynamic = "force-dynamic";

export async function GET(): Promise<Response> {
  try {
    const rows = await runSelect(chaptersQuery());
    const counts = new Map<number, number>();

    for (const row of rows) {
      const index = Number(row.chapterIndex?.value);
      const count = Number(row.museumCount?.value);
      if (Number.isFinite(index)) counts.set(index, Number.isFinite(count) ? count : 0);
    }

    const body: ChaptersResponse = {
      chapters: CHAPTERS.map((chapter) => ({
        index: chapter.index,
        label: chapter.label,
        title: chapter.title,
        museumCount: counts.get(chapter.index) ?? 0,
      })),
    };

    return NextResponse.json(body);
  } catch (error) {
    const detail = error instanceof FusekiError ? error.message : String(error);
    return NextResponse.json(
      {
        error: "Tidak dapat terhubung ke basis data museum.",
        detail,
      },
      { status: 502 },
    );
  }
}
