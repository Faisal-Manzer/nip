#!/bin/bash

script_directory=$(dirname $BASH_SOURCE)
pwd=$(pwd)
filename="$pwd/.niptemp"

python3 ${script_directory}/nip_app.py $@
if [[ $? -eq 0 ]]
then
    if [[ -f ${filename} ]] ; then
        while read p; do
            $p
        done < ${filename}
    fi
fi
removed_file=$(rm ${filename})
