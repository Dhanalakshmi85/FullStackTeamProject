from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime
from bson.objectid import ObjectId
from backend.db import get_db
from backend.models import create_reservation

# Create Blueprint
main = Blueprint("main", __name__)

# ------------------- Static Pages -------------------

@main.route("/", methods=["GET"])
def home():
    return render_template("home.html", title="Home Page")

@main.route("/contact", methods=["GET"])
def contact():
    return render_template("contact.html", title="Contact Page")

@main.route("/cart")
def cart():
    return render_template("cart.html", title="Cart")

@main.route("/signup")
def signup():
    return render_template("signup.html")  

@main.route('/login', methods=['GET', 'POST'])
def login():
    # login logic
    return render_template('login.html')      

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
    data = request.get_json() or {}
    cart = data.get("cart", [])

    if not cart:
        return jsonify({"success": False, "message": "Cart empty"})

    # normalize and validate each item
    normalized = []
    for c in cart:
        try:
            price = float(c.get("price", 0) or 0)
            qty = int(c.get("qty", 0) or 0)
        except (ValueError, TypeError):
            continue
        if qty <= 0:
            continue
        normalized.append({"name": c.get("name", "Unknown"), "price": price, "qty": qty})

    if not normalized:
        return jsonify({"success": False, "message": "No valid items in cart"})

    total = sum(item["price"] * item["qty"] for item in normalized)

    db = get_db()
    user_id = session.get("user_id")
    customer_name = "Guest"
    if user_id:
        try:
            user = db["users"].find_one({"_id": ObjectId(user_id)})
            if user:
                customer_name = user.get("username") or user.get("name") or customer_name
        except Exception:
            pass

    order_doc = {
        "customer_name": session.get("username", customer_name),
        "items": normalized,
        "total": total,
        "status": "Pending",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    db["orders"].insert_one(order_doc)
    return jsonify({"success": True})

# ------------------- Reservation -------------------

@main.route("/reservation", methods=["GET"])
def reservation():
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


@main.route("/add-review", methods=["POST"])
def add_review():
    db = get_db()
    user_name = request.form.get("review-name")
    rating = int(request.form.get("review-rating"))
    comment = request.form.get("review-message")

    db["reviews"].insert_one({
        "user_id": user_name,
        "comment": comment,
        "rating": rating
    })

    return redirect(url_for("main.reviews_page"))  

# Route to display all reviews on front-end
@main.route("/reviews", methods=["GET"])
def reviews_page():
    db = get_db()
    reviews = list(db["reviews"].find())
    return render_template("contact.html", reviews=reviews)    