from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Load dataset
iris = load_iris()

X = iris.data
y = iris.target

# Train model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

# Create artifacts folder
os.makedirs("model/artifacts", exist_ok=True)

# Save model
joblib.dump(
    model,
    "model/artifacts/model.pkl"
)

print("Model trained successfully")
print("Artifact saved: model/artifacts/model.pkl")