# Laporan verifikasi data museum (tugas A4)

Tanggal: 2026-11-26
Ruang lingkup: 28 museum di `data/museums.json`, bidang `name`, `city`,
`province`, `establishedYear`, `address`, `sources`, `verificationStatus`.

## Ringkasan

| Sebelum | Sesudah |
| --- | --- |
| 0 museum `terverifikasi` | **24 museum `terverifikasi`** |
| 24 museum hanya punya 1 sumber | **27 museum punya ≥2 sumber** |
| 4 museum punya 2 sumber | 1 museum tetap 1 sumber (tidak dapat diverifikasi) |
| `check:rdf` 28 peringatan | **4 peringatan** |

Empat museum tetap `perlu-verifikasi`: `museum-sisingamangaraja-xii`,
`museum-siginjai`, `rumah-pengasingan-bung-karno`, `museum-purbakala-pugung-raharjo`.

## Sumber yang dipakai

Urutan kepercayaan yang dipakai saat memilih sumber kedua:

1. **NPNM** — `museum.kemenbud.go.id`, direktori resmi museum ber-Nomor
   Pendaftaran Nasional Museum (Kementerian Kebudayaan). Ini otoritas tertinggi
   untuk keberadaan, alamat, dan tahun museum. 23 dari 28 museum terdaftar.
2. **`indonesia.travel`** — situs resmi Kementerian Pariwisata.
3. **Wikipedia** (id/en) dan **Wikidata**.
4. `museum.co.id` — **diturunkan ke pilihan terakhir** karena ditemukan
   kesalahan (lihat bagian "Sumber yang dibuang").

Catatan: `museum.kemdikbud.go.id`, `kebudayaan.kemdikbud.go.id`,
`referensi.data.kemdikbud.go.id`, dan `sipentas.kemdikbud.go.id` tidak dapat
dihubungi (DNS gagal). Domain yang benar adalah **`museum.kemenbud.go.id`**
(ejaan: kemenbud).

## Aturan tahun berdiri

`establishedYear` = **tahun pendirian/pembangunan**, bukan tahun peresmian.
Bila sumber hanya menyebut tahun peresmian, tahun itu yang dipakai. NPNM
menampilkan keduanya (label "Berdiri" kadang berisi tahun peresmian), jadi
tahun diambil dari prosa sejarah, bukan dari label.

## Perbedaan yang ditemukan dan diperbaiki

### Tahun berdiri salah

| Museum | Data lama | Data baru | Bukti |
| --- | --- | --- | --- |
| `museum-adityawarman` | 1950 | **1974** | NPNM: "mulai dibangun pada tahun anggaran 1974/1975, diresmikan 16 Maret 1977". 1950 tidak disebut sumber mana pun. |
| `museum-sang-nila-utama` | 1976 | **1991** | Wikipedia: "didirikan pada tanggal 9 Januari 1991 melalui SK Mendikbud Nomor 001/0/1991". NPNM "Berdiri 1991". |
| `museum-negeri-lampung` | 1988 | **1975** | NPNM + Wikipedia: "mulai dibangun sejak tahun 1975", batu pertama 1978, diresmikan 24 September 1988. |
| `museum-negeri-jambi` | 1986 | **1981** | Wikipedia: "dibangun pada tanggal 18 Februari 1981 ... diresmikan 6 Juni 1988". NPNM "Berdiri 1981". |
| `museum-tsunami-aceh` | 2009 | **2007** | NPNM: "didirikan ... pada tahun 2007", diresmikan 2009, dibuka publik 2011. |

### Tahun berdiri kosong lalu diisi

