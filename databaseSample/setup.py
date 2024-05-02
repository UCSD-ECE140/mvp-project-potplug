# ALREADY RUN, NO NEED TO RUN AGAIN

import pymysql
from datetime import datetime

# Set the database credentials
host = 'database-140b.c8qaipr0d2zt.us-east-1.rds.amazonaws.com'
port = 3306
user = 'admin'
password = 'ECE140B619'
database = 'database140b'


# Connect to the database
connection = pymysql.connect(
    host=host,
    port=port,
    user=user,
    password=password,
    database=database
)

# Create a cursor object
cursor = connection.cursor()

# Check if the database exists
cursor.execute("SHOW DATABASES LIKE '{}'".format(database))
database_exists = cursor.fetchone()

if not database_exists:
    # Create the database if it doesn't exist
    cursor.execute("CREATE DATABASE {}".format(database))

# Use the specified database
cursor.execute("USE {}".format(database))

# Check if the 'potholes' table exists
cursor.execute("SHOW TABLES LIKE 'potholes'")
potholes_table_exists = cursor.fetchone()

if not potholes_table_exists:
    # Create the 'potholes' table
    cursor.execute("""
        CREATE TABLE potholes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            latitude DECIMAL(10, 8),
            longitude DECIMAL(11, 8),
            reports INT DEFAULT 0,
            last_report_date DATE
        )
    """)
    
    # Insert sample values into the 'potholes' table
    sample_potholes = [
        (40.7128, -74.0060, 5, '2023-01-01'),
        (34.0522, -118.2437, 3, '2023-02-15'),
        (41.8781, -87.6298, 7, '2023-03-20')
    ]
    cursor.executemany("INSERT INTO potholes (latitude, longitude, reports, last_report_date) VALUES (%s, %s, %s, %s)", sample_potholes)

# Check if the 'incident_reports' table exists
cursor.execute("SHOW TABLES LIKE 'incident_reports'")
incident_reports_table_exists = cursor.fetchone()

if not incident_reports_table_exists:
    # Create the 'incident_reports' table
    cursor.execute("""
        CREATE TABLE incident_reports (
            id INT AUTO_INCREMENT PRIMARY KEY,
            latitude DECIMAL(10, 8),
            longitude DECIMAL(11, 8),
            user_id INT,
            date DATE,
            time TIME,
            severity INT
        )
    """)
    
    # Insert sample values into the 'incident_reports' table
    sample_incident_reports = [
        (40.7128, -74.0060, 1, '2023-01-01', '12:00:00', 2),
        (34.0522, -118.2437, 2, '2023-02-15', '13:30:00', 1),
        (41.8781, -87.6298, 3, '2023-03-20', '11:45:00', 3)
    ]
    cursor.executemany("INSERT INTO incident_reports (latitude, longitude, user_id, date, time, severity) VALUES (%s, %s, %s, %s, %s, %s)", sample_incident_reports)

# Commit changes to the database
connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()
