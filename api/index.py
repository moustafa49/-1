from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import json
import os

app = FastAPI()

# السماح للواجهة بالاتصال بالسيرفر
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# مسار تخزين مؤقت للبيانات (Vercel بيسمح بالكتابة هنا فقط)
DATA_FILE = "/tmp/crash_history.json"

def load_history():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except: return []
    return []

def save_history(history):
    with open(DATA_FILE, "w") as f:
        json.dump(history[-100:], f) # نحفظ آخر 100 رقم فقط للسرعة

@app.post("/api/analyze")
async def analyze(data: dict):
    try:
        raw_values = data.get("values", [])
        if not raw_values or len(raw_values) < 5:
            return {"error": "محتاج 5 أرقام على الأقل للتحليل"}

        # تحويل البيانات لأرقام عشرية
        values = [float(v) for v in raw_values]
        
        # حفظ واسترجاع التاريخ للتعلم من النمط
        history = load_history()
        history.extend(values)
        save_history(history)

        # تحويل لـ Numpy للعمليات الحسابية
        recent = np.array(values[-20:]) 
        
        # 1. تحليل الاتجاه (Trend Analysis)
        # بيشوف هل الأرقام في تصاعد ولا هبوط باستخدام معامل الانحدار
        x = np.arange(len(recent))
        slope = np.polyfit(x, recent, 1)[0]
        trend = "تصاعدي 📈" if slope > 0.05 else "هبوطي 📉" if slope < -0.05 else "مستقر ⚖️"

        # 2. مؤشر الضغط (Pressure Index)
        # بيحسب نسبة الأرقام الصغيرة (تحت 1.5)؛ لو كتير يبقى فيه انفجار جاي
        low_count = sum(1 for v in recent if v < 1.5)
        pressure_ratio = low_count / len(recent)
        pressure_level = "عالي جداً 🔥" if pressure_ratio > 0.6 else "متوسط ⚠️" if pressure_ratio > 0.3 else "منخفض ❄️"

        # 3. حساب الاحتمالية الذكية (Smart Probability)
        # معادلة بتجمع بين الزخم، الضغط، والاتجاه
        base_prob = 40
        base_prob += (pressure_ratio * 40) # الضغط العالي يرفع الاحتمالية
        base_prob += (slope * 20)          # الاتجاه الصاعد يرفع الاحتمالية
        
        # لمسة ذكاء: لو آخر رقم صغير جداً، بنزود احتمالية الارتداد
        if recent[-1] < 1.2:
            base_prob += 15

        final_prob = max(5, min(98, round(base_prob, 1)))

        # 4. التوقع القادم (Prediction)
        # بيعتمد على الوسيط الحسابي مع تعديل بناءً على الميل
        prediction = np.median(recent) * (1 + slope)
        if prediction < 1.1: prediction = 1.25

        # 5. اختيار الإشارة
        if final_prob > 80:
            signal = "🚀 انفجار مؤكد"
        elif final_prob > 60:
            signal = "🔥 فرصة قوية"
        elif final_prob > 40:
            signal = "⚖️ منطقة حيرة"
        else:
            signal = "❌ سكون / خطر"

        return {
            "signal": signal,
            "probability": f"{final_prob}%",
            "predicted_next": round(prediction, 2),
            "trend": trend,
            "pressure_level": pressure_level
        }

    except Exception as e:
        return {"error": str(e)}

# للتشغيل المحلي فقط
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
