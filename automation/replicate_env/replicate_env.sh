#!/usr/bin/env bash

echo "test"

grep -riH stage .|cut -d':' -f1 | sort -t: -u -k1,1 > file.txt

for file in $(cat file.txt); do sed -i '' 's/stage/preprod/g' $file; done
