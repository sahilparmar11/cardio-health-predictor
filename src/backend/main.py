from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd
import numpy as np
from pydantic import BaseModel
import os

app = FastAPI(title="Cardio Prediction API")

# Allow CORS for specific origins (or all for dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models
# Paths relative to src/backend/
MODEL_PATH = "../../notebooks/best_logistic_model.pkl"
SCALER_PATH = "../../notebooks/scaler.pkl"

model = None
scaler = None

# Lazy loading or on startup
try:
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print("Model loaded successfully.")
    else:
        print(f"Warning: Model not found at {MODEL_PATH}")

    if os.path.exists(SCALER_PATH):
        scaler = joblib.load(SCALER_PATH)
        print("Scaler loaded successfully.")
    else:
        print(f"Warning: Scaler not found at {SCALER_PATH}")
except Exception as e:
    print(f"Error loading models: {e}")

class PredictionInput(BaseModel):
    gender: int
    height: float
    weight: float
    ap_hi: float
    ap_lo: float
    cholesterol: int
    gluc: int
    smoke: int
    alco: int
    active: int
    age_years: float

@app.get("/")
def read_root():
    return {"message": "Cardio Prediction API is running. Use /predict endpoint."}

@app.post("/predict")
def predict(input_data: PredictionInput):
    global model, scaler
    if model is None or scaler is None:
        raise HTTPException(status_code=503, detail="Model or Scaler not loaded.")
    
    try:
        # Preprocessing Logic reverse-engineered from training data
        # ap_lo was MinMaxScaled with approx min=65, max=105 in the training set
        # We must apply the same transformation to raw input
        # Formula: (x - 65) / 40
        ap_lo_transformed = (input_data.ap_lo - 65) / 40
        
        # Prepare input vector (11 features)
        features = [
            input_data.gender,
            input_data.height,
            input_data.weight,
            input_data.ap_hi,
            ap_lo_transformed, # Use transformed value
            input_data.cholesterol,
            input_data.gluc,
            input_data.smoke,
            input_data.alco,
            input_data.active,
            input_data.age_years
        ]
        
        # Convert to 2D array
        features_array = np.array(features).reshape(1, -1)
        
        # Scale features
        # Scaler expects 11 features
        if scaler.n_features_in_ == 11:
            scaled_features = scaler.transform(features_array)
        else:
             # Fallback if scaler matches model?
             scaled_features = features_array
        
        # Handle Model dimension mismatch
        final_input = scaled_features
        if model.n_features_in_ == 12 and final_input.shape[1] == 11:
            # Prepend dummy id (0)
            dummy_id = np.array([[0.0]])
            final_input = np.hstack((dummy_id, scaled_features))
        
        # Predict
        prediction = model.predict(final_input)
        probability = model.predict_proba(final_input).tolist()
        
        result_class = int(prediction[0])
        result_label = "Positive (Risk)" if result_class == 1 else "Negative (No Risk)"
        
        return {
            "prediction": result_class,
            "prediction_label": result_label,
            "probability": probability[0],
            "input_received": input_data.dict(),
            "debug_ap_lo_transformed": ap_lo_transformed
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
