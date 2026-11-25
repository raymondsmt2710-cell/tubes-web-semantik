import type { MuseumImage } from "@/lib/types";

interface MuseumGalleryProps {
  images: MuseumImage[];
  museumName: string;
}

/**
 * Galeri foto museum. Setiap foto tampil sebagai kartu: gambar, judul, latar
 * belakang singkat, lalu kredit serta lisensi. Kredit wajib terlihat karena
 * gambar berasal dari Wikimedia Commons dengan lisensi berbeda-beda.
 */
export default function MuseumGallery({ images, museumName }: MuseumGalleryProps) {
  if (images.length === 0) return null;

  return (
    <section className="mt-12">
      <div className="flex items-baseline justify-between gap-4 border-b border-[--rule] pb-2">
        <h2 className="text-lg">Galeri</h2>
        <span className="label">{images.length} foto</span>
      </div>

      <ul className="mt-5 grid gap-6 sm:grid-cols-2">
        {images.map((image, index) => (
          <li
            key={image.src}
            className="border border-[--rule] bg-[--paper-2] rounded-sm overflow-hidden flex flex-col"
          >
            <figure className="m-0 flex flex-col h-full">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src={image.src}
                alt={image.alt || image.title || `${museumName} — foto`}
                loading="lazy"
                className="w-full aspect-[4/3] object-cover border-b border-[--rule]"
              />
              <figcaption className="px-4 py-3.5 flex flex-col gap-2 flex-1">
                <div className="flex items-baseline justify-between gap-2">
                  <span className="label">
                    Foto {String(index + 1).padStart(2, "0")}
                  </span>
                  {image.period && (
                    <span className="label text-[--ink-faint]">{image.period}</span>
                  )}
                </div>
                {image.title && (
                  <h3 className="font-serif text-base leading-snug m-0">{image.title}</h3>
                )}
                {image.background && (
                  <p className="m-0 text-sm text-[--ink-soft] leading-relaxed">
                    {image.background}
                  </p>
                )}
                {image.detail && image.detail.length > 0 && (
                  <ul className="m-0 p-0 list-none mt-1 space-y-1 text-sm text-[--ink-soft] leading-relaxed">
                    {image.detail.map((point) => (
                      <li key={point} className="flex gap-2">
                        <span aria-hidden className="text-[--ink-faint] shrink-0">
                          —
                        </span>
                        <span>{point}</span>
                      </li>
                    ))}
                  </ul>
                )}
                <p className="m-0 mt-auto pt-2 text-xs text-[--ink-faint] leading-relaxed">
                  Foto: {image.credit} ·{" "}
                  {image.licenseUrl ? (
                    <a
                      href={image.licenseUrl}
                      target="_blank"
                      rel="noreferrer noopener"
                      className="underline decoration-[--rule]"
                    >
                      {image.license}
                    </a>
                  ) : (
                    image.license
                  )}{" "}
                  ·{" "}
                  <a
                    href={image.sourceUrl}
                    target="_blank"
                    rel="noreferrer noopener"
                    className="underline decoration-[--rule]"
                  >
                    Wikimedia Commons
                  </a>
                </p>
              </figcaption>
            </figure>
          </li>
        ))}
      </ul>
    </section>
  );
}
