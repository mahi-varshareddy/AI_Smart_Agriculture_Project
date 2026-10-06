import os
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "crop_data.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "crop_model.pkl")

df = pd.read_csv(DATA_PATH)

features = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
X = df[features]
y = df["label"]

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)
model.fit(X, y)

os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
joblib.dump(model, MODEL_PATH)

print("Model trained successfully.")
print("Saved to:", MODEL_PATH)
print("Classes:", sorted(y.unique()))
