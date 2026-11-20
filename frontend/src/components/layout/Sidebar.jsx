
import {
  History,
  Newspaper,
  Clock,
  ShieldCheck,
  Trash2,
  LoaderCircle,
} from "lucide-react";

export default function Sidebar({
  history = [],
  historyLoading = false,
  onDeleteHistory,
}) {
  const formatDate = (date) => {
    if (!date) return "Date unavailable";

    return new Date(date).toLocaleString();
  };

  return (
    <aside className="space-y-6">
      <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">
        <div className="mb-5 flex items-center gap-3">
          <div className="rounded-lg bg-blue-500/10 p-2 text-blue-400">
            <History size={20} />
          </div>

          <div>
            <h3 className="font-bold">Analysis history</h3>
            <p className="text-xs text-slate-500">
              Your previous investigations
            </p>
          </div>
        </div>

        {historyLoading ? (
          <div className="flex items-center justify-center gap-2 py-8 text-sm text-slate-400">
            <LoaderCircle size={18} className="animate-spin" />
            Loading history...
          </div>
        ) : history.length === 0 ? (
          <div className="py-8 text-center">
            <Newspaper
              size={30}
              className="mx-auto mb-3 text-slate-600"
            />

            <p className="text-sm text-slate-400">No analyses yet</p>

            <p className="mt-1 text-xs text-slate-600">
              Your completed analyses will appear here.
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {history.slice(0, 10).map((item) => (
              <div
                key={item.id}
                className="rounded-xl bg-slate-950 p-3"
              >
                <div className="flex items-start justify-between gap-2">
                  <p className="min-w-0 break-words text-sm font-medium text-slate-200">
                    {item.title || "Untitled article"}
                  </p>

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
                  {(item.source || "unknown").toUpperCase()}
                </p>

                <p className="mt-1 text-xs text-slate-600">
                  {formatDate(item.created_at || item.time)}
                </p>

                {onDeleteHistory && (
                  <button
                    type="button"
                    onClick={() => onDeleteHistory(item.id)}
                    className="mt-3 flex items-center gap-1 text-xs text-red-400 transition hover:text-red-300"
                  >
                    <Trash2 size={13} />
                    Delete
                  </button>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="rounded-2xl border border-blue-500/20 bg-blue-500/5 p-5">
        <ShieldCheck size={26} className="mb-3 text-blue-400" />

        <h3 className="font-bold">About VerityAI</h3>

        <p className="mt-2 text-sm leading-6 text-slate-400">
          This platform combines a trained machine-learning model
          with AI-based claim extraction and external evidence
          verification.
        </p>

        <p className="mt-3 text-xs leading-5 text-slate-500">
          A machine-learning prediction is not proof that an entire
          article is true or false. Always examine the available
          evidence.
        </p>
      </div>
    </aside>
  );
}
