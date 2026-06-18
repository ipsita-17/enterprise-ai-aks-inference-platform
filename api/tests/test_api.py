from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from api.app import main

main.model = MagicMock()
main.model.predict.return_value = [0]

client = TestClient(main.app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["service"] == "AI Inference API"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy"
    }


def test_version():
    response = client.get("/version")

    assert response.status_code == 200
    assert response.json() == {
        "model": "iris-classifier",
        "version": "1.0.0"
    }


def test_metrics():
    response = client.get("/metrics")

    assert response.status_code == 200


def test_predict():
    response = client.post(
        "/predict",
        json={
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2
        }
    )

    assert response.status_code == 200
    assert response.json()["prediction"] == 0


def test_predict_model_not_loaded():
    original_model = main.model

    try:
        main.model = None

        response = client.post(
            "/predict",
            json={
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2
            }
        )

        assert response.status_code == 200
        assert response.json()["error"] == "Model not loaded"

    finally:
        main.model = original_model