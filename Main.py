import os
import sys
from models.StandardFactory import StandardFactory
from models.ImportTools import *
import numpy as np
import pandas as pd

def process_all_emb(data_dic=None, cores=10, save=False): 
    EmbedFactory = StandardFactory.get_factory("embedding")
    m2vemb = EmbedFactory.get_instance('m2v')
    d3emb = EmbedFactory.get_instance('d3')
    strucemb = EmbedFactory.get_instance('struc')
    result = {}
    for k,v in data_dic.items():
        result_tmp = []
        m2v_t = m2vemb(method='map', data=v.copy(), save=save, cores=cores, prefix=k)        
        d3_t = d3emb(method='map', data=v.copy(), save=save, cores=cores, prefix=k)               
        struce_t = strucemb(method='map', data=v.copy(), save=save, cores=cores, prefix=k)        
        result_tmp.append(m2v_t.get_result())
        result_tmp.append(d3_t.get_result())
        result_tmp.append(struce_t.get_result())
        result[k] = result_tmp
    return result

def process_all_score(data_dic=None, cores=10, save=False): 
    ScoreFactory = StandardFactory.get_factory("scoring")
    m2vscore = ScoreFactory.get_instance('m2v')
    d3score = ScoreFactory.get_instance('d3')
    strucscore = ScoreFactory.get_instance('struc')
    result = {}
    for k,v in data_dic.items():
        result_tmp = []
        m2v_s = m2vscore(method='map', target=v[0][0], data=v[1][0], save=save, cores=cores, prefix=k)
        d3_s = d3score(method='map', target=v[0][1], data=v[1][1], save=save, cores=cores, prefix=k)
        struc_s = strucscore(method='map', target=v[0][2], data=v[1][2], save=save, cores=cores, prefix=k)
        result_tmp.append(m2v_s.get_result())
        result_tmp.append(d3_s.get_result())
        result_tmp.append(struc_s.get_result())
        result[k] = result_tmp
    return result


def emb_filter(data_dic=None):
    result = {}
    for k,v in data_dic.items():
        tmp_lst = []
        for df_tmp in v:
            col = [f for f in df_tmp.columns if f not in ["ID", "SMILES"]][0]
            tmp_lst.append(df_tmp[df_tmp[col] != -1].reset_index(drop=True))
        result[k] = tmp_lst
    return result
    
def get_similarity(input_path="", candidate_file="", target_file=""):
    
    df_c = pd.read_csv(input_path + candidate_file)
    df_t = pd.read_csv(input_path + target_file)

    emb_dic = {}
    emb_dic['test_c'] = df_c
    emb_dic['test_t'] = df_t
    emb_result =emb_filter(data_dic = process_all_emb(data_dic = emb_dic, cores=20)) 
    result_c = emb_result['test_c']
    result_t = emb_result['test_t']
    socre_dic = {}
    socre_dic['test_socre'] = [result_t, result_c]
    score_result = process_all_score(data_dic = socre_dic, cores=20)
    df_result = df_c[['ID']]
    for df_ in score_result['test_socre']:
        df_result = df_result.merge(df_, on='ID', how='left')
    return df_result



if __name__ == "__main__":
    start =time.time()
    result = get_similarity(input_path="./data/", candidate_file="candidate_test.csv", target_file="target_test.csv")
    print(result.head())
    end = time.time()
    print('Running time: %s Seconds'%(end-start))
