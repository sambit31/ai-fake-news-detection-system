
const API_BASE =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

async function historyRequest(endpoint, token, options = {}) {
  if (!token) {
    throw new Error("Please sign in to access your analysis history.");
  }

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers: {
      Authorization: `Bearer ${token}`,
      ...options.headers,
    },
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Could not access analysis history."
    );
  }

  return data;
}

export function fetchHistory(token, page = 1, limit = 10, filters = {}) {
  const params = new URLSearchParams({
    page: String(page),
    limit: String(limit),
  });

  if (filters.source) {
    params.set("source", filters.source);
  }

  if (filters.prediction) {
    params.set("prediction", filters.prediction);
  }

  return historyRequest(`/history/?${params.toString()}`, token);
}

export function fetchHistoryStats(token) {
  return historyRequest("/history/stats", token);
}

export function fetchHistoryItem(token, analysisId) {
  return historyRequest(`/history/${analysisId}`, token);
}

export function deleteHistoryItem(token, analysisId) {
  return historyRequest(`/history/${analysisId}`, token, {
    method: "DELETE",
  });
}
