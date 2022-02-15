from util import *
import multinetx as mx
import networkx as nx
import matplotlib.pyplot as plt

from networkx.drawing.nx_agraph import graphviz_layout
from importlib import reload 

N=100

g1 = ig.Graph.Read_GraphML('input_datas/aerial.GraphML')
g2 = ig.Graph.Read_GraphML('input_datas/fluvial.GraphML')
g3 = ig.Graph.Read_GraphML('input_datas/terrestrial.GraphML')

gx1 = g1.to_networkx()
gx2 = g2.to_networkx()
gx3 = g3.to_networkx()

mg = mx.MultilayerGraph(list_of_layers=[gx2, gx1])


# fig = plt.figure(figsize=(30, 10))

# ax1 = fig.add_subplot(121)

# pos = mx.get_position(mg,mx.fruchterman_reingold_layout(gx3),layer_vertical_shift=0.4,layer_horizontal_shift=0.4,proj_angle=47)
# mx.draw_networkx(mg,pos=pos,ax=ax1,node_size=10,with_labels=False,edge_cmap=plt.cm.jet_r)

# plt.show()


fig = plt.figure(figsize=(15,5))
ax2 = fig.add_subplot(122)
ax2.axis('off')
ax2.set_title('edge colored network')
pos = graphviz_layout(gx1,prog='dot') 
mx.draw_networkx(mg,pos=pos,ax=ax2,node_size=50,with_labels=False,
				 edge_color=[mg[a][b]['weight'] for a,b in mg.edges()],
				 edge_cmap=plt.cm.jet_r)
plt.show()