from tkinter import *
from pathlib import Path
from MedicalPlots import MedicalPlots
class HomePage(Frame):
    def __init__(self, parent, controller ):
        super().__init__(parent, bg="#22266C", width=1000, height=600)
        self.assets_path = Path(str(Path.cwd()) + "/assets/homeImages")
        self.controller = controller
        
    def relative_to_assets(self, path: str) -> Path:
        return self.assets_path / Path(path)
    def tkraise(self, aboveThis=None):
        """Override tkraise to reset fields when the page is raised"""
        super().tkraise(aboveThis)
        self.create_widgets()  # Clear login fields every time the page is shown

    def create_widgets(self):
        # Create and configure canvas - fixed size
        self.canvas = Canvas(
            self,
            bg="#22266C",
            height=600,
            width=1000,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        # Creation another frame inside the homePage frame
        self.inner_frame = Frame(self, background="#8CADBE", width=796, height=474)
        self.inner_frame.grid_propagate(False)

        self.canvas.create_window(
            500,  
            307, 
            window=self.inner_frame,
            width=796,
            height=474
        )
        self.inner_canvas = Canvas(
        self.inner_frame,
        width=796, 
        height=474,
        bd=0,
        bg="#5D7199",
        highlightthickness=0
        )
        self.inner_canvas.pack(fill="both", expand=True)
        
        # Store references to images
        self.entry_images = []
        # Load images 
        self.image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.image_3 = PhotoImage(file=self.relative_to_assets("image_3.png"))
        self.image_4 = PhotoImage(file=self.relative_to_assets("image_4.png"))
        self.image_5 = PhotoImage(file=self.relative_to_assets("image_5.png"))
        self.image_6 = PhotoImage(file=self.relative_to_assets("image_6.png"))
        self.button_1_image = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_2_image = PhotoImage(file=self.relative_to_assets("button_2.png"))
        self.button_3_image = PhotoImage(file=self.relative_to_assets("button_3.png"))
        self.button_4_image = PhotoImage(file=self.relative_to_assets("button_4.png"))
        # self.button_5_image = PhotoImage(file=self.relative_to_assets("button_5.png"))
        # Add images to canvas or other widgets as needed
        # Example: self.canvas.create_image(x, y, image=self.image_1)
        self.canvas.create_image(
            34.0, 
            34.0, 
            image=self.image_1
            )

        self.user_name_lable()

        self.inner_canvas.create_image( 
            160, 
            250,
            image = self.image_2,
            )
        self.inner_canvas.create_image( 
            300, 
            125,
            image = self.image_3,
            )
        self.inner_canvas.create_image(
            65,
            60,
            image = self.image_5
        )
        self.inner_canvas.create_image(
            735,
            410,
            image = self.image_6
        )
        self.inner_canvas.create_text(
            570 ,
            90, 
            text="Your Health is Our\n         Priority ",
            font=("Inter Bold", 30 * -1),
            fill="white" 
        )
        self.inner_canvas.create_text(
            570,
            140,
            text="Caring for You Every Step of the Way",
            font=("Inter Bold" , 20 * -1),
            fill="#FFFFFF"
        )
        self.button_1 = Button(
            self.inner_frame,
            background="#5D7199",
            activebackground="#5D7199",
            command=lambda : self.controller.show_frame("PatientPage"),
            image=self.button_1_image,
            borderwidth=0,
            highlightthickness=0,
        )
        self.button_1.place(x=485, y=200)

        self.button_2 = Button(
            self.inner_frame,
            background="#5D7199",
            activebackground="#5D7199",
            command=lambda:self.controller.show_frame("CinCheck" , "UpdatePatient"),
            image=self.button_2_image, 
            borderwidth=0,
            highlightthickness=0,
        )
        self.button_2.place(x=485, y=260)

        self.button_3 = Button(
            self.inner_frame,
            background="#5D7199",
            activebackground="#5D7199",
            command=lambda:self.controller.show_frame("CinCheck" , "TrackPatient"),
            image=self.button_3_image,
            borderwidth=0,
            highlightthickness=0,
        )
        self.button_3.place(x=485, y=320)

        self.button_4 = Button(
            self.inner_frame,
            background="#5D7199",
            activebackground="#5D7199",
            command=self.open_medical_plots,  # Changed command
            image=self.button_4_image,
            borderwidth=0,
            highlightthickness=0,
        )
        self.button_4.place(x=485, y=380)

        self.button_5 = Button(
            self,
            activebackground="#22266C",
            text="← Back",
            bg="#22266C",
            fg="#FFFFFF",
            activeforeground="#FFFFFF",
            font=("Arial", 12),
            borderwidth=0,
            highlightthickness=0,  
            command=lambda : self.controller.show_frame("LoginPage"),
        )
        self.button_5.place(x=900, y=20)
    def user_name_lable(self):
        self.inner_canvas.create_image(
            200, 
            445,  
            image = self.image_4
        )
        # print("home page :"+self.controller.getFullName()) # debug 
        self.inner_canvas.create_text(
            200,
            435,
            text= self.controller.user_name.get()  ,
            font=("Inter Bold" , 20 * -1),
            fill="#FFFFFF"
        )

    def open_medical_plots(self):
        """Open the Medical Plots window"""
        plots_window = MedicalPlots(self)

