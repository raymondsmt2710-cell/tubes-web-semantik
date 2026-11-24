interface FacilityListProps {
  facilities: string[] | undefined;
}

/**
 * Fasilitas museum yang disebutkan sumbernya. Tidak merender apa pun bila
 * kosong — banyak museum memang tidak mencantumkan daftar fasilitas.
 */
export default function FacilityList({ facilities }: FacilityListProps) {
  if (!facilities || facilities.length === 0) return null;

  return (
    <div>
      <h2 className="text-lg">Fasilitas</h2>
      <ul className="mt-3 flex flex-wrap gap-x-5 gap-y-1.5 text-sm text-[--ink-soft]">
        {facilities.map((facility) => (
          <li key={facility} className="flex items-center gap-1.5">
            <span aria-hidden className="text-[--gold]">•</span>
            <span className="capitalize">{facility}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
