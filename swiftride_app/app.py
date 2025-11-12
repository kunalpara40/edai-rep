
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

        if user and check_password_hash(str(user["password"]), str(data.get("password", ""))):
            session.clear()
            session["user_id"] = user["id"]
            session["firstName"] = user.get("firstName", "")
            session["email"] = user.get("email", "")
            session.permanent = True
            
            return jsonify({
                "message": "Login successful!",
                "user": {
                    "id": user["id"],
                    "firstName": user.get("firstName", ""),
                    "email": user.get("email", "")
                }
            }), 200
        else:
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
# @app.route("/driver/login", methods=["GET", "POST"])
# def driver_login():
   
#     if request.method == "GET":
#         if session.get("driver_id"):
#             return redirect("/driver/dashboard")
#         return render_template("index.html")

    
#     data = request.get_json(silent=True) or {}
#     print("\n=== DRIVER LOGIN ATTEMPT (DEBUG) ===")
#     print("Raw payload:", data)

#     phone = (data.get("phone") or "").strip()
#     email = (data.get("email") or "").strip()
#     password = data.get("password") or ""

  
#     if not password or (not phone and not email):
#         print("❌ Missing phone/email or password")
#         return jsonify({"error": "Phone/email and password required"}), 400

#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor(dictionary=True)

       
#         if phone:
#             print("Looking up driver by phone:", phone)
#             cursor.execute("SELECT * FROM drivers WHERE phone = %s LIMIT 1", (phone,))
#         else:
#             print("Looking up driver by email:", email)
#             cursor.execute("SELECT * FROM drivers WHERE email = %s LIMIT 1", (email,))

#         driver = cursor.fetchone()
#         cursor.close()
#         conn.close()

#         print("DB row (driver):", driver)

#         if not driver:
#             print("❌ No driver found for given identifier")
#             return jsonify({"error": "No driver found with provided phone/email"}), 404


#         stored_pw = None
#         for key in ("password", "password_hash", "pw", "pass", "passwd"):
#             if key in driver and driver[key]:
#                 stored_pw = driver[key]
#                 print(f"Found password column: {key}")
#                 break
#         if stored_pw is None:
            
#             print("Driver DB columns:", list(driver.keys()))
#             return jsonify({"error": "Server misconfigured: no password column found for driver"}), 500

     
#         def looks_like_hash(s):
#             return isinstance(s, str) and s.startswith(("pbkdf2:sha256","argon2","bcrypt","sha256"))

#         if looks_like_hash(stored_pw):
#             pw_ok = check_password_hash(stored_pw, password)
#             print("Password check (hashed):", pw_ok)
#         else:
          
#             pw_ok = (str(stored_pw) == str(password))
#             print("Password check (plain compare):", pw_ok, "| stored:", stored_pw)

#         if not pw_ok:
#             print("❌ Invalid password")
#             return jsonify({"error": "Invalid credentials"}), 401


#         driver_id = driver.get("driver_id") or driver.get("id") or driver.get("user_id")
#         try:
#             driver_id = int(driver_id) if driver_id is not None else None
#         except Exception:
#             pass

#         session.clear()
#         if driver_id:
#             session["driver_id"] = driver_id
#         else:
          
#             session["driver_id"] = driver.get("phone") or driver.get("email")

#         session["driver_firstName"] = str(driver.get("firstName") or driver.get("full_name") or "")
#         session["driver_email"] = str(driver.get("email") or "")
#         session["is_driver"] = True
#         session.permanent = True
#         session.modified = True

#         print(f"✅ Driver login successful. session driver_id: {session['driver_id']}")

#         return jsonify({
#             "message": "Driver login successful!",
#             "redirect": "/driver/dashboard",
#             "driver": {
#                 "id": session.get("driver_id"),
#                 "firstName": session.get("driver_firstName"),
#                 "email": session.get("driver_email")
#             }
#         }), 200

#     except Exception as e:
#         print("❌ Exception in driver_login:", e)
#         import traceback; traceback.print_exc()
#         return jsonify({"error": "Server error", "details": str(e)}), 500



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

