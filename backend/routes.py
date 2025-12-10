from flask import Blueprint, render_template

# Create Blueprint
main = Blueprint("main", __name__)

# ---------------- PAGES ---------------- #

@main.route("/")
def home():
    return render_template("home.html", title="Home Page")

@main.route("/menu")
def menu():
    return render_template("menu.html", title="Menu Page")

@main.route("/contact")
def contact():
    return render_template("contact.html", title="Contact Page")

@main.route("/cart")
def cart():
    return render_template("cart.html", title="Cart")

@main.route("/reservation")
def reservation():
    return render_template("reservation.html", title="Reservation")

@main.route("/signup")
def signup():
    return render_template("signup.html", title="Signup Page")

# ------------- TODAY’S MENU ROUTE ------------- #

@main.route("/todaymenu")
def todaymenu():
    items = [
        {"name": "Idli Sambar",     "price": 4.50, "desc": "Soft idli with hot sambar.",                "image": "img/idli.jpeg"},
        {"name": "Masala Dosa",     "price": 6.00, "desc": "Crispy dosa with masala fill.",             "image": "img/dosa.jpeg"},
        {"name": "Chicken Biryani", "price": 8.50, "desc": "Aromatic biryani served with raita.",       "image": "img/biryani.jpg"},
        {"name": "Parotta + Salna", "price": 7.00, "desc": "Layered parotta served with spicy salna.",  "image": "img/parotta.jpg"},
    ]
    return render_template("todaymenu.html", title="Today's Menu", items=items)
