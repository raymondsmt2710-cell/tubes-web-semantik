import { patches, apply } from "./apply-content.ts";

// ── Bab II: Sumatera Utara ───────────────────────────────────────────────────

patches["museum-negeri-sumatera-utara"] = {
  exhibits: [
    {
      title: "Ruang Masa Prasejarah",
      period: "prasejarah hingga masa migrasi",
      origin: "Ruang pamer tetap, lantai koleksi geologi",
      material: "fosil, replika hewan, dan panel geologi",
      highlight: true,
      description:
        "Ruang pertama ini menampilkan sejarah geologi, pergeseran benua, migrasi manusia, serta replika hewan khas Sumatera dan fosil manusia purba. Alurnya dimulai dari terbentuknya Pulau Sumatera, sehingga pengunjung memahami bahwa daratan ini pernah menyatu dan bergeser sebelum dihuni manusia. Replika hewan dipakai karena fosil utuh jarang ditemukan, sedangkan fosil manusia purba memberi petunjuk kapan manusia pertama tiba di kawasan ini. Menempatkan ruang ini di awal menjadikan geologi sebagai dasar sebelum museum bercerita tentang kerajaan dan kolonialisme.",
    },
    {
      title: "Arca Hindu-Buddha",
      period: "masa Hindu-Buddha",
      origin: "Temuan di wilayah Sumatera Utara",
      material: "batu",
      description:
        "Arca ini peninggalan masa Hindu-Buddha dan menjadi bagian koleksi sejarah kuno Sumatera Utara. Keberadaannya menunjukkan bahwa pengaruh India masuk ke pedalaman Sumatera, bukan hanya ke pesisir dan kerajaan besar di Jawa. Arca semacam ini biasanya ditemukan tidak lengkap, sehingga penjelasan museum mengenai bagian yang hilang sama pentingnya dengan yang tersisa. Bagi pengunjung, benda ini adalah bukti bahwa sebelum kesultanan Islam berdiri, kawasan ini sudah melewati masa keagamaan lain.",
    },
    {
      title: "Replika Masjid Azizi",
      period: "masa masuknya Islam di pesisir timur",
      origin: "Tanjung Pura, Langkat",
      material: "replika",
      description:
        "Replika ini mewakili Masjid Azizi di Tanjung Pura, Langkat, yang menjadi penanda masuknya Islam di pesisir timur Sumatera Utara. Memilih masjid sebagai objek pameran menunjukkan bahwa Islam di kawasan ini berkembang lewat kesultanan dan jaringan dagang pesisir, bukan lewat penaklukan. Bentuk masjidnya yang berlapis dan berkubah menjadi ciri arsitektur Melayu pesisir. Karena berupa replika, pengunjung memperoleh gambaran bentuk keseluruhan tanpa harus membawa bangunan aslinya ke ruang pamer.",
    },
    {
      title: "Ruang kolonial dan kepahlawanan",
      period: "abad ke-19 hingga kemerdekaan",
      origin: "Masa Kolonial Belanda dan perang kemerdekaan",
      material: "perkakas, model figur, poster, lukisan, dan foto",
      description:
        "Ruang ini memuat perkakas masa Kolonial Belanda, model figur kolonial, poster propaganda perang, serta lukisan dan foto para pahlawan serta gubernur Sumatera Utara. Poster propaganda menarik diperhatikan karena menunjukkan bagaimana kedua pihak membentuk opini publik lewat gambar dan slogan. Lukisan gubernur menandai peralihan kekuasaan dari kolonial ke pemerintahan republik. Dengan menempatkan keduanya dalam satu ruang, museum memperlihatkan masa kolonial dan masa kepahlawanan sebagai dua sisi dari periode yang sama.",
    },
  ],
  gallery: [
    {
      src: "/1.jpg",
      period: "diresmikan 1982",
      detail: [
        "Bangunan dua lantai ini berdiri di lahan sekitar 10.468 m² di Jalan H.M. Jhoni, Medan.",
        "Peletakan batu pertama berupa sepasang makara dilakukan Presiden Soekarno pada 1954.",
        "Museum baru diresmikan 19 April 1982 oleh Menteri Pendidikan dan Kebudayaan Daoed Joesoef.",
        "Di dalamnya ada ruang pameran tetap, ruang pameran temporer, ruang audio visual, dan perpustakaan.",
      ],
    },
    {
      src: "/2.jpg",
      period: "Undang-Undang Nomor 10 Tahun 1948",
      detail: [
        "Panel ini mencatat bahwa Provinsi Sumatera Utara dibentuk lewat Undang-Undang Nomor 10 Tahun 1948.",
        "Undang-undang itu membagi Pulau Sumatera menjadi tiga provinsi.",
        "Isi panel menjadi contoh bagaimana museum menyusun kronologi pemerintahan sebagai bagian narasi sejarah daerah.",
        "Museum di sini berfungsi tidak hanya memamerkan benda, tetapi juga menjelaskan pembentukan wilayah.",
      ],
    },
    {
      src: "/3.jpg",
      period: "hingga 2005 tercatat 6.799 koleksi",
      detail: [
        "Kain tenun dipajang tergantung di dalam lemari kaca dengan label kecil di atas setiap helai.",
        "Koleksi tekstil ini mewakili keragaman suku di Sumatera Utara: Batak, Melayu, Nias, dan lainnya.",
        "Tenun menjadi kekuatan utama museum ini karena setiap kelompok punya corak dan teknik berbeda.",
        "Hingga 2005 museum mencatat 6.799 koleksi, sehingga hanya sebagian yang bisa dipamerkan.",
      ],
    },
  ],
};

