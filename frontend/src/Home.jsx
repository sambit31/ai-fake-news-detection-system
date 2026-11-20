
import Header from "./components/layout/Header";
import Footer from "./components/layout/Footer";
import { useAuth } from "./context/useAuth";
import { useNavigate } from "react-router-dom";


import {
  FileText,
  BrainCircuit,
  SearchCheck,
  FileSearch,
  ArrowRight,
  Sparkles,
  CheckCircle2,
  Globe2,
  LockKeyhole,
} from "lucide-react";


const features = [
  {
    icon: BrainCircuit,
    title: "Machine Learning Analysis",
    description:
      "Analyze news content using a trained machine-learning classification model.",
  },
  {
    icon: SearchCheck,
    title: "Evidence-Based Verification",
    description:
      "Extract claims and examine available external evidence to support further investigation.",
  },
  {
    icon: FileSearch,
    title: "PDF Document Analysis",
    description:
      "Upload supported PDF documents and analyze their extracted text.",
  },
  {
    icon: Globe2,
    title: "News URL Analysis",
    description:
      "Submit an article URL to retrieve and analyze its available content.",
  },
];

export default function App() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
 

  return (
    <div className="min-h-screen overflow-hidden text-slate-100">
<Header
  user={user}
  onAuthClick={() => navigate("/login")}
  onLogout={logout}
/>

      {/* Hero section */}
      <section
        id="home"
        className="relative px-5 pb-16 pt-20 sm:pb-24 sm:pt-28"
      >
        <div className="pointer-events-none absolute left-1/2 top-0 -z-10 h-[450px] w-[850px] -translate-x-1/2 rounded-full bg-blue-600/10 blur-[140px]" />

        <div className="mx-auto max-w-5xl text-center">
          <div className="mb-7 inline-flex items-center gap-2 rounded-full border border-blue-400/20 bg-blue-400/[0.07] px-4 py-2 text-xs font-semibold tracking-wide text-blue-300">
            <Sparkles size={15} />
            INTELLIGENCE FOR THE INFORMATION AGE
          </div>

          <h1 className="mx-auto max-w-4xl text-4xl font-bold leading-tight tracking-tight text-white sm:text-6xl lg:text-7xl">
            Know What's Real.
            <br />
            <span className="bg-gradient-to-r from-blue-400 via-cyan-300 to-blue-500 bg-clip-text text-transparent">
              Detect What's Fake.
            </span>
          </h1>

          <p className="mx-auto mt-7 max-w-2xl text-base leading-8 text-slate-400 sm:text-lg">
            Make more informed decisions in a world full of information.
            Analyze news articles with machine learning and investigate
            claims using available external evidence.
          </p>

          <div className="mt-9 flex flex-wrap items-center justify-center gap-4">
            <button
              onClick={() => navigate("/analyzer")}
              className="group flex items-center gap-2 rounded-xl bg-blue-600 px-7 py-4 text-sm font-bold text-white shadow-xl shadow-blue-600/20 transition hover:-translate-y-1 hover:bg-blue-500"
            >
              Analyze a news article
              <ArrowRight
                size={18}
                className="transition group-hover:translate-x-1"
              />
            </button>
          <div>
            <a
              href="#how-it-works"
              className="rounded-xl border border-white/10 bg-white/[0.03] px-7 py-4 text-sm font-semibold text-slate-300 transition hover:border-blue-400/40 hover:bg-white/[0.06]"
            >
              Discover how it works
            </a>
            </div>
          </div>

          <div className="mt-12 flex flex-wrap items-center justify-center gap-x-8 gap-y-4 text-xs font-medium text-slate-500">
            <span className="flex items-center gap-2">
              <CheckCircle2 size={15} className="text-cyan-400" />
              Text analysis
            </span>
            <span className="flex items-center gap-2">
              <CheckCircle2 size={15} className="text-cyan-400" />
              PDF support
            </span>
            <span className="flex items-center gap-2">
              <CheckCircle2 size={15} className="text-cyan-400" />
              URL analysis
            </span>
          </div>
        </div>
      </section>

    

      {/* Features section */}
      <section id="features" className="border-y border-white/[0.06] bg-white/[0.015] px-5 py-20 sm:py-24">
        <div className="mx-auto max-w-7xl">
          <div className="mx-auto mb-12 max-w-2xl text-center">
            <p className="mb-3 text-xs font-bold uppercase tracking-[0.25em] text-blue-400">
              Platform capabilities
            </p>

            <h2 className="text-3xl font-bold text-white sm:text-4xl">
              A smarter way to examine information
            </h2>

            <p className="mt-4 text-sm leading-7 text-slate-400">
              Multiple tools come together to help you investigate
              news content and examine supporting evidence.
            </p>
          </div>

          <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
            {features.map((feature, index) => {
              const Icon = feature.icon;

              return (
                <div
                  key={feature.title}
                  className="group rounded-2xl border border-white/[0.07] bg-slate-900/50 p-6 transition duration-300 hover:-translate-y-2 hover:border-blue-400/30 hover:bg-slate-900"
                >
                  <div className="mb-6 inline-flex rounded-xl border border-blue-400/10 bg-blue-500/10 p-3 text-blue-400 transition group-hover:bg-blue-500 group-hover:text-white">
                    <Icon size={24} />
                  </div>

                  <p className="mb-3 text-xs font-semibold text-slate-600">
                    0{index + 1}
                  </p>

                  <h3 className="text-lg font-bold text-white">
                    {feature.title}
                  </h3>

                  <p className="mt-3 text-sm leading-7 text-slate-400">
                    {feature.description}
                  </p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* How it works */}
      <section id="how-it-works" className="px-5 py-20 sm:py-24">
        <div className="mx-auto max-w-6xl">
          <div className="mb-14 text-center">
            <p className="mb-3 text-xs font-bold uppercase tracking-[0.25em] text-blue-400">
              Simple process
            </p>

            <h2 className="text-3xl font-bold text-white sm:text-4xl">
              How VerityAI works
            </h2>
          </div>

          <div className="grid gap-8 md:grid-cols-3">
            {[
              {
                number: "01",
                title: "Submit your content",
                description:
                  "Enter news text, upload a supported PDF, or provide an article URL.",
                icon: FileText,
              },
              {
                number: "02",
                title: "Analyze the information",
                description:
                  "The machine-learning model examines the available article content.",
                icon: BrainCircuit,
              },
              {
                number: "03",
                title: "Review the findings",
                description:
                  "Examine the prediction, explanation and any available supporting evidence.",
                icon: SearchCheck,
              },
            ].map((step) => {
              const Icon = step.icon;

              return (
                <div key={step.number} className="relative rounded-2xl border border-white/[0.07] bg-slate-900/40 p-7">
                  <div className="mb-6 flex items-center justify-between">
                    <div className="rounded-xl bg-blue-500/10 p-3 text-blue-400">
                      <Icon size={25} />
                    </div>
                    <span className="text-3xl font-bold text-slate-800">
                      {step.number}
                    </span>
                  </div>

                  <h3 className="text-xl font-bold text-white">
                    {step.title}
                  </h3>

                  <p className="mt-3 text-sm leading-7 text-slate-400">
                    {step.description}
                  </p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* About and transparency */}
      <section id="about" className="px-5 pb-20">
        <div className="mx-auto max-w-5xl overflow-hidden rounded-3xl border border-blue-400/15 bg-gradient-to-br from-blue-500/[0.10] via-slate-900/80 to-cyan-500/[0.05] p-7 sm:p-12">
          <div className="flex flex-col gap-6 sm:flex-row sm:items-start">
            <div className="shrink-0 rounded-2xl border border-blue-400/20 bg-blue-500/10 p-4 text-blue-400">
              <LockKeyhole size={30} />
            </div>

            <div>
              <p className="mb-3 text-xs font-bold uppercase tracking-[0.2em] text-blue-400">
                Transparency matters
              </p>

              <h2 className="text-2xl font-bold text-white sm:text-3xl">
                Technology can assist. Critical thinking still matters.
              </h2>

              <p className="mt-4 text-sm leading-7 text-slate-400">
                VerityAI provides machine-learning predictions and
                evidence-based investigation tools. A model prediction
                is not proof that an entire article is true or false.
                Always review the original sources and supporting evidence
                before drawing conclusions.
              </p>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}
