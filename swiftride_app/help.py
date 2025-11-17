
from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from datetime import timedelta
import os
import mysql.connector
from flask_cors import CORS

load_dotenv()

# ----------- App config -----------
app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.getenv("SECRET_KEY", "dev_secret_change_in_production")
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

CORS(app, supports_credentials=True, origins=["http://localhost:5000", "http://127.0.0.1:5000"])

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "swiftride"),
        autocommit=False
    )

# upload config for driver license files
ALLOWED_EXT = {"png", "jpg", "jpeg", "pdf"}
UPLOAD_DIR = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT

# ==================== MAIN ROUTES ====================
@app.route("/")
def index():
    return render_template("index.html")

# ==================== USER AUTH ====================
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
        (firstName, lastName, email, phone, password, address, state, city, zipCode, preferredPayment)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        values = (
            data.get("firstName"),
            data.get("lastName"),
            data.get("email"),
            data.get("phone", ""),
            hashed_pw,
            data.get("address", ""),
            data.get("state", ""),
            data.get("city", ""),
            data.get("zipCode", ""),
            data.get("preferredPayment", "")
        )
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "User created successfully!"}), 201
    except mysql.connector.IntegrityError:
        return jsonify({"error": "Email already registered"}), 409
    except Exception as e:
        print(f"Signup error: {e}")
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

        if user:
            # Access user data correctly based on whether it's a dict or tuple
            user_password = user.get("password") if isinstance(user, dict) else user[4]  # password is at index 4
            user_id = user.get("id") if isinstance(user, dict) else user[0]  # id is at index 0
            first_name = user.get("firstName") if isinstance(user, dict) else user[1]  # firstName is at index 1
            email = user.get("email") if isinstance(user, dict) else user[3]  # email is at index 3
            
            if check_password_hash(str(user_password), str(data.get("password", ""))):
                session.clear()
                session["user_id"] = user_id
                session["firstName"] = first_name
                session["email"] = email
                session.permanent = True
                
                return jsonify({
                    "message": "Login successful!",
                    "user": {
                        "id": user_id,
                        "firstName": first_name,
                        "email": email
                    }
                }), 200
        
        return jsonify({"error": "Invalid email or password"}), 401
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({"error": "Server error", "details": str(e)}), 500

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200

@app.route("/me")
def me():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, firstName, lastName, email, phone, address, state, city, zipCode, preferredPayment 
            FROM users WHERE id=%s
        """, (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify({"user": user}), 200
    except Exception as e:
        print(f"Get user error: {e}")
        return jsonify({"error": "Server error", "details": str(e)}), 500

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
        SET phone=%s, address=%s, state=%s, city=%s, zipCode=%s, preferredPayment=%s
        WHERE id=%s
        """
        values = (
            data.get("phone"),
            data.get("address"),
            data.get("state"),
            data.get("city"),
            data.get("zipCode"),
            data.get("preferredPayment"),
            user_id
        )
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Profile updated successfully"}), 200
    except Exception as e:
        print(f"Update profile error: {e}")
        return jsonify({"error": "Update failed", "details": str(e)}), 500

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
        return jsonify({"message": "Account deleted successfully"}), 200
    except Exception as e:
        print(f"Delete account error: {e}")
        return jsonify({"error": "Delete failed", "details": str(e)}), 500

