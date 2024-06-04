import pymysql
from geopy.distance import geodesic
from datetime import datetime

# Set the database credentials
host = 'database-140b.c8qaipr0d2zt.us-east-1.rds.amazonaws.com'
port = 3306
user = 'admin'
password = 'ECE140B619'
database = 'database140b'

# Connect to the database
def connect_to_database():
    return pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )

# Add a new user
def add_user(user_identifier, username):
    connection = connect_to_database()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO users (user_token, username, emergency_contact_name, emergency_contact_phone, emergency_contact_carrier, user_phone, user_carrier, sensitivity, city_government)
                VALUES (%s, %s, NULL, NULL, NULL, NULL, NULL, NULL, NULL)
            """, (user_identifier, username))
        connection.commit()
    finally:
        connection.close()
    return {"message": "User added successfully."}

# Delete a user by ID
def delete_user(user_id):
    connection = connect_to_database()
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE user_token = %s", (user_id,))
        connection.commit()
    finally:
        connection.close()
    return {"message": "User deleted successfully."}

# Delete a pothole by ID
def delete_pothole(pothole_id):
    connection = connect_to_database()
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM potholes WHERE id = %s", (pothole_id,))
        connection.commit()
    finally:
        connection.close()
    return {"message": "Pothole deleted successfully."}

# Delete a incident by ID
def delete_incident(incident_id):
    connection = connect_to_database()
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM incident_reports WHERE id = %s", (incident_id,))
        connection.commit()
    finally:
        connection.close()
    return {"message": "User deleted successfully."}


# Update user information
def update_user(user_id, username=None, emergency_contact_name=None, emergency_contact_phone=None, emergency_contact_carrier=None, user_phone=None, user_carrier=None, sensitivity=None, city_government=None):
    connection = connect_to_database()
    try:
        with connection.cursor() as cursor:
            updates = []
            params = []
            if username:
                updates.append("username = %s")
                params.append(username)
            if emergency_contact_name:
                updates.append("emergency_contact_name = %s")
                params.append(emergency_contact_name)
            if emergency_contact_phone:
                updates.append("emergency_contact_phone = %s")
                params.append(emergency_contact_phone)
            if emergency_contact_carrier:
                updates.append("emergency_contact_carrier = %s")
                params.append(emergency_contact_carrier)
            if user_phone:
                updates.append("user_phone = %s")
                params.append(user_phone)
            if user_carrier:
                updates.append("user_carrier = %s")
                params.append(user_carrier)
            if sensitivity:
                updates.append("sensitivity = %s")
                params.append(sensitivity)
            if city_government:
                updates.append("city_government = %s")
                params.append(city_government)

            params.append(user_id)
            cursor.execute(f"UPDATE users SET {', '.join(updates)} WHERE user_token = %s", tuple(params))
        connection.commit()
    finally:
        connection.close()
    return {"message": "User updated successfully."}

# Update an incident
def update_incident(incident_id, latitude=None, longitude=None, user_id=None, date=None, time=None, severity=None, incident_type=None):
    connection = connect_to_database()
    try:
        with connection.cursor() as cursor:
            updates = []
            params = []
            if latitude:
                updates.append("latitude = %s")
                params.append(latitude)
            if longitude:
                updates.append("longitude = %s")
                params.append(longitude)
            if user_id:
                updates.append("user_id = %s")
                params.append(user_id)
            if date:
                updates.append("date = %s")
                params.append(date)
            if time:
                updates.append("time = %s")
                params.append(time)
            if severity:
                updates.append("severity = %s")
                params.append(severity)
            if incident_type:
                updates.append("incident_type = %s")
                params.append(incident_type)

            params.append(incident_id)
            cursor.execute(f"UPDATE incident_reports SET {', '.join(updates)} WHERE id = %s", tuple(params))
        connection.commit()
    finally:
        connection.close()
    return {"message": "Incident updated successfully."}

# List all users for debugging
def list_all_users():
    connection = connect_to_database()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            return users
    finally:
        connection.close()

# Report a pothole (inserts entry into pothole table)
def report_pothole(latitude, longitude, length, depth, severity, date_time=None):
    connection = connect_to_database()
    if date_time is None:
        date_time = datetime.now()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO potholes (latitude, longitude, length, depth, severity, date_time)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (latitude, longitude, length, depth, severity, date_time))
        connection.commit()
    finally:
        connection.close()

# Report an incident (inserts entry into incident table)
def report_incident(latitude, longitude, user_id, date, time, severity, incident_type):
    connection = connect_to_database()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO incident_reports (latitude, longitude, user_id, date, time, severity, incident_type)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (latitude, longitude, user_id, date, time, severity, incident_type))
        connection.commit()
    finally:
        connection.close()

# Get nearby potholes within a certain distance in miles
def fetch_nearby_potholes(latitude, longitude, distance):
    connection = connect_to_database()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM potholes")
            potholes = cursor.fetchall()
            nearby_potholes = []
            for pothole in potholes:
                pothole_latitude = pothole[1]
                pothole_longitude = pothole[2]
                pothole_location = (pothole_latitude, pothole_longitude)
                user_location = (latitude, longitude)
                if geodesic(user_location, pothole_location).miles <= distance:
                    nearby_potholes.append(pothole)
            return nearby_potholes
    finally:
        connection.close()

# Get all incidents
def get_all_incidents():
    connection = connect_to_database()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM incident_reports")
            incidents = cursor.fetchall()
            return incidents
    finally:
        connection.close()

# Get all incidents
def get_all_potholes():
    connection = connect_to_database()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM potholes")
            potholes_result = cursor.fetchall()
            potholes = []
            for ph in potholes_result:
                potholes.append(ph)
            return potholes
    finally:
        connection.close()


# Get user information by user identifier
def get_user(user_identifier):
    connection = connect_to_database()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE user_token = %s", (user_identifier,))
            user = cursor.fetchone()
            return user
    finally:
        connection.close()