
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI
from typing import Literal
from pydantic import BaseModel, Field

# Model location
BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR / "model.joblib"

FEATURES = [
    "tenure_months",
    "monthly_charges",
    "support_calls",
    "contract",
    "internet_service",
]

# Input validation
class Customer(BaseModel):
    tenure_months: int = Field(ge=0)
    monthly_charges: float = Field(ge=0)
    support_calls: int = Field(ge=0)
    contract: Literal["month-to-month", "one-year", "two-year"]
    internet_service: Literal["fiber", "dsl", "none"]


# Create FastAPI application
app = FastAPI(title="AI381 Lab 2 Churn Prediction API")

# Load trained model
model = joblib.load(MODEL_PATH)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(customer: Customer):
    customer_data = customer.model_dump()
    X = pd.DataFrame([customer_data])[FEATURES]

    probability = float(model.predict_proba(X)[0, 1])

    return {
        "churn_probability": round(probability, 3)
    }
