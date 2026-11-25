import { patches, apply } from "./apply-content.ts";

// ── Bab VI: Sumatera Selatan dan Bangka Belitung ─────────────────────────────

patches["museum-negeri-sumatera-selatan"] = {
  exhibits: [
    {
      title: "Replika Rumah Limas",
      period: "arsitektur tradisional Palembang",
      origin: "Sumatera Selatan",
      material: "kayu dan atap genteng",
      highlight: true,
      description:
        "Rumah Limas adalah rumah adat Sumatera Selatan yang dibangun sebagai pameran di halaman museum. Namanya berasal dari atapnya yang bertingkat seperti limas, dan luas bangunannya menandai kedudukan pemiliknya. Rumah ini ditinggikan di atas tiang, dengan ruang utama di bagian tengah dan ruang terbuka di depan. Karena yang berdiri di sini adalah replika, pengunjung memperoleh gambaran bentuk keseluruhan rumah tanpa harus mengunjungi kampung asalnya.",
    },
    {
      title: "Arca Hindu-Buddha",
      period: "masa Sriwijaya dan periode klasik",
      origin: "Sumatera bagian selatan",
      material: "batu",
      description:
        "Ruang ini memuat arca dari masa Sriwijaya dan periode klasik Sumatera bagian selatan. Palembang dan sekitarnya pernah menjadi pusat Sriwijaya, kerajaan maritim yang pengaruhnya terasa sampai Semenanjung Melayu. Banyak arca ditemukan tidak lengkap, sebagian mungkin pernah dipindahkan atau rusak jauh sebelum ditemukan kembali. Bagi museum, penjelasan mengenai lokasi penemuan sama pentingnya dengan bentuk arcanya, karena dari situ bisa diperkirakan bagaimana kawasan ini dihuni pada masa lampau.",
    },
    {
      title: "Tenun songket Palembang",
      period: "tradisi tenun Melayu Palembang",
      origin: "Palembang",
      material: "kain sutra dan benang emas",
      highlight: true,
      description:
        "Songket adalah kain tenun bermotif yang dibuat dengan menyelipkan benang emas atau perak ke dalam kain. Di Palembang, songket dipakai pada upacara pernikahan dan acara adat, dan motifnya sering diberi nama seperti bungo pacik atau tampak maco. Karena pembuatannya memakan waktu lama, satu kain bisa menjadi barang warisan keluarga. Museum menampilkan beragam motif agar pengunjung melihat bahwa keragaman songket tidak hanya soal warna, tetapi juga nama dan makna tiap pola.",
    },
    {
      title: "Materai Kesultanan Palembang",
      period: "masa Kesultanan Palembang Darussalam",
      origin: "Kesultanan Palembang Darussalam",
      material: "logam",
      description:
        "Materai ini berasal dari Kesultanan Palembang Darussalam dan dipamerkan sebagai koleksi sejarah. Materai dipakai untuk mengesahkan surat dan perjanjian, sehingga keberadaannya menandai bahwa sebuah dokumen benar berasal dari kesultanan. Palembang pada masa itu adalah pusat perdagangan sungai yang penting, dan banyak kesepakatan dagang memerlukan pengesahan semacam ini. Bagi peneliti, bentuk dan tulisan pada materai membantu menentukan masa pemakaiannya.",
    },
    {
      title: "Koleksi tekstil dan kerajinan",
      _new: true,
      period: "abad ke-19 hingga ke-20",
      origin: "Sumatera Selatan",
      material: "kain, rotan, dan kayu",
      description:
        "Selain songket, museum menyimpan tekstil dan kerajinan lain dari Sumatera Selatan. Kerajinan seperti anyaman dan ukiran biasanya dikerjakan di rumah sebagai pekerjaan sampingan, menggunakan bahan yang tersedia di sekitar. Coraknya berbeda antara daerah rawa, pesisir, dan dataran tinggi, mengikuti bahan dan keperluan setempat. Koleksi semacam ini jarang menjadi pusat perhatian pengunjung, tetapi memberi gambaran paling dekat tentang kehidupan sehari-hari masyarakat.",
    },
  ],
  gallery: [
    {
      src: "/1.jpg",
      period: "bangunan museum provinsi",
      detail: [
        "Gedung ini adalah Museum Negeri Sumatera Selatan di kawasan Sekayu, Palembang.",
        "Bangunannya bergaya rumah limas agar tampil sebagai bagian kebudayaan setempat.",
        "Halaman luas memuat replika rumah adat dan benda berukuran besar.",
        "Fungsinya sebagai museum provinsi sekaligus pusat penelitian kebudayaan daerah.",
      ],
    },
    {
      src: "/2.jpg",
      period: "replika arsitektur",
      detail: [
        "Replika Rumah Limas ini berdiri di halaman museum sebagai pameran arsitektur.",
        "Atapnya bertingkat seperti limas, dan jumlah tingkatnya menandai kedudukan pemilik rumah.",
        "Bangunannya ditinggikan di atas tiang dengan ruang terbuka di bagian depan.",
        "Rumah limas menjadi simbol Sumatera Selatan dan dipakai pada lambang daerah.",
      ],
    },
  ],
};

