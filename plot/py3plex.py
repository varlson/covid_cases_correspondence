from pymnet import *
import igraph as ig

mlt = MultiplexNetwork(couplings='none')

def coordSetter(g):
    coord={}
    for index in range(g.vcount()):
        coord[index]=(g.vs[index]['x'], g.vs[index]['y'])
    return coord

def building(g, layer):

	for tp in g.get_edgelist():
		mlt[tp[0], tp[1], layer, layer]=1



g2010 = ig.Graph.Read_GraphML('2010.GraphML')
# aerial = ig.Graph.Read_GraphML('../input_datas/aerial.GraphML')
# fluvial = ig.Graph.Read_GraphML('../input_datas/fluvial.GraphML')
# terrestrial = ig.Graph.Read_GraphML('../input_datas/terrestrial.GraphML')


# building(terrestrial, 'terrestrial')
# building(fluvial, 'fluvial')

building(g2010, '2010')
# building(aerial, 'aerial')
# building(terrestrial, 'terrestrial')

# coord1 = coorSetter(fluvial)
# coord2 = coorSetter(terrestrial)
# coord3 = coorSetter(fluvial)
coord = coordSetter(g2010)

mlt['2010'].__setattr__('nodeCoords', coord)

fig = draw(
    mlt,
    show=True,
    layout="spring",
    layerColorRule={},
    defaultLayerColor="gray",
    nodeLabelRule={},
    edgeColorRule={"rule":"edgeweight","colormap":"jet","scaleby":0.08}
    ,nodeCoords = {'nodelayerCoords' :coord}             
)


