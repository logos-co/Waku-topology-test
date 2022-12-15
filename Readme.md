This repo contains the scripts to generate various network toplogies for wakukurtosis runs. It can generate networks with specified number of nodes and topics. the network types currently supported is "Newmann" and more is on the way. Use with Python3.

usage: generate_network [-h] [-o <file_name>] [-n <#nodes>] [-t <#topics>]
                        [-T <type>] 
 
Generates and outputs the Waku network conforming to input parameters 
 
optional arguments: 
  -h, --help            show this help message and exit 
  -o <file_name>, --output <file_name> 
                        output json filename for the Waku network 
  -n <#nodes>, --numnodes <#nodes> 
                        number of nodes in the Waku network 
  -t <#topics>, --numtopics <#topics> 
                        number of topics in the Waku network 
  -T <type>, --type <type> 
                        network type of the Waku network 
\
The defaults are: -o "Topology.json" ; -n 1; -t 1; -T "Newmann" 
