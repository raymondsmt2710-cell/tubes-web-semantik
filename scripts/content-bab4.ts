import { patches, apply } from "./apply-content.ts";

// ── Bab IV: Sumatera Barat ───────────────────────────────────────────────────

patches["museum-adityawarman"] = {
  exhibits: [
    {
      title: "Duplikat patung Bhairawa dan Amoghapasa",
      period: "masa Kerajaan Dharmasraya, abad ke-13 hingga ke-14",
      origin: "Kerajaan Dharmasraya, hulu Batanghari",
      material: "batu",
      highlight: true,
      description:
        "Benda purbakala ini peninggalan Kerajaan Dharmasraya dan menjadi koleksi penting museum. Patung Bhairawa dan Amoghapasa termasuk temuan yang paling banyak dibicarakan karena menunjukkan pengaruh Hindu-Buddha di pedalaman Sumatera, jauh dari pusat kerajaan besar di Jawa. Yang dipamerkan di sini adalah duplikat, sementara sebagian temuan aslinya berada di museum lain atau masih di lokasi penemuan. Bagi pengunjung, duplikat tetap berguna karena bentuk dan ukurannya dibuat sepadan dengan aslinya.",
    },
    {
      title: "Rumah gadang dan rangkiang",
      period: "arsitektur tradisional Minangkabau",
      origin: "Sumatera Barat",
      material: "kayu, bambu, dan atap ijuk",
      highlight: true,
      description:
        "Bangunan berarsitektur Minang ini berdiri di halaman museum dan menjadikan kompleksnya semacam taman mini Sumatera Barat. Rumah gadang beratap melengkung seperti tanduk kerbau adalah rumah keluarga besar matrilineal, sedangkan rangkiang adalah lumbung padi yang berdiri di depannya. Letak rangkiang di halaman bukan sekadar penyimpanan, melainkan penanda bahwa rumah itu terhubung dengan pertanian. Dengan menghadirkan keduanya di halaman, museum menjelaskan hubungan antara bentuk rumah dan cara hidup masyarakatnya.",
    },
    {
      title: "Diorama adat matrilineal Minangkabau",
      period: "tradisi Minangkabau",
      origin: "Sumatera Barat",
      material: "diorama, panel, dan benda adat",
      description:
        "Ruang utama ini menjelaskan sistem kekerabatan Minangkabau, peran perempuan, sampai tradisi pantun. Minangkabau menganut garis keturunan ibu, sehingga rumah, tanah, dan gelar adat diwariskan lewat perempuan. Diorama dipakai karena sistem seperti ini tidak bisa dijelaskan hanya dengan satu benda: yang ditampilkan adalah hubungan antarpihak dalam keluarga. Tradisi pantun juga mendapat tempat karena banyak aturan adat disampaikan lewat tutur, bukan dokumen tertulis.",
    },
    {
      title: "Ruang peragaan pelaminan",
      period: "tradisi pernikahan Minang",
      origin: "Sumatera Barat",
      material: "kain sulaman, ukiran, dan perlengkapan upacara",
      description:
        "Pelaminan pernikahan adat Minang ini menjadi salah satu ruang paling diminati pengunjung. Susunannya menampilkan kursi pengantin berhias, kain sulaman, dan ukiran yang dipakai pada acara pernikahan. Dalam adat Minang, pelaminan menandai perpindahan status pengantin dan menjadi titik upacara, bukan hanya latar foto. Karena warna dan hiasannya beragam menurut daerah, satu pelaminan bisa menjelaskan banyak tentang adat suatu nagari.",
    },
    {
      title: "Koleksi Suku Mentawai",
      period: "budaya Mentawai",
      origin: "Kepulauan Mentawai",
      material: "kayu, rotan, dan bahan alam",
      description:
        "Benda budaya Mentawai ini ditampilkan berdampingan dengan koleksi Minangkabau. Kepulauan Mentawai berada di lepas pantai Sumatera Barat, tetapi kebudayaannya berbeda jauh dari Minangkabau: bahasanya berbeda, sistem kekerabatannya tidak matrilineal, dan banyak tradisinya berasal dari tradisi kepulauan yang lebih tua. Menempatkan keduanya dalam satu museum menunjukkan bahwa Sumatera Barat tidak tunggal. Karena itu ruang ini penting untuk memperlihatkan keragaman, bukan hanya kebudayaan mayoritas.",
    },
  ],
  gallery: [
    {
      src: "/1.jpg",
      period: "bangunan museum negeri",
      detail: [
        "Gedung utama ini menampung koleksi Sumatera Barat di Jalan Diponegoro, Padang.",
        "Museum mengambil nama Adityawarman, raja Malayapura pada abad ke-14.",
        "Di depannya berdiri rumah gadang, sehingga bangunan modern dan rumah adat terlihat sekaligus.",
        "Fungsinya sebagai museum negeri provinsi dan pusat penelitian kebudayaan.",
      ],
    },
    {
      src: "/2.jpg",
      period: "arsitektur panggung Minang",
      detail: [
        "Sudut bangunan memperlihatkan atap dan dinding yang memakai bentuk rumah adat Minangkabau.",
        "Atap melengkung seperti tanduk kerbau adalah ciri yang membedakannya dari rumah adat lain.",
        "Bangunan panggung menyisakan ruang di bawah lantai untuk menghindari kelembapan.",
        "Pilihan bentuk ini membuat museum tampil sebagai bagian kebudayaan, bukan gedung asing.",
      ],
    },
    {
      src: "/3.jpg",
      period: "arsitektur tradisional",
      detail: [
        "Rumah gadang berdiri di halaman museum dengan rangkiang atau lumbung padi di depannya.",
        "Atapnya melengkung dan biasanya bertingkat menurut jumlah ruang di dalamnya.",
        "Rumah ini menjadi milik keluarga besar matrilineal, diwariskan lewat garis ibu.",
        "Rangkiang menandai bahwa kehidupan rumah gadang terikat pada pertanian.",
      ],
    },
  ],
};

