from flask import Flask, render_template, request
import numpy as np
import cv2
import os
from tensorflow.keras.models import load_model
import mysql.connector
from datetime import date

# Create static folder if not exists
if not os.path.exists("static"):
    os.makedirs("static")

app = Flask(__name__)

# Load model
model = load_model("model.h5")

# Classes
classes = ["dry", "ewaste", "wet"]

# ---------------- DATABASE FUNCTION ---------------- #
def save_to_db(waste):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="waste_management"
        )

        cursor = conn.cursor()

        cursor.execute(
            "SELECT quantity FROM wastedata WHERE date=%s AND waste_type=%s",
            (date.today(), waste)
        )

        result = cursor.fetchone()

        if result:
            new_quantity = result[0] + 1
            cursor.execute(
                "UPDATE wastedata SET quantity=%s WHERE date=%s AND waste_type=%s",
                (new_quantity, date.today(), waste)
            )
        else:
            cursor.execute(
                "INSERT INTO wastedata (date, waste_type, quantity) VALUES (%s, %s, %s)",
                (date.today(), waste, 1)
            )

        conn.commit()
        conn.close()

    except Exception as e:
        print("DB Error:", e)

# ---------------- ROUTES ---------------- #

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/predict', methods=['POST'])
def predict():
    files = request.files.getlist('image')
    results = []

    for file in files:
        filepath = os.path.join("static", file.filename)
        file.save(filepath)

        img = cv2.imread(filepath)
        img = cv2.resize(img, (128,128))
        img = img / 255.0
        img = np.reshape(img, [1,128,128,3])

        prediction = model.predict(img)
        confidence = np.max(prediction) * 100
        result = classes[np.argmax(prediction)]

        save_to_db(result)

        results.append({
            "result": result,
            "confidence": round(confidence, 2),
            "image": filepath
        })

    return render_template("result.html", results=results)


@app.route('/dashboard')
def dashboard():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="waste_management"
    )

    cursor = conn.cursor()

    cursor.execute("""
        SELECT TRIM(LOWER(waste_type)), SUM(quantity)
        FROM wastedata
        GROUP BY TRIM(LOWER(waste_type))
    """)

    data = cursor.fetchall()
    conn.close()

    labels = []
    values = []

    for row in data:
        labels.append(row[0])
        values.append(row[1])

    return render_template("dashboard.html", labels=labels, values=values)

# Run app
if __name__ == "__main__":
    app.run(debug=True)