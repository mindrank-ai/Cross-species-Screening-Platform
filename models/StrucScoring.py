import os
import sys
from .MultiProcess import MultiProcess
from .Utils import logit, timeit, checkit
from .ImportTools import *

class StrucScoring(MultiProcess): 
    def __init__(self, method="one", cores=10, data=None, save=False, target=None, save_path="", prefix="tmp"):
        MultiProcess.__init__(self, cores=cores, save=save, save_path=save_path, postfix='strucscore', prefix=prefix)
        self.method = method
        self.data = data
        self.target = target
        
    @checkit()
    def sim_structure_AF(self, m1, m2):
        return DataStructs.TanimotoSimilarity(m1,m2)
    
    def strucscore_result(self, data):
        return data["struc_emb"].apply(lambda x:self.target["struc_emb"].apply(lambda y: self.sim_structure_AF(x, y)))
    
    def get_result(self):
        start =time.process_time()
        cols_name=self.target["ID"].tolist()
        rows_name=self.data["ID"].tolist()
        apply_method = self.method_factory(self.method,"apply")
        result = apply_method(self.method_factory('strucscore', 'result'), self.data)

        result.columns = [f+"_Struc" for f in cols_name]
        result['ID'] = rows_name
        self.save_result(result)
        end3 = time.process_time()
        print(f'{self.method} Running time: {round(end3 - start, 5)} Seconds')
        return result