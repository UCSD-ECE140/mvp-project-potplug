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

cursor.execute(f"SELECT * FROM incidents")
rows = cursor.fetchall()
print(f"Contents of table 'sampleusers':")
for row in rows:
    print(row)

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

cursor.close()
connection.close()
