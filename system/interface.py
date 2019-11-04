import tkinter as tk
from tkinter import ttk
from .shared import *
from datetime import datetime

appTitle = 'RoboRUC Control Panel'
rowTitles = ['Motor','Current [A]','Velocity [m/s]']

class Interface:
    
    # Defining the labels
    motorLabel = [None for x in range(4)]
    curLabel = [None for x in range(4)]
    velLabel = [None for x in range(4)]
    titleLabel = [None for x in range(3)]
    
    log = None
    
    def __init__(self):
        
        self.root = tk.Tk()
        self.setup()
        
        self.addToLog("Interface Ready")
        
    def setup(self):
        
        self.root.geometry('800x400')
        self.root.title(appTitle)
        self.root.configure(background='black')
        
        # Divide the root frame into two columns
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1, minsize=500)
        self.root.grid_columnconfigure(1, weight=1)
        

        
        # --- App frames ---
        
        # Left frame 
        leftFrame = tk.Frame(self.root)
        leftFrame.configure(background='black')
        leftFrame.grid(row=0,column=0, sticky="nsew")
        leftFrame.grid_columnconfigure(0, weight=1)
        
        # Frames within the left frame
        
        headerBox = tk.Frame(leftFrame)
        headerBox.configure(background='black')
        headerBox.pack(side=tk.TOP, pady=30)
        
        dataBox = tk.Frame(leftFrame)
        dataBox.configure(background='black')
        dataBox.pack(pady=50)

        footerBox = tk.Frame(leftFrame)
        footerBox.configure(background='black')
        footerBox.pack(side=tk.BOTTOM, pady=20)
        
        # Right frame
        
        rightFrame = tk.Frame(self.root)
        rightFrame.configure(background='blue')
        rightFrame.grid(row=0,column=1, sticky="nsew")
        rightFrame.grid_columnconfigure(0, weight=1)
        rightFrame.grid_rowconfigure(0, weight=1)
        
        self.log = tk.Text(rightFrame)
        self.log.pack(side=tk.LEFT, fill=tk.Y)
        self.log.grid(row=0, column=0, sticky='nsew')
        
        
        # --- App buttons ---
    
        s = ttk.Style()
        s.configure('lg.TButton', font=('Calibri', 22))
        s.configure('sm.TButton', font=('Calibri', 13))
    
        self.startBtn = ttk.Button(headerBox, command=self.setupCar, text="Ignition", style='lg.TButton')
        self.startBtn.pack(side=tk.LEFT, padx=10)
        
        self.stopBtn = ttk.Button(headerBox, command=self.pauseCar, text="Pause", style='lg.TButton')
        self.stopBtn.pack(side=tk.LEFT, padx=10)
        
        self.gamepadBtn = ttk.Button(footerBox, command=self.toggleGamepad, text="Enable gamepad", style='sm.TButton')
        self.gamepadBtn.pack(side=tk.LEFT, padx=10, ipadx=10)
        
        self.logBtn = ttk.Button(footerBox, command=self.toggleLogging, text="Start logging", style='sm.TButton')
        self.logBtn.pack(side=tk.LEFT, padx=10, ipadx=10)
        
        self.closeBtn = ttk.Button(footerBox, command=self.close, text="Close app", style='sm.TButton')
        self.closeBtn.pack(side=tk.LEFT, padx=10, ipadx=10)
        

        # --- Telemetry table ---
        
        for i in range(4):
            
            dataBox.grid_columnconfigure(i+1, minsize=80)
            
            # Label descripting which motor
            labelText = str(i+1)
            self.motorLabel[i] = ttk.Label(dataBox, text=labelText, font=("Calibri", 18), foreground="white", background="black")
            self.motorLabel[i].grid(row=0, column=i+1, padx=5, sticky='e')
            
            
            
            # Label for current
            self.curLabel[i] = ttk.Label(dataBox, text="0.0", font=("Calibri", 16), foreground="white", background="black")
            self.curLabel[i].grid(row=1, column=i+1, padx=5, sticky='e')
            
            # Label for velocity
            self.velLabel[i] = ttk.Label(dataBox, text="0", font=("Calibri", 16), foreground="white", background="black")
            self.velLabel[i].grid(row=2, column=i+1, padx=5, sticky='e')
        
        # Label titles for table
        for i in range(3):
            self.titleLabel[i] = ttk.Label(dataBox, text=rowTitles[i], font=("Calibri", 18), foreground="white", background="black")
            self.titleLabel[i].grid(row=i, column=0, padx=5, sticky='w')
    
    def addToLog(self, newline):
        time = datetime.now().strftime("%H:%M:%S")
        
        self.log.insert(tk.END, time)
        self.log.insert(tk.END, '\t')
        self.log.insert(tk.END, newline)
        self.log.insert(tk.END, '\n')
    
    def pauseCar(self):
        motors.pause()
    
    def toggleGamepad(self):
        if var.gamepadEnabled:
            self.gamepadBtn['text'] = "Enable gamepad"
            var.gamepadEnabled = False
        else:
            self.gamepadBtn['text'] = "Disable gamepad"
            var.gamepadEnabled = True
            
    def toggleLogging(self):
        if var.loggingEnabled:
            self.logBtn['text'] = "Start logging"
            log.stop()
            var.loggingEnabled = False
            
        else:
            self.logBtn['text'] = "Stop logging"
            log.begin()
            var.loggingEnabled = True
            
    
    def setupCar(self):
        motors.setup()
        
    def stopCar(self):
        pass
    
    def update(self):
        
        for i in range(4):
            self.velLabel[i]['text'] = motors.actualVel[i]
            self.curLabel[i]['text'] = motors.actualCur[i]

        
        self.root.update()
        
    def close(self):
        self.root.destroy()
        
    def setLabelValue( self, row='current', value = 0, index = 0 ):
        
        label = None
        if row is 'current':
            label = self.curLabel
        if row is 'velocity':
            label = self.velLabel
        
        if label:
            # If value is array, update how row 
            if isinstance(value, list):
                for i, val in enumerate(value):
                    label[i]['text'] = str( round( val, 2) )
            else:
                label[index]['text'] = str( round( value, 2) )