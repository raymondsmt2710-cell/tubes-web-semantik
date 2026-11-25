import { patches, apply } from "./apply-content.ts";

// ── Bab I: Aceh ──────────────────────────────────────────────────────────────

patches["museum-negeri-aceh"] = {
  exhibits: [
    {
      title: "Rumoh Aceh di halaman museum",
      period: "replika, dibangun 1915",
      origin: "Paviliun Aceh, Pameran Kolonial Semarang 1914",
      material: "kayu dengan atap rumbia",
      highlight: true,
      description:
        "Rumah panggung tradisional Aceh ini berdiri di halaman museum dan menjadi ikon kawasannya. Bangunannya ditinggikan di atas tiang kayu sehingga menyisakan ruang kolong di bawah lantai, cara lama masyarakat Aceh menghadapi tanah yang lembap dan sering tergenang. Rumoh Aceh inilah bangunan asal museum: Paviliun Aceh dari Pameran Kolonial Semarang 1914 yang dibawa kembali ke Kutaraja dan diresmikan sebagai museum pada 31 Juli 1915. Di dekatnya berdiri menara tempat Lonceng Cakra Donya digantung, sehingga halaman ini mempertemukan rumah adat dan pusaka kesultanan dalam satu pandangan.",
    },
    {
      title: "Gedung Pameran Tetap",
      period: "era 1970-an",
      origin: "Proyek Pelita, Jalan Sultan Alaidin Mahmudsyah",
      material: "beton dan kaca, beratap bentuk rumah Aceh",
      description:
        "Gedung ini memadukan arsitektur tradisional dan modern: bentuk atapnya mengingatkan pada rumah Aceh, tetapi struktur dan jendelanya lebar khas bangunan pameran. Museum menempati lokasi ini sejak dipindahkan pada 1969 atas prakarsa T. Hamzah Bendahara, lalu berstatus Museum Negeri Aceh melalui surat keputusan menteri pada 28 Mei 1979 dan diresmikan kembali pada 1 September 1980. Di bagian depan terdapat taman dan sebuah meriam besi peninggalan Belanda dari abad ke-17, yang biasa dipakai pengunjung sebagai penanda arah masuk. Di dalamnya tersusun koleksi etnografika, filologika, dan historika.",
    },
    {
      title: "Lonceng Cakra Donya",
      period: "diperkirakan abad ke-15",
      origin: "Kesultanan Pasai",
      material: "perunggu",
      highlight: true,
      description:
        "Lonceng perunggu ini digantung di menara kayu berlantai tiga di halaman museum, berdekatan dengan Rumoh Aceh. Menurut catatan museum, Cakra Donya dibawa dari Kesultanan Pasai; banyak penulis kemudian menghubungkannya dengan rombongan pelayaran Laksamana Cheng Ho, meski hubungan itu tidak selalu didukung bukti yang sama kuat. Pada masa kesultanan, benda seperti ini berfungsi sebagai penanda kuasa dan pusaka kerajaan, bukan sekadar alat bunyi. Karena itu lonceng ini termasuk koleksi yang paling sering dibicarakan dalam penjelasan tentang Museum Aceh.",
    },
    {
      title: "Prasasti Neusu",
      period: "masa kesultanan Aceh",
      origin: "Neusu, Banda Aceh",
      material: "batu berukir",
      description:
        "Prasasti ini termasuk koleksi andalan museum dan sering disebut dalam catatan resminya. Prasasti berfungsi sebagai dokumen resmi sebuah pemerintahan: isinya biasanya mencatat peristiwa, aturan, atau pemberian tanah, sehingga bisa dipakai untuk merekonstruksi cara kesultanan Aceh mengatur masyarakatnya. Bagi pengunjung, benda semacam ini adalah bukti tertulis yang melengkapi kisah lisan dan foto. Karena bertulisan lama dan permukaannya aus, keterangan di ruang pamer menjadi penting untuk memahami isinya.",
    },
    {
      title: "Koleksi etnografika dan filologika",
      period: "abad ke-17 hingga ke-20",
      origin: "Berbagai daerah di Aceh",
      material: "kain, kayu, logam, dan kertas naskah",
      description:
        "Ruang pamer menyimpan senjata tradisional, pakaian adat, dan manuskrip kuno dari sepuluh jenis klasifikasi koleksi, bagian dari sekitar 6.038 benda yang tercatat. Klasifikasi ini mengikuti cara museum membagi warisan budaya: etnografika untuk benda sehari-hari dan perlengkapan adat, filologika untuk naskah dan tulisan. Kehadiran naskah membuat koleksi museum tidak hanya bercerita tentang benda, tetapi juga tentang bahasa dan tradisi tulis Aceh. Karena jumlahnya besar, yang dipamerkan di ruang tetap hanya sebagian, dan sisanya tersimpan sebagai koleksi penyimpanan.",
    },
  ],
  gallery: [
    {
      src: "/1.jpg",
      period: "bangunan 1970-an, halaman sejak 1915",
      detail: [
        "Bentuk atap gedung meniru rumah tradisional Aceh, tetapi jendelanya lebar khas gedung pameran modern.",
        "Taman di depan menjadi ruang terbuka pertama sebelum pengunjung masuk ke ruang koleksi.",
        "Meriam besi peninggalan Belanda abad ke-17 berdiri di halaman sebagai penanda masa kolonial.",
        "Di dalam gedung tersimpan koleksi etnografika, filologika, dan historika dari sekitar 6.038 benda.",
      ],
    },
    {
      src: "/2.jpg",
      period: "diperkirakan abad ke-15",
      detail: [
        "Menara kayu berlantai tiga ini khusus didirikan sebagai tempat menggantung lonceng, bukan menara masjid.",
        "Lonceng perunggu Cakra Donya digantung di tingkat paling atas menara.",
        "Rumoh Aceh beratap rumbia tampak berdekatan, mempertemukan rumah adat dan pusaka kesultanan.",
        "Menurut catatan museum, lonceng dibawa dari Kesultanan Pasai dan dikaitkan dengan rombongan Cheng Ho.",
      ],
    },
    {
      src: "/3.jpg",
      period: "gerbang era pengembangan museum negeri",
      detail: [
        "Gerbang kayu beratap sirap memakai ukiran dan bentuk atap rumah tradisional Aceh.",
        "Dari gerbang ini pengunjung melihat dua wajah museum sekaligus: Rumoh Aceh dan gedung pameran modern.",
        "Rumoh Aceh di belakang adalah bangunan asal museum dari Pameran Kolonial 1914.",
        "Gedung modern di sisi lain adalah hasil proyek Pelita era 1970-an.",
      ],
    },
  ],
  addSources: [
    {
      label: "Wikipedia: Museum Tsunami Aceh (konteks museum Aceh)",
      url: "https://id.wikipedia.org/wiki/Museum_Tsunami_Aceh",
    },
  ],
};

