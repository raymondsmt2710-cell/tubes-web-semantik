import { patches, apply } from "./apply-content.ts";

// ── Bab V: Jambi dan Bengkulu ────────────────────────────────────────────────

patches["museum-negeri-jambi"] = {
  exhibits: [
    {
      title: "Bangunan berarsitektur rumah panggung",
      period: "dibangun era 1980-an",
      origin: "Kota Jambi, tepi Danau Sipin",
      material: "kayu dan beton beratap bentuk rumah Jambi",
      description:
        "Gedung museum ini memakai ornamen khas Jambi yang menjadi ciri bangunan provinsi. Bentuknya mengacu pada rumah panggung Kayu Tinggi, rumah tradisional Jambi yang ditinggikan di atas tiang. Pilihan bentuk itu membuat museum tampil sebagai bagian kebudayaan setempat, bukan gedung asing di tengah kota. Letaknya di tepi Danau Sipin juga menjadikannya mudah dikenali dari arah danau, dan pada pagi hari pantulan air membuat bangunannya terlihat utuh dari seberang.",
    },
    {
      title: "Koleksi Batanghari",
      period: "masa megalitik hingga masa klasik",
      origin: "Kawasan hulu Sungai Batanghari",
      material: "batu dan logam",
      highlight: true,
      description:
        "Ruang ini memuat arca dan benda megalitik dari kawasan hulu Sungai Batanghari. Sungai Batanghari adalah jalur utama yang menghubungkan pedalaman Sumatera dengan pesisir timur, sehingga banyak temuan arkeologis tersebar di sepanjang alirannya. Benda megalitik menunjukkan kepercayaan lama yang mendahului masuknya Hindu-Buddha dan Islam. Karena temuan di hulu sungai lebih sulit dijangkau, koleksi museum ini menjadi rujukan penting bagi pengunjung yang tidak dapat mendatangi situs aslinya.",
    },
    {
      title: "Budaya Melayu Jambi",
      period: "masa Kesultanan Jambi hingga kini",
      origin: "Masyarakat Melayu Jambi",
      material: "kain, kayu, dan logam",
      description:
        "Ruang ini memuat benda upacara dan perlengkapan adat masyarakat Melayu Jambi. Kebudayaan Melayu Jambi terbentuk dari campuran pengaruh kesultanan, perdagangan sungai, dan tradisi pedalaman, sehingga bentuk upacaranya pun berbeda dari Melayu pesisir. Benda seperti kain dan perlengkapan upacara biasanya dipakai pada peristiwa tertentu, bukan sehari-hari. Karena itu museum menjelaskan kapan dan oleh siapa benda itu dipakai, agar pengunjung tidak menyimpulkan bahwa semuanya dipakai bersamaan.",
    },
    {
      title: "Arca dan temuan hulu Batanghari",
      _new: true,
      period: "masa klasik Sumatera",
      origin: "Hulu Sungai Batanghari",
      material: "batu",
      description:
        "Arca-arca dari hulu Batanghari memperlihatkan pengaruh Hindu-Buddha yang masuk lewat jalur sungai, bukan hanya lewat pesisir. Kawasan hulu Batanghari dikenal sebagai salah satu tempat asal temuan penting yang kemudian tersebar ke berbagai museum, sebagian bahkan dibawa ke luar negeri pada masa kolonial. Bagi museum daerah, menampilkan arca semacam ini berarti mempertahankan hubungan antara benda dan tempat asalnya. Keterangan mengenai lokasi penemuan menjadi bagian penting dari penjelasannya.",
    },
  ],
  gallery: [
    {
      src: "/1.jpg",
      period: "bangunan museum provinsi",
      detail: [
        "Foto ini memperlihatkan Museum Siginjei dari arah Danau Sipin.",
        "Bentuk bangunannya mengacu pada rumah panggung Kayu Tinggi, rumah tradisional Jambi.",
        "Ornamen khas Jambi menjadi ciri yang membedakannya dari bangunan provinsi lain.",
        "Letaknya di tepi danau membuat bangunan mudah dikenali dari kejauhan.",
      ],
    },
  ],
};

