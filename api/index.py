from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import statistics

app = FastAPI()

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
    if not values:
        return {"error": "No data"}

    avg = sum(values) / len(values)
    mx = max(values)
    mn = min(values)

    # 🧠 weighted avg
    weights = list(range(1, len(values)+1))
    weighted_avg = sum(v*w for v,w in zip(values, weights)) / sum(weights)

    # ⚡ momentum
    momentum = sum(values[-3:]) - sum(values[-6:-3]) if len(values) >= 6 else 0

    # 🔥 pressure
    low_count = sum(1 for v in values[-10:] if v < 1.5)
    pressure = low_count / min(len(values),10)

    # 🌊 volatility
    volatility = statistics.stdev(values) if len(values) > 1 else 0

    # 🚀 spike
    spike = max(values[-5:]) if len(values) >= 5 else mx

    # 📈 trend
    trend = "📈 صاعد" if momentum > 0 else "📉 هابط"

    # 🧠 signal
    if pressure > 0.6 and spike < 5:
        signal = "🚀 انفجار قريب"
    elif weighted_avg > 2 and momentum > 0:
        signal = "🔥 دخول قوي"
    elif weighted_avg < 1.5:
        signal = "❌ خطر"
    else:
        signal = "⏳ انتظار"

    # 🔮 prediction (نقطة مهمة)
    base = weighted_avg

    # تعديل حسب الحالة
    if pressure > 0.6:
        base += 1.5
    if momentum > 0:
        base += 0.5
    if volatility > 2:
        base += 0.7

    prediction_low = round(max(1.1, base * 0.7), 2)
    prediction_high = round(base * 1.6, 2)
    next_estimate = round((prediction_low + prediction_high) / 2, 2)

    return {
        "signal": signal,
        "trend": trend,
        "avg": round(avg,2),
        "weighted_avg": round(weighted_avg,2),
        "momentum": round(momentum,2),
        "pressure": round(pressure,2),
        "volatility": round(volatility,2),
        "prediction_low": prediction_low,
        "prediction_high": prediction_high,
        "next_estimate": next_estimate
    }
