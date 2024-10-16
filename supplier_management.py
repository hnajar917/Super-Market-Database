import mysql.connector as con
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox  # Add this line
from PIL import Image, ImageTk
import subprocess
import sys

class SupplierManagerApp:
    def __init__(self, root, username, title, eid):
        self.root = root
        self.root.configure(background="#222831", height=200, width=200)
        self.root.geometry("1050x600")
        self.root.geometry("+100+20")

        # Command-line arguments
        self.username = username
        self.title = title
        self.eid = int(eid)

        self.setup_ui()

    def go_back(self):
        print("Going back to the previous page...")

        self.root.quit()  # Terminate Tkinter main loop
        self.root.destroy()

        try:
            subprocess.run(["python", "control_center.py", self.username, self.title, str(self.eid)])
        except Exception as e:
            print(f"Error opening control_center: {e}")

    def show_suppliers(self):
        datatxt.configure(state='normal')
        connection = con.connect(host="localhost", user="root", password="H123hamza", database="supermarket_sql", port="3306")

        cursor = connection.cursor()
        datatxt.delete('1.0', tk.END)

        supplier_id = supplieridentry.get()
        phone = phoneentry.get()
        name = nameentry.get()
        category = categoryentry.get()

        query = "SELECT * FROM suppliers WHERE 1=1"

        if supplier_id:
            query += f" AND SupplierID = '{supplier_id}'"
        if phone:
            query += f" AND Phone = '{phone}'"
        if name:
            query += f" AND Name = '{name}'"
        if category:
            query += f" AND Category = '{category}'"

        try:
            cursor.execute(query)
        except:
            datatxt.insert(tk.END, "Invalid query or no suppliers found")

        try:
            data = cursor.fetchall()

            # Define standard column widths
            col_widths = {'SupplierID': 12, 'Name': 20, 'Phone': 15, 'Category': 15}

            # Table Header
            header = "┌{0}┬{1}┬{2}┬{3}┐\n".format('─' * col_widths['SupplierID'], '─' * col_widths['Name'],
                                                   '─' * col_widths['Phone'], '─' * col_widths['Category'])
            header += "│{:^12}│{:^20}│{:^15}│{:^15}│\n".format('SupplierID', 'Name', 'Phone', 'Category')
            header += "├{0}┼{1}┼{2}┼{3}┤\n".format('─' * col_widths['SupplierID'], '─' * col_widths['Name'],
                                                    '─' * col_widths['Phone'], '─' * col_widths['Category'])
            datatxt.insert(tk.END, header)

            if len(data) != 0:
                for row in data:
                    line = "│{:<12}│{:<20}│{:<15}│{:<15}│\n".format(str(row[0]), row[1], row[2], row[3])
                    datatxt.insert(tk.END, line)

            # Table Footer
            footer = "└{0}┴{1}┴{2}┴{3}┘\n".format('─' * col_widths['SupplierID'], '─' * col_widths['Name'],
                                                   '─' * col_widths['Phone'], '─' * col_widths['Category'])
            datatxt.insert(tk.END, footer)
        except Exception as e:
            datatxt.insert(tk.INSERT, f"Couldn't fetch data! Error: {e}\n")
        finally:
            datatxt.configure(state='disabled')
            cursor.close()
            connection.close()

    def add_supplier(self):
        name = nameentry.get()
        phone = phoneentry.get()
        category = categoryentry.get()

        if name == '' or phone == '' or category == '':
            messagebox.showerror("Error", "Please fill in all the fields.")
            return

        connection = con.connect(host="localhost", user="root", password="H123hamza", database="supermarket_sql", port="3306")

        cursor = connection.cursor()

        query = "INSERT INTO suppliers (name, phone, category) VALUES (%s, %s, %s)"
        values = (name, phone, category)

        try:
            cursor.execute(query, values)
            connection.commit()

            messagebox.showinfo("Success", "Supplier added successfully")

            nameentry.delete(0, tk.END)
            phoneentry.delete(0, tk.END)
            categoryentry.delete(0, tk.END)
        except:
            messagebox.showerror("Error", "Failed to add supplier")

        cursor.close()
        connection.close()

    def edit_supplier(self):
        supplier_id = supplieridentry.get()
        phone = phoneentry.get()
        category = categoryentry.get()
        name = nameentry.get()

        if supplier_id == '' or phone == '' or category == '' or name == '':
            messagebox.showerror("Error", "Please fill in all the fields.")
            return

        connection = con.connect(host="localhost", user="root", password="H123hamza", database="supermarket_sql", port="3306")

        cursor = connection.cursor()

        query = "UPDATE suppliers SET phone = %s, category = %s, name = %s WHERE supplierID = %s"
        values = (phone, category, name, supplier_id)

        try:
            cursor.execute(query, values)
            connection.commit()

            messagebox.showinfo("Success", "Supplier updated successfully")

            supplieridentry.delete(0, tk.END)
            phoneentry.delete(0, tk.END)
            categoryentry.delete(0, tk.END)
            nameentry.delete(0, tk.END)
        except:
            messagebox.showerror("Error", "Failed to update supplier")

        cursor.close()
        connection.close()

    def setup_ui(self):
        # Loading and placing background image
        bg_image = Image.open("supplier.png")
        resized_bg_image = bg_image.resize((800, 370))
        tk_bg_image = ImageTk.PhotoImage(resized_bg_image)
        bg_label = tk.Label(self.root, image=tk_bg_image)
        bg_label.image = tk_bg_image  # Reference to avoid garbage collection
        bg_label.place(relwidth=1, relheight=1.8)
        # Creating a scrolled text widget for displaying data
        global datatxt
        datatxt = ScrolledText(self.root, background="#ffffff")
        datatxt.place(anchor="nw", relheight=0.6, relwidth=1.0)

        # Supplier ID input and label
        supplieridlbl = tk.Label(self.root)
        supplieridlbl.configure(text='Supplier ID', background="#FFD700")
        supplieridlbl.place(anchor="nw", relwidth=0.1, relx=0.05, rely=0.65)
        global supplieridentry
        supplieridentry = tk.Entry(self.root, background="#EEEEEE")
        supplieridentry.place(anchor="nw", relwidth=0.15, relx=0.15, rely=0.65)

        # Name input and label
        namelbl = tk.Label(self.root, background="#FFD700")
        namelbl.configure(text='Name')
        namelbl.place(anchor="nw", relwidth=0.1, relx=0.05, rely=0.75)
        global nameentry
        nameentry = tk.Entry(self.root, background="#EEEEEE")
        nameentry.place(anchor="nw", relwidth=0.15, relx=0.15, rely=0.75)

        # Phone input and label
        phonelbl = tk.Label(self.root, background="#FFD700")
        phonelbl.configure(text='Phone')
        phonelbl.place(anchor="nw", relwidth=0.1, relx=0.4, rely=0.65)
        global phoneentry
        phoneentry = tk.Entry(self.root, background="#EEEEEE")
        phoneentry.place(anchor="nw", relwidth=0.15, relx=0.5, rely=0.65)

        # Category input and label
        categorylbl = tk.Label(self.root, background="#FFD700")
        categorylbl.configure(text='Category')
        categorylbl.place(anchor="nw", relwidth=0.1, relx=0.4, rely=0.75)
        global categoryentry
        categoryentry = tk.Entry(self.root, background="#EEEEEE")
        categoryentry.place(anchor="nw", relwidth=0.15, relx=0.5, rely=0.75)

        # Buttons for actions
        showSuppliersbt = tk.Button(self.root, command=self.show_suppliers, background="#00ADB5")
        showSuppliersbt.configure(text='Show Suppliers')
        showSuppliersbt.place(anchor="nw", relwidth=0.2, relx=0.05, rely=0.9)

        addSupplierbt = tk.Button(self.root, command=self.add_supplier, background="#00ADB5")
        addSupplierbt.configure(text='Add Supplier')
        addSupplierbt.place(anchor="nw", relwidth=0.2, relx=0.3, rely=0.9)

        editSupplierbt = tk.Button(self.root, command=self.edit_supplier, background="#00ADB5")
        editSupplierbt.configure(text='Edit Supplier')
        editSupplierbt.place(anchor="nw", relwidth=0.2, relx=0.55, rely=0.9)

        # Button to go back
        backbt = tk.Button(self.root, command=self.go_back, background="#00ADB5")
        backbt.configure(text='Back')
        backbt.place(anchor="nw", relwidth=0.2, relx=0.8, rely=0.9)

if __name__ == "__main__":
    root = tk.Tk()
    app = SupplierManagerApp(root, sys.argv[1], sys.argv[2], sys.argv[3])
    root.mainloop()
