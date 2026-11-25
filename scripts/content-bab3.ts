import { patches, apply } from "./apply-content.ts";

// ── Bab III: Riau, Kepulauan Riau, dan jejak Melayu ──────────────────────────

patches["museum-sang-nila-utama"] = {
  exhibits: [
    {
      title: "Pakaian adat pernikahan Melayu",
      period: "tradisi Melayu Riau",
      origin: "Masyarakat Melayu Riau",
      material: "kain tenun, sulaman, dan perhiasan",
      highlight: true,
      description:
        "Busana pernikahan tradisional Riau ini dipamerkan lengkap dengan perlengkapannya. Dalam adat Melayu, pakaian pernikahan bukan sekadar kostum, melainkan penanda status dan urutan upacara, sehingga setiap lapisan kain dan hiasan kepala punya nama serta aturan pemakaiannya. Warna dan coraknya berbeda menurut daerah, misalnya antara pesisir dan pedalaman. Karena itu satu set busana bisa menjelaskan banyak hal tentang adat setempat dalam sekali pandang.",
    },
    {
      title: "Alat musik dan permainan tradisional",
      period: "abad ke-19 hingga ke-20",
      origin: "Riau daratan dan pesisir",
      material: "kayu, kulit, dan logam",
      description:
        "Ruang ini memuat koleksi alat musik Melayu Riau serta permainan rakyat yang kini jarang dimainkan. Alat musik seperti gambus dan rebana berkaitan dengan kesenian yang biasa tampil pada acara adat dan keagamaan. Permainan rakyat ditempatkan berdekatan karena keduanya sama-sama bertahan lewat kebiasaan, bukan benda pameran. Bagi museum, menampilkan keduanya adalah cara mendokumentasikan kegiatan yang sulit direkam hanya dengan foto, yaitu bunyi dan aturan main.",
    },
    {
      title: "Fosil, miniatur candi, dan mata uang",
      period: "prasejarah hingga masa klasik",
      origin: "Kawasan Riau dan sekitarnya",
      material: "fosil batu, keramik, dan logam",
      description:
        "Koleksi ini berisi fosil batu siput, miniatur candi dan masjid, serta mata uang lama yang menunjukkan jejak sejarah kawasan. Fosil siput memberi petunjuk bahwa sebagian wilayah Riau pernah berada di bawah laut, sedangkan miniatur candi dan masjid menandai peralihan masa keagamaan. Mata uang lama menunjukkan kawasan ini terhubung jaringan dagang maritim yang luas. Karena benda-bendanya berasal dari masa yang sangat berbeda, ruang ini disusun sebagai potongan-potongan sejarah yang saling melengkapi.",
    },
    {
      title: "Keramik dan sepeda zaman dahulu",
      period: "abad ke-19 hingga ke-20",
      origin: "Rumah tangga masyarakat Riau",
      material: "keramik, batik, dan logam",
      description:
        "Keramik, batik, dan sepeda kuno di ruang ini menggambarkan kehidupan sehari-hari masyarakat Riau. Keramik Tiongkok dan Eropa menjadi barang penting rumah tangga sekaligus penanda kemampuan ekonomi pemiliknya pada masa lalu. Batik menunjukkan hubungan dagang dengan Jawa, sedangkan sepeda menggambarkan masuknya kendaraan pribadi pada awal abad ke-20. Museum menempatkan benda rumah tangga seperti ini agar pengunjung melihat sisi keseharian, bukan hanya upacara dan kebesaran.",
    },
  ],
  gallery: [
    {
      src: "/1.jpg",
      period: "sekitar 4.195 koleksi pada 2005",
      detail: [
        "Interior ini memperlihatkan ruang pamer dengan deretan tiang jingga dan lemari kaca di sepanjang balkon.",
        "Museum menempati bangunan dua lantai di kompleks Dinas Kebudayaan Provinsi Riau.",
        "Pada 2005 tercatat sekitar 4.195 koleksi.",
        "Isinya beragam, dari fosil, keramik, pakaian adat, sampai sepeda kuno.",
      ],
    },
    {
      src: "/2.jpg",
      period: "didirikan 9 Januari 1991",
      detail: [
        "Gedung ini adalah Museum Negeri Provinsi Riau yang didirikan 9 Januari 1991.",
        "Nama Sang Nila Utama mulai dipakai pada 13 Oktober 1993.",
        "Nama itu merujuk raja Bintan abad ke-13.",
        "Setelah kewenangan daerah berubah pada 1999, statusnya menjadi museum daerah di bawah Dinas Kebudayaan Riau.",
      ],
    },
  ],
};

