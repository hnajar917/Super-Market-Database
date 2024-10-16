import mysql.connector as con
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import sys
from PIL import Image, ImageTk
import subprocess

# Function to go back to the previous page
def go_back(username, title, eid):
    print("Going back to the previous page...")

    root.quit()  # Terminate Tkinter main loop
    root.destroy()

    # Determine which page to go back to based on the user's title
    if title == 'manager':
        try:
            subprocess.run(["python", "control_center.py", username, title, str(eid)])
        except Exception as e:
            print(f"Error opening control_center: {e}")
    else:
        try:
            subprocess.run(["python", "employee_home.py", username, title, str(eid)])
        except Exception as e:
            print(f"Error opening employee_page.py: {e}")

# Command-line arguments
username = sys.argv[1]
title = sys.argv[2]
eid = int(sys.argv[3])

# Create the main window
root = tk.Tk()
root.configure(background="#116A7B", height=200, width=200)
root.geometry("1050x600")
root.geometry("+100+20")

# Load and display the background image
bg_image = Image.open("openSale.png.jpg")
resized_bg_image = bg_image.resize((1050, 370))
tk_bg_image = ImageTk.PhotoImage(resized_bg_image)
bg_label = tk.Label(root, image=tk_bg_image)
bg_label.place(relwidth=1, relheight=1.8)

# ScrolledText widget to display data
datatxt = ScrolledText(root, background="#ffffff")
datatxt.place(anchor="nw", relheight=0.6, relwidth=1.0)

# Entry widgets for filtering
sidtxt = tk.Entry(root, background="#ECE5C7")
sidtxt.place(anchor="nw", relwidth=0.16, relx=0.14, rely=0.7)

cidtxt = tk.Entry(root, background="#ECE5C7")
cidtxt.place(anchor="nw", relwidth=0.16, relx=0.14, rely=0.75)

sdatetxt = tk.Entry(root, background="#ECE5C7")
sdatetxt.place(anchor="nw", relwidth=0.16, relx=0.14, rely=0.8)

# Labels for entry widgets
sidlbl = tk.Label(root)
sidlbl.configure(text='saleid', background="#89CFF0")
sidlbl.place(anchor="nw", relwidth=0.08, relx=0.02, rely=0.7)

cidlbl = tk.Label(root, background="#89CFF0")
cidlbl.configure(text='customerid')
cidlbl.place(anchor="nw", relwidth=0.08, relx=0.02, rely=0.75)

sdatelbl = tk.Label(root, background="#89CFF0")
sdatelbl.configure(text='time')
sdatelbl.place(anchor="nw", relwidth=0.08, relx=0.02, rely=0.8)

# Buttons to show sold items, sales, and go back
itemsbt = tk.Button(root, command=lambda: show_sold_items(title, eid), background="#C2DEDC")
itemsbt.configure(text='show sold items')
itemsbt.place(anchor="nw", relwidth=0.2, relx=0.7, rely=0.78)

salesbt = tk.Button(root, command=lambda: show_sales(title, eid), background="#C2DEDC")
salesbt.configure(text='show sales')
salesbt.place(anchor="nw", relwidth=0.2, relx=0.7, rely=0.70)

backbt = tk.Button(root, command=lambda: go_back(username, title, eid), background="#C2DEDC")
backbt.configure(text='back')
backbt.place(anchor="nw", relwidth=0.2, relx=0.7, rely=0.86)

# Additional labels and entry widgets for manager
if (title == 'manager'):
    eidlbl = tk.Label(root, background="#89CFF0")
    eidlbl.configure(text='employeeid')
    eidlbl.place(anchor="nw", relwidth=0.08, relx=0.02, rely=0.85)

    eidtxt = tk.Entry(root, background="#ECE5C7")
    eidtxt.place(anchor="nw", relwidth=0.16, relx=0.14, rely=0.85)

