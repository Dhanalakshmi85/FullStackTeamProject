from flask import Blueprint, render_template, request, jsonify, session
from datetime import datetime
import backend.db as db_module
from backend.models import create_reservation

main = Blueprint("main", __name__)

@main.route("/", methods=["GET"])

def home():
    return render_template("home.html", title="Home Page")


@main.route("/menu", methods=["GET"])
def menu():
    return render_template("menu.html", title="Menu Page")

@main.route("/contact", methods=["GET"])
def contact():
    return render_template("contact.html", title="Contact Page")

@main.route("/cart", methods=["GET"])
def cart():
    return render_template("cart.html")   

# @main.route("/login", methods=["GET"])
# def login_page():
#     return render_template("login.html", title="Login Page")   

# @main.route('/reservation')
# def reservation():
#     return render_template('reservation.html')

@main.route('/signup')
def signup():
    return render_template('signup.html')    

@main.route("/place-order", methods=["GET","POST"])
def place_order():
    data = request.get_json()
    cart = data.get("cart", [])

    if not cart:
        return jsonify({"success": False, "message": "Cart empty"})

    db = db_module.get_db()

    items = [
        {"name": c["name"], "qty": c["qty"], "price": c["price"]}
        for c in cart
    ]

    total = sum(c["price"] * c["qty"] for c in cart)

    order_doc = {
        "customer_name": session.get("username", "Guest"),
        "items": items,
        "total": total,
        "status": "Pending",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    db["orders"].insert_one(order_doc)

    return jsonify({"success": True})


@main.route("/reservation", methods=["GET"])
def reservation_page():
    return render_template("reservation.html")

@main.route("/create-reservation", methods=["POST"])
def create_reservation_route():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "No data received"}), 400

        # Extract fields
        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")
        party_size_str = data.get("party_size")
        date_str = data.get("date")
        time = data.get("time")
        notes = data.get("notes", "")

        # Validate required fields
        if not all([name, email, phone, party_size_str, date_str, time]):
            return jsonify({"success": False, "message": "Missing required fields"}), 400

        # Convert party_size to int
        try:
            party_size = int(party_size_str)
        except ValueError:
            return jsonify({"success": False, "message": "Party size must be a number"}), 400

        # Convert date string to datetime.date
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"success": False, "message": "Invalid date format"}), 400

        # Insert into MongoDB
        result = create_reservation(name, email, phone, party_size, date_obj, time, notes)

        return jsonify({"success": True, "message": "Reservation created", "id": str(result.inserted_id)})

    except Exception as e:
        print("Error creating reservation:", e)
        return jsonify({"success": False, "message": str(e)}), 500