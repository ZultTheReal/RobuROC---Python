from tkinter import *
from tkinter import ttk
import ApplicationFunctions
from ApplicationFunctions import *
from Functions import *
import Functions

app = Tk()
app.geometry('800x480')
app.title("RoboRuc - Gruppe 734")
# Gets the requested values of the height and widht.
windowWidth = app.winfo_reqwidth()
windowHeight = app.winfo_reqheight()

# Gets both half the screen width/height and window width/height
positionRight = int(app.winfo_screenwidth() / 3 - windowWidth / 3)
positionDown = int(app.winfo_screenheight() / 4 - windowHeight / 4)

# Positions the window in the center of the page.
app.geometry("+{}+{}".format(positionRight, positionDown))

######################### Window setup #########################

Header = Frame(app, bg='black')
Header.pack(fill=X)

mainFrame = Frame(app, relief=SUNKEN, borderwidth=1, bg='black')
mainFrame.pack(fill=BOTH, expand=True)

DataContainer = Frame(mainFrame, highlightbackground="white", highlightcolor="white", highlightthickness=2, bg='black')
DataContainer.place(x=10, y=100)

LoggingContainer = Frame(mainFrame, bg='black', highlightbackground="white", highlightcolor="white", highlightthickness=2)
LoggingContainer.place(x=10, y=280)

SpeedContainer = Frame(mainFrame, bg='black')
SpeedContainer.place(x=380, y=320)

Footer = Frame(app, bg='black')
Footer.pack(fill=X)

######################### Header #########################

# Header Titel
headerLabel = ttk.Label(Header, text="RobuRoc - Controlpanel", font=("Arial Bold", 24), foreground="white",
                        background="black")
headerLabel.place(x=400, y=10)
headerLabel.pack()

######################### MainFrame #########################

# Dataoverview Titel
OverviewTitel = ttk.Label(mainFrame, text="General Overview:", font=("Arial Bold", 16), foreground="white",
                          background="black")
OverviewTitel.pack()

# OverviewSpacer = ttk.Label(OverviewTitelFrame, text="", background="black")
# OverviewSpacer.pack()


### Data Row 0 - Motor Labels ###
label_spacer = ttk.Label(DataContainer, text="", background="black")
label_spacer.grid(row=0, column=0, padx=30)
motor1Label = ttk.Label(DataContainer, text="Motor 1", font=("Arial", 14), foreground="white", background="black")
motor1Label.grid(row=0, column=1, padx=5)
motor2Label = ttk.Label(DataContainer, text="Motor 2", font=("Arial", 14), foreground="white", background="black")
motor2Label.grid(row=0, column=2, padx=5)
motor3Label = ttk.Label(DataContainer, text="Motor 3", font=("Arial", 14), foreground="white", background="black")
motor3Label.grid(row=0, column=3, padx=5)
motor4Label = ttk.Label(DataContainer, text="Motor 4", font=("Arial", 14), foreground="white", background="black")
motor4Label.grid(row=0, column=4, padx=5)

### Data Row 1 - Current ###
label_spacer = ttk.Label(DataContainer, text="Current:", font=("Arial", 14), foreground="white", background="black")
label_spacer.grid(row=1, column=0, padx=5)
cur1Label = ttk.Label(DataContainer, text="20 A", font=("Arial", 12), foreground="white", background="black")
cur1Label.grid(row=1, column=1, padx=5)
cur2Label = ttk.Label(DataContainer, text="20 A", font=("Arial", 12), foreground="white", background="black")
cur2Label.grid(row=1, column=2, padx=5)
cur3Label = ttk.Label(DataContainer, text="20 A", font=("Arial", 12), foreground="white", background="black")
cur3Label.grid(row=1, column=3, padx=5)
cur4Label = ttk.Label(DataContainer, text="20 A", font=("Arial", 12), foreground="white", background="black")
cur4Label.grid(row=1, column=4, padx=5)

