
import { useState } from "react";
import {
  ShieldCheck,
  FileText,
  Link as LinkIcon,
  Upload,
  Search,
  Loader2,
  CheckCircle2,
  AlertTriangle,
  History,
  Newspaper,
  RotateCcw,
  X,
  ExternalLink,
  Clock,
  Info,
} from "lucide-react";

const API_BASE = "http://127.0.0.1:8000";

const tabs = [
  { id: "text", label: "Article Text", icon: FileText },
  { id: "pdf", label: "Upload PDF", icon: Upload },
  { id: "url", label: "News URL", icon: LinkIcon },
];

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

function FactCheckResults({ factCheck }) {
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

export default function App() {
  const [activeTab, setActiveTab] = useState("text");
  const [title, setTitle] = useState("");
  const [articleText, setArticleText] = useState("");
  const [url, setUrl] = useState("");
  const [file, setFile] = useState(null);

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [history, setHistory] = useState([]);

  const resetResult = () => {
    setResult(null);
    setError("");
  };

  const saveHistory = (data) => {
    setHistory((previous) => [
      {
        id: Date.now(),
        source: data.source || "unknown",
        title: data.title || "Untitled article",
        prediction: data.prediction || "UNKNOWN",
        time: new Date().toLocaleTimeString(),
      },
      ...previous,
    ]);
  };

  const handleAnalysis = async (event) => {
    event.preventDefault();
    resetResult();

    if (activeTab === "text" && articleText.trim().length < 30) {
      setError("Please enter at least 30 characters of article text.");
      return;
    }

    if (activeTab === "pdf" && !file) {
      setError("Please select a PDF file.");
      return;
    }

    if (activeTab === "url" && !url.trim()) {
      setError("Please enter a news article URL.");
      return;
    }

    setLoading(true);

    try {
      let response;

      if (activeTab === "text") {
        response = await fetch(`${API_BASE}/predict`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            title,
            text: articleText,
          }),
        });
      }

      if (activeTab === "pdf") {
        const formData = new FormData();
        formData.append("file", file);

        response = await fetch(`${API_BASE}/analyze-pdf`, {
          method: "POST",
          body: formData,
        });
      }

      if (activeTab === "url") {
        response = await fetch(`${API_BASE}/analyze-url`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ url }),
        });
      }

      if (!response) {
        throw new Error("Please select a valid analysis method.");
      }

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Analysis failed. Please try again."
        );
      }

      setResult(data);
      saveHistory(data);
    } catch (err) {
      setError(
        err.message === "Failed to fetch"
          ? "Cannot connect to the backend. Make sure FastAPI is running at http://127.0.0.1:8000."
          : err.message
      );
    } finally {
      setLoading(false);
    }
  };

  const clearForm = () => {
    setTitle("");
    setArticleText("");
    setUrl("");
    setFile(null);
    resetResult();
  };

  const isFake = result?.prediction === "FAKE";

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-950/90">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-5 py-5 lg:px-8">
          <div className="flex items-center gap-3">
            <div className="rounded-xl bg-blue-600 p-2.5">
              <ShieldCheck size={25} />
            </div>

            <div>
              <h1 className="text-xl font-bold tracking-tight">
                Misinformation Detector
              </h1>
              <p className="text-xs text-slate-400">
                ML classification and evidence-based fact-checking
              </p>
            </div>
          </div>

          <div className="hidden items-center gap-2 rounded-full border border-emerald-500/20 bg-emerald-500/10 px-4 py-2 text-sm text-emerald-400 sm:flex">
            <span className="h-2 w-2 rounded-full bg-emerald-400" />
            Analysis platform
          </div>
        </div>
      </header>

      <main className="mx-auto grid max-w-7xl gap-8 px-5 py-10 lg:grid-cols-[1fr_320px] lg:px-8">
        {/* Main analysis section */}
        <section>
          <div className="mb-8">
            <p className="mb-3 text-sm font-semibold uppercase tracking-[0.2em] text-blue-400">
              Misinformation detection
            </p>

            <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
              Examine news with{" "}
              <span className="text-blue-400">evidence.</span>
            </h2>

            <p className="mt-3 max-w-2xl text-slate-400">
              Analyze news articles using machine learning and
              evidence-based AI fact-checking. Paste text, upload a PDF,
              or submit an article URL.
            </p>
          </div>

          {/* Analysis card */}
          <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5 shadow-2xl sm:p-7">
            {/* Tabs */}
            <div className="mb-7 grid grid-cols-3 gap-2 rounded-xl bg-slate-950 p-1.5">
              {tabs.map((tab) => {
                const Icon = tab.icon;

                return (
                  <button
                    key={tab.id}
                    type="button"
                    onClick={() => {
                      setActiveTab(tab.id);
                      resetResult();
                    }}
                    className={`flex items-center justify-center gap-2 rounded-lg px-2 py-3 text-xs font-semibold transition sm:text-sm ${
                      activeTab === tab.id
                        ? "bg-blue-600 text-white shadow-lg"
                        : "text-slate-400 hover:bg-slate-800 hover:text-white"
                    }`}
                  >
                    <Icon size={17} />
                    <span className="hidden sm:inline">{tab.label}</span>
                    <span className="sm:hidden">
                      {tab.id === "text"
                        ? "Text"
                        : tab.id === "pdf"
                          ? "PDF"
                          : "URL"}
                    </span>
                  </button>
                );
              })}
            </div>

            <form onSubmit={handleAnalysis}>
              {/* Text input */}
              {activeTab === "text" && (
                <div className="space-y-5">
                  <div>
                    <label className="mb-2 block text-sm font-medium text-slate-300">
                      Article headline (optional)
                    </label>

                    <input
                      type="text"
                      value={title}
                      onChange={(e) => setTitle(e.target.value)}
                      placeholder="Enter the news headline..."
                      className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm outline-none transition placeholder:text-slate-600 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
                    />
                  </div>

                  <div>
                    <div className="mb-2 flex justify-between">
                      <label className="text-sm font-medium text-slate-300">
                        News article
                      </label>

                      <span className="text-xs text-slate-500">
                        {articleText.length} characters
                      </span>
                    </div>

                    <textarea
                      rows={10}
                      value={articleText}
                      onChange={(e) => setArticleText(e.target.value)}
                      placeholder="Paste the complete news article here..."
                      className="w-full resize-y rounded-xl border border-slate-700 bg-slate-950 px-4 py-4 text-sm leading-7 outline-none transition placeholder:text-slate-600 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
                    />
                  </div>
                </div>
              )}

              {/* PDF input */}
              {activeTab === "pdf" && (
                <div>
                  <label
                    htmlFor="pdf-upload"
                    className="flex min-h-64 cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed border-slate-700 bg-slate-950 p-8 text-center transition hover:border-blue-500 hover:bg-blue-500/5"
                  >
                    <div className="mb-4 rounded-2xl bg-blue-500/10 p-4 text-blue-400">
                      <Upload size={32} />
                    </div>

                    <p className="font-semibold">
                      {file ? file.name : "Upload your news PDF"}
                    </p>

                    <p className="mt-2 text-sm text-slate-400">
                      {file
                        ? "PDF selected successfully"
                        : "Click to browse and select a PDF file"}
                    </p>

                    <p className="mt-3 text-xs text-slate-500">
                      Maximum file size: 10 MB
                    </p>

                    <input
                      id="pdf-upload"
                      type="file"
                      accept=".pdf,application/pdf"
                      className="hidden"
                      onChange={(e) => {
                        const selectedFile = e.target.files?.[0];

                        if (selectedFile) {
                          setFile(selectedFile);
                          resetResult();
                        }
                      }}
                    />
                  </label>

                  {file && (
                    <button
                      type="button"
                      onClick={() => setFile(null)}
                      className="mt-3 flex items-center gap-2 text-sm text-red-400 hover:text-red-300"
                    >
                      <X size={16} />
                      Remove selected file
                    </button>
                  )}
                </div>
              )}

              {/* URL input */}
              {activeTab === "url" && (
                <div className="py-8">
                  <label className="mb-3 block text-sm font-medium text-slate-300">
                    News article URL
                  </label>

                  <div className="flex items-center gap-3 rounded-xl border border-slate-700 bg-slate-950 px-4 py-1 focus-within:border-blue-500">
                    <LinkIcon size={19} className="shrink-0 text-slate-500" />

                    <input
                      type="url"
                      value={url}
                      onChange={(e) => setUrl(e.target.value)}
                      placeholder="https://example.com/news/article"
                      className="w-full bg-transparent py-4 text-sm outline-none placeholder:text-slate-600"
                    />
                  </div>

                  <p className="mt-3 text-xs text-slate-500">
                    Use a publicly accessible individual news article URL.
                  </p>
                </div>
              )}

              {/* Error */}
              {error && (
                <div className="mt-5 flex items-start gap-3 rounded-xl border border-red-500/20 bg-red-500/10 p-4 text-sm text-red-300">
                  <AlertTriangle size={19} className="mt-0.5 shrink-0" />
                  <p>{error}</p>
                </div>
              )}

              {/* Buttons */}
              <div className="mt-7 flex flex-wrap gap-3">
                <button
                  type="submit"
                  disabled={loading}
                  className="flex flex-1 items-center justify-center gap-2 rounded-xl bg-blue-600 px-5 py-3.5 font-semibold text-white transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  {loading ? (
                    <>
                      <Loader2 size={19} className="animate-spin" />
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <Search size={19} />
                      Analyze news
                    </>
                  )}
                </button>

                <button
                  type="button"
                  onClick={clearForm}
                  className="flex items-center justify-center gap-2 rounded-xl border border-slate-700 px-5 py-3.5 text-sm font-medium text-slate-300 transition hover:bg-slate-800"
                >
                  <RotateCcw size={17} />
                  Reset
                </button>
              </div>
            </form>
          </div>

          {/* Analysis result */}
          {result && (
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

                    <p
                      className={`text-2xl font-bold ${
                        isFake ? "text-red-400" : "text-emerald-400"
                      }`}
                    >
                      {result.prediction}
                    </p>
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
          )}
        </section>

        {/* Sidebar */}
        <aside className="space-y-6">
          <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">
            <div className="mb-5 flex items-center gap-3">
              <div className="rounded-lg bg-blue-500/10 p-2 text-blue-400">
                <History size={20} />
              </div>

              <div>
                <h3 className="font-bold">Recent analyses</h3>
                <p className="text-xs text-slate-500">
                  Current session only
                </p>
              </div>
            </div>

            {history.length === 0 ? (
              <div className="py-8 text-center">
                <Newspaper
                  size={30}
                  className="mx-auto mb-3 text-slate-600"
                />

                <p className="text-sm text-slate-400">No analyses yet</p>

                <p className="mt-1 text-xs text-slate-600">
                  Your results will appear here.
                </p>
              </div>
            ) : (
              <div className="space-y-3">
                {history.slice(0, 8).map((item) => (
                  <div
                    key={item.id}
                    className="rounded-xl bg-slate-950 p-3"
                  >
                    <div className="flex items-center justify-between gap-2">
                      <span className="truncate text-sm font-medium">
                        {item.title}
                      </span>

                      <span
                        className={`shrink-0 text-xs font-bold ${
                          item.prediction === "FAKE"
                            ? "text-red-400"
                            : "text-emerald-400"
                        }`}
                      >
                        {item.prediction}
                      </span>
                    </div>

                    <p className="mt-2 flex items-center gap-1 text-xs text-slate-500">
                      <Clock size={12} />
                      {item.source.toUpperCase()} · {item.time}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="rounded-2xl border border-blue-500/20 bg-blue-500/5 p-5">
            <ShieldCheck size={26} className="mb-3 text-blue-400" />

            <h3 className="font-bold">About this system</h3>

            <p className="mt-2 text-sm leading-6 text-slate-400">
              This platform combines a trained LinearSVC machine-learning
              model with AI-based claim extraction and external evidence
              verification.
            </p>

            <p className="mt-3 text-xs leading-5 text-slate-500">
              ML predictions and evidence-based verdicts are separate
              results. Neither guarantees that an entire article is true
              or false.
            </p>
          </div>
        </aside>
      </main>

      <footer className="border-t border-slate-800 px-5 py-6 text-center text-xs text-slate-600">
        Misinformation Detection Platform · Powered by FastAPI, Machine
        Learning and Evidence-Based AI
      </footer>
    </div>
  );
}
