from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import statistics

app = FastAPI()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"msg": "API working"}

@app.post("/analyze")
def analyze(data: dict):

    values = data.get("values", [])

    if len(values) < 5:
        return {"error": "Need at least 5 values"}

    last = values[-10:]

    avg = sum(values) / len(values)
    volatility = statistics.stdev(values)

    # 🔥 low streak
    low_streak = 0
    for v in reversed(last):
        if v < 1.5:
            low_streak += 1
        else:
            break

    # 🔥 ضغط
    low_count = sum(1 for v in last if v < 1.5)

    # ⚡ momentum
    momentum = last[-1] - last[-2]

    # 🧠 score
    score = 0

    if low_streak >= 3:
        score += 2

    if low_count >= 6:
        score += 2

    if momentum > 0:
        score += 1

    if volatility > 2:
        score += 1

    # 🎯 decision
    if score >= 5:
        signal = "🚀 انفجار قوي جدًا"
        pred_low, pred_high = 5, 20
    elif score >= 4:
        signal = "🔥 دخول قوي"
        pred_low, pred_high = 3, 10
    elif score >= 3:
        signal = "⚠️ متوسط"
        pred_low, pred_high = 2, 5
    else:
        signal = "❌ خطر"
        pred_low, pred_high = 1.1, 2

    next_estimate = round((pred_low + pred_high) / 2, 2)

    return {
        "signal": signal,
        "score": score,
        "prediction_low": pred_low,
        "prediction_high": pred_high,
        "next_estimate": next_estimate,
        "low_streak": low_streak,
        "avg": round(avg,2),
        "volatility": round(volatility,2)
    }
