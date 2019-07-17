#!/bin/bash

python $1 > a.py
mv ./a.py /mnt/hgfs/ctf/ctf_games/
echo "check /mnt/hgfs/ctf/ctf_games/a.py"

