from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os
import joblib
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "agriculture.db")
MODEL_PATH = os.path.join(BASE_DIR, "models", "crop_model.pkl")

app = Flask(__name__)
app.secret_key = "smart-agriculture-demo-key"

FEATURES = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sensor_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nitrogen REAL,
            phosphorus REAL,
            potassium REAL,
            temperature REAL,
            humidity REAL,
            soil_moisture REAL,
            ph REAL,
            rainfall REAL,
            irrigation TEXT,
            recommendation TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def load_model():
    if not os.path.exists(MODEL_PATH):
        return None
    return joblib.load(MODEL_PATH)

def irrigation_advice(soil_moisture, temperature, humidity):
    if soil_moisture < 30:
        return "Irrigation required"
    if soil_moisture < 45:
        return "Irrigate soon"
    if temperature > 35 and humidity < 45:
        return "Light irrigation recommended"
    return "No irrigation required"

@app.route("/")
def index():
    conn = get_db()
    readings = conn.execute(
        "SELECT * FROM sensor_readings ORDER BY id DESC LIMIT 10"
    ).fetchall()
    conn.close()
    return render_template("index.html", readings=readings)

@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        values = {
            "N": float(request.form["nitrogen"]),
            "P": float(request.form["phosphorus"]),
            "K": float(request.form["potassium"]),
            "temperature": float(request.form["temperature"]),
            "humidity": float(request.form["humidity"]),
            "soil_moisture": float(request.form["soil_moisture"]),
            "ph": float(request.form["ph"]),
            "rainfall": float(request.form["rainfall"])
        }

        model = load_model()
        if model is None:
            flash("Model not found. Run: python train_model.py", "error")
            return redirect(url_for("index"))

        X = np.array([[values[f] for f in FEATURES]])
        crop = model.predict(X)[0]
        irrigation = irrigation_advice(
            values["soil_moisture"], values["temperature"], values["humidity"]
        )

        recommendation = (
            f"Recommended crop: {crop.title()}. "
            f"Irrigation status: {irrigation}."
        )

        conn = get_db()
        conn.execute("""
            INSERT INTO sensor_readings
            (nitrogen, phosphorus, potassium, temperature, humidity,
             soil_moisture, ph, rainfall, irrigation, recommendation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            values["N"], values["P"], values["K"], values["temperature"],
            values["humidity"], values["soil_moisture"], values["ph"],
            values["rainfall"], irrigation, recommendation
        ))
        conn.commit()
        conn.close()

        return render_template(
            "result.html",
            crop=crop.title(),
            irrigation=irrigation,
            values=values
        )
    except Exception as e:
        flash(f"Invalid input: {e}", "error")
        return redirect(url_for("index"))

@app.route("/clear")
def clear():
    conn = get_db()
    conn.execute("DELETE FROM sensor_readings")
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(debug=False,use_reloader=False)
