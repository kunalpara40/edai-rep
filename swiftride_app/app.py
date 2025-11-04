# # app.py
# from flask import Flask, request, jsonify, render_template, session, redirect, url_for
# from werkzeug.security import generate_password_hash, check_password_hash
# from dotenv import load_dotenv
# import os
# import mysql.connector
# from mysql.connector import Error
# from flask_cors import CORS

# load_dotenv()

# app = Flask(__name__, template_folder="templates", static_folder="static")
# app.secret_key = os.getenv("SECRET_KEY", "dev_secret")
# # CORS(app)  # safe for dev. For production restrict origins.
# CORS(app, supports_credentials=True)

# def get_db_connection():
#     return mysql.connector.connect(
#         host=os.getenv("DB_HOST", "localhost"),
#         user=os.getenv("DB_USER", "root"),
#         password=os.getenv("DB_PASSWORD", ""),
#         database=os.getenv("DB_NAME", "swiftride"),
#         autocommit=False
#     )

# @app.route("/")
# def index():
#     return render_template("index.html")

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
#         (firstName, lastName, email, phone, password, address,state, city, zipCode, preferredPayment)
#         VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
#         """
#         values = (
#             data.get("firstName"),
#             data.get("lastName"),
#             data.get("email"),
#             data.get("phone"),
#             hashed_pw,
#             data.get("address"),
#             data.get("state"),
#             data.get("city"),
#             data.get("zipCode"),
#             data.get("preferredPayment")
#         )
#         cursor.execute(sql, values)
#         conn.commit()
#         cursor.close()
#         conn.close()
#         return jsonify({"message": "User created successfully!"}), 201
#     except mysql.connector.IntegrityError as ie:  # likely duplicate email
#         return jsonify({"error": "Email already registered"}), 409
#     except Exception as e:
#         # log e in real apps
#         return jsonify({"error": "Server error", "details": str(e)}), 500

# # @app.route("/login", methods=["POST"])
# # def login():
# #     data = request.get_json()
# #     if not data.get("email") or not data.get("password"):
# #         return jsonify({"error": "Email and password required"}), 400

# #     try:
# #         conn = get_db_connection()
# #         cursor = conn.cursor(dictionary=True)
# #         cursor.execute("SELECT * FROM users WHERE email = %s", (data.get("email"),))
# #         user = cursor.fetchone()
# #         cursor.close()
# #         conn.close()

# #         if user and check_password_hash(user["password"], data.get("password")):
# #             session["user_id"] = user["id"]
# #             return jsonify({"message": "Login successful!"})
# #         # if user and check_password_hash(user["password"], data.get("password")):
# #         #      session["user_id"] = user["id"]
# #         #      return jsonify({"message": "Login successful!", "redirect": "/landing"})

# #         else:
# #             return jsonify({"error": "Invalid email or password"}), 401
# #     except Exception as e:
# #         return jsonify({"error": "Server error", "details": str(e)}), 500
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
#             session["user_id"] = user["id"]
#             # store firstName to use in templates
#             session["firstName"] = user.get("firstName")
#             # Return user info also (optional)
#             return jsonify({"message": "Login successful!", "user": {"id": user["id"], "firstName": user.get("firstName")}})
#         else:
#             return jsonify({"error": "Invalid email or password"}), 401
#     except Exception as e:
#         return jsonify({"error": "Server error", "details": str(e)}), 500

# @app.route("/me")
# def me():
#     user_id = session.get("user_id")
#     if not user_id:
#         return jsonify({"error": "Not logged in"}), 401
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("SELECT id, firstName, lastName, email, phone, address, state, city, zipCode, preferredPayment FROM users WHERE id=%s", (user_id,))
#         user = cursor.fetchone()
#         cursor.close()
#         conn.close()
#         if not user:
#             return jsonify({"error": "User not found"}), 404
#         return jsonify({"user": user})
#     except Exception as e:
#         return jsonify({"error": "Server error", "details": str(e)}), 500
    
#  #USER PROFILE   
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
#         return jsonify({"message": "Profile updated successfully"})
#     except Exception as e:
#         return jsonify({"error": "Update failed", "details": str(e)}), 500
    

