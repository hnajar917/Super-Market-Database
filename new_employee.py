import mysql.connector as con
import tkinter as tk
from PIL import Image, ImageTk

class EmployeeAddition:
    def __init__(self, root):
        self.root = root
        self.setup_ui()

    def add_employee(self):
        connection = con.connect(host="localhost", user="root", password="H123hamza", database="supermarket_sql", port="3306")
        cursor = connection.cursor()

        query = "INSERT INTO employee (username, name, password, email, phone, age, position) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (self.usernametxt.get(), self.nametxt.get(), self.passwordtxt.get(), self.emailtxt.get(), self.phonetxt.get(), self.agetxt.get(), "employee")

        if self.usernametxt.get() == '' or self.nametxt.get() == '' or self.passwordtxt.get() == '' or self.emailtxt.get() == '' or self.phonetxt.get() == '' or self.agetxt.get() == '':
            self.alarm.configure(text="Please fill the empty fields", fg="red", font=("bold", 14))
        else:
            cursor.execute("SELECT * FROM employee")
            temprows = cursor.fetchall()
            try:
                flag = 1
                for row in temprows:
                    if self.usernametxt.get() in row:
                        flag = 0
                        self.alarm.configure(text="Username already exists", fg="red", font=("bold", 14))
                    elif self.emailtxt.get() in row:
                        flag = 0
                        self.alarm.configure(text="Email already exists", fg="red", font=("bold", 14))
                    elif self.phonetxt.get() in row:
                        flag = 0
                        self.alarm.configure(text="Phone already exists", fg="red", font=("bold", 14))

                if flag == 1:
                    cursor.execute(query, values)
                    connection.commit()
                    self.alarm.configure(text="Employee added successfully", fg="green", font=("bold", 14))
            except con.Error as error:
                self.alarm.configure(text="Failed to add employee {}".format(error), fg="red", font=("bold", 14))

            cursor.close()
            connection.close()

    def setup_ui(self):
        self.root.title("Add Employee")
        self.root.geometry("850x650")

        # Load and resize the background image
        try:
            bg_image = Image.open("background.png")
            resized_bg_image = bg_image.resize((425, 650))  # Adjust dimensions as needed
            self.tk_bg_image = ImageTk.PhotoImage(resized_bg_image)
            background_label = tk.Label(self.root, image=self.tk_bg_image)
            background_label.place(anchor="nw", relx=0, rely=0, relwidth=0.5, relheight=1)
        except tk.TclError as e:
            print(f"Error loading image: {e}")

        label_style = {"background": "#2E3537", "font": ('bold', 14), "fg": "white"}
        entry_style = {"background": "#2E3537", "font": ('bold', 14), "fg": "white"}
        button_style = {"background": "#2E3537", "text": 'Add Employee', "command": self.add_employee, "font": ('bold', 14), "fg": "white"}
        alarm_style = {"highlightthickness": 1, "bd": 0, "bg": "#2E3537", "justify": "center", "font": ('bold', 14), "fg": "white"}

        self.usernamelbl = tk.Label(self.root, text='Username', **label_style)
        self.usernamelbl.place(anchor="nw", relwidth=0.12, relx=0.53, rely=0.2)

        self.namelbl = tk.Label(self.root, text='Name', **label_style)
        self.namelbl.place(anchor="nw", relwidth=0.12, relx=0.53, rely=0.3)

        self.passwordlbl = tk.Label(self.root, text='Password', **label_style)
        self.passwordlbl.place(anchor="nw", relwidth=0.12, relx=0.53, rely=0.4)

        self.emaillbl = tk.Label(self.root, text='Email', **label_style)
        self.emaillbl.place(anchor="nw", relwidth=0.12, relx=0.53, rely=0.5)

        self.phonelbl = tk.Label(self.root, text='Phone', **label_style)
        self.phonelbl.place(anchor="nw", relwidth=0.12, relx=0.53, rely=0.6)

        self.agelbl = tk.Label(self.root, text='Age', **label_style)
        self.agelbl.place(anchor="nw", relwidth=0.12, relx=0.53, rely=0.7)

        self.usernametxt = tk.Entry(self.root, **entry_style)
        self.usernametxt.place(anchor="nw", relx=0.66, rely=0.2, x=0, y=0, relwidth=0.3)

        self.nametxt = tk.Entry(self.root, **entry_style)
        self.nametxt.place(anchor="nw", relx=0.66, rely=0.3, x=0, y=0, relwidth=0.3)

        self.passwordtxt = tk.Entry(self.root, show="•", **entry_style)
        self.passwordtxt.place(anchor="nw", relx=0.66, rely=0.4, x=0, y=0, relwidth=0.3)

        self.emailtxt = tk.Entry(self.root, **entry_style)
        self.emailtxt.place(anchor="nw", relx=0.66, rely=0.5, x=0, y=0, relwidth=0.3)

        self.phonetxt = tk.Entry(self.root, **entry_style)
        self.phonetxt.place(anchor="nw", relx=0.66, rely=0.6, x=0, y=0, relwidth=0.3)

        self.agetxt = tk.Entry(self.root, **entry_style)
        self.agetxt.place(anchor="nw", relx=0.66, rely=0.7, x=0, y=0, relwidth=0.3)

        self.addEmployeebt = tk.Button(self.root, **button_style)
        self.addEmployeebt.place(anchor="nw", relheight=0.1, relwidth=0.2, relx=0.75, rely=0.8)

        self.alarm = tk.Label(self.root, **alarm_style)
        self.alarm.place(anchor="nw", relheight=0.1, relwidth=0.5, x=0, y=0)

# Create the main window
root = tk.Tk()
employee_addition = EmployeeAddition(root)

# Start the main loop
root.mainloop()
