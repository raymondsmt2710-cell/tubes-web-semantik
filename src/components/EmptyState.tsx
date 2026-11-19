interface EmptyStateProps {
  hasFilters: boolean;
  onReset?: () => void;
}

export default function EmptyState({ hasFilters, onReset }: EmptyStateProps) {
  return (
    <div className="border border-[--rule] bg-[--paper-2] rounded-sm px-6 py-12 text-center">
      <p className="label">{hasFilters ? "Tidak ada hasil" : "Katalog kosong"}</p>
      <h2 className="mt-3 text-xl">
        {hasFilters
          ? "Tidak ada museum yang cocok dengan penyaringan Anda."
          : "Belum ada data museum."}
      </h2>
      <p className="mt-2 text-sm text-[--ink-soft] measure mx-auto">
        {hasFilters
          ? "Coba longgarkan salah satu penyaring, atau kembali ke seluruh katalog."
          : "Basis data museum belum berisi entri. Pastikan berkas RDF sudah diunggah ke Fuseki."}
      </p>
      {hasFilters && onReset && (
        <button type="button" onClick={onReset} className="btn btn-ghost mt-6">
          Bersihkan penyaringan
        </button>
      )}
    </div>
  );
}
