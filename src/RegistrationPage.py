from pathlib import Path
from tkinter import Canvas, Button, PhotoImage, StringVar, messagebox, Frame ,Entry , Label
from fonctionality.PlaceHolder import PlaceholderEntry 
import pandas as pd
import mysql.connector
from mysql.connector import Error
from tkinter import messagebox
import os
import re
from dotenv import load_dotenv





class RegistrationPage(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#CBD4F5", width=1000, height=600)
        self.controller = controller
        load_dotenv()
        self.MYSQL_HOST = os.getenv("MYSQL_HOST")
        self.MYSQL_USER = os.getenv("MYSQL_USER")
        self.MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
        self.MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
        # Set fixed size
        self.grid_propagate(False)
        
        # Set up assets path
        self.assets_path = Path(str(Path.cwd()) + '/assets/regestrationImages')
        
        
        # Create and configure canvas - fixed size
        self.canvas = Canvas(
            self,
            bg="#CBD4F5", 
            height=600,
            width=1000,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        
        # Store references to images
        self.entry_images = []
        
    def init_vars(self):
        # Create string variables for form fields
        self.var_full_name = StringVar()
        self.cin = StringVar()
        self.error = StringVar(value="")
        self.var_email = StringVar()
        self.var_password = StringVar()
        self.var_confirm_password = StringVar()
    
    def tkraise(self, aboveThis=None):
        """Override tkraise to reset fields when the page is raised"""
        super().tkraise(aboveThis)
        # print("Befor "+self.error.get())
    
        self.init_vars() 
        print("After : "+self.error.get())
        self.create_widgets()  # Clear login fields every time the page is shown

    def relative_to_assets(self, path: str) -> Path:
        return self.assets_path / Path(path)

    def create_widgets(self):
        # Load images
        self.image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.image_image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.image_image_3 = PhotoImage(file=self.relative_to_assets("image_3.png"))
        self.image_image_4 = PhotoImage(file=self.relative_to_assets("image_4.png"))
        self.image_image_5 = PhotoImage(file=self.relative_to_assets("image_5.png"))
        
        # Place images on canvas
        self.image_1 = self.canvas.create_image(
            34.0, 34.0, image=self.image_image_1
        )
        
        self.image_2 = self.canvas.create_image(
            297.0, 237.0, image=self.image_image_2
        )
        
        self.image_3 = self.canvas.create_image(
            294.0, 215.0, image=self.image_image_3
        )
        
        self.image_4 = self.canvas.create_image(
            312.0, 430.0, image=self.image_image_4
        )
        
        self.image_5 = self.canvas.create_image(
            413.99990113846434, 343.0, image=self.image_image_5
        )
        self.create_entry(self.canvas, "Full Name:", self.var_full_name, 
                         "Enter full name", 628, 64, "entry_2.png")
                         
        self.create_entry(self.canvas, "Email:", self.var_email, 
                         "example@gmail.com", 628, 212, "entry_4.png")
                         
        self.create_entry(self.canvas, "Password:", self.var_password, 
                         "Enter a password", 628, 281, "entry_3.png")
                         
        self.create_entry(self.canvas, "Confirm Password:", self.var_confirm_password, 
                         "Confirm your password", 628, 353, "entry_5.png")


        # Create buttons
        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.register_button = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.registration_check,
            bg="#CBD4F5",
            activebackground="#CBD4F5",
            relief="flat"
        )
        
        # Place register button - FIXED position at x=611
        self.register_button.place(x=611, y=450, width=300, height=45)

        # Create "Already have an account?" text
        self.account_text = self.canvas.create_text(
            648, 539, anchor="nw",
            text="Yes, I have an account?",
            fill="#000000", font=("Inter", 16 * -1)
        )

        # Create login button
        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))
        self.login_button = Button(
            self,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.loginAction,
            bg="#CBD4F5",
            activebackground="#CBD4F5",
            relief="flat"
        )
        
        # Place login button - FIXED position at x=831
        self.login_button.place(x=831, y=539, width=47, height=19)

        self.cin_lable = Label(
            self,
            text="CIN :",
            background="#CBD4F5",
            font=("Inter Bold", 16 * -1),
            foreground="#000000"
        )
        self.cin_lable.place(x=625 , y=130)
        self.entry_1 = PhotoImage(file=self.relative_to_assets("entry_1.png"))
        self.canvas.create_image(
            760,
            173,
            image = self.entry_1
        )
        self.cin_entry = PlaceholderEntry(
            self,
            textvariable=self.cin,
            placeholder="Enter your CIN",
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        self.cin_entry.place(x=628, y=158, width=266, height=32)
        self.cin_entry.bind("<KeyRelease>", self.on_cin_change)
        # Error message
        self.error_label = Label(
            self,
            textvariable=self.error,
            font=("Arial", 10),
            fg="#DC2626",
            bg="#CBD4F5",
            anchor='w'
        )
        self.error_label.place(x=626, y=190)
    def create_entry(self, canvas, label, variable, placeholder, x, y, image_path, show=None):
        canvas.create_text(
            x, y, anchor="nw",
            text=label,
            font=("Inter", 16 * -1),
            fill="#000000"
        )
        
        entry_image = PhotoImage(file=self.relative_to_assets(image_path))
        canvas.create_image(x + 133, y + 41, image=entry_image)
        
        entry = PlaceholderEntry(
            self,
            textvariable=variable,
            placeholder=placeholder,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            show=show
        )
        
        entry.place(x=x, y=y + 25, width=266, height=32)
        self.entry_images.append(entry_image)  # Prevent garbage collection
    def on_cin_change(self, event=None):
        cin_value = self.cin.get().upper()
        if cin_value != self.cin.get():
            current_position = self.cin_entry.index('insert')
            self.cin.set(cin_value)
            self.cin_entry.icursor(current_position)
        
        # Run validation
        self.validate_cin()

    def validate_cin(self):
        cin_value = self.cin.get().strip().upper()
        # Check if empty
        if not cin_value:
            self.error.set("Please enter a CIN number")
            return False
        
        # Check format with regex - CIN starts with 1-2 lowercase letters followed by 4 numbers
        # Check format with regex - CIN starts with 1-2 uppercase letters followed by 4 digits
        pattern = r'^[A-Z]{1,2}\d{4}$'
        if not re.match(pattern, cin_value):
            if len(cin_value) < 1:
                self.error.set("CIN must start with at least 1 letter")
            elif not cin_value[0].isalpha():
                self.error.set("First character must be a letter")
            elif len(cin_value) > 1 and len(cin_value) < 5:
                self.error.set("CIN must be 1-2 letters followed by 4 digits")
            elif len(cin_value) >= 3 and not cin_value[0:2].isalpha() and not cin_value[0:1].isalpha():
                self.error.set("First 1-2 characters must be letters")
            elif len(cin_value) >= 5 and not cin_value[-4:].isdigit():
                self.error.set("Last 4 characters must be digits")
            else:
                self.error.set("Invalid CIN format (e.g., X7890 or AA0123)")
            return False
        # Valid CIN
        self.error.set("")
        return True

    def registration_check(self):
        if not self.validate_cin():
            self.error.set("")
            messagebox.showerror("CIN ERROR" , "Please enter a valid format for CIN")
            return
        registration_info = {
            "Full Name": ["Dr."+self.var_full_name.get().capitalize()],
            "Username": [self.cin.get()],
            "Email": [self.var_email.get()],
            "Password": [self.var_password.get()],
            "Confirm Password": [self.var_confirm_password.get()]
        }

        text = "\n".join([f"{key}: {value}" for key, value in registration_info.items()])
        confirmation = messagebox.askyesnocancel("Confirm Registration", text)
        if confirmation:
           
            df = pd.DataFrame(registration_info)

        if registration_info["Password"] == registration_info["Confirm Password"]:
            print(df)
            self.save_to_mysql(df)
        else:
            messagebox.showerror("Error", "password does not match ")

    # Edited: Moved save_to_mysql method outside registration_check
    def loginAction (self):
        self.error.set("")
        self.controller.show_frame("LoginPage")
    def save_to_mysql(self, df):
        connection = None  # Initialize connection to None
        try:
            # Establish database connection
            connection = mysql.connector.connect(
                host=self.MYSQL_HOST,
                user=self.MYSQL_USER,
                password=self.MYSQL_PASSWORD,
                database=self.MYSQL_DATABASE,
                
            )
                    
            if connection.is_connected():
                cursor = connection.cursor()
                        
                # SQL query to insert data
                fullname = df['Full Name'][0]
                username = df['Username'][0]
                email     = df['Email'][0]
                password = df['Password'][0]
                        
                query = "INSERT INTO doctors(full_name, cin_doctor, email, password) VALUES (%s, %s, %s, %s)"
                values = (fullname, username, email, password)
                cursor.execute(query, values)
                connection.commit()
                messagebox.showinfo("Success", "Login information saved to database!")
                        
                cursor.close()
                self.error.set("")
                self.controller.show_frame("LoginPage")
        except Error as e:
            messagebox.showerror("Database Error", f"Error: {str(e)}")
        finally:
            if connection and connection.is_connected():
                connection.close()
