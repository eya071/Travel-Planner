from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import random

app = Flask(__name__)
CORS(app)
@app.route("/")
def home():
    return "Travel Planner Backend is running 🚀"
@app.route("/trips", methods=["POST"])
def create_trip():
    data = request.get_json()

    destination = data.get("destination")
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    people = int(data.get("people"))
    budget = data.get("budget")

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    days = (end - start).days + 1

    # 🔥 REALISTISK PLAN
    activities = [
        ("🏛️ Visit famous landmarks", "landmark"),
        ("🍝 Try local food", "restaurant food"),
        ("🛍️ Go shopping", "shopping street"),
        ("🌴 Explore nature", "nature landscape"),
        ("🏖️ Relax at the beach", "beach sunset"),
        ("🎭 Discover culture", "museum art")
    ]

    plan = []

    # ✅ LOOP MÅ VÆRE INNI FUNKSJONEN
    for i in range(days):
        title, keyword = activities[i % len(activities)]

        image_url = f"https://picsum.photos/seed/{destination}{i}/600/400"

        plan.append({
            "day": i + 1,
            "date": (start + timedelta(days=i)).strftime("%Y-%m-%d"),
            "title": title,
            "description": f"In {destination}",
            "image": image_url
        })

    # 💰 PRIS
    flight_price = 1200 * people
    hotel_price = 800 * days
    food_price = 300 * days * people

    return jsonify({
        "destination": destination,
        "start_date": start_date,
        "end_date": end_date,
        "people": people,
        "budget": budget,
        "plan": plan,
        "price": {
            "flight": flight_price,
            "hotel": hotel_price,
            "food": food_price,
            "total": flight_price + hotel_price + food_price
        }
    })

if __name__ == "__main__":
    app.run(debug=True)