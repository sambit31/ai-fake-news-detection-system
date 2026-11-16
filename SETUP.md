# How to Install and Run the Project

A beginner-friendly guide to running the AI Fake News Detection System on your computer.

Don't worry if you are new to Python, React or FastAPI. Follow the steps one by one.

# 1. What Do You Need?

Before starting, install these three things:

### 1. Python

Python runs our backend and Machine Learning model.

Download: https://www.python.org/downloads/

### 2. Node.js

Node.js is needed to run our React frontend.

Download: https://nodejs.org/

### 3. VS Code

VS Code is where we open and work with the project.

Download: https://code.visualstudio.com/

After installing, open PowerShell or the VS Code terminal.

Check whether Python is installed:

```powershell
python --version
```

Check Node.js:

```powershell
node --version
```

Check npm:

```powershell
npm --version
```

If all three commands show version numbers, you are ready!

# 2. Open the Project

First, open your project folder in VS Code.

Your folder should look something like this:

```text
fake_news/
│
├── backend/
├── frontend/
├── README.md
└── SETUP.md
```

Open the terminal in VS Code:

**Terminal → New Terminal**

Make sure the terminal is inside the main `fake_news` folder.

For example:

```powershell
cd "C:\Users\techr\OneDrive\Desktop\FackNews\fake_news"
```

# 3. Start the Backend (Python)

Think of the backend as the brain of our project.

It receives news articles, runs the ML model and performs AI fact-checking.

We need to start this first.

### Step 3.1: Enter the backend folder

```powershell
cd backend
```

### Step 3.2: Create a virtual environment

A virtual environment is like a separate box where we install all the Python packages required by this project.

Run this command only the first time:

```powershell
python -m venv .venv
```

### Step 3.3: Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

After activation, your terminal should show something like:

```text
(.venv) PS C:\...\fake_news\backend>
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate again:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 3.4: Install Python packages

Now install all the required libraries.

```powershell
python -m pip install --upgrade pip
```

Then:

```powershell
pip install -r requirements.txt
```

Wait until the installation finishes.

This may take a few minutes.

# 4. Configure API Keys

Our project uses two external services for AI-powered fact-checking.

1. Groq – Extracts and verifies factual claims.
2. Tavily – Searches the internet for evidence.

You need API keys to use the complete fact-checking functionality.

### Step 4.1: Get your API keys

Groq:

https://console.groq.com/keys

Tavily:

https://app.tavily.com/

Create an account and generate your API keys.

### Step 4.2: Create the `.env` file

Inside the `backend` folder, create a new file named:

```text
.env
```

Your folder should look like:

```text
backend/
│
├── api/
├── ml/
├── requirements.txt
└── .env
```

Open `.env` and add:

```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

Replace the example values with your actual API keys.

**Important:**

- Never share your API keys publicly.
- Never upload your `.env` file to GitHub.
- Keep the `.env` file inside the backend folder.

# 5. Start the Backend Server

You should still be inside the `backend` folder.

Run:

```powershell
uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
```

If everything works, you should see something similar to:

```text
Uvicorn running on http://127.0.0.1:8000

Fake news detection model loaded successfully!
```

Congratulations! Your backend is running.

### Test the backend

Open your browser and visit:

http://127.0.0.1:8000

You should see a message saying:

```json
{
  "message": "Fake News Detection API is running",
  "version": "1.2.0"
}
```

You can also visit:

http://127.0.0.1:8000/docs

This opens the interactive API documentation.

**IMPORTANT:** Do not close this terminal. Your backend must keep running.

# 6. Start the Frontend (React)

Now we will start the frontend.

The frontend is the part of the project that users can see and interact with.

### Step 6.1: Open another terminal

In VS Code:

**Terminal → New Terminal**

Keep your backend terminal running.

Now you have two terminals:

```text
Terminal 1 = Backend (Python)
Terminal 2 = Frontend (React)
```

### Step 6.2: Enter the frontend folder

In your new terminal:

```powershell
cd "C:\Users\techr\OneDrive\Desktop\FackNews\fake_news\frontend"
```

### Step 6.3: Install frontend packages

Run:

```powershell
npm install
```

