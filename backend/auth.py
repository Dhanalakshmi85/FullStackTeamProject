from flask import Blueprint, render_template, request, redirect, session, url_for
from backend.models import get_user_by_email, create_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__, url_prefix="/auth")

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        print("DEBUG: POST received")
        print("DEBUG: email:", email)

        user = get_user_by_email(email)
        print("DEBUG: user:", user)

        # Save session
        session["logged_in"] = True
        session["email"] = user["email"]
        session["role"] = user["role"]
        session["user_id"] = str(user["_id"])

        session["username"] = user.get("username")
        print("DEBUG: session:", dict(session))

        # print("DEBUG: check_password_hash result:", check_password_hash(user["password"], password))
        # Redirect based on role
        if user["role"].lower() == "admin":
            print("DEBUG: redirecting to admin dashboard")
            return redirect(url_for("admin_bp.admin_dashboard"))  # or url_for('admin_bp.dashboard') if defined
        else:
            print("DEBUG: redirecting to customer home")
            return redirect(url_for("main.home"))  # safe redirect to home page

    # GET request → show login page
    return render_template("login.html")


# LOGOUT
@auth.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        if password != confirm:
            return render_template("signup.html", error="Passwords do not match")

        # Check if email already exists
        if get_user_by_email(email):
            return render_template("signup.html", error="Email already registered")

        # Hash password
        hashed = generate_password_hash(password)

        create_user(name, email, hashed, role="customer")

        return redirect(url_for("auth.login"))

    return render_template("signup.html")

