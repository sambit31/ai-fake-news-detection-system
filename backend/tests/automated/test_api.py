import pytest
from fastapi.testclient import TestClient

from api import main


client = TestClient(main.app)


# --------------------------------------------------
# ROOT AND HEALTH ENDPOINT TESTS
# --------------------------------------------------

def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Fake News Detection API is running"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["model_loaded"] is True


# --------------------------------------------------
# TEXT VALIDATION TESTS
# --------------------------------------------------

def test_predict_rejects_short_text():
    response = client.post(
        "/predict",
        json={"title": "Test", "text": "Too short"}
    )

    assert response.status_code == 422


def test_predict_requires_text():
    response = client.post(
        "/predict",
        json={"title": "Test"}
    )

    assert response.status_code == 422


def test_predict_rejects_excessively_long_title():
    response = client.post(
        "/predict",
        json={
            "title": "A" * 501,
            "text": "This is a sufficiently long article for validation."
        }
    )

    assert response.status_code == 422


# --------------------------------------------------
# PDF VALIDATION TESTS
# --------------------------------------------------

def test_pdf_rejects_non_pdf_file():
    response = client.post(
        "/analyze-pdf",
        files={
            "file": (
                "document.txt",
                b"This is not a PDF",
                "text/plain"
            )
        }
    )

    assert response.status_code == 400
    assert "PDF" in response.json()["detail"]


def test_pdf_rejects_empty_file():
    response = client.post(
        "/analyze-pdf",
        files={
            "file": (
                "empty.pdf",
                b"",
                "application/pdf"
            )
        }
    )

    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()


# --------------------------------------------------
# URL SECURITY TESTS
# --------------------------------------------------

def test_url_rejects_unsupported_protocol():
    response = client.post(
        "/analyze-url",
        json={"url": "ftp://example.com"}
    )

    assert response.status_code == 400


def test_url_rejects_localhost():
    response = client.post(
        "/analyze-url",
        json={"url": "http://localhost"}
    )

    assert response.status_code == 400
    assert "Local URLs" in response.json()["detail"]


def test_url_rejects_private_ip(monkeypatch):
    monkeypatch.setattr(
        main.socket,
        "getaddrinfo",
        lambda hostname, port: [
            (None, None, None, None, ("192.168.1.10", 0))
        ]
    )

    with pytest.raises(main.HTTPException) as error:
        main.validate_public_url("http://example.com")

    assert error.value.status_code == 400
    assert "Private or local" in error.value.detail


def test_url_accepts_public_ip(monkeypatch):
    monkeypatch.setattr(
        main.socket,
        "getaddrinfo",
        lambda hostname, port: [
            (None, None, None, None, ("8.8.8.8", 0))
        ]
    )

    # This tests URL validation only.
    # It does not make an external network request.
    main.validate_public_url("https://example.com")


def test_url_rejects_unresolvable_domain(monkeypatch):
    import socket

    def raise_dns_error(hostname, port):
        raise socket.gaierror("DNS lookup failed")

    monkeypatch.setattr(
        main.socket,
        "getaddrinfo",
        raise_dns_error
    )

    with pytest.raises(main.HTTPException) as error:
        main.validate_public_url("https://example.invalid")

    assert error.value.status_code == 400
    assert "resolve" in error.value.detail.lower()

# --------------------------------------------------
# ACTUAL ML PREDICTION TEST
# --------------------------------------------------

