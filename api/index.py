from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ أهم سطر (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ممكن تخليها موقعك بس بعدين
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"msg": "API working"}

@app.post("/analyze")
def analyze(data: dict):
    values = data.get("values", [])

    if not values:
        return {"error": "No data"}

    avg = sum(values) / len(values)
    mx = max(values)
    mn = min(values)

    signal = "🔥 دخول قوي" if avg > 2 else "❌ ضعيف"

    return {
        "signal": signal,
        "target": "5x → 7x",
        "confidence": "80%",
        "avg": round(avg, 2),
        "max": mx,
        "min": mn
    }