patches["museum-sultan-mahmud-badaruddin-ii"] = {
  exhibits: [
    {
      title: "Lukisan dan potret Sultan Mahmud Badaruddin II",
      period: "masa perlawanan terhadap Belanda, 1819–1821",
      origin: "Kesultanan Palembang Darussalam",
      material: "lukisan dan foto arsip",
      highlight: true,
      description:
        "Potret serta lukisan pengasingan sultan ini menjadi koleksi utama museum. Sultan Mahmud Badaruddin II memimpin perlawanan terhadap Belanda dan dikenal karena menolak tunduk pada kekuasaan kolonial, sehingga namanya dipakai untuk museum ini dan juga Bandar Udara Palembang. Setelah dikalahkan, ia diasingkan ke Ternate dan meninggal di sana. Lukisan pengasingan penting karena memperlihatkan sisi lain dari seorang tokoh perang: kehidupan jauh dari negerinya sendiri.",
    },
    {
      title: "Tekstil dan pakaian tradisional",
      period: "abad ke-19 hingga ke-20",
      origin: "Sumatera Selatan",
      material: "kain tenun dan sulaman",
      description:
        "Ruang ini memuat kain, pakaian adat, dan kerajinan Sumatera Selatan. Palembang dikenal sebagai pusat kain songket, dan sebagian koleksi di sini menunjukkan bagaimana busana adat dipakai pada upacara kesultanan maupun pernikahan rakyat biasa. Perbedaan bahan menandai tingkat kemampuan pemakainya, misalnya antara sutra bermotif benang emas dan kain tenun sederhana. Dengan memajang keduanya, museum memperlihatkan bahwa busana tradisional tidak tunggal, melainkan berlapis menurut kedudukan sosial.",
    },
    {
      title: "Koleksi senjata dan koin",
      period: "masa kesultanan",
      origin: "Palembang dan jalur dagang Musi",
      material: "logam dan kayu",
      description:
        "Senjata tradisional serta mata uang lama di ruang ini menunjukkan aktivitas perdagangan Palembang. Sungai Musi menjadi jalur utama yang menghubungkan pedalaman dengan pesisir, sehingga koin asing bisa sampai ke kawasan ini. Senjata mengingatkan bahwa Palembang pernah menjadi kota yang diperebutkan, termasuk dalam pertempuran melawan Belanda pada awal abad ke-19. Bersama-sama, benda di ruang ini menjelaskan kota pelabuhan yang kaya sekaligus sering dilanda konflik.",
    },
    {
      title: "Taman arca Sriwijaya",
      period: "masa Sriwijaya",
      origin: "Sumatera bagian selatan",
      material: "batu",
      highlight: true,
      description:
        "Halaman museum dipenuhi artefak masa Sriwijaya, antara lain patung Ganesha dan Buddha. Menempatkan arca di taman, bukan di dalam ruang tertutup, mengikuti kebiasaan museum arkeologi di Asia Tenggara dan memungkinkan benda berukuran besar dipajang. Sriwijaya berpusat di kawasan ini dan pengaruhnya meluas lewat perdagangan maritim. Karena banyak arca ditemukan dalam keadaan tidak lengkap, taman ini juga berfungsi sebagai tempat penyimpanan terbuka yang bisa diteliti.",
    },
  ],
  gallery: [
    {
      src: "/1.jpg",
      period: "bangunan kolonial, menjadi museum",
      detail: [
        "Gedung ini menampung koleksi tentang Sultan Mahmud Badaruddin II dan Palembang.",
        "Letaknya dekat kawasan Benteng Kuto Besak, sisa pusat kekuasaan kesultanan.",
        "Bangunan bergaya kolonial menunjukkan lapisan sejarah kota setelah kesultanan berakhir.",
        "Nama museum diambil dari sultan yang memimpin perlawanan terhadap Belanda.",
      ],
    },
    {
      src: "/2.jpg",
      period: "masa pengasingan",
      detail: [
        "Lukisan ini menggambarkan Sultan Mahmud Badaruddin II semasa diasingkan.",
        "Setelah dikalahkan Belanda, ia diasingkan ke Ternate.",
        "Ia meninggal di pengasingan dan tidak pernah kembali ke Palembang.",
        "Lukisan seperti ini memperlihatkan sisi lain tokoh perang, yaitu kehidupan jauh dari negerinya.",
      ],
    },
    {
      src: "/3.jpg",
      period: "awal abad ke-19",
      detail: [
        "Potret ini menjadi salah satu koleksi utama museum.",
        "Sultan Mahmud Badaruddin II dikenal karena menolak tunduk pada kekuasaan kolonial.",
        "Namanya kini dipakai untuk museum dan Bandar Udara Palembang.",
        "Tidak ada foto dibuat semasa hidupnya, sehingga potret disusun dari penggambaran kemudian.",
      ],
    },
  ],
};

