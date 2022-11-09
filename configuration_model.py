import matplotlib.pyplot
import networkx as nx
import random
import json

# Do we want a single graph, or we can have different hubs.
# We don't have a power-law distribution, right?
#    sequence = nx.random_powerlaw_tree_sequence(10, tries=5000)

name = "waku_"
node_number = 0

ports_shifted = 0

shared_topic = "test"
nodes_to_instantiate = 50

data_to_dump = {}

degrees = [random.randint(1, 9) for i in range(nodes_to_instantiate)]

# Sanity check, as degrees must be even
if (sum(degrees)) % 2 != 0:
    degrees[-1] += 1

# https://networkx.org/documentation/stable/reference/generated/networkx.generators.degree_seq.configuration_model.html
G = nx.configuration_model(degrees)
# Create it as a normal graph instead multigraph (without parallel edges)
G = nx.Graph(G)
# Removing self-loops
G.remove_edges_from(nx.selfloop_edges(G))

mapping = {}
for i in range(nodes_to_instantiate):
    mapping[i] = name + str(node_number)
    node_number += 1

# Labeling nodes to match waku containers
H = nx.relabel_nodes(G, mapping)

# Add information to de data
for node in H.nodes:
    data_to_dump[node] = {}
    data_to_dump[node]["ports-shift"] = ports_shifted
    ports_shifted += 1
    data_to_dump[node]["topics"] = shared_topic
    data_to_dump[node]["static-nodes"] = []
    for edge in H.edges(node):
        data_to_dump[node]["static-nodes"].append(edge[1])


with open('topology.json', 'w') as f:
    json.dump(data_to_dump, f)

nx.draw(H, pos=nx.kamada_kawai_layout(H), with_labels=True)
matplotlib.pyplot.show()
matplotlib.pyplot.savefig("topology.png", format="PNG")
