from process import *

# dataFrame = pd.read_csv('input_datas/filtred/aerial.csv')
# graph = ig.Graph.Read_GraphML('input_datas/aerial.GraphML')

# pat =  'input_datas/filtred/north_of_brazil'
# dirMaker(pat)
# northBrazil_extractor(dataFrame, graph, pat+'/aerial')


_tuple = []
in_path = 'input_datas/filtred/north_of_brazil'
out_path = 'output/north_of_brazil'
name='terrestrial'
graph = ig.Graph.Read_GraphML('input_datas/terrestrial.GraphML')
mobility = pd.read_csv(in_path+'/terrestrial.csv')

ausentes = csv_loader(in_path+'/terrestrial')

degree = sort_by_metric(graph, "degree")
betweenness = sort_by_metric(graph, "betweenness")
betweenness_w = sort_by_metric(graph, "betweenness_w")
strength = sort_by_metric(graph, "strength")

x_axis = [i for i, x in enumerate(graph.vs['geocode']) if x not in list(ausentes['Ausentes'])]

cities_geocodeList = list(mobility['Geocode'])

graph_geocodeList = [x[3] for x in degree]
corresp = correspondence_builder(cities_geocodeList, graph_geocodeList)
spear = mapeador(mobility, degree)
_tuple.append((x_axis, corresp, spear))
processed_data_exporter(x_axis, corresp, out_path+'/csv', name+'k')



graph_geocodeList = [x[3] for x in betweenness]
corresp = correspondence_builder(cities_geocodeList, graph_geocodeList)
spear = mapeador(mobility, betweenness)
_tuple.append((x_axis, corresp, spear))
processed_data_exporter(x_axis, corresp, out_path+'/csv', name+'b')


graph_geocodeList = [x[3] for x in betweenness_w]
corresp = correspondence_builder(cities_geocodeList, graph_geocodeList)
spear = mapeador(mobility, betweenness_w)
_tuple.append((x_axis, corresp, spear))
processed_data_exporter(x_axis, corresp, out_path+'/csv', name+'b_w')


graph_geocodeList = [x[3] for x in strength]
corresp = correspondence_builder(cities_geocodeList, graph_geocodeList)
spear = mapeador(mobility, strength)
_tuple.append((x_axis, corresp, spear))
processed_data_exporter(x_axis, corresp, out_path+'/csv', name+'s')



graphPloter(_tuple, ["$k$","$b$", "$s$", "$b_{w}$"], name, out_path+'/plot')