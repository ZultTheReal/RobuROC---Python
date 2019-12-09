from threading import Timer

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.function   = function
        self.interval   = interval
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

# Timer test
import time

lasttime = [0]

def hello(timing):
    print( (time.time() - timing[0]) )
    timing[0] = time.time();
    #time.sleep(0.01)
    


rt = RepeatedTimer(0.1, hello, lasttime) # it auto-starts, no need of rt.start()
try:
    time.sleep(5) # your long-running job goes here...
finally:
    rt.stop() # better in a try/finally block to make sure the program ends!
    
    