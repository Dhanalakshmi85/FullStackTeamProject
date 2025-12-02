# from flask import request, jsonify
# from datetime import datetime, timedelta, timezone
# import os
# import jwt
# from models import User
# from schemas import UserSchema

# def post_login():
#     """
#     Handle user login and return JWT token if credentials are correct.
#     """
#     try:
#         data = request.get_json() or {}
#         username = data.get("username")
#         password = data.get("password")

#         # Validate input
#         if not username or not password:
#             return jsonify({"message": "Username and password are required"}), 400

#         # Verify credentials
#         user = User.verify_credentials(username, password)  # bcrypt internally
#         if not user:
#             return jsonify({"message": "Invalid credentials"}), 401

#         # Get JWT secret from environment
#         jwt_secret = os.getenv("JWT_SECRET_KEY")
#         if not jwt_secret:
#             # Do NOT use fallback secret in production
#             return jsonify({"message": "Server configuration error"}), 500

#         # Create JWT payload with expiration (24 hours)
#         payload = {
#             "user_id": str(user.id),
#             "username": user.username,
#             "exp": int((datetime.now(timezone.utc) + timedelta(hours=24)).timestamp())
#         }

#         # Encode token
#         token = jwt.encode(payload, jwt_secret, algorithm="HS256")

#         # Return user data and token
#         return jsonify({
#             "message": "Login successful",
#             "user": UserSchema().dump(user),
#             "token": token
#         }), 200

#     except Exception as e:
#         # Log exception in real app, do not expose details in production
#         return jsonify({"message": "Internal server error"}), 500


# @auth.route("/force-admin")
# def force_admin():
#     session["logged_in"] = True
#     session["role"] = "admin"
#     session["email"] = "test-admin@example.com"
#     return redirect("/admin")


from flask import Blueprint, render_template, request, redirect, session, url_for
from backend.models import get_user_by_email
from werkzeug.security import check_password_hash

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

        # if not user:
        #     return render_template("login.html", error="User not found")

        # # Use Werkzeug check_password_hash (works with your stored scrypt hashes)
        # if not check_password_hash(user["password"], password):
        #     return render_template("login.html", error="Incorrect password")

        # Save session
        session["logged_in"] = True
        session["email"] = user["email"]
        session["role"] = user["role"]
        session["user_id"] = str(user["_id"])
        print("DEBUG: session:", dict(session))

        print("DEBUG: check_password_hash result:", check_password_hash(user["password"], password))
        # Redirect based on role
        if user["role"].lower() == "admin":
            print("DEBUG: redirecting to admin dashboard")
            return redirect("/admin/dashboard")  # or url_for('admin_bp.dashboard') if defined
        else:
            print("DEBUG: redirecting to customer home")
            return redirect(url_for("main.home"))  # safe redirect to home page

    # GET request → show login page
    return render_template("login.html")


# # LOGOUT
# @auth.route("/logout")
# def logout():
#     session.clear()
#     return redirect("/login")


# FORCE ADMIN — FOR TESTING WITHOUT LOGIN PAGE
# @auth.route("/force-admin")
# def force_admin():
#     session["logged_in"] = True
#     session["role"] = "admin"
#     session["email"] = "forced-admin@example.com"
#     return redirect("/admin")



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

