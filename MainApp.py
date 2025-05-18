from tkinter import *
from LoginPage import LoginPage
from RegistrationPage import RegistrationPage
from HomePage import HomePage 
from PatientPage import PatientPage
from UpdatePatient import  UpdatePatient 
from CinCheck import CinCheck
from TrackPatient import TrackPatient
class MainApp(Tk):
    def __init__(self):
        super().__init__()
        self.title("Login & Register")
        self.geometry("1000x600")
        
        self.resizable(True, True)
        self.minsize(1000, 600)

        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

       
        outer_container = Frame(self, bg="#06044a")
        outer_container.grid(row=0, column=0, sticky="nsew")
        
     
        outer_container.grid_rowconfigure(0, weight=1)
        outer_container.grid_columnconfigure(0, weight=1)

        
        self.container = Frame(
            outer_container, 
            bg="#CBD4F5", 
            width=1000, 
            height=600
        )
        self.container.grid(row=0, column=0)
        
        # Prevent container from resizing (keep fixed size)
        self.container.grid_propagate(False)


        self.user_name = StringVar(value=" __user_name__ ")
        self.patient_cin = StringVar(value=" __cin__ " )
        self.page_name_call= StringVar(value="UpdatePatient")
        # Dictionary to hold our frames
        self.frames = {}
        # Create each page frame
        for F in [LoginPage, RegistrationPage , HomePage  ,  PatientPage , UpdatePatient , CinCheck , TrackPatient ]:
            page_name = F.__name__
            print(page_name)
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.place(x=0, y=0, width=1000, height=600)
        # Show the login page initially
        self.show_frame("LoginPage")
        # self.show_frame("CinCheck" , "TrackPatient")
        # self.show_frame("CinCheck" , "UpdatePatient")
    def show_frame(self, page_name , page = None ):
        """Show the specified frame"""
        if page == 'UpdatePatient' or page == "TrackPatient": # changing to track page also vue in home page the change
            self.page_name_call.set(page)
            print("page_name_from_call_CinChick from MainApp : " +self.page_name_call.get() )
            
        frame = self.frames[page_name]
        frame.tkraise()
        print(f"Main Page : {page_name}")


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()