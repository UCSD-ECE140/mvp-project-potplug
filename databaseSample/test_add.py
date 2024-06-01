import pymysql

host = 'database-140b.c8qaipr0d2zt.us-east-1.rds.amazonaws.com'
port = 3306
user = 'admin'
password = 'ECE140B619'
database = 'database140b'

connection = pymysql.connect(
    host=host,
    port=port,
    user=user,
    password=password,
    database=database
)

cursor = connection.cursor()


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


cursor.execute(f"SELECT * FROM potholes")
rows = cursor.fetchall()
print(f"Contents of table 'sampleusers':")
for row in rows:
    print(row)

# Print status of the database
cursor.execute("SHOW TABLE STATUS")
status = cursor.fetchall()
print("\nDatabase status:")
for stat in status:
    print(stat)

cursor.execute("SELECT * FROM potholes")
potholes_result = cursor.fetchall()
potholes = []
for ph in potholes_result:
    potholes.append(ph)
print(potholes)

connection.commit()

cursor.close()
connection.close()