#  #FOR DELETING ACCOUNT   
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
#         return jsonify({"message": "Account deleted successfully"})
#     except Exception as e:
#         return jsonify({"error": "Delete failed", "details": str(e)}), 500

# #LOGOUT
# @app.route("/logout", methods=["POST"])
# def logout():
#     session.clear()
#     return jsonify({"message": "Logged out successfully"})

# #List All Users
# @app.route("/users", methods=["GET"])
# def list_users():
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("SELECT id, firstName, lastName, email,state, city, preferredPayment FROM users")
#         users = cursor.fetchall()
#         cursor.close()
#         conn.close()
#         return jsonify({"users": users})
#     except Exception as e:
#         return jsonify({"error": "Failed to fetch users", "details": str(e)}), 500

# #SEARCH USER BY EMAIL/CITY
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
#             return jsonify({"message": "No user found"})
#         return jsonify({"users": result})
#     except Exception as e:
#         return jsonify({"error": "Search failed", "details": str(e)}), 500
    
# #PASSWORD RESET 
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
#         return jsonify({"message": "Password updated successfully"})
#     except Exception as e:
#         return jsonify({"error": "Password reset failed", "details": str(e)}), 500

# # @app.route("/landing")
# # def landing():
# #     if "user_id" not in session:
# #         return render_template("index.html")  # if not logged in, send back to login
# #     return render_template("landing.html")
# # --- GLOBAL CONSTANTS ---
# # BASE_RATE_PER_KM = 12.0
# # BOOKING_FEE = 30.0

# # def calculate_pooled_fare_logic(D_AC, D_Shared, D_P_Exclusive, P_Exclusive_Owner):
# #     cost_ac = float(D_AC) * BASE_RATE_PER_KM
# #     cost_shared = float(D_Shared) * BASE_RATE_PER_KM
# #     cost_exclusive_final = float(D_P_Exclusive) * BASE_RATE_PER_KM

# #     cost_shared_per_person = cost_shared / 2.0

# #     fare_p1_base = cost_ac + cost_shared_per_person
# #     fare_p2_base = cost_shared_per_person

# #     if P_Exclusive_Owner == 'P1':
# #         fare_p1_base += cost_exclusive_final
# #     elif P_Exclusive_Owner == 'P2':
# #         fare_p2_base += cost_exclusive_final

# #     fare_p1_final = round(fare_p1_base + BOOKING_FEE, 2)
# #     fare_p2_final = round(fare_p2_base, 2)

# #     return {
# #         "fare_p1": fare_p1_final,
# #         "fare_p2": fare_p2_final,
# #         "fare_total_paid": round(fare_p1_final + fare_p2_final, 2),
# #         "total_distance": round(float(D_AC) + float(D_Shared) + float(D_P_Exclusive), 2)
# #     }

# # def calculate_solo_fare_logic(distance_km):
# #     return round((float(distance_km) * BASE_RATE_PER_KM) + BOOKING_FEE, 2)

# # # --- POOLING & FARE CALCULATION ENDPOINT ---
# # @app.route("/calculate_fare", methods=["POST"])
# # def calculate_fare():
# #     data = request.get_json()
# #     required_params = ["D_AC", "D_Shared", "D_P_Exclusive", "P_Exclusive_Owner"]

# #     for param in required_params:
# #         if param not in data:
# #             return jsonify({"error": f"Missing required parameter: {param}"}), 400

# #     try:
# #         D_AC = float(data.get("D_AC"))
# #         D_Shared = float(data.get("D_Shared"))
# #         D_P_Exclusive = float(data.get("D_P_Exclusive"))
# #         P_Exclusive_Owner = str(data.get("P_Exclusive_Owner"))

# #         result = calculate_pooled_fare_logic(D_AC, D_Shared, D_P_Exclusive, P_Exclusive_Owner)

# #         # Solo fare for P1
# #         if P_Exclusive_Owner == 'P1':
# #             D_P1_Solo = D_AC + D_Shared + D_P_Exclusive
# #         else:
# #             D_P1_Solo = D_AC + D_Shared

# #         solo_fare_p1 = calculate_solo_fare_logic(D_P1_Solo)