def test_predict_runs_actual_ml_model():
    text = "RBI regulates banks and monetary policy."

    assert 30 <= len(text) < 50

    response = client.post(
        "/predict",
        json={
            "title": "",
            "text": text
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["source"] == "text"
    assert data["prediction"] in ("FAKE", "REAL")
    assert data["label"] in (0, 1)

    assert data["label"] == (
        1 if data["prediction"] == "REAL" else 0
    )

    assert data["decision_threshold"] == -0.50
    assert isinstance(data["decision_score"], float)
    assert data["extracted_text_length"] == len(text)

    assert "not a probability" in data["disclaimer"]

    assert data["fact_check"]["status"] == "skipped"

# --------------------------------------------------
# VALID PDF ANALYSIS TEST
# --------------------------------------------------

def test_pdf_rejects_blank_pdf(monkeypatch):
    from io import BytesIO
    from pypdf import PdfWriter

    writer = PdfWriter()
    writer.add_blank_page(width=300, height=300)

    pdf_buffer = BytesIO()
    writer.write(pdf_buffer)

    def fake_analyze_article(title, text, source):
        return {
            "success": True,
            "source": source,
            "title": title,
            "prediction": "REAL",
            "label": 1,
            "fact_check": {"status": "skipped"}
        }

    monkeypatch.setattr(
        main,
        "analyze_article",
        fake_analyze_article
    )

    response = client.post(
        "/analyze-pdf",
        files={
            "file": (
                "sample.pdf",
                pdf_buffer.getvalue(),
                "application/pdf"
            )
        }
    )

    assert response.status_code == 422
    assert "No readable text" in response.json()["detail"]

# --------------------------------------------------
# SUCCESSFUL PDF EXTRACTION TEST
# --------------------------------------------------

def test_pdf_successful_text_extraction(monkeypatch):
    from io import BytesIO
    from pypdf import PdfWriter

    writer = PdfWriter()
    writer.add_blank_page(width=300, height=300)

    pdf_buffer = BytesIO()
    writer.write(pdf_buffer)

    captured = {}

    def fake_analyze_article(title, text, source):
        captured["title"] = title
        captured["text"] = text
        captured["source"] = source

        return {
            "success": True,
            "source": source,
            "title": title,
            "prediction": "REAL",
            "label": 1,
            "fact_check": {"status": "skipped"}
        }

    monkeypatch.setattr(
        main,
        "analyze_article",
        fake_analyze_article
    )

    # Replace the PDF reader with a controlled
    # reader that returns readable text.
    class FakePage:
        def extract_text(self):
            return "The Reserve Bank of India regulates banks and monetary policy."

    class FakePDF:
        is_encrypted = False
        pages = [FakePage()]

    monkeypatch.setattr(main, "PdfReader", lambda *args, **kwargs: FakePDF())

    response = client.post(
        "/analyze-pdf",
        files={
            "file": (
                "rbi_article.pdf",
                pdf_buffer.getvalue(),
                "application/pdf"
            )
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["filename"] == "rbi_article.pdf"
    assert data["pages"] == 1
    assert data["title"] == "rbi_article"
    assert data["source"] == "pdf"

    assert captured["title"] == "rbi_article"
    assert "Reserve Bank of India" in captured["text"]
    assert captured["source"] == "pdf"

# --------------------------------------------------
# SUCCESSFUL URL ANALYSIS TEST
# --------------------------------------------------

def test_url_successful_analysis(monkeypatch):
    from types import SimpleNamespace
    import httpx

    captured = {}

    class FakeResponse:
        headers = {"content-type": "text/html; charset=utf-8"}
        encoding = "utf-8"

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            pass

        def raise_for_status(self):
            pass

        async def aiter_bytes(self):
            yield b"<html><body>Mock news article</body></html>"

    class FakeClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            pass

        def stream(self, method, url):
            captured["method"] = method
            captured["url"] = url
            return FakeResponse()

    def fake_extract(html, **kwargs):
        return "The Reserve Bank of India regulates banks and monetary policy."

    def fake_metadata(html):
        return SimpleNamespace(title="RBI Article")

    def fake_analyze_article(title, text, source):
        captured["title"] = title
        captured["text"] = text
        captured["source"] = source

        return {
            "success": True,
            "source": source,
            "title": title,
            "prediction": "REAL",
            "label": 1,
            "fact_check": {"status": "skipped"}
        }

    monkeypatch.setattr(main.httpx, "AsyncClient", FakeClient)
    monkeypatch.setattr(main.trafilatura, "extract", fake_extract)
    monkeypatch.setattr(main.trafilatura, "extract_metadata", fake_metadata)
    monkeypatch.setattr(main, "analyze_article", fake_analyze_article)
    monkeypatch.setattr(main, "validate_public_url", lambda url: None)

    response = client.post(
        "/analyze-url",
        json={"url": "https://example.com/article"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["source"] == "url"
    assert data["title"] == "RBI Article"
    assert data["url"] == "https://example.com/article"
    assert data["prediction"] == "REAL"

    assert captured["method"] == "GET"
    assert captured["title"] == "RBI Article"
    assert "Reserve Bank of India" in captured["text"]
    assert captured["source"] == "url"

