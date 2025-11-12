

# from flask import Flask, request, jsonify, render_template, session, redirect, url_for
# from werkzeug.security import generate_password_hash, check_password_hash
# from dotenv import load_dotenv
# import os
# import mysql.connector
# from mysql.connector import Error
# from flask_cors import CORS

# load_dotenv()

# app = Flask(__name__, template_folder="templates", static_folder="static")
# app.secret_key = os.getenv("SECRET_KEY", "dev_secret_change_in_production")
# CORS(app, supports_credentials=True)

# def get_db_connection():
#     return mysql.connector.connect(
#         host=os.getenv("DB_HOST", "localhost"),
#         user=os.getenv("DB_USER", "root"),
#         password=os.getenv("DB_PASSWORD", ""),
#         database=os.getenv("DB_NAME", "swiftride"),
#         autocommit=False
#     )

# # MAIN ROUTE - Renders homepage with authentication state
# @app.route("/")
# def index():
#     # Session is automatically available in Jinja templates
#     # If user is logged in, session['user_id'] will be set
#     return render_template("index.html")

# # SIGNUP ENDPOINT
# @app.route("/signup", methods=["POST"])
# def signup():
#     data = request.get_json()
#     required = ["firstName", "lastName", "email", "password"]
#     for r in required:
#         if not data.get(r):
#             return jsonify({"error": f"{r} is required"}), 400

#     hashed_pw = generate_password_hash(data["password"])

#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         sql = """
#         INSERT INTO users
#         (firstName, lastName, email, phone, password, address, state, city, zipCode, preferredPayment)
#         VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
#         """
#         values = (
#             data.get("firstName"),
#             data.get("lastName"),
#             data.get("email"),
#             data.get("phone"),
#             hashed_pw,
#             data.get("address", ""),
#             data.get("state", ""),
#             data.get("city", ""),
#             data.get("zipCode", ""),
#             data.get("preferredPayment", "")
#         )
#         cursor.execute(sql, values)
#         conn.commit()
#         cursor.close()
#         conn.close()
#         return jsonify({"message": "User created successfully!"}), 201
#     except mysql.connector.IntegrityError:
#         return jsonify({"error": "Email already registered"}), 409
#     except Exception as e:
#         print(f"Signup error: {e}")
#         return jsonify({"error": "Server error", "details": str(e)}), 500

# # LOGIN ENDPOINT
# @app.route("/login", methods=["POST"])
# def login():
#     data = request.get_json()
#     if not data.get("email") or not data.get("password"):
#         return jsonify({"error": "Email and password required"}), 400

#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("SELECT * FROM users WHERE email = %s", (data.get("email"),))
#         user = cursor.fetchone()
#         cursor.close()
#         conn.close()

#         if user and check_password_hash(user["password"], data.get("password")):
#             # Set session data
#             session["user_id"] = user["id"]
#             session["firstName"] = user.get("firstName", "")
#             session["email"] = user.get("email", "")
            
#             return jsonify({
#                 "message": "Login successful!",
#                 "user": {
#                     "id": user["id"],
#                     "firstName": user.get("firstName"),
#                     "email": user.get("email")
#                 }
#             }), 200
#         else:
#             return jsonify({"error": "Invalid email or password"}), 401
#     except Exception as e:
#         print(f"Login error: {e}")
#         return jsonify({"error": "Server error", "details": str(e)}), 500

# # LOGOUT ENDPOINT
# @app.route("/logout", methods=["POST"])
# def logout():
#     session.clear()
#     return jsonify({"message": "Logged out successfully"}), 200

# # GET CURRENT USER INFO
# @app.route("/me")
# def me():
#     user_id = session.get("user_id")
#     if not user_id:
#         return jsonify({"error": "Not logged in"}), 401
    
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("""
#             SELECT id, firstName, lastName, email, phone, address, state, city, zipCode, preferredPayment 
#             FROM users WHERE id=%s
#         """, (user_id,))
#         user = cursor.fetchone()
#         cursor.close()
#         conn.close()
        
#         if not user:
#             return jsonify({"error": "User not found"}), 404
#         return jsonify({"user": user}), 200
#     except Exception as e:
#         print(f"Get user error: {e}")
#         return jsonify({"error": "Server error", "details": str(e)}), 500

# # UPDATE PROFILE
# @app.route("/update_profile", methods=["PUT"])
# def update_profile():
#     user_id = session.get("user_id")
#     if not user_id:
#         return jsonify({"error": "Not logged in"}), 401

#     data = request.get_json()
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         sql = """
#         UPDATE users 
#         SET phone=%s, address=%s, state=%s, city=%s, zipCode=%s, preferredPayment=%s
#         WHERE id=%s
#         """
#         values = (
#             data.get("phone"),
#             data.get("address"),
#             data.get("state"),
#             data.get("city"),
#             data.get("zipCode"),
#             data.get("preferredPayment"),
#             user_id
#         )
#         cursor.execute(sql, values)
#         conn.commit()
#         cursor.close()
#         conn.close()
#         return jsonify({"message": "Profile updated successfully"}), 200
#     except Exception as e:
#         print(f"Update profile error: {e}")
#         return jsonify({"error": "Update failed", "details": str(e)}), 500

# # DELETE ACCOUNT
# @app.route("/delete_account", methods=["DELETE"])
# def delete_account():
#     user_id = session.get("user_id")
#     if not user_id:
#         return jsonify({"error": "Not logged in"}), 401

