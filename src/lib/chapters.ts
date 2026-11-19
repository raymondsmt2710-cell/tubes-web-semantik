export interface ChapterDef {
  index: number;
  label: string;
  title: string;
  intro: string;
  provinces: string[];
}

/**
 * Tujuh bab perjalanan, dari barat ke timur. Definisi ini statis (tidak
 * bergantung pada Fuseki) supaya sampul tetap bisa menampilkan alur ketika
 * basis data sedang tidak dapat dihubungi.
 */
export const CHAPTERS: ChapterDef[] = [
  {
    index: 1,
    label: "Bab I",
    title: "Dari Pelabuhan ke Pedalaman",
    intro:
      "Aceh adalah pintu masuk pertama Islam ke Nusantara dan saksi perang terpanjang melawan kolonialisme. Di antara mesjid, naskah, dan rumah panggung, museum-museumnya menyimpan dua wajah sekaligus: pelabuhan dagang yang kosmopolitan dan pedalaman yang gigih bertahan.",
    provinces: ["Aceh"],
  },
  {
    index: 2,
    label: "Bab II",
    title: "Tanah Karo dan Danau Toba",
    intro:
      "Di sekitar Danau Toba, ingatan disimpan bukan hanya di dalam lemari kaca tetapi juga di rumah adat yang masih berdiri. Bab ini menelusuri jejak Batak Toba, Melayu Deli, dan perlawanan Sisingamangaraja dari tepi danau hingga kota pelabuhan Medan.",
    provinces: ["Sumatera Utara"],
  },
  {
    index: 3,
    label: "Bab III",
    title: "Jejak Kerajaan Melayu",
    intro:
      "Riau dan Kepulauan Riau adalah poros kebudayaan Melayu: bahasa, naskah, dan istana yang tersebar dari Siak sampai Pulau Penyengat. Museum-museum di bab ini menyimpan sisa kejayaan maritim yang pernah menghubungkan Sumatera dengan seluruh Asia Tenggara.",
    provinces: ["Riau", "Kepulauan Riau"],
  },
  {
    index: 4,
    label: "Bab IV",
    title: "Rumah Gadang dan Perang Padri",
    intro:
      "Sumatera Barat menyimpan dua cerita besar: kebudayaan Minangkabau yang matrilineal dan Perang Padri yang mengubah wajah pedalaman. Dari ukiran rumah gadang sampai lokomotif tambang Ombilin, bab ini bergerak antara adat dan industri.",
    provinces: ["Sumatera Barat"],
  },
  {
    index: 5,
    label: "Bab V",
    title: "Antara Batanghari dan Bukit Barisan",
    intro:
      "Jambi dan Bengkulu berdiri di dua sisi Bukit Barisan. Di satu sisi, Batanghari membawa temuan Sriwijaya dan budaya Melayu; di sisi lain, Bengkulu menyimpan rumah pengasingan Soekarno dan kekayaan alam yang keras.",
    provinces: ["Jambi", "Bengkulu"],
  },
  {
    index: 6,
    label: "Bab VI",
    title: "Sungai Musi dan Timah",
    intro:
      "Palembang pernah menjadi pusat maritim terbesar di Nusantara, sementara Bangka Belitung dibentuk oleh tambang timah. Bab ini mempertemukan arkeologi kerajaan dengan sejarah teknologi pertambangan.",
    provinces: ["Sumatera Selatan", "Bangka Belitung"],
  },
  {
    index: 7,
    label: "Bab VII",
    title: "Gerbang Selat Sunda",
    intro:
      "Lampung adalah ujung selatan Sumatera, tempat Selat Sunda memisahkan pulau ini dari Jawa. Bab penutup ini menyatukan situs megalitik, budaya Saibatin dan Pepadun, serta kisah transmigrasi yang membentuk wajah provinsi ini.",
    provinces: ["Lampung"],
  },
];

export function chapterByIndex(index: number): ChapterDef | undefined {
  return CHAPTERS.find((c) => c.index === index);
}

export const ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII"];

export function chapterSlug(index: number): string {
  return String(index);
}
