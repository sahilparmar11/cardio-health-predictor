# Cardiovascular Disease Prediction UI

This project provides a web-based UI for predicting cardiovascular disease based on user inputs using a trained machine learning model.

## Project Structure

- `backend/`: Flask API for model predictions
- `cardio-ui/`: React frontend
- `data/`: Dataset files
- `notebooks/`: Jupyter notebooks for model training and evaluation

## Setup

### Backend

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the Flask app:
   ```
   python app.py
   ```
   The API will be available at http://localhost:5000

### Frontend

1. Navigate to the cardio-ui directory:
   ```
   cd cardio-ui
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the React app:
   ```
   npm start
   ```
   The UI will be available at http://localhost:3000

## Usage

1. Start both the backend and frontend servers.
2. Open the React app in your browser.
3. Fill in the form with the required health metrics.
4. Click "Predict" to get the cardiovascular disease prediction.

## Features

- User-friendly form with dropdowns and inputs
- Real-time prediction from the ML model
- Displays prediction result and probability
- CORS enabled for seamless frontend-backend communication

## Model Details

The model is a Logistic Regression classifier trained on cardiovascular disease data. It takes 11 features as input and predicts whether the person has cardiovascular disease or not.