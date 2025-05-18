from tkinter import *
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import pymysql
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from dotenv import load_dotenv

class MedicalPlots(Toplevel):  # Changed from Frame to Toplevel
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        # Window configuration
        self.title("Medical Statistics Dashboard")
        self.state('zoomed')  # Maximize window on Windows
        
        # Try to make it fullscreen on different platforms
        try:
            self.attributes('-fullscreen', True)  # Full screen mode
        except:
            # If fullscreen fails, try to maximize
            self.state('zoomed')  
            
        # Setup close button
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Load environment variables for database connection
        load_dotenv()
        self.MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
        self.MYSQL_USER = os.getenv("MYSQL_USER", "root")
        self.MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "Chicken@id1@@")
        self.MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "medicaldata")
        
        # Get screen dimensions
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        
        # Setup variables
        self.current_plot_index = 0
        
        # Create necessary widgets
        self.create_widgets()
        
        # Fetch data and show first plot
        self.fetch_data()
        self.update_plot()
        
    def on_close(self):
        """Handle window closing"""
        self.destroy()
        
    def create_widgets(self):
        # Create main frame that fills the window
        self.main_frame = Frame(
            self,
            bg="#22266C",
            width=self.screen_width,
            height=self.screen_height
        )
        self.main_frame.pack(fill=BOTH, expand=True)
        
        # Create inner frame for content that takes most of the space
        self.inner_frame = Frame(
            self.main_frame, 
            background="#8CADBE", 
            width=self.screen_width - 40,
            height=self.screen_height - 40
        )
        self.inner_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.inner_frame.pack_propagate(False)
        
        # Create frame for the plot canvas that takes all available space
        self.plot_frame = Frame(
            self.inner_frame,
            bg="white"
        )
        self.plot_frame.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=10)
        
        # Navigation buttons frame at the bottom
        self.nav_frame = Frame(self.inner_frame, bg="#8CADBE", height=50)
        self.nav_frame.pack(side=BOTTOM, fill=X)
        
        # Previous button
        self.prev_button = Button(
            self.nav_frame,
            text="← Previous Plot",
            font=("Inter Bold", 12),
            bg="#310672",
            fg="white",
            activebackground="#4A148C",
            activeforeground="white",
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.previous_plot
        )
        self.prev_button.pack(side=LEFT, padx=20, pady=10)
        
        # Plot indicator
        self.plot_indicator = Label(
            self.nav_frame,
            text="",
            font=("Inter", 12),
            bg="#8CADBE",
            fg="#22266C"
        )
        self.plot_indicator.pack(side=LEFT, expand=True)
        
        # Next button
        self.next_button = Button(
            self.nav_frame,
            text="Next Plot →",
            font=("Inter Bold", 12),
            bg="#310672",
            fg="white",
            activebackground="#4A148C",
            activeforeground="white",
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.next_plot
        )
        self.next_button.pack(side=RIGHT, padx=20, pady=10)
        
        # Exit button
        self.exit_button = Button(
            self.nav_frame,
            text="✕ Close",
            font=("Inter Bold", 12),
            bg="#CC0000",
            fg="white",
            activebackground="#AA0000",
            activeforeground="white",
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.on_close
        )
        self.exit_button.pack(side=RIGHT, padx=20, pady=10)
        
        # Bind keyboard shortcuts
        self.bind("<Left>", lambda event: self.previous_plot())
        self.bind("<Right>", lambda event: self.next_plot())
        self.bind("<Escape>", lambda event: self.on_close())
        
        # Define plots and their titles
        self.plot_list = [
            self.plot_age_distribution,
            self.plot_gender_distribution,
            self.plot_blood_distribution,
            self.plot_diagnosis_by_gender,
            self.plot_appointments_timeline,
            self.plot_symptom_frequency
        ]
        
        self.plot_titles = [
            "Age Distribution of Patients", 
            "Gender Distribution of Patients", 
            "Blood Type Distribution of Patients",
            "Diagnosis Distribution by Gender",
            "Appointment Frequency Timeline",
            "Most Common Patient Symptoms"
        ]
        
    def fetch_data(self):
        """Fetch data from database"""
        try:
            conn = pymysql.connect(
                host=self.MYSQL_HOST,
                user=self.MYSQL_USER,
                password=self.MYSQL_PASSWORD,
                db=self.MYSQL_DATABASE
            )
            
            # Age distribution data
            self.agedata = pd.read_sql_query(
                """
                SELECT 
                    age, 
                    COUNT(*) AS count 
                FROM 
                    patients 
                GROUP BY 
                    age 
                ORDER BY 
                    age
                """, 
                conn
            )
            
            # Gender distribution data
            self.genderdata = pd.read_sql_query(
                """
                SELECT 
                    sexe, 
                    COUNT(*) AS count 
                FROM 
                    patients 
                GROUP BY 
                    sexe 
                ORDER BY 
                    sexe
                """, 
                conn
            )
            
            # Blood type distribution data
            self.blooddata = pd.read_sql_query(
                """
                SELECT 
                    blood_type, 
                    COUNT(*) AS count 
                FROM 
                    patients 
                GROUP BY 
                    blood_type 
                ORDER BY 
                    blood_type
                """, 
                conn
            )
            
            # Diagnosis by gender data
            self.diagnosisgenderdata = pd.read_sql_query(
                """
                SELECT 
                    d.diagnostics AS diagnosis, 
                    p.sexe, 
                    COUNT(*) AS count 
                FROM 
                    treatments d 
                JOIN 
                    patients p ON d.cin_fk = p.cin 
                GROUP BY 
                    d.diagnostics, p.sexe
                """,
                conn
            )
            
            # Appointment timeline data
            self.appointmentdata = pd.read_sql_query(
                """
                SELECT 
                    appointment_date, 
                    COUNT(*) AS count 
                FROM 
                    appointment_date 
                GROUP BY 
                    appointment_date 
                ORDER BY 
                    appointment_date
                """, 
                conn
            )
            
            # Symptom frequency data
            self.symptomdata = pd.read_sql_query(
                """
                SELECT 
                    symptomes AS description
                FROM 
                    treatments
                """, 
                conn
            )
            
            conn.close()
            
            # Process appointment data - convert to datetime
            self.appointmentdata['appointment_date'] = pd.to_datetime(self.appointmentdata['appointment_date'])
            
            # Process symptom data - count frequencies
            self.symptom_counts = self.symptomdata['description'].value_counts().reset_index()
            self.symptom_counts.columns = ['Symptom', 'count']
            
            # Process diagnosis gender data
            if not self.diagnosisgenderdata.empty:
                self.diagnosis_heatmap = self.diagnosisgenderdata.pivot(
                    index="diagnosis", 
                    columns="sexe", 
                    values="count"
                ).fillna(0)
            
        except Exception as e:
            print(f"Database error: {e}")
            # Create dummy data for testing if connection fails
            self.agedata = pd.DataFrame({'age': list(range(20, 70, 10)), 'count': [10, 15, 20, 15, 10]})
            self.genderdata = pd.DataFrame({'sexe': ['M', 'F'], 'count': [40, 30]})
            self.blooddata = pd.DataFrame({
                'blood_type': ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],
                'count': [15, 5, 10, 5, 5, 2, 20, 8]
            })
            # Dummy data for other plots
            self.diagnosisgenderdata = pd.DataFrame({
                'diagnosis': ['Flu', 'Cold', 'Headache'] * 2,
                'sexe': ['M', 'M', 'M', 'F', 'F', 'F'],
                'count': [10, 8, 5, 12, 6, 7]
            })
            self.diagnosis_heatmap = self.diagnosisgenderdata.pivot(index="diagnosis", columns="sexe", values="count").fillna(0)
            
            self.appointmentdata = pd.DataFrame({
                'appointment_date': pd.date_range(start='2023-01-01', periods=10),
                'count': [5, 8, 12, 7, 9, 15, 10, 6, 8, 11]
            })
            
            self.symptom_counts = pd.DataFrame({
                'Symptom': ['Fever', 'Cough', 'Headache', 'Fatigue', 'Sore throat'],
                'count': [15, 12, 10, 8, 6]
            })
    
    def update_plot(self):
        """Update the current plot"""
        # Clear existing plot
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
            
        # Update plot indicator
        self.plot_indicator.config(
            text=f"Plot {self.current_plot_index + 1} of {len(self.plot_list)}: {self.plot_titles[self.current_plot_index]}"
        )
        
        # Create figure with dimensions based on available space
        fig_width = (self.plot_frame.winfo_width() or self.screen_width - 100) / 100
        fig_height = (self.plot_frame.winfo_height() or self.screen_height - 200) / 100
        
        # Create figure - use larger of calculated dimensions or fallback to large size
        fig = plt.figure(figsize=(max(fig_width, 14), max(fig_height, 9)), dpi=100)
        
        # Call the appropriate plot function
        self.plot_list[self.current_plot_index](fig)
        
        # Create canvas for the plot
        canvas = FigureCanvasTkAgg(fig, self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)
    
    def next_plot(self):
        """Go to next plot"""
        self.current_plot_index = (self.current_plot_index + 1) % len(self.plot_list)
        self.update_plot()
    
    def previous_plot(self):
        """Go to previous plot"""
        self.current_plot_index = (self.current_plot_index - 1) % len(self.plot_list)
        self.update_plot()
    
    def plot_age_distribution(self, fig):
        """Plot age distribution"""
        ax = fig.add_subplot(111)
        sns.barplot(data=self.agedata, x='age', y='count', palette='coolwarm', ax=ax)
        ax.set_title("Age Distribution", fontsize=14)
        ax.set_xlabel("Age", fontsize=12)
        ax.set_ylabel("Number of Patients", fontsize=12)
        ax.tick_params(axis='x', rotation=45)
        fig.tight_layout()
    
    def plot_gender_distribution(self, fig):
        """Plot gender distribution"""
        ax = fig.add_subplot(111)
        ax.pie(
            self.genderdata['count'],
            labels=self.genderdata['sexe'],
            autopct='%1.1f%%',
            colors=sns.color_palette('coolwarm', len(self.genderdata)),
            startangle=90,
            explode=[0.05] * len(self.genderdata),
            shadow=True
        )
        ax.set_title('Gender Distribution', fontsize=14)
        ax.axis('equal')
        fig.tight_layout()
    
    def plot_blood_distribution(self, fig):
        """Plot blood type distribution"""
        ax = fig.add_subplot(111)
        ax.pie(
            self.blooddata['count'],
            labels=self.blooddata['blood_type'],
            autopct='%1.1f%%',
            colors=sns.color_palette('coolwarm', len(self.blooddata)),
            startangle=90,
            explode=[0.05] * len(self.blooddata),
            shadow=True
        )
        ax.set_title('Blood Type Distribution', fontsize=14)
        ax.axis('equal')
        fig.tight_layout()
    
    def plot_diagnosis_by_gender(self, fig):
        """Plot diagnosis distribution by gender as heatmap"""
        ax = fig.add_subplot(111)
        try:
            sns.heatmap(
                self.diagnosis_heatmap, 
                annot=True, 
                cmap="coolwarm", 
                fmt=".0f", 
                linewidths=0.5,
                ax=ax
            )
            ax.set_title("Diagnosis by Gender", fontsize=14)
            ax.set_xlabel("Gender", fontsize=12)
            ax.set_ylabel("Diagnosis", fontsize=12)
        except (AttributeError, ValueError) as e:
            ax.text(0.5, 0.5, f"Not enough data for heatmap\n{e}", ha='center', va='center')
        fig.tight_layout()
    
    def plot_appointments_timeline(self, fig):
        """Plot appointments over time"""
        ax = fig.add_subplot(111)
        sns.lineplot(
            data=self.appointmentdata, 
            x="appointment_date", 
            y="count", 
            marker="o", 
            color="blue",
            ax=ax
        )
        ax.set_title("Appointments Over Time", fontsize=14)
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Number of Appointments", fontsize=12)
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
    
    def plot_symptom_frequency(self, fig):
        """Plot symptom frequency"""
        ax = fig.add_subplot(111)
        
        # Limit to top 10 symptoms if there are many
        data = self.symptom_counts.head(10) if len(self.symptom_counts) > 10 else self.symptom_counts
        
        sns.barplot(data=data, x='Symptom', y='count', palette='coolwarm', ax=ax)
        ax.set_title('Most Common Symptoms', fontsize=14)
        ax.set_xlabel('Symptom', fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.tick_params(axis='x', rotation=90)
        fig.tight_layout()