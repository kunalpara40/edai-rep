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

# Optional: tighten session cookie settings in production
# app.config.update(
#     SESSION_COOKIE_HTTPONLY=True,
#     SESSION_COOKIE_SAMESITE='Lax',
#     SESSION_COOKIE_SECURE=True  # only when using HTTPS
# )

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
    data = request.get_json() or {}
    required = ["firstName", "lastName", "email", "password"]
    for r in required:
        if not data.get(r):
            return jsonify({"error": f"{r} is required"}), 400

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        # quick check if email already exists
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id FROM users WHERE email = %s", (data["email"],))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({"error": "Email already registered"}), 409
        cursor.close()

        # insert new user (hashed password)
        hashed_pw = generate_password_hash(data["password"])
        insert_sql = """
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

        cursor = conn.cursor()
        cursor.execute(insert_sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "User created successfully!"}), 201

    except mysql.connector.IntegrityError:
        # Unique constraint triggered (defensive)
        if conn:
            try:
                conn.rollback()
            except:
                pass
        return jsonify({"error": "Email already registered"}), 409
    except Exception as e:
        if conn:
            try:
                conn.rollback()
            except:
                pass
        return jsonify({"error": "Server error", "details": str(e)}), 500
    finally:
        try:
            if cursor:
                cursor.close()
        except:
            pass
        try:
            if conn:
                conn.close()
        except:
            pass

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if not user:
            # email not found
            return jsonify({"error": "This email is not registered. Please sign up first."}), 404

        # check hashed password
        if not check_password_hash(user["password"], password):
            return jsonify({"error": "Incorrect password. Try again."}), 401

        # success
        session["user_id"] = user["id"]
        return jsonify({"message": "Login successful!"}), 200

    except Exception as e:
        if conn:
            try:
                conn.rollback()
            except:
                pass
        return jsonify({"error": "Server error", "details": str(e)}), 500
    finally:
        try:
            if cursor:
                cursor.close()
        except:
            pass
        try:
            if conn:
                conn.close()
        except:
            pass

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    return jsonify({"message": "Logged out"}), 200

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

if __name__ == "__main__":
    # Run on http://127.0.0.1:5000
    app.run(debug=True)
