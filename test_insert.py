import mysql.connector
from datetime import date

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="waste_management"
)

cursor = conn.cursor()

cursor.execute(
    "INSERT INTO wastedata (date, waste_type, quantity) VALUES (%s, %s, %s)",
    (date.today(), "wet", 99)
)
conn.commit()

print("Inserted successfully")
