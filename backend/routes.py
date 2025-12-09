from flask import Blueprint, render_template, request, jsonify, session
from datetime import datetime
from bson.objectid import ObjectId
from backend.db import get_db
from backend.models import create_reservation

main = Blueprint("main", __name__)

# ------------------- Static Pages -------------------

@main.route("/", methods=["GET"])
def home():
    return render_template("home.html", title="Home Page")

@main.route("/contact", methods=["GET"])
def contact():
    return render_template("contact.html", title="Contact Page")

@main.route("/cart", methods=["GET"])
def cart():
    return render_template("cart.html")   

@main.route("/signup")
def signup():
    return render_template("signup.html")    

# ------------------- Menu Route -------------------

@main.route("/menu/")
def menu():
    db = get_db()  # get the initialized database
    menu_collection = db["menu"]

    north_indian_items = list(menu_collection.find({"category": "north_indian"}))
    south_indian_items = list(menu_collection.find({"category": "south_indian"}))
    sri_lankan_items = list(menu_collection.find({"category": "sri_lankan"}))

    # Convert ObjectId to string for templates
    for item in north_indian_items + south_indian_items + sri_lankan_items:
        item["_id"] = str(item["_id"])

    return render_template(
        "menu.html",
        north_indian_items=north_indian_items,
        south_indian_items=south_indian_items,
        sri_lankan_items=sri_lankan_items
    )

# ------------------- Place Order -------------------

@main.route("/place-order", methods=["POST"])
def place_order():
    data = request.get_json()
    cart = data.get("cart", [])

    if not cart:
        return jsonify({"success": False, "message": "Cart empty"})

    db = get_db()  # get the database inside the route

    items = [{"name": c["name"], "qty": c["qty"], "price": c["price"]} for c in cart]
    total = sum(c["price"] * c["qty"] for c in cart)

    user_id = session.get("user_id")
    customer_name = "Guest"

    if user_id:
        user = db["users"].find_one({"_id": ObjectId(user_id)})
        if user:
            customer_name = user.get("username") or user.get("name") or "Guest"

    order_doc = {
        "customer_name": session.get("username", customer_name),
        "items": items,
        "total": total,
        "status": "Pending",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    db["orders"].insert_one(order_doc)

    return jsonify({"success": True})

# ------------------- Reservation -------------------

@main.route("/reservation", methods=["GET"])
def reservation_page():
    return render_template("reservation.html")

@main.route("/create-reservation", methods=["POST"])
def create_reservation_route():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "No data received"}), 400

        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")
        party_size_str = data.get("party_size")
        date_str = data.get("date")
        time = data.get("time")
        notes = data.get("notes", "")

        if not all([name, email, phone, party_size_str, date_str, time]):
            return jsonify({"success": False, "message": "Missing required fields"}), 400

        try:
            party_size = int(party_size_str)
        except ValueError:
            return jsonify({"success": False, "message": "Party size must be a number"}), 400

        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"success": False, "message": "Invalid date format"}), 400

        result = create_reservation(name, email, phone, party_size, date_obj, time, notes)

        return jsonify({"success": True, "message": "Reservation created", "id": str(result.inserted_id)})

    except Exception as e:
        print("Error creating reservation:", e)
        return jsonify({"success": False, "message": str(e)}), 500