# ==================== DRIVER AUTH ====================
@app.route("/driver/login", methods=["POST"])
def driver_login():
    data = request.get_json(silent=True) or {}
    print("\n=== DRIVER LOGIN ATTEMPT (DEBUG) ===")
    print("Raw payload:", data)

    phone = (data.get("phone") or "").strip()
    email = (data.get("email") or "").strip()
    password = data.get("password") or ""

    if not password or (not phone and not email):
        print("❌ Missing phone/email or password")
        return jsonify({"error": "Phone/email and password required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if phone:
            print("Looking up driver by phone:", phone)
            cursor.execute("SELECT * FROM drivers WHERE phone = %s LIMIT 1", (phone,))
        else:
            print("Looking up driver by email:", email)
            cursor.execute("SELECT * FROM drivers WHERE email = %s LIMIT 1", (email,))

        driver = cursor.fetchone()
        cursor.close()
        conn.close()

        print("DB row (driver):", driver)

        if not driver:
            print("❌ No driver found for given identifier")
            return jsonify({"error": "No driver found with provided phone/email"}), 404

        # Access driver data correctly based on whether it's a dict or tuple
        stored_pw = None
        if isinstance(driver, dict):
            # Look for password field in dict
            for key in ("password", "password_hash", "pw", "pass", "passwd"):
                if key in driver and driver[key]:
                    stored_pw = driver[key]
                    print(f"Found password column: {key}")
                    break
        else:
            # For tuple, assume password is at index 6 (based on the SELECT query)
            stored_pw = driver[6] if len(driver) > 6 else None
            print("Found password at index 6")

        if stored_pw is None:
            print("Driver DB columns:", list(driver.keys()) if isinstance(driver, dict) else f"Tuple with {len(driver)} elements")
            return jsonify({"error": "Server misconfigured: no password column found for driver"}), 500

        def looks_like_hash(s):
            return isinstance(s, str) and s.startswith(("pbkdf2:sha256","argon2","bcrypt","sha256","scrypt"))

        if looks_like_hash(str(stored_pw)):
            pw_ok = check_password_hash(str(stored_pw), str(password))
            print("Password check (hashed):", pw_ok)
        else:
            pw_ok = (str(stored_pw) == str(password))
            print("Password check (plain compare):", pw_ok, "| stored:", stored_pw)

        if not pw_ok:
            print("❌ Invalid password")
            return jsonify({"error": "Invalid credentials"}), 401

        # Access driver ID correctly
        driver_id = None
        if isinstance(driver, dict):
            driver_id = driver.get("driver_id") or driver.get("id") or driver.get("user_id")
        else:
            # Assume driver_id is at index 0
            driver_id = driver[0] if len(driver) > 0 else None

        try:
            driver_id = int(driver_id) if driver_id is not None else None
        except Exception:
            pass

        session.clear()
        if driver_id:
            session["driver_id"] = driver_id
        else:
            session["driver_id"] = driver.get("phone") or driver.get("email") if isinstance(driver, dict) else (driver[3] if len(driver) > 3 else None)

        # Access driver name and email correctly
        driver_first_name = ""
        driver_email = ""
        if isinstance(driver, dict):
            driver_first_name = str(driver.get("firstName") or driver.get("full_name") or "")
            driver_email = str(driver.get("email") or "")
        else:
            # firstName at index 1, full_name at index 3, email at index 4
            driver_first_name = str(driver[1] if len(driver) > 1 else driver[3] if len(driver) > 3 else "")
            driver_email = str(driver[4] if len(driver) > 4 else "")

        session["driver_firstName"] = driver_first_name
        session["driver_email"] = driver_email
        session["is_driver"] = True
        session.permanent = True
        session.modified = True

        print(f"✅ Driver login successful. session driver_id: {session['driver_id']}")

        return jsonify({
            "message": "Driver login successful!",
            "redirect": "/driver/dashboard",
            "driver": {
                "id": session.get("driver_id"),
                "firstName": session.get("driver_firstName"),
                "email": session.get("driver_email")
            }
        }), 200

    except Exception as e:
        print("❌ Exception in driver_login:", e)
        import traceback; traceback.print_exc()
        return jsonify({"error": "Server error", "details": str(e)}), 500

# -------------------- NEW: DRIVER SIGNUP --------------------
# This route accepts both JSON and multipart/form-data (file upload).
# Replace your current /driver/signup route with this fixed version:

@app.route("/driver/signup", methods=["GET", "POST"])
def driver_signup():
    if request.method == "GET":
        return jsonify({"message": "Driver signup endpoint. POST form-data to create a driver."}), 200

    # Parse incoming data
    content_type = request.content_type or ""
    is_json = content_type.startswith("application/json")
    is_form = content_type.startswith("multipart/form-data") or content_type.startswith("application/x-www-form-urlencoded")

    data = {}
    license_path = ""
    
    try:
        if is_json:
            data = request.get_json() or {}
        elif is_form:
            data = request.form.to_dict()
            # Handle file upload if present
            license_file = request.files.get("license_image")
            if license_file and license_file.filename:
                if not allowed_file(license_file.filename):
                    return jsonify({"error": "File type not allowed"}), 400
                filename = secure_filename(license_file.filename)
                save_path = os.path.join(UPLOAD_DIR, filename)
                license_file.save(save_path)
                license_path = save_path
        else:
            data = request.get_json(silent=True) or request.form.to_dict() or {}
    except Exception as e:
        print("❌ Driver signup parse error:", e)
        return jsonify({"error": "Failed to parse request"}), 400

    # Extract and validate fields
    firstName = data.get("firstName", "").strip()
    lastName = data.get("lastName", "").strip()
    full_name = data.get("full_name", "").strip()
    
    # If full_name not provided, build it from firstName + lastName
    if not full_name and firstName and lastName:
        full_name = f"{firstName} {lastName}".strip()
    
    email = data.get("email", "").strip()
    phone = data.get("phone", "").strip()
    password = data.get("password", "")
    license_no = data.get("license_no", "").strip()
    vehicle_type = data.get("vehicle_type", "").strip()

    print("=== DRIVER SIGNUP RECEIVED ===")
    print(f"full_name: {full_name}")
    print(f"firstName: {firstName}")
    print(f"lastName: {lastName}")
    print(f"email: {email}")
    print(f"phone: {phone}")


    print(f"license_no: {license_no}")
    print(f"vehicle_type: {vehicle_type}")
    print(f"license_path: {license_path}")

    # Validation - check required fields based on your schema
    if not full_name:
        return jsonify({"error": "Full name is required (or provide firstName and lastName)"}), 400
    
    if not phone:
        return jsonify({"error": "Phone number is required"}), 400
    
    if not password:
        return jsonify({"error": "Password is required"}), 400

    # Validate phone format
    if not phone.isdigit() or len(phone) != 10:
        return jsonify({"error": "Phone must be exactly 10 digits"}), 400

    try:
        hashed_pw = generate_password_hash(password)
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Match your schema exactly - with all vehicle fields
        sql = """
        INSERT INTO drivers
          (full_name, firstName, lastName, phone, email, license_no, license_path, 
           vehicle_type, vehicle_make, vehicle_model, license_plate, password, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        values = (
            full_name,                              # full_name (NOT NULL)
            firstName or None,                      # firstName (nullable)
            lastName or None,                       # lastName (nullable)
            phone,                                  # phone (NOT NULL, UNIQUE)
            email or None,                          # email (nullable, UNIQUE)
            license_no or None,                     # license_no (nullable)
            license_path or None,                   # license_path (nullable)
            vehicle_type or None,                   # vehicle_type (nullable)
            data.get("vehicle_make", "").strip() or None,   # vehicle_make (nullable)
            data.get("vehicle_model", "").strip() or None,  # vehicle_model (nullable)
            data.get("license_plate", "").strip() or None,  # license_plate (nullable)
            hashed_pw,                              # password (NOT NULL)
            "offline"                               # status (default: offline)
        )
        
        cursor.execute(sql, values)
        conn.commit()
        driver_id = cursor.lastrowid
        cursor.close()
        conn.close()
        
        print(f"✅ Driver created successfully! ID: {driver_id}")
        return jsonify({
            "message": "Driver created successfully!",
            "driver_id": driver_id
        }), 201
        
    except mysql.connector.IntegrityError as e:
        print(f"❌ Integrity error: {e}")
        error_msg = str(e)
        if "phone" in error_msg:
            return jsonify({"error": "Phone number already registered"}), 409
        elif "email" in error_msg:
            return jsonify({"error": "Email already registered"}), 409
        else:
            return jsonify({"error": "Registration failed - duplicate entry"}), 409
            
    except Exception as e:
        print(f"❌ Driver signup error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Server error", "details": str(e)}), 500
# -------------------- end driver signup --------------------

    print("\n=== DRIVER LOGIN ATTEMPT ===")
    
    data = request.get_json()
    phone = data.get("phone")
    password = data.get("password")
    
    print(f"Login attempt - Phone: {phone}")
    
    if not phone or not password:
        return jsonify({"error": "Phone and password required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Try to find driver by phone
        cursor.execute("""
            SELECT driver_id, firstName, lastName, full_name, email, phone, 
                   password, license_no, vehicle_type, vehicle_make, 
                   vehicle_model, license_plate, status
            FROM drivers 
            WHERE phone = %s
        """, (phone,))
        
        driver = cursor.fetchone()
        cursor.close()
        conn.close()

        if not driver:
            print("❌ No driver found")
            return jsonify({"error": "No driver found with provided credentials"}), 404

        # Access driver data correctly
        stored_password = driver.get("password") if isinstance(driver, dict) else driver[6]
        
        print(f"✅ Driver found: ID {driver.get('driver_id') if isinstance(driver, dict) else driver[0]}")

        if not stored_password:
            print("❌ No password stored in database!")
            return jsonify({"error": "Account configuration error"}), 500

        print(f"Stored password type: {type(stored_password)}")
        
        # Verify password using werkzeug's check_password_hash
        password_valid = check_password_hash(str(stored_password), str(password))
        print(f"Password verification result: {password_valid}")

        if not password_valid:
            print("❌ Invalid password")
            return jsonify({"error": "Invalid credentials"}), 401

        # Success! Set session
        driver_id = driver.get("driver_id") if isinstance(driver, dict) else driver[0]
        driver_first_name = driver.get("firstName") if isinstance(driver, dict) else driver[1]
        driver_email = driver.get("email") if isinstance(driver, dict) else driver[4]
        driver_full_name = driver.get("full_name") if isinstance(driver, dict) else driver[3]
        
        session.clear()
        session["driver_id"] = int(str(driver_id))
        session["driver_firstName"] = str(driver_first_name) if driver_first_name else (str(driver_full_name).split()[0] if " " in str(driver_full_name) else str(driver_full_name))
        session["driver_email"] = str(driver_email) if driver_email else ""
        session["is_driver"] = True
        session.permanent = True

        print(f"✅ Login successful! Session: {dict(session)}")

        return jsonify({
            "message": "Driver login successful!",
            "redirect": "/driver/dashboard",
            "driver": {
                "id": int(str(driver_id)),
                "firstName": session.get("driver_firstName"),
                "email": session.get("driver_email")
            }
        }), 200

    except Exception as e:
        print(f"❌ Exception in driver_login: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Server error", "details": str(e)}), 500


# @app.route("/driver/dashboard")
# def driver_dashboard():
#     print(f"\n=== DASHBOARD ACCESS ===")
#     print(f"Session: {dict(session)}")
    
#     driver_id = session.get("driver_id")
    
#     if not driver_id:
#         print("❌ No driver_id in session, redirecting to home")
#         return redirect("/")
    
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor(dictionary=True)
        
       
#         cursor.execute("""
#             SELECT driver_id, firstName, lastName, email, phone, license_number, 
#                    vehicle_type, vehicle_make, vehicle_model, license_plate, 
#                    status, rating, total_rides
#             FROM drivers WHERE driver_id=%s
#         """, (driver_id,))
#         driver = cursor.fetchone()
        
#         if not driver:
#             print("❌ Driver not found in DB")
#             session.clear()
#             cursor.close()
#             conn.close()
#             return redirect("/")
        
#         cursor.execute("""
#             SELECT COUNT(*) as total_rides, 
#                    COALESCE(SUM(fare), 0) as total_earnings
#             FROM rides 
#             WHERE driver_id=%s AND status='completed'
#         """, (driver_id,))
#         stats = cursor.fetchone()
        
      
#         cursor.execute("""
#             SELECT ride_id, user_id, pickup_lat, pickup_lng, drop_lat, drop_lng,
#                    pickup_address, dropoff_address, status, requested_at
#             FROM rides
#             WHERE driver_id=%s AND status IN ('accepted', 'in_progress')
#             ORDER BY requested_at DESC
#         """, (driver_id,))
#         active_rides = cursor.fetchall()
        
#         cursor.close()
#         conn.close()
        
#         print("✅ Rendering dashboard")
#         return render_template(
#             "driver_dashboard.html", 
#             driver=driver, 
#             stats=stats or {},
#             active_rides=active_rides or []
#         )
#     except Exception as e:
#         print(f"❌ Dashboard error: {e}")
#         import traceback
#         traceback.print_exc()
#         return redirect("/")

# @app.route("/driver/logout", methods=["POST"])
# def driver_logout():
#     session.clear()
#     return jsonify({"message": "Driver logged out"}), 200
# Replace your /driver/dashboard route with this fixed version
@app.route("/driver/dashboard")
def driver_dashboard():
    print(f"\n=== DASHBOARD ACCESS ATTEMPT ===")
    print(f"Full session data: {dict(session)}")
    print(f"Session keys: {list(session.keys())}")
    print(f"driver_id from session: {session.get('driver_id')}")
    print(f"is_driver flag: {session.get('is_driver')}")
    
    driver_id = session.get("driver_id")
    
    if not driver_id:
        print("❌ No driver_id in session, redirecting to home")
        return redirect("/")
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        print(f"🔍 Looking up driver with ID: {driver_id}")
        
        # Get driver info (only columns that exist)
        cursor.execute("""
            SELECT driver_id, firstName, lastName, full_name, email, phone, 
                   license_no, vehicle_type, vehicle_make, vehicle_model, 
                   license_plate, status
            FROM drivers WHERE driver_id=%s
        """, (driver_id,))
        driver = cursor.fetchone()
        
        if not driver:
            print(f"❌ Driver not found in database for ID: {driver_id}")
            cursor.close()
            conn.close()
            session.clear()
            return redirect("/")
        
        print(f"✅ Driver found: ID {driver[0] if not isinstance(driver, dict) else driver.get('driver_id')}")
        
        # Get ride statistics from rides table
        try:
            cursor.execute("""
                SELECT COUNT(*) as total_rides, 
                       COALESCE(SUM(fare), 0) as total_earnings
                FROM rides 
                WHERE driver_id=%s AND status='completed'
            """, (driver_id,))
            stats = cursor.fetchone()
        except mysql.connector.Error:
            print("⚠️ Rides table query failed, using defaults")
            stats = {"total_rides": 0, "total_earnings": 0}
        
        # Get active rides
        try:
            cursor.execute("""
                SELECT ride_id, user_id, pickup_lat, pickup_lng, drop_lat, drop_lng,
                       pickup_address, dropoff_address, status, requested_at
                FROM rides
                WHERE driver_id=%s AND status IN ('accepted', 'in_progress')
                ORDER BY requested_at DESC
            """, (driver_id,))
            active_rides = cursor.fetchall()
        except mysql.connector.Error:
            print("⚠️ Active rides query failed")
            active_rides = []
        
        cursor.close()
        conn.close()
        
        print("✅ Rendering dashboard")
        return render_template(
            "driver_dashboard.html", 
            driver=driver, 
            stats=stats or {},
            active_rides=active_rides or []
        )
    except Exception as e:
        print(f"❌ Dashboard error: {e}")
        import traceback
        traceback.print_exc()
        return redirect("/")



@app.route("/driver/logout", methods=["POST"])
def driver_logout():
    session.clear()
    return jsonify({"message": "Driver logged out"}), 200

# ==================== RIDES ====================
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
#         return jsonify({"error": "Create ride failed"}), 500

# @app.route("/driver/available_rides", methods=["GET"])
# def driver_available_rides():
#     driver_id = session.get("driver_id")
#     if not driver_id:
#         return jsonify({"error": "Not logged in"}), 401

#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("""
#             SELECT r.ride_id, r.user_id, r.pickup_lat, r.pickup_lng, r.drop_lat, r.drop_lng, 
#                    r.pickup_address, r.dropoff_address, r.requested_at, r.fare,
#                    u.firstName as user_firstName, u.lastName as user_lastName, u.phone as user_phone
#             FROM rides r
#             JOIN users u ON r.user_id = u.id
#             WHERE r.status='requested'
#             ORDER BY r.requested_at ASC
#             LIMIT 10
#         """)
#         rides = cursor.fetchall()
#         cursor.close()
#         conn.close()
#         return jsonify({"rides": rides}), 200
#     except Exception as e:
#         print(f"Get rides error: {e}")
#         return jsonify({"error": "Failed to fetch rides"}), 500
# Add these routes to your app.py file

# --- RIDE / DRIVER routes (updated) ---

@app.route("/create_ride", methods=["POST"])
def create_ride():
    """User creates a new ride request"""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json() or {}
    
    # Required fields
    required = ["pickup_lat", "pickup_lng", "drop_lat", "drop_lng", 
                "pickup_address", "dropoff_address", "distance", "fare"]
    
    for field in required:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        sql = """
        INSERT INTO rides 
        (user_id, pickup_lat, pickup_lng, drop_lat, drop_lng, 
         pickup_address, dropoff_address, distance, fare, status, requested_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'requested', NOW())
        """
        
        values = (
            user_id,
            data["pickup_lat"],
            data["pickup_lng"],
            data["drop_lat"],
            data["drop_lng"],
            data["pickup_address"],
            data["dropoff_address"],
            data["distance"],
            data["fare"]
        )
        
        cursor.execute(sql, values)
        conn.commit()
        ride_id = cursor.lastrowid
        cursor.close()
        conn.close()
        
        print(f"✅ Ride {ride_id} created by user {user_id}")
        return jsonify({
            "message": "Ride requested successfully!",
            "ride_id": ride_id
        }), 201
        
    except Exception as e:
        print(f"❌ Create ride error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Failed to create ride", "details": str(e)}), 500


@app.route("/driver/available_rides", methods=["GET"])
def driver_available_rides():
    """Get all available (requested) rides for drivers"""
    driver_id = session.get("driver_id")
    if not driver_id:
        return jsonify({"error": "Not logged in"}), 401

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get rides that are 'requested' and not yet assigned to any driver
        cursor.execute("""
            SELECT 
                r.ride_id, 
                r.user_id, 
                r.pickup_lat, 
                r.pickup_lng, 
                r.drop_lat, 
                r.drop_lng, 
                r.pickup_address, 
                r.dropoff_address, 
                r.distance,
                r.fare,
                r.requested_at,
                u.firstName as user_firstName, 
                u.lastName as user_lastName, 
                u.phone as user_phone
            FROM rides r
            JOIN users u ON r.user_id = u.id
            WHERE r.status = 'requested' AND r.driver_id IS NULL
            ORDER BY r.requested_at DESC
            LIMIT 20
        """)
        
        rides = cursor.fetchall()
        cursor.close()
        conn.close()
        
        print(f"✅ Found {len(rides)} available rides")
        return jsonify({"rides": rides}), 200
        
    except Exception as e:
        print(f"❌ Get available rides error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Failed to fetch rides", "details": str(e)}), 500


