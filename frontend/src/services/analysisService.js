const API_BASE = "http://127.0.0.1:8000";

export async function analyzeText(title, text) {
  return fetch(`${API_BASE}/predict`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ title, text }),
  });
}

export async function analyzePdf(file) {
  const formData = new FormData();
  formData.append("file", file);

  return fetch(`${API_BASE}/analyze-pdf`, {
    method: "POST",
    body: formData,
  });
}

export async function analyzeUrl(url) {
  return fetch(`${API_BASE}/analyze-url`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
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