patches["museum-taman-purbakala-sriwijaya"] = {
  exhibits: [
    {
      title: "Museum Sriwijaya",
      period: "situs masa Sriwijaya",
      origin: "Kawasan Karanganyar, tepi Sungai Musi",
      material: "bangunan modern di atas situs",
      description:
        "Bangunan museum ini berdiri di dalam taman yang memuat temuan dan penjelasan situs. Kawasan Karanganyar dipercaya sebagai salah satu pusat permukiman masa Sriwijaya, dan penelitian arkeologi di sini menemukan sisa bangunan serta benda dari masa itu. Museum sengaja dibangun dekat situs agar pengunjung bisa melihat temuan dan lokasi asalnya dalam satu kunjungan. Karena itu koleksinya berbeda dari museum umum: isinya berpusat pada satu kawasan dan satu masa.",
    },
    {
      title: "Pendopo utama Limasan",
      period: "bangunan pendukung",
      origin: "Taman purbakala",
      material: "kayu dan atap limasan",
      description:
        "Pendopo beratap limasan ini menjadi pusat kegiatan di taman purbakala. Bentuk limasan dipilih karena lazim dipakai pada bangunan pertemuan di Sumatera Selatan. Fungsinya bukan untuk memamerkan benda, melainkan untuk kegiatan seperti ceramah, pertunjukan, dan penerimaan tamu. Kehadirannya membuat taman purbakala tidak hanya menjadi tempat melihat reruntuhan, tetapi juga ruang yang dipakai masyarakat sampai sekarang.",
    },
    {
      title: "Struktur bata kuno",
      period: "masa Sriwijaya",
      origin: "Situs Karanganyar",
      material: "bata",
      description:
        "Sisa bangunan dari masa Sriwijaya ini dapat dilihat langsung di area situs. Struktur bata menunjukkan bahwa kawasan ini pernah memiliki bangunan permanen, kemungkinan tempat ibadah atau bangunan keagamaan. Berbeda dari benda yang dipajang di lemari kaca, struktur ini tidak dapat dipindahkan, sehingga dilestarikan di tempatnya. Bagi pengunjung, melihatnya langsung memberi pemahaman tentang skala dan tata letak kawasan yang jauh lebih baik daripada melihat foto.",
    },
    {
      title: "Arca Buddha dari masa Sriwijaya",
      _new: true,
      period: "masa Sriwijaya",
      origin: "Kawasan situs Karanganyar",
      material: "batu",
      highlight: true,
      description:
        "Arca Buddha ini menjadi salah satu temuan yang paling sering ditampilkan dari kawasan situs. Sriwijaya dikenal sebagai pusat pembelajaran Buddhisme, dan catatan dari Tiongkok menyebut adanya hubungan antara kawasan ini dengan pusat pendidikan agama di India. Arca semacam ini menjadi bukti bahwa pengaruh Buddha tidak hanya ada di istana, tetapi menyebar ke permukiman. Bentuk dan gaya pahatannya membantu menentukan masa pembuatannya.",
    },
  ],
  gallery: [
    {
      src: "/1.jpg",
      period: "kawasan situs Sriwijaya",
      detail: [
        "Bangunan museum ini berdiri di dalam taman purbakala Karanganyar.",
        "Kawasan ini dipercaya sebagai salah satu pusat permukiman masa Sriwijaya.",
        "Museum dibangun dekat situs agar temuan dan lokasi asalnya bisa dilihat bersama.",
        "Koleksinya berpusat pada satu kawasan dan satu masa, berbeda dari museum umum.",
      ],
    },
    {
      src: "/2.jpg",
      period: "bangunan pendukung",
      detail: [
        "Pendopo beratap limasan ini menjadi pusat kegiatan di taman purbakala.",
        "Bentuk limasan lazim dipakai pada bangunan pertemuan di Sumatera Selatan.",
        "Fungsinya untuk kegiatan seperti ceramah dan pertunjukan, bukan memamerkan benda.",
        "Kehadirannya membuat taman purbakala juga menjadi ruang yang dipakai masyarakat.",
      ],
    },
    {
      src: "/3.jpg",
      period: "masa Sriwijaya",
      detail: [
        "Arca Buddha ini berasal dari masa Sriwijaya.",
        "Sriwijaya dikenal sebagai pusat pembelajaran Buddhisme di Asia Tenggara.",
        "Catatan Tiongkok menyebut hubungan kawasan ini dengan pusat pendidikan agama di India.",
        "Gaya pahatannya membantu menentukan masa pembuatan arca.",
      ],
    },
  ],
};

