from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import statistics
import numpy as np

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

    if len(values) < 10:
        return {"error": "Need more data"}

    recent = values[-25:]

    avg = np.mean(recent)
    volatility = np.std(recent)

    # 🔥 weighted average (الأحدث أهم)
    weights = np.arange(1, len(recent)+1)
    weighted_avg = np.sum(recent * weights) / np.sum(weights)

    # 🔥 regression (توقع فعلي)
    x = np.arange(len(recent))
    y = np.array(recent)

    coef = np.polyfit(x, y, 1)
    next_pred = coef[0]*len(recent) + coef[1]

    # 🔥 smoothing
    smooth = np.convolve(recent, np.ones(3)/3, mode='valid')[-1]

    # 🔥 streaks
    low_streak = 0
    for v in reversed(recent):
        if v < 1.5:
            low_streak += 1
        else:
            break

    # 🔥 fake pattern detection
    fake_pattern = False
    if volatility < 0.5:
        fake_pattern = True

    # ⚡ momentum
    momentum = recent[-1] - recent[-2]

    # 🔥 pressure
    low_pressure = sum(1 for v in recent if v < 1.5) / len(recent)

    # 🧠 score
    score = 0
    score += low_streak * 2
    score += momentum
    score += volatility
    score += low_pressure * 5

    if fake_pattern:
        score -= 3

    probability = max(5, min(95, round(score * 10, 2)))

    # 🔮 prediction logic
    if probability > 75:
        signal = "🚀 انفجار قوي جداً"
    elif probability > 55:
        signal = "🔥 دخول قوي"
    elif probability > 35:
        signal = "⚠️ متوسط"
    else:
        signal = "❌ خطر"

    # 🎯 range ذكي
    low = round(max(1.1, next_pred * 0.6),2)
    high = round(next_pred * 1.8,2)

    return {
        "signal": signal,
        "probability": probability,
        "predicted_next": round(next_pred,2),
        "range_low": low,
        "range_high": high,
        "avg": round(avg,2),
        "volatility": round(volatility,2),
        "momentum": round(momentum,2),
        "weighted_avg": round(weighted_avg,2),
        "smooth": round(smooth,2),
        "fake_pattern": fake_pattern
    }
