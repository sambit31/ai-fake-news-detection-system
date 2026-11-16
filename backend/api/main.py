
import sys
import ipaddress
import socket

from io import BytesIO
from pathlib import Path
from urllib.parse import urlparse

import httpx
import joblib
import trafilatura

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from pypdf import PdfReader
from starlette.concurrency import run_in_threadpool


# --------------------------------------------------
# PATH CONFIGURATION
# --------------------------------------------------

BACKEND_DIR = Path(__file__).resolve().parents[1]
ML_DIR = BACKEND_DIR / "ml"

MODEL_PATH = ML_DIR / "artifacts" / "fake_news_pipeline.joblib"

# Required to load the preprocessing function
# stored inside the trained sklearn pipeline.
sys.path.insert(0, str(ML_DIR))


# --------------------------------------------------
# LOAD TRAINED MODEL
# --------------------------------------------------

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

model = joblib.load(MODEL_PATH)

print("Fake news detection model loaded successfully!")


# --------------------------------------------------
# APPLICATION CONFIGURATION
# --------------------------------------------------

app = FastAPI(
    title="Fake News Detection API",
    description=(
        "Fake news classification using LinearSVC "
        "and evidence-based AI fact-checking."
    ),
    version="1.2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# LIMITS
# --------------------------------------------------

MAX_PDF_SIZE = 10 * 1024 * 1024
MAX_PDF_PAGES = 30
MAX_URL_SIZE = 8 * 1024 * 1024

MIN_ARTICLE_LENGTH = 30
MIN_FACT_CHECK_LENGTH = 50


# --------------------------------------------------
# REQUEST SCHEMAS
# --------------------------------------------------

class PredictionRequest(BaseModel):
    title: str = Field(default="", max_length=500)
    text: str = Field(
        min_length=MIN_ARTICLE_LENGTH,
        max_length=100000
    )


class URLRequest(BaseModel):
    url: str = Field(min_length=8, max_length=2048)


# --------------------------------------------------
# ML PREDICTION FUNCTION
# --------------------------------------------------


# --------------------------------------------------
# ML PREDICTION FUNCTION
# --------------------------------------------------

DECISION_THRESHOLD = -0.50


def classify_article(title: str, text: str, source: str):

    title = (title or "").strip()
    text = (text or "").strip()

    article = f"{title} {text}".strip()

    if len(article) < MIN_ARTICLE_LENGTH:
        raise HTTPException(
            status_code=422,
            detail="Not enough article text was extracted for prediction."
        )

    try:
        # Get LinearSVC decision score.
        decision_score = float(
            model.decision_function([article])[0]
        )

        # Project label convention:
        # 0 = Fake
        # 1 = Real

        prediction = (
            1 if decision_score >= DECISION_THRESHOLD else 0
        )

        if prediction == 0:
            result = "FAKE"
            explanation = (
                "The machine-learning model classified "
                "this article as Fake."
            )
        else:
            result = "REAL"
            explanation = (
                "The machine-learning model classified "
                "this article as Real."
            )

        return {
            "success": True,
            "source": source,
            "title": title,
            "prediction": result,
            "label": prediction,
            "decision_score": round(decision_score, 4),
            "decision_threshold": DECISION_THRESHOLD,
            "explanation": explanation,
            "extracted_text_length": len(text),
            "disclaimer": (
                "This is a machine-learning classification, "
                "not independent verification of the article's truth. "
                "The decision score is not a probability."
            )
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(error)}"
        )

# --------------------------------------------------
# COMBINED ML + FACT-CHECK ANALYSIS
# --------------------------------------------------

def analyze_article(title: str, text: str, source: str):
    """
    First performs the existing ML prediction.
    Then performs evidence-based fact-checking.

    Fact-checking errors do not remove a successful
    ML prediction.
    """

    # STEP 1: Existing ML prediction
    result = classify_article(
        title=title,
        text=text,
        source=source
    )

    # STEP 2: Check whether enough text exists
    if len(text.strip()) < MIN_FACT_CHECK_LENGTH:

        result["fact_check"] = {
            "status": "skipped",
            "message": (
                "Fact-checking requires at least "
                f"{MIN_FACT_CHECK_LENGTH} characters of article text."
            ),
            "summary": {
                "total_claims": 0,
                "supported": 0,
                "contradicted": 0,
                "insufficient_evidence": 0
            },
            "claims": []
        }

        return result

    # STEP 3: Run the existing fact-checking pipeline
    try:

        # Import lazily so a missing fact-checking dependency
        # does not prevent the API from loading.
        from api.article_fact_check import fact_check_article

        article_text = f"{title}\n{text}".strip()

        fact_check_result = fact_check_article(
            article_text=article_text,
            max_claims=5,
            max_search_results=5,
            max_pages_per_claim=3
        )

        fact_check_result["status"] = "completed"

        result["fact_check"] = fact_check_result

    except Exception as error:

        print(
            "Fact-checking could not be completed:",
            type(error).__name__,
            str(error)
        )

        result["fact_check"] = {
            "status": "unavailable",
            "message": (
                "Fact-checking could not be completed. "
                "The ML prediction is still available."
            ),
            "summary": {
                "total_claims": 0,
                "supported": 0,
                "contradicted": 0,
                "insufficient_evidence": 0
            },
            "claims": []
        }

    return result


# --------------------------------------------------
# URL VALIDATION
# --------------------------------------------------