patches["museum-siginjai"] = {
  exhibits: [
    {
      title: "Siginjai, ikat pinggang pusaka",
      period: "masa Kesultanan Jambi",
      origin: "Kesultanan Jambi",
      material: "logam dan kain",
      highlight: true,
      description:
        "Siginjai adalah benda pusaka kesultanan Jambi yang menjadi asal nama museum. Ikat pinggang pusaka semacam ini dipakai dalam upacara kebesaran, sehingga keberadaannya menandai siapa yang berhak tampil sebagai sultan. Benda pusaka di banyak kesultanan Sumatera berfungsi sebagai bukti keabsahan kekuasaan, bukan hanya perhiasan. Karena itu Siginjai lebih tepat dipahami sebagai simbol politik, dan namanya dipilih untuk museum agar kaitannya dengan kesultanan tetap terlihat.",
    },
    {
      title: "Keramik Cina",
      period: "abad ke-14 hingga ke-19",
      origin: "Jalur perdagangan Batanghari",
      material: "keramik",
      highlight: true,
      description:
        "Keramik ini berasal dari jalur perdagangan Batanghari dan menunjukkan hubungan Jambi dengan Cina. Sungai Batanghari dapat dilayari cukup jauh ke pedalaman, sehingga barang impor bisa sampai ke kawasan yang jauh dari laut. Warna dan motif keramik membantu menentukan masa pembuatannya, dan dengan begitu juga masa ramainya perdagangan di jalur itu. Bagi pengunjung, pecahan keramik yang tampak sederhana sebenarnya adalah bukti hubungan dagang jarak jauh yang berlangsung berabad-abad.",
    },
    {
      title: "Arca dan benda megalitik",
      period: "masa megalitik hingga masa klasik",
      origin: "Hulu Batanghari",
      material: "batu",
      description:
        "Ruang ini memuat temuan arkeologis dari kawasan hulu Batanghari, termasuk arca dan benda batu masa megalitik. Benda megalitik lebih tua daripada arca bercorak Hindu-Buddha, sehingga ruang ini menyimpan dua masa yang berbeda. Menempatkannya berdekatan membantu pengunjung melihat bahwa kawasan hulu Batanghari dihuni terus-menerus, dengan kepercayaan yang berganti. Karena temuan dari kawasan itu sering tidak lengkap, keterangan museum menjadi kunci untuk memahaminya.",
    },
    {
      title: "Stempel dan arsip kesultanan",
      period: "masa Kesultanan Jambi dan kolonial",
      origin: "Kesultanan Jambi",
      material: "logam dan kertas",
      description:
        "Ruang ini memuat stempel serta dokumen yang berkaitan dengan Kesultanan Jambi dan masa pemerintahan kolonial. Stempel kesultanan adalah bukti tertulis bahwa sebuah keputusan benar-benar dikeluarkan oleh pihak berwenang, sehingga diperhatikan dalam penelitian surat-surat lama. Salah satu yang ditampilkan adalah stempel Dewan Patih Kesultanan Jambi, yang menunjukkan bahwa pemerintahan dijalankan oleh beberapa lembaga, bukan sultan seorang diri. Arsip semacam ini melengkapi kisah kesultanan yang biasanya diketahui dari cerita lisan.",
    },
    {
      title: "Instalasi Kilang Avigas",
      _new: true,
      period: "abad ke-20",
      origin: "Kawasan Jambi",
      material: "logam dan pipa",
      description:
        "Instalasi Kilang Avigas menjadi bagian koleksi yang mengingatkan masa industri di Jambi. Avigas berkaitan dengan pengolahan gas dan bahan bakar pada masa ketika kawasan ini mulai terhubung dengan kegiatan pertambangan dan perkebunan. Kehadiran benda industri di museum daerah jarang ditemui, karena sebagian besar koleksi berpusat pada benda budaya. Bagian ini berguna untuk menunjukkan bahwa sejarah Jambi tidak berhenti pada kesultanan, tetapi berlanjut ke masa usaha dan industri.",
    },
  ],
  gallery: [
    {
      src: "/1.jpg",
      period: "masa kolonial",
      detail: [
        "Panel ini memuat keterangan tentang Residen Pertama Djambi pada masa kolonial.",
        "Residen adalah pejabat Belanda yang memimpin wilayah karesidenan.",
        "Panel semacam ini menjadi bagian koleksi karena merekam struktur pemerintahan kolonial.",
        "Ejaan “Djambi” menunjukkan dokumen berasal dari masa sebelum ejaan diperbarui.",
      ],
    },
    {
      src: "/2.jpg",
      period: "abad ke-20",
      detail: [
        "Instalasi ini berkaitan dengan Kilang Avigas yang pernah beroperasi di kawasan Jambi.",
        "Benda industri seperti ini jarang menjadi koleksi museum daerah.",
        "Kehadirannya menunjukkan sejarah Jambi juga mencakup masa usaha dan industri.",
        "Peralatan logam dan pipa menandakan pengolahan bahan bakar, bukan benda rumah tangga.",
      ],
    },
    {
      src: "/3.jpg",
      period: "masa Kesultanan Jambi",
      detail: [
        "Stempel ini adalah cap Dewan Patih Kesultanan Jambi.",
        "Dewan Patih menunjukkan pemerintahan dijalankan beberapa lembaga, bukan sultan seorang diri.",
        "Stempel dipakai sebagai bukti keabsahan surat dan keputusan kesultanan.",
        "Benda seperti ini menjadi rujukan penting dalam penelitian arsip lama.",
      ],
    },
  ],
};

