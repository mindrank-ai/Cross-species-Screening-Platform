import os
import sys
from .ImportTools import *
from .Utils import logit, timeit, checkit
import numpy as np
import pandas as pd

class MultiProcess(object):
    def __init__(self, cores=10, save=False, save_path="./cache", prefix="tmp", postfix="tmp", block=1):
        self.cores = cores
        self.save = save
        self.save_path = save_path
        self.prefix = prefix
        self.postfix = postfix
        self.block = block
    
    @checkit()
    def method_factory(self, funcname, functype):
        return getattr(self, f"{funcname}_{functype}")

        
    @logit()
    def imap_apply(self, func, data):
        print(f"{self.cores} cores called!")
        df_tmp=np.array_split(data, math.ceil(data.shape[0]/self.block))
        with Pool(processes=self.cores) as pool:
            result_parts = [x for x in tqdm(pool.imap(func, df_tmp), total=len(df_tmp))]
        result_parallel = pd.concat(result_parts)
        return result_parallel
    
    @logit()
    def map_apply(self, func, data):
        print(f"{self.cores} cores called!")
        df_tmp=np.array_split(data, math.ceil(data.shape[0]/self.block))
        with Pool(processes=self.cores) as pool:
            result_parts = pool.map(func, df_tmp)
        result_parallel = pd.concat(result_parts)
        return result_parallel
    
    @logit()
    def one_apply(self, func, data):
        return func(data)
    
    @logit()
    def save_result(self, data):
        if self.save:
            data.to_hdf(f"{self.save_path}{self.prefix}_{self.postfix}.hdf", key="data")
            print(f"{self.save_path}{self.prefix}_{self.postfix}.hdf saved succeed!")