### Data Row 2 - Velocity ###
label_spacer = ttk.Label(DataContainer, text="Velocity:", font=("Arial", 14), foreground="white", background="black")
label_spacer.grid(row=2, column=0, padx=5)
vel1Label = ttk.Label(DataContainer, text="2 m/s", font=("Arial", 12), foreground="white", background="black")
vel1Label.grid(row=2, column=1, padx=5)
vel2Label = ttk.Label(DataContainer, text="2 m/s", font=("Arial", 12), foreground="white", background="black")
vel2Label.grid(row=2, column=2, padx=5)
vel3Label = ttk.Label(DataContainer, text="2 m/s", font=("Arial", 12), foreground="white", background="black")
vel3Label.grid(row=2, column=3, padx=5)
vel4Label = ttk.Label(DataContainer, text="2 m/s", font=("Arial", 12), foreground="white", background="black")
vel4Label.grid(row=2, column=4, padx=5)

### Data Row 3 - Position ###
label_spacer = ttk.Label(DataContainer, text="Position:", font=("Arial", 14), foreground="white", background="black")
label_spacer.grid(row=3, column=0, padx=5)
pos1Label = ttk.Label(DataContainer, text="???", font=("Arial", 12), foreground="white", background="black")
pos1Label.grid(row=3, column=1, padx=5)
pos2Label = ttk.Label(DataContainer, text="???", font=("Arial", 12), foreground="white", background="black")
pos2Label.grid(row=3, column=2, padx=5)
pos3Label = ttk.Label(DataContainer, text="???", font=("Arial", 12), foreground="white", background="black")
pos3Label.grid(row=3, column=3, padx=5)
pos4Label = ttk.Label(DataContainer, text="???", font=("Arial", 12), foreground="white", background="black")
pos4Label.grid(row=3, column=4, padx=5)


### Data Row 4 - Temperature ###
label_spacer = ttk.Label(DataContainer, text="Temperature:", font=("Arial", 14), foreground="white", background="black")
label_spacer.grid(row=4, column=0, padx=5)
temp1Label = ttk.Label(DataContainer, text="50 deg", font=("Arial", 12), foreground="white", background="black")
temp1Label.grid(row=4, column=1, padx=5)
temp2Label = ttk.Label(DataContainer, text="50 deg", font=("Arial", 12), foreground="white", background="black")
temp2Label.grid(row=4, column=2, padx=5)
temp3Label = ttk.Label(DataContainer, text="50 deg", font=("Arial", 12), foreground="white", background="black")
temp3Label.grid(row=4, column=3, padx=5)
temp4Label = ttk.Label(DataContainer, text="50 deg", font=("Arial", 12), foreground="white", background="black")
temp4Label.grid(row=4, column=4, padx=5)

######################### Adjust Speed #########################

#Motor Selection Label
motorLabel = Label(SpeedContainer,text="Adjust speed", font=("Arial Bold", 16), foreground="white", background="black")
motorLabel.pack(side=LEFT, padx=5)

#Speed Entry
manualSpeed = Entry(SpeedContainer, text="Enter speed", font=('Arial', 12))
manualSpeed.pack(side=LEFT, padx=5, pady=5)

#Send Speed Button
speedButton = Button(SpeedContainer, text='Adjust', width=10, height=1, command=setSpeed)
speedButton.pack(side=LEFT, pady=5)

######################### Logging Container #########################

motorLabel = Label(LoggingContainer,text="Logging Control:", font=("Arial Bold", 16), foreground="white", background="black")
motorLabel.pack(side=TOP, padx=5)

startLogButton = Button(LoggingContainer, text='Start Logging', width=10, height=2, command=startLogging)
startLogButton.pack(side=LEFT, padx=5, pady=5)

StopLogButton = Button(LoggingContainer, text='Stop Logging', width=10, height=2, command=stopLogging)
StopLogButton.pack(side=LEFT, padx=5, pady=5)

######################### Footer #########################

# Close button -- Closes the app
closeButton = Button(Footer, text="Close", width=10, height=2, command=close)
closeButton.pack(side=RIGHT, padx=5, pady=5)

# Disable button -- Set the drives into DisableVoltage state and stop periodic messages
DisableButton = Button(Footer, text="Disable", width=10, height=2, command=disable)
DisableButton.pack(side=RIGHT, padx=5, pady=5)

# Egnite button -- Reset, Enable and start periodic messages
EgnitionButton = Button(Footer, text="Egnition", width=10, height=2, command=egnition)
EgnitionButton.pack(side=RIGHT, padx=5, pady=5)