patches["museum-timah-indonesia"] = {
  exhibits: [
    {
      title: "Peralatan penambangan timah",
      period: "masa kolonial hingga abad ke-20",
      origin: "Pulau Bangka dan Belitung",
      material: "logam, kayu, dan besi",
      highlight: true,
      description:
        "Artefak tambang ini menunjukkan cara timah dieksplorasi dan diolah sejak masa kolonial. Penambangan timah di Bangka dimulai jauh sebelum kemerdekaan dan menjadi salah satu alasan kawasan ini terhubung erat dengan pemerintah Hindia Belanda. Peralatan sederhana pada masa awal berbeda jauh dari mesin yang dipakai kemudian, dan perbedaan itu menunjukkan perubahan skala penambangan. Bagi pengunjung, benda semacam ini menjelaskan bahwa timah bukan hanya hasil tambang, tetapi bagian dari sejarah kerja banyak orang.",
    },
    {
      title: "Galeri tambang darat dan laut",
      period: "abad ke-20",
      origin: "Bangka Belitung",
      material: "panel, alat, dan model",
      description:
        "Galeri ini membahas penambangan timah di darat, di lepas pantai, hingga proses peleburannya. Penambangan lepas pantai memerlukan cara yang berbeda dari tambang darat, termasuk kapal keruk dan penyaringan pasir. Peleburan juga menjadi bagian penting, karena timah baru bernilai setelah dipisahkan dari bahan lain. Dengan menjelaskan ketiga tahap itu, galeri memperlihatkan bahwa industri timah adalah rangkaian pekerjaan panjang, bukan hanya penggalian.",
    },
    {
      title: "Miniatur lingkungan tambang",
      period: "abad ke-20",
      origin: "Kawasan pertambangan Bangka",
      material: "maket tiga dimensi",
      description:
        "Miniatur tiga dimensi ini menggambarkan lingkungan pertambangan dan permukiman pekerja. Yang ditampilkan bukan hanya lubang tambang, tetapi juga rumah pekerja, jalan, dan bangunan pendukung, karena pertambangan membentuk permukiman di sekitarnya. Maket dipilih karena pengunjung tidak dapat melihat kawasan tambang secara utuh dari dekat. Melalui miniatur, hubungan antara tambang, permukiman, dan pelabuhan bisa dipahami dalam sekali pandang.",
    },
    {
      title: "Koleksi etnografi Bangka",
      period: "abad ke-19 hingga ke-20",
      origin: "Masyarakat Bangka Belitung",
      material: "kain dan peralatan rumah tangga",
      description:
        "Ruang ini memuat pakaian tradisional dan peralatan sehari-hari masyarakat Bangka Belitung. Penduduk Bangka terbentuk dari campuran Melayu, Tionghoa, dan pendatang dari berbagai daerah yang datang untuk bekerja di tambang, sehingga budayanya bercampur. Peralatan rumah tangga menunjukkan bagaimana kehidupan diatur di kawasan yang dahulu sulit dijangkau. Bagian ini penting karena melengkapi kisah tambang dengan kisah orang-orang yang tinggal di sekitarnya.",
    },
  ],
  gallery: [
    {
      src: "/1.jpg",
      period: "bangunan masa kolonial",
      detail: [
        "Gedung ini adalah Museum Timah Indonesia di Pangkalpinang.",
        "Bangunannya berasal dari masa kolonial, ketika timah menjadi komoditas utama kawasan ini.",
        "Koleksinya mencakup peralatan tambang, model, dan dokumen perusahaan.",
        "Museum menempati bangunan yang dahulu berkaitan langsung dengan kegiatan penambangan.",
      ],
    },
    {
      src: "/2.jpg",
      period: "bangunan masa kolonial",
      detail: [
        "Bangunan ini adalah Museum Timah Indonesia di Muntok.",
        "Muntok pernah menjadi pusat pemerintahan dan pelabuhan penting di Bangka bagian barat.",
        "Museum ini melengkapi koleksi serupa di Pangkalpinang.",
        "Keberadaan dua museum menunjukkan luasnya kawasan penambangan timah.",
      ],
    },
  ],
};

apply();
