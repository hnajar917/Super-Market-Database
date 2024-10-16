from tkinter import messagebox, ttk, scrolledtext
import tkinter as tk
import subprocess
from PIL import Image, ImageTk
import sys
import mysql.connector as con

class ProductManagement:
    def __init__(self, root, username, title, eid):
        self.root = root
        self.username = username
        self.title = title
        self.eid = eid
        self.setup_ui()

    def go_back(self):
        self.root.destroy()
        subprocess.run(["python", "control_center.py", self.username, self.title, str(self.eid)])

    def show_products(self):
        self.datatxt.configure(state='normal')
        connection = con.connect(host="localhost", user="root", password="H123hamza", database="supermarket_sql",
                                 port="3306")

        cursor = connection.cursor()

        self.datatxt.delete('1.0', tk.END)

        productID = self.pidtxt.get()
        quantity = self.quantitytxt.get()
        price = self.pricetxt.get()
        name = self.nametxt.get()
        category = self.categorytxt.get()
        supplierID = self.supplieridtxt.get()

        query = "SELECT productID, name, quantity, category, supplierID, price FROM products WHERE 1=1"

        if productID:
            query += f" AND productID = {productID}"
        if quantity:
            if quantity.startswith("<"):
                query += f" AND quantity < {quantity[1:]}"
            elif quantity.startswith(">"):
                query += f" AND quantity > {quantity[1:]}"
            else:
                query += f" AND quantity = {quantity}"
        if price:
            if price.startswith("<"):
                query += f" AND price < {price[1:]}"
            elif price.startswith(">"):
                query += f" AND price > {price[1:]}"
            else:
                query += f" AND price = {price}"
        if name:
            query += f" AND name = '{name}'"
        if category:
            query += f" AND category = '{category}'"
        if supplierID:
            query += f" AND supplierID = {supplierID}"

        try:
            print("Query:", query)  # Print the query for debugging purposes
            cursor.execute(query)
        except Exception as e:
            print("Error executing query:", e)
            self.datatxt.insert(tk.END, "Invalid query or product does not exist")

        try:
            data = cursor.fetchall()
            # Define column widths
            col_widths = [17, 17, 17, 17, 17, 17]  # Adjust these as needed

            # Table Header
            header = "┌" + "┬".join(["─" * w for w in col_widths]) + "┐\n"
            header += "│" + "│".join("{:<{}}".format(title, col_widths[i]) for i, title in enumerate(
                ["productID", "name", "quantity", "category", "supplierID", "price"])) + "│\n"
            header += "├" + "┼".join(["─" * w for w in col_widths]) + "┤\n"
            self.datatxt.insert('1.0', header)

            if len(data) != 0:
                for row in data:
                    row_formatted = [f"{str(item):<{col_widths[i]}}" for i, item in enumerate(row)]
                    line = "│" + "│".join(row_formatted) + "│\n"
                    self.datatxt.insert(tk.END, line)

            # Table Footer
            footer = "└" + "┴".join(["─" * w for w in col_widths]) + "┘\n"
            self.datatxt.insert(tk.END, footer)
            self.datatxt.configure(state='disabled')
        except:
            self.datatxt.insert(tk.INSERT, "Couldn't fetch data!\n")
        cursor.close()
        connection.close()

    def edit_product(self):
        productID = self.pidtxt.get()
        quantity = self.quantitytxt.get()
        price = self.pricetxt.get()
        supplierID = self.supplieridtxt.get()
        name = self.nametxt.get()
        category = self.categorytxt.get()

        if productID == '' or quantity == '':
            messagebox.showerror("Error", "Please fill in the productID and quantity fields.")
            return

        try:
            productID = int(productID)
            quantity = int(quantity)
            if price:
                price = float(price)
            if supplierID:
                supplierID = int(supplierID)
        except:
            messagebox.showerror("Error", "Invalid input format for productID, quantity, supplier_id, or price.")
            return

        connection = con.connect(host="localhost", user="root", password="H123hamza", database="supermarket_sql", port="3306")

        cursor = connection.cursor()

        query = f"UPDATE products SET quantity = {quantity}"
        if price:
            query += f", price = {price}"
        if supplierID:
            query += f", supplierID = {supplierID}"
        if name:
            query += f", name = '{name}'"
        if category:
            query += f", category = '{category}'"

        query += f" WHERE productID = {productID}"

        try:
            cursor.execute(query)
            connection.commit()

            messagebox.showinfo("Success", "Product edited successfully")

            self.pidtxt.delete(0, tk.END)
            self.quantitytxt.delete(0, tk.END)
            self.pricetxt.delete(0, tk.END)
            self.supplieridtxt.delete(0, tk.END)
            self.nametxt.delete(0, tk.END)
            self.categorytxt.delete(0, tk.END)
        except:
            messagebox.showerror("Error", "Failed to edit product")

        cursor.close()
        connection.close()

    def setup_ui(self):
        self.root.configure(background="#222831", height=200, width=200)
        self.root.geometry("1050x600")
        self.root.geometry("+100+20")

        try:
            bg_image = Image.open("product2.jpg")
            resized_bg_image = bg_image.resize((1050, 370))
            tk_bg_image = ImageTk.PhotoImage(resized_bg_image)
            bg_label = tk.Label(self.root, image=tk_bg_image)
            bg_label.place(relwidth=1, relheight=1.8)
            # Store reference to the image to prevent garbage collection
            self.tk_bg_image = tk_bg_image
        except Exception as e:
            print("Error loading image:", e)

        self.datatxt = scrolledtext.ScrolledText(self.root, background="#ffffff")
        self.datatxt.place(anchor="nw", relheight=0.6, relwidth=1.0)

        self.pidlbl = tk.Label(self.root)
        self.pidlbl.configure(text='productID', background="#89CFF0")
        self.pidlbl.place(anchor="nw", relwidth=0.08, relx=0.02, rely=0.65)

        self.pidtxt = tk.Entry(self.root, background="#EEEEEE")
        self.pidtxt.place(anchor="nw", relwidth=0.16, relx=0.14, rely=0.65, x=0, y=0)

        self.quantitylbl = tk.Label(self.root, background="#89CFF0")
        self.quantitylbl.configure(text='quantity')
        self.quantitylbl.place(anchor="nw", relwidth=0.08, relx=0.02, rely=0.7)

        self.quantitytxt = tk.Entry(self.root, background="#EEEEEE")
        self.quantitytxt.place(anchor="nw", relwidth=0.16, relx=0.14, rely=0.7, x=0, y=0)

        self.pricelbl = tk.Label(self.root, background="#89CFF0")
        self.pricelbl.configure(text='price')
        self.pricelbl.place(anchor="nw", relwidth=0.08, relx=0.02, rely=0.75)

        self.pricetxt = tk.Entry(self.root, background="#EEEEEE")
        self.pricetxt.place(anchor="nw", relwidth=0.16, relx=0.14, rely=0.75)

        self.supplieridlbl = tk.Label(self.root, background="#89CFF0")
        self.supplieridlbl.configure(text='supplierID')
        self.supplieridlbl.place(anchor="nw", relwidth=0.08, relx=0.02, rely=0.80)

        self.supplieridtxt = tk.Entry(self.root, background="#EEEEEE")
        self.supplieridtxt.place(anchor="nw", relwidth=0.16, relx=0.14, rely=0.80)

        self.namelbl = tk.Label(self.root)
        self.namelbl.configure(text='Name', background="#89CFF0")
        self.namelbl.place(anchor="nw", relwidth=0.08, relx=0.02, rely=0.85)

        self.nametxt = tk.Entry(self.root, background="#EEEEEE")
        self.nametxt.place(anchor="nw", relwidth=0.16, relx=0.14, rely=0.85, x=0, y=0)

        self.categorylbl = tk.Label(self.root, background="#89CFF0")
        self.categorylbl.configure(text='Category')
        self.categorylbl.place(anchor="nw", relwidth=0.08, relx=0.02, rely=0.9)

        self.categorytxt = tk.Entry(self.root, background="#EEEEEE")
        self.categorytxt.place(anchor="nw", relwidth=0.16, relx=0.14, rely=0.9)

        self.showProductsbt = tk.Button(self.root, command=self.show_products, background="#00ADB5")
        self.showProductsbt.configure(text='Show Products')
        self.showProductsbt.place(anchor="nw", relwidth=0.2, relx=0.7, rely=0.65)

        self.editProductbt = tk.Button(self.root, background="#00ADB5", command=self.edit_product)
        self.editProductbt.configure(text='Edit Product')
        self.editProductbt.place(anchor="nw", relwidth=0.2, relx=0.7, rely=0.775)

        self.backbt = tk.Button(self.root, command=self.go_back, background="#00ADB5")
        self.backbt.configure(text='Back')
        self.backbt.place(anchor="nw", relwidth=0.2, relx=0.7, rely=0.90)


if __name__ == "__main__":
    username = sys.argv[1]
    title = sys.argv[2]
    eid = int(sys.argv[3])

    root = tk.Tk()
    app = ProductManagement(root, username, title, eid)
    root.mainloop()