def validate_public_url(url: str):

    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https"):
        raise HTTPException(
            status_code=400,
            detail="Only HTTP and HTTPS URLs are supported."
        )

    hostname = parsed.hostname

    if not hostname:
        raise HTTPException(
            status_code=400,
            detail="Invalid URL."
        )

    if hostname.lower() == "localhost":
        raise HTTPException(
            status_code=400,
            detail="Local URLs are not allowed."
        )

    try:

        addresses = socket.getaddrinfo(hostname, None)

        for address in addresses:

            ip = ipaddress.ip_address(address[4][0])

            if (
                ip.is_private
                or ip.is_loopback
                or ip.is_link_local
                or ip.is_reserved
                or ip.is_multicast
                or ip.is_unspecified
            ):
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Private or local network URLs "
                        "are not allowed."
                    )
                )

    except HTTPException:
        raise

    except (socket.gaierror, ValueError):
        raise HTTPException(
            status_code=400,
            detail="Unable to resolve the website address."
        )


# --------------------------------------------------
# ROOT ENDPOINT
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "Fake News Detection API is running",
        "version": "1.2.0"
    }


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "model_name": "LinearSVC",
        "fact_checking": "integrated"
    }


# --------------------------------------------------
# TEXT ANALYSIS
# --------------------------------------------------

@app.post("/predict")
def predict_news(request: PredictionRequest):

    return analyze_article(
        title=request.title,
        text=request.text,
        source="text"
    )


# --------------------------------------------------
# PDF ANALYSIS
# --------------------------------------------------

@app.post("/analyze-pdf")
async def analyze_pdf(file: UploadFile = File(...)):

    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF file."
        )

    file_bytes = await file.read(MAX_PDF_SIZE + 1)

    if len(file_bytes) > MAX_PDF_SIZE:
        raise HTTPException(
            status_code=413,
            detail="PDF file is too large. Maximum size is 10 MB."
        )

    if not file_bytes:
        raise HTTPException(
            status_code=400,
            detail="Uploaded PDF is empty."
        )

    try:

        pdf = PdfReader(BytesIO(file_bytes), strict=False)

        if pdf.is_encrypted:
            raise HTTPException(
                status_code=400,
                detail="Password-protected PDFs are not supported."
            )

        if len(pdf.pages) > MAX_PDF_PAGES:
            raise HTTPException(
                status_code=413,
                detail=(
                    f"PDF cannot contain more than "
                    f"{MAX_PDF_PAGES} pages."
                )
            )

        extracted_pages = []

        for page in pdf.pages:

            page_text = page.extract_text() or ""

            if page_text.strip():
                extracted_pages.append(page_text)

        extracted_text = "\n".join(extracted_pages).strip()

        if not extracted_text:
            raise HTTPException(
                status_code=422,
                detail=(
                    "No readable text found. This may be a scanned PDF. "
                    "OCR support is not implemented yet."
                )
            )

        title = Path(file.filename).stem

        # Fact-checking uses external network calls.
        # Run the synchronous analysis in a worker thread.
        result = await run_in_threadpool(
            analyze_article,
            title,
            extracted_text,
            "pdf"
        )

        result["filename"] = file.filename
        result["pages"] = len(pdf.pages)

        return result

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=f"Could not read PDF: {str(error)}"
        )

    finally:
        await file.close()


# --------------------------------------------------
# NEWS URL ANALYSIS
# --------------------------------------------------

@app.post("/analyze-url")
async def analyze_url(request: URLRequest):

    validate_public_url(request.url)

    try:

        async with httpx.AsyncClient(
            timeout=20.0,
            follow_redirects=True,
            max_redirects=5,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(compatible; NewsArticleAnalyzer/1.0)"
                )
            }
        ) as client:

            async with client.stream("GET", request.url) as response:

                response.raise_for_status()

                content_type = response.headers.get(
                    "content-type", ""
                ).lower()

                if "text/html" not in content_type:
                    raise HTTPException(
                        status_code=415,
                        detail=(
                            "The URL does not point to "
                            "an HTML webpage."
                        )
                    )

                chunks = []
                total_size = 0

                async for chunk in response.aiter_bytes():

                    total_size += len(chunk)

                    if total_size > MAX_URL_SIZE:
                        raise HTTPException(
                            status_code=413,
                            detail="Webpage is too large to process."
                        )

                    chunks.append(chunk)

                html_content = b"".join(chunks).decode(
                    response.encoding or "utf-8",
                    errors="replace"
                )

        extracted_text = trafilatura.extract(
            html_content,
            include_comments=False,
            include_tables=True,
            favor_precision=True
        )

        if not extracted_text:
            raise HTTPException(
                status_code=422,
                detail=(
                    "Could not extract the article text. "
                    "The website may block automated access or use "
                    "a format that is not supported."
                )
            )

        metadata = trafilatura.extract_metadata(html_content)

        title = (
            metadata.title
            if metadata and metadata.title
            else ""
        )

        result = await run_in_threadpool(
            analyze_article,
            title,
            extracted_text,
            "url"
        )

        result["url"] = request.url

        return result

    except HTTPException:
        raise

    except httpx.HTTPStatusError as error:
        raise HTTPException(
            status_code=502,
            detail=(
                f"Website returned HTTP status "
                f"{error.response.status_code}."
            )
        )

    except httpx.RequestError:
        raise HTTPException(
            status_code=502,
            detail="Unable to connect to the news website."
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"URL analysis failed: {str(error)}"
        )
