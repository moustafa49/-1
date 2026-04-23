from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import json
import os

app = FastAPI()

# تفعيل الـ CORS عشان Netlify يقدر يكلم Railway
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/analyze")
async def analyze(data: dict):
    try:
        raw_values = data.get("values", [])
        if not raw_values or len(raw_values) < 5:
            return {"error": "محتاج 5 أرقام على الأقل"}

        values = [float(v) for v in raw_values]
        recent = np.array(values[-20:]) 
        
        # تحليل الميل (Trend)
        x = np.arange(len(recent))
        slope = np.polyfit(x, recent, 1)[0]
        trend = "تصاعدي 📈" if slope > 0.05 else "هبوطي 📉" if slope < -0.05 else "مستقر ⚖️"

        # مؤشر الضغط (Pressure)
        low_count = sum(1 for v in recent if v < 1.5)
        pressure_ratio = low_count / len(recent)
        pressure_level = "عالي جداً 🔥" if pressure_ratio > 0.6 else "متوسط ⚠️" if pressure_ratio > 0.3 else "منخفض ❄️"

        # الاحتمالية
        base_prob = 40 + (pressure_ratio * 40) + (slope * 20)
        if values[-1] < 1.2: base_prob += 15
        final_prob = max(5, min(98, round(base_prob, 1)))

        # التوقع
        prediction = np.median(recent) * (1 + slope)

        return {
            "signal": "🚀 انفجار" if final_prob > 75 else "🔥 فرصة" if final_prob > 50 else "❌ خطر",
            "probability": f"{final_prob}%",
            "predicted_next": round(max(1.1, prediction), 2),
            "trend": trend,
            "pressure_level": pressure_level
        }
    except Exception as e:
        return {"error": str(e)}
        
