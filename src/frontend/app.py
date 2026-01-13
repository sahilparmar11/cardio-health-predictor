import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import joblib
import numpy as np
import os
from styles import load_css

# --- Config ---
st.set_page_config(
    page_title="Cardio Health AI",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Global CSS
st.markdown(load_css(), unsafe_allow_html=True)

# --- Helper Functions ---
@st.cache_data
def load_data_resources():
    DATA_PATH = "../../data/cardio_preprocessed.csv"
    MODEL_PATH = "../../notebooks/best_logistic_model.pkl"
    SCALER_PATH = "../../notebooks/scaler.pkl"
    
    if not os.path.exists(DATA_PATH):
        return None, None, None, f"Data file not found at {DATA_PATH}"
        
    try:
        df = pd.read_csv(DATA_PATH)
        # Assuming resources are needed for analytics, return generic objects or None if not strictly needed for dashboard overview
        # But we load them for Analytics page
        return df, MODEL_PATH, SCALER_PATH, None
    except Exception as e:
        return None, None, None, str(e)

import plotly.express as px

# --- Page: Dashboard ---
def render_dashboard():
    # Hero Section
    st.markdown("""
        <div class="hero-box">
            <div class="hero-title">📊 Health Dashboard</div>
            <div class="hero-subtitle">Explore cardiovascular health trends & population statistics</div>
        </div>
    """, unsafe_allow_html=True)
    
    df, _, _, err = load_data_resources()
    
    if err or df is None:
        st.warning("⚠️ Could not load dataset. Dashboard features limited.")
        return

    # Real Data Insights
    total_patients = len(df)
    avg_age = round(df['age_years'].mean(), 1)
    risk_percent = round((df['cardio'].sum() / total_patients) * 100, 1)
    avg_weight = round(df['weight'].mean(), 1)
    
    # --- Custom Stat Cards Row ---
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; gap: 20px; margin-bottom: 40px;">
        <div class="stat-card" style="flex: 1;">
            <div class="stat-icon">👥</div>
            <div class="stat-value">{total_patients:,}</div>
            <div class="stat-label">Total Patients</div>
        </div>
        <div class="stat-card" style="flex: 1;">
            <div class="stat-icon">🎂</div>
            <div class="stat-value">{avg_age}</div>
            <div class="stat-label">Avg. Age (Yrs)</div>
        </div>
        <div class="stat-card" style="flex: 1;">
            <div class="stat-icon">❤️</div>
            <div class="stat-value">{risk_percent}%</div>
            <div class="stat-label">At Risk</div>
        </div>
        <div class="stat-card" style="flex: 1;">
            <div class="stat-icon">⚖️</div>
            <div class="stat-value">{avg_weight}</div>
            <div class="stat-label">Avg. Weight (kg)</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # --- Charts Section ---
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("### 📉 Age vs Risk Distribution")
        # Prepare Data for Plotly
        df['age_bin'] = pd.cut(df['age_years'], bins=[30, 40, 50, 60, 70], labels=['30-40', '40-50', '50-60', '60+'])
        risk_data = df.groupby('age_bin')['cardio'].mean().reset_index()
        risk_data['cardio'] = risk_data['cardio'] * 100
        
        fig = px.bar(risk_data, x='age_bin', y='cardio', 
                     color='cardio', 
                     color_continuous_scale="Viridis",
                     labels={'cardio': 'Risk (%)', 'age_bin': 'Age Group'},
                     template="plotly_white")
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown("### 🚬 Lifestyle Impact Analysis")
        # Smoking vs Risk
        smoke_risk = df.groupby('smoke')['cardio'].mean().reset_index()
        smoke_risk['Type'] = 'Smoker'
        smoke_risk['Status'] = smoke_risk['smoke'].apply(lambda x: 'Yes' if x==1 else 'No')
        
        alco_risk = df.groupby('alco')['cardio'].mean().reset_index()
        alco_risk['Type'] = 'Alcohol'
        alco_risk['Status'] = alco_risk['alco'].apply(lambda x: 'Yes' if x==1 else 'No')
        
        # Combine
        combined_df = pd.concat([smoke_risk[['Type', 'Status', 'cardio']], alco_risk[['Type', 'Status', 'cardio']]])
        combined_df['cardio'] = combined_df['cardio'] * 100
        
        fig2 = px.bar(combined_df, x='Type', y='cardio', color='Status', barmode='group',
                      color_discrete_map={'Yes': '#EF553B', 'No': '#00CC96'},
                      labels={'cardio': 'Risk Probability (%)'},
                      template="plotly_white")
        fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig2, use_container_width=True)

