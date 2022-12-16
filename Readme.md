This repo contains the scripts to generate various network topologies for the wakukurtosis runs. 

## generate_network.py
run_kurtosis_tests.sh will kurtosis on a set of json files given under a directory. It trquires two params. First is the directory of json files. Second is the github root/prefix of the kurtosis module you run the tests under.</br>

usage: ./run_kurtosis_tests.sh <input dir> <repo prefix> </br>

Running this script is somewhat complicated; so follow the following instructions to a dot.

#### step 0)
  symlink this script and the main.star to the root of ur kurtosis module.</br>
#### step 1)
  put the json files you want to run kurtosis in a directory</br>
#### step 2)
   copy that entire directory to the root of your kurtosis module</br>
   !!! WARNING: symlinking the directory will NOT work !!!</br>
####step 3)
   run this script in the kurtosis module root dir of ur module</br>




## gen_jsons.sh
gen_jsons.sh can generate given number of Waku networs and outputs them to a directory. Please make sure that the output directory exists; both relative and absolute paths work. The parameters are generated at random; edit the MIN and MAX for finer control. The script requires bc & /dev/urandom.<br>

usage: ./gen_jsons.sh <output dir> <#json files needed> </br>

## generate_network.py
generate_network.py can generate networks with specified number of nodes and topics. the network types currently supported is "configuration_model" and more is on the way. Use with Python3.

usage: generate_network [-h] [-o <file_name>] [-n <#nodes>] [-t <#topics>]
                        [-T <type>] <br>
</br>
Generates and outputs the Waku network conforming to input parameters<br>
</br>
optional arguments:</br>
&emsp;  -h, --help            show this help message and exit</br>
&emsp;  -o <file_name>, --output <file_name> output json filename for the Waku network </br>
&emsp;  -n <#nodes>, --numnodes <#nodes> number of nodes in the Waku network </br>
&emsp;  -t <#topics>, --numtopics <#topics> number of topics in the Waku network </br>
&emsp;  -T <type>, --type <type>  network type for the Waku network </br>
&emsp;  -p <#partitions>, --numparts <#partitions> number of partitions in the Waku network
</br>
The defaults are: -o "Topology.json"; -n 1; -t 1; -p 1; -T
"configuration_model"
</br>
