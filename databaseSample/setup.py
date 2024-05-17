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
            length FLOAT,
            depth FLOAT,
            severity INT,
            date_time DATETIME,
            reports INT DEFAULT 0,
            last_report_date DATE
        )
    """)
    
    # Insert sample values into the 'potholes' table
    sample_potholes = [
        (40.7128, -74.0060, 1.2, 0.5, 5, '2023-01-01 12:00:00', 5, '2023-01-01'),
        (34.0522, -118.2437, 1.5, 0.7, 3, '2023-02-15 14:00:00', 3, '2023-02-15'),
        (41.8781, -87.6298, 2.0, 1.0, 7, '2023-03-20 09:30:00', 7, '2023-03-20')
    ]
    cursor.executemany("""
        INSERT INTO potholes (latitude, longitude, length, depth, severity, date_time, reports, last_report_date) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, sample_potholes)

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
            severity INT,
            incident_type VARCHAR(255)
        )
    """)
    
    # Insert sample values into the 'incident_reports' table
    sample_incident_reports = [
        (40.7128, -74.0060, 1, '2023-01-01', '12:00:00', 2, 'crash'),
        (34.0522, -118.2437, 2, '2023-02-15', '13:30:00', 1, 'speed bump'),
        (41.8781, -87.6298, 3, '2023-03-20', '11:45:00', 3, 'crash')
    ]
    cursor.executemany("""
        INSERT INTO incident_reports (latitude, longitude, user_id, date, time, severity, incident_type) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, sample_incident_reports)

# Check if the 'users' table exists
cursor.execute("SHOW TABLES LIKE 'users'")
users_table_exists = cursor.fetchone()

if not users_table_exists:
    # Create the 'users' table
    cursor.execute("""
        CREATE TABLE users (
            user_token VARCHAR(255) PRIMARY KEY,
            username VARCHAR(255),
            emergency_contact_name VARCHAR(255),
            emergency_contact_phone BIGINT,
            emergency_contact_carrier VARCHAR(255),
            user_phone BIGINT,
            user_carrier VARCHAR(255),
            sensitivity FLOAT,
            city_government VARCHAR(255)
        )
    """)
    
    # Insert sample values into the 'users' table
    sample_users = [
        ('google-oauth2|117344724568847202933', 'John Doe', None, None, None, None, None, None, None),
        ('google-oauth2|117344724568847202934', 'Jane Smith', None, None, None, None, None, None, None)
    ]
    cursor.executemany("""
        INSERT INTO users (user_token, username, emergency_contact_name, emergency_contact_phone, emergency_contact_carrier, user_phone, user_carrier, sensitivity, city_government) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, sample_users)

# Commit changes to the database
connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()