
import {
  ShieldCheck,
  ArrowRight,
  LogOut,
  UserRound,
} from "lucide-react";
import { useNavigate } from "react-router-dom";

export default function Header({
  user,
  onAuthClick,
  onLogout,
}) 
{
  const navigate = useNavigate();
  return (
    <header className="sticky top-0 z-50 border-b border-white/[0.07] bg-[#070b17]/85 backdrop-blur-xl">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-5 py-4 lg:px-8">
        <a href="#home" className="flex shrink-0 items-center gap-3">
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

        <div className="flex shrink-0 items-center gap-2">
          {user ? (
            <>
              <div className="hidden items-center gap-2 text-sm text-slate-300 sm:flex">
                <UserRound size={17} className="text-blue-400" />
                <span className="max-w-28 truncate">
                  {user.full_name || user.email}
                </span>
              </div>

              <button
                type="button"
                onClick={onLogout}
                className="flex items-center gap-2 rounded-xl border border-white/10 px-3 py-2.5 text-sm font-semibold text-slate-300 transition hover:border-red-400/30 hover:text-red-300"
              >
                <LogOut size={16} />
                <span className="hidden sm:inline">Sign out</span>
              </button>
            </>
          ) : (
            <button
              type="button"
              onClick={onAuthClick}
              className="rounded-xl border border-white/10 px-4 py-2.5 text-sm font-semibold text-slate-300 transition hover:border-blue-400/40 hover:text-white"
            >
              Sign in
            </button>
          )}
   <div>
          <button
            type="button"
            onClick={() => navigate("/register")}
            className="flex items-center gap-2 rounded-xl bg-blue-600 px-3 py-2.5 text-sm font-semibold text-white shadow-lg shadow-blue-600/20 transition hover:bg-blue-500 sm:px-4"
          >
         
            <span className="hidden sm:inline">Start analyzing</span>
            <span className="sm:hidden">Analyze</span>
            <ArrowRight size={16} />
          </button>
          </div>
        </div>
      </div>
    </header>
  );
}
