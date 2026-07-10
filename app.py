from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np
import pandas as pd

# Initialize FastAPI engine
app = FastAPI(title="IoT-Sentinel: Industrial Predictive Maintenance API")

# Load your trained XGBoost model from Google Colab
with open("predictive_maintenance_model.pkl", "rb") as file:
    model = pickle.load(file)

# Define the exact data structure expected from the factory sensors
class SensorPayload(BaseModel):
    vibration: float
    acoustic: float
    temperature: float
    current: float
    IMF_1: float
    IMF_2: float
    IMF_3: float

@app.post("/predict")
def predict_machine_status(data: SensorPayload):
    # Map the incoming JSON payload to match training feature names exactly
    feature_names = ['vibration', 'acoustic', 'temperature', 'current', 'IMF_1', 'IMF_2', 'IMF_3']
    input_data = pd.DataFrame([[
        data.vibration, data.acoustic, data.temperature, 
        data.current, data.IMF_1, data.IMF_2, data.IMF_3
    ]], columns=feature_names)
    
    # Run inference calculations
    prediction = int(model.predict(input_data)[0])
    probability = float(model.predict_proba(input_data)[0, 1])
    
    # Map the numerical class binary back to operational strings
    status = "Critical Failure Risk - Action Required" if prediction == 1 else "Normal Operations"
    
    return {
        "prediction_class": prediction,
        "operational_status": status,
        "failure_probability_percentage": round(probability * 100, 2)
    }
