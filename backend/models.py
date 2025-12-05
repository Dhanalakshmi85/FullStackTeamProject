# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime


# db = SQLAlchemy()
# class User(db.Model):
#     __tablename__ = "user"
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True)
#     password = db.Column(db.String(200), nullable=False)
#     role = db.Column(db.String(20), default="customer")  # admin / customer
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

#     orders = db.relationship("Order", backref="user", lazy=True)
#     reviews = db.relationship("Review", backref="user", lazy=True)

#     def __repr__(self):
#         return f"<User {self.username}>"



# class Menu(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(150), nullable=False)
#     description = db.Column(db.Text)
#     price = db.Column(db.Float, nullable=False)
#     category = db.Column(db.String(50))   # optional (pizza, drinks, etc.)
#     image = db.Column(db.String(300))    # image path
#     available = db.Column(db.Boolean, default=True)

#     order_items = db.relationship("OrderItem", backref="menu", lazy=True)

#     def __repr__(self):
#         return f"<Menu {self.name}>"

# class Order(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
#     total_price = db.Column(db.Float, default=0)
#     status = db.Column(db.String(20), default="pending")   # pending, preparing, delivered
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

#     items = db.relationship("OrderItem", backref="order", lazy=True)

#     def __repr__(self):
#         return f"<Order {self.id}>"


# class OrderItem(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
#     menu_id = db.Column(db.Integer, db.ForeignKey("menu.id"), nullable=False)

#     quantity = db.Column(db.Integer, default=1)
#     price = db.Column(db.Float, nullable=False)  # price at the time of order

#     def __repr__(self):
#         return f"<OrderItem order={self.order_id} menu={self.menu_id}>"



# class Review(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
#     menu_id = db.Column(db.Integer, db.ForeignKey("menu.id"), nullable=True)
    
#     rating = db.Column(db.Integer, nullable=False)  # 1–5
#     comment = db.Column(db.Text)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

#     def __repr__(self):
#         return f"<Review {self.id}>"     



from datetime import datetime
from bson.objectid import ObjectId
import backend.db as db_module  # always use module access

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


# ------------ MENU COLLECTION ------------
def create_menu_item(name, description, price, category, image=None, available=True):
    item = {
        "name": name,
        "description": description,
        "price": price,
        "category": category,
        "image": image,
        "available": available
    }
    return db_module.db["menu"].insert_one(item)


def get_all_menu():
    return list(db_module.db["menu"].find())


def get_menu_item(menu_id):
    return db_module.db["menu"].find_one({"_id": ObjectId(menu_id)})


# ------------ ORDERS COLLECTION ------------
def create_order(user_id, items, total_price):
    order = {
        "user_id": ObjectId(user_id),
        "items": items,
        "total_price": total_price,
        "status": "pending",
        "created_at": datetime.utcnow()
    }
    return db_module.db["orders"].insert_one(order)


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