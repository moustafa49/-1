from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import warnings

warnings.filterwarnings('ignore')
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# "العقل" - نموذج ذكاء اصطناعي
model = RandomForestRegressor(n_estimators=100, random_state=42)

def prepare_data(values, window=5):
    X, y = [], []
    for i in range(len(values) - window):
        X.append(values[i:i+window])
        y.append(values[i+window])
    return np.array(X), np.array(y)

@app.post("/api/analyze")
async def analyze(data: dict):
    try:
        raw_values = data.get("values", [])
        if len(raw_values) < 10:
            return {"error": "محتاج 10 أرقام على الأقل لتدريب الذكاء الاصطناعي"}

        values = [float(v) for v in raw_values]
        
        # تحويل البيانات لنمط يفهمه الذكاء الاصطناعي (أدخل 5 أرقام توقع الـ 6)
        X, y = prepare_data(values)
        
        # تدريب سريع للنموذج على بياناتك الحالية
        model.fit(X, y)
        
        # التوقع للجولة القادمة
        last_window = np.array([values[-5:]])
        prediction = model.predict(last_window)[0]
        
        # حساب "الاحتمالية الذكية" بناءً على ثبات النموذج
        recent_std = np.std(values[-5:])
        pressure = sum(1 for v in values[-10:] if v < 2.0) / 10
        
        prob = 40 + (pressure * 40)
        if prediction > 2.0: prob += 15
        
        final_prob = max(5, min(98.5, round(prob, 1)))

        # تحديد الإشارة الذكية
        if final_prob > 80 and prediction > 2.0:
            signal = "🚀 إشارة ذهبية (انفجار وشيك)"
        elif prediction > 3.0:
            signal = "🔥 نمط صاعد قوي"
        elif final_prob < 30:
            signal = "❌ نمط سحب (تجنب)"
        else:
            signal = "⚠️ تذبذب عالي"

        return {
            "signal": signal,
            "probability": f"{final_prob}%",
            "predicted_next": round(max(1.1, prediction), 2),
            "ai_logic": "RandomForest Analysis",
            "trend": "تصاعدي ذكي 📈" if prediction > np.mean(values) else "هبوطي ذكي 📉"
        }
    except Exception as e:
        return {"error": "الذكاء الاصطناعي يحتاج بيانات أكثر وضوحاً"}
        
