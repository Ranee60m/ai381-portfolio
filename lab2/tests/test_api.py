import joblib
from fastapi.testclient import TestClient
from src.app.main import app, MODEL_PATH

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}



def test_model_loads():
    model = joblib.load(MODEL_PATH)

    assert model is not None
    assert hasattr(model, "predict_proba")

def test_invalid_input():
    customer = {
        "tenure_months": -5,
        "monthly_charges": 89.9,
        "support_calls": 3,
        "contract": "month-to-month",
        "internet_service": "fiber"
    }

    response = client.post("/predict", json=customer)

    assert response.status_code == 422
def test_valid_prediction():
    customer = {
        "tenure_months": 12,
        "monthly_charges": 89.9,
        "support_calls": 3,
        "contract": "month-to-month",
        "internet_service": "fiber"
    }

    response = client.post("/predict", json=customer)

    assert response.status_code == 200
    assert "churn_probability" in response.json()
def test_probability_range():
    customer = {
        "tenure_months": 12,
        "monthly_charges": 89.9,
        "support_calls": 3,
        "contract": "month-to-month",
        "internet_service": "fiber"
    }

    response = client.post("/predict", json=customer)

    assert response.status_code == 200

    probability = response.json()["churn_probability"]

    assert 0 <= probability <= 1

def test_deterministic_prediction():
    customer = {
        "tenure_months": 12,
        "monthly_charges": 89.9,
        "support_calls": 3,
        "contract": "month-to-month",
        "internet_service": "fiber"
    }

    first_response = client.post("/predict", json=customer)
    second_response = client.post("/predict", json=customer)

    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert first_response.json() == second_response.json()
