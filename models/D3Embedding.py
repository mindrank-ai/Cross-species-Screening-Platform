import os
import sys
from .MultiProcess import MultiProcess
from .Utils import logit, timeit, checkit
from .ImportTools import *

class D3Embedding(MultiProcess):
        
    def __init__(self, method="", cores=10, data=None, save=False, save_path="", prefix="tmp"):
        MultiProcess.__init__(self, cores=cores, save=save, save_path=save_path, postfix='d3emb', prefix=prefix)
        self.method = method
        self.data = data
        
    @checkit()
    def d3_mol(self, m):
        mol = Chem.MolFromSmiles(m)
        mol = Chem.AddHs(mol)
        AllChem.EmbedMolecule(mol,randomSeed=42)
        AllChem.UFFOptimizeMolecule(mol)
        return mol
    
    def d3mol_result(self, data):
        return data['SMILES'].apply(lambda x: self.d3_mol(x))
        
    def get_result(self):
        start =time.process_time()
        apply_method = self.method_factory(self.method,"apply")
        self.data['d3_emb'] = apply_method(self.method_factory('d3mol', 'result'), self.data)
        self.save_result(self.data)
        end3 = time.process_time()
        print(f'{self.method} Running time: {round(end3 - start, 5)} Seconds')
        return self.data