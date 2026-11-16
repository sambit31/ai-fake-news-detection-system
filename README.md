# AI Fake News Detection & Verification System

An AI-powered web application that helps users analyze news articles and identify potentially misleading information using Machine Learning and evidence-based AI fact-checking.

## 1. Project Overview

Fake news spreads quickly through social media, websites and digital newspapers. It can be difficult for ordinary people to identify whether an article is trustworthy.

Manually checking every news article takes time and effort.

This project provides a system where users can submit news articles in three different ways:

- Paste news article text.
- Upload a newspaper or news article PDF.
- Enter a news article URL.

The system first uses a trained Machine Learning model to classify the article as **FAKE** or **REAL**. It then uses AI-powered fact-checking to extract factual claims, search for external evidence and evaluate those claims.

The goal is to combine traditional Machine Learning with evidence-based AI verification.

## 2. Main Objectives

1. Detect potentially fake news using Machine Learning.
2. Support multiple news input formats.
3. Extract readable text from PDF documents and news websites.
4. Identify factual claims from news articles.
5. Search external sources for supporting evidence.
6. Verify claims using actual webpage content.
7. Display understandable results to users.

## 3. Features

### A. Multiple Input Methods

| Input | Description |
|---|---|
| Article Text | Paste news content directly |
| PDF Upload | Upload a PDF and extract its text |
| News URL | Extract article text from a webpage |

### B. Machine Learning Classification

The trained ML model classifies news articles into:

- **FAKE** – The model identifies patterns associated with fake news.
- **REAL** – The model identifies patterns associated with real news.

The model also returns a decision score and an explanation.

### C. AI-Powered Fact-Checking

The system extracts factual claims from an article and checks them against external sources.

Each claim receives one of three verdicts:

- SUPPORTED
- CONTRADICTED
- INSUFFICIENT EVIDENCE

The application also displays evidence sources and explanations for individual claims.

### D. Combined Analysis

The final response contains both:

1. Machine Learning classification.
2. Evidence-based claim verification.

If fact-checking fails, the ML classification can still be returned.

## 4. Technology Stack

| Component | Technology |
|---|---|
| Frontend | React.js |
| Styling | Tailwind CSS |
| Build Tool | Vite |
| Backend | Python, FastAPI |
| Machine Learning | Scikit-learn |
| NLP | TF-IDF |
| ML Classifier | LinearSVC |
| Data Processing | Pandas, NumPy |
| Model Storage | Joblib |
| AI Claim Extraction | Groq API |
| Evidence Search | Tavily API |
| PDF Processing | PyPDF |
| URL Extraction | HTTPX, Trafilatura |

## 5. System Architecture

The application follows a frontend-backend architecture.

```text
                 USER
                   |
                   v
          REACT FRONTEND
                   |
          Select Input Method
                   |
       +-----------+-----------+
       |           |           |
       v           v           v
    TEXT         PDF          URL
       |           |           |
       |           v           v
       |       PDF Text    Web Article
       |       Extraction  Extraction
       |           |           |
       +-----------+-----------+
                   |
                   v
             FASTAPI BACKEND
                   |
                   v
          TEXT + TITLE INPUT
                   |
                   v
          TEXT PREPROCESSING
                   |
                   v
          TRAINED ML PIPELINE
              (LinearSVC)
                   |
                   v
           ML CLASSIFICATION
              FAKE / REAL
                   |
                   v
           AI FACT-CHECKING
                   |
                   v
           GROQ API
          Claim Extraction
                   |
                   v
             TAVILY API
            Evidence Search
                   |
                   v
          FETCH WEBPAGE CONTENT
                   |
                   v
            GROQ API
          Evidence Verification
                   |
                   v
          FINAL ANALYSIS RESULT
                   |
                   v
            REACT FRONTEND
                   |
                   v
             DISPLAY RESULT
```

## 6. Machine Learning Architecture

The Machine Learning component uses a TF-IDF-based text classification pipeline.

### Dataset

The project uses labeled news articles containing:

- Title
- Article text
- Label

Label mapping:

| Label | Meaning |
|---|---|
| 0 | Fake News |
| 1 | Real News |

### ML Training Process

