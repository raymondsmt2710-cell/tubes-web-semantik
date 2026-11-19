import Link from "next/link";

export default function MuseumNotFound() {
  return (
    <div className="min-h-screen paper-texture flex items-center justify-center px-5">
      <div className="max-w-md text-center">
        <p className="label">Museum tidak ditemukan</p>
        <h1 className="mt-3 text-2xl">Catatan museum ini tidak ada di arsip</h1>
        <p className="mt-3 text-sm text-[--ink-soft]">
          Slug yang Anda buka tidak cocok dengan entri mana pun. Mungkin tautannya
          sudah berubah, atau museum tersebut belum masuk ke dalam data.
        </p>
        <div className="mt-6 flex justify-center gap-3">
          <Link href="/katalog" className="btn">
            Telusuri katalog
          </Link>
          <Link href="/" className="btn btn-ghost">
            Kembali ke sampul
          </Link>
        </div>
      </div>
    </div>
  );
}