patches["museum-huta-bolon-simanindo"] = {
  exhibits: [
    {
      title: "Pustaha laklak",
      period: "tradisi tulis Batak pra-kolonial",
      origin: "Kawasan Danau Toba, Samosir",
      material: "kulit kayu dan tali",
      highlight: true,
      description:
        "Pustaha laklak adalah naskah Batak berbahan kulit kayu yang memuat ilmu tradisional dan ramalan. Isinya ditulis dengan aksara Batak dan dilipat seperti akordeon, sehingga bisa dibuka panjang saat dibaca. Naskah semacam ini biasanya dipegang oleh dukun atau ahli adat, bukan bacaan umum, karena berkaitan dengan pengobatan dan penentuan hari baik. Bagi museum, pustaha menunjukkan bahwa masyarakat Batak punya tradisi tulis sendiri, bukan hanya tradisi lisan yang lebih sering diceritakan.",
    },
    {
      title: "Tunggal panaluan",
      period: "tradisi adat Batak",
      origin: "Kawasan Samosir",
      material: "kayu berukir",
      highlight: true,
      description:
        "Tunggal panaluan adalah tongkat pusaka berukir yang dipakai dalam upacara masyarakat Batak. Ukirannya biasanya berupa sosok-sosok bertumpuk, dan tongkat ini dianggap memiliki kekuatan yang hanya bisa dipakai oleh orang tertentu. Dalam upacara, benda seperti ini berfungsi sebagai penanda otoritas sekaligus perlengkapan ritual. Karena itu tunggal panaluan termasuk benda yang paling sering dibicarakan dalam penjelasan tentang kebudayaan Batak, dan kehadirannya di museum membantu pengunjung memahami sisi spiritual masyarakat Danau Toba.",
    },
    {
      title: "Solu bolon",
      period: "perahu tradisional Danau Toba",
      origin: "Tepi Danau Toba",
      material: "kayu",
      description:
        "Solu bolon adalah perahu kayu besar khas Batak yang dipamerkan di kompleks huta. Danau Toba menjadi jalur penghubung antarkampung, sehingga perahu bukan hanya alat transportasi tetapi juga bagian dari kehidupan sehari-hari. Ukurannya yang besar menunjukkan bahwa perjalanan air bisa melibatkan banyak orang dan barang sekaligus. Menempatkannya di kompleks rumah adat membantu pengunjung melihat hubungan antara kampung di tepi danau dan wilayah seberang.",
    },
    {
      title: "Parhalaan",
      period: "kalender tradisional Batak",
      origin: "Kawasan Samosir",
      material: "kayu atau tulang bertulis",
      description:
        "Parhalaan adalah kalender tradisional Batak dan menjadi salah satu koleksi andalan museum. Isinya mencatat penanggalan dan penanda waktu yang dipakai untuk menentukan kapan bercocok tanam atau menggelar upacara. Keberadaan kalender seperti ini menunjukkan bahwa masyarakat Batak mengamati musim dan peredaran bulan secara cermat sebelum ada kalender modern. Bagi pengunjung, parhalaan menjelaskan bagaimana kegiatan pertanian dan adat di kawasan Danau Toba diatur oleh waktu yang disepakati bersama.",
    },
  ],
  gallery: [
    {
      src: "/1.jpg",
      period: "kompleks warisan sejak 1969",
      detail: [
        "Rumah adat Batak berbentuk rumah panggung dengan atap melengkung ini adalah inti kompleks Huta Bolon Simanindo.",
        "Kompleks ini adalah warisan Raja Sidauruk sejak 1969.",
        "Terdiri atas dua susun rumah adat yang saling berhadapan, masing-masing lima rumah.",
        "Letaknya di tepi Danau Toba, sehingga latar air menjadi bagian dari pandangan kawasan.",
      ],
    },
    {
      src: "/2.jpg",
      period: "tata ruang kampung tradisional",
      detail: [
        "Dari depan terlihat struktur rumah panggung dengan tiang penyangga dan ukiran pada bagian atap.",
        "Susunan huta (kampung) sengaja dipertahankan seperti aslinya.",
        "Tujuannya agar pengunjung memahami rumah adat sebagai bagian tata ruang kampung, bukan bangunan tunggal.",
        "Rumah-rumah saling berhadapan membentuk ruang bersama di tengahnya.",
      ],
    },
    {
      src: "/3.jpg",
      period: "tradisi megalitik",
      detail: [
        "Dua patung batu berwujud sosok duduk ini diletakkan di bawah naungan atap rumbia.",
        "Dalam tradisi Batak, patung semacam ini berfungsi sebagai penjaga kampung dan penanda leluhur.",
        "Gayanya yang sederhana menunjukkan tradisi megalitik yang lebih tua daripada arsitektur rumah adatnya.",
        "Karena itu patung batu ini memberi petunjuk bahwa kawasan ini dihuni jauh sebelum rumah panggung dibangun.",
      ],
    },
  ],
};

