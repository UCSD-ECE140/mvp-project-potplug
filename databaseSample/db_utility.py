import pymysql
from geopy.distance import geodesic

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

# Report a pothole (inserts entry into pothole table)
def report_pothole(latitude, longitude):
    connection = connect_to_database()
    try:
        with connection.cursor() as cursor:
            # Check if the pothole already exists
            cursor.execute("SELECT * FROM potholes WHERE latitude=%s AND longitude=%s", (latitude, longitude))
            existing_pothole = cursor.fetchone()
            if existing_pothole:
                cursor.execute("UPDATE potholes SET reports = reports + 1, last_report_date = %s WHERE id = %s", (datetime.now().date(), existing_pothole[0]))
            else:
                cursor.execute("INSERT INTO potholes (latitude, longitude, reports, last_report_date) VALUES (%s, %s, %s, %s)", (latitude, longitude, 1, datetime.now().date()))
        connection.commit()
    finally:
        connection.close()

# Report an incident (inserts entry into incident table)
def report_incident(latitude, longitude, user_id, date, time, severity):
    connection = connect_to_database()
    try:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO incident_reports (latitude, longitude, user_id, date, time, severity) VALUES (%s, %s, %s, %s, %s, %s)", (latitude, longitude, user_id, date, time, severity))
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