#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
#         conn.commit()
#         cursor.close()
#         conn.close()
#         session.clear()
#         return jsonify({"message": "Account deleted successfully"}), 200
#     except Exception as e:
#         print(f"Delete account error: {e}")
#         return jsonify({"error": "Delete failed", "details": str(e)}), 500

# # LIST ALL USERS (Admin functionality)
# @app.route("/users", methods=["GET"])
# def list_users():
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("SELECT id, firstName, lastName, email, state, city, preferredPayment FROM users")
#         users = cursor.fetchall()
#         cursor.close()
#         conn.close()
#         return jsonify({"users": users}), 200
#     except Exception as e:
#         print(f"List users error: {e}")
#         return jsonify({"error": "Failed to fetch users", "details": str(e)}), 500

# # SEARCH USER BY EMAIL/CITY
# @app.route("/search_user", methods=["GET"])
# def search_user():
#     email = request.args.get("email")
#     city = request.args.get("city")

#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor(dictionary=True)

#         if email:
#             cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
#         elif city:
#             cursor.execute("SELECT * FROM users WHERE city=%s", (city,))
#         else:
#             return jsonify({"error": "Provide email or city as query parameter"}), 400

#         result = cursor.fetchall()
#         cursor.close()
#         conn.close()

#         if not result:
#             return jsonify({"message": "No user found"}), 404
#         return jsonify({"users": result}), 200
#     except Exception as e:
#         print(f"Search user error: {e}")
#         return jsonify({"error": "Search failed", "details": str(e)}), 500

# # PASSWORD RESET
# @app.route("/reset_password", methods=["PUT"])
# def reset_password():
#     user_id = session.get("user_id")
#     if not user_id:
#         return jsonify({"error": "Not logged in"}), 401

#     data = request.get_json()
#     new_password = data.get("newPassword")
#     if not new_password:
#         return jsonify({"error": "New password required"}), 400

#     hashed_pw = generate_password_hash(new_password)

#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute("UPDATE users SET password=%s WHERE id=%s", (hashed_pw, user_id))
#         conn.commit()
#         cursor.close()
#         conn.close()
#         return jsonify({"message": "Password updated successfully"}), 200
#     except Exception as e:
#         print(f"Reset password error: {e}")
#         return jsonify({"error": "Password reset failed", "details": str(e)}), 500

# # CREATE RIDE (Authenticated users only)
# @app.route("/create_ride", methods=["POST"])
# def create_ride():
#     user_id = session.get("user_id")
#     if not user_id:
#         return jsonify({"error": "Not logged in"}), 401

#     data = request.get_json() or {}
#     required = ["pickup_lat", "pickup_lng", "drop_lat", "drop_lng"]
#     for r in required:
#         if r not in data:
#             return jsonify({"error": f"{r} is required"}), 400

#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         sql = """
#         INSERT INTO rides (user_id, pickup_lat, pickup_lng, drop_lat, drop_lng, status, requested_at)
#         VALUES (%s, %s, %s, %s, %s, 'requested', NOW())
#         """
#         cursor.execute(sql, (user_id, data["pickup_lat"], data["pickup_lng"], 
#                             data["drop_lat"], data["drop_lng"]))
#         conn.commit()
#         ride_id = cursor.lastrowid
#         cursor.close()
#         conn.close()
#         return jsonify({"message": "Ride requested", "ride_id": ride_id}), 201
#     except Exception as e:
#         print(f"Create ride error: {e}")
#         return jsonify({"error": "Create ride failed", "details": str(e)}), 500

# # ASSIGN DRIVER (Transactional)
# @app.route("/assign_driver", methods=["POST"])
# def assign_driver():
#     data = request.get_json() or {}
#     ride_id = data.get("ride_id")
#     if not ride_id:
#         return jsonify({"error": "ride_id required"}), 400

#     conn = None
#     cursor = None
#     try:
#         conn = get_db_connection()
#         conn.start_transaction()
#         cursor = conn.cursor()

#         cursor.execute("SELECT driver_id FROM drivers WHERE status='available' LIMIT 1 FOR UPDATE")
#         row = cursor.fetchone()
#         if not row:
#             conn.rollback()
#             return jsonify({"error": "No available drivers right now"}), 409

#         driver_id = row[0]

#         cursor.execute("""
#             UPDATE rides
#             SET driver_id=%s, status='assigned', assigned_at=NOW()
#             WHERE ride_id=%s AND status='requested'
#         """, (driver_id, ride_id))

#         if cursor.rowcount == 0:
#             conn.rollback()
#             return jsonify({"error": "Ride not in requested state or not found"}), 409

#         cursor.execute("UPDATE drivers SET status='busy', updated_at=NOW() WHERE driver_id=%s", (driver_id,))

#         conn.commit()
#         return jsonify({"message": "Driver assigned", "driver_id": driver_id, "ride_id": ride_id}), 200
#     except Exception as e:
#         if conn:
#             conn.rollback()
#         print(f"Assign driver error: {e}")
#         return jsonify({"error": "Assignment failed", "details": str(e)}), 500
#     finally:
#         if cursor:
#             cursor.close()
#         if conn:
#             conn.close()

# if __name__ == "__main__":
#     app.run(debug=True)
