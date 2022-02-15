from pymnet import *
import igraph  as ig

mlt = MultiplexNetwork()



def idSetter(g1,g2, g3):
    
    g1.vs['idef'] = [x for x in range(g1.vcount())]
    index=96
    
    idef = []
    
    for geo in g2.vs['geocode']:
        if geo in g1.vs['geocode']:
            ind = g1.vs['geocode'].index(geo)
            idef.append(ind)
        else:
            idef.append(index)
            index+=1
    g2.vs['idef'] = idef
    
    idef=[]
    
    index=219
    
    for geo in g3.vs['geocode']:
        if geo in g1.vs['geocode']:
            ind = g1.vs['geocode'].index(geo)
            idef.append(ind)
        elif geo in g2.vs['geocode']:
            ind = g2.vs['geocode'].index(geo)
            temp = g2.vs[ind]['idef']
            idef.append(temp)
        else:
            idef.append(index)
            index+=1    
    
    g3.vs['idef'] = idef


def uniqGeocodeExtractor(graphList):
    uniq=[]
    
    for graph in graphList:
        for geocode in graph.vs['geocode']:
            if geocode not in uniq:
                uniq.append(geocode)
    return uniq



def colorizer(color, layer):
    colorDict={}

    for node in mlt.iter_nodes([layer]):
        if mlt[node, layer].deg() == 0:
            colorDict.update({(node, layer): 'gray'})
        else:
            colorDict.update({(node, layer): color})
    return colorDict
 
def edgeSetter(g, lay):  
    for src, trg in g.get_edgelist():        
        source = g.vs['idef'][src]
        target = g.vs['idef'][trg]        
        mlt[source, target, lay, lay] = 1



def coordMaker(g, uniqList):
    coordDict ={}
    
    for geo in uniqList:
        if geo in g.vs['geocode']:
            index = g.vs['geocode'].index(geo)
            X = g.vs['X'][index]
            Y = g.vs['Y'][index]
            coordDict[g.vs[index]['idef']]= (X, Y)
    return coordDict


aerial = ig.Graph.Read_GraphML('aerial.GraphML')
fluvial =ig.Graph.Read_GraphML('fluvial.GraphML')
terrestrial = ig.Graph.Read_GraphML('terrestrial.GraphML')



aerial_l='aerial'
fluvial_l='fluvial'
terrestrial_l='terrestrial'


idSetter(aerial, fluvial, terrestrial)


edgeSetter(aerial, aerial_l) 
edgeSetter(fluvial, fluvial_l) 
edgeSetter(terrestrial, terrestrial_l) 

colorDict={}
colorDict.update(colorizer('#53c7fc', aerial_l))
colorDict.update(colorizer('#0769ab', fluvial_l))
colorDict.update(colorizer('#11059c', terrestrial_l))

uniq = uniqGeocodeExtractor([aerial, fluvial, terrestrial])
coord = coordMaker(aerial, aerial.vs['geocode'])
coord.update(coordMaker(fluvial, uniq))
coord.update(coordMaker(terrestrial, uniq))


fig = draw(mlt, nodeCoords=coord, nodeLabelRule={},
     defaultLayerColor="#bab6b6", defaultEdgeColor="#050505",  defaultEdgeWidth=0.05,
     nodeSizeRule={"rule":"degree","propscale":0.005}, nodeColorDict=colorDict, figsize=(18.5, 10.5))
fig.savefig('multiplex_aerial_fluvial_terrestrial.png')