| Museum | Tahun | Bukti |
| --- | --- | --- |
| `museum-malikussaleh` | **2011** | NPNM + Wikipedia: "dibangun secara bertahap mulai tahun 2011 sampai dengan 2016". |
| `museum-huta-bolon-simanindo` | **1969** | NPNM: "didirikan pada tahun 1969". |
| `museum-daerah-deli-serdang` | **2001** | NPNM: "dibangun pada tahun 2001", diresmikan 12 Agustus 2003, diresmikan ulang 2018. |
| `museum-sultan-sulaiman-badrul-alamsyah` | **2009** | NPNM: "diresmikan oleh Walikota Tanjungpinang pada 31 Januari 2009". |
| `museum-linggam-cahaya` | **2002** | NPNM: "pembangunannya dimulai pada Agustus 2002 dan selesai pada 7 Mei 2003". |
| `museum-istana-siak` | **1989** | NPNM "Berdiri 1989"; bangunan istana sendiri mulai dibangun 1889 (Wikipedia). |
| `museum-rumah-kelahiran-buya-hamka` | **2001** | NPNM: "diresmikan pada tanggal 11 November 2001". |
| `museum-tuanku-imam-bonjol` | **1990** | NPNM "Berdiri 1990". |
| `museum-kereta-api-sawahlunto` | **2003** | NPNM "Berdiri 2003"; diresmikan 17 Desember 2005; bangunan stasiun 1902. |
| `museum-sultan-mahmud-badaruddin-ii` | **2009** | NPNM "Berdiri 2009". |
| `museum-taman-purbakala-sriwijaya` | **2008** | NPNM "Berdiri 2008". |
| `museum-ketransmigrasian-lampung` | **2004** | NPNM: "berdiri sejak Tahun 2004". |
| `museum-cut-nyak-dhien` | **1983** | Wikidata Q137460742: P571 = 1983 (P1619 = 1987). |

### Alamat salah

| Museum | Data lama | Data baru | Bukti |
| --- | --- | --- | --- |
| `museum-negeri-lampung` | `Jl. Dr. Ryacudu` | **`Jl. H. Zainal Arifin Pagar Alam No. 64`** | NPNM + Wikipedia. `Jl. Dr. Ryacudu` tidak disebut sumber mana pun. |
| `museum-negeri-jambi` | `Jl. Urip Sumoharjo` | `Jl. Urip Sumoharjo No. 1` | NPNM + Wikipedia ("Nomor 1"). |
| `museum-kereta-api-sawahlunto` | `Jl. Raya Sawahlunto` | **`Jl. Ahmad Yani`** | NPNM. |
| `museum-tb-silalahi-center` | `Jl. Patuan Nagari` | **`Jl. Dr. TB Silalahi No. 88`** | NPNM. |
| `museum-sultan-mahmud-badaruddin-ii` | `Jl. Merdeka` | **`Jl. Sultan Mahmud Badaruddin II No. 2`** | NPNM. |
| `museum-negeri-sumatera-selatan` | `Jl. Srijaya Negara` | **`Jl. Srijaya I No. 288 KM. 5,5`** | NPNM. |
| `museum-negeri-aceh` | `Jl. Sultan Mahmudsyah` | `Jl. Sultan Alaiddin Mahmudsyah` | NPNM (nama jalan lengkap). |

Alamat lain dilengkapi (nama gampong/jorong/kecamatan) tanpa mengubah jalan:
`museum-tsunami-aceh`, `museum-cut-nyak-dhien`, `museum-malikussaleh`,
`museum-negeri-sumatera-utara`, `museum-huta-bolon-simanindo`,
`museum-daerah-deli-serdang`, `museum-sultan-sulaiman-badrul-alamsyah`,
`museum-linggam-cahaya`, `museum-rumah-kelahiran-buya-hamka`,
`museum-tuanku-imam-bonjol`, `museum-negeri-bengkulu`,
`museum-ketransmigrasian-lampung`, `museum-purbakala-pugung-raharjo`.

### Sumber lama yang rusak atau tidak mendukung

