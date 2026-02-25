import mysql.connector
from datetime import date


# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="waste_management"
)

cursor = conn.cursor()

# user Input 
waste_type = input("Enter waste type (wet/dry/e-waste): ").lower()
quantity = int(input("Enter quantity: "))
today = date.today()

#validation + classification
if waste_type not in ["wet", "dry", "e-waste"]:
    print("Invalid waste type")
else:
    query = "INSERT INTO wastedata (date, waste_type, quantity) VALUES (%s, %s, %s)"
    values = (today, waste_type, quantity)
    cursor.execute(query, values)
    conn.commit()
    print("Waste data stored successfully")

   