patches["museum-tb-silalahi-center"] = {
  exhibits: [
    {
      title: "Gedung T.B. Silalahi",
      period: "pusat budaya modern",
      origin: "Balige, tepi Danau Toba",
      material: "beton dan kaca",
      description:
        "Bangunan utama ini adalah wajah kompleks T.B. Silalahi Center, pusat budaya Batak di Balige. Selain sebagai museum, tempat ini dipakai sebagai ruang kegiatan budaya, sehingga fungsinya lebih luas daripada museum pada umumnya. Artinya, pengunjung bisa menemukan pameran tetap sekaligus acara seperti pertunjukan atau pertemuan adat pada waktu tertentu. Posisinya di tepi Danau Toba menjadikan Balige titik yang mudah dicapai dari banyak kampung di sekitar danau.",
    },
    {
      title: "Rumah adat Karo",
      period: "arsitektur tradisional Karo",
      origin: "Kawasan Karo, Sumatera Utara bagian utara",
      material: "kayu dan atap ijuk",
      highlight: true,
      description:
        "Rumah adat Karo beratap ijuk tinggi ini berdiri di kompleks museum sebagai pameran arsitektur. Kehadirannya menunjukkan bahwa kawasan Toba dihuni beberapa sub-etnis Batak dengan bentuk rumah yang berbeda: Karo di utara, Toba di sekitar danau. Atap ijuk yang menjulang adalah ciri yang mudah dibedakan dari rumah adat Toba. Dengan menempatkannya di sini, museum menjelaskan bahwa kebudayaan Batak tidak seragam, melainkan terdiri atas beberapa tradisi yang berdampingan.",
    },
    {
      title: "Koleksi budaya Batak",
      period: "abad ke-19 hingga ke-20",
      origin: "Berbagai daerah Batak",
      material: "kain, kayu, dan logam",
      description:
        "Koleksi ini berisi benda-benda budaya yang mengisahkan sejarah dan kehidupan masyarakat Batak di sekitar Danau Toba. Isinya mencakup perlengkapan rumah tangga, alat kerja, dan benda adat yang dipakai dalam kehidupan sehari-hari. Berbeda dari museum yang menonjolkan benda pusaka, koleksi semacam ini memperlihatkan sisi keseharian: bagaimana orang memasak, bertani, dan berpakaian. Karena kawasan Toba erat dengan pertanian dan danau, banyak benda di sini berkaitan dengan kedua hal itu.",
    },
  ],
  gallery: [
    {
      src: "/1.jpg",
      period: "kompleks budaya modern",
      detail: [
        "Bangunan utama ini adalah wajah kompleks T.B. Silalahi Center, pusat budaya Batak di Balige.",
        "Selain museum, tempat ini dipakai sebagai ruang kegiatan budaya.",
        "Karena itu fungsinya lebih luas daripada museum pada umumnya.",
        "Posisinya di tepi Danau Toba menjadikannya mudah dicapai dari banyak kampung sekitar danau.",
      ],
    },
    {
      src: "/2.jpg",
      period: "arsitektur Karo",
      detail: [
        "Rumah adat Karo beratap ijuk tinggi ini berdiri di kompleks museum sebagai pameran arsitektur.",
        "Bentuknya berbeda dari rumah adat Toba di sekitar danau.",
        "Kehadirannya menunjukkan kawasan Toba dihuni beberapa sub-etnis Batak.",
        "Karo mendiami bagian utara, sementara Toba berada di sekitar danau.",
      ],
    },
    {
      src: "/3.jpg",
      period: "lanskap Balige",
      detail: [
        "Hamparan sawah dan pepohonan ini adalah latar keseharian kompleks museum di Balige.",
        "Pemandangan seperti ini menjelaskan mengapa koleksi budaya di kawasan Danau Toba erat dengan pertanian.",
        "Danau dan kehidupan kampung menjadi bagian yang tidak terpisahkan dari kebudayaan setempat.",
        "Lanskapnya juga memperlihatkan bahwa museum ini berada di kawasan pertanian, bukan pusat kota.",
      ],
    },
  ],
};

