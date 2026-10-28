
# AI381 Portfolio — Lab 2: Container & CI

[![Lab 2 CI](https://github.com/Ranee60m/ai381-portfolio/actions/workflows/lab2-ci.yml/badge.svg?branch=main)](https://github.com/Ranee60m/ai381-portfolio/actions/workflows/lab2-ci.yml)

## Project Overview

This project implements a Customer Churn Prediction API using Python, scikit-learn, and FastAPI.

The model is packaged as a Docker container and automatically tested, scanned, and published through GitHub Actions.

## Technologies

- Python 3.13
- FastAPI and Pydantic
- scikit-learn
- pytest and Ruff
- Docker
- GitHub Actions
- Trivy Security Scanner
- GitHub Container Registry (GHCR)

## Run the Service with One Command

From the repository root, with Docker running:

```bash
docker build -t ai381-churn ./lab2 && docker run --rm -p 8000:8000 ai381-churn
```

The API will be available at:

http://localhost:8000

Interactive API documentation:

http://localhost:8000/docs

## API Endpoints

### GET /health

Checks whether the API is running.

Expected response:

```json
{
  "status": "ok"
}
```

### POST /predict

Predicts customer churn probability.

Example request:

```json
{
  "tenure_months": 12,
  "monthly_charges": 89.9,
  "support_calls": 3,
  "contract": "month-to-month",
  "internet_service": "fiber"
}
```

The response includes `churn_probability`, a value between 0 and 1.

## Automated Tests

The project includes pytest tests covering:

- Health endpoint response
- Model loading
- Invalid input validation
- Valid prediction response
- Prediction probability range

Run tests locally from the `lab2` directory:

```bash
python -m pytest tests/ -v
```

## Continuous Integration

GitHub Actions runs the following pipeline:

**Pull Requests to main**
- Run Ruff lint checks
- Run pytest tests

**Pushes to main**
- Build the Docker image
- Scan the image with Trivy
- Push the image to GHCR using the commit SHA as its tag
- Display the published image digest

## Docker Security

The Dockerfile uses a multi-stage build, runs the application as a non-root user, and includes a HEALTHCHECK.

Trivy scans for HIGH and CRITICAL vulnerabilities using the configured CI security policy.

## Repository Structure

```text
ai381-portfolio/
├── .github/workflows/lab2-ci.yml
├── lab2/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── model.joblib
│   ├── data/
│   ├── src/
│   │   ├── app/main.py
│   │   └── train/train.py
│   └── tests/test_api.py
└── README.md
```

## Branch Protection

The `main` branch requires pull requests and successful `Lint and pytest` status checks before merging.

## Course

AI381 — Machine Learning Operations

Lab 2 — Bring Your Own Model: Container + CI
