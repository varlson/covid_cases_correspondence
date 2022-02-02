import igraph as ig
import pandas as pd
import numpy as np
from os import mkdir,path


"""
# Cria um diretorio caso o mesmo nao exista
# Entrada: nome de um ou diretorio com sub diretorios no formato: ex: "dados" caso um só, 
#   "dados/dados_importantes" diretorio com subdiretorio
"""
def dirMaker(dir):
    if not len(dir):
        print('invalid path')
        return 0
    
    subdirs = dir.split('/')
    fullPath =[]
    
    for index, dir in enumerate(subdirs):
        if not index:
            fullPath.append(dir)
        else:
            fullPath.append(fullPath[index-1]+'/'+dir)
    # print(fullPath)
    
    try:
        for p in fullPath:
            if not path.isdir(p):
                mkdir(p)
    except:
        print('Houve umerro, verifique o path inserito se esta no formato uma_pasta/outra_pasta/...')
        return 0



""" ---------------------------------------------
    counter => Função auxialiador da função correspondence_builder,
        ela retorna a numero de aparição de n nós nos primeiros n cidades
        
    Paramentros:
        nodes => Nós da rede
        cities => lista de cidades de aparição de casos
"""

def counter(n, nodes,cities):
    count=0
    for node in nodes[:n]:
        if node in cities[:n]:
            count+=1
    
    return count



def csv_loader(path):
    return pd.read_csv(path+'.csv')


def graph_ml_loader(path):
    return ig.Graph.Read_GraphML(path+'.GraphML')

def north_brazil_geocode_extractor(label, graph, dataFrame):
    geocode =[]
    