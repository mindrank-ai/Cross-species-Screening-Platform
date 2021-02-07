from rdkit import Chem, DataStructs, RDConfig
from rdkit.Chem import AllChem, rdShapeHelpers
from rdkit.Chem.Pharm2D import Gobbi_Pharm2D, Generate
from rdkit import Chem
from functools import lru_cache
from rdkit.Chem.FeatMaps import FeatMaps
import os
import sys
import threading
from tqdm import tqdm
tqdm.pandas()
import time
from gensim.models import word2vec
from mol2vec.features import mol2alt_sentence, mol2sentence, MolSentence, DfVec, sentences2vec
from multiprocessing import Pool
import math

from sklearn.metrics.pairwise import cosine_similarity, pairwise_distances
import numpy as np
import pandas as pd
import argparse
from functools import wraps
from rdkit import RDConfig,RDLogger
import warnings

warnings.filterwarnings("ignore")

lg = RDLogger.logger()
lg.setLevel(RDLogger.CRITICAL )