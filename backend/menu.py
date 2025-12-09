import os
import json

def load_menu(category):
    base_path = os.path.join("frontend", "static", "img")
    category_path = os.path.join(base_path, category)

    items = []

    for file in os.listdir(category_path):
        if file.lower().endswith((".png", ".jpg", ".jpeg")):
            name = os.path.splitext(file)[0].replace("_", " ").title()

            items.append({
                "name": name,
                "image": f"/static/img/{category}/{file}",
                "price": 10.00  
            })

    return items