patches["museum-sultan-sulaiman-badrul-alamsyah"] = {
  exhibits: [
    {
      title: "Duplikat cogan Johor–Riau–Lingga",
      period: "masa Kesultanan Johor–Riau–Lingga",
      origin: "Kesultanan Johor–Riau–Lingga",
      material: "emas, perak, dan permata mirah",
      highlight: true,
      description:
        "Cogan adalah alat kebesaran kerajaan yang dalam upacara berfungsi sebagai penanda kekuasaan sultan. Duplikat di museum ini dibuat dari emas dan perak bertahtakan permata mirah, dengan lempengan emas berbentuk daun sirih berinsikripsi Arab Melayu. Tulisan Arab Melayu itu menunjukkan bahwa kebudayaan Melayu dan tradisi Islam menyatu dalam simbol kerajaan. Karena yang dipamerkan adalah duplikat, benda ini menjelaskan bahwa cogan asli sering tidak lagi berada di tempat asalnya.",
    },
    {
      title: "Ruang Tanjungpinang Kota Bermula",
      period: "abad ke-18 hingga ke-20",
      origin: "Tanjungpinang, Pulau Bintan",
      material: "panel, peta, dan foto lama",
      description:
        "Ruang ini mengisahkan awal terbentuknya Tanjungpinang sebagai kota pelabuhan. Letaknya di Pulau Bintan menjadikannya titik persinggahan kapal yang berlayar antara Selat Malaka dan Laut Cina Selatan, sehingga kota tumbuh dari perdagangan dan administrasi, bukan dari pertanian. Kisahnya berkaitan langsung dengan Kesultanan Johor–Riau–Lingga yang berpusat di kawasan ini pada beberapa periode. Bagi pengunjung, ruang ini menjelaskan mengapa Tanjungpinang punya bangunan kolonial dan tata kota pesisir seperti sekarang.",
    },
    {
      title: "Ruang Budaya Bahari dan Keramik",
      period: "abad ke-14 hingga ke-19",
      origin: "Jalur perdagangan maritim Kepulauan Riau",
      material: "keramik, kendi, piring, dan guci",
      description:
        "Keramik, kendi, piring, dan guci di ruang ini mencerminkan jalur perdagangan maritim Kepulauan Riau. Barang-barang itu berasal dari Tiongkok, Asia Tenggara, dan Eropa, sehingga warnanya berbeda menurut asal dan masa pembuatannya. Bagi penduduk pesisir, keramik bukan hanya perkakas tetapi juga barang simpanan yang diwariskan. Karena Kepulauan Riau berada di tengah jalur pelayaran, temuan keramik di sini bisa dipakai untuk menelusuri ramainya perdagangan beberapa abad silam.",
    },
    {
      title: "Ruang Alam Perkawinan Melayu",
      period: "tradisi Melayu Kepulauan Riau",
      origin: "Masyarakat Melayu Tanjungpinang",
      material: "busana, perlengkapan upacara, dan panel",
      description:
        "Ruang ini menampilkan benda dan tata cara perkawinan adat Melayu sebagai satu kesatuan. Yang dipamerkan bukan hanya busana, tetapi juga urutan upacara seperti tepuk tepung tawar dan pemberian gelar, yang berbeda antara satu daerah dan daerah lain. Tata cara ini biasanya dijelaskan lewat gambar dan panel karena berlangsung dalam waktu tertentu. Menempatkannya sebagai ruang khusus menunjukkan bahwa pernikahan Melayu dipandang sebagai peristiwa adat yang melibatkan keluarga besar, bukan urusan pribadi semata.",
    },
    {
      title: "Temuan neolitikum",
      period: "masa neolitikum",
      origin: "Kawasan Kepulauan Riau",
      material: "batu andesit",
      description:
        "Ruang ini memuat kapak genggam, kapak batu, dan beliung persegi berbahan andesit dari koleksi prasejarah. Beliung persegi adalah penanda penting masa neolitikum karena dipakai untuk mengolah kayu dan membuka lahan, tidak sekadar berburu. Temuan seperti ini menunjukkan bahwa pulau-pulau kecil di Kepulauan Riau sudah dihuni jauh sebelum munculnya kerajaan maritim. Bagi museum, benda batu sederhana ini menjadi titik awal alur sejarah sebelum masuk ke masa kesultanan dan kolonial.",
    },
  ],
  gallery: [
    {
      src: "/1.jpg",
      period: "menjadi museum 31 Januari 2009",
      detail: [
        "Bangunan beratap limas ini dahulu Holland Irlandsch School (HIS), sekolah dasar pertama di Tanjungpinang.",
        "Pada masa pendudukan Jepang namanya berubah menjadi Futsuko Gakka I.",
        "Setelah kemerdekaan bangunan dipakai sebagai Sekolah Rakyat.",
        "Sejak 31 Januari 2009 tempat ini menjadi museum.",
      ],
    },
  ],
};