| Museum | Masalah | Tindakan |
| --- | --- | --- |
| `museum-purbakala-pugung-raharjo` | `id.wikipedia.org/wiki/Pugung_Raharjo` → **HTTP 404** | Diganti `Taman_Purbakala_Pugung_Raharjo` (200) |
| `museum-malikussaleh` | Sumber satu-satunya adalah berkas Commons (`File:Museum_Islam_Samudra_Pasai_2.jpg`) — foto, bukan sumber keterangan | Diganti Wikipedia + NPNM + indonesia.travel |
| `museum-tb-silalahi-center` | Sumber satu-satunya berkas Commons | Diganti NPNM + indonesia.travel |
| `museum-istana-siak` | Sumber satu-satunya berkas Commons | Diganti Wikipedia + NPNM + indonesia.travel |
| `museum-negeri-bengkulu` | Sumber satu-satunya berkas Commons | Diganti Wikipedia + NPNM + indonesia.travel |
| `museum-negeri-sumatera-selatan` | Sumber satu-satunya berkas Commons | Diganti Wikipedia + NPNM + indonesia.travel |
| `museum-negeri-lampung` | Sumber satu-satunya berkas Commons | Diganti Wikipedia + NPNM + indonesia.travel |
| `museum-taman-purbakala-sriwijaya` | Sumber satu-satunya berkas Commons | Diganti Wikipedia + NPNM + indonesia.travel |
| `museum-ketransmigrasian-lampung` | Sumber satu-satunya berkas Commons | Diganti Wikipedia + NPNM + indonesia.travel |
| `museum-negeri-aceh` | Sumber kedua adalah artikel Museum Tsunami Aceh — tidak relevan | Diganti NPNM + indonesia.travel |
| `museum-negeri-jambi` | Sumber Commons + `museum.co.id` | Diganti Wikipedia + NPNM |
| `museum-siginjai` | Sumber `museum.co.id` (berisi alamat salah) | Dibiarkan (lihat temuan di bawah) |

**Pelajaran:** berkas Wikimedia Commons adalah sumber untuk **foto**, bukan
untuk fakta museum. Ia dipakai di `gallery[].sourceUrl`, bukan di `sources`.

### Sumber yang dibuang

`museum.co.id` diturunkan ke pilihan terakhir setelah ditemukan:

- Halaman "Museum Bung Karno" berisi **Museum Bung Karno di Bali**
  (`Jl. Pegangsaan Timur 56`, Denpasar Selatan), bukan rumah pengasingan di
  Bengkulu.
- `museum-siginjai-jamb` memberi alamat `Jl. Prof. Dr. Sri Soedewi`, sedangkan
  NPNM dan Wikipedia sama-sama menyebut `Jl. Urip Sumoharjo No. 01`.
- Data koordinat Deli Serdang tidak cocok dengan lokasi sebenarnya.

### Catatan kejujuran: tahun yang bersandar pada satu sumber

Untuk sebagian museum, **nama, kota, dan provinsi** cocok di dua sumber atau
lebih, tetapi **tahun berdirinya** hanya disebut satu sumber. Tahun-tahun itu
tetap diisi karena sumbernya otoritatif (NPNM atau Wikidata), bukan karena
ditebak:

- Dari **NPNM saja**: `museum-huta-bolon-simanindo`, `museum-tb-silalahi-center`,
  `museum-daerah-deli-serdang`, `museum-sultan-sulaiman-badrul-alamsyah`,
  `museum-linggam-cahaya`, `museum-istana-siak`, `museum-tuanku-imam-bonjol`,
  `museum-kereta-api-sawahlunto`, `museum-sultan-mahmud-badaruddin-ii`,
  `museum-taman-purbakala-sriwijaya`, `museum-ketransmigrasian-lampung`.
- Dari **Wikidata saja**: `museum-cut-nyak-dhien` (1983),
  `museum-timah-indonesia` (1997).

Tahun yang disebut **dua sumber atau lebih**: `museum-adityawarman` (1974),
`museum-sang-nila-utama` (1991), `museum-negeri-lampung` (1975),
`museum-negeri-jambi` (1981), `museum-malikussaleh` (2011),
`museum-tsunami-aceh` (2007).

## Temuan yang TIDAK diubah (perlu keputusan pemilik data)

### 1. `museum-negeri-jambi` dan `museum-siginjai` adalah museum yang sama

Keduanya merujuk satu museum:

- NPNM memberi **nomor pendaftaran identik**: `15.71.U.03.0014`.
- Keduanya beralamat `Jl. Urip Sumoharjo No. 01`.
- Wikipedia memiliki **satu** artikel untuk keduanya: "Museum Siginjei Jambi",
  yang menyebut museum ini dulu bernama Museum Negeri Provinsi Jambi, lalu
  berganti nama menjadi Museum Siginjei pada 30 Oktober 2012.

Akibatnya data sekarang menghitung satu museum dua kali, dengan dua tahun
berdiri berbeda (1981 dan 1988) dan dua alamat berbeda. **Tidak diubah** karena
perbaikan ini berarti menggabungkan/menghapus record, yang mengubah jumlah
museum, peta, dan TTL. Perlu keputusan pemilik data.

