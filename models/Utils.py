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
    
    
@checkit()
def parse_args():
    """Parses input arguments."""
    parser = argparse.ArgumentParser(description="Scoring the SMILES.")
    parser.add_argument("--query-type", "-q",
                        help="Input query type.",
                        type=str, default="drugs")
    
    parser.add_argument("--query-size", "-s",
                        help="Input query type.",
                        type=int, default=10)
    
    parser.add_argument("--max-theads", "-m",
                        help="Input query type.",
                        type=int, default=20)
    parser.add_argument("--target", "-t",
                        help="Input target.",
                        type=str, required = True)
    
    parser.add_argument("--file-name", "-n",
                        help="Input result file file name.",
                        type=str, default="result")
    parser.add_argument("--save", action="store_true", help="Save result or not.")
    parser.add_argument("--isTest", action="store_true", help="Testing or not.")

    return parser.parse_args()