# Function to display sales based on filters
def show_sales(title, eid):
    datatxt.configure(state='normal')
    connection = con.connect(host="localhost", user="root", password="H123hamza", database="supermarket_sql", port="3306")

    cursor = connection.cursor()

    datatxt.delete('1.0', tk.END)

    if (title == 'manager'):
        query = "select * from sales"
        try:
            # Build the query based on the provided filters
            if (sidtxt.get() != ''):
                query += " where saleid = %s"
                cursor.execute(query, (sidtxt.get(),))
            elif (cidtxt.get() != '' and sdatetxt.get() != ''):
                query += " where customerid = %s and time = %s"
                cursor.execute(query, (cidtxt.get(), sdatetxt.get(),))
            elif (eidtxt.get() != '' and sdatetxt.get() != ''):
                query += " where employeeid = %s and time = %s"
                cursor.execute(query, (eidtxt.get(), sdatetxt.get(),))
            elif (eidtxt.get() != '' and cidtxt.get() != ''):
                query += " where employeeid = %s and customerid = %s"
                cursor.execute(query, (eidtxt.get(), cidtxt.get(),))
            elif (cidtxt.get() != '' and sdatetxt.get() != '' and eidtxt.get() != ''):
                query += " where customerid = %s and time = %s and employeeid = %s"
                cursor.execute(query, (cidtxt.get(), sdatetxt.get(), eidtxt.get()))
            elif (eidtxt.get() != ''):
                query += " where employeeid = %s"
                cursor.execute(query, (eidtxt.get(),))
            elif (cidtxt.get() != ''):
                query += " where customerid = %s"
                cursor.execute(query, (cidtxt.get(),))
            elif (sdatetxt.get() != ''):
                query += " where time = %s"
                cursor.execute(query, (sdatetxt.get(),))
            else:
                cursor.execute(query)
        except:
            datatxt.insert(tk.INSERT, "Invalid filters\n")

    else:
        query = "select * from sales where employeeid = %s"
        try:
            # Build the query based on the provided filters
            if (sidtxt.get() != ''):
                query += " and saleid = %s"
                cursor.execute(query, (eid, sidtxt.get(),))
            elif (cidtxt.get() != '' and sdatetxt.get() != ''):
                query += " and customerid = %s and time = %s"
                cursor.execute(query, (eid, cidtxt.get(), sdatetxt.get(),))
            elif (cidtxt.get() != ''):
                query += " and customerid = %s"
                cursor.execute(query, (eid, cidtxt.get(),))
            elif (sdatetxt.get() != ''):
                query += " and time = %s"
                cursor.execute(query, (eid, sdatetxt.get(),))
            else:
                cursor.execute(query, (eid,))
        except:
            datatxt.insert(tk.INSERT, "Invalid filters\n")

    try:
        data = cursor.fetchall()

        # Define standard column widths
        col_widths = {'saleid': 10, 'customerid': 12, 'employeeid': 12, 'payment_method': 15, 'cost': 10, 'time': 10}

        # Table Header
        header = "┌{0}┬{1}┬{2}┬{3}┬{4}┬{5}┐\n".format('─' * col_widths['saleid'], '─' * col_widths['customerid'],
                                                      '─' * col_widths['employeeid'],
                                                      '─' * col_widths['payment_method'],
                                                      '─' * col_widths['cost'], '─' * col_widths['time'])
        header += "│{:^10}│{:^12}│{:^12}│{:^15}│{:^10}│{:^10}│\n".format('saleid', 'customerid', 'employeeid',
                                                                         'payment_method', 'cost', 'time')
        header += "├{0}┼{1}┼{2}┼{3}┼{4}┼{5}┤\n".format('─' * col_widths['saleid'], '─' * col_widths['customerid'],
                                                       '─' * col_widths['employeeid'],
                                                       '─' * col_widths['payment_method'],
                                                       '─' * col_widths['cost'], '─' * col_widths['time'])
        datatxt.insert('1.0', header)

        if len(data) != 0:
            for row in data:
                line = "│{:<10}│{:<12}│{:<12}│{:<15}│{:<10}│{:<10}│\n".format(str(row[0])[:10],
                                                                              str(row[1])[:12],
                                                                              str(row[2])[:12],
                                                                              str(row[3])[:15],
                                                                              str(row[4])[:10],
                                                                              str(row[5])[:10])
                datatxt.insert(tk.END, line)

        # Table Footer
        footer = "└{0}┴{1}┴{2}┴{3}┴{4}┴{5}┘\n".format('─' * col_widths['saleid'], '─' * col_widths['customerid'],
                                                      '─' * col_widths['employeeid'],
                                                      '─' * col_widths['payment_method'],
                                                      '─' * col_widths['cost'], '─' * col_widths['time'])
        datatxt.insert(tk.END, footer)
    except Exception as e:
        datatxt.insert(tk.INSERT, f"Couldn't fetch data! Error: {e}\n")
    finally:
        datatxt.configure(state='disabled')
        cursor.close()
        connection.close()

