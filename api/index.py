from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def home():
    return {"msg": "API working"}

@app.get("/analyze")
def analyze():
    return {
        "signal": "🔥 دخول قوي",
        "confidence": "85%",
        "next_target": "5x - 8x"
    }
