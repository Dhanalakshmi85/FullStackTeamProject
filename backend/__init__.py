from flask import Flask
from pathlib import Path
from .routes import main  
from .admin import admin_bp
from .auth import auth
from backend.db import init_db
from .today_menu import today_menu

from dotenv import load_dotenv
import os


BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / "frontend" / "templates"
STATIC_DIR = BASE_DIR / "frontend" / "static"

# Load .env variables
load_dotenv()


def create_app():
    app = Flask(
        __name__,
        template_folder=str(TEMPLATE_DIR),
        static_folder=str(STATIC_DIR)
    )

    app.config["SECRET_KEY"] = "my_super_secret_key_123"

    # Read the DB URI from the .env file
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise Exception("MONGO_URI missing in .env")

    init_db(mongo_uri)

    app.register_blueprint(admin_bp)
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(today_menu)

    return app
