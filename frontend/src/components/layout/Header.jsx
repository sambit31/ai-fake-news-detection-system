import { ShieldCheck } from "lucide-react";

export default function Header() {
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

}
