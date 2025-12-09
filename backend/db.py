from pymongo import MongoClient

# Change this to your database URI
# client = MongoClient("mongodb://localhost:27017/")

# db = client["restaurant_db"]

# Collections (think of them like tables)


client = None
db = None


def init_db(uri):
    global db, client
    client = MongoClient(uri)
    db = client["restaurant_db"]

def get_db():
    global db
    if db is None:
        raise Exception("Database not initialized. Call init_db() first.")
    return db

# users_col = db["users"]
# menu_col = db["menu_items"]
# orders_col = db["orders"]
# cart_col = db["cart"]



