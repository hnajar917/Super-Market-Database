import mysql.connector as con
import tkinter as tk
from tkinter import messagebox
import subprocess

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1050x600')
        self.root.configure(bg="#F0D9C7")  # Set background color to Sand

        self.setup_ui()

    def open_manager_page(self, user, title, eid):
        self.root.destroy()
        subprocess.run(["python", "control_center.py", user, title, str(eid)])

    def open_employee_page(self, user, title, eid):
        self.root.destroy()
        subprocess.run(["python", "employee_home.py", user, title, str(eid)])

    def confirm_login(self):
        connection = con.connect(host="localhost", user="root", password="H123hamza", database="supermarket_sql", port="3306")
        cursor = connection.cursor()
        query = "SELECT * FROM employee WHERE username = %s"
        cursor.execute(query, (self.entry1.get(),))
        data = cursor.fetchall()

        if self.entry1.get() == "" or self.entry2.get() == "" or not data or len(data[0]) == 0:
            self.alarm.config(text="Username not found or password incorrect!", fg="red")
            self.alarm.pack()
        else:
            title = data[0][7]
            eid = data[0][0]
            if data[0][7] == "manager" and data[0][3] == self.entry2.get():
                self.open_manager_page(self.entry1.get(), title, eid)
            elif data[0][7] == "employee" and data[0][3] == self.entry2.get():
                self.open_employee_page(self.entry1.get(), title, eid)
            elif data[0][7] == "manager" and data[0][3] != self.entry2.get():
                self.alarm.config(text="Username not found or password incorrect!", fg="red")
                self.alarm.pack()
            elif data[0][7] == "employee" and data[0][3] != self.entry2.get():
                self.alarm.config(text="Username not found or password incorrect!", fg="red")
                self.alarm.pack()
            else:
                self.alarm.config(text="User title unknown!", fg="red")
                self.alarm.pack()

        connection.commit()
        cursor.close()
        connection.close()

    def setup_ui(self):
        image1 = tk.PhotoImage(file="xx.png")
        image1 = image1.zoom(2)  # Zoom the image
        image1 = image1.subsample(14, 14)
        background_label = tk.Label(self.root, image=image1, bg="#F0D9C7")
        background_label.image = image1
        background_label.place(anchor="center", relx=0.5, rely=0.5, relwidth=1, relheight=1)

        labelLogin = tk.Label(text="LOG IN", bg="#F0D9C7", font=("bold", 25), fg="#404040")
        labelLogin.place(anchor="center", relheight=0.15, relwidth=0.2, relx=0.5, rely=0.4)

        labelUsername = tk.Label(text="USERNAME", font=("Helvetica", 12), bg="#F0D9C7", fg="#404040")
        labelUsername.place(anchor="center", relheight=0.04, relwidth=0.14, relx=0.45, rely=0.55)

        labelPassword = tk.Label(text="PASSWORD", font=("Helvetica", 12), bg="#F0D9C7", fg="#404040")
        labelPassword.place(anchor="center", relheight=0.04, relwidth=0.14, relx=0.45, rely=0.65)

        self.entry1 = tk.Entry(self.root, bd=2, fg="#404040", font=("dark bold", 20))
        self.entry1.place(anchor="center", relheight=0.04, relwidth=0.15, relx=0.58, rely=0.55)

        self.entry2 = tk.Entry(self.root, bd=2, font=("dark bold", 20), show="*")
        self.entry2.place(anchor="center", relheight=0.04, relwidth=0.15, relx=0.58, rely=0.65)

        button = tk.Button(text="lets go", cursor="hand2", command=self.confirm_login, bg="#f28749", font=("Helvetica", 20), fg="#404040")
        button.place(anchor="center", relheight=0.1, relwidth=0.1, relx=0.5, rely=0.75)

        self.alarm = tk.Label(self.root, text="", bg="#F0D9C7", fg="red", font=("bold", 20))


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
