from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import statistics

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
def analyze(data: dict):

    values = data.get("values", [])

    if len(values) < 5:
        return {"error": "Need more data"}

    recent = values[-25:]

    avg = float(np.mean(recent))
    volatility = float(np.std(recent))

    # 🔥 weighted avg
    weights = np.arange(1, len(recent)+1)
    weighted_avg = float(np.sum(np.array(recent)*weights) / np.sum(weights))

    # 🔥 regression prediction
    x = np.arange(len(recent))
    y = np.array(recent)

    coef = np.polyfit(x, y, 1)
    next_pred = float(coef[0]*len(recent) + coef[1])

    # 🔥 momentum
    momentum = recent[-1] - recent[-2] if len(recent) > 1 else 0

    # 🔥 low streak
    low_streak = 0
    for v in reversed(recent):
        if v < 1.5:
            low_streak += 1
        else:
            break

    # 🔥 fake pattern
    fake_pattern = volatility < 0.5

    # 🔥 score
    score = 0
    score += low_streak * 2
    score += momentum
    score += volatility
    score += (sum(1 for v in recent if v < 1.5) / len(recent)) * 5

    if fake_pattern:
        score -= 3

    probability = max(5, min(95, round(score * 10, 2)))

    # 🔮 signal
    if probability > 75:
        signal = "🚀 انفجار قوي جداً"
    elif probability > 55:
        signal = "🔥 دخول قوي"
    elif probability > 35:
        signal = "⚠️ متوسط"
    else:
        signal = "❌ خطر"

    # 🎯 range
    low = round(max(1.1, next_pred * 0.6),2)
    high = round(next_pred * 1.8,2)

    return {
        "signal": signal,
        "probability": probability,
        "predicted_next": round(next_pred,2),
        "range_low": low,
        "range_high": high,
        "avg": round(avg,2),
        "vol
