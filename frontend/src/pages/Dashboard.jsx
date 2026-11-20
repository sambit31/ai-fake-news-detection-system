
import { useNavigate } from "react-router-dom";
import {
  ShieldCheck,
  LogOut,
  ScanSearch,
  History,
  FileText,
  Trash2,
  Clock,
  TrendingUp,
  CheckCircle2,
  AlertTriangle,
} from "lucide-react";

import { useAuth } from "../context/useAuth";
import useNewsAnalysis from "../components/hooks/useNewsAnalysis";

export default function Dashboard() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const {
    history = [],
    stats,
    historyLoading,
    handleDeleteHistory,
  } = useNewsAnalysis();

  const onLogout = () => {
    logout();
    navigate("/app");
  };

  const formatDate = (date) => {
    if (!date) return "Date unavailable";

    return new Date(date).toLocaleString();
  };

  return (
    <div className="min-h-screen bg-[#070b17] text-slate-100">
      <header className="sticky top-0 z-50 border-b border-white/[0.07] bg-[#070b17]/90 backdrop-blur-xl">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-5 py-4">
          <div className="flex items-center gap-3">
            <div className="rounded-xl bg-gradient-to-br from-blue-500 to-cyan-400 p-2.5">
              <ShieldCheck size={24} />
            </div>
            <div>
              <h1 className="text-lg font-bold">
                Verity<span className="text-blue-400">AI</span>
              </h1>
              <p className="text-[10px] tracking-wider text-slate-500">
                HISTORY DASHBOARD
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <span className="hidden text-sm text-slate-400 sm:inline">
              {user?.full_name || user?.email}
            </span>

            <button
              type="button"
              onClick={() => navigate("/analyzer")}
              className="flex items-center gap-2 rounded-lg bg-blue-600 px-3 py-2 text-sm font-semibold text-white hover:bg-blue-500"
            >
              <ScanSearch size={16} />
              <span className="hidden sm:inline">Open Analyzer</span>
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
        <section className="mb-9">
          <div className="flex items-center gap-2 text-sm text-blue-400">
            <History size={17} />
            Your activity
          </div>

          <h2 className="mt-3 text-3xl font-bold sm:text-4xl">
            Analysis History
          </h2>

          <p className="mt-3 text-sm leading-7 text-slate-400">
            Review your previous investigations and track your
            news analysis activity.
          </p>
        </section>

        <section className="mb-9 grid gap-4 sm:grid-cols-3">
          <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">
            <div className="flex items-center justify-between">
              <p className="text-sm text-slate-400">Total analyses</p>
              <TrendingUp className="text-blue-400" size={21} />
            </div>
            <p className="mt-3 text-3xl font-bold">
              {stats?.total_analyses ?? 0}
            </p>
          </div>

          <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">
            <div className="flex items-center justify-between">
              <p className="text-sm text-slate-400">Predicted real</p>
              <CheckCircle2 className="text-emerald-400" size={21} />
            </div>
            <p className="mt-3 text-3xl font-bold text-emerald-400">
              {stats?.real_count ?? 0}
            </p>
          </div>

          <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">
            <div className="flex items-center justify-between">
              <p className="text-sm text-slate-400">Predicted fake</p>
              <AlertTriangle className="text-red-400" size={21} />
            </div>
            <p className="mt-3 text-3xl font-bold text-red-400">
              {stats?.fake_count ?? 0}
            </p>
          </div>
        </section>

        <section className="rounded-2xl border border-slate-800 bg-slate-900 p-5 sm:p-7">
          <div className="mb-6 flex items-center justify-between gap-3">
            <div>
              <h3 className="text-xl font-bold">Previous analyses</h3>
              <p className="mt-1 text-sm text-slate-400">
                Your saved news investigations
              </p>
            </div>
            <History size={24} className="text-blue-400" />
          </div>

          {historyLoading ? (
            <p className="py-10 text-center text-slate-400">
              Loading your history...
            </p>
          ) : history.length === 0 ? (
            <div className="py-12 text-center">
              <FileText
                size={38}
                className="mx-auto mb-4 text-slate-600"
              />
              <h4 className="font-semibold">No analysis history yet</h4>
              <p className="mt-2 text-sm text-slate-500">
                Your completed analyses will appear here.
              </p>
              <button
                type="button"
                onClick={() => navigate("/analyzer")}
                className="mt-5 rounded-lg bg-blue-600 px-5 py-2.5 text-sm font-semibold hover:bg-blue-500"
              >
                Analyze your first article
              </button>
            </div>
          ) : (
            <div className="space-y-3">
              {history.map((item) => (
                <div
                  key={item.id}
                  className="rounded-xl border border-slate-800 bg-[#070b17] p-4"
                >
                  <div className="flex flex-col justify-between gap-3 sm:flex-row sm:items-center">
                    <div className="min-w-0">
                      <h4 className="break-words font-semibold text-slate-200">
                        {item.title || "Untitled article"}
                      </h4>

                      <div className="mt-2 flex flex-wrap items-center gap-3 text-xs text-slate-500">
                        <span className="flex items-center gap-1">
                          <FileText size={13} />
                          {(item.source || "unknown").toUpperCase()}
                        </span>
                        <span className="flex items-center gap-1">
                          <Clock size={13} />
                          {formatDate(item.created_at || item.time)}
                        </span>
                      </div>
                    </div>

                    <div className="flex shrink-0 items-center justify-between gap-4 sm:justify-end">
                      <span
                        className={`rounded-lg px-3 py-1.5 text-xs font-bold ${
                          item.prediction === "FAKE"
                            ? "bg-red-500/10 text-red-400"
                            : "bg-emerald-500/10 text-emerald-400"
                        }`}
                      >
                        {item.prediction || "UNKNOWN"}
                      </span>

                      <button
                        type="button"
                        onClick={() => handleDeleteHistory(item.id)}
                        className="rounded-lg p-2 text-slate-500 transition hover:bg-red-500/10 hover:text-red-400"
                        title="Delete analysis"
                      >
                        <Trash2 size={17} />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}
