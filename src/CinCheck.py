from tkinter import *
from tkinter import  messagebox
from pathlib import Path
import mysql.connector
from mysql.connector import Error
import re
from fonctionality.PlaceHolder import PlaceholderEntry
import os
from dotenv import load_dotenv




class CinCheck(Frame):
    def __init__(self, parent, controller ):
        super().__init__(parent)
        # Load environment variables from .env file
        load_dotenv()
        self.MYSQL_HOST = os.getenv("MYSQL_HOST")
        self.MYSQL_USER = os.getenv("MYSQL_USER")
        self.MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
        self.MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
        self.controller = controller

        self.configure(bg="#22266C")
        # Set paths for assets
        self.OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = self.OUTPUT_PATH / Path(str(Path.cwd())+"/assets/cinCheckImages")

    def init_vars (self):
        # Initialize variables
        self.cin = StringVar()
        self.error = StringVar()
        self.isLoading = False
    
        
    def tkraise(self, aboveThis = None):
        super().tkraise(aboveThis)
        # Create content
        self.init_vars()
        self.create_widget_content()
    
    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)
    
    def create_widget_content(self):
    # Create the main container
        self.center_frame = Frame(
            self, 
            bg="white",
            bd=0,
            highlightthickness=0
        )
        self.center_frame.place(relx=0.5, rely=0.5, anchor=CENTER, width=700, height=600)
        self.canvas = Canvas(
            self,
            width=80,
            height=80,
            bg="#22266C",
            bd=0,
            highlightthickness=0
        )
        self.canvas.place(x= 0 , y= 0 )
        self.icon_image = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.canvas.create_image(
            34 , 34 , image = self.icon_image
        )
        self.icon_label = Label(
                self.center_frame,
                text="🏥",
                font=("Arial", 32),
                fg="#22266C",
                bg="white"
            )
        self.icon_label.pack(pady=(40, 16))
        
        # Title
        self.title_label = Label(
            self.center_frame,
            text="Patient CIN Verification",
            font=("Arial", 28, "bold"),
            fg="#22266C",
            bg="white"
        )
        self.title_label.pack(pady=(0, 16))
        
        # Description
        self.desc_label = Label(
            self.center_frame,
            text="Enter  Moroccan National ID Card number",
            font=("Arial", 16),
            fg="#666",
            bg="white",
            justify=CENTER
        )
        self.desc_label.pack(pady=(0, 24))
        
        # Input container
        self.input_frame = Frame(
            self.center_frame,
            bg="white"
        )
        self.input_frame.pack(fill=X, padx=40, pady=(0, 20))
        
        # CIN Label
        self.cin_label = Label(
            self.input_frame,
            text="Patient CIN Number",
            font=("Arial", 14, "bold"),
            fg="#444",
            bg="white",
            anchor=W
        )
        self.cin_label.pack(fill=X, pady=(0, 8))
        
        # CIN Input field with uppercase conversion
        self.cin_entry = PlaceholderEntry(
            self.input_frame,
            textvariable=self.cin,
            font=("Arial", 16),
            placeholder="XX0000 or X0000",
            bd=2,
            relief=SOLID
        )
        self.cin_entry.pack(fill=X, ipady=10)
        self.cin_entry.bind("<KeyRelease>", self.on_cin_change)
        
        # Error message
        self.error_label = Label(
            self.input_frame,
            textvariable=self.error,
            font=("Arial", 12),
            fg="#DC2626",
            bg="white",
            anchor=W
        )
        self.error_label.pack(fill=X, pady=(8, 0))
        
        # Submit button
        self.submit_button = Button(
            self.center_frame,
            text="Verify Patient",
            font=("Arial", 16, "bold"),
            bg="#22266C",
            fg="white",
            bd=0,
            activebackground="#2D3282",
            activeforeground="white",
            cursor="hand2",
            command=self.handle_submit
        )
        self.submit_button.pack(fill=X, padx=40, ipady=12)
        
        # Format guide
        self.format_frame = Frame(
            self.center_frame,
            bg="#FFFFFF",
            padx=12,
            pady=12
        )
        self.format_frame.pack(fill=X, padx=40, pady=(16, 0))
        
        self.format_title = Label(
            self.format_frame,
            text="Format Guide:",
            font=("Arial", 12, "bold"),
            fg="#22266C",
            bg=self.format_frame["bg"],
            anchor=W
        )
        self.format_title.pack(fill=X)
        
        format_info = [
            "• Two Or One uppercase letters (A-Z)",
            "• Followed by 4 numbers",
            "• Example: XY1234 or X1234"
        ]
        
        for info in format_info:
            format_label = Label(
                self.format_frame,
                text=info,
                font=("Arial", 12),
                fg="#666",
                bg=self.format_frame["bg"],
                anchor=W
            )
            format_label.pack(fill=X, pady=(4, 0))
        
        # Back button
        self.back_button = Button(
            self,
            text="← Back",
            font=("Arial", 12),
            bg="#22266C",
            fg="white",
            bd=0,
            activebackground="#22266C",
            activeforeground="white",
            cursor="hand2",
            command=lambda: self.controller.show_frame("HomePage")
        )
        self.back_button.place(x=900, y=20)
    
    def on_cin_change(self, event=None):
        cin_value = self.cin.get().upper()
        if cin_value != self.cin.get():
            current_position = self.cin_entry.index(INSERT)
            self.cin.set(cin_value)
            self.cin_entry.icursor(current_position)
        
        # Run validation
        self.validate_cin()
    
    def validate_cin(self):
        cin_value = self.cin.get().strip().upper()
        
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
    
    def setCinPatient(self , cin ):
        self.controller.patient_cin.set(cin)

    def handle_submit(self):
        if not self.validate_cin():
            return
        
        # Simulate loading state
        self.isLoading = True
        self.submit_button.config(text="Verifying...", state=DISABLED)
        self.update()
        
        # Get CIN value
        cin_value = self.cin.get().strip().upper()
        print(cin_value)
        """Checking the data base"""
        # For demonstration purposes, we'll simulate an API call with a delay
        self.after(1000, lambda: self.process_verification(cin_value))
    
    def process_verification(self, cin_value):
        # Reset loading state
        self.isLoading = False
        self.submit_button.config(text="Verify Patient", state=NORMAL)
        try :
            """Checking the data base"""
            connection = mysql.connector.connect(
                host=self.MYSQL_HOST,
                user=self.MYSQL_USER,
                password=self.MYSQL_PASSWORD,
                database=self.MYSQL_DATABASE
            )
            cursor = connection.cursor(dictionary=True)
            query_1 = """
            SELECT 
                cin
            From 
                patients
            where 
                cin = %s
            """
            values = [cin_value]
            cursor.execute(query_1 , values)
            results = cursor.fetchall()
            if results:
                messagebox.showinfo("Patient Found", f"Patient with CIN {cin_value} found successfully!")
                self.setCinPatient(cin_value)
            else:
                messagebox.showerror("Patient Error" ,f"Patient with CIN : {cin_value} does'nt exist")
                return
            print("self.controller.page_name_call.get() " +self.controller.page_name_call.get())
            if self.controller.page_name_call.get() != "TrackPatient" and  results:
                query_test = """
                    SELECT 
                        cin_fk 
                    from
                        treatments
                    where 
                        cin_fk = %s 
                    """
                values = [cin_value]
                cursor.execute(query_test , values)
                test_query = cursor.fetchall()
                print("test_query : ",test_query)
                if not test_query:
                    messagebox.showerror("Patien error " ,f" Patient with this CIN  : {cin_value} , does not have any treatment yet " )
                    response = messagebox.askyesno("Navigate into Track Patient Page" , "Would you Give the patient a treatment ? ")
                    if response:
                        self.controller.show_frame("TrackPatient")
                        return
                    else:
                        return
           
            print("self.controller.page from CinCheck : " , self.controller.page_name_call.get())
            self.controller.show_frame(self.controller.page_name_call.get())
        except Error as e :
            messagebox.showerror("DataBases Error " , f"Error : {str(e)}")
            print("SQL ERROR :" , e)
