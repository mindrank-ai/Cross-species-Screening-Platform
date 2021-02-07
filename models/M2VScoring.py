import os
import sys
from .MultiProcess import MultiProcess
from .Utils import logit, timeit, checkit
from .ImportTools import *

class M2VScoring(MultiProcess):   
    def __init__(self, method="one", cores=10, data=None, save=False, target=None, save_path="", prefix="tmp"):
        MultiProcess.__init__(self, cores=cores, save=save, save_path=save_path, postfix='m2vscore', prefix=prefix)
        self.method = method
        self.data = data
        self.target = target
        self.block = 1
        
    def matrix_result(self, data):
        return data['mol2vec'].apply(lambda x:x.vec)
    
    @checkit()
    def cosine_result(self, X, Y):
        return pairwise_distances(X, Y, metric="cosine")
        
    def get_result(self):
        start =time.process_time()
        cols_name=self.target["ID"].tolist()
        rows_name=self.data["ID"].tolist()
#         apply_method = self.method_factory(self.method,"apply")
        
#         X = np.vstack(apply_method(self.method_factory('matrix', 'result'), self.data))
#         Y = np.vstack(apply_method(self.method_factory('matrix', 'result'), self.target))

        X = np.vstack(self.method_factory('matrix', 'result')(self.data))
        Y = np.vstack(self.method_factory('matrix', 'result')(self.target))
        caculater = self.method_factory('cosine', 'result')
        cos_result = caculater(X, Y)

        df_result = pd.DataFrame(cos_result, columns=[f+"_COS" for f in cols_name])
        df_result["ID"] = rows_name
        self.save_result(df_result)
        
        end3 = time.process_time()
        print(f'{self.method} Running time: {round(end3 - start, 5)} Seconds')
        return df_result