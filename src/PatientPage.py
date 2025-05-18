from pathlib import Path
from tkinter import Frame, Canvas,Text, Button, Label ,PhotoImage, Tk,StringVar,IntVar,Checkbutton,messagebox 
from tkinter.ttk import Combobox
from tkcalendar import DateEntry 
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from fonctionality.PlaceHolder import PlaceholderEntry
import re
import os
from dotenv import load_dotenv

class PatientPage(Frame):
    def __init__(self, parent , controller):
        super().__init__(parent ,bg="#FFFFFF" ,width=1000, height=600  )
        self.controller = controller
        load_dotenv()
        self.MYSQL_HOST = os.getenv("MYSQL_HOST")
        self.MYSQL_USER = os.getenv("MYSQL_USER")
        self.MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
        self.MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
        
        self.OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = self.OUTPUT_PATH / Path(str(Path.cwd())+"/assets/PatienImages")
        
        # Store all PhotoImage objects
        self.images = {}
    def vars_init(self):
        self.full_name = StringVar()
        self.email = StringVar()
        self.age = StringVar()
        self.diagnosis = StringVar()
        self.cin = StringVar()
        self.phone = StringVar()
        self.description = StringVar()
        self.blood_type_var = StringVar()
        self.var_male = IntVar()
        self.var_female = IntVar()
        self.var_gender = StringVar()
        self.appointment_date_var = StringVar()
        self.error_cin = StringVar()
        self.error_email = StringVar()
    def tkraise(self, aboveThis = None):
        super().tkraise(aboveThis)
        self.vars_init()
        self.create_widgets()
    
    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)
    
    def create_widgets(self):


        # Create canvas
        self.canvas = Canvas(
            self,
            bg="#FFFFFF",
            height=600,
            width=1000,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        
        # Create main rectangle header
        self.canvas.create_rectangle(
            0.0,
            0.0,
            1283.0,
            87.0,
            fill="#22266C",
            outline=""
        )
        
        # Patient Section header text
        self.canvas.create_text(
            400.0,
            25.0,
            anchor="nw",
            text="Patient Section",
            fill="#FFFFFF",
            font=("Inter Bold", 30 * -1)
        )
        
        # Patient Registration Form header
        self.canvas.create_text(
            628.0,
            102.0,
            anchor="nw",
            text="Patient Registration Form",
            fill="#22266C",
            font=("SourceSansPro Bold", 25 * -1)
        )

        
        # Create all entry fields, labels and buttons
        self.create_form_fields()
        
    def create_form_fields(self):

        self.back = Button(
            self.canvas,
            bd=0,
            activebackground="#22266C",
            activeforeground="white",
            bg="#22266C",
            text="← Back",
            fg="white",
            font=("Arial", 12),
            command=lambda: self.controller.show_frame("HomePage")
        )
        self.back.place(x=900 , y=20 )

        self.images["image_2"] = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.canvas.create_image(
            34,34,image=self.images["image_2"]
        )
        # Entry 1 - FullName
        self.images["entry_image_1"] = PhotoImage(file=self.relative_to_assets("entry_1.png"))
        self.canvas.create_image(
            675.0,
            231.5,
            image=self.images["entry_image_1"]
        )
        self.entry_1 = PlaceholderEntry(
            self,
            bd=0,
            placeholder="Enter the full name",
            bg="#EEEEEE",
            textvariable=self.full_name,
            fg="#000716",
            highlightthickness=0
        )
        self.entry_1.place(
            x=610.0,
            y=221.0,
            width=130.0,
            height=19.0
        )

        self.canvas.create_text(
            600.0,
            199.0,
            anchor="nw",
            text="FullName",
            fill="#22266C",
            font=("SourceSansPro Bold", 10 * -1)
        )
        
        # Entry 2 - Email
        self.images["entry_image_2"] = PhotoImage(file=self.relative_to_assets("entry_2.png"))
        entry_bg_2 = self.canvas.create_image(
            675.0,
            298.5,
            image=self.images["entry_image_2"]
        )
        self.entry_2 = PlaceholderEntry(
            self,
            bd=0,
            placeholder="example@gmail.com",
            bg="#EEEEEE",
            fg="#000716",
            textvariable = self.email,
            highlightthickness=0
        )
        self.entry_2.place(
            x=610.0,
            y=288.0,
            width=130.0,
            height=19.0
        )
        self.entry_2.bind("<KeyRelease>" ,  self.on_email_change)

        self.canvas.create_text(
            603.0,
            269.0,
            anchor="nw",
            text="E-mail",
            fill="#22266C",
            font=("SourceSansPro Bold", 10 * -1)
        )
        
        # Entry 3 - Age
        self.images["entry_image_3"] = PhotoImage(file=self.relative_to_assets("entry_3.png"))
        entry_bg_3 = self.canvas.create_image(
            675.0,
            366.5,
            image=self.images["entry_image_3"]
        )
        self.entry_3 = PlaceholderEntry(
            self,
            bd=0,
            placeholder="Enter patient age",
            bg="#EEEEEE",
            fg="#000716",
            textvariable = self.age,
            highlightthickness=0
        )
        self.entry_3.place(
            x=610.0,
            y=356.0,
            width=130.0,
            height=19.0
        )
        
        self.canvas.create_text(
            602.0,
            338.0,
            anchor="nw",
            text="Age",
            fill="#22266C",
            font=("SourceSansPro Bold", 10 * -1)
        )

        # Entry 4 - Disease
        self.images["entry_image_4"] = PhotoImage(file=self.relative_to_assets("entry_4.png"))
        entry_bg_4 = self.canvas.create_image(
            875.0,
            365.5,
            image=self.images["entry_image_4"]
        )
        self.entry_4 = PlaceholderEntry(
            self,
            bd=0,
            placeholder="Enter diagnosis",
            bg="#EEEEEE",
            textvariable = self.diagnosis,
            fg="#000716",
            highlightthickness=0
        )
        self.entry_4.place(
            x=810.0,
            y=355.0,
            width=130.0,
            height=19.0
        )

        self.canvas.create_text(
            800.0,
            338.0,
            anchor="nw",
            text="Diagnosis",
            fill="#22266C",
            font=("SourceSansPro Bold", 10 * -1)
        )
        
        # Entry 5 - CIN
        self.images["entry_image_5"] = PhotoImage(file=self.relative_to_assets("entry_5.png"))
        entry_bg_5 = self.canvas.create_image(
            875.0,
            231.5,
            image=self.images["entry_image_5"]
        )
        self.entry_5 = PlaceholderEntry(
            self,
            bd=0,
            placeholder="Enter CIN number",
            textvariable = self.cin,
            bg="#EEEEEE",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_5.place(
            x=810.0,
            y=221.0,
            width=130.0,
            height=19.0
        )
        self.entry_5.bind("<KeyRelease>" ,  self.on_cin_change)

        self.canvas.create_text(
            800.0,
            205.0,
            anchor="nw",
            text="CIN",
            fill="#22266C",
            font=("SourceSansPro Bold", 10 * -1)
        )

        # Entry 6 - Phone
        self.images["entry_image_6"] = PhotoImage(file=self.relative_to_assets("entry_6.png"))
        entry_bg_6 = self.canvas.create_image(
            875.0,
            298.5,
            image=self.images["entry_image_6"]
        )
        self.entry_6 = PlaceholderEntry(
            self,
            bd=0,
            placeholder="06********",
            bg="#EEEEEE",
            textvariable = self.phone,  
            fg="#000716",
            highlightthickness=0
        )
        self.entry_6.place(
            x=810.0,
            y=288.0,
            width=130.0,
            height=19.0
        )

        self.canvas.create_text(
            800.0,
            269.0,
            anchor="nw",
            text="Phone",
            fill="#22266C",
            font=("SourceSansPro Bold", 10 * -1)
        )
            
        self.add_remaining_widgets()

    def on_email_change(self , event=None):
        email_value = self.email.get()
        # Run validation
        self.validate_email()

    def validate_email(self):
        email_value = self.email.get().strip()
        
        # Check if empty
        if not email_value:
            self.error_email.set("Please enter an email address")
            return False
        
        # Check for placeholder text
        if email_value == "example@gmail.com":
            self.error_email.set("Please enter your email address")
            return False
        
        # Email pattern validation
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email_value):
            if '@' not in email_value:
                self.error_email.set("Email must contain @")
            elif '.' not in email_value:
                self.error_email.set("Email must contain a domain (.com, .org, etc)")
            elif not re.match(r'^[a-zA-Z0-9._%+-]+@', email_value):
                self.error_email.set("Invalid characters before @")
            elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.', email_value):
                self.error_email.set("Invalid domain format")
            else:
                self.error_email.set("Invalid email format")
            return False
        # Valid email
        self.error_email.set("")
        return True

    def on_cin_change(self , event=None):
        cin_value = self.cin.get().upper()
        if cin_value != self.cin.get():
            current_position = self.entry_5.index("insert")
            self.cin.set(cin_value)
            self.entry_5.icursor(current_position)

        # Run validation
        self.validate_cin()

    def validate_cin(self):
        cin_value = self.cin.get().strip().upper()
        
        # Check for placeholder text
        if cin_value == "XX0000" or cin_value == "X0000":
            self.error_cin.set("Please enter a CIN number")
            return False
        
        # Check if empty
        if not cin_value:
            self.error_cin.set("Please enter a CIN number")
            return False
        
        pattern = r'^[A-Z]{1,2}\d{4}$'
        if not re.match(pattern, cin_value):
            if len(cin_value) < 1:
                self.error_cin.set("CIN must start with at least 1 letter")
            elif not cin_value[0].isalpha():
                self.error_cin.set("First character must be a letter")
            elif len(cin_value) > 1 and len(cin_value) < 5:
                self.error_cin.set("CIN must be 1-2 letters followed by 4 digits")
            elif len(cin_value) >= 3 and not cin_value[0:2].isalpha() and not cin_value[0:1].isalpha():
                self.error_cin.set("First 1-2 characters must be letters")
            elif len(cin_value) >= 5 and not cin_value[-4:].isdigit():
                self.error_cin.set("Last 4 characters must be digits")
            else:
                self.error_cin.set("Invalid CIN format (e.g., X7890 or AA0123)")
            return False
        
        # Valid CIN
        self.error_cin.set("")
        return True
    

    def add_remaining_widgets(self):
            # Texte Blood type
        self.canvas.create_text(
            600.0,
            401.0,
            anchor="nw",
            text="Blood type",
            fill="#22266C",
            font=("SourceSansPro Bold", 10 * -1)
        )
        blood_types = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        self.blood_type_var = StringVar()
        
        self.blood_type_combobox = Combobox(
            self,
            values=blood_types,
            textvariable=self.blood_type_var,
            state="readonly",
        )

        self.blood_type_combobox.place(
            x=610.0,
            y=416.0,
            width=60.0,
            height=19.0
        )

        self.blood_type_combobox.current(0) 
        
      
        # Sex section
        self.canvas.create_text(
            800.0,
            406.0,
            anchor="nw",
            text="Sexe",
            fill="#22266C",
            font=("SourceSansPro Bold", 10 * -1)
        )

        self.var_male = IntVar()
        self.var_female = IntVar()
        self.var_gender = StringVar()

        def toggle_sex(gender):
            if gender == "M":
                self.var_female.set(0)
                self.var_gender.set("Male")
            else:
                self.var_male.set(0)
                self.var_gender.set("Female")
         

    # Checkbox for "M"
        self.check_male = Checkbutton(
            self,
            text="M",
            variable=self.var_male,
            command=lambda: toggle_sex("M"),
            bg="#FFFFFF",
            font=("SourceSansPro Bold", 10 * -1)
        )
        self.check_male.place(x=834.0, y=420.0)

        # Checkbox for  "F"
        self.check_female = Checkbutton(
            self,
            text="F",
            variable=self.var_female,
            command=lambda: toggle_sex("F"),
            bg="#FFFFFF",
            font=("SourceSansPro Bold", 10 * -1)
        )
        self.check_female.place(x=916.0, y=420.0)
        
        # Description text area
        self.canvas.create_text(
            603.0,
            459.0,
            anchor="nw",
            text="Description",
            fill="#22266C",
            font=("SourceSansPro Bold", 10 * -1)
        )
        
        self.images["entry_image_9"] = PhotoImage(file=self.relative_to_assets("entry_9.png"))
        self.canvas.create_image(
            675.0,
            510.5,
            image=self.images["entry_image_9"]
        )
        self.entry_9 = Text(
            self,
            bd=0,
            font=("Inter Bold" , 13*-1),
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_9.place(
            x=600.0,
            y=477.0,
            width=150.0,
            height=65.0
        )
        
        # Appointment Date
        self.canvas.create_text(
            806.0,
            465.0,
            anchor="nw",
            text="Appointment Date",
            fill="#22266C",
            font=("SourceSansPro Bold", 15 * -1)
        )
        self.appointment_date_var = StringVar()
        self.appointment_date_entry = DateEntry(
            self,
            textvariable=self.appointment_date_var,
            date_pattern="yyyy-mm-dd",  
            background="darkblue",
            foreground="white",
            borderwidth=2
        )
        self.appointment_date_entry.place(
            x=813.0,
            y=493.0,
            width=130.0,
            height=25.0
        )
                # Submit button
        self.images["button_image_1"] = PhotoImage(file=self.relative_to_assets("button_1.png"))
        
        self.button_1 = Button(
            self,
            image=self.images["button_image_1"],
            borderwidth=0,
            bg="#FFF",
            activebackground="#FFF",
            highlightthickness=0,
            command=self.actionn,
            relief="flat"
        )
        self.button_1.place(
            x=916.0,
            y=562.0,
            width=86.39286041259766,
            height=28.0
        )
        
        # Patient image
        self.images["image_image_1"] = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.canvas.create_image(
            287.0,
            343.0,
            image=self.images["image_image_1"]
        )

        self.input_frame_cin = Frame(
            self.canvas,
            width=200,
            height=20,
            bg="#FFFFFF"

        )
        self.input_frame_cin.place(x=800 ,y= 245)
        # Error message
        self.error_cin_label = Label(
            self.input_frame_cin,
            textvariable=self.error_cin,
            font=("Inter bold", 7),
            fg="#DC2626",
            bg="white",
            anchor="w"
        )
        self.error_cin_label.place(x=0 , y= 0)

        self.input_frame_email = Frame(
            self.canvas,
            width=200,
            height=20,
            bg="#FFF"
        )
        self.input_frame_email.place(x=600 , y = 310)
        self.erro_email_label =  Label(
            self.input_frame_email,
            textvariable=self.error_email,
            font=("Inter bold", 7),
            fg="#DC2626",
            bg="white",
            anchor="w"
        )
        self.erro_email_label.place(x=0 , y=0)
    def actionn(self):
        if not self.validate_cin():
            self.error_cin.set("")
            self.error_email.set("")
            messagebox.showerror
            return
        infos = {
            "fullname": self.entry_1.get(),
            "email": self.entry_2.get(),
            "age": self.entry_3.get(),
            "diagnosis": self.entry_4.get(),
            "cin": self.entry_5.get(),
            "phone": self.entry_6.get(),
            "description": self.entry_9.get("1.0", "end-1c"),
            "gender": self.var_gender.get(),
            "blood_type": self.blood_type_combobox.get(),
            "appointment_date": self.appointment_date_entry.get()
        }

        try:
            # No need to convert the format since we're already using YYYY-MM-DD
            appointment_date = infos["appointment_date"]
            # Just validate it's a valid date
            datetime.strptime(appointment_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Date Error", "Incorrect date format. Please use YYYY-MM-DD.")
            return
        
        try:
            connection = mysql.connector.connect(
                host=self.MYSQL_HOST,
                user=self.MYSQL_USER,
                password=self.MYSQL_PASSWORD,
                database=self.MYSQL_DATABASE
            )

            if connection.is_connected():
                print("connection.is_connected()")
                cursor = connection.cursor()

                query = """
                    INSERT INTO patients (cin, full_name, email, phone, age, blood_type, sexe)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    infos["cin"], infos["fullname"], infos["email"], infos["phone"],
                    infos["age"], infos["blood_type"], infos["gender"]
                )
                cursor.execute(query, values)
        
                query = """
                    INSERT INTO symptomes (cin_fk, description)
                    VALUES (%s, %s)
                """
                values = (
                    infos["cin"],
                    infos["description"]
                )
                cursor.execute(query, values)

                query = """
                    INSERT INTO diagnostics(cin_fk, diagnosis)
                    VALUES (%s, %s)
                """
                values = (
                    infos["cin"],
                    infos["diagnosis"]
                )
                cursor.execute(query, values)

                query = """
                    INSERT INTO appointment_date(cin_fk, appointment_date)
                    VALUES (%s, %s)
                """
                values = (
                    infos["cin"],
                    infos["appointment_date"]
                )
                cursor.execute(query, values)


                connection.commit()
                messagebox.showinfo("Success", "Data saved to database!")

                cursor.close()

        except Error as e:
            messagebox.showerror("Database Error", f"Error: {str(e)}")
        finally:
            if connection:
                if connection.is_connected():
                    connection.close()

