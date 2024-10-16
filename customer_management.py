from tkinter import messagebox
import mysql.connector as con
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
from tkinter.font import Font
import subprocess
import sys


class CustomerManager:
    def __init__(self, root, username, title, eid):
        self.root = root
        self.username = username
        self.title = title
        self.eid = eid

        self.setup_ui()

    def setup_ui(self):
        self.root.configure(background="#222831", height=200, width=200)
        self.root.geometry("1050x600")
        self.root.geometry("+100+20")

        # Background image
        bg_image = Image.open("show_customer.png")
        resized_bg_image = bg_image.resize((1050, 370))
        self.tk_bg_image = ImageTk.PhotoImage(resized_bg_image)  # Store as an attribute
        bg_label = tk.Label(self.root, image=self.tk_bg_image)
        bg_label.place(relwidth=1, relheight=1.8)

        # ScrolledText widget
        self.datatxt = ScrolledText(self.root, background="#FFFFFF")
        self.datatxt.place(anchor="nw", relheight=0.6, relwidth=1.0)

        # Labels and Entry widgets
        labels = ['Customer ID:', 'Phone:', 'Name:', 'Email:']
        self.entries = [tk.Entry(self.root, background="#EEEEEE") for _ in range(4)]

        for i, label_text in enumerate(labels):
            label = tk.Label(self.root, background="#00ADB5", text=label_text)
            label.place(anchor="nw", relwidth=0.15, relx=0.02, rely=0.7 + i * 0.05)

            entry = self.entries[i]
            entry.place(anchor="nw", relwidth=0.2, relx=0.17, rely=0.7 + i * 0.05)

        # Assigning Entry widgets to variables
        self.customeridtxt, self.phonetxt, self.nametxt, self.emailtxt = self.entries

        # Buttons
        edit_customer_bt = tk.Button(self.root, background="#00ADB5", command=self.edit_customer, text='Edit Customer')
        edit_customer_bt.place(anchor="nw", relwidth=0.2, relx=0.7, rely=0.7)

        show_customers_bt = tk.Button(self.root, command=self.show_customers, background="#00ADB5", text='Show Customers')
        show_customers_bt.place(anchor="nw", relwidth=0.2, relx=0.7, rely=0.75)

        back_bt = tk.Button(self.root, command=self.go_back, background="#00ADB5", text='Back')
        back_bt.place(anchor="nw", relwidth=0.2, relx=0.7, rely=0.8)

    def go_back(self):
        # Function to go back to the manager page
        self.root.destroy()
        subprocess.run(["python", "control_center.py", self.username, self.title, str(self.eid)])

    def show_customers(self):
        # Function to retrieve and display customer data
        self.datatxt.configure(state='normal')
        connection = con.connect(host="localhost", user="root", password="H123hamza", database="supermarket_sql", port="3306")

        cursor = connection.cursor()
        self.datatxt.delete('1.0', tk.END)

        customer_id = self.customeridtxt.get()
        phone = self.phonetxt.get()
        name = self.nametxt.get()
        email = self.emailtxt.get()

        query = "SELECT * FROM customers WHERE 1=1"

        if customer_id:
            query += f" AND CustomerID = '{customer_id}'"
        if phone:
            query += f" AND Phone = '{phone}'"
        if name:
            query += f" AND Name = '{name}'"
        if email:
            query += f" AND Email = '{email}'"

        try:
            cursor.execute(query)
        except:
            self.datatxt.insert(tk.END, "Invalid query or no customers found")

        try:
            data = cursor.fetchall()
            # Use a monospaced font for better alignment
            monospace_font = Font(family="Courier", size=10)
            self.datatxt.configure(font=monospace_font)

            # Header
            header = "┌───────────────────┬───────────────────┬───────────────────┬──────────────────────┐\n"
            header += "│ CustomerID        │ Name              │ Phone             │ Email                │\n"
            header += "├───────────────────┼───────────────────┼───────────────────┼──────────────────────┤\n"
            self.datatxt.insert('1.0', header)

            if len(data) != 0:
                for row in data:
                    line = f"│ {row[0]:<17} │ {row[1]:<17} │ {row[2]:<17} │ {row[3]:<20} │"
                    self.datatxt.insert(tk.END, line + "\n")

            # Footer
            footer = "└───────────────────┴───────────────────┴───────────────────┴──────────────────────┘\n"
            self.datatxt.insert(tk.END, footer)
            self.datatxt.configure(state='disabled')
        except:
            self.datatxt.insert(tk.INSERT, "Couldn't fetch data!\n")
        cursor.close()
        connection.close()

    def edit_customer(self):
        # Function to edit customer details
        customer_id = self.customeridtxt.get()
        phone = self.phonetxt.get()
        name = self.nametxt.get()
        email = self.emailtxt.get()

        if customer_id == '' or phone == '' or name == '' or email == '':
            messagebox.showerror("Error", "Please fill in all the fields.")
            return

        try:
            customer_id = int(customer_id)
        except:
            messagebox.showerror("Error", "Invalid input format for Customer ID.")
            return

        connection = con.connect(host="localhost", user="root", password="H123hamza", database="supermarket_sql", port="3306")

        cursor = connection.cursor()

        query = f"UPDATE customers SET Phone = '{phone}', Name = '{name}', Email = '{email}' WHERE CustomerID = {customer_id}"

        try:
            cursor.execute(query)
            connection.commit()

            messagebox.showinfo("Success", "Customer edited successfully")

            # Clearing the entry fields after successful edit
            self.customeridtxt.delete(0, tk.END)
            self.phonetxt.delete(0, tk.END)
            self.nametxt.delete(0, tk.END)
            self.emailtxt.delete(0, tk.END)
        except:
            messagebox.showerror("Error", "Failed to edit customer")

        cursor.close()
        connection.close()


# Extracting command-line arguments
username = sys.argv[1]
title = sys.argv[2]
eid = int(sys.argv[3])

# Create the main window
root = tk.Tk()
customer_manager = CustomerManager(root, username, title, eid)

# Start the main loop
root.mainloop()
