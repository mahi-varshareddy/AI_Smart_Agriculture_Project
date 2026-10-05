# AI-Powered Smart Agriculture Monitoring and Crop Recommendation System

## Features
1. AI/ML-based crop recommendation.
2. Soil N-P-K input.
3. Temperature and humidity monitoring.
4. Soil-moisture based irrigation advice.
5. Soil pH and rainfall input.
6. SQLite storage of readings.
7. Web dashboard using Flask.

## Requirements
- Python 3.10 or newer recommended
- pip

## Installation

Open Command Prompt/Terminal in this project folder:

```bash
python -m venv venv
```

Windows:
```bash
venv\Scripts\activate
```

Linux/macOS:
```bash
source venv/bin/activate
```

Install packages:
```bash
pip install -r requirements.txt
```

Train the ML model:
```bash
python train_model.py
```

Run the web application:
```bash
python app.py
```

Open:
```text
http://127.0.0.1:5000
```

## Sample values

Try:
- Nitrogen: 90
- Phosphorus: 42
- Potassium: 43
- Temperature: 20.9
- Humidity: 82
- Soil Moisture: 55
- pH: 6.5
- Rainfall: 202

The model will recommend a crop based on the supplied agricultural parameters.

## Project structure

AI_Smart_Agriculture_Project/
├── app.py
├── train_model.py
├── requirements.txt
├── README.md
├── agriculture.db              # created automatically
├── data/
│   └── crop_data.csv
├── models/
│   └── crop_model.pkl          # created by train_model.py
├── static/
│   └── style.css
└── templates/
    ├── index.html
    └── result.html

## Note
The included dataset is a compact educational/demo dataset. For a real agricultural deployment, use locally validated soil/weather data, calibrated sensors, and agronomist-reviewed recommendations.
