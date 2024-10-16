import tkinter as tk
from tkinter import ttk
import mysql.connector as con
import sys
from queue import Queue
from tkinter import font
import subprocess
import pymysql
from PIL import Image, ImageTk
from tkinter import ttk




root2 = tk.Tk()
root2.configure(background="#ffffff", height=200, width=200)
root2.geometry("800x500")

bg_image = Image.open("productInsale.png")
resized_bg_image = bg_image.resize((600, 580))  # Resize the image to match the window size

# Convert the resized image to a format Tkinter can use
bg_photo_image = ImageTk.PhotoImage(resized_bg_image)

# Create a label with the image and set it to cover the entire window
bg_label = tk.Label(root2, image=bg_photo_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

cost = 0
combo = ttk.Combobox(root2)
saleID = sys.argv[1]
text_area = tk.Text(root2, width=70, height=10)
text_area.place(x=200, y=130)
text_area.configure(background="#ffffff")

def fetch_product_names():
    connection = con.connect(host='localhost', database='supermarket_sql', user='root', password='H123hamza', port='3306')

    cursor = connection.cursor()
    cursor.execute("SELECT name FROM products")  # Assuming 'name' is the column name for product names
    products = cursor.fetchall()
    connection.close()
    return [item[0] for item in products]  # Extracting product names

# Insert text into the text area
text_area.insert(tk.END, "solditemID            PRODUCT_NAME          QUANTITY          PRICE")
queue = Queue()

def add_product():
    combo.place(x=-1000, y=-1000)
    done = tk.Label(root2)
    if nameCombo.get() == "" and quantityEntry.get() == "":
        done.configure(background="#00C4FF", text='make sure to provide all data fields')
        done.place(x=70, y=280)
    else:
        connection = con.connect(host='localhost', database='supermarket_sql', user='root', password='H123hamza',
                                 port='3306')

        cursor = connection.cursor()
        query = "select price, quantity,productID from products where name ='" + str(nameCombo.get()) + "'"
        print(query)
        cursor.execute(query)
        data = cursor.fetchall()
        priceReal = int(data[0][0])
        productID = data[0][2]
        quantityReal = int(data[0][1])
        price = priceReal * int(quantityEntry.get())
        print(price)

        if quantityReal < int(quantityEntry.get()):
            done.configure(text="there is not enough quantity")
        else:
            connection = con.connect(host='localhost', database='supermarket_sql', user='root',
                                     password='H123hamza', port='3306')

            cursor = connection.cursor()
            quantityReal = quantityReal - int(quantityEntry.get())
            query = "UPDATE products SET quantity = " + str(quantityReal) + " WHERE name ='" + str(nameCombo.get()) + "'"
            cursor.execute(query)
            connection.commit()
            cursor.close()
            connection.close()

            connection = con.connect(host='localhost', database='supermarket_sql', user='root',
                                     password='H123hamza', port='3306')

            cursor = connection.cursor()
            query = "INSERT INTO sold_item (productID,productName,saleID, quantity,price) VALUES ('" + str(
                productID) + "','" + nameCombo.get() + "','" + str(saleID) + "'," + "'" + quantityEntry.get() + "','" + str(price) + "')"
            cursor.execute(query)
            connection.commit()
            cursor.close()
            connection.close()
            connection = con.connect(host='localhost', database='supermarket_sql', user='root',
                                     password='H123hamza', port='3306')

            cursor = connection.cursor()
            query = "select sum(price) from sold_item where saleID='" + str(saleID) + "'"
            cursor.execute(query)
            data = cursor.fetchall()
            cost = data[0][0]
            connection.commit()
            cursor.close()
            connection.close()

            connection = con.connect(host='localhost', database='supermarket_sql', user='root',
                                     password='H123hamza', port='3306')

            cursor = connection.cursor()
            query = "select max(solditemID) from sold_item "
            cursor.execute(query)
            data = cursor.fetchall()
            soldID = data[0][0]
            connection.commit()
            cursor.close()
            connection.close()
            textString = "\n" + str(soldID) + "          " + nameCombo.get() + "          " + "" + quantityEntry.get() + "           " + "" + str(price)
            queue.put(textString)
            text_area.insert(tk.END, "\n" + str(soldID) + "\t\t\t" + nameCombo.get() + "\t\t\t" + "" + quantityEntry.get() + "\t\t" + "" + str(price))

            nameCombo.delete(0, tk.END)
            quantityEntry.delete(0, tk.END)

fontt = font.Font(size=20)
name = tk.Label(root2)
name.configure(background="#00C4FF", width=20, height=2, text='NAME')
name.place(x=70, y=20)
quantity = tk.Label(root2)
quantity.configure(background="#00C4FF", width=20, height=2, text='QUANTITY')
quantity.place(x=70, y=80)

product_names = fetch_product_names()

nameCombo = ttk.Combobox(root2, values=product_names)
nameCombo.configure(background="#FFF5B8", font=fontt)
nameCombo.place(x=200, y=20)

quantityEntry = tk.Entry(root2)
quantityEntry.configure(background="#ffffff", font=fontt)
quantityEntry.place(x=200, y=80)

confirmbt = tk.Button(root2)
confirmbt.configure(background="#30A2FF", width=13, height=2, default="normal", state="normal", text='confirm', command=lambda: add_product())
confirmbt.place(x=70, y=130)

def remove_single_product(event):
    text = combo.get()
    text2 = text
    combo.delete(combo['values'].index(text))
    deletedSoldID = text.split()[0]

    connection = con.connect(host='localhost', database='supermarket_sql', user='root', password='H123hamza', port='3306')

    cursor = connection.cursor()
    query = "select quantity from sold_item where solditemID = " + deletedSoldID
    cursor.execute(query)
    data = cursor.fetchall()
    quantity_b = data[0][0]
    connection.commit()
    cursor.close()
    connection.close()

    connection = con.connect(host='localhost', database='supermarket_sql', user='root', password='H123hamza', port='3306')

    cursor = connection.cursor()
    query = "update products set quantity = quantity + " + str(
        quantity_b) + " where productID = (select productID from sold_item where solditemID = " + deletedSoldID + ")"
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()

    connection = con.connect(host='localhost', database='supermarket_sql', user='root', password='H123hamza', port='3306')

    cursor = connection.cursor()
    query = "delete from sold_item where solditemID =" + deletedSoldID
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()

    connection = con.connect(host='localhost', database='supermarket_sql', user='root', password='H123hamza', port='3306')

    cursor = connection.cursor()
    query = "select solditemID,productName ,quantity,price from sold_item where saleID =" + saleID
    cursor.execute(query)
    buildTextArea = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()

    print(buildTextArea)

    text_area.delete("1.0", "end")
    text_area.insert(tk.END, "solditemID            PRODUCT_NAME          QUANTITY          PRICE")
    combo['values'] = ()
    queue2 = Queue()
    for row in buildTextArea:
        text_area.insert(tk.END, "\n" + "" + str(row[0]) + "\t\t\t" + row[1] + "\t\t\t" + str(row[2]) + "\t\t" + str(row[3]))
        item = "" + str(row[0]) + "   " + " " + row[1] + "    " + str(row[2]) + "   " + str(row[3])
        queue2.put(item)
    while not queue.empty():
        queue.get()

    combo['values'] = list(queue2.queue)
    while not queue2.empty():
        queue.put(queue2.get())

def remove_product():
    combo.place(x=70, y=320, width=350, height=30)
    combo['values'] = list(queue.queue)
    combo.bind("<<ComboboxSelected>>", remove_single_product)

remove = tk.Button(root2)
remove.configure(background="#30A2FF", width=13, height=2, default="normal", state="normal", text='remove product',
                 command=lambda: remove_product())
remove.place(x=70, y=180)

def exit():
    connection = con.connect(host='localhost', database='supermarket_sql', user='root', password='H123hamza', port='3306')

    cursor = connection.cursor()
    query2 = query = "UPDATE sales SET cost = " + str(cost) + " WHERE saleID =" + str(saleID)
    cursor.execute(query2)
    connection.commit()
    cursor.close()
    connection.close()

    root2.destroy()

exitt = tk.Button(root2, width=10, height=1)
exitt.configure(background="#30A2FF", width=13, height=2, default="normal", command=lambda: exit(), state="normal", text='exit')
exitt.place(x=70, y=230)

alarm = tk.Label(root2)
alarm.configure(background="#ffffff")
alarm.pack(fill="x", side="top")
root2.mainloop()
