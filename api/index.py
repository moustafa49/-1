from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = "history.json"

# تحميل بيانات قديمة
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

# حفظ بيانات
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

@app.post("/analyze")
def analyze(data: dict):

    values = data.get("values", [])
    if len(values) < 6:
        return {"error": "Need more data"}

    # 🔥 learning storage
    history = load_data()
    history.extend(values[-5:])
    save_data(history[-500:])  # حفظ آخر 500

    recent = values[-25:]

    avg = np.mean(recent)
    volatility = np.std(recent)

    # weighted
    weights = np.arange(1, len(recent)+1)
    weighted_avg = np.sum(recent * weights) / np.sum(weights)

    # regression
    x = np.arange(len(recent))
    y = np.array(recent)
    coef = np.polyfit(x, y, 1)
    next_pred = coef[0]*len(recent) + coef[1]

    # streak
    low_streak = sum(1 for v in reversed(recent) if v < 1.5)

    # momentum
    momentum = recent[-1] - recent[-2]

    # pressure
    low_pressure = sum(1 for v in recent if v < 1.5)/len(recent)

    # 🧠 learning boost (من الداتا القديمة)
    history_avg = np.mean(history) if history else avg

    score = 0
    score += low_streak * 2
    score += momentum
    score += volatility
    score += low_pressure * 4

    if avg < history_avg:
        score += 2

    probability = max(5, min(95, round(score * 10,2)))

    if probability > 75:
        signal = "🚀 انفجار عالي"
    elif probability > 55:
        signal = "🔥 فرصة قوية"
    elif probability > 35:
        signal = "⚠️ متوسط"
    else:
        signal = "❌ خطر"

    low = max(1.1, next_pred * 0.6)
    high = next_pred * 1.8

    return {
        "signal": signal,
        "probability": probability,
        "predicted": round(next_pred,2),
        "range_low": round(low,2),
        "range_high": round(high,2),
        "avg": round(avg,2),
        "volatility": round(volatility,2),
        "momentum": round(momentum,2),
        "history_avg": round(history_avg,2)
    }
