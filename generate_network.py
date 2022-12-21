#! /usr/bin/env python3

import matplotlib.pyplot as plt
import networkx as nx
import random, math
import json
import argparse, os, sys

# dump to json file
def write_json(filename, data_2_dump):
    json.dump(data_2_dump, open(filename,'w'), indent=2)


# has trouble with non-integer/non-hashable keys 
def read_json(filename):
    with open(filename) as f:
        jdata = json.load(f)
    return nx.node_link_graph(jdata)


# draw the network and output the image to a file
def draw(fname, H):
    nx.draw(H, pos=nx.kamada_kawai_layout(H), with_labels=True)
    plt.savefig(os.path.splitext(fname)[0] + ".png", format="png")
    plt.show()


# Initialize parser, set the defaults, and extract the options
def get_options():
    parser = argparse.ArgumentParser(
            prog = 'generate_network',
            description = '''Generates and outputs 
            the Waku network conforming to input parameters''',
            epilog = '''Defaults: -o "Topology.json"; 
            -n 1; -t 1; -p 1; -T "configuration_model"
            Supported nw types "configuration_model", "scalefree",
            "newman_watts_strogatz"''')
    parser.add_argument("-o", "--output", 
            default='Topology.json', dest='fname', 
            help='output json filename for the Waku network', 
            type=str, metavar='<file_name>')
    parser.add_argument("-n", "--numnodes", 
            default=1, dest='num_nodes', 
            help='number of nodes in the Waku network', 
            type=int, metavar='<#nodes>')
    parser.add_argument("-t", "--numtopics", 
            default=1, dest='num_topics', 
            help='number of topics in the Waku network', 
            type=int, metavar='<#topics>')
    parser.add_argument("-T", "--type", 
            default="configuration_model", dest='nw_type', 
            help='network type of the Waku network', 
            type=str, metavar='<type>')
    parser.add_argument("-p", "--numparts", 
            default=1, dest='num_partitions', 
            help='The number of partitions in the Waku network', 
            type=int, metavar='<#partitions>')
#    parser.add_argument("-e", "--numedges",
#            default=1, dest='num_edges', 
#            help='The number of edges in the Waku network', 
#            type=int, metavar='#edges>')
    return parser.parse_args()


# Generate a random string (UC chars) of len n
def generate_topic_string(n):
    rs = ""
    for _ in range(n):
        r = random.randint(65, 65 + 26 - 1) # only letters
        rs += (chr(r))                      # append the char generated
    return rs


# Generate the topics - UC chars prefixed by "topic"
def generate_topics(num_topics):
    topics = []
    base = 26
    topic_len = int(math.log(num_topics)/math.log(base)) + 1
    topics = {}
    for i in range(num_topics):
        topics[i] = "topic_" + generate_topic_string(topic_len)
    return topics


# Get a random sub-list of topics
def get_random_sublist(topics):
    n = len(topics)
    lo = random.randint(0, n - 1)
    hi = random.randint(lo + 1, n)
    sublist = []
    for i in range(lo, hi):
        sublist.append(topics[i])
    return sublist


# Network Types
# https://networkx.org/documentation/stable/reference/generated/networkx.generators.degree_seq.configuration_model.html
def generate_config_model(n):
    #degrees = nx.random_powerlaw_tree_sequence(n, tries=10000)
    degrees = [random.randint(1, n) for i in range(n)]
    if (sum(degrees)) % 2 != 0:         # adjust the degree to even
        degrees[-1] += 1
    return nx.configuration_model(degrees) # generate the graph


def generate_scalefree_graph(n):
    return  nx.scale_free_graph(n)


# n must be larger than k
def generate_newman_watts_strogatz_graph(n):
    return nx.newman_watts_strogatz_graph(n, 12, 0.5)


# Generate the network from nw type
def generate_network(num_nodes, nw_type, prefix):
    G = nx.empty_graph()
    if nw_type == "configuration_model":
        G = generate_config_model(num_nodes)
    elif nw_type == "scalefree":
        G = generate_scalefree_graph(num_nodes)
    elif nw_type == "newman_watts_strogatz":
        G = generate_newman_watts_strogatz_graph(num_nodes) 
    else: 
        print(nw_type +": Unsupported network type")
        sys.exit(1)
    H = postprocess_network(G, prefix)
    return H


# used by generate_dump_data, *ought* to be global to handle partitions
ports_shifted = 0
def postprocess_network(G, prefix):
    G = nx.Graph(G)         # prune out parallel/multi edges
    G.remove_edges_from(nx.selfloop_edges(G))   # Removing self-loops
    # Labeling nodes to match waku containers
    mapping = {}
    for i in range(len(G)):
        mapping[i] = prefix + str(i)
    return nx.relabel_nodes(G, mapping)


# Generate dump data from the network and topics
def generate_dump_data(H, topics):
    data_to_dump = {}
    global ports_shifted
    for node in H.nodes:
        data_to_dump[node] = {}
        data_to_dump[node]["ports-shift"] = ports_shifted
        ports_shifted += 1
        data_to_dump[node]["topics"] = get_random_sublist(topics)
        data_to_dump[node]["static-nodes"] = []
        for edge in H.edges(node):
            data_to_dump[node]["static-nodes"].append(edge[1])
    return data_to_dump


def main():
    #extract the CLI arguments and assign params
    options = get_options()
    fname = options.fname
    num_nodes = options.num_nodes
    num_topics = options.num_topics
    nw_type = options.nw_type
    prefix = "waku_"     
    num_partitions = options.num_partitions
    #num_edges = options.num_edges    ## need to control num_edges?

    if num_partitions > 1:
        print("-p",num_partitions,
                "Sorry, we do not yet support partitions")
        sys.exit(1)

    # Generate the network and postprocess it
    H = generate_network(num_nodes, nw_type, prefix)
    # Generate the topics
    topics = generate_topics(num_topics)
    # Generate the dump data
    dump_data = generate_dump_data(H, topics)
    # Dump the network in a json file
    write_json(fname, dump_data)
    # Display the graph
    #draw(fname, H)


if __name__ == "__main__":
    main()