patches["museum-rumah-kelahiran-buya-hamka"] = {
  exhibits: [
    {
      title: "Rak buku karya Hamka",
      period: "1928–1981",
      origin: "Karya tulis Buya Hamka",
      material: "buku dan rak kaca",
      highlight: true,
      description:
        "Lima rak kaca ini berisi puluhan judul buku karangan Buya Hamka, bagian dari sekitar 200 judul koleksi museum. Hamka menulis dalam berbagai bentuk: novel, tafsir, sejarah, dan esai, sehingga rak ini memperlihatkan luas minatnya. Beberapa judulnya menjadi bacaan penting di Indonesia dan Malaysia, dan sebagian diterjemahkan ke bahasa lain. Karena terletak di rumah kelahirannya, rak ini menghubungkan karya dengan tempat tumbuh penulisnya, bukan hanya memajang buku sebagai benda.",
    },
    {
      title: "Foto perjalanan hidup Hamka",
      period: "1908–1981",
      origin: "Arsip keluarga dan dokumentasi",
      material: "foto",
      description:
        "Foto-foto ini mengikuti Hamka sejak kanak-kanak, remaja, bersama tokoh nasional, hingga iring-iringan jenazahnya pada 1981. Urutan foto berfungsi sebagai biografi ringkas yang mudah diikuti pengunjung. Foto kebersamaannya dengan tokoh nasional menunjukkan bahwa ia bergerak di lingkaran politik dan keagamaan, bukan hanya di dunia tulis. Sementara foto pemakaman menutup kisahnya dan menjelaskan mengapa rumah ini kemudian dijadikan museum.",
    },
    {
      title: "Kamar tidur dan kelambu",
      period: "masa hidup Hamka",
      origin: "Rumah kelahiran di Maninjau",
      material: "kayu, kain, dan kelambu",
      description:
        "Ruang ini menampilkan tempat tidur dengan kelambu putih yang dahulu dipakai Hamka. Kamar dipertahankan seperti keadaan rumah tinggal, sehingga pengunjung melihat sisi sehari-hari seorang tokoh yang biasanya dikenang lewat buku dan pidato. Kelambu adalah perlengkapan rumah tangga biasa di kawasan Danau Maninjau pada masa itu, ketika nyamuk menjadi bagian kehidupan malam. Dengan mempertahankan kamar seperti aslinya, museum memilih menyajikan kedekatan, bukan kemegahan.",
    },
    {
      title: "Benda pribadi keluarga",
      period: "awal abad ke-20",
      origin: "Keluarga Hamka",
      material: "kayu, logam, kain, dan koper",
      description:
        "Ruang ini memuat kursi peninggalan orang tua Hamka, lampu gantung kuno, koper haji pertama, delapan tongkat, dan baju wisuda lengkap dengan toga. Koper haji menunjukkan bahwa perjalanan ke Makkah pada masa itu berlangsung lama dan menjadi peristiwa besar bagi sebuah keluarga. Toga wisuda mengingatkan bahwa Hamka juga menerima penghargaan akademik atas karyanya. Benda-benda seperti ini memberi gambaran tentang kehidupan rumah tangga yang membentuknya.",
    },
  ],
  gallery: [
    {
      src: "/1.jpg",
      period: "kelahiran 1908",
      detail: [
        "Rumah ini adalah tempat kelahiran Buya Hamka pada 1908 di Maninjau.",
        "Bentuknya rumah panggung dengan atap bergonjong khas Minangkabau.",
        "Kini dipertahankan sebagai museum dengan perabot dan benda pribadi keluarga.",
        "Letaknya di tepi Danau Maninjau, kawasan yang banyak disebut dalam karya Hamka.",
      ],
    },
    {
      src: "/2.jpg",
      period: "rumah tinggal awal abad ke-20",
      detail: [
        "Serambi ini adalah ruang terbuka tempat keluarga biasa menerima tamu.",
        "Bangunan panggung menyisakan kolong yang dipakai untuk kegiatan sehari-hari.",
        "Ukiran kayu pada dinding dan tiang mengikuti gaya rumah adat di kawasan Maninjau.",
        "Serambi seperti ini juga menjadi tempat anak-anak belajar dan mengaji.",
      ],
    },
  ],
};

