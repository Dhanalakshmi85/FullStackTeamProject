from flask import Blueprint, render_template, session, redirect, request, url_for
from bson.objectid import ObjectId
from .models import (
    get_user_by_id, get_all_users, create_menu_item, get_all_menu,
    get_menu_item, create_order, get_user_orders, add_review
)

from .db import get_db

admin_bp = Blueprint("admin_bp", __name__, url_prefix="/admin")


UPLOAD_FOLDER = "frontend/static/uploads"  # or wherever you want to store images
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

    recent_orders = list(
        db["orders"].find().sort("time", -1).limit(5)  # Adjust "time" field as needed
    )

    return render_template(
        "admin-panel/dashboard.html",
        users=total_users,
        orders=total_orders,
        menu=total_menu_items,
        reviews=total_reviews,
        recent_orders=recent_orders
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

@admin_bp.route("/users/edit/<user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    if not admin_required():
        return redirect("/login")

    db = get_db()
    user = db["users"].find_one({"_id": ObjectId(user_id)})


    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        role = request.form["role"]

        db["users"].update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {
                "username": username,
                "email": email,
                "role": role
            }}
        )

    if not user:
        return "User not found", 404

    return render_template("admin-panel/edit_user.html", user=user)    
 

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
    category = request.form["category"]

    # Grab the uploaded file
    image_file = request.files.get("image_file")
    if image_file and allowed_file(image_file.filename):
        filename = secure_filename(image_file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        image_file.save(filepath)
        image_url = f"/static/uploads/{filename}"  # store this in DB
    else:
        image_url = ""  # default if no file uploaded

    create_menu_item(name, description, price, category=category, image=image_url)

    return redirect("/admin/menu")

@admin_bp.route("/menu/edit/<menu_id>", methods=["GET", "POST"])
def edit_menu_item(menu_id):
    if not admin_required():
        return redirect("/login")

    db = get_db()
    item = db["menu"].find_one({"_id": ObjectId(menu_id)})

    if not item:
        return "Menu item not found", 404

    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        price = float(request.form.get("price"))
        category = request.form.get("category")

        image_file = request.files.get("image_file")
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            image_file.save(filepath)
            image_url = f"/static/uploads/{filename}"
        else:
            image_url = item.get("image", "")

        db["menu"].update_one(
            {"_id": ObjectId(menu_id)},
            {"$set": {
                "name": name,
                "description": description,
                "price": price,
                "category": category,
                "image": image_url
            }}
        )

        return redirect("/admin/menu")

    return render_template("admin-panel/edit-menu-item.html", item=item)


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

    orders = list(get_db()["orders"].find({
        "status": {"$nin": ["Completed", "Cancelled"]}
    }))
    return render_template("admin-panel/orders.html", orders=orders)


@admin_bp.route("/orders/update/<order_id>", methods=["POST"])
def update_order_status(order_id):
    if not admin_required():
        return redirect("/login")

    new_status = request.form.get("status")
    print("New status:", new_status)   # TEMPORARY DEBUG

    db = get_db()
    db["orders"].update_one(
        {"_id": ObjectId(order_id)},
        {"$set": {"status": new_status}}
    )

    return redirect("/admin/orders")

# ------------- REVIEWS MANAGEMENT -------------
@admin_bp.route("/reviews", methods=["GET", "POST"])
def admin_reviews():
    if not admin_required():
        return redirect("/login")

    db = get_db()

    if request.method == "POST":
        user_name = request.form.get("review-name")
        rating = int(request.form.get("review-rating"))
        comment = request.form.get("review-message")

        # Save to MongoDB
        db["reviews"].insert_one({
            "user_id": user_name,
            "comment": comment,
            "rating": rating
        })

        # Redirect to refresh the page
        return redirect("/admin/reviews")

    # GET → display reviews
    reviews = list(db["reviews"].find())
    return render_template("admin-panel/review.html", reviews=reviews)

@admin_bp.route("/reviews/delete/<review_id>", methods=["POST"])
def delete_review(review_id):
    if not admin_required():
        return redirect("/login")
    db = get_db()
    db["reviews"].delete_one({"_id": ObjectId(review_id)})
    return redirect(url_for("admin_bp.admin_reviews"))

# ------------- ADMIN LOGOUT -------------
@admin_bp.route("/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("main.home")) 

 
