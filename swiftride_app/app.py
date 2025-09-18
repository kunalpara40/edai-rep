# app.py
from flask import Flask, request, jsonify, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
import mysql.connector
from mysql.connector import Error
from flask_cors import CORS

load_dotenv()

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.getenv("SECRET_KEY", "dev_secret")
CORS(app)  # safe for dev. For production restrict origins.

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "swiftride"),
        autocommit=False
    )

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    required = ["firstName", "lastName", "email", "password"]
    for r in required:
        if not data.get(r):
            return jsonify({"error": f"{r} is required"}), 400

    hashed_pw = generate_password_hash(data["password"])

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
        INSERT INTO users
        (firstName, lastName, email, phone, password, address, city, zipCode, preferredPayment)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        values = (
            data.get("firstName"),
            data.get("lastName"),
            data.get("email"),
            data.get("phone"),
            hashed_pw,
            data.get("address"),
            data.get("city"),
            data.get("zipCode"),
            data.get("preferredPayment")
        )
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "User created successfully!"}), 201
    except mysql.connector.IntegrityError as ie:  # likely duplicate email
        return jsonify({"error": "Email already registered"}), 409
    except Exception as e:
        # log e in real apps
        return jsonify({"error": "Server error", "details": str(e)}), 500

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email and password required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (data.get("email"),))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user["password"], data.get("password")):
            session["user_id"] = user["id"]
            return jsonify({"message": "Login successful!"})
        else:
            return jsonify({"error": "Invalid email or password"}), 401
    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500

@app.route("/me")
def me():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, firstName, lastName, email, phone, address, city, zipCode, preferredPayment FROM users WHERE id=%s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify({"user": user})
    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500
    
 #USER PROFILE   
@app.route("/update_profile", methods=["PUT"])
def update_profile():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
        UPDATE users 
        SET phone=%s, address=%s, city=%s, zipCode=%s, preferredPayment=%s
        WHERE id=%s
        """
        values = (
            data.get("phone"),
            data.get("address"),
            data.get("city"),
            data.get("zipCode"),
            data.get("preferredPayment"),
            user_id
        )
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Profile updated successfully"})
    except Exception as e:
        return jsonify({"error": "Update failed", "details": str(e)}), 500
    

 #FOR DELETING ACCOUNT   
@app.route("/delete_account", methods=["DELETE"])
def delete_account():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
        session.clear()
        return jsonify({"message": "Account deleted successfully"})
    except Exception as e:
        return jsonify({"error": "Delete failed", "details": str(e)}), 500

#LOGOUT
@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"})

#List All Users
@app.route("/users", methods=["GET"])
def list_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, firstName, lastName, email, city, preferredPayment FROM users")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({"users": users})
    except Exception as e:
        return jsonify({"error": "Failed to fetch users", "details": str(e)}), 500

#SEARCH USER BY EMAIL/CITY
@app.route("/search_user", methods=["GET"])
def search_user():
    email = request.args.get("email")
    city = request.args.get("city")

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if email:
            cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        elif city:
            cursor.execute("SELECT * FROM users WHERE city=%s", (city,))
        else:
            return jsonify({"error": "Provide email or city as query parameter"}), 400

        result = cursor.fetchall()
        cursor.close()
        conn.close()

        if not result:
            return jsonify({"message": "No user found"})
        return jsonify({"users": result})
    except Exception as e:
        return jsonify({"error": "Search failed", "details": str(e)}), 500
    
#PASSWORD RESET 
@app.route("/reset_password", methods=["PUT"])
def reset_password():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json()
    new_password = data.get("newPassword")
    if not new_password:
        return jsonify({"error": "New password required"}), 400

    hashed_pw = generate_password_hash(new_password)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET password=%s WHERE id=%s", (hashed_pw, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Password updated successfully"})
    except Exception as e:
        return jsonify({"error": "Password reset failed", "details": str(e)}), 500



if __name__ == "__main__":
    # Run on http://127.0.0.1:5000
    app.run(debug=True)
