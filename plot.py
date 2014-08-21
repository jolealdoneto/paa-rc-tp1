import networkx as nx
import matplotlib.pyplot as plt
from pymongo import MongoClient
import json

client = MongoClient()
db = client.vk_crawl
nodes = db.nodes
edges = db.edges
iedges = db.i_edges

G = nx.Graph()

all_nodes = nodes.find()
uid_nodes = [int(node['uid']) for node in all_nodes.clone()]
G.add_nodes_from(uid_nodes)
for node in all_nodes:
    node_edges = edges.find({ 'eid': { '$regex': str(node['uid']) } })
    #print node['uid'], node_edges.count()
    for node in node_edges:
        node_tuple = json.loads(node['eid'].replace("'", '"'))
        node_tuple = [int(node_tuple[0]), int(node_tuple[1])]

        if node_tuple[0] in uid_nodes and node_tuple[1] in uid_nodes:
            G.add_edge(int(node_tuple[0]), int(node_tuple[1]))

# draw graph
#pos = nx.spring_layout(G)
#nx.draw(G, pos = pos, node_size = 120, with_labels=False)
#labels = {}
#for id in uid_nodes:
#    labels[id] = id
#nx.draw_networkx_labels(G,pos,labels,font_size=16, font_color='g')
#
### show graph
#plt.show()

print nx.clustering(G)

