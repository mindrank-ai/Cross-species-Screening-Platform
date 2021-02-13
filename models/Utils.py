import os
import sys
from .ImportTools import *

class logit(object):
    def __init__(self, logfile="out.log"):
        self.logfile = logfile
        
    def __call__(self, func):
        @wraps(func)
        def wrapped_function(self, *args, **kwargs):
            print(func.__name__ + " was called")
            res = func(self, *args, **kwargs)
            return res
        return wrapped_function
 
    def notify(self):
        pass
    
class timeit(object):
    def __init__(self):
        pass
 
    def __call__(self, func):
        @wraps(func)
        def wrapped_function(self, *args, **kwargs):
            start = time.process_time()
            res = func(self, *args, **kwargs)
            end =time.process_time()
            print(f'{func.__name__} used: {round(end - start, 5)}s')
            return res
        return wrapped_function
 
    def notify(self):
        pass
    
class checkit(object):
    def __init__(self):
        pass
 
    def __call__(self, func):
        @wraps(func)
        def wrapped_function(self, *args, **kwargs):
            try:
                res = func(self, *args, **kwargs)
            except Exception as e:
                print(f"###{func.__name__}### {e}")
                return -1
            return res
        return wrapped_function
 
    def notify(self):
        pass
    
    

def parse_args():
    """Parses input arguments."""
    parser = argparse.ArgumentParser(description="Cross species Screening Platform.")
    parser.add_argument("--candidate-file", "-c",
                        help="Candidate data filename.",
                        type=str, required = True)
    
    parser.add_argument("--target-file", "-t",
                        help="Target data filename.",
                        type=str, required = True)
    
    parser.add_argument("--output-file", "-o",
                        help="Output data filename.",
                        type=str, default="output")
    
    parser.add_argument("--path", "-p",
                        help="input file path",
                        type=str, default="./data")
    
    parser.add_argument("--cores", "-cores",
                        help="computing cores.",
                        type=int, default=20)
    
    parser.add_argument("--save", action="store_true", help="Save result or not.")

    return parser.parse_args()