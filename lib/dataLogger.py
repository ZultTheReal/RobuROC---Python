import time
import locale

locale.setlocale(locale.LC_ALL, 'da_DK')

path = 'logs/'
logExt = '.csv'

class Logging:
    
    log = None
    data = []
    titles = []
    logNextTime = 0
    logStartTime = 0
    logLine = 0
    
    def __init__(self, filename):
        
        self.log = open( path + filename + logExt, "a+")
        
    
    def begin(self):
        
        # Clear old log (if filename is the same as before)
        self.log.truncate(0)
        
        self.logStartTime = time.time()
        self.logLine = 0
        
        
        header = 'Time [s];'
        
        for i in range( len( self.titles ) ):
            header += self.titles[i] + ';'
            
        header += '\n'
        
        self.log.write(header)
        
        
    def addMeasurements( self, pointer, titles):
        
        self.data.append(pointer)
        
        for i in range(len(titles)):
            self.titles.append( titles[i] )
            
        # If some titles are missing (should be one for each data item), then fill in an empty string
        missing = max(len(pointer) - len(titles), 0)
        
        for i in range(missing):
            self.titles.append('-')
        
    
    def update( self, interval = 0, samples = 0 ):
        
        
        if( time.time() >= self.logNextTime and self.logLine < samples):
            
            # Calculate the timestamp for this measurement
            now = time.time() - self.logStartTime
            
            # Calculate and fix shift in time due to timing inaccuracies 
            dif = now - interval*self.logLine

            # Set next time a new line should be written to log
            self.logNextTime = time.time() + interval - dif 
            
            string = locale.format('%.4f', now ) + ';'
            
            for i in range( len(self.data) ):
                for j in range( len(self.data[i]) ):
                    string += locale.format('%.4f', self.data[i][j]) + ';'
               
            string += '\n'
            
            self.log.write(string)
            self.logLine += 1
            
            print(string)
            
        if self.logLine >= samples:
            self.log.close()