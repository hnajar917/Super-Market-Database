from tkinter import messagebox
import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import sys

class ManagerPage:
    def __init__(self, root, username, eid, title):
        self.root = root
        self.username = username
        self.eid = eid
        self.title = title
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Manager Page")
        self.root.geometry("1050x600")
        self.root.geometry("+100+20")

        try:
            image2 = Image.open("backgroundd.png")
            width, height = image2.size
            ratio = min(self.root.winfo_screenwidth() / width, self.root.winfo_screenheight() / height)
            image2 = image2.resize((int(width * ratio), int(height * ratio)))
            self.image2 = ImageTk.PhotoImage(image2)
            background_label = tk.Label(self.root, image=self.image2)
            background_label.place(anchor="center", relx=0.5, rely=0.5)
        except tk.TclError as e:
            messagebox.showerror("Image Error", f"Error loading image: {e}")

        button_style = {"relief": "flat", "borderwidth": 0, "highlightthickness": 0, "cursor": "hand2"}

        button_colors = {
            "new employee": "#ae4e38",
            "customer registration": "#db8065",
            "record sale": "#db8065",
            "new product entry": "#f19888",
            "supplier management": "#d79330",
            "customer management": "#f0d9c7",
            "employee home": "#f0d9c7",
            "inventory": "#f19888",
            "account security": "#d79330",
            "sales management": "#db8065",
            "logout": "#e74c3c"
        }

        self.new_employee_img = tk.PhotoImage(file="add employye.png").subsample(2, 3)
        self.customer_registration_img = tk.PhotoImage(file="add customer.png").subsample(5, 5)
        self.record_sale_img = tk.PhotoImage(file="add sale.png").subsample(2, 3)
        self.new_product_entry_img = tk.PhotoImage(file="add product.png").subsample(2, 3)
        self.supplier_management_img = tk.PhotoImage(file="supply.png").subsample(2, 3)
        self.customer_management_img = tk.PhotoImage(file="customer.png").subsample(2, 3)
        self.employee_home_img = tk.PhotoImage(file="employee.png").subsample(2, 3)
        self.inventory_img = tk.PhotoImage(file="product.png").subsample(5, 5)
        self.account_security_img = tk.PhotoImage(file="password.png").subsample(5, 5)
        self.sales_management_img = tk.PhotoImage(file="sale.png").subsample(2, 3)
        self.logout_img = tk.PhotoImage(file="logout.png").subsample(5, 5)

        # Keep references to the images used by labels
        self.label_images = {
            "new employee": self.new_employee_img,
            "customer registration": self.customer_registration_img,
            "record sale": self.record_sale_img,
            "new product entry": self.new_product_entry_img,
            "supplier management": self.supplier_management_img,
            "customer management": self.customer_management_img,
            "employee home": self.employee_home_img,
            "inventory": self.inventory_img,
            "account security": self.account_security_img,
            "sales management": self.sales_management_img,
            "logout": self.logout_img
        }

        buttons_info = [
            ("new employee", self.new_employee_img, self.new_employee),
            ("customer registration", self.customer_registration_img, self.customer_registrations),
            ("record sale", self.record_sale_img, lambda: self.record_sale(self.eid)),
            ("new product entry", self.new_product_entry_img, self.new_product_entry),
            ("supplier management", self.supplier_management_img, self.supplier_management),
            ("customer management", self.customer_management_img,
             lambda: self.open_customer_management(self.username, self.eid, self.title)),
            ("employee home", self.employee_home_img, lambda: self.employee_home(self.username, self.eid, self.title)),
            ("inventory", self.inventory_img, lambda: self.inventory(self.username, self.eid, self.title)),
            ("account security", self.account_security_img, lambda: self.open_password_change(self.username)),
            ("sales management", self.sales_management_img,
             lambda: self.sales_management(self.username, self.eid, self.title)),
            ("logout", self.logout_img, self.logout)
        ]

        for i, (label, img, command) in enumerate(buttons_info):
            button = tk.Button(self.root, image=img, command=command, bg=button_colors[label], **button_style)
            button.place(anchor="nw", relx=0.06 + 0.23 * (i % 4), rely=0.15 + 0.25 * (i // 4), relwidth=0.2,
                         relheight=0.15)

            label_widget = tk.Label(self.root, text=label, font=('bold', 10), background=button_colors[label])
            label_widget.place(anchor="nw", relx=0.06 + 0.23 * (i % 4), rely=0.3 + 0.25 * (i // 4), relwidth=0.2,
                               relheight=0.05)

    def new_employee(self):
        subprocess.run(["python", "new_employee.py"])

    def customer_registrations(self):
        subprocess.run(["python", "customer_registration.py"])

    def record_sale(self, eid):
        subprocess.run(["python", "record_sale.py", str(eid)])

    def new_product_entry(self):
        subprocess.run(["python", "new_product_entry.py"])

    def supplier_management(self):
        subprocess.run(["python", "supplier_management.py", self.username, self.title, str(self.eid)])

    def open_customer_management(self, username, eid, title):
        subprocess.run(["python", "customer_management.py", username, title, str(eid)])

    def employee_home(self, username, eid, title):
        subprocess.run(["python", "employee_management.py", username, title, str(eid)])

    def inventory(self, username, eid, title):
        subprocess.run(["python", "inventory.py", username, title, str(eid)])

    def open_password_change(self, user):
        subprocess.run(["python", "account_security.py", user])

    def sales_management(self, username, eid, title):
        subprocess.run(["python", "sales_management.py", username, title, str(eid)])

    def logout(self):
        self.root.destroy()
        # Execute the supermarket_management script directly
        sys.exit(subprocess.call(["python", "supermarket_management.py"]))


# Extracting command-line arguments
username = sys.argv[1]
title = sys.argv[2]
eid = int(sys.argv[3])

# Create the main window
root = tk.Tk()
manager_page = ManagerPage(root, username, eid, title)

# Start the main loop
root.mainloop()