patches["museum-negeri-bengkulu"] = {
  exhibits: [
    {
      title: "Perkakas masak tradisional Bengkulu",
      period: "abad ke-19 hingga ke-20",
      origin: "Rumah tangga masyarakat Bengkulu",
      material: "tempurung, bambu, dan kayu",
      highlight: true,
      description:
        "Ruang ini memuat peralatan dapur dari bahan alami yang mencerminkan kehidupan rumah tangga masyarakat Bengkulu. Perkakas dari tempurung kelapa dan bambu dipakai karena mudah didapat dan tahan terhadap panas, bukan karena harganya murah semata. Setiap bentuk punya kegunaan khusus, misalnya untuk menanak nasi, mengaduk, atau menyimpan air. Bagi museum, peralatan seperti ini merekam pengetahuan praktis yang mulai hilang sejak aluminium dan plastik masuk ke dapur.",
    },
    {
      title: "Koleksi uang lama",
      period: "edisi lama rupiah",
      origin: "Koleksi numismatika museum",
      material: "kertas",
      description:
        "Uang kertas rupiah edisi lama ini disimpan sebagai koleksi numismatika. Salah satu yang ditampilkan adalah uang kertas seribu rupiah edisi lama, dan ada pula yang memuat tanda tangan pejabat dengan ejaan lama. Uang seperti ini berguna untuk menelusuri perubahan nilai, desain, dan lembaga yang menerbitkannya dari masa ke masa. Bagi pengunjung yang lebih muda, benda ini sering menjadi kejutan karena bentuknya sangat berbeda dari uang yang dipakai sekarang.",
    },
    {
      title: "Koleksi etnografi",
      period: "abad ke-19 hingga ke-20",
      origin: "Masyarakat Bengkulu",
      material: "kain, kayu, dan logam",
      description:
        "Ruang ini memuat benda sehari-hari dan perlengkapan adat masyarakat Bengkulu. Bengkulu dihuni beberapa kelompok dengan bahasa dan adat berbeda, termasuk Rejang, Serawai, dan Melayu pesisir, sehingga koleksinya beragam. Perlengkapan adat biasanya dipakai pada upacara daur hidup seperti kelahiran, pernikahan, dan kematian. Karena itu museum menjelaskan asal benda dari kelompok mana, agar keragaman itu tidak tenggelam menjadi satu label “Bengkulu” yang terlalu umum.",
    },
    {
      title: "Uang kertas bertanda tangan lama",
      _new: true,
      period: "edisi lama rupiah",
      origin: "Koleksi numismatika museum",
      material: "kertas",
      description:
        "Salah satu koleksi menampilkan uang kertas lima ratus rupiah bertanda tangan pejabat dengan ejaan lama. Perbedaan ejaan pada tanda tangan menunjukkan dokumen dibuat sebelum pembaruan ejaan bahasa Indonesia. Bagi peneliti, uang seperti ini membantu memastikan masa penerbitan dan pejabat yang menjabat pada saat itu. Dipamerkan bersama perkakas dapur, koleksi uang ini memberi gambaran bahwa perubahan alat tukar berlangsung bersamaan dengan perubahan barang sehari-hari.",
    },
  ],
  gallery: [
    {
      src: "/1.jpg",
      period: "edisi lama",
      detail: [
        "Foto ini memperlihatkan uang kertas seribu rupiah edisi lama.",
        "Desainnya berbeda jauh dari uang yang dipakai sekarang.",
        "Uang lama disimpan museum sebagai koleksi numismatika.",
        "Koleksi seperti ini dipakai untuk menelusuri perubahan nilai dan desain uang.",
      ],
    },
    {
      src: "/2.jpg",
      period: "sebelum pembaruan ejaan",
      detail: [
        "Uang kertas lima ratus rupiah ini memuat tanda tangan bertuliskan “LIPPHARTODES”.",
        "Ejaan “LIPP” menunjukkan dokumen dibuat sebelum pembaruan ejaan bahasa Indonesia.",
        "Tanda tangan pejabat membantu memastikan masa penerbitan uang.",
        "Benda seperti ini menjadi bukti kecil perubahan administrasi negara.",
      ],
    },
    {
      src: "/3.jpg",
      period: "abad ke-19 hingga ke-20",
      detail: [
        "Perkakas dapur ini dibuat dari tempurung kelapa.",
        "Bahan alami dipakai karena mudah didapat dan tahan panas.",
        "Setiap bentuk punya kegunaan khusus, misalnya menanak nasi atau menyimpan air.",
        "Pengetahuan membuat dan memakai perkakas seperti ini mulai hilang sejak aluminium dan plastik masuk.",
      ],
    },
  ],
};