# #         return jsonify({
# #             "status": "success",
# #             "fare_pooled": {
# #                 "P1_Requester": result["fare_p1"],
# #                 "P2_Sharer": result["fare_p2"],
# #                 "total_paid": result["fare_total_paid"],
# #                 "total_distance_km": result["total_distance"]
# #             },
# #             "fare_solo_p1": solo_fare_p1,
# #             "savings_p1": round(solo_fare_p1 - result["fare_p1"], 2)
# #         }), 200

# #     except Exception as e:
# #         return jsonify({"error": "Fare calculation failed", "details": str(e)}), 500
# # @app.route('/')
# # def home():
# #     map_sdk_key = "80770a36d59caa869260ae69c9902da4"
# #     return render_template('index.html', map_sdk_key=map_sdk_key)
# # app.py additions:

# # import requests # Make sure 'requests' is installed: pip install requests
# # import json
# # # Load your ORS API key from .env or set it here temporarily
# # ORS_API_KEY = os.getenv("ORS_API_KEY", "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6Ijg0MWNjMGU1OGNhYTQzZGFhMjM4NjYzMWY5Y2M1NTM3IiwiaCI6Im11cm11cjY0In0=") # Replace with your key

# # # --- NEW ROUTING & GEOCODING ENDPOINT ---
# # @app.route("/get_route_and_fare", methods=["POST"])
# # def get_route_and_fare():
# #     data = request.get_json()
# #     pickup = data.get("pickup")
# #     dropoff = data.get("dropoff")

# #     if not pickup or not dropoff:
# #         return jsonify({"error": "Pickup and dropoff locations required"}), 400

# #     # 1. Geocoding (Convert addresses to coordinates)
# #     def geocode_location(location):
# #         url = "https://api.openrouteservice.org/geocode/search"
# #         params = {
# #             'api_key': ORS_API_KEY,
# #             'text': location,
# #             'boundary.country': 'IN', # Limit search to India
# #             'size': 1 
# #         }
# #         response = requests.get(url, params=params)
# #         if response.status_code == 200 and response.json()['features']:
# #             coords = response.json()['features'][0]['geometry']['coordinates']
# #             # ORS returns [Lon, Lat], we need [Lat, Lon] for Leaflet
# #             return coords[1], coords[0] 
# #         return None

# #     pickup_lat, pickup_lon = geocode_location(pickup)
# #     dropoff_lat, dropoff_lon = geocode_location(dropoff)

# #     if not pickup_lat or not dropoff_lat:
# #         return jsonify({"error": "Could not locate one or both addresses."}), 404

# #     # 2. Routing (Get distance and route path)
# #     profile = 'driving-car'
# #     route_url = f"https://api.openrouteservice.org/v2/directions/{profile}"
# #     headers = {'Authorization': ORS_API_KEY}
    
# #     body = {
# #         "coordinates": [
# #             [pickup_lon, pickup_lat],
# #             [dropoff_lon, dropoff_lat]
# #         ]
# #     }
    
# #     route_response = requests.post(route_url, headers=headers, json=body)
# #     route_data = route_response.json()

# #     if route_response.status_code != 200 or 'routes' not in route_data:
# #         # Log the route_data error for debugging if needed
# #         return jsonify({"error": "Routing failed. Check API key or ORS server status."}), 500

# #     # Extract distance (in meters, convert to km)
# #     distance_km = route_data['routes'][0]['summary']['distance'] / 1000.0
    
# #     # Get the geometry (path coordinates)
# #     geometry_polyline = route_data['routes'][0]['geometry'] # GeoJSON format
    
# #     # 3. Calculate Fare (using your existing logic from /calculate_fare)
# #     # Note: Ensure BASE_RATE_PER_KM and BOOKING_FEE are defined globally in app.py
# #     fare = calculate_solo_fare_logic(distance_km) 

# #     return jsonify({
# #         "status": "success",
# #         "fare": fare,
# #         "distance_km": round(distance_km, 2),
# #         "pickup_coords": [pickup_lat, pickup_lon],
# #         "dropoff_coords": [dropoff_lat, dropoff_lon],
# #         "route_geometry": geometry_polyline # Send GeoJSON back to frontend
# #     }), 200

