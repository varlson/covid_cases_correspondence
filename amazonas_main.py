from process import *

# dataFrame = pd.read_csv('input_datas/filtred/aerial.csv')
# graph = ig.Graph.Read_GraphML('input_datas/aerial.GraphML')

# pat =  'input_datas/amazonas_state'
# dirMaker(pat)
# amazonas_extractor(dataFrame, graph, pat+'/aerial')



_tuple = []
in_path = 'input_datas/amazonas_state'
out_path = 'output/amazonas_state'
name='terrestrial'
graph = ig.Graph.Read_GraphML('input_datas/terrestrial.GraphML')
mobility = pd.read_csv(in_path+'/terrestrial.csv')

ausentes = csv_loader(in_path+'/terrestrial_ausentes')

degree = sort_by_metric(graph, "degree")
betweenness = sort_by_metric(graph, "betweenness")
betweenness_w = sort_by_metric(graph, "betweenness_w")
strength = sort_by_metric(graph, "strength")

x_axis = [i for i, x in enumerate(graph.vs['geocode']) if x not in list(ausentes['Ausentes'])]

graph_geocodeList = [x[3] for x in degree if x[3] not in list(ausentes['Ausentes'])]
cities_geocodeList = [x for x in list(mobility['Geocode']) if x not in list(ausentes['Ausentes'])]


corresp = correspondence_builder(cities_geocodeList, graph_geocodeList)
spear = mapeador(mobility, degree)
_tuple.append((x_axis, corresp, spear))
processed_data_exporter(x_axis, corresp, out_path+'/csv', name+'k')

# print(f'x_axis: {x_axis}')
# print(f'y_axis: {corresp}')


graph_geocodeList = [x[3] for x in betweenness if x[3] not in list(ausentes['Ausentes'])]
corresp = correspondence_builder(cities_geocodeList, graph_geocodeList)
spear = mapeador(mobility, betweenness)
_tuple.append((x_axis, corresp, spear))
processed_data_exporter(x_axis, corresp, out_path+'/csv', name+'b')


graph_geocodeList = [x[3] for x in betweenness_w if x[3] not in list(ausentes['Ausentes'])]

corresp = correspondence_builder(cities_geocodeList, graph_geocodeList)
spear = mapeador(mobility, betweenness_w)
_tuple.append((x_axis, corresp, spear))
processed_data_exporter(x_axis, corresp, out_path+'/csv', name+'b_w')


graph_geocodeList = [x[3] for x in strength if x[3] not in list(ausentes['Ausentes'])]
corresp = correspondence_builder(cities_geocodeList, graph_geocodeList)
spear = mapeador(mobility, strength)
_tuple.append((x_axis, corresp, spear))
processed_data_exporter(x_axis, corresp, out_path+'/csv', name+'s')



graphPloter(_tuple, ["$k$","$b$", "$s$", "$b_{w}$"], name, out_path+'/plot')