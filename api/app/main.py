from fastapi import FastAPI
from pydantic import BaseModel
import joblib

from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import Response

app = FastAPI()

model = joblib.load("model/artifacts/model.pkl")

# Metrics

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

    prediction = model.predict([[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width
    ]])

    return {
        "prediction": int(prediction[0])
    }