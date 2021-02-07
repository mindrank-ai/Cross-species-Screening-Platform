import os
import sys
from .MultiProcess import MultiProcess
from .Utils import logit, timeit, checkit
from .ImportTools import *

class StrucEmbedding(MultiProcess):
    def __init__(self, method="one", cores=10, data=None, save=False, save_path="", prefix="tmp"):
        MultiProcess.__init__(self, cores=cores, save=save, save_path=save_path, postfix='strucemb', prefix=prefix)
        self.method = method
        self.data = data
      
    @checkit()
    def struc_emb(self,m):
        mol = Chem.MolFromSmiles(m)
        fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, useFeatures=True)
        return fp
    
    def struc_result(self,data):
        return data['SMILES'].apply(lambda x: self.struc_emb(x))
        
    def get_result(self):
        start =time.process_time()
        apply_method = self.method_factory(self.method,"apply")
        self.data['struc_emb'] = apply_method(self.method_factory('struc', 'result'), self.data)
        self.save_result(self.data)
        end3 = time.process_time()
        print(f'{self.method} Running time: {round(end3 - start, 5)} Seconds')
        return self.data