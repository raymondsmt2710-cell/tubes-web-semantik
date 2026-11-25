# Desain: Memperdalam Isi Pameran dan Memperkaya Galeri

**Tanggal:** 2026-02-14
**Status:** Disetujui (pengguna memilih "langsung aja" atas arah C)
**Plan:** `docs/superpowers/plans/2026-02-14-isi-pameran-galeri.md`

## Intent dan alasan

Halaman museum saat ini terasa tipis. Isi pameran rata-rata hanya 86 karakter
per item — satu baris yang mengulang judulnya. Galeri rata-rata 2,4 foto, dan
empat museum hanya punya satu foto. Yang diminta: isi pameran dan galeri
terasa **lebih penuh**.

## Sasaran

- Setiap entri isi pameran menjelaskan apa bendanya, dari masa/asal mana, dan
  kenapa penting — minimal 3 kalimat / 180 karakter.
- Entri pameran membawa metadata terstruktur (periode, asal, bahan, penanda
  andalan) sehingga informasi itu ikut masuk graf, bukan hanya prosa.
- Setiap foto galeri punya latar belakang ≥220 karakter dan 2–4 poin
  pengamatan.
- Ambang kedalaman ditegakkan otomatis supaya tidak surut lagi.

## Bukan sasaran

- Mengubah tata letak besar-besaran atau sistem desain.
- Menambah bagian naratif baru di luar pameran dan galeri (kronologi, tokoh).
- Mengubah status verifikasi data — semua tetap `perlu-verifikasi`.

## Anti-sasaran

- Mengarang nama benda, tahun, atau angka yang tidak didukung sumber.
- Memakai foto dari situs resmi museum (hak cipta tidak jelas).
- Menambah foto tanpa `credit`, `license`, dan `sourceUrl` lengkap.

## Kendala

- Sumber kebenaran tunggal: `data/museums.json` → `npm run generate:rdf` →
  `npm run upload:fuseki`. Tidak boleh ada data yang hanya hidup di RDF.
- Aplikasi membaca graf lewat SPARQL; properti baru harus dideklarasikan di
  ontologi **dan** ditarik di kueri, atau datanya tidak akan pernah tampil.
- Proyek memakai npm, bukan bun.

## Pendekatan yang dipertimbangkan

| | Isi | Trade-off | Hasil |
|---|---|---|---|
| **A** | Perdalam teks saja | Cepat, nol risiko foto; halaman tidak berubah strukturnya | Ditolak sendirian |
| **C** | Teks + bidang naratif baru (`period`, `origin`, `material`, `highlight`, `detail`) | Mengubah skema, validator, dua komponen; tidak bergantung pada ketersediaan foto | **Dipilih** |
| **B** | C + tambah 2–3 foto per museum | Paling penuh; verifikasi lisensi manual; 4 museum hanya punya 1 foto layak di Commons | Dikerjakan terbatas setelah C |

Alasan memilih C: permintaan pengguna menyentuh *isi pameran* lebih dulu
daripada jumlah gambar, dan kedalaman teks tidak bergantung pada apa yang
kebetulan tersedia berlisensi di Wikimedia Commons. B lalu dikerjakan sebatas
foto yang benar-benar layak.

## Keputusan yang diambil

**Oleh pengguna:**
- Arah C, dilanjutkan B secara terbatas.
- Boleh menambah sumber acuan baru; isi tidak harus terkurung pada sumber yang
  sudah tercantum sekarang.

**Oleh pembangun (bisa dikoreksi):**
- Enam datatype property baru: `exhibitPeriod`, `exhibitOrigin`,
  `exhibitMaterial`, `exhibitHighlight` (xsd:boolean), `imagePeriod`,
  `imageDetail` (satu triple per poin).
- Ambang ditegakkan sebagai **warning**, bukan error, supaya data lama tidak
  memblokir build — tapi nol warning dijadikan syarat selesai Task 6.
- `detail` disimpan sebagai beberapa triple `imageDetail`, bukan satu string
  bergaris pemisah, supaya bisa dibaca sebagai daftar di banyak tempat.
- Penulisan data dilakukan per bab (7 commit), bukan satu commit raksasa,
  supaya mudah ditinjau dan dibatalkan.

## Yang diserahkan ke pembangun

- Kalimat sebenarnya untuk 28 museum.
- Foto tambahan mana yang layak dipakai.
- Detail tata letak `ExhibitList` dua kolom, selama metadata kosong tidak
  menyisakan pemisah menggantung.
