This repo contains the scripts to generate different network models for wakukurtosis runs. 

## run_kurtosis_tests.sh
run_kurtosis_tests.sh will run kurtosis on a set of json files in a directory. It requires two arguments. First is a directory containing json files; other file types in the directory are ignored. Second is the github root/prefix of the kurtosis module you run the tests under.</br>

> usage: ./run_kurtosis_tests.sh <input_dir> <repo_prefix> </br>

Running this script is somewhat complicated; so follow the following instructions to a dot. You **WILL** require the main.star provided here. The main.star reads a input json and instantiates Waku nodes accordingly. The runs are repeated for each of the input json files under the specified directory.

#### step 0)
  symlink  run_kurtosis_tests.sh to the root directory of your kurtosis module.</br>
#### step 1)
  backup the your kurtosis module's own main.star. copy the main.star provided here to the root directory of your kurtosis module.</br>
     !!! WARNING: symlinking the main.star will NOT work !!!</br>
#### step 3)
  put all the json files you want to use in a directory. Call it *Foo*</br>
#### step 3)
   copy the *Foo* directory to the root of your kurtosis module</br>
   !!! WARNING: symlinking the directory will NOT work !!!</br>
#### step 4)
   run this script in the root directory of the kurtosis module. provide the directory (*Foo*) and the github root/prefix of the kurtosis module as arguments to the script</br>


## gen_jsons.sh
gen_jsons.sh can generate given number of Waku networs and outputs them to a directory. Please make sure that the output directory exists; both relative and absolute paths work. The Wakunode parameters are generated at random; edit the MIN and MAX for finer control. The script requires bc & /dev/urandom.<br>

> usage: ./gen_jsons.sh <output_dir> <#json files needed> </br>

## generate_network.py
generate_network.py can generate networks with specified number of nodes and topics. the network types currently supported is "configuration_model" and more are on the way. Use with Python3. Comment out the `#draw(fname, H)` line to visualise the generate graph.

> usage: generate_network [-h] [-o <file_name>] [-n <#nodes>] [-t <#topics>]
                        [-T <type>] <br>
>> </br>
>> Generates and outputs the Waku network conforming to input parameters<//br>
>> </br>
>> optional arguments:</br>
>> &emsp;  -h, --help            show this help message and exit</br>
>> &emsp;  -o <file_name>, --output <file_name> output json filename for the Waku network </br>
>> &emsp;  -n <#nodes>, --numnodes <#nodes> number of nodes in the Waku network </br>
>> &emsp;  -t <#topics>, --numtopics <#topics> number of topics in the Waku network </br>
>> &emsp;  -T <type>, --type <type>  network type for the Waku network </br>
>> &emsp;  -p <#partitions>, --numparts <#partitions> number of partitions in the Waku network</br>
  >></br>
>>The defaults are: -o "Topology.json"; -n 1; -t 1; -p 1; -T "configuration_model"</br>