# ---- RENAMED to avoid endpoint collision ----
@app.route("/driver/accept_ride", methods=["POST"])
def driver_accept_ride_post():
    """Driver accepts a ride request"""
    driver_id = session.get("driver_id")
    if not driver_id:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json() or {}
    ride_id = data.get("ride_id")
    
    if not ride_id:
        return jsonify({"error": "ride_id required"}), 400

    conn = None
    try:
        conn = get_db_connection()
        conn.start_transaction()
        cursor = conn.cursor(dictionary=True)

        # Check if ride is still available
        cursor.execute("""
            SELECT ride_id, status, driver_id 
            FROM rides 
            WHERE ride_id=%s AND status='requested' AND driver_id IS NULL
            FOR UPDATE
        """, (ride_id,))
        
        ride = cursor.fetchone()
        
        if not ride:
            conn.rollback()
            cursor.close()
            conn.close()
            return jsonify({"error": "Ride not available or already accepted"}), 409

        # Assign ride to driver
        cursor.execute("""
            UPDATE rides
            SET driver_id=%s, status='accepted', accepted_at=NOW()
            WHERE ride_id=%s AND status='requested' AND driver_id IS NULL
        """, (driver_id, ride_id))

        if cursor.rowcount == 0:
            conn.rollback()
            cursor.close()
            conn.close()
            return jsonify({"error": "Failed to accept ride"}), 409

        # Update driver status to busy
        cursor.execute("""
            UPDATE drivers 
            SET status='busy' 
            WHERE driver_id=%s
        """, (driver_id,))

        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"✅ Driver {driver_id} accepted ride {ride_id}")
        return jsonify({"message": "Ride accepted successfully", "ride_id": ride_id}), 200

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"❌ Accept ride error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Failed to accept ride", "details": str(e)}), 500


