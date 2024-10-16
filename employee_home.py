import tkinter as tk
import subprocess
from tkinter import messagebox
from PIL import Image, ImageTk
import sys

class EmployeePage:
    def __init__(self, root, username, eid, title):
        self.root = root
        self.username = username
        self.eid = eid
        self.title = title
        self.setup_ui()

    def open_password_change(self):
        subprocess.run(["python", "account_security.py", self.username])

    def logout(self):
        self.root.destroy()
        subprocess.run(["python", "supermarket_management.py"])

    def sales_management(self):
        self.root.destroy()
        subprocess.run(["python", "sales_management.py", self.username, self.title, str(self.eid)])

    def customer_registrations(self):
        subprocess.run(["python", "customer_registration.py"])

    def record_sale(self):
        subprocess.run(["python", "record_sale.py", str(self.eid)])

    def setup_ui(self):
        self.root.title("Employee Page")
        self.root.configure(background="#0A4D68")
        self.root.geometry("1050x600")
        self.root.geometry("+100+20")

        try:
            image2 = Image.open("hello.png")
            width, height = image2.size
            ratio = min(self.root.winfo_screenwidth() / width, self.root.winfo_screenheight() / height)
            image2 = image2.resize((int(width * ratio), int(height * ratio)))
            image2 = ImageTk.PhotoImage(image2)
            self.image2 = image2  # store it as an instance variable
            background_label = tk.Label(self.root, image=self.image2)
            background_label.place(anchor="center", relx=0.5, rely=0.5)
        except tk.TclError as e:
            messagebox.showerror("Image Error", f"Error loading image: {e}")

        button_colors = {
            "customer_registration": "#db8065",
            "record_sale": "#db8065",
            "account_security": "#d79330",
            "sales_management": "#db8065",
            "logout": "#e74c3c"
        }

        button_style = {"relief": "flat", "borderwidth": 0, "highlightthickness": 0, "cursor": "hand2"}

        # Image loading with resizing
        customer_registration_img = tk.PhotoImage(file="add customer.png").subsample(5, 5)
        sales_management_img = tk.PhotoImage(file="sale.png").subsample(2, 3)
        record_sale_img = tk.PhotoImage(file="add sale.png").subsample(2, 3)
        account_security_img = tk.PhotoImage(file="password.png").subsample(5, 5)
        logout_img = tk.PhotoImage(file="logout.png").subsample(5, 5)

        # Store them as instance variables
        self.customer_registration_img = customer_registration_img
        self.sales_management_img = sales_management_img
        self.record_sale_img = record_sale_img
        self.account_security_img = account_security_img
        self.logout_img = logout_img

        addCustomerbt = tk.Button(self.root, image=self.customer_registration_img, command=self.customer_registrations,
                                  bg=button_colors["customer_registration"], **button_style)
        addCustomerbt.place(relheight=0.15, relwidth=0.2, relx=0.1, rely=0.25)

        addCustomerLabel = tk.Label(self.root, text="Customer Registration", font=('bold', 10),
                                    background=button_colors["customer_registration"])
        addCustomerLabel.place(anchor="nw", relx=0.1, rely=0.40, relwidth=0.2, relheight=0.05)

        recordSalebt = tk.Button(self.root, image=self.record_sale_img, command=self.record_sale,
                                 bg=button_colors["record_sale"], **button_style)
        recordSalebt.place(relheight=0.15, relwidth=0.2, relx=0.4, rely=0.25)

        recordSaleLabel = tk.Label(self.root, text="Record Sale", font=('bold', 10),
                                   background=button_colors["record_sale"])
        recordSaleLabel.place(anchor="nw", relx=0.4, rely=0.40, relwidth=0.2, relheight=0.05)

        salesbt = tk.Button(self.root, image=self.sales_management_img, command=self.sales_management,
                            bg=button_colors["sales_management"], **button_style)
        salesbt.place(relheight=0.15, relwidth=0.2, relx=0.1, rely=0.55)

        salesLabel = tk.Label(self.root, text="Sales Management", font=('bold', 10),
                              background=button_colors["sales_management"])
        salesLabel.place(anchor="nw", relx=0.1, rely=0.70, relwidth=0.2, relheight=0.05)

        changePassbt = tk.Button(self.root, image=self.account_security_img, command=self.open_password_change,
                                 bg=button_colors["account_security"], **button_style)
        changePassbt.place(relheight=0.15, relwidth=0.2, relx=0.4, rely=0.55)

        changePassLabel = tk.Label(self.root, text="Account Security", font=('bold', 10),
                                   background=button_colors["account_security"])
        changePassLabel.place(anchor="nw", relx=0.4, rely=0.70, relwidth=0.2, relheight=0.05)

        logoutbt = tk.Button(self.root, image=self.logout_img, command=self.logout,
                             bg=button_colors["logout"], **button_style)
        logoutbt.place(relheight=0.15, relwidth=0.2, relx=0.7, rely=0.55)

        logoutLabel = tk.Label(self.root, text="Logout", font=('bold', 10), background=button_colors["logout"])
        logoutLabel.place(anchor="nw", relx=0.7, rely=0.70, relwidth=0.2, relheight=0.05)

# Command line arguments
username = sys.argv[1]
title = sys.argv[2]
eid = int(sys.argv[3])

# Create the main window
root = tk.Tk()
employee_page = EmployeePage(root, username, eid, title)

# Start the main loop
root.mainloop()
