#! /usr/bin/env python3

import matplotlib.pyplot as mp
import networkx as nx
import random, math
from random import randint
import json
import argparse,sys

def write_json(filename, data_2_dump):
    json.dump(data_to_dump, open(filename,'w'), indent=2)

def read_json(filename):
    with open(filename) as f:
        js_graph = json.load(f)
    return json_graph.node_link_graph(js_graph)

def draw(H):
    nx.draw(H, pos=nx.kamada_kawai_layout(H), with_labels=True)
    mp.show()
    mp.savefig("topology.png", format="PNG")

def init_arg_parser() :
    # Initialize parser
    parser = argparse.ArgumentParser(
            prog = 'generate_network',
            description = '''Generates and outputs 
            the Waku network conforming to input parameters''',
            epilog = 'Text at the bottom of help')
    # Adding optional arguments with defaults
    parser.add_argument("-o", "--output", 
            default='Topology.json', dest='fname', 
            help='The output json filename for the Waku network', 
            type=str, metavar='<file_name>')
    parser.add_argument("-n", "--numnodes", 
            default=1, dest='num_nodes', 
            help='The number of nodes in the Waku network', 
            type=int, metavar='<#nodes>')
#    parser.add_argument("-e", "--numedges",
#            default=1, dest='num_edges', 
#            help='The number of edges in the Waku network', 
#            type=int, metavar='#edges>')
#    parser.add_argument("-p", "--numparts", 
#            default=1, dest='num_parts', 
#            help='The number of partitions in the Waku network', 
#            type=int, metavar='<#partitions>')
    parser.add_argument("-t", "--numtopics", 
            default=1, dest='num_topics', 
            help='The number of topics in the Waku network', 
            type=int, metavar='<#topics>')
    parser.add_argument("-T", "--type", 
            default="Neumann", dest='nw_type', 
            help='The network type of the Waku network', 
            type=str, metavar='<type>')
    return parser

# https://networkx.org/documentation/stable/reference/generated/networkx.generators.degree_seq.configuration_model.html
def gen_newmann_graph(n):
    #degrees = nx.random_powerlaw_tree_sequence(n, tries=10000)
    degrees = [random.randint(1, n) for i in range(n)]
    if (sum(degrees)) % 2 != 0:         # adjust the degree sum to be even
        degrees[-1] += 1
    G = nx.configuration_model(degrees) # generate the graph
    return G

def gen_topic_string(n):
    rs = ""
    for _ in range(n):
        r = random.randint(65, 65 + 26 - 1) # only letters
        rs += (chr(r))                      # append the char generated
    return rs

def get_random_sublist(topics):
    n = len(topics)
    lo = randint(0, n - 1)
    hi = randint(lo + 1, n)
    sublist = []
    for i in range(lo, hi):
        sublist.append(topics[i])
    return sublist
#def get_sublists(length):
#    return [lst[i:i + length] for i in range(len(lst) - length + 1)]




args = init_arg_parser().parse_args()
#arguments to generate the nwtworks
fname = args.fname
num_nodes = args.num_nodes
#num_edges = args.num_edges
#num_parts = args.num_parts
num_topics = args.num_topics
nw_type = args.nw_type


# waku defaults
prefix = "waku_"
node_number = 0
ports_shifted = 0
topics = []

# generate  the network
G = nx.empty_graph()
if nw_type == "Neumann":
    G = gen_newmann_graph(num_nodes)
else: 
    print(nw_type +": Unsupported Network Type")
    sys.exit(1)

# pre-process the network
G = nx.Graph(G)                     # prune out parallel/multi edges
G.remove_edges_from(nx.selfloop_edges(G))   # Removing self-loops

# generate the topics - uppercase alphabetic strings
topic_len = int(math.log(num_topics)/math.log(26)) + 1
topics = {}
for i in range(num_topics):
    topics[i] = "topic_" + gen_topic_string(topic_len)

# Labeling nodes to match waku containers
mapping = {}
for i in range(num_nodes):
    mapping[i] = prefix + str(i)
H = nx.relabel_nodes(G, mapping)

# Generate the dump data
data_to_dump = {}
for node in H.nodes:
    data_to_dump[node] = {}
    data_to_dump[node]["ports-shift"] = ports_shifted
    ports_shifted += 1
    data_to_dump[node]["topics"] = get_random_sublist(topics)
    data_to_dump[node]["static-nodes"] = []
    for edge in H.edges(node):
        data_to_dump[node]["static-nodes"].append(edge[1])

# dump the network to the json file
write_json(fname, data_to_dump)
draw(H)