# # Remember to update your .env file with ORS_API_KEY
# # ORS_API_KEY="YOUR_API_KEY"
# # @app.route("/dashboard")
# # def dashboard():
# #     # optionally check session here and redirect if not logged-in
# #     if "user_id" not in session:
# #         return redirect(url_for('index'))
# #     return render_template("dashboard.html")
# # --- create_ride endpoint (insert a requested ride) ---
# @app.route("/create_ride", methods=["POST"])
# def create_ride():
#     """
#     Request body JSON:
#     {
#       "pickup_lat": float,
#       "pickup_lng": float,
#       "drop_lat": float,
#       "drop_lng": float
#     }
#     """
#     user_id = session.get("user_id")
#     if not user_id:
#         return jsonify({"error": "Not logged in"}), 401

#     data = request.get_json() or {}
#     required = ["pickup_lat", "pickup_lng", "drop_lat", "drop_lng"]
#     for r in required:
#         if r not in data:
#             return jsonify({"error": f"{r} is required"}), 400

#     conn = None
#     cursor = None
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         sql = """
#         INSERT INTO rides (user_id, pickup_lat, pickup_lng, drop_lat, drop_lng, status, requested_at)
#         VALUES (%s, %s, %s, %s, 'requested', NOW())
#         """
#         cursor.execute(sql, (user_id, data["pickup_lat"], data["pickup_lng"], data["drop_lat"], data["drop_lng"]))
#         conn.commit()
#         ride_id = cursor.lastrowid
#         return jsonify({"message": "Ride requested", "ride_id": ride_id}), 201
#     except Exception as e:
#         if conn:
#             conn.rollback()
#         print("create_ride error:", repr(e))
#         return jsonify({"error": "Create ride failed"}), 500
#     finally:
#         if cursor:
#             cursor.close()
#         if conn:
#             conn.close()

# # --- assign_driver endpoint (transactional) ---
# @app.route("/assign_driver", methods=["POST"])
# def assign_driver():
#     """
#     Assigns an available driver to a ride in a transaction.
#     Request body JSON: { "ride_id": <int> }
#     """
#     data = request.get_json() or {}
#     ride_id = data.get("ride_id")
#     if not ride_id:
#         return jsonify({"error": "ride_id required"}), 400

#     conn = None
#     cursor = None
#     try:
#         conn = get_db_connection()
#         # begin transaction explicitly
#         conn.start_transaction()
#         cursor = conn.cursor()

#         # Lock candidate driver row(s). For now pick the first available driver.
#         # If you want nearest driver, JOIN with driver_locations and add WHERE bounding box.
#         cursor.execute("SELECT driver_id FROM drivers WHERE status='available' LIMIT 1 FOR UPDATE")
#         row = cursor.fetchone()
#         if not row:
#             conn.rollback()
#             return jsonify({"error": "No available drivers right now"}), 409

#         driver_id = row[0]

#         # assign ride and mark assigned_at, status
#         cursor.execute("""
#             UPDATE rides
#             SET driver_id=%s, status='assigned', assigned_at=NOW()
#             WHERE ride_id=%s AND status='requested'
#         """, (driver_id, ride_id))

#         if cursor.rowcount == 0:
#             # ride may have been assigned/cancelled already
#             conn.rollback()
#             return jsonify({"error": "Ride not in requested state or not found"}), 409

#         # set driver to busy
#         cursor.execute("UPDATE drivers SET status='busy', updated_at=NOW() WHERE driver_id=%s", (driver_id,))

#         conn.commit()
#         return jsonify({"message": "Driver assigned", "driver_id": driver_id, "ride_id": ride_id})
#     except Exception as e:
#         if conn:
#             conn.rollback()
#         print("assign_driver error:", repr(e))
#         return jsonify({"error": "Assignment failed"}), 500
#     finally:
#         if cursor:
#             cursor.close()
#         if conn:
#             conn.close()



# if __name__ == "__main__":
#     # Run on http://127.0.0.1:5000
#     app.run(debug=True)


from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
import mysql.connector
from mysql.connector import Error
from flask_cors import CORS