patches["museum-tuanku-imam-bonjol"] = {
  exhibits: [
    {
      title: "Senjata Perang Padri",
      period: "1803–1838",
      origin: "Perang Padri, Minangkabau",
      material: "logam dan kayu; sebagian replika",
      highlight: true,
      description:
        "Ruang ini memuat senjata yang dipakai Tuanku Imam Bonjol dan kaum Padri, sebagian berupa replika karena benda asli hilang atau dicuri. Perang Padri berlangsung puluhan tahun dan mula-mula merupakan konflik antarumat di Minangkabau sebelum Belanda ikut campur. Karena itu senjata di ruang ini tidak hanya berbicara tentang pertempuran melawan Belanda, tetapi juga tentang perang saudara yang mendahuluinya. Keterangan soal mana yang asli dan mana yang replika menjadi penting agar pengunjung tidak salah memahami benda yang dilihatnya.",
    },
    {
      title: "Lukisan Tuanku Imam Bonjol",
      period: "abad ke-20",
      origin: "Karya Jenderal Hoegeng Imam Santoso",
      material: "lukisan",
      description:
        "Lukisan ini dibuat oleh Jenderal Hoegeng Imam Santoso, Kepala Polisi Republik Indonesia pada 1968–1971. Menariknya, pelukisnya adalah pejabat negara, bukan seniman yang dikenal khusus melukis tokoh sejarah. Karena tidak ada potret dibuat semasa hidup Tuanku Imam Bonjol, wajahnya di banyak penggambaran disusun dari deskripsi dan bayangan seniman. Lukisan seperti ini menunjukkan bagaimana tokoh sejarah dibentuk kembali citranya oleh generasi sesudahnya, termasuk lewat karya pejabat negara.",
    },
    {
      title: "Pakaian kebesaran ulama",
      period: "awal abad ke-19",
      origin: "Tuanku Imam Bonjol dan tokoh sezamannya",
      material: "kain dan aksesori",
      description:
        "Kostum kebesaran ini pernah dipakai Tuanku Imam Bonjol dan tokoh lain pada masanya. Pakaian ulama pada masa Perang Padri menandai kedudukan sebagai pemimpin agama sekaligus pemimpin masyarakat, karena kedua peran itu tidak dipisahkan. Warna dan potongannya berbeda dari pakaian adat sehari-hari, sehingga bisa dikenali dalam penggambaran sejarah. Bagi pengunjung, busana ini membantu membayangkan sosok yang selama ini dikenal lewat lukisan dan cerita perang.",
    },
    {
      title: "Lantai dua: perkakas dan uang kuno",
      period: "abad ke-18 hingga ke-20",
      origin: "Minangkabau dan jalur dagang pesisir",
      material: "logam, keramik, dan perunggu",
      description:
        "Lantai dua memuat peralatan dapur, uang kuno, keramik antik, serta gamelan dan gong berbagai ukuran. Peralatan dapur dan keramik menggambarkan rumah tangga Minangkabau, sedangkan uang kuno menunjukkan bahwa kawasan ini terhubung dengan perdagangan lintas wilayah. Gamelan di Minangkabau menarik diperhatikan karena kesenian ini lebih sering dikaitkan dengan Jawa dan Bali, sehingga kehadirannya menunjukkan percampuran budaya. Bersama-sama, benda di lantai ini melengkapi kisah perang dengan gambaran kehidupan sehari-hari.",
    },
    {
      title: "Naskah kuno dan replika",
      period: "masa Perang Padri",
      origin: "Minangkabau",
      material: "kertas dan kulit; sebagian replika",
      description:
        "Ruang ini memuat sejumlah naskah lama, dan sebagian telah hilang sehingga digantikan replika oleh pengelola. Naskah pada masa Perang Padri biasanya berisi ajaran keagamaan, catatan peristiwa, atau surat menyurat antarpemimpin. Kehilangan naskah adalah masalah serius bagi penelitian sejarah karena isinya tidak bisa digantikan. Karena itu museum mencantumkan mana yang asli dan mana yang replika, supaya pengunjung dan peneliti tidak salah menyimpulkan.",
    },
  ],
  gallery: [
    {
      src: "/1.jpg",
      period: "bangunan museum",
      detail: [
        "Gedung museum ini memakai bentuk rumah gadang dengan atap melengkung.",
        "Letaknya di Bonjol, kawasan yang menjadi pusat perlawanan kaum Padri.",
        "Bentuk bangunan dipilih agar museum tampil sebagai bagian kebudayaan Minangkabau.",
        "Di dalamnya tersimpan senjata, pakaian, naskah, dan perkakas dari masa Perang Padri.",
      ],
    },
    {
      src: "/2.jpg",
      period: "monumen peringatan",
      detail: [
        "Patung ini menggambarkan Tuanku Imam Bonjol sebagai pemimpin Perang Padri.",
        "Tidak ada potret dibuat semasa hidupnya, sehingga wajahnya disusun dari deskripsi.",
        "Patung semacam ini menjadi penanda tempat dan dipakai sebagai latar kunjungan.",
        "Ia diasingkan ke Cianjur lalu ke Lotta, Sulawesi Utara, dan meninggal pada 1864.",
      ],
    },
    {
      src: "/3.jpg",
      period: "kompleks museum",
      detail: [
        "Halaman ini mempertemukan bangunan museum dan rumah adat dalam satu kompleks.",
        "Rumah gadang di sekitarnya menunjukkan bahwa museum berada di kawasan permukiman.",
        "Pohon-pohon besar memberi keteduhan pada area kunjungan.",
        "Dari halaman ini pengunjung biasanya melanjutkan ke makam Tuanku Imam Bonjol.",
      ],
    },
  ],
};

