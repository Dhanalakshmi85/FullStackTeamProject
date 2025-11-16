from flask import Blueprint, render_template

main = Blueprint("main", __name__)

@main.route("/", methods=["GET"])

def home():
    return render_template("home.html", title="Home Page")