@app.route("/user/my_rides", methods=["GET"])
def user_my_rides():
    """Get user's ride history"""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT 
                r.ride_id,
                r.pickup_address,
                r.dropoff_address,
                r.distance,
                r.fare,
                r.status,
                r.requested_at,
                r.accepted_at,
                r.completed_at,
                d.full_name as driver_name,
                d.phone as driver_phone,
                d.vehicle_type,
                d.license_plate
            FROM rides r
            LEFT JOIN drivers d ON r.driver_id = d.driver_id
            WHERE r.user_id = %s
            ORDER BY r.requested_at DESC
            LIMIT 50
        """, (user_id,))
        
        rides = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify({"rides": rides}), 200
        
    except Exception as e:
        print(f"❌ Get user rides error: {e}")
        return jsonify({"error": "Failed to fetch rides"}), 500


@app.route("/user/cancel_ride/<int:ride_id>", methods=["POST"])
def cancel_ride(ride_id):
    """User cancels a ride request"""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if ride belongs to user and is cancellable
        cursor.execute("""
            UPDATE rides
            SET status='cancelled', completed_at=NOW()
            WHERE ride_id=%s AND user_id=%s AND status IN ('requested', 'accepted')
        """, (ride_id, user_id))
        
        if cursor.rowcount == 0:
            conn.rollback()
            cursor.close()
            conn.close()
            return jsonify({"error": "Cannot cancel this ride"}), 400
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"✅ User {user_id} cancelled ride {ride_id}")
        return jsonify({"message": "Ride cancelled successfully"}), 200
        
    except Exception as e:
        print(f"❌ Cancel ride error: {e}")
        return jsonify({"error": "Failed to cancel ride"}), 500


# Add these routes to your app.py

@app.route("/user/ride_status/<int:ride_id>", methods=["GET"])
def get_ride_status(ride_id):
    """Get current status of a ride with driver location"""
    user_id = session.get("user_id")
    
    # Debug logging
    print(f"🔍 Ride status request - User ID: {user_id}, Ride ID: {ride_id}")
    
    if not user_id:
        print("❌ User not authenticated for ride status")
        return jsonify({"error": "Not logged in", "redirect": "/login"}), 401

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get ride details - verify the ride belongs to this user
        cursor.execute("""
            SELECT 
                r.ride_id,
                r.user_id,
                r.driver_id,
                r.pickup_lat,
                r.pickup_lng,
                r.drop_lat,
                r.drop_lng,
                r.pickup_address,
                r.dropoff_address,
                r.distance,
                r.fare,
                r.status,
                r.requested_at,
                r.accepted_at,
                r.completed_at
            FROM rides r
            WHERE r.ride_id = %s AND r.user_id = %s
        """, (ride_id, user_id))
        
        ride = cursor.fetchone()
        
        if not ride:
            cursor.close()
            conn.close()
            print(f"❌ Ride {ride_id} not found for user {user_id}")
            return jsonify({"error": "Ride not found or access denied"}), 404
        
        driver = None
        
        # If ride is accepted, get driver details and location
        if ride.get('driver_id') if isinstance(ride, dict) else ride[2]:  # driver_id is at index 2
            driver_id = ride.get('driver_id') if isinstance(ride, dict) else ride[2]
            cursor.execute("""
                SELECT 
                    driver_id,
                    full_name,
                    firstName,
                    lastName,
                    phone,
                    vehicle_type,
                    vehicle_make,
                    vehicle_model,
                    license_plate,
                    rating,
                    current_lat,
                    current_lng
                FROM drivers
                WHERE driver_id = %s
            """, (driver_id,))
            
            driver = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        print(f"✅ Ride status retrieved for ride {ride_id}")
        return jsonify({
            "ride": ride,
            "driver": driver
        }), 200
        
    except Exception as e:
        print(f"❌ Get ride status error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Failed to get ride status", "details": str(e)}), 500


# @app.route("/user/confirm_payment", methods=["POST"])
# def confirm_payment():
#     """User confirms payment for completed ride"""
#     user_id = session.get("user_id")
#     if not user_id:
#         return jsonify({"error": "Not logged in"}), 401

#     data = request.get_json() or {}
#     ride_id = data.get("ride_id")
#     payment_method = data.get("payment_method")
    
#     if not ride_id or not payment_method:
#         return jsonify({"error": "ride_id and payment_method required"}), 400
    
#     if payment_method not in ["wallet", "upi"]:
#         return jsonify({"error": "Invalid payment method"}), 400

#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor(dictionary=True)
        
       
#         cursor.execute("""
#             SELECT ride_id, user_id, fare, status
#             FROM rides
#             WHERE ride_id = %s AND user_id = %s
#         """, (ride_id, user_id))
        