patches["museum-sisingamangaraja-xii"] = {
  exhibits: [
    {
      title: "Benda peninggalan Sisingamangaraja XII",
      period: "abad ke-19",
      origin: "Kawasan Bakkara, tepi Danau Toba",
      material: "pusaka dan perlengkapan",
      highlight: true,
      description:
        "Ruang ini memuat pusaka dan perlengkapan yang dikaitkan dengan perjuangan raja Batak terakhir. Sisingamangaraja XII memimpin perlawanan terhadap Belanda sampai gugur pada 1907, dan benda-benda peninggalannya menjadi penghubung langsung dengan masa itu. Bakkara, di tepi Danau Toba, adalah kampung asal Sisingamangaraja dan kini menjadi kawasan makam raja-raja Batak. Karena itu kunjungan ke museum ini biasanya menyatu dengan ziarah ke kompleks makam di dekatnya.",
    },
    {
      title: "Senjata tradisional Batak",
      period: "Perang Batak, 1878–1907",
      origin: "Kawasan Toba",
      material: "logam dan kayu",
      description:
        "Senjata ini dipakai dalam perlawanan terhadap Belanda di kawasan Toba. Perang Batak berlangsung lama dan berpindah-pindah, mengikuti gerak pasukan raja yang bergerilya di perbukitan sekitar danau. Senjata tradisional menghadapi senjata api menjelaskan mengapa perlawanan itu berlangsung gigih tetapi akhirnya berakhir dengan gugurnya raja. Bagi pengunjung, benda seperti ini memperlihatkan bahwa perlawanan di Sumatera Utara tidak hanya terjadi di pesisir, tetapi juga di pedalaman danau.",
    },
    {
      title: "Dokumentasi Perang Batak",
      period: "1878–1907",
      origin: "Arsip kolonial dan catatan setempat",
      material: "foto dan catatan",
      description:
        "Foto dan catatan di ruang ini menguraikan jalannya perlawanan di Tanah Batak. Sebagian besar dokumentasi berasal dari pihak kolonial, sehingga cara pandangnya perlu dibaca dengan hati-hati: foto dibuat untuk keperluan administrasi dan laporan militer. Meski begitu, arsip semacam ini tetap menjadi sumber penting karena pihak Batak sendiri jarang meninggalkan catatan tertulis tentang perang tersebut. Museum menempatkannya bersama benda peninggalan agar kedua sisi bisa dibandingkan.",
    },
  ],
  gallery: [
    {
      src: "/1.jpg",
      period: "kawasan makam raja-raja Batak",
      detail: [
        "Bakkara, di tepi Danau Toba, adalah kampung asal Sisingamangaraja.",
        "Kawasan ini kini menjadi kompleks makam raja-raja Batak.",
        "Makamnya berada dekat museum yang mengisahkan perlawanan terhadap Belanda.",
        "Perlawanan itu berakhir dengan gugurnya raja pada 1907.",
      ],
    },
    {
      src: "/2.jpg",
      period: "arsip kolonial, domain publik",
      detail: [
        "Foto ini berasal dari arsip kolonial dan sudah menjadi domain publik.",
        "Sisingamangaraja XII digambarkan dalam busana kebesaran.",
        "Potret semacam ini dipakai sebagai rujukan visual untuk patung, prangko, dan lukisan yang dibuat kemudian.",
        "Karena berasal dari pihak kolonial, konteks pembuatannya perlu diperhatikan.",
      ],
    },
  ],
};

