from datetime import datetime
from bson.objectid import ObjectId
import backend.db as db_module
from .db import get_db # always use module access

# ------------ USERS COLLECTION ------------
def create_user(username, email, password, role="customer"):
    user = {
        "username": username,
        "email": email,
        "password": password,
        "role": role,
        "created_at": datetime.utcnow()
    }
    return db_module.db["users"].insert_one(user)


def get_user_by_email(email):
    return db_module.db["users"].find_one({"email": email})


def get_user_by_id(user_id):
    return db_module.db["users"].find_one({"_id": ObjectId(user_id)})

def get_all_users():
    """Return a list of all users"""
    return list(db_module.db["users"].find())    


# ------------ MENU COLLECTION ------------
def create_menu_item(name, description, price, category, image=None, available=True):
    db = get_db()
    item = {
        "name": name,
        "description": description,
        "price": price,
        "category": category,
        "image": image,
        "available": available
    }
    result = db["menu"].insert_one(item)
    print("Inserted menu item ID:", result.inserted_id)
    return result


def get_all_menu():
    return list(db_module.db["menu"].find())


def get_menu_item(menu_id):
    return db_module.db["menu"].find_one({"_id": ObjectId(menu_id)})


# ------------ ORDERS COLLECTION ------------
def create_order(user_id, items, total_price):
    db = db_module.get_db()

    if user_id:
        user = db["users"].find_one({"_id": ObjectId(user_id)})
        customer_name = user.get("username", "Guest")
    else:
        customer_name = "Guest"

    order = {
        "user_id": ObjectId(user_id) if user_id else None,
        "customer_name": customer_name,
        "items": items,
        "total": total_price,
        "status": "Pending",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    return db["orders"].insert_one(order)

def get_user_orders(user_id):
    return list(db_module.db["orders"].find({"user_id": ObjectId(user_id)}))


# ------------ REVIEWS COLLECTION ------------
def add_review(user_id, menu_id, rating, comment):
    review = {
        "user_id": ObjectId(user_id),
        "menu_id": ObjectId(menu_id),
        "rating": rating,
        "comment": comment,
        "created_at": datetime.utcnow()
    }
    return db_module.db["reviews"].insert_one(review)


# ------------ RESERVATIONS COLLECTION ------------
def create_reservation(name, email, phone, party_size, date, time, notes=""):

    date_dt = datetime.combine(date, datetime.min.time())

    reservation = {
        "name": name,
        "email": email,
        "phone": phone,
        "party_size": int(party_size),
        "date": date_dt,       # datetime.date object
        "time": time,
        "notes": notes,
        "created_at": datetime.utcnow()
    }
    return db_module.db["reservations"].insert_one(reservation)


def get_reservations_for_date(date):
    return list(db_module.db["reservations"].find({"date": date}))


def get_all_reservations():
    return list(db_module.db["reservations"].find())