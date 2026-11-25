from flask import Flask, jsonify, request, send_from_directory
from datetime import datetime
import os

app = Flask(__name__, static_folder=".")

# In-memory store for bookings (persists while server runs)
BOOKINGS = []


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/api/bookings", methods=["GET"])
def get_bookings():
    return jsonify({"count": len(BOOKINGS), "bookings": BOOKINGS}), 200


@app.route("/api/bookings", methods=["POST"])
def create_booking():
    data = request.get_json(silent=True) or {}
    required = ["itemName", "from", "to", "date", "amount", "passenger", "pnr"]
    missing = [field for field in required if not data.get(field)]

    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    booking = {
        "pnr": data["pnr"],
        "category": data.get("category", "GENERAL"),
        "itemId": data.get("itemId", ""),
        "itemName": data["itemName"],
        "from": data["from"],
        "to": data["to"],
        "date": data["date"],
        "pax": data.get("pax", "1"),
        "passenger": data["passenger"],
        "email": data.get("email", ""),
        "payMethod": data.get("payMethod", "UPI"),
        "amount": data["amount"],
        "status": "CONFIRMED & PAID",
        "bookedAt": datetime.utcnow().isoformat() + "Z",
    }
    BOOKINGS.insert(0, booking)
    return jsonify({"message": "Booking confirmed", "booking": booking}), 201


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
