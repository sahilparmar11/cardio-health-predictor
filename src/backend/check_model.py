import joblib
import pandas as pd
import os

model_path = r"../../notebooks/best_logistic_model.pkl"
scaler_path = r"../../notebooks/scaler.pkl"

try:
    model = joblib.load(model_path)
    print(f"Model loaded. n_features_in_: {model.n_features_in_}")
    if hasattr(model, 'feature_names_in_'):
        print(f"Feature names: {model.feature_names_in_}")
    else:
        print("Model does not have feature_names_in_ attribute.")
        
    scaler = joblib.load(scaler_path)
    print(f"Scaler loaded. n_features_in_: {scaler.n_features_in_}")
except Exception as e:
    print(f"Error: {e}")
