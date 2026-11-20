import { AlertTriangle, CheckCircle2 } from "lucide-react";
import FactCheckResults from "./FactCheckResults";
import VerdictBadge from "../common/VerdictBadge";

export default function AnalysisResult({ result }) {
  if (!result) return null;

  const isFake = result.prediction === "FAKE";

  return (
    <div className="mt-7 rounded-2xl border border-slate-800 bg-slate-900 p-6">
      <div className="mb-5 flex items-center justify-between gap-3">
        <h3 className="text-lg font-bold">Analysis result</h3>

        <span className="rounded-full bg-slate-800 px-3 py-1 text-xs uppercase text-slate-400">
          {result.source}
        </span>
      </div>

      {/* ML prediction */}
      <div
        className={`rounded-xl border p-5 ${
          isFake
            ? "border-red-500/30 bg-red-500/10"
            : "border-emerald-500/30 bg-emerald-500/10"
        }`}
      >
        <div className="flex items-center gap-3">
          {isFake ? (
            <AlertTriangle size={30} className="text-red-400" />
          ) : (
            <CheckCircle2 size={30} className="text-emerald-400" />
          )}

          <div>
            <p className="text-xs font-medium uppercase tracking-wider text-slate-400">
              Machine-learning prediction
            </p>

            <div className="mt-2">
              <VerdictBadge prediction={result.prediction} />
            </div>
          </div>
        </div>

        <p className="mt-4 text-sm leading-6 text-slate-300">
          {result.explanation}
        </p>
      </div>

      {/* Article information */}
      <div className="mt-5 grid gap-3 sm:grid-cols-2">
        <div className="rounded-xl bg-slate-950 p-4">
          <p className="text-xs text-slate-500">Article title</p>
          <p className="mt-1 break-words text-sm font-medium">
            {result.title || "Not available"}
          </p>
        </div>

        <div className="rounded-xl bg-slate-950 p-4">
          <p className="text-xs text-slate-500">
            Extracted characters
          </p>
          <p className="mt-1 text-sm font-medium">
            {result.extracted_text_length ?? "Not available"}
          </p>
        </div>
      </div>

      {/* Evidence-based fact-check */}
      <FactCheckResults factCheck={result.fact_check} />

      {result.disclaimer && (
        <p className="mt-5 text-xs leading-5 text-slate-500">
          Disclaimer: {result.disclaimer}
        </p>
      )}
    </div>
  );
}