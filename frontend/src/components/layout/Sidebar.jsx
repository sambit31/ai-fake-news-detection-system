import { History, Newspaper, Clock, ShieldCheck } from "lucide-react";

export default function Sidebar({ history }) {
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
                      {item.source.toUpperCase()} Â· {item.time}
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

}
