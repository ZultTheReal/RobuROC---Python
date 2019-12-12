import tkinter as tk
from tkinter import ttk
from .shared import *
from datetime import datetime
import time
import utm

# For plotting
#import matplotlib
#matplotlib.use("TkAgg")
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#from matplotlib.figure import Figure
#import matplotlib.animation as animation
#from matplotlib import style

#style.use('ggplot')


appTitle = 'RoboRUC Control Panel'
rowTitles = ['Motor','Current [A]','Velocity [m/s]']

dataTitles = ['gZ', 'GPS speed', 'GPS count']
motorTitle = ['Left', 'Right']

class Interface:
    

    # Defining the labels
    motorLabel = [None for x in range(2)]
    curLabel = [None for x in range(4)]
    velLabel = [None for x in range(2)]
    titleLabel = [None for x in range(3)]
    
    gpsTitleLabel = [None for x in range(5)]
    gpsDataLabel = [None for x in range(5)]
    
    
    # Pointer to data sources for gui
    gpsDataSource = None
    velDataSource = None
    gyroDataSource = None
    curDataSource = None
    pathDataSource = None
    
    log = None
    
    appOpen = True
    
    def isOpen(self):
        if 'normal' == self.root.state():
            return True
        
        return False
    
    def __init__(self):
        
        self.root = tk.Tk()
        self.setup()
        
        self.addToLog('GUI', 'Ready')
        
    def setup(self):
        
        self.root.geometry('1200x500')
        self.root.title(appTitle)
        self.root.configure(background='black')
        
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        
        # Divide the root frame into two columns
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1, minsize=800)
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
        dataBox.pack(pady=30)
        
        extraDataBox = tk.Frame(leftFrame)
        extraDataBox.configure(background='black')
        extraDataBox.pack(pady=30)
    


        footerBox = tk.Frame(leftFrame)
        footerBox.configure(background='black')
        footerBox.pack(side=tk.BOTTOM, pady=20)
        
        # Box for inputting GPS coordinates to follow
        #pathBox = tk.Frame(leftFrame)
        #pathBox.configure(background='black')
        #pathBox.pack(side=tk.BOTTOM, pady=20)
        
        #self.gpsInput = tk.Entry(pathBox, width=60)
        #self.gpsInput.grid(row=0, column=0, ipady=10, pady=40, padx=5, sticky='we')
        #self.gpsBtn = ttk.Button(pathBox, text="Add coordinate", command=self.addPath, style='sm.TButton')
        #self.gpsBtn.grid(row=0, column=1, ipady=3, padx=10, ipadx=10, pady=40, sticky='e')
        
        # Right frame
        
        rightFrame = tk.Frame(self.root)
        rightFrame.configure(background='blue')
        rightFrame.grid(row=0,column=1, sticky="nsew")
        rightFrame.grid_columnconfigure(0, weight=1)
        rightFrame.grid_rowconfigure(0, weight=1)
        rightFrame.grid_rowconfigure(1, weight=1)
        
        self.log = tk.Text(rightFrame)
        self.log.grid(row=0, column=0, sticky='nsew')
        
        
        self.paths = tk.Text(rightFrame)
        self.paths.grid(row=1, column=0, sticky='nsew')
        self.paths.config(state=tk.NORMAL) 
        
        
        
        # --- App buttons ---
    
        s = ttk.Style()
        s.configure('lg.TButton', font=('Calibri', 22))
        s.configure('sm.TButton', font=('Calibri', 13))
    
        self.startBtn = ttk.Button(headerBox, command=self.setupCar, text="Ignition", style='lg.TButton')
        self.startBtn.pack(side=tk.LEFT, padx=10)
        
        self.stopBtn = ttk.Button(headerBox, command=self.pauseCar, text="Pause", style='lg.TButton')
        self.stopBtn.pack(side=tk.LEFT, padx=10)
        
        
        self.controlBtn = ttk.Button(footerBox, command=self.startFollow, text="Start pathfollow", style='sm.TButton')
        self.controlBtn.pack(side=tk.LEFT, padx=10, ipadx=10)
        
        self.gamepadBtn = ttk.Button(footerBox, command=self.toggleGamepad, text="Enable gamepad", style='sm.TButton')
        self.gamepadBtn.pack(side=tk.LEFT, padx=10, ipadx=10)
        
        self.logBtn = ttk.Button(footerBox, command=self.toggleLogging, text="Start logging", style='sm.TButton')
        self.logBtn.pack(side=tk.LEFT, padx=10, ipadx=10)
        
        self.closeBtn = ttk.Button(footerBox, command=self.close, text="Close app", style='sm.TButton')
        self.closeBtn.pack(side=tk.LEFT, padx=10, ipadx=10)
        

        # --- Telemetry table ---
        
        for i in range(2):
            
            dataBox.grid_columnconfigure(i+1, minsize=150)
            
            # Label descripting which motor
            labelText = motorTitle[i]
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
            
        
        for i in range(3):
            
            extraDataBox.grid_columnconfigure(i, minsize=150)
            
            self.gpsTitleLabel[i] = ttk.Label(extraDataBox, text=dataTitles[i], font=("Calibri", 18), foreground="white", background="black")
            self.gpsTitleLabel[i].grid(row=0, column=i, padx=5, sticky='w')
            
            self.gpsDataLabel[i] = ttk.Label(extraDataBox, text='0', font=("Calibri", 18), foreground="white", background="black")
            self.gpsDataLabel[i].grid(row=1, column=i, padx=5, sticky='e')
    
    
        extraDataBox.grid_rowconfigure(0, weight=1)
        extraDataBox.grid_rowconfigure(1, weight=1)
    
        #self.setupGraph()
        
    def startFollow(self):
        var.startFollowPath = True
        
    
    def addToLog(self, arg, message):
        time = datetime.now().strftime("%H:%M:%S")
        
        string = time + ' - ' + arg + ': ' + message + '\n'
    
        self.log.insert(tk.END, string)
    
    def pauseCar(self):
        motors.pause()
        
    def addPath(self):
        
        data = self.gpsInput.get()
        self.gpsInput.delete(0,tk.END)
        
        items = data.split('\n')
        
        for i in range(len(items)):
            
            if items[i]:
                coordinate = items[i].split(',')  
                utmData = utm.from_latlon(float(coordinate[0]), float(coordinate[1]))
                
                self.pathDataSource.append([utmData[0], utmData[1]])

        self.updatePath()
          
    
    def updatePath(self):
        
        self.paths.delete(1.0,tk.END)
        
        for i in range(len(self.pathDataSource)):

            string = str(i+1) + ": " + str(self.pathDataSource[i][0]) + " " + str(self.pathDataSource[i][1]) + "\n"
            self.paths.insert(tk.END, string)
    
    
    def setGyroSource(self, source):
        self.gyroDataSource = source
        
    def setPathSource(self, source):
        self.pathDataSource = source
        self.updatePath()
        
    def setGpsSource(self, source):
        self.gpsDataSource = source
        
    
    
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
        
        self.velLabel[0]['text'] = (motors.actualVel[0] + motors.actualVel[3])/2
        self.curLabel[0]['text'] = str(round(motors.actualCur[0],2)) + " " + str(round(motors.actualCur[3],2));
        
        self.velLabel[1]['text'] = (motors.actualVel[1] + motors.actualVel[2])/2
        self.curLabel[1]['text'] = str(round(motors.actualCur[1],2)) + " " + str(round(motors.actualCur[2],2));
        
        for i in range(2):
            self.velLabel[i]['text'] = motors.actualVel[i]
            self.curLabel[i]['text'] = motors.actualCur[i]
          
        
        self.gpsDataLabel[0]['text'] = round(self.gyroDataSource[2],6)
        self.gpsDataLabel[1]['text'] = round(self.gpsDataSource[3],4)
        self.gpsDataLabel[2]['text'] = round(self.gpsDataSource[4],4)
        
        self.root.update()
        
    def close(self):
        self.appOpen = False
        self.root.destroy()
 