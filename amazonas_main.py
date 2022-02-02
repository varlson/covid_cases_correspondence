from process import *

dataFrame = pd.read_csv('filtred/terrestrial.csv')
graph = ig.Graph.Read_GraphML('input_datas/terrestrial.GraphML')

pat =  'input_datas/amazonas_state'
dirMaker(pat)
amazonas_extractor(dataFrame, graph, pat+'/terrestrial')
