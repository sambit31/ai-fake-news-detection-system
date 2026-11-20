
import { ShieldCheck, ArrowRight } from "lucide-react";

export default function Header() {
  return (
    <header className="sticky top-0 z-50 border-b border-white/[0.07] bg-[#070b17]/85 backdrop-blur-xl">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-5 py-4 lg:px-8">
        <a href="#home" className="flex items-center gap-3">
          <div className="rounded-xl bg-gradient-to-br from-blue-500 to-cyan-400 p-2.5 text-white shadow-lg shadow-blue-500/20">
            <ShieldCheck size={25} />
          </div>

          <div>
            <h1 className="text-lg font-bold tracking-tight text-white">
              Verity<span className="text-blue-400">AI</span>
            </h1>
            <p className="text-[10px] tracking-wider text-slate-500">
              INTELLIGENCE PLATFORM
            </p>
          </div>
        </a>

        <nav className="hidden items-center gap-8 text-sm text-slate-400 md:flex">
          <a href="#home" className="hover:text-white">Home</a>
          <a href="#features" className="hover:text-white">Features</a>
          <a href="#how-it-works" className="hover:text-white">How it works</a>
          <a href="#about" className="hover:text-white">About</a>
        </nav>

        <a
          href="#analyzer"
          className="flex items-center gap-2 rounded-xl bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white shadow-lg shadow-blue-600/20 hover:bg-blue-500"
        >
          Start analyzing
          <ArrowRight size={16} />
        </a>
      </div>
    </header>
  );
}
