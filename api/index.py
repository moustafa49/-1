from fastapi import FastAPI
from typing import List

app = FastAPI()

@app.get("/")
def home():
    return {"msg": "API working"}

@app.post("/analyze")
def analyze(data: List[float]):
    if len(data) < 5:
        return {
            "result": "Need more data",
            "target": "--",
            "confidence": "0%",
            "trend": "-"
        }

    last5 = data[-5:]
    avg = sum(data) / len(data)
    recent_avg = sum(last5) / len(last5)

    high_count = len([x for x in data if x > 2])
    power = high_count / len(data)

    if recent_avg > 2.5 and power > 0.6:
        result = "🔥 Strong Entry"
        target = "5x → 10x"
        confidence = "85%"
        trend = "UP"
    elif recent_avg > 2:
        result = "⚡ Medium"
        target = "3x → 6x"
        confidence = "65%"
        trend = "Stable"
    else:
        result = "❌ Weak"
        target = "1x → 2x"
        confidence = "40%"
        trend = "Down"

    return {
        "result": result,
        "target": target,
        "confidence": confidence,
        "trend": trend,
        "avg": round(avg, 2),
        "recent": round(recent_avg, 2),
        "max": max(data),
        "min": min(data)
    }