#         ride = cursor.fetchone()
        
#         if not ride:
#             cursor.close()
#             conn.close()
#             return jsonify({"error": "Ride not found"}), 404
        
        
#         cursor.execute("""
#             UPDATE rides
#             SET payment_method = %s, payment_status = 'paid'
#             WHERE ride_id = %s
#         """, (payment_method, ride_id))
        
#         conn.commit()
#         cursor.close()
#         conn.close()
        
#         print(f"✅ Payment confirmed for ride {ride_id} via {payment_method}")
#         return jsonify({
#             "message": "Payment confirmed successfully",
#             "payment_method": payment_method
#         }), 200
        
#     except Exception as e:
#         print(f"❌ Confirm payment error: {e}")
#         import traceback
#         traceback.print_exc()
#         return jsonify({"error": "Failed to confirm payment"}), 500
# ---------- simple confirm payment (renamed to avoid endpoint collision) ----------
@app.route("/user/confirm_payment_simple", methods=["POST"], endpoint="confirm_payment_simple")
def confirm_payment_simple():
    """Simple payment confirmation (kept for backward/compat/test). 
    NOTE: If you want this to remain at /user/confirm_payment, remove the wallet flow or merge them.
    """
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json() or {}
    ride_id = data.get("ride_id")
    payment_method = data.get("payment_method")

    if not ride_id or not payment_method:
        return jsonify({"error": "ride_id and payment_method required"}), 400

    if payment_method not in ["wallet", "upi"]:
        return jsonify({"error": "Invalid payment method"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Verify ride belongs to user
        cursor.execute("""
            SELECT ride_id, user_id, fare, status
            FROM rides
            WHERE ride_id = %s AND user_id = %s
        """, (ride_id, user_id))

        ride = cursor.fetchone()

        if not ride:
            cursor.close()
            conn.close()
            return jsonify({"error": "Ride not found"}), 404

        # Mark payment status as paid (simple flow)
        cursor.execute("""
            UPDATE rides
            SET payment_method = %s, payment_status = 'paid'
            WHERE ride_id = %s
        """, (payment_method, ride_id))

        conn.commit()
        cursor.close()
        conn.close()

        print(f"✅ Payment confirmed for ride {ride_id} via {payment_method} (simple)")
        return jsonify({
            "message": "Payment confirmed successfully",
            "payment_method": payment_method
        }), 200

    except Exception as e:
        print(f"❌ Confirm payment (simple) error: {e}")
        import traceback; traceback.print_exc()
        return jsonify({"error": "Failed to confirm payment", "details": str(e)}), 500

@app.route("/driver/update_location", methods=["POST"])
def driver_update_location():
    """Driver updates their current location"""
    driver_id = session.get("driver_id")
    if not driver_id:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json() or {}
    lat = data.get("lat")
    lng = data.get("lng")
    
    if lat is None or lng is None:
        return jsonify({"error": "lat and lng required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE drivers
            SET current_lat = %s, current_lng = %s, last_location_update = NOW()
            WHERE driver_id = %s
        """, (lat, lng, int(str(driver_id))))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Location updated"}), 200
        
    except Exception as e:
        print(f"❌ Update location error: {e}")
        return jsonify({"error": "Failed to update location"}), 500


@app.route("/driver/start_ride/<int:ride_id>", methods=["POST"])
def driver_start_ride(ride_id):
    """Driver starts the ride (changes status to in_progress)"""
    driver_id = session.get("driver_id")
    if not driver_id:
        return jsonify({"error": "Not logged in"}), 401

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE rides
            SET status = 'in_progress', started_at = NOW()
            WHERE ride_id = %s AND driver_id = %s AND status = 'accepted'
        """, (ride_id, driver_id))
        
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return jsonify({"error": "Cannot start this ride"}), 400
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"✅ Ride {ride_id} started by driver {driver_id}")
        return jsonify({"message": "Ride started"}), 200
        
    except Exception as e:
        print(f"❌ Start ride error: {e}")
        return jsonify({"error": "Failed to start ride"}), 500


@app.route("/driver/complete_ride/<int:ride_id>", methods=["POST"])
def driver_complete_ride(ride_id):
    """Driver completes the ride"""
    driver_id = session.get("driver_id")
    if not driver_id:
        return jsonify({"error": "Not logged in"}), 401

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Update ride status
        cursor.execute("""
            UPDATE rides
            SET status = 'completed', completed_at = NOW()
            WHERE ride_id = %s AND driver_id = %s AND status = 'in_progress'
        """, (ride_id, driver_id))
        
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return jsonify({"error": "Cannot complete this ride"}), 400
        
        # Update driver status to available
        cursor.execute("""
            UPDATE drivers
            SET status = 'available'
            WHERE driver_id = %s
        """, (driver_id,))
        
        # Update driver's total rides and earnings
        cursor.execute("""
            UPDATE drivers d
            JOIN rides r ON d.driver_id = r.driver_id
            SET d.total_rides = d.total_rides + 1,
                d.total_earnings = d.total_earnings + r.fare
            WHERE d.driver_id = %s AND r.ride_id = %s
        """, (driver_id, ride_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"✅ Ride {ride_id} completed by driver {driver_id}")
        return jsonify({"message": "Ride completed successfully"}), 200
        
    except Exception as e:
        print(f"❌ Complete ride error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Failed to complete ride"}), 500        


# Optional: quick route to print registered routes for debugging (remove in production)
@app.route("/_debug/routes", methods=["GET"])
def _debug_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            "endpoint": rule.endpoint,
            "rule": str(rule),
            "methods": sorted([m for m in rule.methods if m not in ("HEAD", "OPTIONS")])
        })
    return jsonify({"routes": routes})


# Add this route to your app.py file