patches["museum-daerah-deli-serdang"] = {
  exhibits: [
    {
      title: "Lantai 1: prasejarah dan kesultanan",
      period: "prasejarah hingga Kesultanan Deli dan Serdang",
      origin: "Lantai satu gedung museum",
      material: "panel, replika, dan benda koleksi",
      highlight: true,
      description:
        "Lantai pertama memuat sejarah Deli Serdang, Kesultanan Deli, dan Kesultanan Serdang, termasuk kisah perjuangan di Deli Serdang. Alurnya disusun dari masa prasejarah menuju berdirinya kesultanan, sehingga pengunjung memahami bahwa dua kesultanan itu muncul dalam lanskap yang sudah lama dihuni. Letak Deli Serdang yang dekat dengan pelabuhan membuat kawasan ini tumbuh cepat pada masa kolonial. Karena itu lantai ini menjadi dasar sebelum pengunjung naik ke koleksi kesultanan di lantai berikutnya.",
    },
    {
      title: "Kisah Putri Hijau",
      period: "legenda Melayu",
      origin: "Tradisi lisan Deli dan Serdang",
      material: "panel naratif",
      description:
        "Kisah Putri Hijau dipaparkan di tangga antara lantai satu dan dua. Legenda ini dikenal luas dalam tradisi Melayu dan dikaitkan dengan asal-usul Kesultanan Deli, sehingga berfungsi sebagai penghubung antara bagian prasejarah dan bagian kesultanan. Menempatkannya di tangga adalah pilihan tata pamer yang menarik: pengunjung membaca kisah sambil berpindah lantai, seperti berpindah dari mitos ke sejarah. Karena berupa legenda, isinya tidak dipakai sebagai bukti sejarah, melainkan sebagai cara masyarakat mengingat asal-usulnya.",
    },
    {
      title: "Lantai 2: koleksi Kesultanan Serdang",
      period: "masa Kesultanan Serdang",
      origin: "Kesultanan Serdang",
      material: "kain, alat musik, perlengkapan rumah tangga, prasasti",
      description:
        "Lantai dua memuat pakaian, alat musik, perlengkapan rumah tangga, hingga prasasti dari masa kesultanan. Koleksi semacam ini memperlihatkan kehidupan istana dari sisi yang jarang dibayangkan: bukan hanya upacara besar, tetapi juga peralatan sehari-hari dan cara orang berpakaian. Alat musik menunjukkan bahwa kesultanan menjadi pusat kegiatan seni, sementara prasasti memberi bukti tertulis tentang pemerintahan. Bersama-sama, benda di lantai ini menggambarkan kesultanan sebagai pusat kebudayaan, bukan hanya kekuasaan.",
    },
    {
      title: "Lantai 3: pasca kemerdekaan",
      period: "setelah 1945",
      origin: "Masa kemerdekaan Indonesia",
      material: "dokumen, foto, dan benda koleksi",
      description:
        "Lantai tiga memuat koleksi yang mengingatkan masa-masa setelah Indonesia merdeka. Bagian ini melengkapi dua lantai sebelumnya dengan menunjukkan apa yang berubah setelah kesultanan tidak lagi berkuasa. Bagi Deli Serdang, masa itu ditandai oleh peralihan pemerintahan, perubahan tata guna tanah, dan pertumbuhan kota di sekitar Medan. Dengan menutup alur di lantai ini, museum menyusun perjalanan dari masa prasejarah sampai pemerintahan republik dalam satu bangunan.",
    },
  ],
  gallery: [
    {
      src: "/1.jpg",
      period: "diresmikan 8 September 2018",
      detail: [
        "Halaman berumput dan deretan pohon ini adalah area museum baru Deli Serdang di Lubuk Pakam.",
        "Museum dibangun di lahan eks Dinas Pertanian.",
        "Diresmikan 8 September 2018.",
        "Museum sebelumnya, dibuka 12 Agustus 2003, berada di kompleks perkantoran Tanjung Garbus.",
      ],
    },
    {
      src: "/2.jpg",
      period: "panel pengantar",
      detail: [
        "Panel kaca ini memuat data luas, jumlah penduduk, dan daftar kabupaten/kota Sumatera Utara.",
        "Isinya juga mencakup fisiografi, yaitu gambaran bentuk permukaan wilayah.",
        "Letaknya di awal alur pameran, sebelum bagian sejarah kesultanan.",
        "Fungsinya memberi konteks geografis sebelum pengunjung masuk ke sejarah Kesultanan Deli dan Serdang.",
      ],
    },
    {
      src: "/3.jpg",
      period: "data pemerintahan",
      detail: [
        "Panel ini memuat daftar kecamatan yang termasuk wilayah Deli Serdang.",
        "Daftar semacam ini membantu pengunjung memahami batas wilayah kabupaten saat ini.",
        "Penempatannya di ruang pamer menunjukkan museum juga mendokumentasikan pemerintahan, bukan hanya benda lama.",
        "Bagi pengunjung lokal, panel ini biasanya menjadi tempat mencari nama kampungnya sendiri.",
      ],
    },
  ],
};

apply();
