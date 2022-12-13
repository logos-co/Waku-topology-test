import matplotlib.pyplot
import networkx as nx
import random
import json
import argparse, sys


# Initialize parser
parser = argparse.ArgumentParser(
                    prog = 'generate_network',
                    description = 'Generates and outputs the Waku network conforming to input parameters',
                    epilog = 'Text at the bottom of help')

# Adding optional arguments with defaults
parser.add_argument("-o", "--output", default='Topology.json', dest='fname', help='The output json filename for the Waku network', type=str, metavar='<file_name>')
parser.add_argument("-n", "--numnodes", default=1, dest='num_nodes', help='The number of nodes in the Waku network', type=int, metavar='<#nodes>')
parser.add_argument("-e", "--numedges", default=1, dest='num_edges', help='The number of edges in the Waku network', type=int, metavar='#edges>')
parser.add_argument("-p", "--numparts", default=1, dest='num_parts', help='The number of partitions in the Waku network', type=int, metavar='<#partitions>')
parser.add_argument("-t", "--numtopics", default=1, dest='num_topics', help='The number of topics in the Waku network', type=int, metavar='<#topics>')
parser.add_argument("-T", "--type", default="waku", dest='nw_type', help='The network type of the Waku network', type=str, metavar='<type>')
#parser.add_argument(help = "Show Output")
args = parser.parse_args()

#arguments
fname = args.fname
num_nodes = args.num_nodes
num_edges = args.num_edges
num_parts = args.num_parts
num_topics = args.num_topics
nw_type = args.nw_type

#print ("ARGS:", fname, num_nodes, num_edges, num_parts, num_topics, nw_type)

# Do we want a single graph, or we can have different hubs.
# We don't have a power-law distribution, right?
#    sequence = nx.random_powerlaw_tree_sequence(10, tries=5000)
# waku defaults

prefix = "waku_"
node_number = 0
ports_shifted = 0
shared_topic = "test"
data_to_dump = {}

degrees = [random.randint(1, 9) for i in range(num_nodes)]

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
for i in range(num_nodes):
    mapping[i] = prefix + str(node_number)
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


with open(fname, 'w') as f:
    json.dump(data_to_dump, f)

nx.draw(H, pos=nx.kamada_kawai_layout(H), with_labels=True)
matplotlib.pyplot.show()
matplotlib.pyplot.savefig("topology.png", format="PNG")