# --- Page: Assessment ---
def render_assessment():
    st.markdown('<div class="main-header assessment-header">🩺 Risk Assessment</div>', unsafe_allow_html=True)
    st.markdown("Enter patient vitals below to generate a real-time risk prediction.")

    col_input, col_result = st.columns([1, 1], gap="large")

    with col_input:
        with st.container(border=True):
            st.markdown("#### Patient Vitals Form")
            with st.form("assessment_form", border=False):
                c1, c2 = st.columns(2)
                with c1:
                    gender = st.selectbox("Gender", options=[1, 2], format_func=lambda x: "Female" if x==1 else "Male")
                    height = st.number_input("Height (cm)", 55, 250, 165)
                    ap_hi = st.number_input("Systolic BP", 50, 300, 120)
                    cholesterol = st.selectbox("Cholesterol", options=[1, 2, 3], format_func=lambda x: ["Normal", "Above Normal", "High"][x-1])
                with c2:
                    age_years = st.number_input("Age (Years)", 10.0, 100.0, 50.0)
                    weight = st.number_input("Weight (kg)", 10.0, 200.0, 65.0)
                    ap_lo = st.number_input("Diastolic BP", 30, 200, 80)
                    gluc = st.selectbox("Glucose", options=[1, 2, 3], format_func=lambda x: ["Normal", "Above Normal", "High"][x-1])

                st.markdown("---")
                st.markdown("**Lifestyle Factors**")
                l1, l2, l3 = st.columns(3)
                with l1: smoke = st.selectbox("Smoker?", [0, 1], format_func=lambda x: "No" if x==0 else "Yes")
                with l2: alco = st.selectbox("Alcohol?", [0, 1], format_func=lambda x: "No" if x==0 else "Yes")
                with l3: active = st.selectbox("Active?", [0, 1], format_func=lambda x: "No" if x==0 else "Yes")

                st.markdown("")
                # Add custom class for styling primary button if we could inject specific CSS for this button ID
                submitted = st.form_submit_button("Run Analysis", use_container_width=True)

    with col_result:
        # Placeholder or Result
        if submitted:
             data = {
                "gender": gender, "height": height, "weight": weight, "ap_hi": ap_hi, "ap_lo": ap_lo,
                "cholesterol": cholesterol, "gluc": gluc, "smoke": smoke, "alco": alco, "active": active,
                "age_years": age_years
            }
             
             with st.spinner("Analyzing Vitals..."):
                try:
                    # Get Backend URL from env or default to localhost
                    # Ensure no trailing slash issues if user sets env var
                    base_url = os.getenv("BACKEND_URL", "http://localhost:8000")
                    api_url = f"{base_url.rstrip('/')}/predict"
                    
                    response = requests.post(api_url, json=data)
                    if response.status_code == 200:
                        res = response.json()
                        prob = res['probability'][1] * 100
                        
                        # Result Card
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, {'#ff9a9e' if res['prediction']==1 else '#a18cd1'}, {'#fecfef' if res['prediction']==1 else '#fbc2eb'}); padding: 20px; border-radius: 15px; text-align: center; color: white; margin-bottom: 20px;">
                            <h2 style="margin:0;">Risk Probability</h2>
                            <h1 style="font-size: 4em; margin:0;">{prob:.1f}%</h1>
                            <h3 style="margin:0;">{'High Risk Warning' if res['prediction']==1 else 'Low Risk Profile'}</h3>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.progress(int(prob))
                        
                        if res['prediction'] == 1:
                            st.warning("Recommendation: Consult a cardiologist for a thorough check-up.")
                        else:
                            st.success("Recommendation: Maintain healthy habits and regular check-ups.")
                            
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Backend connection failed. {e}")

        else:
            # Empty State
            st.info("👈 Fill out the form to see results here.")
            st.image("https://img.freepik.com/free-vector/medical-healthcare-blue-background-with-cardiograph_1017-26838.jpg?w=1380", use_container_width=True, caption="AI-Powered Cardiology")


