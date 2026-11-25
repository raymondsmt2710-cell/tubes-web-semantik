import { describe, it, expect } from "vitest";
import type { Exhibit, MuseumImage } from "./types";

describe("tipe isi pameran dan foto", () => {
  it("menerima bidang kedalaman pada Exhibit", () => {
    const exhibit: Exhibit = {
      title: "Lonceng Cakra Donya",
      description: "Deskripsi panjang yang memenuhi ambang validator.",
      period: "abad ke-15",
      origin: "Kesultanan Pasai",
      material: "perunggu",
      highlight: true,
    };
    expect(exhibit.period).toBe("abad ke-15");
    expect(exhibit.highlight).toBe(true);
  });

  it("menerima bidang kedalaman pada MuseumImage", () => {
    const image: MuseumImage = {
      src: "/images/museums/x/1.jpg",
      alt: "Foto",
      caption: "Keterangan",
      credit: "Seseorang",
      license: "CC BY-SA 4.0",
      licenseUrl: null,
      sourceUrl: "https://commons.wikimedia.org/wiki/File:X.jpg",
      period: "1915",
      detail: ["Poin pertama", "Poin kedua"],
    };
    expect(image.detail).toHaveLength(2);
  });
});
