import tkinter as tk
import mysql.connector as con
from PIL import Image, ImageTk
import sys

class PasswordUpdater:
    def __init__(self, root):
        self.root = root
        self.setup_ui()

    def setup_ui(self):
        self.root.configure(background="white", height=200, width=200)
        self.root.geometry("850x650")

        label_style = {"background": "#ADD8E6", "font": ('bold', 14), "fg": "black", "borderwidth": 1, "relief": "solid"}
        entry_style = {"background": "white", "font": ('bold', 14), "fg": "black", "borderwidth": 1, "relief": "solid"}
        button_style = {"background": "#00BFFF", "text": 'Change Password', "command": self.update_password,
                        "font": ('bold', 14), "fg": "white", "bd": 0}

        try:
            original_image = Image.open("change password.png")
            resized_image = original_image.resize((int(850 * 0.5), int(650)))
            image2 = ImageTk.PhotoImage(resized_image)
            background_label = tk.Label(self.root, image=image2)
            background_label.photo = image2  # Keep a reference to avoid garbage collection
            background_label.place(anchor="nw", relx=0, rely=0, relwidth=0.5, relheight=1)
        except Exception as e:
            print(f"Error loading image: {e}")

        usernamelbl = tk.Label(self.root, text='Username', **label_style)
        usernamelbl.place(anchor="nw", relwidth=0.2, relx=0.5, rely=0.1)

        old_password_lbl = tk.Label(self.root, text='Old Password', **label_style)
        old_password_lbl.place(anchor="nw", relwidth=0.2, relx=0.5, rely=0.3)

        new_password_lbl = tk.Label(self.root, text='New Password', **label_style)
        new_password_lbl.place(anchor="nw", relwidth=0.2, relx=0.5, rely=0.5)

        confirm_password_lbl = tk.Label(self.root, text='Confirm Password', **label_style)
        confirm_password_lbl.place(anchor="nw", relwidth=0.2, relx=0.5, rely=0.7)

        self.usernametxt = tk.Entry(self.root, **entry_style)
        self.usernametxt.place(anchor="nw", relwidth=0.25, relx=0.72, rely=0.1)

        self.old_password_txt = tk.Entry(self.root, show="*", **entry_style)
        self.old_password_txt.place(anchor="nw", relwidth=0.25, relx=0.72, rely=0.3)

        self.new_password_txt = tk.Entry(self.root, show="*", **entry_style)
        self.new_password_txt.place(anchor="nw", relwidth=0.25, relx=0.72, rely=0.5)

        self.confirm_password_txt = tk.Entry(self.root, show="*", **entry_style)
        self.confirm_password_txt.place(anchor="nw", relwidth=0.25, relx=0.72, rely=0.7)

        change_password_bt = tk.Button(self.root, **button_style)
        change_password_bt.place(anchor="nw", relheight=0.1, relwidth=0.2, relx=0.75, rely=0.8)

        self.alarm = tk.Label(self.root, bg="white")
        self.alarm.pack(fill="x", side="top")

    def update_password(self):
        connection = con.connect(host="localhost", user="root", password="H123hamza", database="supermarket_sql", port="3306")
        cursor = connection.cursor()

        if len(sys.argv) > 1:
            username = sys.argv[1]
            query = "SELECT * FROM employee WHERE username = %s"
            cursor.execute(query, (username,))
            data = cursor.fetchall()

            if data:
                if data[0][3] == self.old_password_txt.get():
                    if self.new_password_txt.get() == self.confirm_password_txt.get() and self.new_password_txt.get() != "":
                        query = "UPDATE employee SET password = %s WHERE username = %s"
                        cursor.execute(query, (self.new_password_txt.get(), username,))
                        self.alarm.config(text="Password changed successfully!", bg="white", font=("bold", 20), fg="green")
                        self.alarm.pack()
                    else:
                        self.alarm.config(text="Passwords do not match or password not specified", bg="white", font=("bold", 20), fg="red")
                        self.alarm.pack()
                else:
                    self.alarm.config(text="Old password is incorrect", bg="white", font=("bold", 20), fg="red")
                    self.alarm.pack()
            else:
                self.alarm.config(text="Username not found", bg="white", font=("bold", 20), fg="red")
                self.alarm.pack()
        else:
            self.alarm.config(text="Username not provided", bg="white", font=("bold", 20), fg="red")
            self.alarm.pack()

        connection.commit()
        cursor.close()
        connection.close()

# Create the main window
root = tk.Tk()
password_updater = PasswordUpdater(root)

# Start the GUI main loop
root.mainloop()
