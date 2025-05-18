from tkinter import Tk , Frame
from TrackPatient import TrackPatient


app = Tk()
app.geometry("1000x600")
# app.configure(background="#040626")
app.resizable(height=True , width=True)

""" the purpos of app.minize is when we minimize the app it set at this dimension"""

app.minsize(
    height=600,   
    width=1000
)

# Configure the root window grid
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

outer_controller = Frame(app, bg="#06044a")
outer_controller.grid(row=0, column=0, sticky="nsew")
outer_controller.grid_rowconfigure(0, weight=1)
outer_controller.grid_columnconfigure(0, weight=1)
container = Frame(
    outer_controller,
    bg= "#22266C",
    width=1000,
    height=600
    )
container.grid(row=0 , column=0)
# container.propagate(False) is alais of container.pack_propagate
container.grid_propagate(False)
homePage = TrackPatient(container,  app)
homePage.place(x=0, y=0, width=1000, height=600)
# homePage.tkraise()
app.mainloop()