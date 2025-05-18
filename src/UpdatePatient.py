from tkinter import *
from pathlib import Path
from tkcalendar import DateEntry
from tkinter import filedialog , messagebox
import mysql.connector 
import datetime
from mysql.connector import Error
from PIL import Image, ImageTk ,ImageDraw
import os
from dotenv import load_dotenv

class UpdatePatient (Frame):
    def __init__(self , parent , controller):
        super().__init__(parent )
        load_dotenv()
        self.MYSQL_HOST = os.getenv("MYSQL_HOST")
        self.MYSQL_USER = os.getenv("MYSQL_USER")
        self.MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
        self.MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
        
        self.controller = controller
        self.propagate(False)
        self.OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = self.OUTPUT_PATH / Path(str(Path.cwd())+"/assets/updatePatientImages")
        self.current_date_var =  StringVar()
    def tkraise(self, aboveThis = None):
        super().tkraise(aboveThis)
        self.create_widgets()
        self.patient_information()

    def init_vars (self):
        self.cin_var = StringVar()
        self.fullname_var = StringVar()
        self.age_var = StringVar()
        self.email_var = StringVar()
        self.phone_var = StringVar()
        self.bloodtype_var = StringVar()
        self.gender_var = StringVar()
        self.current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.cin_var.set(self.controller.patient_cin.get())
        self.read_from_data_base()
    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)
    def create_widgets(self):
        self.image_icon = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.Header = Frame (
            self,
            width=1000,
            height=70,
            bg="#310672"
        )
        self.Header.place(x=0 , y=0)
        self.icon_canvas = Canvas(
            self.Header,
            bg="#310672",
            width=80,
            height=70,
            bd=0,
            highlightthickness=0
        )
        self.icon_canvas.place(
            x=0,
            y=0
        )
        
        self.icon_canvas.create_image(
            34,34,image=self.image_icon
        )

        self.title = Label(
            self.Header,
            bg="#310672",
            text="Update appointment",
            font=("Inter Bold" , 40*-1),
            fg = "#FFFFFF"
        )
        self.title.place(
            x = 358,
            y=10
        )

        self.body = Frame(
            self,
            width=1000,
            height=530
        )
        self.body.place(
            x=0,
            y=70
        )

        self.Personal_Information = Frame(
            self.body,
            width=418,
            height=530,
            bg="#93b7bf",
            bd=2,
            highlightthickness=2,
            highlightbackground="black"
        )
        self.Personal_Information.place(
            x = 0 ,
            y = 0
        )

        self.doctor_part = Frame(
            self.body,
            width=582,
            height=530,
            bg="#CBD4F5",
            bd=2,
            highlightthickness=2,
            highlightbackground="black"            
        )

        self.doctor_part.place(
            x = 418,
            y = 0
        )

        self.create_user_cercle = Canvas(
            self.body,
            width=150,
            height=150,
            bg="#93b7bf",
            bd=0,
            highlightthickness=0
        )
        self.create_user_cercle.place(x=135 , y= 2)

        self.create_user_cercle.create_oval(
            2,
            2,
            145,
            145,
            fill="gray",
            outline="black",
            
        )
        
        self.user_image = PhotoImage(file=self.relative_to_assets("ProfileUser.png"))
        self.create_user_cercle.create_image(
            74,
            74,
            image=self.user_image
        )

        self.Personal_Information_Container = Frame (
            self.Personal_Information,
            width=390,
            height=308,
            bg="#BBBBBB"
        )
        self.Personal_Information_Container.place(
            x=14,
            y=214
        )

        self.rounded_rect_canvas = Canvas(
            self.Personal_Information,
            width=390,
            height=46,
            bg="#93b7bf",
            highlightthickness=0
        )
        self.rounded_rect_canvas.place(x=14, y=180.5)

        self.rounded_rect_canvas.create_rectangle(
            0, 49, 390, 46,
            fill="#D9D9D9",
            outline=""
        )

        self.rounded_rect_canvas.create_rectangle(
            49, 0, 390-49, 49,
            fill="#D9D9D9",
            outline=""
        )
        
        self.rounded_rect_canvas.create_arc(
            0, 0, 98, 98,
            start=90, 
            extent=90,
            fill="#D9D9D9",
            outline=""
        )

        self.rounded_rect_canvas.create_arc(
            390-98, 0, 390, 98,
            start=0, 
            extent=90,
            fill="#D9D9D9",
            outline=""
        )
        self.rounded_rect_canvas.create_text(
            200,
            20,
            text="Patient Information",
            fill="#150e45",
            font=("Inter Bold" , 20 * -1)
        )

        # Add browse button and functionality for patient image
        self.browse_frame = Frame(
            self.Personal_Information,
            width=170,
            height=110,
            bg="#93b7bf"
        )
        self.browse_frame.place(x=100, y=70)

        self.browse_button = Button(
            self.browse_frame,
            text="Upload Image",
            font=("Inter", 10),
            bg="#93b7bf",
            activebackground="#93b7bf",
            fg="black",
            highlightcolor="black",
            command=self.upload_image,
            cursor="hand2"
        )
        self.browse_button.place(x=60 , y=80)

        self.patient_image = None
        self.patient_image_path = None
        self.patient_image_on_canvas = None

        self.current_appointment = Label(
            self.doctor_part,
            text="Current Appointment Date ",
            fg="Black",
            bg="#CBD4F5",
            font=("Inter Bold" , 20*-1)
        )
        self.current_appointment.place(x = 300 , y= 20)
        self.current_appointment_date = Frame(
            self.doctor_part,
            width=228,
            height=49,
            bg="#CBD4F5",
            bd=2,
            relief=GROOVE
        )
        self.current_appointment_date.place(x = 310 , y= 60)

        self.current_appointment_label = Label(
            self.current_appointment_date,
            text= self.current_date_var.get(),
            bg="gray",
            fg="black",
            font=("Inter Bold", 16 *-1)
        )
        self.current_appointment_label.place(x= 60, y= 10 )
       
        self.Change_appointment = Label(
            self.doctor_part,
            text="Change Appointment Date ",
            fg="Black",
            bg="#CBD4F5",
            font=("Inter Bold" , 20*-1)
        )
        self.Change_appointment.place(x = 20 , y= 20)

        # Create a rectangle frame for the date input
        self.change_appointment_date = Frame(
            self.doctor_part,
            width=300,
            height=50,
            bg="#CBD4F5",
            bd=2,
            relief=GROOVE
        )
        self.change_appointment_date.place(x=30, y=60)

        # Create date input using DateEntry widget
        self.date_cal = DateEntry(
            self.change_appointment_date, 
            width=20, 
            background='#310672',
            foreground='white', 
            borderwidth=2,
            date_pattern='yyyy-mm-dd',
            font=("Inter", 12)
        )
        self.date_cal.pack(padx=10, pady=10)


        

        # Diagnostics Section
        self.diagnostics_label = Label(
            self.doctor_part,
            text="Diagnostics",
            fg="#22266C",
            bg="#CBD4F5",
            font=("Inter Bold", 20*-1)
        )
        self.diagnostics_label.place(x=20, y=130)

        self.diagnostics_frame = Frame(
            self.doctor_part,
            width=540,
            height=70,
            bg="white",
            bd=2,
            relief=GROOVE
        )
        self.diagnostics_frame.place(x=20, y=160)

        # Replace Text widget with styled Label
        self.diagnostics_content = Label(
            self.diagnostics_frame,
            text="",  # Will be set in read_from_data_base
            fg="#333333",
            bg="white",
            font=("Inter", 11),
            wraplength=520,  # Allow text wrapping
            justify=LEFT,
            anchor="nw"
        )
        self.diagnostics_content.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Symptoms Section
        self.symptoms_label = Label(
            self.doctor_part,
            text="Symptoms",
            fg="#22266C",
            bg="#CBD4F5",
            font=("Inter Bold", 20*-1)
        )
        self.symptoms_label.place(x=20, y=220)

        self.symptoms_frame = Frame(
            self.doctor_part,
            width=540,
            height=70,
            bg="white",
            bd=2,
            relief=GROOVE
        )
        self.symptoms_frame.place(x=20, y=250)

        # Replace Text widget with styled Label
        self.symptoms_content = Label(
            self.symptoms_frame,
            text="",  # Will be set in read_from_data_base
            fg="#333333",
            bg="white",
            font=("Inter", 11),
            wraplength=520,  # Allow text wrapping
            justify=LEFT,
            anchor="nw"
        )
        self.symptoms_content.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Treatment Section with scrollable display
        self.treatment_label = Label(
            self.doctor_part,
            text="Treatment",
            fg="#22266C",
            bg="#CBD4F5",
            font=("Inter Bold", 20*-1)
        )
        self.treatment_label.place(x=20, y=310)

        # Fixed-size treatment frame
        self.treatment_frame = Frame(
            self.doctor_part,
            width=540,
            height=120,  # Fixed height
            bg="white",
            bd=2,
            relief=GROOVE
        )
        self.treatment_frame.place(x=20, y=340)
        self.treatment_frame.pack_propagate(False)  # Prevent resizing

        # Create header for the treatment table with enhanced styling
        self.treatment_header_frame = Frame(self.treatment_frame, bg="#310672", height=30)
        self.treatment_header_frame.pack(fill=X, padx=2, pady=2)

        # Create styled column headers
        self.medicine_header = Label(
            self.treatment_header_frame,
            text="MEDICINE",
            fg="white",
            bg="#310672",
            font=("Inter Bold", 11),
            width=18
        )
        self.medicine_header.pack(side=LEFT, padx=2, pady=5)

        self.dosage_header = Label(
            self.treatment_header_frame,
            text="DOSAGE",
            fg="white",
            bg="#310672",
            font=("Inter Bold", 11),
            width=18
        )
        self.dosage_header.pack(side=LEFT, padx=2, pady=5)

        self.duration_header = Label(
            self.treatment_header_frame,
            text="DURATION",
            fg="white",
            bg="#310672",
            font=("Inter Bold", 11),
            width=18
        )
        self.duration_header.pack(side=LEFT, padx=2, pady=5)

        # Create scrollable container for treatment rows
        self.treatment_canvas = Canvas(
            self.treatment_frame,
            bg="white",
            bd=0,
            highlightthickness=0,
            height=83  # Height of the scrollable area
        )
        self.treatment_canvas.pack(side=LEFT, fill=BOTH, expand=True, padx=2)

        # Add scrollbar
        self.treatment_scrollbar = Scrollbar(
            self.treatment_frame,
            orient=VERTICAL,
            command=self.treatment_canvas.yview
        )
        self.treatment_scrollbar.pack(side=RIGHT, fill=Y)
        self.treatment_canvas.configure(yscrollcommand=self.treatment_scrollbar.set)

        # Create a frame inside the canvas to hold the rows
        self.treatment_rows_frame = Frame(self.treatment_canvas, bg="white")
        self.treatment_canvas.create_window((0, 0), window=self.treatment_rows_frame, anchor=NW)

        # Configure the scrolling region when rows are added
        def configure_scroll_region(event):
            self.treatment_canvas.configure(scrollregion=self.treatment_canvas.bbox("all"))

        self.treatment_rows_frame.bind("<Configure>", configure_scroll_region)

        # Add mouse wheel scrolling functionality
        def _on_mousewheel(event):
            # Windows and macOS (event.delta)
            if event.delta:
                self.treatment_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            # Linux (event.num)
            elif event.num == 4:
                self.treatment_canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.treatment_canvas.yview_scroll(1, "units")

        # Bind mouse wheel events
        self.treatment_canvas.bind_all("<MouseWheel>", _on_mousewheel)  # Windows and macOS
        self.treatment_canvas.bind_all("<Button-4>", _on_mousewheel)    # Linux scroll up
        self.treatment_canvas.bind_all("<Button-5>", _on_mousewheel)    # Linux scroll down

        # Bind enter/leave events to activate/deactivate scrolling only when mouse is over the canvas
        def _bind_mousewheel(event):
            self.treatment_canvas.bind_all("<MouseWheel>", _on_mousewheel)
            self.treatment_canvas.bind_all("<Button-4>", _on_mousewheel)
            self.treatment_canvas.bind_all("<Button-5>", _on_mousewheel)

        def _unbind_mousewheel(event):
            self.treatment_canvas.unbind_all("<MouseWheel>")
            self.treatment_canvas.unbind_all("<Button-4>")
            self.treatment_canvas.unbind_all("<Button-5>")

        # Make scrolling active only when mouse is over the treatment canvas
        self.treatment_canvas.bind("<Enter>", _bind_mousewheel)
        self.treatment_canvas.bind("<Leave>", _unbind_mousewheel)

        # Save Button
        self.save_button = Button(
            self.doctor_part,
            text="Save",
            font=("Inter Bold", 14),
            bg="#310672",
            fg="white",
            activebackground="#310672",
            relief=RAISED,
            bd=1,
            width=10,
            height=1,
            cursor="hand2",
            command=self.action
        )
        self.save_button.place(x=450, y=470) 
        self.back_button = Button(
            self.Header,
            text="← Back",
            font=("Arial", 12),
            bd=0,
            highlightthickness=0,
            fg="#FFFFFF",
            bg="#310672",
            activeforeground="#FFFFFF",
            activebackground="#310672",
            cursor="hand2",
            command=lambda:self.controller.show_frame("HomePage")
        )
        self.back_button.place(x=900 , y=20)


    def patient_information (self):
        # Initialize variables first
        self.init_vars()
        
        self.cin = Label(
            self.Personal_Information_Container,
            text="CIN : " + self.cin_var.get(),
            fg="black",
            bg="#BBBBBB",
            font=("Inter Bold", 16*-1)
        )
        self.cin.place(x=10, y=20)
        
        self.full_name = Label(
            self.Personal_Information_Container,
            text="Full Name : " + self.fullname_var.get(),
            fg="black",
            bg="#BBBBBB",
            font=("Inter Bold", 16*-1)
        )
        self.full_name.place(x=10, y=60)

        self.Age = Label(
            self.Personal_Information_Container,
            text="Age : " + self.age_var.get(),
            fg="black",
            bg="#BBBBBB",
            font=("Inter Bold", 16*-1)
        )
        self.Age.place(x=10, y=100)

        self.email = Label(
            self.Personal_Information_Container,
            text="Email : " + self.email_var.get(),
            fg="black",
            bg="#BBBBBB",
            font=("Inter Bold", 16*-1)
        )
        self.email.place(x=10, y=140)

        self.Phone = Label(
            self.Personal_Information_Container,
            text="Phone Number : " + self.phone_var.get(),
            fg="black",
            bg="#BBBBBB",
            font=("Inter Bold", 16*-1)
        )
        self.Phone.place(x=10, y=180)

        self.BlodType = Label(
            self.Personal_Information_Container,
            text="Blood Type : " + self.bloodtype_var.get(),
            fg="black",
            bg="#BBBBBB",
            font=("Inter Bold", 16*-1)
        )
        self.BlodType.place(x=10, y=220)

        self.Gender = Label(
            self.Personal_Information_Container,
            text="Gender : " + self.gender_var.get(),
            fg="black",
            bg="#BBBBBB",
            font=("Inter Bold", 16*-1)
        )
        self.Gender.place(x=10, y=260)
    def upload_image(self):
        # Open file dialog to select an image
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        
        if file_path:
            self.patient_image_path = file_path
            print(self.patient_image_path)
            # Open the image
            img = Image.open(file_path)
            
            # Create a square crop of the image (to avoid distortion)
            width, height = img.size
            size = min(width, height)
            left = (width - size) // 2
            top = (height - size) // 2
            right = left + size
            bottom = top + size
            img = img.crop((left, top, right, bottom))
            
            # Resize to fit the oval (exactly 149x149)
            img = img.resize((149, 149), Image.LANCZOS)
            
            # Create a circular mask
            mask = Image.new('L', (149, 149), 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse((0, 0, 149, 149), fill=255)
            
            # Apply the mask to create circular image
            result = Image.new('RGBA', (149, 149), (0, 0, 0, 0))
            result.paste(img, (0, 0), mask)
            
            # Convert to PhotoImage
            self.patient_image = ImageTk.PhotoImage(result)
            
            # Clear previous image
            if hasattr(self, 'patient_image_on_canvas') and self.patient_image_on_canvas:
                self.create_user_cercle.delete(self.patient_image_on_canvas)
            
            # Display new image in the oval - centered perfectly
            self.patient_image_on_canvas = self.create_user_cercle.create_image(
                75, 75, 
                image=self.patient_image
            )
    def action (self):
        current_appoitment = self.current_date_var.get()
        print("current appoitment : "+current_appoitment)
        changing_date = self.date_cal.get_date()
        print(type(changing_date))
        print("changing_date : "+str(changing_date))
        print("current time  :" +str(datetime.datetime.strptime(self.current_date, "%Y-%m-%d").date()))

        try:
            conn = mysql.connector.connect(
                host=self.MYSQL_HOST,
                user=self.MYSQL_USER,
                password=self.MYSQL_PASSWORD,
                database=self.MYSQL_DATABASE
            )
            if conn.is_connected():
                if changing_date > datetime.datetime.strptime(self.current_date, "%Y-%m-%d").date():
                    cursor = conn.cursor()
                    query = """
                    UPDATE 
                        appointment_date
                    SET 
                        appointment_date = %s
                    WHERE 
                        cin_fk = %s 
                    """
                    values = (changing_date.strftime("%Y-%m-%d"), self.cin_var.get())
                    cursor.execute(query, values)
                    conn.commit()
                    messagebox.showinfo("Date input" ,"Appointment date updated successfully." )
                    self.controller.show_frame("HomePage")
                    print("Appointment date updated successfully.")
                else:
                    messagebox.showwarning("Date input" , "New appointment date must be in the future.")
                    print("New appointment date must be in the future.")
                conn.close()
        except Error as e :
            print("Error from action page Update Patien " , e)



    def read_from_data_base  (self):

        try:
            connection = mysql.connector.connect(
                host=self.MYSQL_HOST,
                user=self.MYSQL_USER,
                password=self.MYSQL_PASSWORD,
                database=self.MYSQL_DATABASE
                )
            if connection.is_connected():
                cursor = connection.cursor(dictionary=True) 
                query = """
                SELECT 
                    MAX(appointment_date) AS last_appointment
                FROM appointment_date
                    WHERE cin_fk = %s
                """
                values = [self.cin_var.get()]
                print("self.cin_var.get()"+ self.cin_var.get())
                cursor.execute(query , values)
                print("here 2")
                result_1 = cursor.fetchall() # current appointment date if exist
                print("result of quey 1 ",result_1)

                query_2 = """
                SELECT 
                symptomes , diagnostics , visit_day
                FROM treatments
                group by cin_fk , symptomes , diagnostics , visit_day
                having cin_fk = %s
                """
                values = [self.cin_var.get()]
                print(values)
                cursor.execute(query_2 ,  values)
                result_2 = cursor.fetchall()
                print(result_2)
                # print("result of query2 ", result_2 ) # fech symptomes , diagnostics and visit_day
                # print("result_2[0]['visit_day'] :",result_2[0]['visit_day'])
                query_3 = """
                SELECT 
                    medicine , dosage , duration
                FROM
                    treatments
                where 
                    visit_day = %s and cin_fk = %s
                """
                # print( "type :  : ", type(result_2[0]['visit_day']))
                values = (result_2[0]['visit_day'] , self.cin_var.get())
                cursor.execute(query_3 , values)
                result_3 = cursor.fetchall()
                print("result of query 3 ", result_3 )


                #last version
                query_4 ="""
                SELECT  
                    full_name, 
                    email, 
                    phone, 
                    age, 
                    blood_type, 
                    sexe  
                FROM  
                    patients 
                WHERE 
                    cin = %s 
                """

                values = [self.cin_var.get()]
                cursor.execute(query_4 , values)
                result = cursor.fetchall() 
                print("result : ", result)
                
                if result:

                    self.fullname_var.set(result[0]['full_name'])
                    self.email_var.set(result[0]['email'])
                    self.phone_var.set(result[0]['phone'])
                    self.age_var.set(str(result[0]['age']))
                    self.bloodtype_var.set(result[0]['blood_type'])
                    self.gender_var.set(result[0]['sexe'])

                    self.current_date_var.set(str(result_1[0]['last_appointment']))
                    self.current_appointment_label.config(text=self.current_date_var.get())

                    # Set diagnostics content
                    self.diagnostics_content.config(text=result_2[0]['diagnostics'])

                    # Set symptoms content
                    self.symptoms_content.config(text=result_2[0]['symptomes'])

                    # Clear existing treatment rows
                    for widget in self.treatment_rows_frame.winfo_children():
                        widget.destroy()

                    # Add treatment rows with enhanced styling
                    for i, treatment in enumerate(result_3):
                        row_frame = Frame(
                            self.treatment_rows_frame,
                            bg="#F0F0F0" if i % 2 == 0 else "white",  # Alternating row colors
                            width=520,  # Match width of parent
                            height=25   # Fixed row height
                        )
                        row_frame.pack(fill=X, pady=1)
                        row_frame.pack_propagate(False)  # Keep fixed size
                        
                        # Medicine column with hover effect
                        medicine_label = Label(
                            row_frame,
                            text="        "+treatment['medicine'],
                            bg=row_frame["bg"],
                            font=("Inter", 10),
                            width=18,
                            anchor="w",
                            padx=5
                        )
                        medicine_label.pack(side=LEFT, padx=2)
                        
                        # Add hover effect
                        def on_enter(e, widget=medicine_label):
                            widget.config(fg="#310672", font=("Inter Bold", 10))
                        def on_leave(e, widget=medicine_label, bg=row_frame["bg"]):
                            widget.config(fg="black", font=("Inter", 10))
                            
                        medicine_label.bind("<Enter>", on_enter)
                        medicine_label.bind("<Leave>", on_leave)
                        
                        # Dosage column
                        dosage_label = Label(
                            row_frame,
                            text="              "+treatment['dosage'],
                            bg=row_frame["bg"],
                            font=("Inter", 10),
                            width=18,
                            anchor="w",
                            padx=5
                        )
                        dosage_label.pack(side=LEFT, padx=2)
                        
                        # Duration column
                        duration_label = Label(
                            row_frame,
                            text= "              "+treatment['duration'],
                            bg=row_frame["bg"],
                            font=("Inter", 10),
                            width=18,
                            anchor="w",
                            padx=5
                        )
                        duration_label.pack(side=LEFT, padx=2)

                    # Update the scrollregion after adding all rows
                    self.treatment_canvas.update_idletasks()
                    self.treatment_canvas.configure(scrollregion=self.treatment_canvas.bbox("all"))

                cursor.close()
                connection.close()
            
        except Error as e :
            print(f"Error : {str(e)}")
