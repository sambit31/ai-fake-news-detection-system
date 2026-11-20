import { useState } from "react";
import AnalysisResult from "./components/analysis/AnalysisResult";
import AnalysisForm from "./components/analysis/AnalysisForm";
import Header from "./components/layout/Header";
import Sidebar from "./components/layout/Sidebar";
import Footer from "./components/layout/Footer";
import useNewsAnalysis from "./components/hooks/useNewsAnalysis";

import {
  FileText,
  Link as LinkIcon,
  Upload,
} from "lucide-react";

const tabs = [
  { id: "text", label: "Article Text", icon: FileText },
  { id: "pdf", label: "Upload PDF", icon: Upload },
  { id: "url", label: "News URL", icon: LinkIcon },
];

export default function App() {
  const [activeTab, setActiveTab] = useState("text");
  const [title, setTitle] = useState("");
  const [articleText, setArticleText] = useState("");
  const [url, setUrl] = useState("");
  const [file, setFile] = useState(null);

  const {
    loading,
    result,
    error,
    history,
    resetResult,
    handleAnalysis,
  } = useNewsAnalysis();

  const onAnalyze = (event) => {
    handleAnalysis(
      event,
      activeTab,
      title,
      articleText,
      file,
      url
    );
  };

  const clearForm = () => {
    setTitle("");
    setArticleText("");
    setUrl("");
    setFile(null);
    resetResult();
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <Header />

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
            handleAnalysis={onAnalyze}
            clearForm={clearForm}
          />

          <AnalysisResult result={result} />
        </section>

        <Sidebar history={history} />
      </main>

      <Footer />
    </div>
  );
}