patches["museum-linggam-cahaya"] = {
  exhibits: [
    {
      title: "Al-Qur'an tulisan tangan",
      period: "abad ke-19",
      origin: "Kesultanan Riau-Lingga",
      material: "kertas, sebagian dedaunan dan kulit hewan",
      highlight: true,
      description:
        "Mushaf kuno ini ditulis tangan, sebagian pada dedaunan dan kulit hewan, menunjukkan tradisi Islam di Lingga. Mushaf abad ke-19 dari Kesultanan Riau-Lingga ini beriluminasi khas Pantai Timur Semenanjung. Selain sebagai kitab, mushaf seperti ini adalah benda seni: pola hiasnya menunjukkan percampuran tradisi Melayu dengan pengaruh Islam dari Timur Tengah dan India. Karena ditulis tangan, setiap mushaf berbeda, dan gaya tulisnya bisa menjadi petunjuk tempat pembuatannya.",
    },
    {
      title: "Perhiasan adat Melayu",
      period: "masa Kesultanan Lingga",
      origin: "Masyarakat Melayu Lingga",
      material: "logam dan kain sulaman",
      description:
        "Ruang ini memuat aneka perhiasan serta tudung manto yang menjadi ciri busana Melayu Lingga. Tudung manto adalah penutup kepala bersulam yang dikenakan pada acara adat, dan bentuknya berbeda dari busana Melayu di daerah lain. Perhiasan menunjukkan tingkat kemampuan ekonomi pemakainya, sehingga benda seperti ini juga menandai kedudukan sosial. Karena Lingga pernah menjadi pusat kesultanan, gaya busananya dipengaruhi oleh istana dan menyebar ke masyarakat sekitarnya.",
    },
    {
      title: "Alat tangkap ikan tradisional",
      period: "kehidupan pesisir Lingga",
      origin: "Perairan Lingga",
      material: "rotan, bambu, dan jaring",
      description:
        "Peralatan menangkap hasil laut ini mencerminkan kedekatan masyarakat Lingga dengan perairan. Lingga terdiri atas pulau-pulau kecil yang dikelilingi laut, sehingga sebagian besar penduduknya bergantung pada tangkapan harian. Bentuk alat tangkap berbeda menurut jenis ikan dan kedalaman air, dan pengetahuan semacam ini diwariskan secara lisan. Bagi museum, peralatan seperti ini merekam pengetahuan praktis yang mudah hilang ketika pekerjaan berubah, bukan hanya benda yang indah dipandang.",
    },
    {
      title: "Porselen dan buli-buli",
      period: "abad ke-18 hingga ke-19",
      origin: "Jalur dagang Tiongkok dan Eropa",
      material: "porselen",
      description:
        "Perkakas rumah tangga berbahan porselen ini bermotif khas Melayu dan dipakai dalam kehidupan sehari-hari. Buli-buli, wadah kecil bertutup, biasanya dipakai untuk menyimpan minyak atau obat, dan bentuknya mudah dikenali di ruang pamer. Motif pada porselen menunjukkan perpaduan selera lokal dengan barang impor dari Tiongkok dan Eropa. Karena Lingga berada di jalur pelayaran, keberadaan porselen seperti ini sekaligus bukti bahwa kawasan ini terhubung dengan perdagangan jarak jauh.",
    },
  ],
  gallery: [
    {
      src: "/1.jpg",
      period: "abad ke-19",
      detail: [
        "Mushaf abad ke-19 ini berasal dari Kesultanan Riau-Lingga.",
        "Iluminasinya khas Pantai Timur Semenanjung.",
        "Selain sebagai kitab, mushaf seperti ini adalah benda seni.",
        "Pola hiasnya menunjukkan percampuran tradisi Melayu dengan pengaruh Islam dari Timur Tengah dan India.",
      ],
    },
  ],
};