patches["museum-tsunami-aceh"] = {
  exhibits: [
    {
      title: "Lorong cerobong gelombang",
      period: "dibangun 2008",
      origin: "Rancangan museum peringatan tsunami",
      material: "beton dan dinding berlapis",
      highlight: true,
      description:
        "Lorong masuk museum ini sempit, tinggi, dan berkelok, dirancang menyerupai gelombang tsunami yang sedang menggulung. Pengunjung melewatinya sebagai pengalaman pertama sebelum sampai ke ruang pamer, sehingga suasana sudah terbentuk sejak pintu. Dindingnya berlapis dan cahaya masuk dari celah di atas, membuat ruang terasa pengap sekaligus megah. Pilihan rancangan ini menjadikan lorong bukan sekadar jalan masuk, melainkan bagian dari cara museum menyampaikan peristiwa 26 Desember 2004.",
    },
    {
      title: "Simulasi elektronik gempa dan tsunami",
      period: "peristiwa 26 Desember 2004",
      origin: "Ruang pamer tetap museum",
      material: "perangkat elektronik dan panel tampilan",
      description:
        "Pameran ini menggambarkan proses gempa dan tsunami Samudra Hindia 2004 secara elektronik, sehingga pengunjung bisa mengikuti rangkaian kejadian dan bukan hanya melihat akibatnya. Penjelasannya menautkan gempa di dasar laut dengan gelombang yang menghantam pesisir Aceh. Bagi museum kebencanaan, bagian seperti ini berfungsi sebagai alat belajar: pengunjung diharapkan memahami tanda-tanda bahaya dan jalur evakuasi. Karena itu museum juga dirancang sebagai tempat evakuasi darurat bila tsunami terjadi lagi.",
    },
    {
      title: "Diorama 26 Desember 2004",
      period: "26 Desember 2004",
      origin: "Koleksi dan rekonstruksi museum",
      material: "maket, kayu, dan benda temuan",
      description:
        "Diorama ini menggambarkan kejadian tsunami sekaligus menampilkan benda-benda yang terbawa gelombang dan kemudian disimpan sebagai koleksi. Salah satu yang paling dikenal adalah maket masjid yang sebagian bangunannya menonjol keluar dari dinding, dikelilingi serakan kayu dan puing. Banyak masjid di pesisir Aceh hancur atau berdiri miring oleh hantaman gelombang, sementara bangunan yang selamat seperti Masjid Baiturrahman kemudian menjadi titik berkumpul penyintas. Susunan diorama sengaja dibuat sebagai ruang belajar bencana, bukan galeri foto korban.",
    },
    {
      title: "Ruang kisah penyintas",
      period: "kesaksian 2004 dan sesudahnya",
      origin: "Dokumentasi museum",
      material: "foto, panel teks, dan rekaman",
      description:
        "Ruang ini memuat foto korban dan kesaksian para penyintas yang disusun sebagai tempat refleksi. Panel-panelnya tidak berhenti pada angka kerugian, tetapi menampilkan pengalaman orang yang selamat, kehilangan keluarga, dan membangun kembali kehidupan. Cara penyajian seperti ini lazim di museum bencana: kesaksian pribadi membuat peristiwa berskala besar bisa dipahami secara manusiawi. Karena isinya menyentuh, ruang ini biasanya dilewati pengunjung dengan tempo lebih lambat daripada ruang diorama.",
    },
  ],
  gallery: [
    {
      src: "/1.jpg",
      period: "ruang pamer tetap",
      detail: [
        "Lantai berkarpet biru dan panel berdinding bersudut membentuk alur kunjungan yang berkelok.",
        "Diorama bertutup kaca menampilkan pemukiman pesisir sebelum dan sesudah gelombang.",
        "Boneka kecil menirukan situasi darurat untuk menunjukkan skala bencana.",
        "Pameran dirancang sebagai ruang belajar bencana, bukan sekadar galeri foto korban.",
      ],
    },
    {
      src: "/2.jpg",
      period: "peristiwa 26 Desember 2004",
      detail: [
        "Maket masjid berkubah ini dibuat seolah sebagian bangunannya terdorong keluar dari dinding.",
        "Serakan kayu dan puing di sekelilingnya menggambarkan kekuatan hantaman gelombang.",
        "Banyak masjid pesisir Aceh hancur atau berdiri miring akibat gelombang itu.",
        "Bangunan yang selamat, seperti Masjid Baiturrahman, kemudian menjadi titik berkumpul penyintas.",
      ],
    },
    {
      src: "/3.jpg",
      period: "museum dibuka 2011",
      detail: [
        "Plakat logam ini dipasang di dinding pintu masuk utama museum.",
        "Latar plakat memuat relief garis pantai Aceh sebagai penanda wilayah yang terdampak.",
        "Museum dibangun pada 2008 dengan dana donor yang dikoordinasikan BRR.",
        "Diresmikan Presiden Susilo Bambang Yudhoyono pada 2009, lalu dibuka untuk publik pada 2011.",
      ],
    },
  ],
};

