#!/bin/sh

# -> symlink - ln -s source/dir .

# step 0)
#  symlink this script and the main.star to the root of ur kurtosis module.
#
# step 1)
#  put the json files you want to run kurtosis in a directory
#
# step 2)
#   copy that entire directory to the root of your kurtosis module
#   !!! WARNING: symlinking the directory will NOT work !!!
#
# step 3)
#   run this script in the kurtosis module root dir of ur module


if [ "$#" -ne 2 ] || ! [ -d "$1" ]; then
  echo "usage: $0 <input dir> <repo prefix>" >&2
  exit 1
fi

path=$1
repo=$2
echo "Ok, will run kurtosis on all .json networks under '$path'."

for json in "$path"/*.json
do
 cmd="kurtosis run . --args '{\"json_nw_name\": \"$repo/$json\"}'"
 echo $cmd
 eval $cmd
done

echo $repo, $path, "DONE!"