load_dotenv()

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.getenv("SECRET_KEY", "dev_secret_change_in_production")
CORS(app, supports_credentials=True)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "swiftride"),
        autocommit=False
    )

# MAIN ROUTE - Renders homepage with authentication state
@app.route("/")
def index():
    # Session is automatically available in Jinja templates
    # If user is logged in, session['user_id'] will be set
    return render_template("index.html")

# SIGNUP ENDPOINT
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
            data.get("phone"),
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

# LOGIN ENDPOINT
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
            # Set session data
            session["user_id"] = user["id"]
            session["firstName"] = user.get("firstName", "")
            session["email"] = user.get("email", "")
            
            return jsonify({
                "message": "Login successful!",
                "user": {
                    "id": user["id"],
                    "firstName": user.get("firstName"),
                    "email": user.get("email")
                }
            }), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({"error": "Server error", "details": str(e)}), 500

# LOGOUT ENDPOINT
@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200

# GET CURRENT USER INFO
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

# UPDATE PROFILE
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

# DELETE ACCOUNT
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

# LIST ALL USERS (Admin functionality)
@app.route("/users", methods=["GET"])
def list_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, firstName, lastName, email, state, city, preferredPayment FROM users")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({"users": users}), 200
    except Exception as e:
        print(f"List users error: {e}")
        return jsonify({"error": "Failed to fetch users", "details": str(e)}), 500

# SEARCH USER BY EMAIL/CITY
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
            return jsonify({"message": "No user found"}), 404
        return jsonify({"users": result}), 200
    except Exception as e:
        print(f"Search user error: {e}")
        return jsonify({"error": "Search failed", "details": str(e)}), 500

# PASSWORD RESET
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
        return jsonify({"message": "Password updated successfully"}), 200
    except Exception as e:
        print(f"Reset password error: {e}")
        return jsonify({"error": "Password reset failed", "details": str(e)}), 500

# CREATE RIDE (Authenticated users only)
@app.route("/create_ride", methods=["POST"])
def create_ride():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json() or {}
    required = ["pickup_lat", "pickup_lng", "drop_lat", "drop_lng"]
    for r in required:
        if r not in data:
            return jsonify({"error": f"{r} is required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
        INSERT INTO rides (user_id, pickup_lat, pickup_lng, drop_lat, drop_lng, status, requested_at)
        VALUES (%s, %s, %s, %s, %s, 'requested', NOW())
        """
        cursor.execute(sql, (user_id, data["pickup_lat"], data["pickup_lng"], 
                            data["drop_lat"], data["drop_lng"]))
        conn.commit()
        ride_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({"message": "Ride requested", "ride_id": ride_id}), 201
    except Exception as e:
        print(f"Create ride error: {e}")
        return jsonify({"error": "Create ride failed", "details": str(e)}), 500

# ASSIGN DRIVER (Transactional)
@app.route("/assign_driver", methods=["POST"])
def assign_driver():
    data = request.get_json() or {}
    ride_id = data.get("ride_id")
    if not ride_id:
        return jsonify({"error": "ride_id required"}), 400

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        conn.start_transaction()
        cursor = conn.cursor()

        cursor.execute("SELECT driver_id FROM drivers WHERE status='available' LIMIT 1 FOR UPDATE")
        row = cursor.fetchone()
        if not row:
            conn.rollback()
            return jsonify({"error": "No available drivers right now"}), 409

        driver_id = row[0]

        cursor.execute("""
            UPDATE rides
            SET driver_id=%s, status='assigned', assigned_at=NOW()
            WHERE ride_id=%s AND status='requested'
        """, (driver_id, ride_id))

        if cursor.rowcount == 0:
            conn.rollback()
            return jsonify({"error": "Ride not in requested state or not found"}), 409

        cursor.execute("UPDATE drivers SET status='busy', updated_at=NOW() WHERE driver_id=%s", (driver_id,))

        conn.commit()
        return jsonify({"message": "Driver assigned", "driver_id": driver_id, "ride_id": ride_id}), 200
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Assign driver error: {e}")
        return jsonify({"error": "Assignment failed", "details": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    app.run(debug=True)