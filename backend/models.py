from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="customer")  # admin / customer
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    orders = db.relationship("Order", backref="user", lazy=True)
    reviews = db.relationship("Review", backref="user", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"



class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50))   # optional (pizza, drinks, etc.)
    image = db.Column(db.String(300))    # image path
    available = db.Column(db.Boolean, default=True)

    order_items = db.relationship("OrderItem", backref="menu", lazy=True)

    def __repr__(self):
        return f"<Menu {self.name}>"

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    total_price = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default="pending")   # pending, preparing, delivered
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship("OrderItem", backref="order", lazy=True)

    def __repr__(self):
        return f"<Order {self.id}>"


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    menu_id = db.Column(db.Integer, db.ForeignKey("menu.id"), nullable=False)

    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Float, nullable=False)  # price at the time of order

    def __repr__(self):
        return f"<OrderItem order={self.order_id} menu={self.menu_id}>"



class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    menu_id = db.Column(db.Integer, db.ForeignKey("menu.id"), nullable=True)
    
    rating = db.Column(db.Integer, nullable=False)  # 1–5
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Review {self.id}>"                            