patches["museum-cut-nyak-dhien"] = {
  exhibits: [
    {
      title: "Surat dan dokumen Cut Nyak Dhien",
      period: "akhir abad ke-19",
      origin: "Perlawanan Aceh di pedalaman Aceh Besar",
      material: "kertas dan tinta",
      highlight: true,
      description:
        "Ruang pamer menyimpan surat-surat serta dokumen yang menunjukkan cara Cut Nyak Dhien menyusun strategi perlawanan. Dokumen semacam ini penting karena perang Aceh berlangsung lama dan banyak di antaranya bergantung pada komunikasi antarwilayah, bukan hanya pertempuran terbuka. Bagi museum, kertas bertulisan tangan membawa pengunjung lebih dekat ke sosok yang bersangkutan daripada patung atau lukisan. Cut Nyak Dhien lahir pada 1848 dan memimpin perlawanan setelah suaminya, Teuku Umar, gugur pada 1899.",
    },
    {
      title: "Foto masa pengasingan",
      period: "1905–1908",
      origin: "Pengasingan di Sumedang, Jawa Barat",
      material: "foto arsip",
      description:
        "Foto ini memperlihatkan wajah Cut Nyak Dhien semasa diasingkan di Sumedang, Jawa Barat, setelah tertangkap pada 1905 di pedalaman Aceh Besar. Dalam foto arsip Tropenmuseum ia tampak bersama kerabatnya, dalam kondisi sakit dan sudah berusia lanjut. Ia meninggal di Sumedang pada 1908, jauh dari tanah yang diperjuangkannya. Foto seperti ini menjadi koleksi visual museum untuk menautkan kisah perlawanan dengan tokohnya secara langsung, bukan lewat reka ulang.",
    },
    {
      title: "Diorama perlawanan Aceh",
      period: "1873–1905",
      origin: "Perang Aceh",
      material: "diorama, foto, dan replika",
      description:
        "Diorama dan foto di ruang ini menggambarkan peristiwa penting dalam perang Aceh melawan Belanda. Perang itu berlangsung puluhan tahun dan mengubah wajah banyak kampung di Aceh Besar, termasuk Lampisang tempat museum ini berdiri. Penyajiannya membantu pengunjung memahami bahwa perlawanan tidak berlangsung sekali, tetapi berganti strategi dari perang terbuka menjadi gerilya di pedalaman. Rumah tempat museum ini berada pun menjadi bagian dari kisah itu: rumah aslinya dibakar Belanda pada 1896.",
    },
    {
      title: "Tata ruang kamar yang menyamar",
      period: "sebelum 1905",
      origin: "Rumah asli di Lampisang",
      material: "kayu dan sekat ruang",
      description:
        "Kamar dayang-dayang sengaja diletakkan di depan, sedangkan kamar Cut Nyak Dhien berada di belakang. Susunan ini bukan soal urutan ruang biasa, melainkan upaya agar ia punya waktu meloloskan diri bila rumah diserang mendadak. Tata ruang seperti ini memperlihatkan bagaimana perlawanan juga berlangsung di rumah, melalui kewaspadaan sehari-hari. Yang bisa dilihat pengunjung sekarang adalah hasil pemugaran, karena rumah aslinya dibakar Belanda pada 1896 dan hanya pondasinya yang tersisa.",
    },
    {
      title: "Rumoh Aceh 65 tiang",
      period: "dipugar 1981",
      origin: "Lampisang, Peukan Bada, Aceh Besar",
      material: "kayu ulin, atap rumbia",
      highlight: true,
      description:
        "Bangunan ini adalah rumah panggung berukuran sekitar 25 × 17 meter dengan 65 tiang kayu dan atap rumbia. Ukiran kayu ulin dan susunan tiangnya dirancang tahan gempa, pilihan teknis yang lazim pada rumah tradisional Aceh. Rumah aslinya dibakar Belanda pada 1896, dipugar pada 1981, lalu diresmikan sebagai museum pada 1987 oleh Menteri Pendidikan dan Kebudayaan Fuad Hassan. Karena itu yang berdiri sekarang adalah bangunan hasil pemugaran, dan hanya pondasinya yang masih asli.",
    },
  ],
  gallery: [
    {
      src: "/1.jpg",
      period: "1905",
      detail: [
        "Foto arsip Tropenmuseum ini memperlihatkan Cut Nyak Dhien bersama kerabatnya setelah tertangkap.",
        "Ia ditangkap pada 1905 di pedalaman Aceh Besar dalam kondisi sakit dan sudah berusia lanjut.",
        "Setelah itu ia diasingkan ke Sumedang, Jawa Barat, dan meninggal di sana pada 1908.",
        "Foto semacam ini dipakai museum untuk menautkan kisah perlawanan dengan tokohnya secara langsung.",
      ],
    },
    {
      src: "/2.jpg",
      period: "dipugar 1981, diresmikan 1987",
      detail: [
        "Rumah panggung Aceh ini kini menjadi museum di Gampong Lampisang, Peukan Bada.",
        "Ukurannya sekitar 25 × 17 meter dengan 65 tiang kayu dan atap rumbia.",
        "Rumah aslinya dibakar Belanda pada 1896; hanya pondasi yang masih asli.",
        "Bangunan sekarang adalah hasil pemugaran 1981 yang diresmikan sebagai museum pada 1987.",
      ],
    },
    {
      src: "/3.jpg",
      period: "patung modern",
      detail: [
        "Patung ini berdiri di Museum Mandala Bhakti Wanitatama, Yogyakarta — bukan di Lampisang.",
        "Foto dipakai sebagai rujukan visual sosok Cut Nyak Dhien dalam busana dan sikap yang lazim digambarkan.",
        "Museum di Lampisang tidak memiliki patung serupa di halamannya.",
        "Karena itu kredit dan lokasi patung dicantumkan terbuka agar tidak menyesatkan.",
      ],
    },
  ],
};

