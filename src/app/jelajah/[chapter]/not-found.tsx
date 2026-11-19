import Link from "next/link";

export default function ChapterNotFound() {
  return (
    <div className="min-h-screen paper-texture flex items-center justify-center px-5">
      <div className="max-w-md text-center">
        <p className="label">Bab tidak ditemukan</p>
        <h1 className="mt-3 text-2xl">Alur pameran ini hanya punya tujuh bab</h1>
        <p className="mt-3 text-sm text-[--ink-soft]">
          Nomor bab yang Anda buka tidak ada. Kembali ke sampul untuk memilih bab
          lain, atau langsung ke katalog.
        </p>
        <div className="mt-6 flex justify-center gap-3">
          <Link href="/" className="btn">
            Kembali ke sampul
          </Link>
          <Link href="/katalog" className="btn btn-ghost">
            Katalog
          </Link>
        </div>
      </div>
    </div>
  );
}
