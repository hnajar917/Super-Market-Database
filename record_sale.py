import datetime
import tkinter as tk
import mysql.connector as con
import subprocess
from PIL import Image, ImageTk
from tkinter import ttk
import sys
class SaleManager:
    def __init__(self, root):
        self.root = root
        self.root.configure(background="#ffffff", height=200, width=200)
        self.root.geometry("600x580")
        self.eid = sys.argv[1]
        self.check = True
        self.saleID = 0

        self.setup_ui()

    def add_product(self):
        # Function to add a product to the sale
        self.done.place(x=2000, y=4300)
        self.check = False

        # Connect to the database
        connection = con.connect(host="localhost", user="root", password="H123hamza", database="supermarket_sql", port="3306")
        cursor = connection.cursor()

        # Insert sale information into the sales table
        query = "INSERT INTO sales (customerID,employeeID, payment_method,cost,time) VALUES ('" + str(self.customerEntry.get()) + "','" + (str(self.eid)) + "','" + str(self.paymentCombo.get()) + "','" + str(self.totalEntry.cget("text")) + "','" + str(datetime.date.today()) + "')"
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()

        # Retrieve the last saleID from the sales table
        connection = con.connect(host="localhost", user="root", password="H123hamza", database="supermarket_sql", port="3306")
        cursor = connection.cursor()
        query2 = "SELECT saleID FROM sales ORDER BY saleID DESC LIMIT 1"
        cursor.execute(query2)
        data = cursor.fetchall()
        self.saleID = data[0][0]
        connection.commit()
        cursor.close()
        connection.close()

        # Run the "product_sale_manager.py" script with the saleID as an argument
        subprocess.run(["python", "product_sale_manager.py", str(self.saleID)])

    def revel_price(self):
        self.done.place(x=2000, y=4300)
        print(self.check)
        if self.check:
            self.totalEntry.configure(text="0")
        else:
            connection = con.connect(host="localhost", user="root", password="H123hamza", database="supermarket_sql", port="3306")

            cursor = connection.cursor()
            query ="SELECT sum(price) FROM sold_item where saleID="+str(self.saleID)
            cursor.execute(query)
            data = cursor.fetchall()
            total_price = data[0][0]
            if total_price is not None:
                self.totalEntry.configure(text="" + str(total_price))
            connection.commit()
            cursor.close()
            connection.close()

    def add_sale(self):
        if self.customerEntry.get() == "" and self.paymentCombo.get()=="":
            self.done.configure(background="#ffffff", text='make sure to provide all data fields', font=("Arial", 18))
            self.done.place(anchor="nw", relheight=0.1, relwidth=0.9, relx=0.05, rely=0.64)
        elif self.check:
            self.done.configure(background="#ffffff", text='make sure to add products to your sale', font=("Arial", 18))
            self.done.place(x=150,y=430)
        else:
            connection = con.connect(host="localhost", user="root", password="H123hamza", database="supermarket_sql", port="3306")

            cursor = connection.cursor()
            try:
                query = "SELECT sum(price) FROM sold_item where saleID=" + str(self.saleID)
                cursor.execute(query)
            except mysql.connector.Error as error :
                print(f"Error executing MySQL query: {error}")
            data = cursor.fetchall()
            connection.commit()
            cursor.close()
            connection.close()
            connection = con.connect(host="localhost", user="root", password="H123hamza", database="supermarket_sql", port="3306")

            cursor = connection.cursor()

            try:
                query="UPDATE sales SET cost=0"+str(data[0][0]) +" WHERE saleID=" + str(self.saleID)
                if data[0][0] == None:
                    query = "UPDATE sales SET cost=0"+ " WHERE saleID=" + str(self.saleID)
                cursor.execute(query)
            except mysql.connector.Error as error :
                print(f"Error executing MySQL query: {error}")
            connection.commit()
            cursor.close()
            connection.close()
            self.done.configure(background="#00C4FF", text='sale has been added!!', font=("Arial", 18))
            self.done.place(x=200,y=430)
            self.root.after(1000, self.root.destroy)

    def setup_ui(self):
        try:
            bg_image = Image.open("backgrounSale.png")
            resized_bg_image = bg_image.resize((600, 580))  # Resize the image to match the window size
            bg_photo_image = ImageTk.PhotoImage(resized_bg_image)

            # Create a label with the image and set it to cover the entire window
            bg_label = tk.Label(self.root, image=bg_photo_image)
            bg_label.image = bg_photo_image  # Reference to avoid garbage collection
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except tk.TclError as e:
            print(f"Error loading image: {e}")
        # Create a label with the image and set it to cover the entire window
        bg_label = tk.Label(self.root, image=bg_photo_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        customerID = tk.Label(self.root)
        customerID.configure(background="#ffffff", text='CUSTOMERID')
        customerID.place(anchor="nw", relheight=0.1, relwidth=0.25, relx=0.05, rely=0.05)

        payment = tk.Label(self.root)
        payment.configure(background="#ffffff", text='PAYMENT METHOD')
        payment.place(anchor="nw", relheight=0.1, relwidth=0.25, relx=0.05, rely=0.16)

        total = tk.Button(self.root)
        total.configure(background="#ff6f61", justify="left",command=self.revel_price ,text='TOTAL PRICE')
        total.place(anchor="nw", relheight=0.1, relwidth=0.25, relx=0.05, rely=0.40)

        self.customerEntry = tk.Entry(self.root)
        self.customerEntry.configure(background="#ffffff")
        self.customerEntry.place(anchor="nw", relheight=0.1, relwidth=0.4, relx=0.35, rely=0.05)

        options = ['Cash', 'Visa']

        # Create a Combobox widget
        self.paymentCombo = ttk.Combobox(self.root, values=options)

        # Set default value (optional)
        self.paymentCombo.current(0)  # Sets the first item as default

        # Place the combobox on the window
        self.paymentCombo.place(anchor="nw", relheight=0.1, relwidth=0.4, relx=0.35, rely=0.16)

        self.totalEntry = tk.Label(self.root)
        self.totalEntry.configure(background="#ffffff",text="0")
        self.totalEntry.place(anchor="nw", relheight=0.1, relwidth=0.4, relx=0.35, rely=0.40)

        confirmbt = tk.Button(self.root)
        confirmbt.configure(background="#ff6f61", default="normal",command=self.add_sale, state="normal", text='confirm')
        confirmbt.place(anchor="nw", relheight=0.1, relwidth=0.3, relx=0.35, rely=0.52)
        addProduct = tk.Button(self.root)
        addProduct.configure(background="#ff6f61", default="normal",command=self.add_product, state="normal", text='ADD PRODUCTS')
        addProduct.place(anchor="nw", relheight=0.1, relwidth=0.3, relx=0.05, rely=0.28)
        self.done = tk.Label(self.root)

        alarm = tk.Label(self.root)
        alarm.configure(background="#ffffff")
        alarm.pack(fill="x", side="top")

# Create the main window
root = tk.Tk()
sale_manager = SaleManager(root)

# Start the main loop
root.mainloop()