patches["museum-malikussaleh"] = {
  exhibits: [
    {
      title: "Fragmen batu nisan Samudera Pasai",
      period: "abad ke-13 hingga ke-16",
      origin: "Kompleks makam kerajaan Samudera Pasai",
      material: "batu berkaligrafi",
      highlight: true,
      description:
        "Batu nisan berkaligrafi Arab ini berasal dari kompleks makam kerajaan Samudera Pasai dan menjadi bukti awal masuknya Islam di Sumatera. Tulisan pada nisan biasanya memuat nama, tarikh, dan kutipan keagamaan, sehingga bisa dipakai menelusuri siapa yang dimakamkan dan kapan. Bagi penelitian, nisan seperti ini lebih dapat dipercaya daripada kisah lisan karena tarikhnya tertulis. Kawasan Samudera Pasai sendiri tercatat sebagai kerajaan Islam pertama di Nusantara, dan makam sultan pertamanya menjadi salah satu situs utama di sini.",
    },
    {
      title: "Mata uang kuno",
      period: "abad ke-13 hingga ke-14",
      origin: "Kesultanan Samudera Pasai",
      material: "logam",
      highlight: true,
      description:
        "Koin dari masa kesultanan ini menunjukkan aktivitas perdagangan Samudera Pasai. Keberadaan mata uang sendiri menandakan kerajaan ini sudah memiliki sistem ekonomi dan administrasi yang mapan, bukan sekadar permukiman pesisir. Samudera Pasai berada di jalur dagang Selat Malaka, sehingga koin dan barang dagangan bergerak bersama kapal dari berbagai negeri. Bagi pengunjung, benda kecil ini menjelaskan sisi lain kerajaan yang biasanya dikenang hanya dari makam dan naskah.",
    },
    {
      title: "Temuan arkeologis kawasan situs",
      period: "abad ke-13 hingga ke-16",
      origin: "Sekitar bekas kota Samudera Pasai",
      material: "keramik, logam, dan batu",
      description:
        "Koleksi di kawasan situs berpusat pada tinggalan Samudera Pasai berupa fragmen, mata uang, dan temuan arkeologis dari sekitar bekas kota kerajaan. Temuan permukaan seperti pecahan keramik membantu menentukan batas permukiman lama dan jalur perdagangan yang melewatinya. Kawasan ini sekarang dikelilingi kebun kelapa dan sawah, sehingga bekas kota tidak lagi terlihat jelas di permukaan. Museum berfungsi merangkai temuan yang berserakan itu menjadi gambaran utuh, termasuk menautkannya dengan makam Malikussaleh yang menjadi salah satu situs utama di sini.",
    },
  ],
  gallery: [
    {
      src: "/1.jpg",
      period: "dibangun bertahap 2011–2016",
      detail: [
        "Gedung berkubah putih dengan ornamen geometris ini adalah museum khusus di kawasan bekas Samudera Pasai.",
        "Pembangunannya berlangsung bertahap sejak 2011 hingga 2016.",
        "Kawasan ini oleh banyak catatan disebut sebagai kerajaan Islam pertama di Nusantara.",
        "Koleksi di sekitarnya berpusat pada tinggalan abad ke-13 sampai ke-16.",
      ],
    },
    {
      src: "/2.jpg",
      period: "kawasan bekas kerajaan",
      detail: [
        "Gerbang ini menandai masuknya pengunjung ke kawasan permukiman bekas pusat Samudera Pasai.",
        "Kawasan sekitarnya berupa kebun kelapa dan sawah.",
        "Nama Malikussaleh merujuk sultan pertama kerajaan itu.",
        "Makam sultan tersebut menjadi salah satu situs utama di dalam kawasan.",
      ],
    },
    {
      src: "/3.jpg",
      period: "abad ke-13 hingga ke-14",
      detail: [
        "Koin emas bertulisan Arab ini adalah mata uang kesultanan Samudera Pasai.",
        "Keberadaan mata uang menunjukkan sistem ekonomi dan administrasi yang sudah mapan.",
        "Masa kejayaannya sezaman dengan ramainya jalur dagang Selat Malaka.",
        "Benda sekecil ini menjelaskan sisi perdagangan kerajaan, bukan hanya sisi keagamaannya.",
      ],
    },
  ],
};

apply();
