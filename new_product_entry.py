import mysql.connector as con
import tkinter as tk
from tkinter import messagebox

class ProductAddition:
    def __init__(self, root):
        self.root = root
        self.setup_ui()

    def add_product(self):
        connection = con.connect(host='localhost', database='supermarket_sql', user='root', password='H123hamza', port='3306')
        cursor = connection.cursor()

        query = "INSERT INTO products (name, quantity, category, supplierID, price) VALUES (%s, %s, %s, %s, %s)"
        values = (self.name_txt.get(), self.quantity_txt.get(), self.category_txt.get(), self.supplier_id_txt.get(), self.price_txt.get())

        if (
            self.name_txt.get() == ''
            or self.quantity_txt.get() == ''
            or self.category_txt.get() == ''
            or self.supplier_id_txt.get() == ''
            or self.price_txt.get() == ''
        ):
            messagebox.showerror("Error", "Please fill all the fields")
        else:
            try:
                cursor.execute(query, values)
                connection.commit()
                messagebox.showinfo("Success", "Product added successfully")
            except con.Error as error:
                messagebox.showerror("Error", f"Failed to add product: {error}")

        cursor.close()
        connection.close()

    def setup_ui(self):
        self.root.title("Add Product")
        self.root.geometry("850x650")

        # Styling for labels, entries, and buttons
        label_style = {"background": "#4E5759", "font": ('bold', 14), "fg": "white"}
        entry_style = {"background": "#2E3537", "font": ('bold', 14), "fg": "white"}
        button_style = {"background": "#277080", "text": 'Add Product', "command": self.add_product, "font": ('bold', 14), "fg": "white"}
        alarm_style = {"highlightthickness": 0, "bd": 0, "bg": "#2E3537", "justify": "center", "font": ('bold', 14), "fg": "white"}

        # Labels
        name_lbl = tk.Label(self.root, text='Name', **label_style)
        name_lbl.place(anchor="nw", relwidth=0.12, relx=0.05, rely=0.15)

        quantity_lbl = tk.Label(self.root, text='Quantity', **label_style)
        quantity_lbl.place(anchor="nw", relwidth=0.12, relx=0.05, rely=0.3)

        category_lbl = tk.Label(self.root, text='Category', **label_style)
        category_lbl.place(anchor="nw", relwidth=0.12, relx=0.05, rely=0.45)

        supplier_id_lbl = tk.Label(self.root, text='Supplier ID', **label_style)
        supplier_id_lbl.place(anchor="nw", relwidth=0.12, relx=0.05, rely=0.6)

        price_lbl = tk.Label(self.root, text='Price', **label_style)
        price_lbl.place(anchor="nw", relwidth=0.12, relx=0.05, rely=0.75)

        # Entries
        self.name_txt = tk.Entry(self.root, **entry_style)
        self.name_txt.place(anchor="nw", relx=0.18, rely=0.15, x=0, y=0, relwidth=0.25)

        self.quantity_txt = tk.Entry(self.root, **entry_style)
        self.quantity_txt.place(anchor="nw", relx=0.18, rely=0.3, x=0, y=0, relwidth=0.25)

        self.category_txt = tk.Entry(self.root, **entry_style)
        self.category_txt.place(anchor="nw", relx=0.18, rely=0.45, x=0, y=0, relwidth=0.25)

        self.supplier_id_txt = tk.Entry(self.root, **entry_style)
        self.supplier_id_txt.place(anchor="nw", relx=0.18, rely=0.6, x=0, y=0, relwidth=0.25)

        self.price_txt = tk.Entry(self.root, **entry_style)
        self.price_txt.place(anchor="nw", relx=0.18, rely=0.75, x=0, y=0, relwidth=0.25)

        # Add a background image on the right side
        try:
            bg_image = tk.PhotoImage(file="produce.png").subsample(1, 1)  # Adjust the subsample values
            self.tk_bg_image = bg_image  # Store as an attribute
            background_label = tk.Label(self.root, image=self.tk_bg_image)
            background_label.place(anchor="ne", relx=1, rely=0, relwidth=0.5, relheight=1)
        except tk.TclError as e:
            print(f"Error loading image: {e}")

        # Button
        add_product_bt = tk.Button(self.root, **button_style)
        add_product_bt.place(anchor="nw", relheight=0.1, relwidth=0.2, relx=0.05, rely=0.9)

        # Alarm Label
        alarm = tk.Label(self.root, **alarm_style)
        alarm.place(anchor="nw", relheight=0.1, relwidth=1, x=0, y=0)

# Create the main window
root = tk.Tk()
product_addition = ProductAddition(root)

# Start the main loop
root.mainloop()
