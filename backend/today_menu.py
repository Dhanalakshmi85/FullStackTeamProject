from flask import Blueprint, render_template


today_menu = Blueprint("today_menu", __name__, url_prefix="/today_menu")

TODAY_SPECIAL = [
    {
        "name": "Palak Paneer",
        "price": 10,
        "image": "img/palak.jpeg",
        "desc": "Fresh spinach cooked with soft cottage cheese."
    },
    {
        "name": "Dosa",
        "price": 10,
        "image": "img/dosa.jpeg",
        "desc": "Crispy dosa with sambar and chutney."
    },
    {
        "name": "Full Rice Dish",
        "price": 10,
        "image": "img/full-dish-sri.jpeg",
        "desc": "Rice served with Sri Lankan curries."
    }
]

@today_menu.route("/today_menu")
def today_menu_page():
    return render_template("today_menu.html", items=TODAY_SPECIAL)
      
