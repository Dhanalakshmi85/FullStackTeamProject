from flask import Blueprint, render_template, session, redirect, request
from bson.objectid import ObjectId
from .models import (
    get_user_by_id, get_all_users, create_menu_item, get_all_menu,
    get_menu_item, create_order, get_user_orders, add_review
)

from .db import get_db

admin_bp = Blueprint("admin_bp", __name__, url_prefix="/admin")

# ------------- Helper: Admin Access Only -------------
def admin_required():
    if session.get("role") != "admin":
        return False
    return True

# ------------- ADMIN DASHBOARD -------------
@admin_bp.route("/")
def admin_dashboard():
    if not admin_required():
        return redirect("/login")

    db = get_db()
    total_users = db["users"].count_documents({})
    total_orders = db["orders"].count_documents({})
    total_menu_items = db["menu"].count_documents({})
    total_reviews = db["reviews"].count_documents({})

    return render_template(
        "admin-panel/dashboard.html",
        users=total_users,
        orders=total_orders,
        menu=total_menu_items,
        reviews=total_reviews
    )

# ------------- USERS MANAGEMENT -------------
@admin_bp.route("/users")
def admin_users():
    if not admin_required():
        return redirect("/login")

    users = list(get_db()["users"].find())
    return render_template("admin-panel/users.html", users=users)

@admin_bp.route("/users/delete/<user_id>")
def delete_user(user_id):
    if not admin_required():
        return redirect("/login")

    db = get_db()
    db["users"].delete_one({"_id": ObjectId(user_id)})

    return redirect("/admin/users")
 

# ------------- MENU MANAGEMENT -------------
@admin_bp.route("/menu")
def admin_menu():
    if not admin_required():
        return redirect("/login")

    menu_items = list(get_db()["menu"].find())
    return render_template("admin-panel/menu-items.html", menu=menu_items)

@admin_bp.route("/menu/add", methods=["POST"])
def add_menu_item_route():
    if not admin_required():
        return redirect("/login")

    name = request.form["name"]
    description = request.form["description"]
    price = float(request.form["price"])
    image_url = request.form.get("image_url", "")

    create_menu_item(name, description, price, category="general", image=image_url)

    return redirect("/admin/menu")

@admin_bp.route("/menu/update/<menu_id>", methods=["POST"])
def update_menu_item(menu_id):
    if not admin_required():
        return redirect("/login")

    db = get_db()
    item = db["menu"].find_one({"_id": ObjectId(menu_id)})

    if not item:
        return "Menu item not found", 404

    db["menu"].update_one(
        {"_id": ObjectId(menu_id)},
        {"$set": {
            "name": request.form["name"],
            "description": request.form["description"],
            "price": float(request.form["price"]),
            "image": request.form.get("image_url", "")
        }}
    )

    return redirect("/admin/menu")

@admin_bp.route("/menu/delete/<menu_id>", methods=["POST"])
def delete_menu_item(menu_id):
    if not admin_required():
        return redirect("/login")

    db = get_db()
    db["menu"].delete_one({"_id": ObjectId(menu_id)})

    return redirect("/admin/menu")

# ------------- ORDERS MANAGEMENT -------------
@admin_bp.route("/orders")
def admin_orders():
    if not admin_required():
        return redirect("/login")

    orders = list(get_db()["orders"].find())
    return render_template("admin-panel/orders.html", orders=orders)


@admin_bp.route("/orders/update/<order_id>", methods=["POST"])
def update_order_status(order_id):
    if not admin_required():
        return redirect("/login")

    new_status = request.form.get("status")

    db = get_db()
    db["orders"].update_one(
        {"_id": ObjectId(order_id)},
        {"$set": {"status": new_status}}
    )

    return redirect("/admin/orders")

# ------------- REVIEWS MANAGEMENT -------------
@admin_bp.route("/reviews")
def admin_reviews():
    if not admin_required():
        return redirect("/login")

    reviews = list(get_db()["reviews"].find())
    return render_template("admin-panel/review.html", reviews=reviews)



