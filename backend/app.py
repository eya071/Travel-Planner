from flask import Flask, jsonify, request

app = Flask(__name__)

trips = []

@app.route("/")
def home():
    return jsonify({"message": "Travel Planner API is running"})


@app.route("/trips", methods=["GET"])
def get_trips():
    return jsonify(trips)


@app.route("/trips", methods=["POST"])
def create_trip():
    data = request.get_json()

    trip = {
        "destination": data.get("destination"),
        "start_date": data.get("start_date"),
        "end_date": data.get("end_date")
    }

    trips.append(trip)

    return jsonify(trip), 201


if __name__ == "__main__":
    app.run(debug=True)