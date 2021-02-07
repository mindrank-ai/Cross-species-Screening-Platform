import os
import sys
from .MultiProcess import MultiProcess
from .Utils import logit, timeit, checkit
from .ImportTools import *


class M2VEmbedding(MultiProcess):
    def __init__(self, method="one", cores=10, data=None, save=False, save_path="", prefix=""):
        MultiProcess.__init__(self, cores=cores, save=save, save_path=save_path, postfix='m2vemb')
        self.model_path = "./data"
        self.method = method
        self.data = data
        self.model = word2vec.Word2Vec.load(f'{self.model_path}/model_300dim.pkl')
       
    @checkit()
    def sentence2vec_result(self, data):
        return DfVec(sentences2vec([MolSentence(mol2alt_sentence(Chem.MolFromSmiles(data), 1))], self.model, unseen='UNK'))
    
    def mol2vec_result(self, data):
        return data['SMILES'].apply(lambda x: self.sentence2vec_result(x))
        
    def get_result(self):
        start =time.process_time()
        apply_method = self.method_factory(self.method,"apply")
        self.data['mol2vec'] = apply_method(self.method_factory('mol2vec', 'result'), self.data)
        self.save_result(self.data)
        end3 = time.process_time()
        print(f'{self.method} Running time: {round(end3 - start, 5)} Seconds')
        return self.data