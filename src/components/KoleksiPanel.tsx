interface KoleksiPanelProps {
  collections: string[] | undefined;
}

/**
 * Klasifikasi koleksi museum (chip). Tidak merender apa pun bila data kosong,
 * supaya halaman museum tanpa kategori bersumber tidak menyisakan bagian kosong.
 */
export default function KoleksiPanel({ collections }: KoleksiPanelProps) {
  if (!collections || collections.length === 0) return null;

  return (
    <div>
      <h2 className="text-lg">Klasifikasi koleksi</h2>
      <div className="mt-3 flex flex-wrap gap-2">
        {collections.map((category) => (
          <span key={category} className="chip capitalize">
            {category}
          </span>
        ))}
      </div>
    </div>
  );
}
