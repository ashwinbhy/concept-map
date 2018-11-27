import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout
import os
from networkx.drawing.nx_agraph import write_dot



def GenerateGraphvizGraph(relList):
    G = nx.DiGraph()

    for r in relList:
        G.add_edges_from([(r[0].lower(), r[2].lower())], label=r[1])

    write_dot(G, "grid.dot")
    os.system('dot -Tpng grid.dot -o concept_map.png')

def GenerateGraph(relList):
    G = nx.DiGraph()

    for r in relList:
        G.add_edges_from([(r[0], r[2])], r=r[1],length=300)

    edge_labels = nx.get_edge_attributes(G,'r')
    pos = graphviz_layout(G)
    nx.draw(G,pos,node_size=1200,with_labels=True)
    nx.draw_networkx_edge_labels(G,pos, edge_labels = edge_labels)


    plt.draw()
    plt.show()