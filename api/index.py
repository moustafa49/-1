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
            return {"error": "محتاج داتا أكتر للصيد"}

        values = [float(v) for v in raw_values]
        recent = values[-12:] # تركيز على آخر 12 دورة (النطاق الساخن)
        
        # 1. كاشف الفخاخ (Trap Detector)
        # لو السيرفر مكرر أرقام تحت 1.2 أكتر من 3 مرات، إحنا في "مرحلة شفط"
        traps = sum(1 for v in values[-4:] if v < 1.2)
        
        # 2. تحليل "النبض" (Pulse Score)
        # بنشوف المسافة بين آخر "انفجار" (أكبر من 3x) ودلوقتي
        last_big_index = -1
        for i, v in enumerate(reversed(values)):
            if v >= 3.0:
                last_big_index = i
                break
        
        # 3. محرك الاحتمالية الهجومي (Aggressive Probability Engine)
        prob = 30.0
        
        # قانون الضغط: كل ما زاد عدد الأرقام الصغيرة (1.0 - 1.8) زاد احتمال الانفجار
        pressure = sum(1 for v in recent if v < 2.0) / len(recent)
        prob += (pressure * 60) 

        # قانون التبريد: لو لسه طالع رقم فلكي (أكبر من 10x)، الاحتمال بيقل فوراً
        if values[-1] > 8:
            prob -= 50
        elif values[-1] < 1.1: # الارتداد من القاع
            prob += 20

        # لو السيرفر بقاله كتير (أكتر من 6 أدوار) مجابش رقم فوق 2x، الاحتمالية بتنفجر
        if last_big_index > 6 or last_big_index == -1:
            prob += 25

        final_prob = max(1, min(99.9, round(prob, 1)))

        # 4. محرك التوقعات (Target Predictor)
        # النظام هنا "بيطمع" معاك لو الاحتمالية عالية
        if final_prob > 85:
            signal = "🚀 انفجار مؤكد (Target: 5x+)"
            # بيتوقع رقم بين أكبر رقمين في آخر 20 دورة
            top_vals = sorted([v for v in values[-20:] if v > 2])
            prediction = np.mean(top_vals[-2:]) if len(top_vals) >= 2 else 4.5
        elif final_prob > 65:
            signal = "🔥 فرصة قوية (Target: 2x)"
            prediction = 2.15
        elif final_prob > 40:
            signal = "⚠️ انتظار (خطر متقلب)"
            prediction = 1.45
        else:
            signal = "❌ منطقة موت (تجنب)"
            prediction = 1.01

        return {
            "signal": signal,
            "probability": f"{final_prob}%",
            "predicted_next": round(prediction, 2),
            "trend": "تجميع قوي 💎" if pressure > 0.7 else "توزيع 💸",
            "pressure_level": "خطير (شفط) 🧛" if traps >= 2 else "آمن (توزيع) ✅"
        }
    except Exception as e:
        return {"error": "بيانات غير صالحة"}
        
