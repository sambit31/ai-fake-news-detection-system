import {
  AlertTriangle,
  Loader2,
  Search,
  RotateCcw,
} from "lucide-react";

import TextInput from "./TextInput.jsx";
import PDFInput from "./PDFInput.jsx";
import URLInput from "./URLInput.jsx";

export default function AnalysisForm({
  tabs,
  activeTab,
  setActiveTab,
  resetResult,
  title,
  setTitle,
  articleText,
  setArticleText,
  file,
  setFile,
  url,
  setUrl,
  error,
  loading,
  handleAnalysis,
  clearForm,
}) {
  return (
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
          <TextInput
            title={title}
            setTitle={setTitle}
            articleText={articleText}
            setArticleText={setArticleText}
          />
        )}

        {/* PDF input */}
        {activeTab === "pdf" && (
          <PDFInput
            file={file}
            setFile={setFile}
            resetResult={resetResult}
          />
        )}

        {/* URL input */}
        {activeTab === "url" && (
          <URLInput
            url={url}
            setUrl={setUrl}
          />
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
  );
}