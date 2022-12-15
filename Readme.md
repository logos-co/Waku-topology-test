This repo contains the scripts to generate various network toplogies for wakukurtosis runs. It can generate networks with specified number of nodes and topics. the network types currently supported is "Newmann" and more is on the way. Use with Python3.

usage: generate_network [-h] [-o <file_name>] [-n <#nodes>] [-t <#topics>]
                        [-T <type>] <br>
</br>
Generates and outputs the Waku network conforming to input parameters<br>
</br>
optional arguments:</br>
  -h, --help            show this help message and exit</br>
  -o <file_name>, --output <file_name> /<br>
                        output json filename for the Waku network </br>
  -n <#nodes>, --numnodes <#nodes> </br>
                        number of nodes in the Waku network </br>
  -t <#topics>, --numtopics <#topics> </br>
                        number of topics in the Waku network </br>
  -T <type>, --type <type> </br>
                        network type of the Waku network </br>
</br>
The defaults are: -o "Topology.json" ; -n 1; -t 1; -T "Newmann"</br> 
