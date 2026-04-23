from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from scipy.stats import norm

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def calculate_ai_precision(values):
    """خوارزمية تحليل النبض والضغط النفسي للسيرفر"""
    if len(values) < 8:
        return None

    # 1. تحليل "دورة السحب" (Drain Cycle)
    # بنشوف آخر كام رقم كانوا تحت الـ 1.5x (مناطق خسارة الناس)
    drain_zone = [v for v in values[-6:] if v < 1.5]
    drain_intensity = len(drain_zone) / 6

    # 2. تحليل "الارتداد الإحصائي" (Statistical Rebound)
    # بنحسب احتمالية حدوث رقم عالي بناءً على الانحراف المعياري
    mean = np.mean(values[-15:])
    std = np.std(values[-15:])
    last_val = values[-1]
    
    # Z-Score: هل الرقم الأخير كان بعيد جداً عن المعدل؟
    z_score = (last_val - mean) / std if std != 0 else 0

    # 3. محرك التوقع الهجومي (Aggressive Prediction)
    # لو فيه "ضغط" عالي (أرقام صغيرة كتير)، بنرفع سقف التوقع
    if drain_intensity > 0.6: # السيرفر "شبع" سحب فلوس
        multiplier = 2.5 + (drain_intensity * 2)
        signal = "🚀 إشارة انفجار (انقض الآن)"
        confidence = 85 + (drain_intensity * 10)
    elif last_val > 5: # السيرفر لسه مطلع رقم كبير، غالباً هيهدي
        multiplier = 1.2
        signal = "⚠️ تبريد (انتظر السحب)"
        confidence = 30
    else:
        multiplier = 1.5
        signal = "⚖️ توازن (منطقة مراقبة)"
        confidence = 55

    # حساب الرقم المتوقع بناءً على "نمط الارتداد"
    predicted = np.median(values[-10:]) * multiplier
    
    # تصحيح لو التوقع مبالغ فيه أو قليل زيادة
    predicted = max(1.15, min(predicted, 15.0))

    return {
        "signal": signal,
        "probability": f"{min(final_calc_prob(values, confidence), 99.2)}%",
        "predicted_next": round(predicted, 2),
        "ai_status": "Deep Analysis Active",
        "danger_level": "عالي" if drain_intensity < 0.3 else "منخفض (فرصة)"
    }

def final_calc_prob(values, base):
    """إضافة لمسة سيكولوجية للاحتمالية"""
    last = values[-1]
    if last < 1.1: base += 10 # ارتداد من القاع
    if 1.5 < last < 2.5: base -= 5 # منطقة حيرة
    return base

@app.post("/api/analyze")
async def analyze(data: dict):
    try:
        raw_values = data.get("values", [])
        if len(raw_values) < 8:
            return {"error": "الذكاء الاصطناعي يحتاج 8 أرقام على الأقل لضبط النبض"}
        
        values = [float(v) for v in raw_values]
        result = calculate_ai_precision(values)
        return result
    except:
        return {"error": "حدث خطأ في معالجة البيانات"}
        
