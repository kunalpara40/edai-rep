import requests # Make sure 'requests' is installed: pip install requests
# import json
# # Load your ORS API key from .env or set it here temporarily
# ORS_API_KEY = os.getenv("ORS_API_KEY", "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6Ijg0MWNjMGU1OGNhYTQzZGFhMjM4NjYzMWY5Y2M1NTM3IiwiaCI6Im11cm11cjY0In0=") # Replace with your key

# # --- NEW ROUTING & GEOCODING ENDPOINT ---
# @app.route("/get_route_and_fare", methods=["POST"])
# def get_route_and_fare():
#     data = request.get_json()
#     pickup = data.get("pickup")
#     dropoff = data.get("dropoff")

#     if not pickup or not dropoff:
#         return jsonify({"error": "Pickup and dropoff locations required"}), 400

#     # 1. Geocoding (Convert addresses to coordinates)
#     def geocode_location(location):
#         url = "https://api.openrouteservice.org/geocode/search"
#         params = {
#             'api_key': ORS_API_KEY,
#             'text': location,
#             'boundary.country': 'IN', # Limit search to India
#             'size': 1 
#         }
#         response = requests.get(url, params=params)
#         if response.status_code == 200 and response.json()['features']:
#             coords = response.json()['features'][0]['geometry']['coordinates']
#             # ORS returns [Lon, Lat], we need [Lat, Lon] for Leaflet
#             return coords[1], coords[0] 
#         return None

#     pickup_lat, pickup_lon = geocode_location(pickup)
#     dropoff_lat, dropoff_lon = geocode_location(dropoff)

#     if not pickup_lat or not dropoff_lat:
#         return jsonify({"error": "Could not locate one or both addresses."}), 404

#     # 2. Routing (Get distance and route path)
#     profile = 'driving-car'
#     route_url = f"https://api.openrouteservice.org/v2/directions/{profile}"
#     headers = {'Authorization': ORS_API_KEY}
    
#     body = {
#         "coordinates": [
#             [pickup_lon, pickup_lat],
#             [dropoff_lon, dropoff_lat]
#         ]
#     }
    
#     route_response = requests.post(route_url, headers=headers, json=body)
#     route_data = route_response.json()

#     if route_response.status_code != 200 or 'routes' not in route_data:
#         # Log the route_data error for debugging if needed
#         return jsonify({"error": "Routing failed. Check API key or ORS server status."}), 500

#     # Extract distance (in meters, convert to km)
#     distance_km = route_data['routes'][0]['summary']['distance'] / 1000.0
    
#     # Get the geometry (path coordinates)
#     geometry_polyline = route_data['routes'][0]['geometry'] # GeoJSON format
    
#     # 3. Calculate Fare (using your existing logic from /calculate_fare)
#     # Note: Ensure BASE_RATE_PER_KM and BOOKING_FEE are defined globally in app.py
#     fare = calculate_solo_fare_logic(distance_km) 

#     return jsonify({
#         "status": "success",
#         "fare": fare,
#         "distance_km": round(distance_km, 2),
#         "pickup_coords": [pickup_lat, pickup_lon],
#         "dropoff_coords": [dropoff_lat, dropoff_lon],
#         "route_geometry": geometry_polyline # Send GeoJSON back to frontend
#     }), 200