import time;
from threading import Timer

controlSystem = False;

def repeater(start, interval, count):
    
    # Get current time
    ticks = time.time()
    
    # Set next timing event
    t = Timer( interval - (ticks-start-count*interval), repeater, [start, interval, count+1])
    t.start()
    
    # Perform function here
    print(ticks - start, "#", count )
    print("HAR DU ET STORT OSTEHJUL?", controlSystem)
    time.sleep(0.01)



dt = 0.025 # interval in sec
t = Timer(dt, repeater, [round(time.time()), dt, 0]) # start over at full second, round only for testing here
t.start()

while(1):
    
    time.sleep(0.2);
    print("GRYDERENS")
    
    controlSystem = not controlSystem;