patches["museum-kereta-api-sawahlunto"] = {
  exhibits: [
    {
      title: "Lokomotif uap bergigi E1060",
      period: "akhir abad ke-19",
      origin: "Jalur Kayu Tanam–Batu Tabal dan Padang Panjang–Bukittinggi",
      material: "baja",
      highlight: true,
      description:
        "Ini adalah satu-satunya lokomotif uap di museum, dirancang untuk jalur curam Kayu Tanam–Batu Tabal dan Padang Panjang–Bukittinggi. Lokomotif bergigi memakai roda bergerigi yang mencengkeram rel khusus agar tidak meluncur mundur di tanjakan tajam. Teknologi ini dipilih karena jalur kereta di Sumatera Barat melewati perbukitan yang sulit dilalui lokomotif biasa. Bagi pengunjung, lokomotif ini menjelaskan bahwa pengangkutan batu bara dari Sawahlunto bergantung pada rekayasa yang dirancang khusus untuk medan setempat.",
    },
    {
      title: "Gerbong dan miniatur lokomotif",
      period: "masa operasi tambang",
      origin: "Jalur kereta batu bara Sawahlunto",
      material: "baja dan kayu",
      description:
        "Museum memuat lima gerbong dan sembilan miniatur lokomotif dari total 106 koleksi. Gerbong mengangkut batu bara dari tambang menuju pelabuhan, sehingga ukuran dan bentuknya disesuaikan dengan muatan berat. Miniatur dipakai karena tidak semua jenis lokomotif yang pernah beroperasi bisa dipertahankan dalam ukuran asli. Dengan menampilkan keduanya, museum memperlihatkan bahwa jalur ini memakai beberapa jenis kendaraan yang berbeda sesuai kebutuhan.",
    },
    {
      title: "Peralatan sinyal dan komunikasi",
      period: "abad ke-19 hingga ke-20",
      origin: "Stasiun dan jalur kereta Sawahlunto",
      material: "logam, kayu, dan kaca",
      description:
        "Tiga puluh empat alat sinyal dan komunikasi kereta api masih dipamerkan di ruang stasiun. Sebelum ada radio, keselamatan jalur bergantung pada sinyal mekanik dan telegraf yang menghubungkan stasiun satu dengan lainnya. Kesalahan kecil dalam urutan sinyal bisa berakibat tabrakan, sehingga peralatan ini dirawat dengan aturan ketat. Melihat alat-alatnya membantu pengunjung memahami bahwa kerja perkeretaapian adalah kerja koordinasi, bukan hanya mengemudikan lokomotif.",
    },
    {
      title: "Dokumentasi foto perkeretaapian",
      period: "akhir abad ke-19 hingga ke-20",
      origin: "Arsip perkeretaapian Sawahlunto",
      material: "foto",
      description:
        "Tiga puluh empat foto dokumentasi ini merekam masa operasi jalur kereta batu bara Sawahlunto. Foto-foto itu memperlihatkan stasiun, lokomotif, dan pekerja yang menjalankan jalur setiap hari. Sawahlunto tumbuh sebagai kota tambang karena kereta inilah yang mengangkut hasil tambang ke pelabuhan, sehingga foto-foto tersebut sekaligus menjadi sejarah kota. Banyak bangunan yang tampak dalam foto sudah berubah, menjadikan arsip ini rujukan penting untuk memahami tata kota lama.",
    },
  ],
  gallery: [
    {
      src: "/1.jpg",
      period: "akhir abad ke-19",
      detail: [
        "Stasiun Sawahlunto ini dibangun untuk mengangkut batu bara dari tambang ke pelabuhan.",
        "Lokomotif uap tampak berdiri di jalur depan bangunan stasiun.",
        "Arsitektur stasiun mengikuti gaya bangunan kolonial dengan atap tinggi.",
        "Jalurnya melewati perbukitan sehingga sebagian lokomotif dirancang bergerigi.",
      ],
    },
  ],
};

apply();
