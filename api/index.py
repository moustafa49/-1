from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/analyze")
async def analyze(data: dict):
    try:
        raw_values = data.get("values", [])
        if len(raw_values) < 5:
            return {"error": "محتاج بيانات أكتر"}

        values = [float(v) for v in raw_values]
        recent = np.array(values[-15:])
        
        # 1. تحليل "قوة الارتداد" (Rebound Strength)
        # لو الأرقام اللي فاتت كانت صغيرة جداً، الاحتمال لقفزة كبيرة بيزيد
        low_streak = 0
        for v in reversed(values):
            if v < 1.5: low_streak += 1
            else: break
            
        # 2. تحليل التذبذب (Volatility)
        volatility = np.std(recent)
        
        # 3. حساب الاحتمالية الذكية
        # بنزود الوزن للأرقام الصغيرة اللي بتعمل "تجميع" (Pressure)
        pressure = sum(1 for v in recent if v < 1.3) / len(recent)
        
        base_prob = 35
        base_prob += (pressure * 50)  # كل ما زاد الضغط زادت فرصة الانفجار
        base_prob += (low_streak * 5) # كل ما زاد الثبات على الصغير زادت فرصة القفزة
        
        # لو آخر رقم كان عالي جداً، بنقلل الاحتمالية (التبريد)
        if values[-1] > 10: base_prob -= 30
        
        final_prob = max(5, min(99, round(base_prob, 1)))

        # 4. معادلة التوقع الهجومية (Aggressive Prediction)
        # بدل ما نضرب في الميل بس، هنستخدم الانحراف المعياري لتوقع "القفزة"
        if final_prob > 70:
            # توقع انفجار بناءً على متوسط الأرقام العالية السابقة
            big_hits = [v for v in values if v > 2.0]
            prediction = np.mean(big_hits) if big_hits else 2.5
        else:
            # توقع آمن
            prediction = np.median(recent) * 1.2

        # 5. اختيار الإشارة
        if final_prob > 80: signal = "🚀 انفجار مؤكد (قريباً)"
        elif final_prob > 60: signal = "🔥 منطقة تجميع صاعدة"
        elif final_prob > 40: signal = "⚠️ حذر متذبذب"
        else: signal = "❌ خطر / سكون"

        return {
            "signal": signal,
            "probability": f"{final_prob}%",
            "predicted_next": round(max(1.1, prediction), 2),
            "trend": "تجميع 📦" if low_streak > 2 else "مستقر ⚖️",
            "pressure_level": "انفجاري 🧨" if pressure > 0.6 else "هادئ ❄️"
        }
    except Exception as e:
        return {"error": str(e)}
        