@app.route("/driver/login", methods=["GET", "POST"])
def driver_login():
    if request.method == "GET":
        if session.get("driver_id"):
            return redirect("/driver/dashboard")
        return render_template("index.html")

    data = request.get_json(silent=True) or {}
    
    print("\n=== DRIVER LOGIN DEBUG ===")
    print("Payload received:", data)

    phone = (data.get("phone") or "").strip()
    email = (data.get("email") or "").strip()
    password = data.get("password") or ""

    print(f"Phone: {phone}")
    print(f"Email: {email}")
    print(f"Password provided: {bool(password)}")

    if not password or (not phone and not email):
        print("❌ Missing credentials")
        return jsonify({"error": "Phone/email and password required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Lookup driver by phone or email
        if phone:
            print(f"🔍 Looking up driver by phone: {phone}")
            cursor.execute("SELECT * FROM drivers WHERE phone = %s LIMIT 1", (phone,))
        else:
            print(f"🔍 Looking up driver by email: {email}")
            cursor.execute("SELECT * FROM drivers WHERE email = %s LIMIT 1", (email,))

        driver = cursor.fetchone()
        cursor.close()
        conn.close()

        if not driver:
            print("❌ No driver found")
            return jsonify({"error": "No driver found with provided credentials"}), 404

        print(f"✅ Driver found: {driver.get('full_name')} (ID: {driver.get('driver_id')})")
        print(f"Driver columns: {list(driver.keys())}")

        # Get the stored password hash
        stored_password = driver.get('password')
        
        if not stored_password:
            print("❌ No password stored in database!")
            return jsonify({"error": "Account configuration error"}), 500

        print(f"Stored password (first 50 chars): {stored_password[:50]}...")
        
        # Verify password using werkzeug's check_password_hash
        password_valid = check_password_hash(stored_password, password)
        print(f"Password verification result: {password_valid}")

        if not password_valid:
            print("❌ Invalid password")
            return jsonify({"error": "Invalid credentials"}), 401

        # Success! Set session
        driver_id = driver.get("driver_id") or driver.get("id")
        
        session.clear()
        session["driver_id"] = driver_id
        session["driver_firstName"] = driver.get("firstName") or driver.get("full_name", "").split()[0]
        session["driver_email"] = driver.get("email") or ""
        session["is_driver"] = True
        session.permanent = True

        print(f"✅ Login successful! Session: {dict(session)}")

        return jsonify({
            "message": "Driver login successful!",
            "redirect": "/driver/dashboard",
            "driver": {
                "id": driver_id,
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
        
        print(f"✅ Driver found: {driver.get('full_name')} (ID: {driver.get('driver_id')})")
        
        # Try to get rating and total_rides if columns exist
        try:
            cursor.execute("""
                SELECT rating, total_rides, total_earnings
                FROM drivers WHERE driver_id=%s
            """, (driver_id,))
            extra_stats = cursor.fetchone()
            if extra_stats:
                driver.update(extra_stats)
        except mysql.connector.Error as e:
            print(f"⚠️ Some driver stats columns don't exist yet: {e}")
            driver['rating'] = 0.0
            driver['total_rides'] = 0
            driver['total_earnings'] = 0.0
        
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
            print("⚠️ Active rides query failed, using empty list")
            active_rides = []
        
        cursor.close()
        conn.close()
        
        print("✅ Successfully rendering dashboard")
        return render_template(
            "driver_dashboard.html", 
            driver=driver, 
            stats=stats or {"total_rides": 0, "total_earnings": 0},
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
@app.route("/driver/accept_ride", methods=["POST"])
def driver_accept_ride():
    driver_id = session.get("driver_id")
    if not driver_id:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json() or {}
    ride_id = data.get("ride_id")
    
    if not ride_id:
        return jsonify({"error": "ride_id required"}), 400

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
        return jsonify({"message": "Ride accepted", "ride_id": ride_id}), 200

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Accept ride error: {e}")
        return jsonify({"error": "Accept failed"}), 500

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