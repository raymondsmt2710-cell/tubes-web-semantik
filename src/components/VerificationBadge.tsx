interface VerificationBadgeProps {
  status: string | null;
}

export default function VerificationBadge({ status }: VerificationBadgeProps) {
  const verified = status === "terverifikasi";
  return (
    <span
      className={`inline-flex items-center gap-1.5 text-xs px-2 py-1 border rounded-sm ${
        verified
          ? "border-[--accent] text-[--accent] bg-[--accent-soft]"
          : "border-[--rule] text-[--ink-soft] bg-[--paper-2]"
      }`}
      title={
        verified
          ? "Data museum ini sudah diperiksa."
          : "Data museum ini disusun untuk pembelajaran dan belum diperiksa ulang."
      }
    >
      <span aria-hidden>{verified ? "✓" : "!"}</span>
      {verified ? "Terverifikasi" : "Perlu verifikasi"}
    </span>
  );
}