patches["rumah-pengasingan-bung-karno"] = {
  exhibits: [
    {
      title: "Rumah masa pengasingan",
      period: "1938–1942",
      origin: "Bengkulu",
      material: "kayu dan beton",
      highlight: true,
      description:
        "Bangunan asli ini menjadi tempat tinggal Soekarno selama diasingkan di Bengkulu. Ia diasingkan ke sini pada 1938 setelah sebelumnya dibuang ke Flores, dan tinggal sampai 1942 ketika Jepang masuk. Rumahnya sederhana dan tidak besar, sehingga pengunjung bisa membayangkan bahwa pengasingan berlangsung dalam kehidupan yang sangat terbatas. Meski begitu, selama di Bengkulu Soekarno tetap aktif menulis dan mengajar, sehingga masa pengasingan bukan masa berhentinya kegiatan politik.",
    },
    {
      title: "Perabot dan benda pribadi",
      period: "masa pengasingan",
      origin: "Rumah pengasingan Bengkulu",
      material: "kayu, kain, dan logam",
      description:
        "Ruang ini memuat perlengkapan rumah tangga yang dipakai pada masa pengasingan. Perabotnya menunjukkan standar hidup yang sederhana, jauh dari kesan istana yang sering dibayangkan orang tentang seorang tokoh nasional. Beberapa benda berkaitan dengan kegiatan sehari-hari seperti membaca, menulis, dan menerima tamu. Dengan mempertahankan perabot aslinya, museum memilih menampilkan kehidupan rumah, bukan sekadar benda bersejarah, sehingga masa pengasingan terasa lebih nyata.",
    },
    {
      title: "Dokumentasi periode 1938–1942",
      period: "1938–1942",
      origin: "Arsip kolonial dan dokumentasi keluarga",
      material: "foto dan catatan",
      description:
        "Catatan dan foto di ruang ini menguraikan kegiatan Soekarno selama berada di Bengkulu. Selama periode itu ia aktif dalam kegiatan keagamaan dan pendidikan, termasuk mengajar dan bergaul dengan tokoh setempat. Dokumentasi semacam ini penting karena masa pengasingan sering hanya dikenang sebagai hukuman, padahal di situlah beberapa gagasannya berkembang. Bagi Bengkulu sendiri, periode ini meninggalkan jejak pada kehidupan organisasi dan pendidikan di kota tersebut.",
    },
  ],
  gallery: [
    {
      src: "/1.jpg",
      period: "museum sejak era 1980-an",
      detail: [
        "Papan nama ini menandai rumah yang kini menjadi museum.",
        "Bangunan aslinya dipakai Soekarno sebagai tempat tinggal selama diasingkan.",
        "Statusnya sebagai cagar budaya membuat bentuk bangunannya tidak banyak berubah.",
        "Papan ini juga menandai alamat rumah yang biasa dicari pengunjung.",
      ],
    },
    {
      src: "/2.jpg",
      period: "1938–1942",
      detail: [
        "Halaman ini adalah bagian dari rumah pengasingan Soekarno di Bengkulu.",
        "Bangunannya sederhana, menunjukkan kehidupan yang terbatas semasa pengasingan.",
        "Soekarno diasingkan ke sini pada 1938 dan tinggal sampai 1942.",
        "Di halaman ini pula ia biasa menerima tamu dan berdiskusi.",
      ],
    },
    {
      src: "/3.jpg",
      period: "arsitektur rumah kolonial",
      detail: [
        "Rumah pengasingan ini terlihat dari sisi jalan, memakai gaya rumah kolonial sederhana.",
        "Jendela dan pintunya besar agar udara masuk, ciri bangunan di daerah panas.",
        "Posisinya di jalan utama memudahkan pengawasan pada masa pengasingan.",
        "Dari sisi ini pengunjung biasanya masuk sebelum melihat perabot di dalam.",
      ],
    },
  ],
};

apply();
