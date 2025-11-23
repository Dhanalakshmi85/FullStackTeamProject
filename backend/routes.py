from flask import Blueprint, render_template

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