patches["museum-istana-siak"] = {
  exhibits: [
    {
      title: "Bangunan Istana Siak",
      period: "dibangun masa Sultan Assyaidis Syarif Hasyim",
      origin: "Siak Sri Indrapura",
      material: "batu, kaca, dan kayu",
      highlight: true,
      description:
        "Istana itu sendiri adalah pameran utama: arsitektur Melayu dengan ornamen dan tata ruang kerajaan. Fasadnya berwarna krem dan memadukan bentuk Eropa seperti menara, jendela lengkung runcing, dan pintu melengkung dengan tata ruang istana Melayu. Perpaduan itu bukan kebetulan, karena istana dibangun pada masa Sultan Assyaidis Syarif Hasyim, ketika hubungan Siak dengan pemerintah Hindia Belanda cukup dekat. Karena itu bangunan ini bisa dibaca sebagai pernyataan politik lewat arsitektur, bukan hanya sebagai tempat tinggal sultan.",
    },
    {
      title: "Koleksi kebesaran kesultanan",
      period: "masa Kesultanan Siak",
      origin: "Istana Siak Sri Indrapura",
      material: "logam berlapis emas, kain, dan kayu",
      description:
        "Ruang-ruang istana dipakai memamerkan benda dan perlengkapan kebesaran kesultanan. Salah satu yang paling menonjol adalah kursi singgasana berlapis emas, yang dipajang dalam lemari kaca dengan label namanya. Singgasana adalah pusat upacara kerajaan: di sinilah sultan menerima pembesar dan tamu, sehingga posisinya dalam tata ruang istana menandai hierarki kekuasaan. Dengan mempertahankan benda di ruang aslinya, museum membuat pengunjung bisa membaca arti sebuah benda dari letaknya, bukan hanya dari keterangannya.",
    },
    {
      title: "Arsip foto Sultan Siak",
      period: "awal abad ke-20",
      origin: "Koleksi arsip kolonial",
      material: "foto studio",
      description:
        "Foto studio Sultan Siak dalam busana kebesaran berasal dari arsip kolonial awal abad ke-20. Potret semacam ini biasanya dibuat untuk kepentingan administrasi kolonial sekaligus sebagai penanda hubungan antara kesultanan dan pemerintah Hindia Belanda. Posisi duduk, pakaian, dan latar foto semuanya dipilih untuk menyampaikan wibawa. Bagi museum, arsip ini penting karena banyak bangunan dan upacara istana tidak lagi dapat disaksikan, sehingga foto menjadi satu-satunya gambaran yang tersisa.",
    },
  ],
  gallery: [
    {
      src: "/1.jpg",
      period: "awal abad ke-20",
      detail: [
        "Foto studio ini berasal dari arsip kolonial awal abad ke-20.",
        "Sultan Siak digambarkan dalam busana kebesaran.",
        "Potret semacam ini dibuat untuk kepentingan administrasi kolonial.",
        "Sekaligus menjadi penanda hubungan antara kesultanan dan pemerintah Hindia Belanda.",
      ],
    },
    {
      src: "/2.jpg",
      period: "masa Sultan Assyaidis Syarif Hasyim",
      detail: [
        "Istana berwarna krem ini memadukan bentuk Eropa dengan tata ruang istana Melayu.",
        "Unsur Eropa tampak pada menara, jendela lengkung runcing, dan pintu melengkung.",
        "Istana Siak Sri Indrapura dibangun pada masa Sultan Assyaidis Syarif Hasyim Abdul Jalil Syaifuddin.",
        "Kini menjadi museum yang menyimpan regalia kesultanan.",
      ],
    },
    {
      src: "/3.jpg",
      period: "masa Kesultanan Siak",
      detail: [
        "Kursi berlapis emas ini dipajang dalam lemari kaca.",
        "Labelnya berbunyi “Kursi Singgasana Kerajaan Siak Sri Indrapura”.",
        "Singgasana adalah pusat upacara kerajaan tempat sultan menerima pembesar dan tamu.",
        "Posisinya dalam tata ruang istana menandai hierarki kekuasaan.",
      ],
    },
  ],
};

apply();
