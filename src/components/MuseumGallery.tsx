import type { MuseumImage } from "@/lib/types";

interface MuseumGalleryProps {
  images: MuseumImage[];
  museumName: string;
}

/**
 * Galeri foto museum. Setiap foto wajib menampilkan kredit dan lisensi, karena
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

      <ul className="mt-5 grid gap-5 sm:grid-cols-2">
        {images.map((image) => (
          <li key={image.src} className="border border-[--rule] bg-[--paper-2] rounded-sm">
            <figure className="m-0">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src={image.src}
                alt={image.alt || `${museumName} — foto`}
                loading="lazy"
                className="w-full aspect-[4/3] object-cover"
              />
              <figcaption className="px-3 py-2.5 text-xs text-[--ink-soft] leading-relaxed">
                {image.caption && <p className="m-0 mb-1 text-[--ink]">{image.caption}</p>}
                <p className="m-0 text-[--ink-faint]">
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
