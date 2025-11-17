from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from datetime import timedelta, datetime
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
        (firstName, lastName, email, phone, password, address, state, city, zipCode, preferredPayment, wallet_balance)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, 2000.00)
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
            # CLEAR any driver session first
            session.pop('driver_id', None)
            session.pop('is_driver', None)
            session.pop('driver_firstName', None)
            session.pop('driver_email', None)
            
            # Set user session
            session["user_id"] = user["user_id"]
            session["firstName"] = user.get("firstName", "")
            session["email"] = user.get("email", "")
            session["is_user"] = True
            session.permanent = True
            session.modified = True
            
            print(f"✅ User login successful: {user['user_id']}")
            print(f"   Session data: {dict(session)}")
            
            return jsonify({
                "message": "Login successful!",
                "user": {
                    "user_id": user["user_id"],
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
    print(f"🔍 /me endpoint - Session: {dict(session)}")
    
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT user_id, firstName, lastName, email, phone, address, state, city, zipCode, preferredPayment, wallet_balance
            FROM users WHERE user_id=%s
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

# ==================== DRIVER AUTH ====================
@app.route("/driver/signup", methods=["GET", "POST"])
def driver_signup():
    if request.method == "GET":
        return jsonify({"message": "Driver signup endpoint. POST form-data to create a driver."}), 200

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

    firstName = data.get("firstName", "").strip()
    lastName = data.get("lastName", "").strip()
    full_name = data.get("full_name", "").strip()
    
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

    if not full_name:
        return jsonify({"error": "Full name is required (or provide firstName and lastName)"}), 400
    
    if not phone:
        return jsonify({"error": "Phone number is required"}), 400
    
    if not password:
        return jsonify({"error": "Password is required"}), 400

    if not phone.isdigit() or len(phone) != 10:
        return jsonify({"error": "Phone must be exactly 10 digits"}), 400

    try:
        hashed_pw = generate_password_hash(password)
        conn = get_db_connection()
        cursor = conn.cursor()
        
        sql = """
        INSERT INTO drivers
          (full_name, firstName, lastName, phone, email, license_no, license_path, 
           vehicle_type, vehicle_make, vehicle_model, license_plate, password, status, wallet_balance)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 0.00)
        """
        
        values = (
            full_name,
            firstName or None,
            lastName or None,
            phone,
            email or None,
            license_no or None,
            license_path or None,
            vehicle_type or None,
            data.get("vehicle_make", "").strip() or None,
            data.get("vehicle_model", "").strip() or None,
            data.get("license_plate", "").strip() or None,
            hashed_pw,
            "offline"
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

@app.route("/driver/login", methods=["GET", "POST"])
def driver_login():
    if request.method == "GET":
        if session.get("driver_id"):
            return redirect("/driver/dashboard")
        return render_template("index.html")

    data = request.get_json(silent=True) or {}
    
    phone = (data.get("phone") or "").strip()
    email = (data.get("email") or "").strip()
    password = data.get("password") or ""

    if not password or (not phone and not email):
        return jsonify({"error": "Phone/email and password required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if phone:
            cursor.execute("SELECT * FROM drivers WHERE phone = %s LIMIT 1", (phone,))
        else:
            cursor.execute("SELECT * FROM drivers WHERE email = %s LIMIT 1", (email,))

        driver = cursor.fetchone()
        cursor.close()
        conn.close()

        if not driver:
            return jsonify({"error": "No driver found with provided credentials"}), 404

        stored_password = driver.get('password')
        
        if not stored_password:
            return jsonify({"error": "Account configuration error"}), 500

        password_valid = check_password_hash(stored_password, password)

        if not password_valid:
            return jsonify({"error": "Invalid credentials"}), 401

        driver_id = driver.get("driver_id") or driver.get("id")
        
        # CLEAR any user session first
        session.pop('user_id', None)
        session.pop('is_user', None)
        session.pop('firstName', None)
        session.pop('email', None)
        
        # Set driver session
        session["driver_id"] = driver_id
        session["driver_firstName"] = driver.get("firstName") or driver.get("full_name", "").split()[0]
        session["driver_email"] = driver.get("email") or ""
        session["is_driver"] = True
        session.permanent = True
        session.modified = True

        print(f"✅ Driver login successful! ID: {driver_id}")
        print(f"   Session data: {dict(session)}")

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
        
        cursor.execute("""
            SELECT driver_id, firstName, lastName, full_name, email, phone, 
                   license_no, vehicle_type, vehicle_make, vehicle_model, 
                   license_plate, status, wallet_balance
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
@app.route("/create_ride", methods=["POST"])
def create_ride():
    """User creates a new ride request"""
    user_id = session.get("user_id")
    
    print(f"🔍 Create ride - Session: {dict(session)}")
    
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json() or {}
    
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
            JOIN users u ON r.user_id = u.user_id
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

@app.route("/driver/accept_ride", methods=["POST"])
def driver_accept_ride():
    """Driver accepts a ride request - ENHANCED VERSION"""
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

        # Get ride details with user info for notification
        cursor.execute("""
            SELECT r.ride_id, r.user_id, r.status, r.driver_id, u.firstName as user_name
            FROM rides r 
            JOIN users u ON r.user_id = u.user_id
            WHERE r.ride_id=%s AND r.status='requested' AND r.driver_id IS NULL
            FOR UPDATE
        """, (ride_id,))
        
        ride = cursor.fetchone()
        
        if not ride:
            conn.rollback()
            cursor.close()
            conn.close()
            return jsonify({"error": "Ride not available or already accepted"}), 409

        # Update ride with driver assignment
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

        # Update driver status
        cursor.execute("""
            UPDATE drivers 
            SET status='busy' 
            WHERE driver_id=%s
        """, (driver_id,))

        # Get driver details for response
        cursor.execute("""
            SELECT full_name, phone, vehicle_type, license_plate 
            FROM drivers WHERE driver_id=%s
        """, (driver_id,))
        driver = cursor.fetchone()

        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"✅ Driver {driver_id} accepted ride {ride_id}")
        print(f"   User {ride['user_id']} will see driver: {driver['full_name']}")
        
        return jsonify({
            "message": "Ride accepted successfully", 
            "ride_id": ride_id,
            "driver": driver
        }), 200

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

@app.route("/user/ride_status/<int:ride_id>", methods=["GET"])
def get_ride_status(ride_id):
    """Get current status of a ride with driver location"""
    user_id = session.get("user_id")
    
    print(f"🔍 Get ride status - Session: {dict(session)}")
    print(f"🔍 User ID: {user_id}, Ride ID: {ride_id}")
    
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
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
                r.completed_at,
                r.payment_status
            FROM rides r
            WHERE r.ride_id = %s AND r.user_id = %s
        """, (ride_id, user_id))
        
        ride = cursor.fetchone()
        
        if not ride:
            cursor.close()
            conn.close()
            return jsonify({"error": "Ride not found"}), 404
        
        driver = None
        
        if ride['driver_id']:
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
            """, (ride['driver_id'],))
            
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
        return jsonify({"error": "Failed to get ride status"}), 500

# ==================== ENHANCED RIDE STATUS UPDATES ====================
@app.route("/user/ride_updates/<int:ride_id>", methods=["GET"])
def get_ride_updates(ride_id):
    """Get real-time updates for a specific ride"""
    user_id = session.get("user_id")
    
    print(f"🔍 Ride updates request - Ride ID: {ride_id}, User ID: {user_id}")
    
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get ride with driver details
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
            return jsonify({"error": "Ride not found"}), 404
        
        print(f"✅ Ride status: {ride['status']}, Driver: {ride.get('driver_name', 'None')}")
        
        return jsonify({
            "ride": ride,
            "last_updated": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        print(f"❌ Ride updates error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Failed to get ride updates"}), 500

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
        """, (lat, lng, driver_id))
        
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
        
        cursor.execute("""
            UPDATE rides
            SET status = 'completed', completed_at = NOW()
            WHERE ride_id = %s AND driver_id = %s AND status = 'in_progress'
        """, (ride_id, driver_id))
        
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return jsonify({"error": "Cannot complete this ride"}), 400
        
        cursor.execute("""
            UPDATE drivers
            SET status = 'available'
            WHERE driver_id = %s
        """, (driver_id,))
        
        try:
            cursor.execute("""
                UPDATE drivers d
                JOIN rides r ON d.driver_id = r.driver_id
                SET d.total_rides = d.total_rides + 1,
                    d.total_earnings = d.total_earnings + r.fare
                WHERE d.driver_id = %s AND r.ride_id = %s
            """, (driver_id, ride_id))
        except:
            pass
        
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

# ==================== WALLET SYSTEM ====================
@app.route("/user/wallet_balance", methods=["GET"])
def get_user_wallet_balance():
    """Get user's current wallet balance"""
    user_id = session.get("user_id")
    
    print(f"🔍 Wallet balance request - Session: {dict(session)}")
    print(f"🔍 User ID from session: {user_id}")
    
    if not user_id:
        return jsonify({
            "error": "Not logged in", 
            "session_data": dict(session),
            "has_cookies": bool(request.cookies)
        }), 401

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT user_id, firstName, lastName, wallet_balance
            FROM users WHERE user_id = %s
        """, (user_id,))
        
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not user:
            print(f"❌ User not found in database for ID: {user_id}")
            return jsonify({"error": "User not found"}), 404
        
        print(f"✅ Wallet balance retrieved: ₹{user['wallet_balance']}")
        
        return jsonify({
            "wallet_balance": float(user['wallet_balance']),
            "user_name": f"{user['firstName']} {user['lastName']}"
        }), 200
        
    except Exception as e:
        print(f"❌ Get wallet balance error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Failed to get wallet balance", "details": str(e)}), 500

@app.route("/driver/wallet_balance", methods=["GET"])
def get_driver_wallet_balance():
    """Get driver's current wallet balance"""
    driver_id = session.get("driver_id")
    if not driver_id:
        return jsonify({"error": "Not logged in"}), 401

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT driver_id, full_name, wallet_balance
            FROM drivers WHERE driver_id = %s
        """, (driver_id,))
        
        driver = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not driver:
            return jsonify({"error": "Driver not found"}), 404
        
        return jsonify({
            "wallet_balance": float(driver['wallet_balance']),
            "driver_name": driver['full_name']
        }), 200
        
    except Exception as e:
        print(f"❌ Get driver wallet balance error: {e}")
        return jsonify({"error": "Failed to get wallet balance"}), 500

@app.route("/user/confirm_payment", methods=["POST"])
def confirm_payment():
    """User confirms wallet payment - transfers money from user to driver"""
    user_id = session.get("user_id")
    
    print(f"🔍 Payment request - Session: {dict(session)}")
    print(f"🔍 User ID: {user_id}")
    
    if not user_id:
        print("❌ No user_id in session")
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
        
        # Get ride details with wallet balances
        cursor.execute("""
            SELECT r.ride_id, r.user_id, r.driver_id, r.fare, r.status, r.payment_status,
                   u.wallet_balance as user_wallet,
                   d.wallet_balance as driver_wallet
            FROM rides r
            JOIN users u ON r.user_id = u.user_id
            LEFT JOIN drivers d ON r.driver_id = d.driver_id
            WHERE r.ride_id = %s AND r.user_id = %s
            FOR UPDATE
        """, (ride_id, user_id))
        
        ride = cursor.fetchone()
        
        if not ride:
            conn.rollback()
            cursor.close()
            conn.close()
            return jsonify({"error": "Ride not found"}), 404
        
        if ride['payment_status'] == 'paid':
            conn.rollback()
            cursor.close()
            conn.close()
            return jsonify({"error": "Payment already completed"}), 400
        
        if not ride['driver_id']:
            conn.rollback()
            cursor.close()
            conn.close()
            return jsonify({"error": "No driver assigned to this ride"}), 400
        
        fare = float(ride['fare'])
        user_wallet = float(ride['user_wallet'])
        driver_wallet = float(ride['driver_wallet'])
        
        print(f"💰 Payment processing:")
        print(f"   Fare: ₹{fare}")
        print(f"   User wallet: ₹{user_wallet}")
        print(f"   Driver wallet: ₹{driver_wallet}")
        
        # Check if user has sufficient balance
        if user_wallet < fare:
            conn.rollback()
            cursor.close()
            conn.close()
            return jsonify({
                "error": "Insufficient wallet balance",
                "required": fare,
                "available": user_wallet
            }), 400
        
        # Calculate new balances
        new_user_balance = user_wallet - fare
        new_driver_balance = driver_wallet + fare
        
        # Deduct from user wallet
        cursor.execute("""
            UPDATE users
            SET wallet_balance = %s
            WHERE user_id = %s
        """, (new_user_balance, user_id))
        
        # Add to driver wallet
        cursor.execute("""
            UPDATE drivers
            SET wallet_balance = %s, total_earnings = total_earnings + %s
            WHERE driver_id = %s
        """, (new_driver_balance, fare, ride['driver_id']))
        
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
        """, (user_id, ride_id, -fare, user_wallet, new_user_balance, 
              f"Payment for Ride #{ride_id}"))
        
        # Record transaction for driver (credit)
        cursor.execute("""
            INSERT INTO wallet_transactions 
            (driver_id, ride_id, transaction_type, amount, balance_before, balance_after, description)
            VALUES (%s, %s, 'ride_payment', %s, %s, %s, %s)
        """, (ride['driver_id'], ride_id, fare, driver_wallet, new_driver_balance,
              f"Received payment for Ride #{ride_id}"))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"✅ Payment successful: User {user_id} paid ₹{fare} to Driver {ride['driver_id']}")
        print(f"   User balance: ₹{user_wallet} → ₹{new_user_balance}")
        print(f"   Driver balance: ₹{driver_wallet} → ₹{new_driver_balance}")
        
        return jsonify({
            "message": "Payment successful",
            "fare": fare,
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

@app.route("/user/add_money", methods=["POST"])
def add_money_to_wallet():
    """Add money to user wallet (for testing/top-up)"""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json() or {}
    amount = data.get("amount")
    
    if not amount or amount <= 0:
        return jsonify({"error": "Invalid amount"}), 400

    try:
        conn = get_db_connection()
        conn.start_transaction()
        cursor = conn.cursor(dictionary=True)
        
        # Get current balance
        cursor.execute("""
            SELECT wallet_balance FROM users WHERE user_id = %s FOR UPDATE
        """, (user_id,))
        
        user = cursor.fetchone()
        old_balance = float(user['wallet_balance'])
        new_balance = old_balance + float(amount)
        
        # Update balance
        cursor.execute("""
            UPDATE users SET wallet_balance = %s WHERE user_id = %s
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

# ==================== DEBUG ENDPOINTS ====================
@app.route("/debug/session", methods=["GET"])
def debug_session():
    """Debug endpoint to check session status"""
    return jsonify({
        "session_data": dict(session),
        "user_id": session.get("user_id"),
        "is_user": session.get("is_user"),
        "driver_id": session.get("driver_id"),
        "is_driver": session.get("is_driver"),
        "session_permanent": session.permanent,
        "cookies_received": list(request.cookies.keys())
    }), 200

@app.route("/_debug/routes", methods=["GET"])
def _debug_routes():
    """Debug endpoint to list all registered routes"""
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            "endpoint": rule.endpoint,
            "rule": str(rule),
            "methods": sorted([m for m in rule.methods if m not in ("HEAD", "OPTIONS")])
        })
    return jsonify({"routes": routes})

if __name__ == "__main__":
    # Debug listing of routes
    print("\n=== 🚀 SwiftRide Server Starting ===")
    print("Registered routes:")
    for rule in app.url_map.iter_rules():
        methods = ','.join([m for m in rule.methods if m not in ("HEAD", "OPTIONS")])
        print(f"  {rule.rule:50} [{methods}]")
    print("=" * 60 + "\n")
    
    app.run(debug=True, port=5000)
