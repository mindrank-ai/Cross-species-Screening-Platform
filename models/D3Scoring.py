import os
import sys
from .MultiProcess import MultiProcess
from .Utils import logit, timeit, checkit
from .ImportTools import *

class D3Scoring(MultiProcess):
    
    def __init__(self, method="", cores=10, data=None, save=False, target=None, save_path="", prefix="tmp", block=1):
        MultiProcess.__init__(self, cores=cores, save=save, save_path=save_path, postfix='d3score', prefix=prefix, block=block)
        self.method = method
        self.data = data
        self.target = target
     

    def get_FeatureMapScore(self, query_mol, ref_mol):
        fdefName = os.path.join(RDConfig.RDDataDir, 'BaseFeatures.fdef')
        fdef = AllChem.BuildFeatureFactory(fdefName)
        fmParams = {}
        for k in fdef.GetFeatureFamilies():
            fparams = FeatMaps.FeatMapParams()
            fmParams[k] = fparams
        keep = ('Donor', 'Acceptor', 'NegIonizable', 'PosIonizable', 
                'ZnBinder', 'Aromatic', 'Hydrophobe', 'LumpedHydrophobe')
        
        featLists = []
        for m in [query_mol, ref_mol]:
            rawFeats = fdef.GetFeaturesForMol(m)
            featLists.append([f for f in rawFeats if f.GetFamily() in keep])
        fms = [FeatMaps.FeatMap(feats=x, weights=[1] * len(x), params=fmParams) for x in featLists]
        fms[0].scoreMode=FeatMaps.FeatMapScoreMode.Best
        fm_score = fms[0].ScoreFeats(featLists[1]) / min(fms[0].GetNumFeatures(), len(featLists[1]))
        return fm_score

    @checkit()
    def calc_SC_RDKit_score(self, query_mol, ref_mol):
        fm_score = self.get_FeatureMapScore(query_mol, ref_mol)
        protrude_dist = rdShapeHelpers.ShapeProtrudeDist(query_mol, ref_mol, allowReordering=False)
        SC_RDKit_score = 0.5*fm_score + 0.5*(1 - protrude_dist)
        return SC_RDKit_score
    
    def d3score_result(self, data):
        return data["d3_emb"].apply(lambda x:self.target["d3_emb"].apply(lambda y: self.calc_SC_RDKit_score(x, y))) 
    
    def get_result(self):
        start =time.process_time()
        cols_name=self.target["ID"].tolist()
        rows_name=self.data["ID"].tolist()
        apply_method = self.method_factory(self.method,"apply")
        result = apply_method(self.method_factory('d3score', 'result'), self.data)

        result.columns = [f+"_D3" for f in cols_name]
        result['ID'] = rows_name
        self.save_result(result)
        end3 = time.process_time()
        print(f'{self.method} Running time: {round(end3 - start, 5)} Seconds')
        return result