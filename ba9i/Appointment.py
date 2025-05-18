from tkinter import *
from pathlib import Path
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import datetime
import pymysql
from PIL import Image, ImageTk

class AppointmentManage(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#E6EEF7", width=1000, height=600)
        
        self.controller = controller
        
        # Set fixed size
        self.pack_propagate(False)
        
        # Set up assets path
        self.ASSETS_PATH = Path(str(Path.cwd()) + "/assets/ModifyAppointmentImages")
        

        # Canvas with fixed size
        self.canvas = Canvas(
            self, 
            bg="#E6EEF7", 
            height=600, 
            width=1000, 
            bd=0, 
            highlightthickness=0, 
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        
        # Create header background
        self.header_bg = self.canvas.create_rectangle(
            0, 0, 1000, 80, 
            fill="#22266C", 
            outline=""
        )
        
        # Create UI elements
        self.create_ui()
        
    def create_ui(self):
        """Create all UI elements"""
        # Header title
        self.title_text = self.canvas.create_text(
            500, 40, 
            text="Patient Appointment", 
            fill="#FFFFFF", 
            font=("Inter Bold", 24)
        )
        
        # Back button
        self.back_button = Button(
            self,
            text="← Back",
            font=("Inter", 12),
            bg="#22266C",
            fg="#FFFFFF",
            activebackground="#2c3187",
            activeforeground="#FFFFFF",
            bd=0,
            cursor="hand2",
            command=lambda: self.controller.show_frame("HomePage")
        )
        self.back_button.place(x=900, y=20, width=80, height=35)
        
        self.logo = Canvas(
            self,
            width=80,
            height=80,
            bg="#FFFFFF"
        )
        self.logo.place(x=0 , y=0)


        # Create left panel (patient info)
        self.left_panel = Frame(self, bg="#FFFFFF", width=300, height=480)
        self.left_panel.place(x=20, y=100)
        
        # Create right panel (appointment details)
        self.right_panel = Frame(self, bg="#FFFFFF", width=660, height=480)
        self.right_panel.place(x=330, y=100)
        
        # Add patient information section
        self.create_patient_info()
        
        # Add appointment details section
        self.create_appointment_details()
        
    def create_patient_info(self):
        """Create patient information section"""
        # Title for patient info
        patient_title = Label(
            self.left_panel,
            text="Patient Information",
            font=("Inter Bold", 16),
            bg="#FFFFFF",
            fg="#22266C"
        )
        patient_title.place(x=20, y=15)
        
        # Separator
        separator = ttk.Separator(self.left_panel, orient='horizontal')
        separator.place(x=20, y=45, width=260)
        
        # Try to load a placeholder profile image
        try:
            profile_img = Image.open(self.relative_to_assets("profile_placeholder.png"))
            profile_img = profile_img.resize((100, 100), Image.LANCZOS)
            self.profile_photo = ImageTk.PhotoImage(profile_img)
            
            profile_label = Label(
                self.left_panel, 
                image=self.profile_photo,
                bg="#FFFFFF"
            )
            profile_label.place(x=100, y=60)
        except:
            # Fallback if image is not available
            profile_frame = Frame(
                self.left_panel, 
                bg="#E6EEF7",
                width=100,
                height=100,
            )
            profile_frame.place(x=100, y=60)
            
            profile_text = Label(
                profile_frame,
                text="Profile",
                font=("Inter", 12),
                bg="#E6EEF7",
                fg="#22266C"
            )
            profile_text.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        # Patient Information Fields
        fields = [
            ("Patient Name:", 170),
            ("CIN:", 210),
            ("Age:", 250),
            ("Gender:", 290),
            ("Blood Type:", 330),
            ("Phone:", 370)
        ]
        
        for text, y_pos in fields:
            label = Label(
                self.left_panel,
                text=text,
                font=("Inter", 12),
                bg="#FFFFFF",
                fg="#22266C",
                anchor="w"
            )
            label.place(x=20, y=y_pos)
            
            # Create matching entry fields on the right side
            field_value = Entry(
                self.left_panel,
                font=("Inter", 12),
                bg="#F5F7FA",
                relief="flat",
                highlightthickness=1,
                highlightbackground="#D0D7E1",
                highlightcolor="#22266C"
            )
            field_value.place(x=120, y=y_pos, width=160, height=28)
    
    def create_appointment_details(self):
        """Create appointment details section"""
        # Title for appointment details
        appt_title = Label(
            self.right_panel,
            text="Appointment Details",
            font=("Inter Bold", 16),
            bg="#FFFFFF",
            fg="#22266C"
        )
        appt_title.place(x=20, y=15)
        
        # Separator
        separator = ttk.Separator(self.right_panel, orient='horizontal')
        separator.place(x=20, y=45, width=620)
        
        # Appointment Date & Time
        date_label = Label(
            self.right_panel,
            text="Date & Time:",
            font=("Inter", 12),
            bg="#FFFFFF",
            fg="#22266C",
            anchor="w"
        )
        date_label.place(x=20, y=60)
        
        # Date picker (requires tkcalendar package)
        try:
            self.date_picker = DateEntry(
                self.right_panel,
                width=12,
                background="#22266C",
                foreground="white",
                borderwidth=0,
                font=("Inter", 12)
            )
            self.date_picker.place(x=120, y=60, width=160, height=28)
        except:
            # Fallback if tkcalendar is not available
            self.date_entry = Entry(
                self.right_panel,
                font=("Inter", 12),
                bg="#F5F7FA",
                relief="flat",
                highlightthickness=1,
                highlightbackground="#D0D7E1",
                highlightcolor="#22266C"
            )
            self.date_entry.place(x=120, y=60, width=160, height=28)
            self.date_entry.insert(0, "MM/DD/YYYY")
        
        # Time picker
        time_label = Label(
            self.right_panel,
            text="Time:",
            font=("Inter", 12),
            bg="#FFFFFF",
            fg="#22266C",
            anchor="w"
        )
        time_label.place(x=300, y=60)
        
        # Time dropdown (hours)
        hour_values = [f"{i:02d}" for i in range(8, 18)]  # 8 AM to 5 PM
        self.hour_var = StringVar()
        self.hour_dropdown = ttk.Combobox(
            self.right_panel,
            textvariable=self.hour_var,
            values=hour_values,
            font=("Inter", 12),
            width=5,
            state="readonly"
        )
        self.hour_dropdown.place(x=350, y=60, width=60, height=28)
        self.hour_dropdown.set("09")
        
        colon_label = Label(
            self.right_panel,
            text=":",
            font=("Inter", 12),
            bg="#FFFFFF",
            fg="#22266C"
        )
        colon_label.place(x=415, y=60)
        
        # Time dropdown (minutes)
        minute_values = ["00", "15", "30", "45"]
        self.minute_var = StringVar()
        self.minute_dropdown = ttk.Combobox(
            self.right_panel,
            textvariable=self.minute_var,
            values=minute_values,
            font=("Inter", 12),
            width=5,
            state="readonly"
        )
        self.minute_dropdown.place(x=430, y=60, width=60, height=28)
        self.minute_dropdown.set("00")
        
        # Reason for visit
        reason_label = Label(
            self.right_panel,
            text="Reason for Visit:",
            font=("Inter", 12),
            bg="#FFFFFF",
            fg="#22266C",
            anchor="w"
        )
        reason_label.place(x=20, y=100)
        
        self.reason_text = Text(
            self.right_panel,
            font=("Inter", 12),
            bg="#F5F7FA",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#D0D7E1",
            highlightcolor="#22266C"
        )
        self.reason_text.place(x=20, y=130, width=620, height=80)
        
        # Medical History
        history_label = Label(
            self.right_panel,
            text="Medical History:",
            font=("Inter", 12),
            bg="#FFFFFF",
            fg="#22266C",
            anchor="w"
        )
        history_label.place(x=20, y=220)
        
        self.history_text = Text(
            self.right_panel,
            font=("Inter", 12),
            bg="#F5F7FA",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#D0D7E1",
            highlightcolor="#22266C"
        )
        self.history_text.place(x=20, y=250, width=620, height=100)
        
        # Doctor's Notes
        notes_label = Label(
            self.right_panel,
            text="Doctor's Notes:",
            font=("Inter", 12),
            bg="#FFFFFF",
            fg="#22266C",
            anchor="w"
        )
        notes_label.place(x=20, y=360)
        
        self.notes_text = Text(
            self.right_panel,
            font=("Inter", 12),
            bg="#F5F7FA",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#D0D7E1",
            highlightcolor="#22266C"
        )
        self.notes_text.place(x=20, y=390, width=450, height=70)
        
        # Save Button
        self.save_button = Button(
            self.right_panel,
            text="Save Appointment",
            font=("Inter Bold", 12),
            bg="#22266C",
            fg="#FFFFFF",
            activebackground="#2c3187",
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            command=self.save_appointment
        )
        self.save_button.place(x=480, y=390, width=160, height=70)
    
    def save_appointment(self):
        """Save appointment to database"""
        try:
            messagebox.showinfo("Success", "Appointment saved successfully!")
            # Here you would implement the actual database saving logic
            # similar to your login page's action method
        except Exception as e:
            messagebox.showerror("Error", f"Could not save appointment: {str(e)}")
    
    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)