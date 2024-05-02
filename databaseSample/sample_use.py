#SAMPLE CODE TO ACCESS DATABASE

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

try:
    # Verify if tables exist
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    if tables:
        print("Tables in the database:")
        for table in tables:
            print(table[0])
    else:
        print("No tables found in the database.")

    # Print contents of all tables
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        print(f"Contents of table '{table_name}':")
        for row in rows:
            print(row)

    # Print status of the database
    cursor.execute("SHOW TABLE STATUS")
    status = cursor.fetchall()
    print("\nDatabase status:")
    for stat in status:
        print(stat)

except pymysql.Error as e:
    print("Error:", e)

# Close the cursor and connection
cursor.close()
connection.close()
