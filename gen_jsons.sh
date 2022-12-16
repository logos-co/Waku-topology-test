#!/bin/sh


#max and min for topics and num nodes
MIN=5
MAX=100

#requires bc
getrand(){
  orig=$(od -An -N1 -i /dev/urandom)
  range=`echo "$MIN + ($orig % ($MAX - $MIN + 1))" | bc`
  RANDOM=$range
}

getrand1(){
  orig=$(od -An -N1 -i /dev/urandom)
  range=`echo "$MIN + ($orig % ($MAX - $MIN + 1))" | bc`
  return range
  #getrand1  # call the fun and use the return value
  #n=$? 
}

if [ "$#" -ne 2 ] || [ $2 -le 0 ] || ! [ -d "$1" ]; then
  echo "Usage: $0 <output dir> <#json files needed>" >&2
  exit 1
fi

path=$1
nfiles=$2

echo "Ok, will generate $nfiles networks & put them  under '$path'."

prefix=$path"/WakuNet_"
suffix=".json"

for i in $(seq $nfiles)
do
  getrand
  n=$((RANDOM+1))
  getrand 
  t=$((RANDOM+1))
  fname=$prefix$i$suffix
  nwtype="configuration_model"
  $(./generate_network.py -n $n -t $t -T $nwtype -o $fname)
  echo "#$i\tn=$n\tt=$t\tT=$nwtype\to=$fname"
done
