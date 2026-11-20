import {
  CheckCircle2,
  AlertTriangle,
  ExternalLink,
  Info,
} from "lucide-react";
const verdictStyles = {
  SUPPORTED: {
    label: "SUPPORTED",
    color: "text-emerald-400",
    background: "bg-emerald-500/10",
    border: "border-emerald-500/30",
    icon: CheckCircle2,
  },
  CONTRADICTED: {
    label: "CONTRADICTED",
    color: "text-red-400",
    background: "bg-red-500/10",
    border: "border-red-500/30",
    icon: AlertTriangle,
  },
  INSUFFICIENT_EVIDENCE: {
    label: "INSUFFICIENT EVIDENCE",
    color: "text-amber-400",
    background: "bg-amber-500/10",
    border: "border-amber-500/30",
    icon: Info,
  },
};

function VerdictBadge({ verdict }) {
  const style =
    verdictStyles[verdict] ||
    verdictStyles.INSUFFICIENT_EVIDENCE;

  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full border px-3 py-1.5 text-xs font-bold ${style.color} ${style.background} ${style.border}`}
    >
      <style.icon size={14} />
      {style.label}
    </span>
  );
}

export default function FactCheckResults({ factCheck }) {
  if (!factCheck) {
    return (
      <div className="mt-6 rounded-xl border border-slate-700 bg-slate-950 p-5">
        <div className="flex items-center gap-2 text-slate-400">
          <Info size={19} />
          <h4 className="font-semibold">Fact-check information unavailable</h4>
        </div>
        <p className="mt-2 text-sm text-slate-500">
          The machine-learning result is available, but no fact-check
          information was returned.
        </p>
      </div>
    );
  }

  if (factCheck.status === "unavailable") {
    return (
      <div className="mt-6 rounded-xl border border-amber-500/30 bg-amber-500/5 p-5">
        <div className="flex items-center gap-2 text-amber-400">
          <AlertTriangle size={19} />
          <h4 className="font-semibold">Fact-checking unavailable</h4>
        </div>
        <p className="mt-2 text-sm leading-6 text-slate-400">
          The article was classified by the ML model, but the fact-checking
          process could not be completed. Please try again later.
        </p>
      </div>
    );
  }

  if (factCheck.status === "skipped") {
    return (
      <div className="mt-6 rounded-xl border border-slate-700 bg-slate-950 p-5">
        <div className="flex items-center gap-2 text-slate-300">
          <Info size={19} />
          <h4 className="font-semibold">Fact-checking skipped</h4>
        </div>
        <p className="mt-2 text-sm text-slate-400">
          The submitted article did not contain enough text for fact-checking.
        </p>
      </div>
    );
  }

  const summary = factCheck.summary || {};
  const claims = Array.isArray(factCheck.claims)
    ? factCheck.claims
    : [];

  return (
    <div className="mt-7 space-y-5">
      {/* Fact-check heading */}
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h3 className="text-lg font-bold">Evidence-based fact-check</h3>
          <p className="mt-1 text-xs text-slate-500">
            Claims evaluated using external webpage content
          </p>
        </div>

        <span className="rounded-full border border-emerald-500/20 bg-emerald-500/10 px-3 py-1.5 text-xs font-semibold text-emerald-400">
          {factCheck.status === "completed" ? "Completed" : "Available"}
        </span>
      </div>

      {/* Summary cards */}
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
        <div className="rounded-xl border border-slate-700 bg-slate-950 p-4">
          <p className="text-xs text-slate-500">Total claims</p>
          <p className="mt-2 text-2xl font-bold">
            {summary.total_claims ?? claims.length}
          </p>
        </div>

        <div className="rounded-xl border border-emerald-500/20 bg-emerald-500/5 p-4">
          <p className="text-xs text-emerald-400">Supported</p>
          <p className="mt-2 text-2xl font-bold text-emerald-400">
            {summary.supported ?? 0}
          </p>
        </div>

        <div className="rounded-xl border border-red-500/20 bg-red-500/5 p-4">
          <p className="text-xs text-red-400">Contradicted</p>
          <p className="mt-2 text-2xl font-bold text-red-400">
            {summary.contradicted ?? 0}
          </p>
        </div>

        <div className="rounded-xl border border-amber-500/20 bg-amber-500/5 p-4">
          <p className="text-xs text-amber-400">Insufficient</p>
          <p className="mt-2 text-2xl font-bold text-amber-400">
            {summary.insufficient_evidence ?? 0}
          </p>
        </div>
      </div>

      {/* Individual claims */}
      <div className="space-y-4">
        <h4 className="font-semibold text-slate-200">
          Individual claim analysis
        </h4>

        {claims.length === 0 ? (
          <div className="rounded-xl border border-slate-700 bg-slate-950 p-5 text-sm text-slate-400">
            No verifiable claims were extracted from this article.
          </div>
        ) : (
          claims.map((claim, index) => {
            const verdict = claim.verdict;
            const style =
              verdictStyles[verdict] ||
              verdictStyles.INSUFFICIENT_EVIDENCE;

            const sources = Array.isArray(claim.sources_used)
              ? claim.sources_used
              : [];

            const reviewed = Array.isArray(claim.sources_reviewed)
              ? claim.sources_reviewed
              : [];

            return (
              <div
                key={claim.claim_number ?? index}
                className="rounded-xl border border-slate-700 bg-slate-950 p-5"
              >
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">
                    Claim {claim.claim_number ?? index + 1}
                  </span>

                  <VerdictBadge verdict={verdict} />
                </div>

                <p className="mt-4 text-sm font-medium leading-7 text-slate-200">
                  {claim.claim}
                </p>

                {claim.importance && (
                  <p className="mt-2 text-xs text-slate-500">
                    Importance: {claim.importance}
                  </p>
                )}

                <div
                  className={`mt-4 rounded-lg border p-4 ${style.border} ${style.background}`}
                >
                  <p className="mb-2 text-xs font-semibold uppercase tracking-wider text-slate-400">
                    Verification explanation
                  </p>
                  <p className="text-sm leading-6 text-slate-300">
                    {claim.explanation ||
                      "No explanation was provided."}
                  </p>
                </div>

                {/* Sources used */}
                <div className="mt-5">
                  <h5 className="mb-3 flex items-center gap-2 text-sm font-semibold text-slate-300">
                    <ExternalLink size={16} />
                    Evidence sources
                  </h5>

                  {sources.length === 0 ? (
                    <p className="text-sm text-slate-500">
                      No external sources were cited for this verdict.
                    </p>
                  ) : (
                    <div className="space-y-2">
                      {sources.map((source, sourceIndex) => (
                        <div
                          key={`${source.url}-${sourceIndex}`}
                          className="rounded-lg border border-slate-800 bg-slate-900 p-3"
                        >
                          <p className="break-words text-sm font-medium text-slate-200">
                            {source.title || "External source"}
                          </p>

                          {source.url && (
                            <a
                              href={source.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="mt-2 inline-flex items-center gap-1.5 break-all text-xs text-blue-400 hover:text-blue-300"
                            >
                              Open source
                              <ExternalLink size={13} />
                            </a>
                          )}
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                {/* Source retrieval details */}
                {reviewed.length > 0 && (
                  <details className="mt-4 rounded-lg border border-slate-800 bg-slate-900">
                    <summary className="cursor-pointer px-4 py-3 text-xs font-medium text-slate-400 hover:text-slate-200">
                      View source retrieval details ({reviewed.length})
                    </summary>

                    <div className="space-y-3 border-t border-slate-800 p-4">
                      {reviewed.map((source, sourceIndex) => (
                        <div
                          key={`${source.url}-${sourceIndex}`}
                          className="text-xs"
                        >
                          <p className="break-words font-medium text-slate-300">
                            {source.title || "Untitled source"}
                          </p>
                          <p className="mt-1 break-all text-slate-500">
                            {source.url}
                          </p>
                          <p
                            className={`mt-1 font-semibold ${
                              source.status === "FETCHED"
                                ? "text-emerald-400"
                                : "text-amber-400"
                            }`}
                          >
                            {source.status}
                          </p>
                          {source.error && (
                            <p className="mt-1 break-words text-red-400">
                              {source.error}
                            </p>
                          )}
                        </div>
                      ))}
                    </div>
                  </details>
                )}
              </div>
            );
          })
        )}
      </div>

      <p className="text-xs leading-5 text-slate-500">
        Evidence-based verdicts are generated by an AI system using retrieved
        webpage content. They are not guaranteed to be correct. Review the
        cited sources independently.
      </p>
    </div>
  );
}

