from tkinter import *
from fonctionality.PlaceHolder import PlaceholderEntry
from pathlib import Path
import mysql.connector
from mysql.connector import Error
from tkinter import messagebox
import os
import re
from dotenv import load_dotenv
class LoginPage(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#CBD4F5", width=1000, height=600)
        load_dotenv()
        self.MYSQL_HOST = os.getenv("MYSQL_HOST")
        self.MYSQL_USER = os.getenv("MYSQL_USER")
        self.MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
        self.MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
        self.controller = controller
        self.configure(bg="#CBD4F5")
        
        # Set fixed size
        self.pack_propagate(False)
        
        # Set up assets path
        self.ASSETS_PATH = Path(str(Path.cwd()) + "/assets/loginImages")
        self.relative_to_assets = lambda path: self.ASSETS_PATH / Path(path)

        # Canvas with fixed size
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
    
    def  init_vars(self):
        # Store variables
        self.var1 = StringVar()
        self.var2 = StringVar()
        self.error = StringVar(value="")

    def tkraise(self, aboveThis=None):
        """Override tkraise to reset fields when the page is raised"""
        super().tkraise(aboveThis)
        self.init_vars()
        self.create_ui()  # Clear login fields every time the page is shown

    def create_ui(self):
        """Create all UI elements"""
        # Blue rectangle background
        self.blue_rect = self.canvas.create_rectangle(
            656.0, 0.0, 1000.0, 600.0, 
            fill="#22256C", outline=""
        )
        
        # Create text elements
        self.account_text = self.canvas.create_text(
            250.0, 491.0, anchor="nw", 
            text="Don't have an account?", 
            fill="#000000", font=("Inter", 16 * -1)
        )
        
        self.username_label = self.canvas.create_text(
            72.0, 163.0, anchor="nw", 
            text="Doctor's ID:", 
            fill="#000000", font=("Inter", 16 * -1)
        )
        
        self.welcome_label = self.canvas.create_text(
            220.0, 69.0, anchor="nw", 
            text="Welcome Back!", 
            fill="#191919", font=("Inter Bold", 16 * -1)
        )
        
        self.password_label = self.canvas.create_text(
            72.0, 264.0, anchor="nw", 
            text="Password:", 
            fill="#000000", font=("Inter", 16 * -1)
        )
        
        # Load images
        self.image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.image_3 = PhotoImage(file=self.relative_to_assets("image_3.png"))
        self.image_4 = PhotoImage(file=self.relative_to_assets("image_4.png"))
        self.entry_bg_1 = PhotoImage(file=self.relative_to_assets("entry_1.png"))
        self.entry_bg_2 = PhotoImage(file=self.relative_to_assets("entry_2.png"))
        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))
        self.eye_open = PhotoImage(file=self.relative_to_assets("eye_open.png"))
        self.eye_closed = PhotoImage(file=self.relative_to_assets("eye_closed.png"))

        
        # Place images on canvas
        self.image1_obj = self.canvas.create_image(828.0, 416.0, image=self.image_1)
        self.image2_obj = self.canvas.create_image(34.0, 34.0, image=self.image_2)
        self.image3_obj = self.canvas.create_image(85.0, 536.0, image=self.image_3)
        self.image4_obj = self.canvas.create_image(91.0, 556.0, image=self.image_4)
        
        # Create entry backgrounds
        self.entry_bg2_obj = self.canvas.create_image(276.5, 210.5, image=self.entry_bg_2)
        self.entry_bg1_obj = self.canvas.create_image(275.5, 313.5, image=self.entry_bg_1)
        # Error message
        self.error_label = Label(
            self,
            textvariable=self.error,
            font=("Arial", 12),
            fg="#DC2626",
            bg="#CBD4F5",
            anchor=W
        )
        self.error_label.place(x=115.5, y=240.0, width=322.0)
        # Create entry widgets
        self.entry_2 = PlaceholderEntry(
            self, bd=0, bg="#FFFFFF", fg="#000716", 
            font=("Inter Bold", 16 * -1),
            placeholder="enter your CIN", 
            highlightthickness=0, 
            textvariable=self.var1
        )
        self.entry_2.place(x=115.5, y=190.0, width=322.0, height=43.0)
        # self.entry_2.pack(fill=X, ipady=10)
        self.entry_2.bind("<KeyRelease>", self.on_cin_change)
        self.entry_1 = PlaceholderEntry(
            self, 
            bd=0, 
            bg="#FFFFFF", 
            fg="#000716", 
            font=("Inter Bold", 16 * -1), 
            highlightthickness=0, 
            textvariable=self.var2, 
            show="*",
            placeholder="enter your password"
        )
        self.entry_1.place(x=114.5, y=293.0, width=322.0, height=43.0)
        
        # Add eye button for password visibility
        self.is_password_visible = False
        self.eye_button = Button(
            self,
            image=self.eye_closed,
            bd=0,
            bg="#FFFFFF",
            activebackground="#FFFFFF",
            highlightthickness=0,
            command=self.toggle_password_visibility,
            relief="flat",
            cursor="hand2"  # Show hand cursor when hovering
        )
        self.eye_button.place(x=397, y=300, width=25, height=25)

        # Create buttons
        self.login_button = Button(
            self, 
            image=self.button_image_1, 
            borderwidth=0, 
            bg="#CBD4F5", 
            activebackground="#CBD4F5", 
            highlightthickness=0, 
            command=self.action, 
            relief="flat"
        )
        self.login_button.place(x=92.0, y=395.0, width=367.0, height=50.0)

        self.register_button = Button(
            self, 
            image=self.button_image_2, 
            borderwidth=0, 
            bg="#CBD4F5", 
            activebackground="#CBD4F5", 
            highlightthickness=0, 
            command=lambda: self.controller.show_frame("RegistrationPage"), 
            relief="flat"
        )
        self.register_button.place(x=450.0, y=491.0, width=64.0, height=19.0)

    def setFullName (self , name ):
        self.controller.user_name.set(name)

    def toggle_password_visibility(self):
        """Toggle password field visibility between shown and hidden"""
        if self.is_password_visible:
            # Change to hidden password
            self.entry_1.config(show="*")
            self.eye_button.config(image=self.eye_closed)
            self.is_password_visible = False
        else:
            # Change to visible password
            self.entry_1.config(show="")
            self.eye_button.config(image=self.eye_open)
            self.is_password_visible = True
    def on_cin_change(self, event=None):
        cin_value = self.var1.get().upper()
        if cin_value != self.var1.get():
            current_position = self.entry_2.index(INSERT)
            self.var1.set(cin_value)
            self.entry_2.icursor(current_position)
        
        # Run validation
        self.validate_cin()
    def validate_cin(self):
        cin_value = self.var1.get().strip().upper()
        
        # Check for placeholder text
        if cin_value == "XX000000":
            self.error.set("Please enter a CIN number")
            return False
        
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
    

    def action(self):
            
            if not self.validate_cin():
                self.error.set("")
                messagebox.showerror("CIN ERROR" , "Please enter a valid format for CIN")
                return

            login = {
                "username": self.entry_2.get(),
                "password": self.entry_1.get()
            }
            
            try:
                conn = mysql.connector.connect(
                    user=self.MYSQL_USER, 
                    host=self.MYSQL_HOST, 
                    password=self.MYSQL_PASSWORD, 
                    database=self.MYSQL_DATABASE
                )
                
                cursor = conn.cursor(dictionary=True)
                cursor.execute('SELECT cin_doctor, password, full_name FROM doctors')
                results = cursor.fetchall()
                for row in results:
                    if row['cin_doctor'] == login['username'] and row['password'] == login['password']:
                        print("User exists")  # der chi haraka hna
                        self.setFullName(row['full_name'])
                        # Update any global variables before showing the page
                        cursor.close()
                        conn.close()
                        self.controller.show_frame("HomePage")
                        return
                
                cursor.close()
                conn.close()
                
            except Error as e:
                messagebox.showerror("Database Error", f"Connection failed: {e}")
                return
                
            msg_error = messagebox.askquestion("Login Failed", "User does not exist. Would you like to register?")
            
            if msg_error == "yes":
                self.controller.show_frame("RegistrationPage")
                