@app.route("/driver/update_status", methods=["POST"])
def driver_update_status():
    driver_id = session.get("driver_id")
    if not driver_id:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json() or {}
    status = data.get("status")
    
    if status not in ["available", "busy", "offline"]:
        return jsonify({"error": "Invalid status"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE drivers 
            SET status = %s 
            WHERE driver_id = %s
        """, (status, driver_id))
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"✅ Driver {driver_id} status updated to: {status}")
        return jsonify({"message": "Status updated", "status": status}), 200
    except Exception as e:
        print(f"❌ Update status error: {e}")
        return jsonify({"error": "Failed to update status"}), 500
# @app.route("/driver/accept_ride", methods=["POST"])
# def driver_accept_ride():
#     driver_id = session.get("driver_id")
#     if not driver_id:
#         return jsonify({"error": "Not logged in"}), 401

#     data = request.get_json() or {}
#     ride_id = data.get("ride_id")
    
#     if not ride_id:
#         return jsonify({"error": "ride_id required"}), 400

#     try:
#         conn = get_db_connection()
#         conn.start_transaction()
#         cursor = conn.cursor()

#         cursor.execute("""
#             SELECT status FROM rides 
#             WHERE ride_id=%s AND status='requested'
#             FOR UPDATE
#         """, (ride_id,))
#         ride = cursor.fetchone()
        
#         if not ride:
#             conn.rollback()
#             cursor.close()
#             conn.close()
#             return jsonify({"error": "Ride not available"}), 409

#         cursor.execute("""
#             UPDATE rides
#             SET driver_id=%s, status='accepted', accepted_at=NOW()
#             WHERE ride_id=%s AND status='requested'
#         """, (driver_id, ride_id))

#         cursor.execute("UPDATE drivers SET status='busy' WHERE driver_id=%s", (driver_id,))

#         conn.commit()
#         cursor.close()
#         conn.close()
#         return jsonify({"message": "Ride accepted", "ride_id": ride_id}), 200

#     except Exception as e:
#         if conn:
#             conn.rollback()
#         print(f"Accept ride error: {e}")
#         return jsonify({"error": "Accept failed"}), 500
# ---------- duplicate accept ride (renamed to avoid collision) ----------
@app.route("/driver/accept_ride_simple", methods=["POST"], endpoint="driver_accept_ride_simple")
def driver_accept_ride_simple():
    """Alternate/legacy accept ride handler (kept for compatibility/tests)."""
    driver_id = session.get("driver_id")
    if not driver_id:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json() or {}
    ride_id = data.get("ride_id")

    if not ride_id:
        return jsonify({"error": "ride_id required"}), 400

    conn = None
    try:
        conn = get_db_connection()
        conn.start_transaction()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT status FROM rides 
            WHERE ride_id=%s AND status='requested'
            FOR UPDATE
        """, (ride_id,))
        ride = cursor.fetchone()

        if not ride:
            conn.rollback()
            cursor.close()
            conn.close()
            return jsonify({"error": "Ride not available"}), 409

        cursor.execute("""
            UPDATE rides
            SET driver_id=%s, status='accepted', accepted_at=NOW()
            WHERE ride_id=%s AND status='requested'
        """, (driver_id, ride_id))

        cursor.execute("UPDATE drivers SET status='busy' WHERE driver_id=%s", (driver_id,))

        conn.commit()
        cursor.close()
        conn.close()
        print(f"✅ (simple) Driver {driver_id} accepted ride {ride_id}")
        return jsonify({"message": "Ride accepted", "ride_id": ride_id}), 200

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Accept ride (simple) error: {e}")
        import traceback; traceback.print_exc()
        return jsonify({"error": "Accept failed", "details": str(e)}), 500


# Add these enhanced routes to your app.py

# ==================== DRIVER RIDE MANAGEMENT ====================

@app.route("/driver/reject_ride/<int:ride_id>", methods=["POST"])
def driver_reject_ride(ride_id):
    """Driver rejects a ride request"""
    driver_id = session.get("driver_id")
    if not driver_id:
        return jsonify({"error": "Not logged in"}), 401

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if ride exists and is in requested status
        cursor.execute("""
            SELECT ride_id, status 
            FROM rides 
            WHERE ride_id = %s AND status = 'requested'
        """, (ride_id,))
        
        ride = cursor.fetchone()
        
        if not ride:
            cursor.close()
            conn.close()
            return jsonify({"error": "Ride not available"}), 404
        
        # Mark as cancelled (driver rejected)
        cursor.execute("""
            UPDATE rides
            SET status = 'cancelled', completed_at = NOW()
            WHERE ride_id = %s
        """, (ride_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"✅ Driver {driver_id} rejected ride {ride_id}")
        return jsonify({"message": "Ride rejected"}), 200
        
    except Exception as e:
        print(f"❌ Reject ride error: {e}")
        return jsonify({"error": "Failed to reject ride"}), 500


@app.route("/driver/active_ride", methods=["GET"])
def driver_active_ride():
    """Get driver's current active ride"""
    driver_id = session.get("driver_id")
    if not driver_id:
        return jsonify({"error": "Not logged in"}), 401

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT 
                r.ride_id,
                r.user_id,
                r.pickup_lat,
                r.pickup_lng,
                r.drop_lat,
                r.drop_lng,
                r.pickup_address,
                r.dropoff_address,
                r.distance,
                r.fare,
                r.status,
                r.accepted_at,
                u.firstName,
                u.lastName,
                u.phone as user_phone
            FROM rides r
            JOIN users u ON r.user_id = u.id
            WHERE r.driver_id = %s 
            AND r.status IN ('accepted', 'in_progress')
            ORDER BY r.accepted_at DESC
            LIMIT 1
        """, (driver_id,))
        
        ride = cursor.fetchone()
        cursor.close()
        conn.close()
        
        return jsonify({"ride": ride}), 200
        
    except Exception as e:
        print(f"❌ Get active ride error: {e}")
        return jsonify({"error": "Failed to get active ride"}), 500


# ==================== USER RIDE NOTIFICATIONS ====================

@app.route("/user/ride_updates/<int:ride_id>", methods=["GET"])
def get_ride_updates(ride_id):
    """Get real-time updates for a specific ride"""
    user_id = session.get("user_id")
    
    # Debug logging
    print(f"🔍 Ride updates request - User ID: {user_id}, Ride ID: {ride_id}")
    
    if not user_id:
        print("❌ User not authenticated for ride updates")
        return jsonify({"error": "Not logged in", "redirect": "/login"}), 401

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Verify the ride belongs to this user
        cursor.execute("""
            SELECT 
                r.ride_id,
                r.status,
                r.driver_id,
                r.accepted_at,
                r.started_at,
                r.completed_at,
                r.payment_status,
                d.full_name as driver_name,
                d.phone as driver_phone,
                d.vehicle_type,
                d.vehicle_make,
                d.vehicle_model,
                d.license_plate,
                d.rating as driver_rating,
                d.current_lat as driver_lat,
                d.current_lng as driver_lng
            FROM rides r
            LEFT JOIN drivers d ON r.driver_id = d.driver_id
            WHERE r.ride_id = %s AND r.user_id = %s
        """, (ride_id, user_id))
        
        ride = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not ride:
            print(f"❌ Ride {ride_id} not found for user {user_id}")
            return jsonify({"error": "Ride not found or access denied"}), 404
        
        print(f"✅ Ride updates retrieved for ride {ride_id}")
        return jsonify({"ride": ride}), 200
        
    except Exception as e:
        print(f"❌ Get ride updates error: {e}")
        return jsonify({"error": "Failed to get updates", "details": str(e)}), 500


# ==================== ENHANCED WALLET SYSTEM ====================

@app.route("/user/wallet_history", methods=["GET"])
def user_wallet_history():
    """Get detailed wallet transaction history"""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get wallet balance
        cursor.execute("""
            SELECT wallet_balance FROM users WHERE id = %s
        """, (user_id,))
        user = cursor.fetchone()
        
        # Get transactions
        cursor.execute("""
            SELECT 
                wt.transaction_id,
                wt.ride_id,
                wt.transaction_type,
                wt.amount,
                wt.balance_before,
                wt.balance_after,
                wt.description,
                wt.created_at,
                r.pickup_address,
                r.dropoff_address
            FROM wallet_transactions wt
            LEFT JOIN rides r ON wt.ride_id = r.ride_id
            WHERE wt.user_id = %s
            ORDER BY wt.created_at DESC
            LIMIT 100
        """, (user_id,))
        
        transactions = cursor.fetchall()
        cursor.close()
        conn.close()
        
        wallet_balance = user.get("wallet_balance") if isinstance(user, dict) else user[0] if user else 0
        
        return jsonify({
            "wallet_balance": float(str(wallet_balance)),
            "transactions": transactions
        }), 200
        
    except Exception as e:
        print(f"❌ Wallet history error: {e}")
        return jsonify({"error": "Failed to get wallet history"}), 500


@app.route("/driver/wallet_history", methods=["GET"])
def driver_wallet_history():
    """Get driver's wallet transaction history"""
    driver_id = session.get("driver_id")
    if not driver_id:
        return jsonify({"error": "Not logged in"}), 401

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get wallet balance
        cursor.execute("""
            SELECT wallet_balance, total_earnings 
            FROM drivers WHERE driver_id = %s
        """, (driver_id,))
        driver = cursor.fetchone()
        
        # Get transactions
        cursor.execute("""
            SELECT 
                wt.transaction_id,
                wt.ride_id,
                wt.transaction_type,
                wt.amount,
                wt.balance_before,
                wt.balance_after,
                wt.description,
                wt.created_at,
                r.pickup_address,
                r.dropoff_address
            FROM wallet_transactions wt
            LEFT JOIN rides r ON wt.ride_id = r.ride_id
            WHERE wt.driver_id = %s
            ORDER BY wt.created_at DESC
            LIMIT 100
        """, (driver_id,))
        
        transactions = cursor.fetchall()
        cursor.close()
        conn.close()
        
        wallet_balance = driver.get("wallet_balance") if isinstance(driver, dict) else driver[0] if driver else 0
        total_earnings = driver.get("total_earnings") if isinstance(driver, dict) else driver[1] if driver else 0
        
        return jsonify({
            "wallet_balance": float(str(wallet_balance)),
            "total_earnings": float(str(total_earnings)),
            "transactions": transactions
        }), 200
        
    except Exception as e:
        print(f"❌ Driver wallet history error: {e}")
        return jsonify({"error": "Failed to get wallet history"}), 500


# ==================== RIDE COMPLETION WITH PAYMENT ====================

@app.route("/driver/complete_ride_with_payment/<int:ride_id>", methods=["POST"])
def complete_ride_with_payment(ride_id):
    """Driver completes ride and triggers payment notification"""
    driver_id = session.get("driver_id")
    if not driver_id:
        return jsonify({"error": "Not logged in"}), 401

    conn = None
    try:
        conn = get_db_connection()
        conn.start_transaction()
        cursor = conn.cursor(dictionary=True)
        
        # Get ride details
        cursor.execute("""
            SELECT ride_id, driver_id, user_id, fare, status, payment_status
            FROM rides
            WHERE ride_id = %s AND driver_id = %s
        """, (ride_id, driver_id))
        
        ride = cursor.fetchone()
        
        if not ride:
            conn.rollback()
            cursor.close()
            conn.close()
            return jsonify({"error": "Ride not found"}), 404
        
        ride_status = ride.get("status") if isinstance(ride, dict) else ride[4]
        payment_status = ride.get("payment_status") if isinstance(ride, dict) else ride[5]
        
        if ride_status != 'in_progress':
            conn.rollback()
            cursor.close()
            conn.close()
            return jsonify({"error": "Ride is not in progress"}), 400
        
        # Update ride status to completed
        cursor.execute("""
            UPDATE rides
            SET status = 'completed', completed_at = NOW()
            WHERE ride_id = %s
        """, (ride_id,))
        
        # Update driver status to available
        cursor.execute("""
            UPDATE drivers
            SET status = 'available'
            WHERE driver_id = %s
        """, (driver_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"✅ Ride {ride_id} completed - waiting for payment")
        return jsonify({
            "message": "Ride completed - awaiting payment",
            "payment_pending": payment_status != 'paid'
        }), 200
        
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"❌ Complete ride error: {e}")
        return jsonify({"error": "Failed to complete ride"}), 500


# ==================== NOTIFICATION SYSTEM ====================

@app.route("/user/notifications", methods=["GET"])
def user_notifications():
    """Get user notifications about ride status changes"""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get recent ride status changes
        cursor.execute("""
            SELECT 
                r.ride_id,
                r.status,
                r.accepted_at,
                r.started_at,
                r.completed_at,
                d.full_name as driver_name
            FROM rides r
            LEFT JOIN drivers d ON r.driver_id = d.driver_id
            WHERE r.user_id = %s
            AND r.requested_at >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
            ORDER BY r.requested_at DESC
            LIMIT 10
        """, (user_id,))
        
        notifications = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify({"notifications": notifications}), 200
        
    except Exception as e:
        print(f"❌ Get notifications error: {e}")
        return jsonify({"error": "Failed to get notifications"}), 500


# Replace/Add these routes to your app.py for wallet system

@app.route("/user/wallet_balance", methods=["GET"])
def get_user_wallet_balance():
    """Get user's current wallet balance"""
    user_id = session.get("user_id")
    
    # Debug logging
    print(f"🔍 Wallet balance request - User ID: {user_id}")
    
    if not user_id:
        print("❌ User not authenticated for wallet balance")
        return jsonify({"error": "Not logged in", "redirect": "/login"}), 401

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT id, firstName, lastName, wallet_balance
            FROM users WHERE id = %s
        """, (user_id,))
        
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not user:
            print(f"❌ User {user_id} not found")
            return jsonify({"error": "User not found"}), 404
        
        wallet_balance = user.get("wallet_balance") if isinstance(user, dict) else user[3]
        first_name = user.get("firstName") if isinstance(user, dict) else user[1]
        last_name = user.get("lastName") if isinstance(user, dict) else user[2]
        
        print(f"✅ Wallet balance retrieved for user {user_id}")
        return jsonify({
            "wallet_balance": float(str(wallet_balance)),
            "user_name": f"{first_name} {last_name}"
        }), 200
        
    except Exception as e:
        print(f"❌ Get wallet balance error: {e}")
        return jsonify({"error": "Failed to get wallet balance", "details": str(e)}), 500


@app.route("/user/confirm_payment", methods=["POST"])
def confirm_user_payment():
    """User confirms payment for a completed ride"""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json()
    ride_id = data.get("ride_id")
    
    if not ride_id:
        return jsonify({"error": "Ride ID required"}), 400

    conn = None
    try:
        conn = get_db_connection()
        conn.start_transaction()
        cursor = conn.cursor(dictionary=True)
        
        # Get ride details
        cursor.execute("""
            SELECT r.ride_id, r.user_id, r.driver_id, r.fare, r.status, r.payment_status,
                   u.wallet_balance as user_wallet,
                   d.wallet_balance as driver_wallet
            FROM rides r
            JOIN users u ON r.user_id = u.id
            JOIN drivers d ON r.driver_id = d.driver_id
            WHERE r.ride_id = %s AND r.user_id = %s
        """, (ride_id, user_id))
        
        ride = cursor.fetchone()
        
        if not ride:
            conn.rollback()
            cursor.close()
            conn.close()
            return jsonify({"error": "Ride not found"}), 404
            
        # Check if already paid
        payment_status = ride.get("payment_status") if isinstance(ride, dict) else ride[5]
        if payment_status == 'paid':
            conn.rollback()
            cursor.close()
            conn.close()
            return jsonify({"error": "Ride already paid"}), 400
            
        # Check if ride is completed
        ride_status = ride.get("status") if isinstance(ride, dict) else ride[4]
        if ride_status != 'completed':
            conn.rollback()
            cursor.close()
            conn.close()
            return jsonify({"error": "Ride not completed yet"}), 400
            
        fare = ride.get("fare") if isinstance(ride, dict) else ride[3]
        user_wallet = ride.get("user_wallet") if isinstance(ride, dict) else ride[6]
        driver_wallet = ride.get("driver_wallet") if isinstance(ride, dict) else ride[7]
        driver_id = ride.get("driver_id") if isinstance(ride, dict) else ride[2]
        
        # Check if user has sufficient balance
        if float(str(user_wallet)) < float(str(fare)):
            conn.rollback()
            cursor.close()
            conn.close()
            return jsonify({"error": "Insufficient wallet balance"}), 400
            
        # Process payment
        new_user_balance = float(str(user_wallet)) - float(str(fare))
        new_driver_balance = float(str(driver_wallet)) + float(str(fare))
        
        # Update user wallet
        cursor.execute("""
            UPDATE users SET wallet_balance = %s WHERE id = %s
        """, (new_user_balance, user_id))
        
        # Update driver wallet
        cursor.execute("""
            UPDATE drivers SET wallet_balance = %s, total_earnings = total_earnings + %s 
            WHERE driver_id = %s
        """, (new_driver_balance, fare, driver_id))
        
        # Update ride payment status
        cursor.execute("""
            UPDATE rides
            SET payment_method = 'wallet', 
                payment_status = 'paid'
            WHERE ride_id = %s
        """, (ride_id,))
        
        # Record transaction for user (debit)
        cursor.execute("""
            INSERT INTO wallet_transactions 
            (user_id, ride_id, transaction_type, amount, balance_before, balance_after, description)
            VALUES (%s, %s, 'ride_payment', %s, %s, %s, %s)
        """, (user_id, ride_id, -float(str(fare)), float(str(user_wallet)), new_user_balance, 
              f"Payment for Ride #{ride_id}"))
        
        # Record transaction for driver (credit)
        cursor.execute("""
            INSERT INTO wallet_transactions 
            (driver_id, ride_id, transaction_type, amount, balance_before, balance_after, description)
            VALUES (%s, %s, 'ride_payment', %s, %s, %s, %s)
        """, (driver_id, ride_id, float(str(fare)), float(str(driver_wallet)), new_driver_balance,
              f"Received payment for Ride #{ride_id}"))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"✅ Payment successful: User {user_id} paid ₹{fare} to Driver {driver_id}")
        print(f"   User balance: ₹{user_wallet} → ₹{new_user_balance}")
        print(f"   Driver balance: ₹{driver_wallet} → ₹{new_driver_balance}")
        
        return jsonify({
            "message": "Payment successful",
            "fare": float(str(fare)),
            "user_new_balance": new_user_balance,
            "driver_new_balance": new_driver_balance,
            "transaction_completed": True
        }), 200
        
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"❌ Payment error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Payment failed", "details": str(e)}), 500


@app.route("/user/wallet_transactions", methods=["GET"])
def get_user_wallet_transactions():
    """Get user's wallet transaction history"""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT 
                transaction_id,
                ride_id,
                transaction_type,
                amount,
                balance_before,
                balance_after,
                description,
                created_at
            FROM wallet_transactions
            WHERE user_id = %s
            ORDER BY created_at DESC
            LIMIT 50
        """, (user_id,))
        
        transactions = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify({"transactions": transactions}), 200
        
    except Exception as e:
        print(f"❌ Get transactions error: {e}")
        return jsonify({"error": "Failed to get transactions"}), 500


@app.route("/driver/wallet_transactions", methods=["GET"])
def get_driver_wallet_transactions():
    """Get driver's wallet transaction history"""
    driver_id = session.get("driver_id")
    if not driver_id:
        return jsonify({"error": "Not logged in"}), 401

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT 
                transaction_id,
                ride_id,
                transaction_type,
                amount,
                balance_before,
                balance_after,
                description,
                created_at
            FROM wallet_transactions
            WHERE driver_id = %s
            ORDER BY created_at DESC
            LIMIT 50
        """, (driver_id,))
        
        transactions = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify({"transactions": transactions}), 200
        
    except Exception as e:
        print(f"❌ Get driver transactions error: {e}")
        return jsonify({"error": "Failed to get transactions"}), 500


@app.route("/user/add_money", methods=["POST"])
def user_add_money_to_wallet():
    """Add money to user's wallet"""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json()
    amount = data.get("amount")
    
    if not amount or float(amount) <= 0:
        return jsonify({"error": "Invalid amount"}), 400

    conn = None
    try:
        conn = get_db_connection()
        conn.start_transaction()
        cursor = conn.cursor(dictionary=True)
        
        # Get current balance
        cursor.execute("""
            SELECT wallet_balance FROM users WHERE id = %s FOR UPDATE
        """, (user_id,))
        
        user = cursor.fetchone()
        if not user:
            conn.rollback()
            cursor.close()
            conn.close()
            return jsonify({"error": "User not found"}), 404
            
        wallet_balance = user.get("wallet_balance") if isinstance(user, dict) else user[0]
        old_balance = float(str(wallet_balance))
        new_balance = old_balance + float(amount)
        
        # Update balance
        cursor.execute("""
            UPDATE users SET wallet_balance = %s WHERE id = %s
        """, (new_balance, user_id))
        
        # Record transaction
        cursor.execute("""
            INSERT INTO wallet_transactions 
            (user_id, transaction_type, amount, balance_before, balance_after, description)
            VALUES (%s, 'deposit', %s, %s, %s, 'Money added to wallet')
        """, (user_id, amount, old_balance, new_balance))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"✅ User {user_id} added ₹{amount} to wallet")
        return jsonify({
            "message": "Money added successfully",
            "new_balance": new_balance
        }), 200
        
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"❌ Add money error: {e}")
        return jsonify({"error": "Failed to add money"}), 500

# ==================== TEST ROUTES ====================
@app.route("/test_session")
def test_session():
    return jsonify({
        "session": dict(session),
        "driver_id": session.get("driver_id"),
        "user_id": session.get("user_id")
    })

if __name__ == "__main__":
    # helpful debug listing of routes
    print("Registered routes:")
    print(app.url_map)
    app.run(debug=True)