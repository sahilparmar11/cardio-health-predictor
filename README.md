# ❤️ Cardiovascular Health Predictor

A modern, web-based application utilizing Machine Learning to predict cardiovascular disease risk. Built with a powerful **FastAPI** backend and a stylish **Streamlit** frontend.

## ✨ Features

*   **Multi-Page Interface**:
    *   **📊 Dashboard**: Interactive insights into the training dataset using Plotly charts.
    *   **🩺 Assessment**: Real-time CVD risk prediction form for users.
    *   **📈 Analytics**: Deep dive into model performance (Confusion Matrix, Feature Importance, Accuracy).
*   **Modern UI/UX**:
    *   Fully responsive design with a "Glassmorphism" aesthetic.
    *   **Dark/Light Mode** toggle with custom high-contrast medical themes.
    *   Interactive charts and dynamic metric cards.
*   **Machine Learning**:
    *   Powered by a **Logistic Regression** model (approx. 73% accuracy).
    *   Data preprocessing and scaling pipelines included.

## 🛠️ Tech Stack

*   **Frontend**: Streamlit, Plotly, Streamlit-Option-Menu
*   **Backend**: FastAPI, Uvicorn
*   **ML Engine**: Scikit-Learn, Pandas, NumPy, Joblib
*   **Visualization**: Plotly Express, Seaborn. Matplotlib

## 🚀 Quick Start

### Prerequisites
*   Python 3.9+
*   Git

### 1. Clone the Repository
```bash
git clone https://github.com/sahilparmar11/cardio-health-predictor.git
cd cardio-health-predictor
```

### 2. Set Up Environment
It is recommended to use a virtual environment.
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
You can run the Streamlit frontend directly (for Dashboard/Analytics features):
```bash
streamlit run src/frontend/app.py
```

*To enable the prediction API, you must also run the backend:*
```bash
uvicorn src.backend.main:app --reload
```

## 📂 Project Structure

```
├── data/                   # Dataset (csv)
├── notebooks/              # Jupyter Notebooks for training & analysis
├── src/
│   ├── backend/            # FastAPI Application
│   └── frontend/           # Streamlit Web Interface
│       ├── app.py          # Main Application Entry
│       └── styles.py       # Custom CSS Styling
├── requirements.txt        # Project Dependencies
└── README.md               # Documentation
```

## ☁️ Deployment

*   **Frontend**: Deployed on [Streamlit Community Cloud](https://streamlit.io/cloud).
*   **Backend**: Ready for deployment on [Render](https://render.com) or [Railway](https://railway.app).

## 📄 License
This project is open-source and available under the MIT License.