from time import time
from itertools import cycle



class ProgressBar:
    
    def __init__(self, 
                 format=None, 
                 max=100, 
                 width=100, 
                 message="Processing: ", 
                 elapsed=False, 
                 eta=True):
        
        self.max = max
        self.width = width
        self.message = message
        self._elapsed = elapsed
        self._eta = eta
        
        self.index = 0
        self.since = time()
        
        if format is None:
            self.l_char = "#"
            self.r_char = " "
            
        elif format == "Charging":
            self.l_char = "\u2588"
            self.r_char = "\u2219"
            
        elif format == "FillingSquares":
            self.l_char = "\u25a3"
            self.r_char = "\u25a2"
            
        elif format == "FillingCircles":
            self.l_char = "\u25c9"
            self.r_char = "\u25ef"
    
    
    @staticmethod
    def time_to_str(time_val):
        if time_val//60:
            return f"{time_val//60 :.0f}m {time_val%60 :.0f}s"
        
        else: 
            return f"{time_val :.0f}s"
    
    
    def elapsed(self):
        time_elapsed = time() - self.since
        return self.time_to_str(time_elapsed)
    
    
    def eta(self, index):
        time_eta = (time() - self.since) / index * (self.max - index)
        return self.time_to_str(time_eta)
    
    
    def show(self, index):
        count = self.width * index // self.max
        left = self.l_char * count
        right = self.r_char * (self.width - count)
        
        if self._elapsed and self._eta:
            info = f" [elapsed: {self.elapsed()}; ETA: {self.eta(index)}]".ljust(25)
        elif self._elapsed:
            info = f" [elapsed: {self.elapsed()}]".ljust(25)
        elif self._eta:
            info = f" [ETA: {self.eta(index)}]".ljust(25)
        else:
            info = ""
        
        print(f"\r{self.message}[{left}{right}] {index/self.max :.0%}{info}", 
              end="", flush=True)
    
    
    def next(self):
        self.index += 1
        self.show(self.index)
     
    
    def finish(self):
        self.index = 0
        self.since = time()
    
    
    def __enter__(self):
        return self
    
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.finish()



class ProgressSpinner:

    def __init__(self, format=None, message="Processing: "):
        self.message = message
        
        if format is None:
            self.cycle = cycle("-\|/")
            
        elif format == "Pie":
            self.cycle = cycle("\u25f7\u25f6\u25f5\u25f4")
        
        elif format == "Moon":
            self.cycle = cycle("\u25d0\u25d3\u25d1\u25d2")
            
        elif format == "Pixel":
            self.cycle = cycle("\u28f7\u28ef\u28df\u287f\u28bf\u28fb\u28fd\u28fe")
        
        
    def next(self):
        frame = next(self.cycle)
        print(f"\r{self.message}{frame}", end="", flush=True)
        
        
    def __enter__(self):
        return self
    
    
    def __exit__(self, exc_type, exc_value, traceback):
        pass
