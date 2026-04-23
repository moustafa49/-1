from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np

app = FastAPI()

# تفعيل الربط مع Netlify (CORS)
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
        if len(raw_values) < 5:
            return {"error": "محتاج 5 أرقام على الأقل"}

        values = [float(v) for v in raw_values]
        recent = np.array(values[-20:])
        
        # تحليل الاتجاه والميل
        x = np.arange(len(recent))
        slope = np.polyfit(x, recent, 1)[0]
        
        # مؤشر الضغط (الأرقام الصغيرة)
        low_count = sum(1 for v in recent if v < 1.5)
        pressure = low_count / len(recent)

        # حساب الاحتمالية
        prob = 40 + (pressure * 40) + (slope * 20)
        if values[-1] < 1.2: prob += 15
        final_prob = max(5, min(98, round(prob, 1)))

        # التوقع
        prediction = np.median(recent) * (1 + slope)

        return {
            "signal": "🚀 انفجار" if final_prob > 75 else "🔥 فرصة" if final_prob > 50 else "❌ خطر",
            "probability": f"{final_prob}%",
            "predicted_next": round(max(1.1, prediction), 2),
            "trend": "تصاعدي 📈" if slope > 0 else "هبوطي 📉",
            "pressure_level": "عالي 🔥" if pressure > 0.5 else "منخفض ❄️"
        }
    except Exception as e:
        return {"error": str(e)}
        
