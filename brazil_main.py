from process import *

def data_separator(dataFrame, output_path, graph, filename):
    extractor(dataFrame, graph, output_path, filename)


# o_path = "input_datas/filtred"
# g = graph_ml_loader('input_datas/aerialUTP')
# dataFrame = csv_loader('input_datas/cases-brazil-cities-time')
# data_separator(dataFrame, o_path, g, 'aerial')
# g = graph_ml_loader('input_datas/terrestrial')
# data_separator(dataFrame, o_path, g, 'terrestrial')




_tuple = []
name='terrestrial'
o_path = "output/brazil/"
graph = graph_ml_loader('input_datas/'+name)

mobility = csv_loader('input_datas/filtred/'+name)

degree = sort_by_metric(graph, "degree")
betweenness = sort_by_metric(graph, "betweenness")
betweenness_w = sort_by_metric(graph, "betweenness_w")
strength = sort_by_metric(graph, "strength")

x_axis = [x for x in range(graph.vcount())]

cities_geocodeList = list(mobility['Geocode'])

graph_geocodeList = [x[3] for x in degree]
corresp = correspondence_builder(cities_geocodeList, graph_geocodeList)
spear = mapeador(mobility, degree)
_tuple.append((x_axis, corresp, spear))
processed_data_exporter(x_axis, corresp, o_path+'/csv', name+'k')

graph_geocodeList = [x[3] for x in betweenness]
corresp = correspondence_builder(cities_geocodeList, graph_geocodeList)
spear = mapeador(mobility, betweenness)
_tuple.append((x_axis, corresp, spear))
processed_data_exporter(x_axis, corresp, o_path+'/csv', name+'b')

graph_geocodeList = [x[3] for x in strength]
corresp = correspondence_builder(cities_geocodeList, graph_geocodeList)
spear = mapeador(mobility, strength)
_tuple.append((x_axis, corresp, spear))
processed_data_exporter(x_axis, corresp, o_path+'/csv', name+'st')


graph_geocodeList = [x[3] for x in betweenness_w]
corresp = correspondence_builder(cities_geocodeList, graph_geocodeList)
spear = mapeador(mobility, betweenness_w)
_tuple.append((x_axis, corresp, spear))
processed_data_exporter(x_axis, corresp, o_path+'/csv', name+'b_w')


graphPloter(_tuple, ["$k$", "$b$", "$s$", "$b_{w}$"], name,o_path+'/plots')