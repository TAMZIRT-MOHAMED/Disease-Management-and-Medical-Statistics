from tkinter import *
from tkinter import messagebox
# from PIL import Image, ImageTk
from pathlib import Path
from tkcalendar import DateEntry
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import os
from dotenv import load_dotenv

class TrackPatient(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#FFFFFF")
        load_dotenv()
        self.MYSQL_HOST = os.getenv("MYSQL_HOST")
        self.MYSQL_USER = os.getenv("MYSQL_USER")
        self.MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
        self.MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
        # Set paths for assets
        self.OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = self.OUTPUT_PATH / Path(str(Path.cwd())+"/assets/trackPatientImages")
        
        # Track treatments
        self.treatment_rows = []
        self.next_treatment_id = 1


    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)
        
    def init_vars(self):
        # Get CIN from the controller if it's set
        cin_value = self.controller.patient_cin.get().strip()
        self.patient_cin_var = StringVar()
        self.patient_name_var = StringVar()
        self.appointment_date_var = StringVar()
        self.blood_type_var = StringVar()
        self.age_var = StringVar()
        self.gender_var = StringVar()
        self.diagnostics_var = StringVar()
        self.symptomes_var = StringVar()
        self.current_date_var = StringVar()
        self.current_date_var.set(datetime.now())
        if cin_value and cin_value != " __cin__ ":
            self.patient_cin_var.set(cin_value)
            # Fetch patient data
            self.fetch_patient_data(cin_value)
    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        self.init_vars()
        self.create_widgets()
    
    def fetch_patient_data(self, cin):
      
        """Fetch patient data from database based on CIN"""
        try:
            conn = mysql.connector.connect(
                host=self.MYSQL_HOST,
                user=self.MYSQL_USER, 
                password=self.MYSQL_PASSWORD, 
                database=self.MYSQL_DATABASE
            )
            
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM patients WHERE cin = %s", (cin,))
            patient = cursor.fetchone()
            
            if patient:
                self.patient_name_var.set(patient['full_name'])
                self.age_var.set(patient['age'])
                self.blood_type_var.set(patient['blood_type'])
                self.gender_var.set(patient['sexe'])
                # Any other patient data you want to fetch
            
            cursor.close()
            conn.close()
            
        except Error as e:
            print(f"Database error: {e}")
    
    def create_widgets(self):
        # Clear any existing widgets
        for widget in self.winfo_children():
            widget.destroy()
            
        # Create header frame
        self.header_frame = Frame(self, bg="#22266C", height=70)
        self.header_frame.pack(fill=X)
        # logo
        self.image_logo = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.canvas = Canvas(
            self.header_frame,
            width=80,
            height=80,
            bg="#22266C",
            bd=0,
            highlightthickness=0
        ) 
        self.canvas.place(x=0 , y= 0 )
        self.canvas.create_image(
            34,
            34,
            image = self.image_logo
        )
        # Back button
        self.back_button = Button(
            self.header_frame,
            text="← Back",
            font=("Arial", 12),
            bg="#22266C",
            fg="white",
            bd=0,
            activebackground="#22266C",
            activeforeground="#CCCCCC",
            cursor="hand2",
            command=lambda: self.controller.show_frame("HomePage")
        )
        self.back_button.place(x=900, y=20)
        
        # Title
        self.title_label = Label(
            self.header_frame,
            text="Patient Treatment Tracking",
            font=("Arial", 20, "bold"),
            bg="#22266C",
            fg="white"
        )
        self.title_label.place(relx=0.5, y=35, anchor="center")
        
        # Main content area with scrolling
        self.main_canvas = Canvas(self, bg="white")
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.main_canvas.yview)
        self.scrollable_frame = Frame(self.main_canvas, bg="white")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(
                scrollregion=self.main_canvas.bbox("all")
            )
        )
        
        self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.main_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Enable scrolling with the mouse wheel
        self.scrollable_frame.bind("<MouseWheel>", lambda e: self.main_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        self.main_canvas.bind("<MouseWheel>", lambda e: self.main_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        # For Linux/Mac - different event name
        self.scrollable_frame.bind("<Button-4>", lambda e: self.main_canvas.yview_scroll(-1, "units"))
        self.scrollable_frame.bind("<Button-5>", lambda e: self.main_canvas.yview_scroll(1, "units"))
        self.main_canvas.bind("<Button-4>", lambda e: self.main_canvas.yview_scroll(-1, "units"))
        self.main_canvas.bind("<Button-5>", lambda e: self.main_canvas.yview_scroll(1, "units"))
        
        self.main_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Patient Information Section
        self.create_patient_info_section()
        
        # Treatments Section
        self.create_treatments_section()

        # diagnostics Section
        self.create_diagnostcis_section ()

        # symptomes Section
        self.create_symptomes_section ()

        # Appointment Section
        self.create_appointment_section()
        
        # Action Buttons
        self.create_action_buttons()
    
    def create_patient_info_section(self):
        # Patient Information Frame
        patient_frame = Frame(
            self.scrollable_frame,
            bg="white",
            bd=1,
            relief=GROOVE,
            padx=20,
            pady=15
        )
        patient_frame.pack(fill=X, padx=30, pady=(30, 15))
        
        # Section Title
        section_title = Label(
            patient_frame,
            text="Patient Information",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#22266C"
        )
        section_title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))
        
        # Patient Fields
        # Name
        name_label = Label(
            patient_frame,
            text="Patient Name :",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#444"
        )
        name_label.grid(row=1, column=0, sticky="w", pady=5)
        
        name_value = Label(
            patient_frame,
            textvariable=self.patient_name_var,
            font=("Arial", 12),
            bg="white",
            fg="#000"
        )
        name_value.grid(row=1, column=1, sticky="w", padx=(20, 0), pady=5)
        
        # CIN
        cin_label = Label(
            patient_frame,
            text="CIN Number   :",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#444"
        )
        cin_label.grid(row=2, column=0, sticky="w", pady=5)
        
        cin_value = Label(
            patient_frame,
            textvariable=self.patient_cin_var,
            font=("Arial", 12),
            bg="white",
            fg="#000"
        )
        cin_value.grid(row=2, column=1, sticky="w", padx=(20, 0), pady=5)
        
        # Age
        age_label = Label(
            patient_frame,
            text="Age                   :",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#444"
        )
        age_label.grid(row=3, column=0, sticky="w", pady=5)
        
        age_value = Label(
            patient_frame,
            textvariable=self.age_var,
            font=("Arial", 12),
            bg="white",
            fg="#000"
        )
        age_value.grid(row=3, column=1, sticky="w", padx=(20, 0), pady=5)
        
        # Blood Type
        blood_type_label = Label(
            patient_frame,
            text="Blood Type    :",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#444"
        )
        blood_type_label.grid(row=4, column=0, sticky="w", pady=5)
        
        blood_type_value = Label(
            patient_frame,
            textvariable=self.blood_type_var,
            font=("Arial", 12),
            bg="white",
            fg="#000"
        )
        blood_type_value.grid(row=4, column=1, sticky="w", padx=(20, 0), pady=5)
        
        # Gender
        gender_label = Label(
            patient_frame,
            text="Gender            :",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#444"
        )
        gender_label.grid(row=5, column=0, sticky="w", pady=5)
        
        gender_value = Label(
            patient_frame,
            textvariable=self.gender_var,
            font=("Arial", 12),
            bg="white",
            fg="#000"
        )
        gender_value.grid(row=5, column=1, sticky="w", padx=(20, 0), pady=5)
        
        # Add a separator line
        separator = Frame(
            patient_frame,
            bg="#CCCCCC",
            height=2,
            bd=0,
            relief=RIDGE
        )
        separator.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(10, 10))
        
        # Add some padding around the frame
        patient_frame.pack_propagate(False)
        patient_frame.config(padx=20, pady=20)
    
    def create_treatments_section(self):
        # Treatments Frame
        self.treatments_frame = Frame(
            self.scrollable_frame,
            bg="white",
            bd=1,
            relief=GROOVE,
            padx=20,
            pady=15
        )
        self.treatments_frame.pack(fill=X, padx=30, pady=15)
        
        # Section Title
        section_title = Label(
            self.treatments_frame,
            text="Treatment Plan",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#22266C"
        )
        section_title.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 15))
        
        # Column Headers
        headers = ["medicine", "Dosage", "Duration", ""]
        for i, header in enumerate(headers):
            header_label = Label(
                self.treatments_frame,
                text=header,
                font=("Arial", 12, "bold"),
                bg="white",
                fg="#555"
            )
            header_label.grid(row=1, column=i, padx=10, pady=(0, 10), sticky="w")
        
        # Add first treatment row
        self.add_treatment_row()
    
    def add_treatment_row(self):
        row_index = len(self.treatment_rows) + 2  # +2 for the header rows
        treatment_id = self.next_treatment_id
        self.next_treatment_id += 1
        
        # Medical Name
        med_name_var = StringVar()
        med_name_entry = Entry(
            self.treatments_frame,
            textvariable=med_name_var,
            font=("Arial", 12),
            width=25,
            bd=1,
            relief=SOLID
        )
        med_name_entry.grid(row=row_index, column=0, padx=10, pady=10, sticky="w")
        
        # Dosage
        dosage_var = StringVar()
        dosage_entry = Entry(
            self.treatments_frame,
            textvariable=dosage_var,
            font=("Arial", 12),
            width=15,
            bd=1,
            relief=SOLID
        )
        dosage_entry.grid(row=row_index, column=1, padx=10, pady=10, sticky="w")
        
        # Duration
        duration_var = StringVar()
        duration_entry = Entry(
            self.treatments_frame,
            textvariable=duration_var,
            font=("Arial", 12),
            width=15,
            bd=1,
            relief=SOLID
        )
        duration_entry.grid(row=row_index, column=2, padx=10, pady=10, sticky="w")
        
        # Remove Button
        remove_btn = Button(
            self.treatments_frame,
            text="✕",
            font=("Arial", 12),
            bg="#f44336",
            fg="white",
            width=2,
            bd=0,
            cursor="hand2",
            command=lambda tid=treatment_id: self.remove_treatment_row(tid)
        )
        remove_btn.grid(row=row_index, column=3, padx=10, pady=10, sticky="w")
        
        # Store row information
        treatment_row = {
            "id": treatment_id,
            "row_index": row_index,
            "med_name_var": med_name_var,
            "dosage_var": dosage_var,
            "duration_var": duration_var,
            "widgets": [med_name_entry, dosage_entry, duration_entry, remove_btn]
        }
        
        self.treatment_rows.append(treatment_row)
    
    def remove_treatment_row(self, treatment_id):
        # Find the treatment row to remove
        row_to_remove = None
        for row in self.treatment_rows:
            if row["id"] == treatment_id:
                row_to_remove = row
                break
        
        if row_to_remove:
            # Remove widgets
            for widget in row_to_remove["widgets"]:
                widget.destroy()
            
            # Remove from list
            self.treatment_rows.remove(row_to_remove)
            
            # Reposition remaining rows
            for row in self.treatment_rows:
                if row["row_index"] > row_to_remove["row_index"]:
                    row["row_index"] -= 1
                    for widget, col in zip(row["widgets"], range(4)):
                        widget.grid(row=row["row_index"], column=col, padx=10, pady=10, sticky="w")
    
    def create_diagnostcis_section(self):
        # Diagnostics Frame
        diagnostics_frame = Frame(
            self.scrollable_frame,
            bg="white",
            bd=1,
            relief=GROOVE,
            padx=20,
            pady=15
        )
        diagnostics_frame.pack(fill=X, padx=30, pady=15)
        
        # Section Title
        section_title = Label(
            diagnostics_frame,
            text="Diagnostics",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#22266C"
        )
        section_title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))
        
        # Diagnostics Text Area
        diagnostics_text = Text(
            diagnostics_frame,
            font=("Arial", 12),
            width=60,
            height=5,
            bd=1,
            relief=SOLID
        )
        diagnostics_text.grid(row=1, column=0, columnspan=2, sticky="w", padx=(20, 0), pady=5)
        
        # Bind the text area to the diagnostics variable
        diagnostics_text.bind("<KeyRelease>", lambda e: self.diagnostics_var.set(diagnostics_text.get("1.0", "end-1c")))

    def create_symptomes_section(self):

        # Symptoms Frame
        symptoms_frame = Frame(
            self.scrollable_frame,
            bg="white",
            bd=1,
            relief=GROOVE,
            padx=20,
            pady=15
        )
        symptoms_frame.pack(fill=X, padx=30, pady=15)
        
        # Section Title
        section_title = Label(
            symptoms_frame,
            text="Symptoms",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#22266C"
        )
        section_title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))
        
        # Symptoms Text Area
        symptoms_text = Text(
            symptoms_frame,
            font=("Arial", 12),
            width=60,
            height=5,
            bd=1,
            relief=SOLID
        )
        symptoms_text.grid(row=1, column=0, columnspan=2, sticky="w", padx=(20, 0), pady=5)
        
        # Bind the text area to the symptoms variable
        symptoms_text.bind("<KeyRelease>", lambda e: self.symptomes_var.set(symptoms_text.get("1.0", "end-1c")))

    def create_appointment_section(self):
        # Appointment Frame
        appointment_frame = Frame(
            self.scrollable_frame,
            bg="white",
            bd=1,
            relief=GROOVE,
            padx=20,
            pady=15
        )
        appointment_frame.pack(fill=X, padx=30, pady=15)
        
        # Section Title
        section_title = Label(
            appointment_frame,
            text="Next Appointment",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#22266C"
        )
        section_title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))
        
        # Date Label
        date_label = Label(
            appointment_frame,
            text="Appointment Date:",
            font=("Arial", 12 , "bold"),
            bg="white",
            fg="#555"
        )
        date_label.grid(row=1, column=0, sticky="w", pady=5)
        
        # Date Entry
        date_entry = DateEntry(
            appointment_frame,
            width=20,
            background="#22266C",
            foreground="white",
            borderwidth=2,
            date_pattern="yyyy-mm-dd",
            textvariable=self.appointment_date_var,
            font=("Inter", 12, "bold")
        )
        date_entry.grid(row=1, column=1, sticky="w", padx=(20, 0), pady=5)

        current_date_label = Label(
            appointment_frame,
            text="Current Date:",
            font=("Arial", 12 , "bold"),
            bg="white",
            fg="#555"
        )
        current_date_label.grid(row=2, column=0, sticky="w", pady=5)

        current_date_value = Label(
            appointment_frame,
            font=("Arial", 12),
            bg="white",
            fg="black",
            textvariable=self.current_date_var
        )
        current_date_value.grid(row=2, column=1, sticky="w", padx=(20, 0), pady=5)

        self.update_clock()

    def update_clock(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.current_date_var.set(now)
        self.after(1000, self.update_clock)
    
    def create_action_buttons(self):
        # Buttons Frame
        buttons_frame = Frame(
            self.scrollable_frame,
            bg="white",
            pady=20
        )
        buttons_frame.pack(fill=X, padx=30, pady=(15, 30))
        
        # Add Treatment Button
        add_treatment_btn = Button(
            buttons_frame,
            text="+ Add Treatment",
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            padx=15,
            pady=8,
            bd=0,
            cursor="hand2",
            command=self.add_treatment_row
        )
        add_treatment_btn.pack(side=LEFT, padx=(0, 15))
        
        # Save Button
        save_btn = Button(
            buttons_frame,
            text="Save Treatment Plan",
            font=("Arial", 12, "bold"),
            bg="#22266C",
            fg="white",
            padx=15,
            pady=8,
            bd=0,
            cursor="hand2",
            command=self.save_treatment_plan
        )
        save_btn.pack(side=RIGHT)
    
    def search_patient(self):
        cin = self.patient_cin_var.get().strip()
        if not cin:
            messagebox.showerror("Error", "Please enter a CIN number")
            return
            
        self.fetch_patient_data(cin)
    
    def save_treatment_plan(self):
        # Validate form
        if not self.validate_form():
            return
            
        # Gather treatment data
        treatments = []
        for row in self.treatment_rows:
            treatment = {
                "medicine": row["med_name_var"].get(),
                "dosage": row["dosage_var"].get(),
                "duration": row["duration_var"].get()
            }
            treatments.append(treatment)
            
        # Create treatment plan object
        treatment_plan = {
            "patient_cin": self.patient_cin_var.get(),
            "patient_name": self.patient_name_var.get(),
            "appointment_date": self.appointment_date_var.get(),
            "treatments": treatments,
            "created_date": datetime.now().strftime("%Y-%m-%d"),
            "diagnostics" :self.diagnostics_var.get().strip(),
            "symptomes"   :self.symptomes_var.get().strip()
        }
        
        # Save to database (you'll need to implement this)
        try:
            self.save_to_database(treatment_plan)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save treatment plan: {str(e)}")
            print("Error is ::--> "+e)
    
    def validate_form(self):
        # Check patient info
        if not self.patient_name_var.get().strip():
            messagebox.showerror("Error", "Patient name is required")
            return False
            
        if not self.patient_cin_var.get().strip():
            messagebox.showerror("Error", "CIN number is required")
            return False
        if not self.diagnostics_var.get().strip():
            messagebox.showerror("Error" ,"Diagnostics is required" )
            return False
        if not self.symptomes_var.get().strip():
            messagebox.showerror("Error" ,"symptomes is required" )
            return False
        # Check treatments
        if not self.treatment_rows:
            messagebox.showerror("Error", "At least one treatment is required")
            return False
            
        for i, row in enumerate(self.treatment_rows):
            if not row["med_name_var"].get().strip():
                messagebox.showerror("Error", f"Medical name is required for treatment {i+1}")
                return False
                
            if not row["dosage_var"].get().strip():
                messagebox.showerror("Error", f"Dosage is required for treatment {i+1}")
                return False
                
            if not row["duration_var"].get().strip():
                messagebox.showerror("Error", f"Duration is required for treatment {i+1}")
                return False
                
        return True
    
    def save_to_database(self, treatment_plan):
        """Save treatment plan to database - implement according to your database schema"""
        try:
            conn = mysql.connector.connect(
                host=self.MYSQL_HOST,
                user=self.MYSQL_USER, 
                password=self.MYSQL_PASSWORD, 
                database=self.MYSQL_DATABASE
            )
            
            cursor = conn.cursor()

            response = messagebox.askyesnocancel("Change Appointment" , f"Do you want to give {self.patient_name_var.get()} an appointment on {self.appointment_date_var.get()}? ")
            print(response)
            
            if response :
                if datetime.strptime(self.appointment_date_var.get(), "%Y-%m-%d") <= datetime.now():
                    raise Exception("Appointment date must be in the future")
                query = """
                INSERT INTO treatments (
                cin_fk , 
                medicine , 
                dosage , 
                duration , 
                visit_day , 
                diagnostics , 
                symptomes
                )
                values (
                %s,   
                %s,   
                %s,   
                %s,   
                %s,   
                %s,   
                %s  
                )
                """
                for i in range(len(treatment_plan['treatments'])):
                    print ("i = ",i)
                    values = (treatment_plan['patient_cin'] , treatment_plan['treatments'][i]['medicine'],  treatment_plan['treatments'][i] ['dosage'], treatment_plan['treatments'][i] ['duration'],  treatment_plan['created_date'] ,treatment_plan['diagnostics'], treatment_plan['symptomes'] )
                    print("Values to be inserted:", values)
                    cursor.execute(query , values)
                    print("treatments table : "+str(cursor.fetchall()))
                query = """
                INSERT INTO appointment_date(
                cin_fk,
                appointment_date
                )
                values(
                %s,
                %s
                )
                """
                values=(treatment_plan['patient_cin'],treatment_plan['appointment_date'])
                cursor.execute(query , values)
                print("appointment day table : "+str(cursor.fetchall()))

                query = """
                INSERT INTO diagnostics(
                cin_fk,
                diagnosis
                )
                values(
                %s,
                %s
                )
                """
                values=(treatment_plan['patient_cin'],treatment_plan['diagnostics'])
                cursor.execute(query , values)
                print("diagnostics table : "+str(cursor.fetchall()))
                query = """
                INSERT INTO symptomes(
                cin_fk,
                description
                )
                values(
                %s,
                %s
                )
                """
                values=(treatment_plan['patient_cin'],treatment_plan['symptomes'])
                cursor.execute(query , values)
                print("symptomes table : "+str(cursor.fetchall()))
                messagebox.showinfo("Success", "Treatment plan saved successfully!")
                self.controller.show_frame("HomePage")
            elif response == False :
                query = """
                INSERT INTO treatments (
                cin_fk , 
                medicine , 
                dosage , 
                duration , 
                visit_day , 
                diagnostics , 
                symptomes
                )
                values (
                %s,   
                %s,   
                %s,   
                %s,   
                %s,   
                %s,   
                %s  
                )
                """
                for i in range(len(treatment_plan['treatments'])):
                    values = (treatment_plan['patient_cin'] , treatment_plan['treatments'][i]['medicine'],  treatment_plan['treatments'][i] ['dosage'], treatment_plan['treatments'][i] ['duration'],  treatment_plan['created_date'] ,treatment_plan['diagnostics'], treatment_plan['symptomes'] )
                    cursor.execute(query , values)
                    print("treatments table : "+str(cursor.fetchall()))
                query = """
                INSERT INTO diagnostics(
                cin_fk,
                diagnosis
                )
                values(
                %s,
                %s
                )
                """
                values=(treatment_plan['patient_cin'],treatment_plan['diagnostics'])
                cursor.execute(query , values)

                query = """
                INSERT INTO symptomes(
                cin_fk,
                description
                )
                values(
                %s,
                %s
                )
                """
                values=(treatment_plan['patient_cin'],treatment_plan['symptomes'])
                cursor.execute(query , values)
                messagebox.showinfo("Success", "Treatment plan saved successfully!"  )
                self.controller.show_frame("HomePage")

            else:
                pass
            conn.commit()
            cursor.close()
            conn.close()
        except Error as e:
            raise Exception(f"Database error: {e}")
