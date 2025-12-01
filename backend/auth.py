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


from flask import Blueprint, render_template, request, redirect, session

auth = Blueprint("auth", __name__)

# TEMPORARY USERS FOR TESTING (remove when DB is ready)
FAKE_USERS = {
    "admin@example.com": {"password": "admin123", "role": "admin"},
    "customer@example.com": {"password": "cust123", "role": "customer"}
}

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = FAKE_USERS.get(email)

        if user and user["password"] == password:
            session["logged_in"] = True
            session["email"] = email
            session["role"] = user["role"]

            if user["role"] == "admin":
                return redirect("/admin")
            return redirect("/")

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


# LOGOUT
@auth.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# FORCE ADMIN — FOR TESTING WITHOUT LOGIN PAGE
@auth.route("/force-admin")
def force_admin():
    session["logged_in"] = True
    session["role"] = "admin"
    session["email"] = "forced-admin@example.com"
    return redirect("/admin")



