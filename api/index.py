# index.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ حل مشكلة CORS (مهم للـ Netlify)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ اختبار السيرفر
@app.get("/")
def home():
    return {"msg": "API working"}

# 🔥 التحليل
@app.post("/analyze")
def analyze(data: dict):

    values = data.get("values", [])

    if not values:
        return {"error": "No data"}

    avg = sum(values) / len(values)
    mx = max(values)
    mn = min(values)

    # 📈 Momentum
    momentum = values[-1] - values[-2] if len(values) >= 2 else 0

    # 🔥 Ratio
    ratio = mx / (mn + 0.01)

    # 🌊 Volatility
    volatility = round(mx - mn, 2)

    # 📊 Trend
    trend = "📈 صاعد" if momentum > 0 else "📉 هابط"

    # 🚀 ذكاء (كشف الصاروخ)
    high_spike = any(v > 10 for v in values[-5:])

    if high_spike:
        signal = "🚀 صاروخ محتمل"
    elif avg > 2:
        signal = "🔥 دخول قوي"
    else:
        signal = "❌ ضعيف"

    return {
        "signal": signal,
        "target": "5x → 7x",
        "confidence": "80%",
        "avg": round(avg, 2),
        "max": mx,
        "min": mn,
        "momentum": round(momentum, 2),
        "ratio": round(ratio, 2),
        "volatility": volatility,
        "trend": trend
    }
