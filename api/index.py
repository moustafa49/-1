from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Data(BaseModel):
    values: list[float]

@app.get("/")
def home():
    return {"msg": "API working"}

@app.post("/analyze")
def analyze(data: Data):
    values = data.values

    if not values:
        return {"error": "no data"}

    avg = sum(values) / len(values)
    mx = max(values)
    mn = min(values)

    # تحليل بسيط ذكي
    high = [v for v in values if v >= 2]
    low = [v for v in values if v < 2]

    if len(high) > len(low):
        signal = "🔥 دخول قوي"
        target = "5x - 8x"
        confidence = "85%"
    else:
        signal = "⚠️ حذر"
        target = "2x - 3x"
        confidence = "60%"

    return {
        "signal": signal,
        "target": target,
        "confidence": confidence,
        "avg": round(avg, 2),
        "max": mx,
        "min": mn
    }
