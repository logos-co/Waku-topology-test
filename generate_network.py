#! /usr/bin/env python3

import matplotlib.pyplot as plt
import networkx as nx
import random, math
import json
import sys, os
import string
import typer
from enum import Enum

# Consts
class networkType(Enum):
    configmodel = "CONFIGMODEL"
    scalefree = "SCALEFREE"                     # power law
    newmanwattsstrogatz = "NEWMANWATTSSTROGATZ" # mesh, smallworld
    barbell = "BARBELL"                         # partition
    balancedtree = "BALANCEDTREE"               # committees?
    star = "STAR"                               # spof

class nodeType(Enum):
    desktop = "DESKTOP"
    mobile = "MOBILE"

NW_DATA_FNAME = "network_data.json"
PREFIX = "waku_"

### I/O related fns ###########################################################

# Dump to a json file
def write_json(dirname, json_dump):
    fname = os.path.join(dirname, NW_DATA_FNAME)
    with open(fname, "w") as f:
        json.dump(json_dump, f, indent=2)


def write_toml(dirname, node_name, toml):
    fname = os.path.join(dirname, f"{node_name}.toml")
    with open(fname, "w") as f:
        f.write(toml)


# Draw the network and output the image to a file
def draw(dirname, H):
    nx.draw(H, pos=nx.kamada_kawai_layout(H), with_labels=True)
    fname = os.path.join(dirname, NW_DATA_FNAME)
    plt.savefig(f"{os.path.splitext(fname)[0]}.png", format="png")
    plt.show()


# Has trouble with non-integer/non-hashable keys 
def read_json(fname):
    with open(fname) as f:
        jdata = json.load(f)
    return nx.node_link_graph(jdata)

def exists_and_nonempty(dirname):
    if not os.path.exists(dirname):
        return False
    elif not os.path.isfile(dirname) and os.listdir(dirname):
        print(f"{dirname}: exists and not empty")
        return True
    elif os.path.isfile(dirname):
        print(f"{dirname}: exists but not a directory")
        return True
    else:
        return False

### topics related fns ###########################################################

# Generate a random string of upper case chars
def generate_random_string(n):
    return "".join(random.choice(string.ascii_uppercase) for _ in range(n))


# Generate the topics - topic followed by random UC chars - Eg, topic_XY"
def generate_topics(num_topics):
    topic_len = int(math.log(num_topics)/math.log(26)) + 1  # base is 26 - upper case letters
    topics = {i: f"topic_{generate_random_string(topic_len)}" for i in range(num_topics)}
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


### network processing related fns ###########################################################

# Network Types
def generate_config_model(n):
    #degrees = nx.random_powerlaw_tree_sequence(n, tries=10000)
    degrees = [random.randint(1, n) for i in range(n)]
    if (sum(degrees)) % 2 != 0:         # adjust the degree to be even
        degrees[-1] += 1
    return nx.configuration_model(degrees) # generate the graph


def generate_scalefree_graph(n):
    return  nx.scale_free_graph(n)


# n must be larger than k=D=3
def generate_newmanwattsstrogatz_graph(n):
    return nx.newman_watts_strogatz_graph(n, 3, 0.5)


def generate_barbell_graph(n):
    return nx.barbell_graph(int(n/2), 1)


def generate_balanced_tree(n, fanout=3):
    height = int(math.log(n)/math.log(fanout))
    return nx.balanced_tree(fanout, height)


def generate_star_graph(n):
    return nx.star_graph(n)


# Generate the network from nw type
def generate_network(n, nw_type):
    switch = {
        networkType.configmodel: generate_config_model(n),
        networkType.scalefree: generate_scalefree_graph(n),
        networkType.newmanwattsstrogatz: generate_newmanwattsstrogatz_graph(n), 
        networkType.barbell: generate_barbell_graph(n),
        networkType.balancedtree: generate_balanced_tree(n), 
        networkType.star: generate_star_graph(n)
    }
    return postprocess_network(switch.get(nw_type))


# Label the generated network with prefix
def postprocess_network(G):
    G = nx.Graph(G)                             # prune out parallel/multi edges
    G.remove_edges_from(nx.selfloop_edges(G))   # remove the self-loops
    mapping = {i: f"{PREFIX}{i}" for i in range(len(G))}
    return nx.relabel_nodes(G, mapping)         # label the nodes


### file format related fns ###########################################################

#Generate per node toml configs
def generate_toml(topics, node_type=nodeType.desktop):
    topic_str =  " ". join(get_random_sublist(topics))    # topics as a space separated string
    switch = {
        nodeType.desktop: "rpc-admin = true\nkeep-alive = true\n",
        nodeType.mobile: "rpc-admin = true\nkeep-alive = true\n"
    }
    toml = f"{switch.get(node_type)}topics = \"{topic_str}\"\n"
    return toml


# Generates network-wide json and per-node toml and writes them 
def generate_and_write_files(dirname, num_topics, H): 
    topics = generate_topics(num_topics)
    json_dump = {}
    for node in H.nodes:
        write_toml(dirname, node, generate_toml(topics))        # per node toml
        json_dump[node] = {}
        json_dump[node]["static-nodes"] = []
        for edge in H.edges(node):
            json_dump[node]["static-nodes"].append(edge[1])
    write_json(dirname, json_dump)                              # network wide json


### the main ###########################################################
def main(
        dirname: str = "Waku", num_nodes: int = 3, num_topics: int = 1, 
        nw_type: networkType = "NEWMANWATTSSTROGATZ", 
        node_type: nodeType = "DESKTOP",
        num_partitions: int = 1):

    if num_partitions > 1:
        print("-p",num_partitions, "Sorry, we do not yet support partitions")
        sys.exit(1)

    # Generate the network and do post-process 
    G = generate_network(num_nodes, nw_type)
    postprocess_network(G)

    # Generate file format specific data structs and write the files; optionally, draw the network
    if exists_and_nonempty(dirname) :
        sys.exit(1)
    os.makedirs(dirname, exist_ok=True)

    generate_and_write_files(dirname, num_topics, G)
    draw(dirname, G)


if __name__ == "__main__":
    typer.run(main)
