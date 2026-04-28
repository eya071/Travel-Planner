from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# 🔹 Test route (så du slipper "Not Found")
@app.route("/")
def home():
    return "Backend is running 🚀"


# 🔹 API route
@app.route("/trips", methods=["POST"])
def create_trip():
    data = request.get_json()

    # 🔹 Sjekk om data finnes
    if not data:
        return jsonify({"error": "No data received"}), 400

    destination = data.get("destination")
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    people = data.get("people")
    budget = data.get("budget")

    # 🔹 Sjekk at alt er fylt inn
    if not all([destination, start_date, end_date, people, budget]):
        return jsonify({"error": "Missing fields"}), 400

    try:
        # 🔹 konverter dato
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
    except:
        return jsonify({"error": "Wrong date format (use YYYY-MM-DD)"}), 400

    days = (end - start).days + 1

    if days <= 0:
        return jsonify({"error": "End date must be after start date"}), 400

    # 🔹 aktiviteter
    activities = [
        "Utforsk byen",
        "Besøk museum",
        "Spis på restaurant",
        "Strand / natur",
        "Shopping",
        "Sightseeing",
        "Ta bilder og slapp av"
    ]

    plan = []

    for i in range(days):
        day_date = start + timedelta(days=i)
        activity = activities[i % len(activities)]

        plan.append({
            "day": i + 1,
            "date": day_date.strftime("%Y-%m-%d"),
            "activity": activity
        })

    # 🔹 fake pris
    flight_price = 1500 * int(people)
    hotel_price = 800 * days
    food_price = 300 * days * int(people)

    total_price = flight_price + hotel_price + food_price

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
            "total": total_price
        }
    })


if __name__ == "__main__":
    app.run(debug=True)