```text
Raw News Dataset
       |
       v
Dataset Cleaning
       |
       v
Text Preparation
       |
       v
Combine Title + Article
       |
       v
Train-Test Split (80:20)
       |
       v
TF-IDF Feature Extraction
       |
       +---------------------+
       |                     |
       v                     v
   Word TF-IDF          Character TF-IDF
       |                     |
       +----------+----------+
                  |
                  v
          Feature Combination
                  |
                  v
          Model Comparison
                  |
       +----------+----------+
       |          |          |
       v          v          v
   Logistic    Naive       Linear
  Regression   Bayes        SVM
       |          |          |
       +----------+----------+
                  |
                  v
           Best Model Selection
                  |
                  v
          Save Trained Pipeline
                  |
                  v
          fake_news_pipeline.joblib
```

### Feature Extraction

The system uses two types of TF-IDF features:

- Word TF-IDF: Identifies important words and word combinations.
- Character TF-IDF: Identifies character-level patterns.

Both feature sets are combined using Scikit-learn's FeatureUnion.

### Model Training

Three classifiers are compared:

1. Logistic Regression
2. Multinomial Naive Bayes
3. Linear Support Vector Machine (LinearSVC)

The best-performing model is selected using evaluation metrics, including accuracy, precision, recall and F1-score.

The final trained pipeline is saved using Joblib.

**Important:** The running application loads the already-trained model. Retraining is not required every time the application starts.

## 7. AI Fact-Checking Architecture

The fact-checking component works separately from the ML classification stage.

### Step-by-Step Workflow

**Step 1: Claim Extraction**

Groq AI reads the article and extracts factual claims.

**Step 2: Evidence Search**

Tavily searches the internet for webpages related to each claim.

**Step 3: Webpage Extraction**

HTTPX downloads webpages, and Trafilatura extracts readable content.

**Step 4: Evidence Verification**

Groq AI evaluates the extracted webpage content against the original claim.

**Step 5: Verdict Generation**

Each claim receives one of these results:

- SUPPORTED
- CONTRADICTED
- INSUFFICIENT_EVIDENCE

**Step 6: Final Summary**

The backend calculates the number of supported, contradicted and insufficiently supported claims and sends the result to the frontend.

## 8. API Endpoints

Base URL: `http://127.0.0.1:8000`

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Check whether the API is running |
| GET | `/health` | Check API and model status |
| POST | `/predict` | Analyze news text |
| POST | `/analyze-pdf` | Analyze uploaded PDF |
| POST | `/analyze-url` | Analyze news URL |

Interactive API documentation:

`http://127.0.0.1:8000/docs`

## 9. Project Structure

```text
fake_news/
│
├── backend/
│   │
│   ├── api/
│   │   ├── main.py
│   │   ├── article_fact_check.py
│   │   ├── ai_fact_checker.py
│   │   ├── evidence_search.py
│   │   ├── evidence_fetch.py
│   │   └── evidence_verifier.py
│   │
│   ├── ml/
│   │   ├── artifacts/
│   │   │   └── fake_news_pipeline.joblib
│   │   │
│   │   ├── data/
│   │   ├── evaluation/
│   │   ├── training/
│   │   │   └── train_model.py
│   │   │
│   │   └── text_preprocessing.py
│   │
│   ├── data/
│   │   ├── Fake.csv/
│   │   ├── True.csv/
│   │   └── processed/
│   │       └── cleaned_dataset.csv
│   │
│   ├── tests/
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── package.json
│   └── vite.config.js
│
├── README.md
└── SETUP.md
```

## 10. Limitations

- ML predictions are based on patterns learned from the training dataset. They do not independently establish whether a news article is factually true.
- The ML decision score is not a probability or guaranteed confidence percentage.
- AI-generated verification may be incorrect or incomplete.
- External evidence availability depends on search results and accessible webpages.
- Scanned PDFs that contain images instead of selectable text are not supported because OCR is not implemented.
- PDF analysis currently extracts the document text and analyzes it as one document; automatic separation of individual newspaper articles is not implemented.
- Some news websites may block automated extraction.

**This project is designed as a decision-support tool, not a replacement for professional fact-checking.**

## 11. Future Improvements

- OCR support for scanned newspaper PDFs.
- Automatic newspaper article segmentation.
- More datasets and multilingual support.
- Improved model generalization.
- User accounts and analysis history.
- Source reliability analysis.
- Better explainability of ML predictions.

## 12. Installation and Execution

For complete installation instructions, see:

**[SETUP.md](./SETUP.md)**

## 13. Author

**Sambit Ghosh**

GitHub: [@sambit31](https://github.com/sambit31)

Project Repository: [AI Fake News Detection System](https://github.com/sambit31/ai-fake-news-detection-system)

---

*Academic Major Project – AI and Machine Learning Based Fake News Detection and Verification System.*