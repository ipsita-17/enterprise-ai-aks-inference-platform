import pandas as pd
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

import joblib
import mlflow
import mlflow.sklearn
import os

# MLflow experiment
mlflow.set_experiment("iris-classification")

# Load dataset
iris = load_iris()

X = iris.data
y = iris.target

# Train/Test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

with mlflow.start_run():

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)

    # Log parameters
    mlflow.log_param(
        "n_estimators",
        100
    )

    mlflow.log_param(
        "test_size",
        0.2
    )

    # Log metrics
    mlflow.log_metric(
        "accuracy",
        accuracy
    )

    # Log model
    # mlflow.sklearn.log_model(
    #     model,
    #     "model"
    # )

    print(f"Accuracy: {accuracy}")

# Create artifacts folder
os.makedirs("model/artifacts", exist_ok=True)

# Save model locally
joblib.dump(
    model,
    "model/artifacts/model.pkl"
)

print("Model trained successfully")
print("Artifact saved: model/artifacts/model.pkl")