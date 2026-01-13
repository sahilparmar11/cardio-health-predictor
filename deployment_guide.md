# Deployment Guide

## 1. Deploying the Backend (FastAPI) to Render.com (Free)

1.  Push this repository to GitHub.
2.  Sign up/Log in to [Render.com](https://render.com).
3.  Click **New +** -> **Web Service**.
4.  Connect your GitHub repository.
5.  Settings:
    *   **Runtime**: Python 3
    *   **Build Command**: `pip install -r src/backend/requirements.txt`
    *   **Start Command**: `uvicorn src.backend.main:app --host 0.0.0.0 --port $PORT`
    *   **Root Directory**: `.` (or leave empty)
6.  Click **Create Web Service**.
7.  Copy the URL (e.g., `https://cardio-backend.onrender.com`).

## 2. Deploying the Frontend (Streamlit) to Streamlit Cloud (Free)

1.  Ensure `src/frontend/requirements.txt` exists.
2.  Sign up/Log in to [share.streamlit.io](https://share.streamlit.io).
3.  Click **New app**.
4.  Select your Repository, Branch, and Main file path (`src/frontend/app.py`).
5.  Click **Deploy**.
6.  **Important**: Update the API URL in `src/frontend/app.py`.
    *   Currently, it points to `http://localhost:8000`.
    *   You need to change it to your Render Backend URL (e.g., `https://cardio-backend.onrender.com/predict`).
    *   *Tip*: Use `st.secrets` in Streamlit to manage the URL without hardcoding.

## 3. Running Locally

**Backend:**
```bash
cd src/backend
uvicorn main:app --reload
```

**Frontend:**
```bash
cd src/frontend
streamlit run app.py
```
