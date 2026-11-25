
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  ShieldCheck,
  LogOut,
  Home,
  FileText,
  Upload,
  Link as LinkIcon,
  History,
  ScanSearch,
} from "lucide-react";

import { useAuth } from "../context/useAuth";
import useNewsAnalysis from "../components/hooks/useNewsAnalysis";
import AnalysisForm from "../components/analysis/AnalysisForm";
import AnalysisResult from "../components/analysis/AnalysisResult";
import Sidebar from "../components/layout/Sidebar";

const tabs = [
  { id: "text", label: "Article Text", icon: FileText },
  { id: "pdf", label: "Upload PDF", icon: Upload },
  { id: "url", label: "News URL", icon: LinkIcon },
];

export default function Dashboard() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const [activeTab, setActiveTab] = useState("text");
  const [title, setTitle] = useState("");
  const [articleText, setArticleText] = useState("");
  const [file, setFile] = useState(null);
  const [url, setUrl] = useState("");

  const {
    loading,
    result,
    error,
    history,
    stats,
    historyLoading,
    resetResult,
    handleAnalysis,
    handleDeleteHistory,
  } = useNewsAnalysis();

  const clearForm = () => {
    setTitle("");
    setArticleText("");
    setFile(null);
    setUrl("");
    resetResult();
  };

  const onLogout = () => {
    logout();
    navigate("/app");
  };

  return (
    <div className="min-h-screen bg-[#070b17] text-slate-100">
      {/* Dashboard header */}
      <header className="sticky top-0 z-50 border-b border-white/[0.07] bg-[#070b17]/90 backdrop-blur-xl">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-5 py-4">
          <div className="flex items-center gap-3">
            <div className="rounded-xl bg-gradient-to-br from-blue-500 to-cyan-400 p-2.5">
              <ShieldCheck size={24} />
            </div>

            <div>
              <h1 className="text-lg font-bold">
                Verity<span className="text-blue-400">AI</span>
              </h1>
              <p className="text-[10px] tracking-wider text-slate-500">
                ANALYSIS WORKSPACE
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <span className="hidden text-sm text-slate-400 sm:inline">
              {user?.full_name || user?.email}
            </span>

            <button
              type="button"
              onClick={() => navigate("/")}
              className="flex items-center gap-2 rounded-lg border border-white/10 px-3 py-2 text-sm text-slate-300 hover:bg-white/5"
            >
              <Home size={16} />
              <span className="hidden sm:inline">Home</span>
            </button>

            <button
  type="button"
  onClick={() => navigate("/dashboard")}
  className="flex items-center gap-2 rounded-lg border border-blue-500/20 px-3 py-2 text-sm text-blue-300 hover:bg-blue-500/10"
>
  <History size={16} />
  <span className="hidden sm:inline">History</span>
</button>

            <button
              type="button"
              onClick={onLogout}
              className="flex items-center gap-2 rounded-lg border border-red-500/20 px-3 py-2 text-sm text-red-300 hover:bg-red-500/10"
            >
              <LogOut size={16} />
              <span className="hidden sm:inline">Logout</span>
            </button>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-5 py-10">
        {/* Welcome */}
        <section className="mb-10">
  <div className="flex items-center gap-2 text-sm font-semibold tracking-widest text-blue-400">
    <ScanSearch size={17} />
    VERITYAI INTELLIGENCE PLATFORM
  </div>

  <h2 className="mt-4 text-3xl font-bold tracking-tight text-white sm:text-4xl">
    Welcome back, {user?.full_name?.split(" ")[0] || "User"}
    <span className="text-blue-400">.</span>
  </h2>

  <div className="mt-3 flex flex-wrap items-center gap-3 text-sm">
    <span className="text-slate-400">
      Your workspace for smarter news verification.
    </span>

    <span className="hidden h-1 w-1 rounded-full bg-slate-600 sm:block" />

    <span className="inline-flex items-center gap-1.5 text-emerald-400">
      <span className="h-2 w-2 rounded-full bg-emerald-400" />
      AI analysis workspace
    </span>
  </div>

  <p className="mt-5 max-w-2xl text-sm leading-7 text-slate-400">
    Analyze news articles using text, PDF documents, or URLs.
    Extract important claims, investigate information, and examine
    supporting evidence to make more informed decisions.
  </p>
</section>

       

        {/* Analyzer */}
        <section id="analyzer">
          <div className="mb-5">
            <h3 className="text-2xl font-bold text-white">
              News Analyzer
            </h3>
            <p className="mt-2 text-sm text-slate-400">
              Choose an input method to start investigating an article.
            </p>
          </div>

          <div className="grid items-start gap-7 lg:grid-cols-[minmax(0,1fr)_340px]">
            <div className="min-w-0">
              <AnalysisForm
                tabs={tabs}
                activeTab={activeTab}
                setActiveTab={setActiveTab}
                resetResult={resetResult}
                title={title}
                setTitle={setTitle}
                articleText={articleText}
                setArticleText={setArticleText}
                file={file}
                setFile={setFile}
                url={url}
                setUrl={setUrl}
                error={error}
                loading={loading}
                handleAnalysis={(event) =>
                  handleAnalysis(
                    event,
                    activeTab,
                    title,
                    articleText,
                    file,
                    url
                  )
                }
                clearForm={clearForm}
              />

              <AnalysisResult result={result} />
            </div>

            <Sidebar
              history={history}
              stats={stats}
              historyLoading={historyLoading}
              onDeleteHistory={handleDeleteHistory}
            />
          </div>
        </section>
      </main>
    </div>
  );
}