# from flask import Blueprint, render_template, request, jsonify, session
# from datetime import datetime
# from bson.objectid import ObjectId
# from backend.db import get_db
# from backend.models import create_reservation

# main = Blueprint("main", __name__)

# # ------------------- Static Pages -------------------

# @main.route("/", methods=["GET"])
# def home():
#     return render_template("home.html", title="Home Page")


# @main.route("/contact", methods=["GET"])
# def contact():
#     return render_template("contact.html", title="Contact Page")


# @main.route("/cart", methods=["GET"])
# def cart():
#     return render_template("cart.html")   


# @main.route("/signup")
# def signup():
#     return render_template("signup.html")    


# # ------------------- Menu Route -------------------

# @main.route("/menu/")
# def menu():
    
#     db = get_db() 
#     menu_collection = db["menu"]

#     # Query items by category
#     north_indian_items = list(menu_collection.find({"category": "north_indian"}))
#     south_indian_items = list(menu_collection.find({"category": "south_indian"}))
#     sri_lankan_items = list(menu_collection.find({"category": "sri_lankan"}))

#     # Convert ObjectId to string
#     for item in north_indian_items + south_indian_items + sri_lankan_items:
#         item["_id"] = str(item["_id"])

#     return render_template(
#         "menu.html",
#         north_indian_items=north_indian_items,
#         south_indian_items=south_indian_items,
#         sri_lankan_items=sri_lankan_items
#     )


# # ------------------- Place Order -------------------

# @main.route("/place-order", methods=["GET","POST"])
# def place_order():
#     data = request.get_json()
#     cart = data.get("cart", [])

#     if not cart:
#         return jsonify({"success": False, "message": "Cart empty"})

#     db = get_db()
#     items = [{"name": c["name"], "qty": c["qty"], "price": c["price"]} for c in cart]
#     total = sum(c["price"] * c["qty"] for c in cart)

#     user_id = session.get("user_id")
#     customer_name = "Guest"

#     if user_id:
#         user = db["users"].find_one({"_id": ObjectId(user_id)})
#         if user:
#             customer_name = user.get("username") or user.get("name") or "Guest"

#     order_doc = {
#         "customer_name": session.get("username", customer_name),
#         "items": items,
#         "total": total,
#         "status": "Pending",
#         "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     }

#     db["orders"].insert_one(order_doc)

#     return jsonify({"success": True})


# # ------------------- Reservation Pages -------------------

# @main.route("/reservation", methods=["GET"])
# def reservation_page():
#     return render_template("reservation.html")


# @main.route("/create-reservation", methods=["POST"])
# def create_reservation_route():
#     try:
#         data = request.get_json()
#         if not data:
#             return jsonify({"success": False, "message": "No data received"}), 400

#         # Extract fields
#         name = data.get("name")
#         email = data.get("email")
#         phone = data.get("phone")
#         party_size_str = data.get("party_size")
#         date_str = data.get("date")
#         time = data.get("time")
#         notes = data.get("notes", "")

#         # Validate required fields
#         if not all([name, email, phone, party_size_str, date_str, time]):
#             return jsonify({"success": False, "message": "Missing required fields"}), 400

#         # Convert party_size to int
#         try:
#             party_size = int(party_size_str)
#         except ValueError:
#             return jsonify({"success": False, "message": "Party size must be a number"}), 400

#         # Convert date string to datetime.date
#         try:
#             date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
#         except ValueError:
#             return jsonify({"success": False, "message": "Invalid date format"}), 400

#         # Insert into MongoDB using your model function
#         result = create_reservation(name, email, phone, party_size, date_obj, time, notes)

#         return jsonify({"success": True, "message": "Reservation created", "id": str(result.inserted_id)})

#     except Exception as e:
#         print("Error creating reservation:", e)
#         return jsonify({"success": False, "message": str(e)}), 500
