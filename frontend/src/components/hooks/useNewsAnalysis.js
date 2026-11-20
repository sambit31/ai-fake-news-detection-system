
import { useCallback, useEffect, useState } from "react";

import {
  analyzeText,
  analyzePdf,
  analyzeUrl,
  getAnalysisResult,
} from "../../services/analysisService";

import {
  fetchHistory,
  fetchHistoryStats,
  deleteHistoryItem,
} from "../../services/historyService";

import { useAuth } from "../../context/useAuth";

export default function useNewsAnalysis() {
  const { token, isAuthenticated } = useAuth();

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [history, setHistory] = useState([]);
  const [stats, setStats] = useState(null);
  const [historyLoading, setHistoryLoading] = useState(false);

  const resetResult = () => {
    setResult(null);
    setError("");
  };

  const loadHistory = useCallback(async () => {
    if (!token || !isAuthenticated) {
      setHistory([]);
      setStats(null);
      return;
    }

    setHistoryLoading(true);

    try {
      const [historyData, statsData] = await Promise.all([
        fetchHistory(token, 1, 10),
        fetchHistoryStats(token),
      ]);

      setHistory(historyData.items || []);
      setStats(statsData);
    } catch (err) {
      console.error("History loading failed:", err);
      setError(err.message || "Could not load analysis history.");
    } finally {
      setHistoryLoading(false);
    }
  }, [token, isAuthenticated]);

  useEffect(() => {
  let active = true;

  if (isAuthenticated && token) {
    Promise.all([
      fetchHistory(token, 1, 10),
      fetchHistoryStats(token),
    ])
      .then(([historyData, statsData]) => {
        if (!active) return;

        setHistory(historyData.items || []);
        setStats(statsData);
      })
      .catch((err) => {
        if (!active) return;

        console.error("History loading failed:", err);
        setError(err.message || "Could not load analysis history.");
      })
      .finally(() => {
        if (active) {
          setHistoryLoading(false);
        }
      });
  } else {
    Promise.resolve().then(() => {
      if (!active) return;

      setHistory([]);
      setStats(null);
      setHistoryLoading(false);
    });
  }

  return () => {
    active = false;
  };
}, [isAuthenticated, token]);


  const handleDeleteHistory = async (analysisId) => {
    try {
      await deleteHistoryItem(token, analysisId);
      await loadHistory();
    } catch (err) {
      setError(err.message || "Could not delete analysis history.");
    }
  };

  const saveGuestHistory = (data) => {
    setHistory((previous) => [
      {
        id: Date.now(),
        source: data.source || "unknown",
        title: data.title || "Untitled article",
        prediction: data.prediction || "UNKNOWN",
        time: new Date().toISOString(),
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
        response = await analyzeText(title, articleText, token);
      } else if (activeTab === "pdf") {
        response = await analyzePdf(file, token);
      } else if (activeTab === "url") {
        response = await analyzeUrl(url, token);
      } else {
        throw new Error("Please select a valid analysis method.");
      }

      const data = await getAnalysisResult(response);

      setResult(data);

      if (isAuthenticated) {
        await loadHistory();
      } else {
        saveGuestHistory(data);
      }
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
    stats,
    historyLoading,
    setError,
    resetResult,
    handleAnalysis,
    handleDeleteHistory,
    refreshHistory: loadHistory,
  };
}
