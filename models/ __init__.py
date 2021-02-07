# import os
# import sys
# sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# import time
# from functools import wraps

# from rdkit import Chem, DataStructs, RDConfig
# from rdkit.Chem import AllChem, rdShapeHelpers
# from rdkit.Chem.Pharm2D import Gobbi_Pharm2D, Generate
# from rdkit import Chem
# from functools import lru_cache
# from rdkit.Chem.FeatMaps import FeatMaps
# import time
# from gensim.models import word2vec
# from mol2vec.features import mol2alt_sentence, mol2sentence, MolSentence, DfVec, sentences2vec
# from multiprocessing import Pool
# from sklearn.metrics.pairwise import cosine_similarity, pairwise_distances
# import warnings
# warnings.filterwarnings("ignore")

# __all__ = []
# # for loader, module_name, is_pkg in  pkgutil.walk_packages(__path__):
# #     __all__.append(module_name)
# #     _module = loader.find_module(module_name).load_module(module_name)
# #     globals()[module_name] = _module