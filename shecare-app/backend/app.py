from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import google.generativeai as genai  # ✅ Gemini library

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# ✅ SET YOUR GEMINI API KEY HERE
genai.configure(api_key="AIzaSyDSMEg7oa8bid-4UDEAWReF1JbsiPDqhao")  # ← Replace with your own API key

@app.route("/")
def home():
    return "SheCare Flask Backend is running!"

# ✅ Predict Period & Fertile Window
@app.route("/predict_period", methods=["POST"])
def predict_period():
    data = request.get_json()
    last_period = data.get("last_period_date")
    cycle_length = int(data.get("cycle_length"))

    try:
        last_date = datetime.strptime(last_period, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400

    next_period = last_date + timedelta(days=cycle_length)
    fertile_start = last_date + timedelta(days=cycle_length - 14)
    fertile_end = fertile_start + timedelta(days=5)

    return jsonify({
        "next_period": next_period.strftime("%Y-%m-%d"),
        "fertile_start": fertile_start.strftime("%Y-%m-%d"),
        "fertile_end": fertile_end.strftime("%Y-%m-%d")
    })

#  Mood-Based Suggestions
@app.route("/get_suggestions", methods=["POST"])
def get_suggestions():
    data = request.get_json()
    mood = data.get("mood", "")
    symptoms = data.get("symptoms", [])

    suggestions = {
        "music": [],
        "diet": [],
        "remedies": [],
        "tips": []
    }

    # Mood Music
    if mood == "Anxious":
        suggestions["music"].append("Listen to calm piano or ocean waves.")
    elif mood == "Sad":
        suggestions["music"].append("Try happy acoustic or feel-good pop songs.")
    elif mood == "Stressed":
        suggestions["music"].append("Lofi beats or ambient focus music can help.")
    elif mood == "Tired":
        suggestions["music"].append("Soft jazz or nature sounds can soothe.")
    elif mood=="Happy" :
        suggestions["music"].append("Fun, colorful, and upbeat tracks. ")
    elif mood=="Energetic":  
     suggestions["music"].append(" High energy and rhythm.")
                
    

    # Diet based on symptoms
    if "Bloating" in symptoms:
        suggestions["diet"].append("Avoid salty snacks. Try mint tea or cucumber.")
    if "Cramps" in symptoms:
        suggestions["diet"].append("Eat bananas, spinach, and dark chocolate.")
    if "Headache" in symptoms:
        suggestions["diet"].append("Drink water and eat magnesium-rich foods.")
    if "Bloating" in symptoms:
        suggestions["diet"].append("Eat small, frequent meals with fiber-rich veggies.")
    if "Mood Swings" in symptoms:
        suggestions["diet"].append("Eat balanced meals with complex carbs,and magnesium-rich foods like bananas and dark chocolate.")
    if "Nausea" in symptoms:
        suggestions["diet"].append("Eat small, bland meals like crackers, bananas, or plain toast.")

    # Remedies based on symptoms
    if "Cramps" in symptoms:
        suggestions["remedies"].append("Use a heating pad on your lower abdomen.")
    if "Bloating" in symptoms:
        suggestions["remedies"].append("Drink warm water with a pinch of fennel or ginger and avoid salty, carbonated, and processed foods.")
    if "Headache" in symptoms:
        suggestions["remedies"].append("Stay hydrated, rest in a quiet dark room, apply a cold or warm compress.")
    if "Mood Swings" in symptoms:
        suggestions["remedies"].append(" practice calming routines like deep breathing or journaling.")
    if "Nausea" in symptoms:
        suggestions["remedies"].append("Sip ginger tea, stay hydrated with small sips of water, and avoid strong smells or heavy foods.")
    if "Backpain" in symptoms:
        suggestions["remedies"].append("Apply a heating pad, maintain good posture, and do gentle stretche.")

    # Tips
    suggestions["tips"].append("Stay hydrated and rest well.")
    if mood in ["Tired", "Sad"]:
        suggestions["tips"].append("Take a short walk in sunlight or stretch gently.")

    return jsonify(suggestions)

# AskShe
@app.route("/ask_shecare", methods=["POST"])
def ask_shecare():
    data = request.get_json()
    user_query = data.get("query", "")

    if not user_query:
        return jsonify({"error": "Query is empty"}), 400

    try:
        # ✅ Use latest model list for compatibility
        model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

        chat = model.start_chat(history=[
            {"role": "user", "parts": [
                "You are SheCare, a friendly women’s health assistant. Answer questions about periods, PCOS, cramps, female wellness, and emotional support. Be warm, clear, helpful, and supportive."
            ]}
        ])

        response = chat.send_message(user_query)
        return jsonify({"answer": response.text.strip()})
    except Exception as e:
        print("Gemini Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
