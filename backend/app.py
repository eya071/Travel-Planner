from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import logging

from database import init_db, save_trip, get_all_trips

# Logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)

# Initialise DB
init_db()


@app.route("/")
def home():
    return "Travel Planner Backend is running 🚀"


@app.route("/trips", methods=["POST"])
def create_trip():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        destination = data.get("destination")
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        people = int(data.get("people", 1))
        budget = data.get("budget")

        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")

        days = (end - start).days + 1

        activities = [
    "Besøk kjente landemerker",
    "Spis lokal mat",
    "Handle i byen",
    "Utforsk naturen",
    "Slapp av ved stranden",
    "Besøk museum"
]

        plan = []

        for i in range(days):
            title = activities[i % len(activities)]
            image_url = f"https://picsum.photos/seed/{destination}{i}/600/400"

            plan.append({
                "day": i + 1,
                "date": (start + timedelta(days=i)).strftime("%Y-%m-%d"),
                "title": title,
                "description": f"I {destination}",
                "image": image_url
            })

        # Price calculation
        flight_price = 1200 * people
        hotel_price = 800 * days
        food_price = 300 * days * people

        # Save to DB
        save_trip(destination, start_date, end_date, people, budget)

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

    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"error": "Something went wrong"}), 500


@app.route("/trips", methods=["GET"])
def list_trips():
    trips = get_all_trips()
    return jsonify(trips)


if __name__ == "__main__":
    app.run(debug=True)