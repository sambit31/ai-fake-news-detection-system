export default function VerdictBadge({ prediction }) {
  const isReal = prediction === "REAL";

  return (
    <span
      className={`inline-flex items-center rounded-full px-3 py-1 text-xs font-bold ${
        isReal
          ? "bg-emerald-500/10 text-emerald-400 ring-1 ring-emerald-500/20"
          : "bg-red-500/10 text-red-400 ring-1 ring-red-500/20"
      }`}
    >
      {prediction}
    </span>
  );
}