Tiga foto `museum-siginjai` berasal dari **Museum Perjuangan Rakyat Jambi**
(`Jl. Prof. Dr. Sri Soedewi`), museum yang berbeda — ini menjelaskan asal alamat
yang salah.

### 2. `museum-sisingamangaraja-xii` tidak dapat diverifikasi

Tidak ditemukan di sumber mana pun:

| Sumber | Hasil |
| --- | --- |
| NPNM, 19 museum Sumatera Utara | tidak terdaftar |
| Wikipedia id/en (artikel museum) | tidak ada artikel |
| "Daftar museum di Sumatera Utara" (Wikipedia, 19 entri) | tidak tercantum |
| `indonesia.travel` (564 halaman Sumatra) | tidak ada |
| `museum.co.id` (semua listing + pencarian situs) | tidak ada |
| Wikidata (id + en) | tidak ada entitas museum |
| OpenStreetMap/Overpass | API tidak dapat dihubungi (502/504) |

Satu-satunya sumber yang ada adalah artikel **biografi** Sisingamangaraja XII,
yang tidak menyebut museum. `establishedYear` kosong dan alamat tidak
terkonfirmasi.

Wikipedia "Balige, Toba" menyebut kecamatan Balige berisi "Museum Batak, Museum
T.B. Silalahi Center, dan **Makam** Pahlawan Nasional Si Singamangaraja XII" —
makam, bukan museum. `museum-tb-silalahi-center` sudah menjadi record terpisah.

Sesuai tugas A4 ("jangan dipaksa"), record dibiarkan `perlu-verifikasi` dengan
sumber seadanya. Test `test_setiap_museum_punya_minimal_dua_sumber` memakai
daftar pengecualian eksplisit (`SUMBER_DIKECUALIKAN`) yang mencantumkan alasan,
dan `test_pengecualian_sumber_masih_relevan` memastikan pengecualian itu dihapus
begitu museumnya berhasil diverifikasi.

### 3. `museum-timah-indonesia`: kota benar, tetapi artikel Wikipedia tentang cabang lain

NPNM tidak mendaftarkan museum ini. Wikidata Q109430877 berlabel "Museum Timah
Indonesia – Pangkalpinang" (P131 = Pangkalpinang, P571 = 1997), dan
`indonesia.travel` berjudul "Museum Timah Indonesia, Wisata Edukasi di
Pangkalpinang". Jadi kota dan tahun **terkonfirmasi**.

Namun artikel Wikipedia yang tersedia adalah "Museum Timah Indonesia **Muntok**"
(Kabupaten Bangka Barat), yang diresmikan 7 November 2013 — museum berbeda di
lokasi berbeda. Sumber ini dipakai sebagai konteks sejarah timah Bangka, bukan
sebagai bukti lokasi. Bila ketelitian tinggi dibutuhkan, ganti dengan sumber
khusus Pangkalpinang.

### 4. NPNM kadang bertentangan dengan prosanya sendiri

Label "Berdiri" pada NPNM kadang berisi tahun peresmian, bukan tahun pendirian,
dan kadang berbeda dari prosa di halaman yang sama. Contoh `museum-daerah-deli-serdang`:
label "Berdiri 2016", prosa "dibangun 2001 ... diresmikan 12 Agustus 2003 ...
diresmikan 8 September 2018". Karena itu tahun diambil dari prosa sejarah.

### 5. `rumah-pengasingan-bung-karno` tetap `perlu-verifikasi`

Tiga sumber tersedia (Wikipedia id, Wikipedia en, Wikidata Q16878966) dan
semuanya saling mendukung: rumah pengasingan Soekarno di Bengkulu, 1938–1942.
Tetap `perlu-verifikasi` karena tahun 1938 adalah tahun **Soekarno mulai
diasingkan di sana**, bukan tahun bangunan dijadikan museum, dan tidak ada
sumber yang menyebut tahun peresmian museumnya.

## Pemeriksaan akhir

```
pytest                    218 passed
npm test                  200 passed
npm run check:rdf         0 error, 4 warning (semuanya verificationStatus)
cek_ontologi.py           lulus, tidak ada temuan
closure                   4113 asserted -> 7695 (OWL-RL) / 6853 (RDFS), konsisten
museum / foto / sumber    28 museum, 75 foto, 77 node Source
```
