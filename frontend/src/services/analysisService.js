
const API_BASE =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

// Add the access token only when a user is logged in.
function getHeaders(token, additionalHeaders = {}) {
  return {
    ...additionalHeaders,
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
}

export async function analyzeText(title, text, token = null) {
  return fetch(`${API_BASE}/predict`, {
    method: "POST",
    headers: getHeaders(token, {
      "Content-Type": "application/json",
    }),
    body: JSON.stringify({ title, text }),
  });
}

export async function analyzePdf(file, token = null) {
  const formData = new FormData();
  formData.append("file", file);

  return fetch(`${API_BASE}/analyze-pdf`, {
    method: "POST",
    headers: getHeaders(token),
    body: formData,
  });
}

export async function analyzeUrl(url, token = null) {
  return fetch(`${API_BASE}/analyze-url`, {
    method: "POST",
    headers: getHeaders(token, {
      "Content-Type": "application/json",
    }),
    body: JSON.stringify({ url }),
  });
}

export async function getAnalysisResult(response) {
  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Analysis failed. Please try again."
    );
  }

  return data;
}
