#!/bin/bash

# Download all PDFs listed in links.txt and rename it to the name indicated in
# this file. If the file was already downloaded it will not download again.

RES_FILE="links.txt"
SEPARATOR="	"

while read line; do
	title="${line%%$SEPARATOR*}.pdf"
	url=${line##*$SEPARATOR}

	if [ -e "${title}" ] ; then
		echo "\"${title}\" exists, it will not download."
	else
		wget -nv --show-progress $url -O "${title}"
	fi
done < $RES_FILE
