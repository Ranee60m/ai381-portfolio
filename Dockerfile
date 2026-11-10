# Install dependencies and export only a promoted model. Never silently retrain while building.
FROM python:3.12.15-slim-trixie AS builder
WORKDIR /build
COPY requirements.txt .
COPY src/ src/
COPY artifacts/ artifacts/
ARG GIT_SHA=local
RUN test -f artifacts/model.joblib && test -f artifacts/metadata.json
# Optional certificate bundle for networks with an HTTPS proxy; TLS verification stays enabled.
RUN --mount=type=secret,id=pip_ca,target=/run/secrets/pip_ca \
    if [ -f /run/secrets/pip_ca ]; then export PIP_CERT=/run/secrets/pip_ca; fi; \
    pip install --no-cache-dir --prefix=/install -r requirements.txt && \
    mkdir -p models && cp artifacts/model.joblib artifacts/metadata.json models/ && \
    python -c "import json,sys; p='models/metadata.json'; m=json.load(open(p)); m['model_version']=sys.argv[1][:7]; json.dump(m,open(p,'w'))" "$GIT_SHA" && \
    rm -rf artifacts && chmod -R a+rX /build /install

FROM python:3.12.15-slim-trixie
LABEL org.opencontainers.image.title="ai381-churn-lab3" \
      org.opencontainers.image.description="Tracked champion churn API, local Docker deployment"
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 MODEL_DIR=/app/models
RUN useradd --create-home --uid 10001 app
WORKDIR /app
COPY --from=builder /install /usr/local
COPY --from=builder /build /app
USER 10001
EXPOSE 8000
HEALTHCHECK --interval=15s --timeout=3s --start-period=10s --retries=3 \
  CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health', timeout=2)"]
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
