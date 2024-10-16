from tkinter import messagebox
import mysql.connector as con
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import subprocess
import sys


class EmployeeManager:
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
        bg_image = Image.open("employeee.jpg")
        resized_bg_image = bg_image.resize((1050, 300))
        self.tk_bg_image = ImageTk.PhotoImage(resized_bg_image)  # Store as an attribute
        bg_label = tk.Label(self.root, image=self.tk_bg_image)
        bg_label.place(relwidth=1, relheight=1.5)

        # ScrolledText widget
        self.datatxt = ScrolledText(self.root, background="#FFFFFF")
        self.datatxt.place(anchor="nw", relheight=0.6, relwidth=1.0)

        # Labels and Entry widgets
        labels = ['Employee ID:', 'Username:', 'Name:', 'Position:']
        self.entries = [tk.Entry(self.root, background="#EEEEEE") for _ in range(4)]

        for i, label_text in enumerate(labels):
            label_color = "#FF8C00" if i % 2 == 0 else "#00ADB5"
            label = tk.Label(self.root, background=label_color, text=label_text)
            label.place(anchor="nw", relwidth=0.15, relx=0.02, rely=0.7 + i * 0.05)

            entry = self.entries[i]
            entry.place(anchor="nw", relwidth=0.2, relx=0.17, rely=0.7 + i * 0.05)

        self.eidtxt, self.usernametxt, self.nametxt, self.titletxt = self.entries

        # Buttons
        show_employees_bt = tk.Button(self.root, command=self.show_employee, background="#00ADB5", text='Show Employees')
        show_employees_bt.place(anchor="nw", relwidth=0.2, relx=0.7, rely=0.7)

        remove_employee_bt = tk.Button(self.root, background="#00ADB5", command=self.show_confirmation, text='Remove Employee')
        remove_employee_bt.place(anchor="nw", relwidth=0.2, relx=0.7, rely=0.75)

        back_bt = tk.Button(self.root, command=self.go_back, background="#00ADB5", text='Back')
        back_bt.place(anchor="nw", relwidth=0.2, relx=0.7, rely=0.8)

    def show_employee(self):
        # Function to display employee details based on user input
        self.datatxt.configure(state='normal')
        connection = con.connect(host="localhost", user="root", password="H123hamza", database="supermarket_sql",
                                 port="3306")
        cursor = connection.cursor()
        self.datatxt.delete('1.0', tk.END)

        query = "select employeeid,username,name,email,age,phone,position from employee"

        try:
            if self.eidtxt.get() != '':
                query += " where employeeid = " + self.eidtxt.get()
            elif self.usernametxt.get() != '':
                query += " where username = '" + self.usernametxt.get() + "'"
            elif self.nametxt.get() != '':
                query += " where name = '" + self.nametxt.get() + "'"
            elif self.titletxt.get() != '':
                query += " where position = '" + self.titletxt.get() + "'"

            cursor.execute(query)
        except:
            self.datatxt.insert(tk.END, "Invalid query or employee does not exist")

        try:
            data = cursor.fetchall()
            self.datatxt.insert('1.0', "employeeid\t\tusername\t\tname\t\temail\t\t\tage\t\tphone\t\tposition\n")

            if len(data) != 0:
                for row in data:
                    line = f"{row[0]}\t\t{row[1]}\t\t{row[2]}\t\t{row[3]}\t\t\t{row[4]}\t\t{row[5]}\t\t{row[6]}"
                    self.datatxt.insert(tk.END, line + "\n")

            self.datatxt.configure(state='disabled')
        except:
            self.datatxt.insert(tk.INSERT, "Couldn't fetch data!\n")

        cursor.close()
        connection.close()

    def remove_employee(self):
        # Function to remove an employee from the database
        self.datatxt.configure(state='normal')
        connection = con.connect(host="localhost", user="root", password="H123hamza", database="supermarket_sql",
                                 port="3306")
        cursor = connection.cursor()
        self.datatxt.delete('1.0', tk.END)

        query = "update employee set position = 'unemployed' where employeeID = '" + self.eidtxt.get() + "'"

        try:
            if self.eidtxt.get() != '':
                if int(self.eidtxt.get()) == int(self.eid):
                    self.datatxt.insert(tk.END, "You cannot remove yourself")
                else:
                    cursor.execute(query)
                    connection.commit()
                    self.datatxt.insert(tk.END, "Employee removed successfully")
                    self.datatxt.configure(state='disabled')
            else:
                self.datatxt.insert(tk.END, "Employee ID field is empty or employee does not exist")
                self.datatxt.configure(state='disabled')
        except:
            self.datatxt.insert(tk.END, "Invalid query or employee does not exist")

        cursor.close()
        connection.close()

    def show_confirmation(self):
        # Function to display confirmation dialog before removing an employee
        result = messagebox.askyesno("Confirmation", "Are you sure you want to remove employee?")

        if result:
            self.remove_employee()
        else:
            self.datatxt.configure(state='normal')
            self.datatxt.delete('1.0', tk.END)
            self.datatxt.insert(tk.END, "Employee not removed")
            self.datatxt.configure(state='disabled')

    def go_back(self):
        # Function to go back to the manager page
        self.root.destroy()
        subprocess.run(["python", "control_center.py", self.username, self.title, str(self.eid)])


# Command line arguments
username = sys.argv[1]
title = sys.argv[2]
eid = int(sys.argv[3])

# Create the main window
root = tk.Tk()
employee_manager = EmployeeManager(root, username, title, eid)

# Start the main loop
root.mainloop()
