import tkinter as tk
import mysql.connector as con
from PIL import Image, ImageTk


class CustomerAdder:
    def __init__(self, root):
        self.root = root
        self.setup_ui()

    def setup_ui(self):
        self.root.configure(background="#FFE7A0", height=200, width=200)
        self.root.geometry("500x400")

        # Background image
        original_image = Image.open("backgroundCus.png")
        resized_image = original_image.resize((500, 400))  # Resize the image to window size
        self.bg_image = ImageTk.PhotoImage(resized_image)

        # Create a label with the image
        bg_label = tk.Label(self.root, image=self.bg_image)
        bg_label.place(relwidth=1, relheight=1)  # Make label cover the whole window

        # Labels and Entry widgets
        labels = ['NAME', 'PHONE', 'EMAIL']
        entries = [tk.Entry(self.root, background="#FFFFFF") for _ in range(3)]

        for i, label_text in enumerate(labels):
            label = tk.Label(self.root, background="#89CFF0", text=label_text)
            label.place(anchor="nw", relheight=0.1, relwidth=0.25, relx=0.05, rely=0.2 + i * 0.2)

            entry = entries[i]
            entry.configure(background="#FFFFFF")
            entry.place(anchor="nw", relheight=0.1, relwidth=0.4, relx=0.35, rely=0.2 + i * 0.2)

        self.nameEntry, self.phoneEntry, self.emailEntry = entries

        confirm_bt = tk.Button(self.root, background="#89CFF0", default="normal", state="normal", text='Confirm',
                               command=self.add_customer)
        confirm_bt.place(anchor="nw", relheight=0.1, relwidth=0.3, relx=0.4, rely=0.8)

        exit_bt = tk.Button(self.root, width=10, height=1, background="#89CFF0", default="normal", command=self.exit,
                            state="normal", text='Exit')
        exit_bt.place(x=0, y=325)

        # Label to display messages
        self.alarm = tk.Label(self.root, background="#FFFFFF")
        self.alarm.pack(fill="x", side="top")

    def add_customer(self):
        # Function to add customer details to the database
        done = tk.Label(self.root)
        connection = con.connect(host="localhost", user="root", password="H123hamza", database="supermarket_sql",
                                 port="3306")

        cursor = connection.cursor()
        query = "INSERT INTO customers (name, phone, email) VALUES (%s, %s, %s)"
        data = (self.nameEntry.get(), self.phoneEntry.get(), self.emailEntry.get())

        if not all(data):
            done.configure(background="#89CFF0", text='Make sure to provide all data fields')
            done.place(x=200, y=20)
        else:
            query2 = "SELECT * FROM customers WHERE phone = %s"
            cursor.execute(query2, (self.phoneEntry.get(),))
            result = cursor.fetchall()

            if len(result) > 0:
                done.configure(background="#89CFF0", text='This phone number already exists')
                done.place(x=200, y=20)
            else:
                cursor.execute(query, data)
                connection.commit()
                done.configure(background="#89CFF0", text='The customer has been added')
                done.place(x=200, y=20)

        cursor.close()
        connection.close()

    def exit(self):
        self.root.destroy()


# Create the main window
root2 = tk.Tk()
customer_adder = CustomerAdder(root2)

# Start the main loop
root2.mainloop()
