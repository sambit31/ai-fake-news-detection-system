import { useState } from "react";
import {
  analyzeText,
  analyzePdf,
  analyzeUrl,
  getAnalysisResult,
} from "../../services/analysisService";

export default function useNewsAnalysis() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [history, setHistory] = useState([]);

  const resetResult = () => {
    setResult(null);
    setError("");
  };

  const saveHistory = (data) => {
    setHistory((previous) => [
      {
        id: Date.now(),
        source: data.source || "unknown",
        title: data.title || "Untitled article",
        prediction: data.prediction || "UNKNOWN",
        time: new Date().toLocaleTimeString(),
      },
      ...previous,
    ]);
  };

  const handleAnalysis = async (
    event,
    activeTab,
    title,
    articleText,
    file,
    url
  ) => {
    event.preventDefault();
    resetResult();

    if (activeTab === "text" && articleText.trim().length < 30) {
      setError("Please enter at least 30 characters of article text.");
      return;
    }

    if (activeTab === "pdf" && !file) {
      setError("Please select a PDF file.");
      return;
    }

    if (activeTab === "url" && !url.trim()) {
      setError("Please enter a news article URL.");
      return;
    }

    setLoading(true);

    try {
      let response;

      if (activeTab === "text") {
        response = await analyzeText(title, articleText);
      } else if (activeTab === "pdf") {
        response = await analyzePdf(file);
      } else if (activeTab === "url") {
        response = await analyzeUrl(url);
      } else {
        throw new Error("Please select a valid analysis method.");
      }

      const data = await getAnalysisResult(response);

      setResult(data);
      saveHistory(data);
    } catch (err) {
      setError(
        err.message === "Failed to fetch"
          ? "Cannot connect to the backend. Make sure FastAPI is running at http://127.0.0.1:8000."
          : err.message
      );
    } finally {
      setLoading(false);
    }
  };

  return {
    loading,
    result,
    error,
    history,
    setError,
    resetResult,
    handleAnalysis,
  };
}
