from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import Response

from prometheus_client import Counter, Histogram, generate_latest

import joblib
import os

app = FastAPI()

# Model Loading

MODEL_PATH = "model/artifacts/model.pkl"

model = None

if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)

# Prometheus Metrics

prediction_counter = Counter(
    "prediction_requests_total",
    "Total prediction requests"
)

prediction_latency = Histogram(
    "prediction_latency_seconds",
    "Prediction latency"
)


class IrisRequest(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


@app.get("/")
def root():
    return {
        "status": "healthy",
        "service": "AI Inference API"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/version")
def version():
    return {
        "model": "iris-classifier",
        "version": "1.0.0"
    }


@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type="text/plain"
    )


@app.post("/predict")
@prediction_latency.time()
def predict(data: IrisRequest):

    prediction_counter.inc()

    if model is None:
        return {
            "error": "Model not loaded"
        }

    prediction = model.predict([[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width
    ]])

    return {
        "prediction": int(prediction[0])
    }