# --- Page: Analytics ---
def render_analytics():
    st.markdown('<div class="main-header analytics-header">📈 Model Analytics</div>', unsafe_allow_html=True)
    st.markdown("Technical performance metrics of the Logistic Regression model.")
    
    df, model_path, scaler_path, err = load_data_resources()
    
    if err:
        st.error(f"Cannot load resources: {err}")
        return

    # Load artifacts on demand
    try:
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
    except:
        st.error("Model artifacts missing.")
        return

    # Tab layout
    t1, t2, t3 = st.tabs(["Performance Metrics", "Confusion Matrix", "Feature Importance"])

    # Prepare Data (Cached logic would be better but keeping simple for now)
    X = df.drop(columns=['cardio'])
    y = df['cardio']
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Scaling & Align helper (Condensed)
    def prep(X_in):
        X_s = scaler.transform(X_in if X_in.shape[1] == 11 else X_in.iloc[:, 1:])
        return np.hstack((np.zeros((X_s.shape[0], 1)), X_s)) if model.n_features_in_ == 12 and X_s.shape[1] == 11 else X_s

    y_pred = model.predict(prep(X_test))
    acc = accuracy_score(y_test, y_pred)
    
    with t1:
        c1, c2 = st.columns(2)
        c1.metric("Model Accuracy", f"{acc:.4f}", "Test Set")
        c2.metric("Training Size", f"{len(X_train):,}", "80% Split")
        
        st.text("Classification Report:")
        st.dataframe(pd.DataFrame(classification_report(y_test, y_pred, output_dict=True)).T.style.format("{:.3f}"))

    with t2:
        cm = confusion_matrix(y_test, y_pred)
        fig, ax = plt.subplots()
        sns.heatmap(cm, annot=True, fmt='d', cmap='magma', ax=ax) # unique color for analytics
        st.pyplot(fig)
        
    with t3:
        corr = df.corr()
        fig2, ax2 = plt.subplots(figsize=(10,8))
        sns.heatmap(corr, cmap='RdBu_r', center=0, ax=ax2)
        st.pyplot(fig2)

from streamlit_option_menu import option_menu

# --- Main App Logic ---
def main():
    # Helper: Toggle Theme
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'

    def toggle_theme():
        if st.session_state.theme == 'light':
            st.session_state.theme = 'dark'
        else:
            st.session_state.theme = 'light'

    # --- Top Layout: Nav (Left/Center) + Toggle (Right) ---
    col_nav, col_toggle = st.columns([5, 1])

    with col_nav:
        selected = option_menu(
            menu_title=None,
            options=["Dashboard", "Assessment", "Analytics"],
            icons=["bar-chart-fill", "activity", "graph-up-arrow"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#2E7D32", "font-size": "20px"},
                "nav-link": {
                    "font-size": "18px",
                    "text-align": "center",
                    "margin": "0px",
                    "--hover-color": "#E8F5E9",
                    "color": "#1B5E20"
                },
                "nav-link-selected": {"background-color": "#2E7D32", "color": "white !important"},
            }
        )

    with col_toggle:
        # Toggle Button
        btn_txt = "🌙 Dark" if st.session_state.theme == 'light' else "☀️ Light"
        if st.button(btn_txt):
            toggle_theme()
            st.rerun()

    # --- Theme Injection (Dark Mode Override) ---
    if st.session_state.theme == 'dark':
        st.markdown("""
        <style>
            /* Dark Mode Clean High-Contrast Overrides */
            .stApp {
                background-color: #0E1117 !important;
                color: #FFFFFF !important;
            }
            
            /* Containers & Cards */
            [data-testid="stForm"], [data-testid="stVerticalBlockBorderWrapper"], .stCard, .css-1r6slb0, [data-testid="stMetric"], .hero-box {
                background-color: #161B22 !important;
                border: 1px solid #30363D !important;
                box-shadow: 0 4px 6px rgba(0,0,0,0.3) !important;
                color: #FFFFFF !important;
            }
            
            /* Inputs */
            .stTextInput input, .stNumberInput input, .stSelectbox > div > div {
                background-color: #010409 !important;
                color: #FFFFFF !important;
                border: 1px solid #30363D !important;
            }
            .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox > div > div:focus {
                border-color: #2EA043 !important; /* Bright Green Focus */
            }
            
            /* Text Visibility */
            h1, h2, h3, h4, h5, h6, .hero-title, .hero-subtitle, label, p, div, span {
                color: #F0F6FC !important; /* Off-White for softness */
            }
            
            /* Specific Metric Labels usually act up in dark mode */
            [data-testid="stMetricLabel"] {
                color: #8B949E !important; /* Muted gray for label */
            }
            [data-testid="stMetricValue"] {
                color: #3FB950 !important; /* Bright Green value */
            }
            
            /* Hero Section Gradient Adjustment for Dark Mode */
            .hero-box {
                background: linear-gradient(135deg, #164E24 0%, #297C3B 100%) !important;
                border: none !important;
            }
            
            /* Navigation Bar in Dark Mode */
            .nav-link {
                color: #C9D1D9 !important;
            }
            .nav-link-selected {
                background-color: #238636 !important;
                color: white !important;
            }
        </style>
        """, unsafe_allow_html=True)

    # Route Page
    if selected == "Dashboard":
        render_dashboard()
    elif selected == "Assessment":
        render_assessment()
    elif selected == "Analytics":
        render_analytics()

if __name__ == "__main__":
    main()
