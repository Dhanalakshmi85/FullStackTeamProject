from flask import Flask
from pathlib import Path
from .routes import main  
from .admin import admin_bp
from .auth import auth
from .models import db

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / "frontend" / "templates"
STATIC_DIR = BASE_DIR / "frontend" / "static"


def create_app():
    app = Flask(
        __name__,
        template_folder=str(TEMPLATE_DIR),
        static_folder=str(STATIC_DIR)
    )

    app.config["SECRET_KEY"] = "my_super_secret_key_123"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    app.register_blueprint(admin_bp)
    app.register_blueprint(main) 
    app.register_blueprint(auth)


    return app