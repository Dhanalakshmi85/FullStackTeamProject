from flask import Blueprint, render_template, session, redirect
from .models import User, Menu, Order, Review

admin_bp = Blueprint("admin_bp", __name__, url_prefix="/admin")

# ------------- Helper: Admin Access Only -------------
def admin_required():
    """Check if the user is admin"""
    if session.get("role") != "admin":
        return False
    return True

# ------------- ADMIN DASHBOARD -------------
@admin_bp.route("/")
def admin_dashboard():
    if not admin_required():
        return redirect("/login")

    total_users = User.query.count()
    total_orders = Order.query.count()
    total_menu_items = Menu.query.count()
    total_reviews = Review.query.count()

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

    users = User.query.all()
    return render_template("admin-panel/users.html", users=users)

@admin_bp.route("/admin/users/delete/<int:id>")
def delete_user(id):
    if not admin_required():
        return redirect("/login")

    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/admin/users")    

# ------------- MENU MANAGEMENT -------------
@admin_bp.route("/menu")
def admin_menu():
    if not admin_required():
        return redirect("/login")

    menu_items = Menu.query.all()
    return render_template("admin-panel/menu-items.html", menu=menu_items)


# ------------- ADD MENU ITEM -------------
@admin_bp.route("/admin/menu/add", methods=["POST"])
def add_menu_item():
    if not admin_required():
        return redirect("/login")

    name = request.form["name"]
    description = request.form["description"]
    price = float(request.form["price"])
    image_url = request.form["image_url"]

    new_item = Menu(name=name, description=description, price=price, image_url=image_url)
    db.session.add(new_item)
    db.session.commit()

    return redirect("/admin/menu")


# ------------- UPDATE MENU ITEM -------------

@admin_bp.route("/admin/menu/update/<int:id>", methods=["POST"])
def update_menu_item(id):
    if not admin_required():
        return redirect("/login")

    item = Menu.query.get(id)

    item.name = request.form["name"]
    item.description = request.form["description"]
    item.price = float(request.form["price"])
    item.image_url = request.form["image_url"]

    db.session.commit()
    return redirect("/admin/menu")


# ------------- DELETE MENU ITEM -------------


@admin_bp.route('/menu/delete/<int:id>', methods=['POST'])
def delete_menu_item(id):
    if not admin_required():
        return redirect("/login")

    item = Menu.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()

    return redirect('/admin/menu')



# ------------- ORDERS MANAGEMENT -------------
@admin_bp.route("/orders")
def admin_orders():
    if not admin_required():
        return redirect("/login")

    orders = Order.query.all()
    return render_template("admin-panel/orders.html", orders=orders)


# ------------- REVIEWS MANAGEMENT -------------
@admin_bp.route("/admin/review")
def admin_reviews():
    if not admin_required():
        return redirect("/login")

    reviews = Review.query.all()
    return render_template("admin-panel/review.html", reviews=reviews)


