# Menyiapkan Apache Jena Fuseki

Panduan ini memakai dataset bernama `museum`. Nama itu penting karena menjadi
bagian dari URL endpoint: `http://localhost:3030/museum/query`.

## 1. Unduh dan jalankan Fuseki

1. Unduh Apache Jena Fuseki dari <https://jena.apache.org/download/>.
2. Ekstrak arsipnya, lalu jalankan dari folder hasil ekstrak:
   - Windows: `fuseki-server.bat`
   - Linux/macOS: `./fuseki-server`
3. Buka <http://localhost:3030>. Halaman pengelolaan Fuseki akan tampil.

Alternatif Docker (opsional):

```bash
docker run -d --name fuseki -p 3030:3030 -e ADMIN_PASSWORD=admin stain/jena-fuseki
```

Dengan Docker, buka `http://localhost:3030` dan masuk memakai pengguna `admin`.

## 2. Buat dataset `museum`

Lewat UI:

1. Klik **Manage datasets** → **Add new dataset**.
2. Isi:
   - Dataset name: `museum`
   - Dataset type: **TDB2** (persisten; pilih *in-memory* hanya untuk uji
     sementara)
3. Simpan. Fuseki membuat endpoint:
   - Query: `http://localhost:3030/museum/query`
   - Update/Graph Store: `http://localhost:3030/museum/data`

## 3. Unggah RDF

### Cara A — skrip proyek (disarankan)

1. Salin `.env.example` menjadi `.env`.
2. Pastikan isinya:

   ```env
   FUSEKI_ENDPOINT=http://localhost:3030/museum/query
   FUSEKI_UPDATE=http://localhost:3030/museum/data
   ```

3. Dari akar proyek:

   ```bash
   npm run generate:rdf
   npm run upload:fuseki
   ```

   Skrip ini mengosongkan graph default lewat Graph Store Protocol
   (`DELETE` pada `FUSEKI_UPDATE?default`) lalu mengunggah
   `data/museum-sumatera.rdf` sebagai RDF/XML ke graph default.

### Cara B — lewat UI Fuseki

1. Buka dataset `museum`, pilih tab **Add data**.
2. Pilih **Upload file**, pilih `data/museum-sumatera.rdf`.
3. Pastikan target graph adalah **default graph**, lalu unggah.

Bila sebelumnya sudah pernah mengunggah data lama, kosongkan graph default
terlebih dahulu (**Delete data** → *Delete default graph* atau jalankan
`CLEAR DEFAULT` di tab Update) agar tidak ada sisa entri.

## 4. Verifikasi

Di tab **Query** dataset `museum`, jalankan:

```sparql
PREFIX sdp: <https://museumsumatera.id/ontology#>
SELECT (COUNT(*) AS ?n) WHERE { ?s a sdp:Museum }
```

Hasil yang diharapkan: **28**.

Coba juga sebaran per provinsi:

```sparql
PREFIX sdp: <https://museumsumatera.id/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?province (COUNT(?museum) AS ?jumlah)
WHERE {
  ?museum a sdp:Museum ;
          sdp:locatedInProvince ?p .
  ?p rdfs:label ?province .
}
GROUP BY ?province
ORDER BY DESC(?jumlah)
```

## 5. Hubungkan ke situs

`.env` di akar proyek:

```env
FUSEKI_ENDPOINT=http://localhost:3030/museum/query
```

Lalu jalankan `npm run dev` dan buka <http://localhost:3000>. Sampul akan
menampilkan jumlah museum per bab bila sambungan berhasil.

Bila memakai URL atau nama dataset lain, cukup ubah `FUSEKI_ENDPOINT` — tidak
ada alamat Fuseki yang ditulis di kode aplikasi.

## Pemecahan masalah

| Gejala | Kemungkinan penyebab |
|---|---|
| `404 Dataset not found` | Nama dataset bukan `museum`, atau path endpoint salah. Cek di UI Fuseki. |
| `Basis data museum menolak permintaan` (502) | Kueri gagal di server. Lihat log Fuseki; pastikan dataset memakai TDB2 dan RDF sudah terunggah. |
| Katalog berkata "Belum ada data museum" | Dataset kosong, atau data terunggah ke graph bernama padahal aplikasi membaca graph default. |
| `Tidak dapat terhubung ke basis data museum` | Fuseki belum berjalan, port berbeda, atau `FUSEKI_ENDPOINT` salah. |
| Situs jalan tetapi semua jumlah bab `—` | Sama seperti di atas; sampul sengaja tetap merender narasi saat basis data mati. |
| Port 3030 sudah dipakai | Hentikan proses lain atau jalankan Fuseki dengan `--port` lain, lalu sesuaikan `.env`. |

Catatan: browser tidak pernah menghubungi Fuseki secara langsung. Semua kueri
melewati route handler Next.js di sisi server, jadi CORS tidak perlu diatur.
