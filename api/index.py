from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return {"msg": "API working"}

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json.get("numbers", [])

    if not data:
        return jsonify({"error": "No data"}), 400

    avg = sum(data) / len(data)
    max_val = max(data)
    min_val = min(data)

    # تحليل بسيط
    if avg < 2:
        signal = "ضعيف ❌"
    elif avg < 5:
        signal = "متوسط ⚠️"
    else:
        signal = "قوي 🔥"

    return jsonify({
        "avg": round(avg, 2),
        "max": max_val,
        "min": min_val,
        "signal": signal
    })

# مهم لRailway
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