# Function to display sold items based on filters
def show_sold_items(title, eid):
    datatxt.configure(state='normal')
    connection = con.connect(host="localhost", user="root", password="H123hamza", database="supermarket_sql", port="3306")

    cursor = connection.cursor()

    # Debug print to check the values of eid and other variables
    print(f"title: {title}, eid: {eid}, sidtxt: {sidtxt.get()}, cidtxt: {cidtxt.get()}")

    if (title == 'employee'):
        query = "select * from sold_item where saleid in (select saleid from sales where employeeid = %s)"
        try:
            if (sidtxt.get() != ''):
                query += " and saleid = %s"
                cursor.execute(query, (eid, sidtxt.get(),))
            elif (cidtxt.get() != ''):
                query = "select * from sold_item where saleid in (select saleid from sales where employeeid = %s and customerid = %s)"
                cursor.execute(query, (eid, cidtxt.get(),))
            else:
                cursor.execute(query, (eid,))
        except Exception as e:
            print(f"Error executing query: {e}")
            datatxt.insert(tk.INSERT, f"Error executing query: {e}\n")
            return
    else:
        # The manager part of the code remains unchanged
        query = "select * from sold_item"
        try:
            if (sidtxt.get() != ''):
                query += " where saleid = %s"
                cursor.execute(query, (sidtxt.get(),))
            elif (cidtxt.get() != '' and eidtxt.get() != ''):
                query += " where saleid in (select saleid from sales where customerid = %s and employeeid = %s)"
                cursor.execute(query, (cidtxt.get(), eidtxt.get(),))
            elif (cidtxt.get() != ''):
                query += " where saleid in (select saleid from sales where customerid = %s)"
                cursor.execute(query, (cidtxt.get(),))
            elif (eidtxt.get() != ''):
                query += " where saleid in (select saleid from sales where employeeid = %s)"
                cursor.execute(query, (eidtxt.get(),))
            else:
                cursor.execute(query)
        except Exception as e:
            datatxt.insert(tk.INSERT, f"Error executing manager query: {e}\n")
            print(f"Error executing manager query: {e}")

    try:
        data = cursor.fetchall()
        datatxt.delete('1.0', tk.END)

        # Adjusted column widths based on content
        col_widths = {'solditemID': 10, 'productID': 25, 'saleID': 10, 'quantity': 10, 'price': 12, 'product name': 15}

        # Table Header
        header = "┌{0}┬{1}┬{2}┬{3}┬{4}┬{5}┐\n".format('─' * col_widths['solditemID'], '─' * col_widths['productID'],
                                                      '─' * col_widths['saleID'], '─' * col_widths['quantity'],
                                                      '─' * col_widths['price'], '─' * col_widths['product name'])
        header += "│{:^10}│{:^25}│{:^10}│{:^10}│{:^12}│{:^15}│\n".format('solditemID', 'productID', 'saleID',
                                                                         'quantity', 'price', 'product name')
        header += "├{0}┼{1}┼{2}┼{3}┼{4}┼{5}┤\n".format('─' * col_widths['solditemID'], '─' * col_widths['productID'],
                                                       '─' * col_widths['saleID'], '─' * col_widths['quantity'],
                                                       '─' * col_widths['price'], '─' * col_widths['product name'])
        datatxt.insert(tk.END, header)

        if len(data) != 0:
            for row in data:
                line = "│{:<10}│{:<25}│{:<10}│{:<10}│{:<12}│{:<15}│\n".format(str(row[0])[:10],
                                                                              str(row[1])[:25],
                                                                              str(row[2])[:10],
                                                                              str(row[3])[:10],
                                                                              str(row[4])[:12],
                                                                              str(row[5])[:15])
                datatxt.insert(tk.END, line)

        # Table Footer
        footer = "└{0}┴{1}┴{2}┴{3}┴{4}┴{5}┘\n".format('─' * col_widths['solditemID'], '─' * col_widths['productID'],
                                                      '─' * col_widths['saleID'], '─' * col_widths['quantity'],
                                                      '─' * col_widths['price'], '─' * col_widths['product name'])
        datatxt.insert(tk.END, footer)
    except Exception as e:
        print(f"Error fetching data: {e}")
    finally:
        datatxt.configure(state='disabled')
        cursor.close()
        connection.close()


root.mainloop()