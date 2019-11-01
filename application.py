import tkinter as tk
from tkinter import ttk

appTitle = 'RoboRUC Control Panel'
rowTitles = ['Motor','Current [A]','Velocity [m/s]']

class Application():
    
    # Defining the labels
    motorLabel = [None for x in range(4)]
    curLabel = [None for x in range(4)]
    velLabel = [None for x in range(4)]
    titleLabel = [None for x in range(3)]
    
    def __init__(self):
        
        self.root = tk.Tk()
        self.root.geometry('800x480')
        self.root.title(appTitle)
        self.root.configure(background='black')
        
        # --- App frames ---
        
        headerBox = tk.Frame(self.root)
        headerBox.configure(background='black')
        headerBox.pack(side=tk.TOP, pady=30)
        
        dataBox = tk.Frame(self.root)
        dataBox.configure(background='black')
        dataBox.pack(pady=50)

        footerBox = tk.Frame(self.root)
        footerBox.configure(background='black')
        footerBox.pack(side=tk.BOTTOM, pady=50)
        
        # --- App buttons ---
    
        s = ttk.Style()
        s.configure('lg.TButton', font=('Calibri', 22))
        s.configure('sm.TButton', font=('Calibri', 13))
    
        self.startBtn = ttk.Button(headerBox, text="Ignition", style='lg.TButton')
        self.startBtn.pack(side=tk.LEFT, padx=10)
        
        self.stopBtn = ttk.Button(headerBox, text="Stop", style='lg.TButton')
        self.stopBtn.pack(side=tk.LEFT, padx=10)
        
        self.gamepadBtn = ttk.Button(footerBox, text="Enable gamepad", style='sm.TButton')
        self.gamepadBtn.pack(side=tk.LEFT, padx=10, ipadx=10)
        
        self.logBtn = ttk.Button(footerBox, text="Start logging", style='sm.TButton')
        self.logBtn.pack(side=tk.LEFT, padx=10, ipadx=10)
        
        self.closeBtn = ttk.Button(footerBox, command=self.close, text="Close app", style='sm.TButton')
        self.closeBtn.pack(side=tk.LEFT, padx=10, ipadx=10)
        

        # --- Telemetry table ---
        
        for i in range(4):
            # Label descripting which motor
            labelText = str(i+1)
            self.motorLabel[i] = ttk.Label(dataBox, text=labelText, font=("Calibri", 18), foreground="white", background="black")
            self.motorLabel[i].grid(row=0, column=i+1, padx=5)
            
            # Label for current
            self.curLabel[i] = ttk.Label(dataBox, text="0.0", font=("Calibri", 18), foreground="white", background="black")
            self.curLabel[i].grid(row=1, column=i+1, padx=5)
            
            # Label for velocity
            self.velLabel[i] = ttk.Label(dataBox, text="0", font=("Calibri", 18), foreground="white", background="black")
            self.velLabel[i].grid(row=2, column=i+1, padx=5)
        
        # Label titles for table
        for i in range(3):
            self.titleLabel[i] = ttk.Label(dataBox, text=rowTitles[i], font=("Calibri", 18), foreground="white", background="black")
            self.titleLabel[i].grid(row=i, column=0, padx=5)
            
    def update(self):
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
        


app = Application();

while(1):
    
    app.setLabelValue( 'current', [23, 12, 245, 11] )
    app.update()