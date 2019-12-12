import time
import locale

locale.setlocale(locale.LC_ALL, 'da_DK')

path = 'logs/'
logExt = '.csv'

class Logging:
    
    filename = None
    
    log = None
    data = []
    titles = []
    logNextTime = 0
    logStartTime = 0
    logLine = 0
    
    startLogging = False
    
    def __init__(self, filename):
       self.filename = filename
    
    def begin(self):
        
        if self.filename:
            
            self.log = open( path + self.filename + logExt, "a+")
            
            # Clear old log (if filename is the same as before)
            self.log.truncate(0)
            
            self.logStartTime = time.time()
            self.logLine = 0
            self.startLogging = True
            
            
            header = 'Time [s];'
            
            for i in range( len( self.titles ) ):
                header += self.titles[i] + ';'
                
            header += '\n'
            
            self.log.write(header)
        
    def stop(self):
        self.startLogging = False
        self.log.close()
        
    def addMeasurements( self, pointer, titles ):
        
        self.data.append(pointer)
        
        for i in range(len(titles)):
            self.titles.append( titles[i] )
            
        # If some titles are missing (should be one for each data item), then fill in an empty string
        missing = max(len(pointer) - len(titles), 0)
        
        for i in range(missing):
            self.titles.append('-')
        
    
    def addLine( self ):
        if self.startLogging:
            # Calculate the timestamp for this measurement
            now = time.time() - self.logStartTime
            try:
                string = locale.format('%.4f', now ) + ';'
            
                for i in range( len(self.data) ):
                    for j in range( len(self.data[i]) ):
                        string += locale.format('%.10f', self.data[i][j]) + ';'
            except Exception as error:
                print("LOGGING:", error)
                
            string += '\n'
            
            self.log.write(string)
            self.logLine += 1
                
    
    def update( self, interval = 0, samples = 0 ):
        
        if self.startLogging:
            if( time.time() >= self.logNextTime and (self.logLine < samples or samples == 0) ):
                
                # Calculate the timestamp for this measurement
                now = time.time() - self.logStartTime
                
                # Calculate and fix shift in time due to timing inaccuracies 
                dif = now - interval*self.logLine

                # Set next time a new line should be written to log
                self.logNextTime = time.time() + interval - dif 
                
                string = locale.format('%.4f', now ) + ';'
                
                for i in range( len(self.data) ):
                    for j in range( len(self.data[i]) ):
                        string += locale.format('%.6f', self.data[i][j]) + ';'
                   
                string += '\n'
                
                self.log.write(string)
                self.logLine += 1
                
                #print(string)
        
            # If we have reached the wanted number of samples, stop and close the file
            if self.logLine >= samples and samples != 0:
                self.startLogging = False
                self.log.close()
