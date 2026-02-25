import mysql.connector
from datetime import date
import tkinter as tk
from tkinter import messagebox

# MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="waste_management"
)
cursor = conn.cursor()

root = tk.Tk()
root.title("Waste Management System")
root.geometry("400x300")

tk.Label(root, text="Waste Management System",
         font=("Arial", 16, "bold")).pack(pady=10)

waste_var = tk.StringVar()
waste_var.set("Select Waste Type")

tk.Label(root, text="Waste Type").pack()
tk.OptionMenu(root, waste_var, "wet", "dry", "e-waste").pack(pady=5)

tk.Label(root, text="Quantity").pack()
quantity_entry = tk.Entry(root)
quantity_entry.pack(pady=5)
def submit_data():
    waste = waste_var.get()
    qty = quantity_entry.get()
    today = date.today()

    # ❌ Invalid case 1: waste type not selected
    if waste == "Select Waste Type":
        messagebox.showerror("Error", "Please select waste type")
        return

    # ❌ Invalid case 2: quantity empty
    if qty == "":
        messagebox.showerror("Error", "Quantity cannot be empty")
        return

    # ❌ Invalid case 3: quantity not a number
    try:
        qty = int(qty)
    except:
        messagebox.showerror("Error", "Quantity must be a number")
        return

    # ❌ Invalid case 4: quantity zero or negative
    if qty <= 0:
        messagebox.showerror("Error", "Quantity must be greater than zero")
        return

    # ✅ Valid case → insert into database
    try:
        query = "INSERT INTO wastedata (date, waste_type, quantity) VALUES (%s, %s, %s)"
        values = (today, waste, qty)
        cursor.execute(query, values)
        conn.commit()

        messagebox.showinfo("Success", "Waste data stored successfully")
        quantity_entry.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Database Error", str(e))


tk.Button(root, text="Submit", command=submit_data,
          bg="green", fg="white").pack(pady=10)

root.mainloop()