This downloads all the packages needed by React.

Wait until it finishes.

You only need to run `npm install` again if your dependencies change or you set up a fresh copy of the project.

### Step 6.4: Start React

Run:

```powershell
npm run dev
```

You should see something similar to:

```text
VITE ready

Local: http://localhost:5173/
```

# 7. Open the Project in Your Browser

Now open:

http://localhost:5173

Your application should appear!

You can now:

1. Paste a news article.
2. Upload a PDF.
3. Enter a news article URL.
4. Click the analyze button.
5. Wait for the ML classification and fact-checking results.

# 8. Understand How to Run the Project Next Time

This is important.

After the first installation, you do not need to install everything again.

Whenever you want to use the project, follow these steps:

### Terminal 1 – Backend

```powershell
cd "C:\Users\techr\OneDrive\Desktop\FackNews\fake_news\backend"
```

Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Start the backend:

```powershell
uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
```

### Terminal 2 – Frontend

Open another terminal:

```powershell
cd "C:\Users\techr\OneDrive\Desktop\FackNews\fake_news\frontend"
```

Start React:

```powershell
npm run dev
```

Open:

http://localhost:5173

That's it!

# 9. How Does the Project Work?

Imagine that you give the application a newspaper article.

Here is what happens:

```text
       YOU
        |
        v
   Submit News
        |
        v
   REACT FRONTEND
        |
        v
   PYTHON BACKEND
        |
        v
    ML MODEL
        |
        v
   FAKE or REAL
        |
        v
   AI FACT-CHECKING
        |
        v
   Extract Claims
        |
        v
   Search Internet
        |
        v
   Collect Evidence
        |
        v
   Verify Each Claim
        |
        v
   Final Result
        |
        v
   DISPLAY ON WEBSITE
```

The Machine Learning model checks patterns in the news article.

The AI fact-checker searches for external evidence and evaluates individual factual claims.

Both results are shown on the website.

# 10. Common Problems and Solutions

### Problem 1: Python is not recognized

Check Python installation:

```powershell
python --version
```

If this fails, install Python and ensure it is added to PATH.

### Problem 2: Virtual environment is not activating

Run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Problem 3: ModuleNotFoundError

This usually means a required Python package is missing.

Make sure the virtual environment is activated and run:

```powershell
pip install -r requirements.txt
```

### Problem 4: Model not found

Check whether this file exists:

```text
backend/ml/artifacts/fake_news_pipeline.joblib
```

The application needs this trained model to start.

You do not need to train the model again if this file is already present.

### Problem 5: Frontend cannot connect to backend

Check that:

- Backend is running on port 8000.
- Frontend is running on port 5173.
- The backend terminal has no errors.
- You are using the correct API address.

The frontend currently uses:

```javascript
const API_BASE = "http://127.0.0.1:8000";
```

### Problem 6: Fact-checking is unavailable

Check that:

- `backend/.env` exists.
- `GROQ_API_KEY` is correct.
- `TAVILY_API_KEY` is correct.
- Your internet connection is working.
- Your API accounts have available usage.

The ML prediction can still work even when fact-checking is unavailable.

### Problem 7: PDF text is not extracted

The current PDF implementation supports PDFs containing selectable text.

Scanned image-based PDFs require OCR, which is not implemented yet.

# 11. Optional: Train the ML Model Again

You do not need to train the model every time you run the project.

However, if you want to train it again, make sure you have the cleaned dataset:

```text
backend/data/processed/cleaned_dataset.csv
```

From the backend folder, run:

```powershell
python ml/training/train_model.py
```

This trains and compares the models and saves the selected trained pipeline in:

```text
backend/ml/artifacts/
```

Training can take some time depending on your computer.

# 12. Final Checklist

Before running the application, make sure:

- [ ] Python is installed.
- [ ] Node.js is installed.
- [ ] Python virtual environment is activated.
- [ ] Python packages are installed.
- [ ] Backend `.env` contains the API keys.
- [ ] Trained ML model exists.
- [ ] Backend is running on port 8000.
- [ ] Frontend packages are installed.
- [ ] Frontend is running on port 5173.

**You are ready to use the AI Fake News Detection System!**