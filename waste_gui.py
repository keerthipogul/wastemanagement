import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import mysql.connector
from datetime import date

# Model initially empty
model = None

# Classes (must match training)
classes = ["dry", "ewaste", "wet"]

# GUI Window
root = tk.Tk()
root.title("Waste Management System")
root.geometry("400x350")

tk.Label(root, text="Waste Management System",
         font=("Arial", 16, "bold")).pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=10)

# Classify function
def classify_image(path):
    global model

    if model is None:
        model = load_model("model.h5")

    img = cv2.imread(path)

    if img is None:
        result_label.config(text="Image not found ❌")
        return

    img = cv2.resize(img, (128,128))
    img = img / 255.0
    img = np.reshape(img, [1, 128, 128, 3])

    prediction = model.predict(img)

    confidence = np.max(prediction) * 100
    result = classes[np.argmax(prediction)]

    if confidence < 40:
        result_label.config(text="Unknown Waste ❌")
    else:
        result_label.config(text=f"{result} ({confidence:.2f}%)")

        success = save_to_db(result)

        if success:
            messagebox.showinfo("Success", f"{result} saved successfully ✅")

result_label.config(text="")   # 🔥 reset screen

# Save to DB
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

        return True

    except Exception as e:
        messagebox.showerror("DB Error", str(e))
        return False

# Upload button
def upload_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        classify_image(file_path)

tk.Button(root, text="Upload Image",
          command=upload_image,
          bg="blue", fg="white").pack(pady=20)

root.mainloop()